// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders server status indicator", () => {
  render(<App />);
  const linkElement = screen.getByText(/Server status/i);
  expect(linkElement).toBeInTheDocument();
});
