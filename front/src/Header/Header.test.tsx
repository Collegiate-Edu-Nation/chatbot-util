// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen } from "@testing-library/react";
import Header from "./Header";

test("renders generate button", () => {
  render(<Header />);
  const linkElement = screen.getByAltText(/Logo/i);
  expect(linkElement).toBeInTheDocument();
});
