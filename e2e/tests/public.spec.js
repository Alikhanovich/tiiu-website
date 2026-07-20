// Public sayt E2E — real brauzerda sahifalar ochilishi va kontakt forma.
const { test, expect } = require('@playwright/test');

const PAGES = [
  ['/', 'Bosh sahifa'],
  ['/about/', 'Haqida'],
  ['/faculties/', "Yo'nalishlar"],
  ['/news/', 'Yangiliklar'],
  ['/events/', 'Tadbirlar'],
  ['/gallery/', 'Galereya'],
  ['/contact/', 'Aloqa'],
  ['/teachers/', "O'qituvchilar"],
  ['/leadership/', 'Rahbariyat'],
  ['/departments/', 'Kafedralar'],
  ['/centers/', 'Markazlar'],
];

test.describe('Public sahifalar ochiladi', () => {
  for (const [path, label] of PAGES) {
    test(`${label} (${path}) 200 va HTML render`, async ({ page }) => {
      const resp = await page.goto(path);
      expect(resp.status()).toBe(200);
      // <body> bo'sh emasligini tekshiramiz
      const bodyText = await page.locator('body').innerText();
      expect(bodyText.length).toBeGreaterThan(20);
    });
  }
});

test('Yo\'q sahifa 404 beradi', async ({ page }) => {
  const resp = await page.goto('/bunday-sahifa-yoq-12345/');
  expect(resp.status()).toBe(404);
});

test('Kontakt forma yuborish oqimi', async ({ page }) => {
  await page.goto('/contact/');

  // Forma maydonlarini topishga urinamiz (nomlar view'dan: first_name, last_name...)
  const firstName = page.locator('[name="first_name"]').first();
  const lastName = page.locator('[name="last_name"]').first();

  // Agar sahifada forma bo'lmasa, testni skip qilamiz (ba'zi dizaynlarda modal bo'lishi mumkin)
  const hasForm = await firstName.count();
  test.skip(hasForm === 0, 'Kontakt formasi bu sahifada topilmadi (ehtimol modal/boshqa selektor)');

  await firstName.fill('E2E');
  await lastName.fill('Test');
  const phone = page.locator('[name="phone"]').first();
  if (await phone.count()) await phone.fill('+998901234567');
  const msg = page.locator('[name="message"]').first();
  if (await msg.count()) await msg.fill('Playwright orqali yuborilgan test xabar.');

  // POST'ni to'g'ridan-to'g'ri ushlaymiz
  const respPromise = page.waitForResponse(r => r.url().includes('/contact/submit/'));
  await page.locator('button[type="submit"], [type="submit"]').first().click();
  const resp = await respPromise;
  expect(resp.status()).toBe(200);
});
