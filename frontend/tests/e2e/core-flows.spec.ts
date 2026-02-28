import { test, expect } from "@playwright/test";

test("core layout sections render", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("CloudyIntel")).toBeVisible();
  await expect(page.getByText("Provider Results")).toBeVisible();
  await expect(page.getByText("Run History")).toBeVisible();
});
