// E2E uchun test staff foydalanuvchisini yaratadi (agar mavjud bo'lmasa).
// Django management buyrug'i orqali ishlaydi — alohida test DB'ga tegmaydi,
// shuning uchun lokal dev DB'da 'e2e_admin' foydalanuvchisi paydo bo'ladi.
const { execSync } = require('child_process');
const path = require('path');

module.exports = async () => {
  const projectRoot = path.resolve(__dirname, '..');
  const py = `
from django.contrib.auth import get_user_model
U = get_user_model()
u, created = U.objects.get_or_create(username='e2e_admin', defaults={'is_staff': True, 'is_active': True})
u.is_staff = True
u.is_active = True
u.set_password('e2e-Pass-123!')
u.save()
print('e2e_admin ready (created=%s)' % created)
`.trim();

  try {
    execSync(`python manage.py shell -c "${py.replace(/"/g, '\\"')}"`, {
      cwd: projectRoot,
      stdio: 'inherit',
      env: { ...process.env, DJANGO_SETTINGS_MODULE: 'config.settings', DEBUG: 'True' },
    });
  } catch (e) {
    console.error('global-setup: staff user yaratishda xatolik', e.message);
    throw e;
  }
};
