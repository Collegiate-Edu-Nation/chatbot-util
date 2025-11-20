// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { render, screen, fireEvent } from "@testing-library/react";
import Header from "./header.tsx";

test("fileCheckIcon is visible in the status popover", () => {
  render(
    <Header
      verStatus={false}
      setVerStatus={() => {}}
      LLMStatus={200}
      setLLMStatus={() => {}}
      folderStatus={true}
      setFolderStatus={() => {}}
    />,
  );

  const statusButton = screen.getByRole("button", {
    name: /status button/i,
  });
  fireEvent.click(statusButton);
  const fileCheckButton = screen.getByRole("button", {
    name: /file check icon/i,
  });

  expect(fileCheckButton).toBeInTheDocument();
});
