import { test, expect } from '@playwright/test';

test('landing page loads with expected content', async ({ page }) => {
  await page.goto('/');

  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('h1')).toContainText('Welcome');
});
