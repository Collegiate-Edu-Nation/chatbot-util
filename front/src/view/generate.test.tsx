// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen } from "@testing-library/react";
import Generate from "./generate.tsx";

test("generate button is disabled when LLM is not found", () => {
  render(
    <Generate setVerStatus={() => {}} LLMStatus={400} folderStatus={false} />,
  );

  const linkElement = screen.getByRole("button", {
    name: /generate button/i,
  });
  expect(linkElement).toBeDisabled();
});

test("generate button is disabled when data/config folder is not found", () => {
  render(
    <Generate setVerStatus={() => {}} LLMStatus={200} folderStatus={false} />,
  );

  const linkElement = screen.getByRole("button", {
    name: /generate button/i,
  });
  expect(linkElement).toBeDisabled();
});

test("generate button is enabled when both LLM and data/config folder are good to go", () => {
  render(
    <Generate setVerStatus={() => {}} LLMStatus={200} folderStatus={true} />,
  );

  const linkElement = screen.getByRole("button", {
    name: /generate button/i,
  });
  expect(linkElement).toBeEnabled();
});
