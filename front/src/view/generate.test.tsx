// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen } from "@testing-library/react";
import Generate from "./generate.tsx";

test("renders generate button", () => {
  render(
    <Generate setVerStatus={() => {}} LLMStatus={200} folderStatus={false} />,
  );

  const linkElement = screen.getByText(/Upload and Generate/i);
  expect(linkElement).toBeInTheDocument();
});
