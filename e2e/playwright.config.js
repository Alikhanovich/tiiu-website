// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * TIIU Website E2E konfiguratsiyasi.
 * Django dev-server'ni avtomatik ishga tushiradi (webServer) va unga qarshi test qiladi.
 *
 * Ishga tushirishdan oldin: bir marta test uchun staff foydalanuvchi kerak.
 * global-setup.js buni avtomatik yaratadi.
 */
module.exports = defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,          // bir DB, ketma-ket ishlaydi
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-report' }]],

  use: {
    baseURL: process.env.BASE_URL || 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    locale: 'uz-UZ',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    // Kerak bo'lsa oching:
    // { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    // { name: 'mobile',  use: { ...devices['Pixel 5'] } },
  ],

  // Django serverni avtomatik boshqarish
  webServer: {
    command: 'python ../manage.py runserver 127.0.0.1:8000 --noreload',
    url: 'http://127.0.0.1:8000/',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
    env: {
      DJANGO_SETTINGS_MODULE: 'config.settings',
      DEBUG: 'True',
    },
  },

  globalSetup: require.resolve('./global-setup.js'),
});
