import { Page, expect } from '@playwright/test';

export class MfiPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('https://mfi.ug.edu.pl/');
  }

  async goToStaff() {
    await this.page.getByRole('link', { name: 'Pracownicy' }).click();
    await this.page.getByRole('link', { name: 'skład osobowy' }).click();
  }

  async searchStaff(name: string) {
    await this.page.getByPlaceholder('Szukaj').fill(name);
    await this.page.keyboard.press('Enter');
  }
}