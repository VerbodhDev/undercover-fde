import type { Status } from "./api";

const dollars = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

export const money = (amount: number) => dollars.format(amount);

export const statusLabels: Record<Status, string> = {
  waiting: "Waiting",
  in_progress: "In progress",
  waiting_for_sign_off: "Waiting for sign-off",
  decided: "Decided",
};

export const label = (value: string) => {
  const words = value.replaceAll("_", " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
};
