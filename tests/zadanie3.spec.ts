import { test, expect } from '@playwright/test';
import { StaffPage } from '../pages/StaffPage';

test('Zadanie 3: Sprawdzenie pracownika mgr Anna Baran', async ({ page }) => {
  const staffPage = new StaffPage(page);


  await staffPage.navigateToMfi();


  await page.goto('https://mfi.ug.edu.pl/pracownicy/sklad-osobowy/instytut-fizyki-doswiadczalnej');


  await page.waitForLoadState('networkidle');


  const pracownik = page.locator('text=/Anna Baran/i').first();
  

  await expect(pracownik).toBeAttached({ timeout: 15000 });

  await expect(pracownik).toBeVisible();
});

//nie działa :((