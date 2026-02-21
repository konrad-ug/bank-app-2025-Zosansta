import { Page } from '@playwright/test';

export class StaffPage {
  constructor(private page: Page) {}


  async navigateToMfi() {
    await this.page.goto('https://mfi.ug.edu.pl/');
  }

  async openStaffList() {
    await this.page.locator('a:has-text("Pracownicy")').first().click();
    
    await this.page.getByRole('link', { name: 'skład osobowy' }).first().click({ force: true });
  }
}