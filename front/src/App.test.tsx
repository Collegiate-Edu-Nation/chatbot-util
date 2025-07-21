// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders generate button", () => {
  render(<App />);
  const linkElement = screen.getByText(/Generate/i);
  expect(linkElement).toBeInTheDocument();
});
