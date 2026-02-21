import { test, expect } from '@playwright/test';
import { MfiPage } from '../pages/MfiPage';

test('sprawdź czy mgr Anna Baran pracuje w Instytucie Fizyki Doświadczalnej', async ({ page }) => {
  const mfi = new MfiPage(page);

  await mfi.navigate();

  await mfi.goToStaff();

  await page.getByRole('link', { name: 'Instytut Fizyki Doświadczalnej' }).click();

  const pracownik = page.getByText('mgr Anna Baran');
  await expect(pracownik).toBeVisible();
});