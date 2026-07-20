// Admin panel E2E — login, dashboard, navigatsiya va CRUD oqimlari.
const { test, expect } = require('@playwright/test');

const ADMIN = { username: 'e2e_admin', password: 'e2e-Pass-123!' };

// Har bir testdan oldin panelga kiramiz
async function login(page) {
  await page.goto('/panel/');
  await page.locator('#login-username').fill(ADMIN.username);
  await page.locator('#login-password').fill(ADMIN.password);
  await page.locator('#login-btn').click();
  // login muvaffaqiyatli bo'lsa #app ko'rinadi, #login-screen yashirinadi
  await expect(page.locator('#app')).toBeVisible({ timeout: 10_000 });
}

test.describe('Panel autentifikatsiya', () => {
  test('Noto\'g\'ri parol xato ko\'rsatadi', async ({ page }) => {
    await page.goto('/panel/');
    await page.locator('#login-username').fill(ADMIN.username);
    await page.locator('#login-password').fill('notogri-parol');
    await page.locator('#login-btn').click();
    await expect(page.locator('#login-error')).toBeVisible({ timeout: 10_000 });
    // App ko'rinmasligi kerak
    await expect(page.locator('#app')).toBeHidden();
  });

  test('To\'g\'ri login dashboardga olib kiradi', async ({ page }) => {
    await login(page);
    await expect(page.locator('[data-page="dashboard"]')).toBeVisible();
  });
});

test.describe('Panel navigatsiya', () => {
  test.beforeEach(async ({ page }) => login(page));

  const SECTIONS = ['faculty', 'teachers', 'news', 'events', 'leadership', 'departments', 'centers', 'pages'];

  for (const section of SECTIONS) {
    test(`"${section}" bo'limiga o'tish ishlaydi`, async ({ page }) => {
      const nav = page.locator(`[data-page="${section}"]`);
      await expect(nav).toBeVisible();
      await nav.click();
      // URL hash yangilanishi kerak
      await expect(page).toHaveURL(new RegExp(`#${section}`));
    });
  }
});

test.describe('Panel CRUD oqimi (API orqali, brauzer sessiyasida)', () => {
  test.beforeEach(async ({ page }) => login(page));

  test('Yo\'nalish qo\'shish -> ro\'yxatda ko\'rinadi -> o\'chirish', async ({ page }) => {
    const name = `E2E Yo'nalish ${Date.now()}`;

    // CREATE — panel API'ga sessiya cookie'lari bilan so'rov (CSRF bilan)
    const created = await page.evaluate(async (facName) => {
      const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
      const fd = new FormData();
      fd.append('name', facName);
      fd.append('description', 'E2E test tavsifi');
      fd.append('is_active', 'true');
      const r = await fetch('/panel/api/faculty/', {
        method: 'POST', body: fd, headers: { 'X-CSRFToken': csrf },
      });
      return { status: r.status, body: await r.json() };
    }, name);
    expect(created.status).toBe(200);
    expect(created.body.success).toBe(true);
    const pk = created.body.data.id;

    // READ — ro'yxatda bor
    const listed = await page.evaluate(async () => {
      const r = await fetch('/panel/api/faculty/');
      return r.json();
    });
    expect(listed.data.some(f => f.id === pk)).toBe(true);

    // DELETE
    const deleted = await page.evaluate(async (id) => {
      const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
      const r = await fetch(`/panel/api/faculty/${id}/`, {
        method: 'DELETE', headers: { 'X-CSRFToken': csrf },
      });
      return { status: r.status };
    }, pk);
    expect(deleted.status).toBe(200);
  });

  test('Statistika endpointi raqamlar qaytaradi', async ({ page }) => {
    const stats = await page.evaluate(async () => {
      const r = await fetch('/panel/api/stats/');
      return r.json();
    });
    expect(stats.success).toBe(true);
    expect(typeof stats.data.news).toBe('number');
    expect(typeof stats.data.teachers).toBe('number');
  });
});

test.describe('Auth bo\'lmasa panel API 403', () => {
  test('Anonim so\'rov bloklanadi', async ({ page }) => {
    await page.goto('/panel/');
    const res = await page.evaluate(async () => {
      const r = await fetch('/panel/api/stats/');
      return r.status;
    });
    expect(res).toBe(403);
  });
});
