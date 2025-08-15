// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen } from "@testing-library/react";
import Header from "./header.tsx";

test("renders generate button", () => {
  render(
    <Header
      verStatus={false}
      setVerStatus={() => {}}
      LLMStatus={200}
      setLLMStatus={() => {}}
      fileStatus={false}
      setFileStatus={() => {}}
    />,
  );

  const linkElement = screen.getByAltText(/Logo/i);
  expect(linkElement).toBeInTheDocument();
});
