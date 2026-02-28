import { test, expect } from "@playwright/test";

test("workflow graph and handoff timeline are visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Workflow Graph State")).toBeVisible();
  await expect(page.getByText("Hand-off Timeline")).toBeVisible();
});
