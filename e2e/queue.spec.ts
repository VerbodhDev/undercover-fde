import { expect, test } from "@playwright/test";

test("the queue lists every claim and opens one", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Claims queue" }),
  ).toBeVisible();
  await expect(page.locator("tbody tr")).toHaveCount(25);
  await page.getByRole("link", { name: "CLM-1001" }).click();
  await expect(page.getByText("My flight home from Rome")).toBeVisible();
  await page.getByRole("link", { name: "Back to the queue" }).click();
  await expect(page.locator("tbody tr")).toHaveCount(25);
});

test("the instructions are shown read only", async ({ page }) => {
  await page.goto("/#/instructions");
  await expect(page.getByText("You are the UnderCover Agent.")).toBeVisible();
  await expect(page.getByRole("textbox")).toHaveCount(0);
});
