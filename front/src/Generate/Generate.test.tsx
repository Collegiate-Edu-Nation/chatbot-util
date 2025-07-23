// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen } from "@testing-library/react";
import Generate from "./Generate";

test("renders generate button", () => {
  render(<Generate />);
  const linkElement = screen.getByText(/Generate/i);
  expect(linkElement).toBeInTheDocument();
});
