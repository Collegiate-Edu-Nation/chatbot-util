// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import Header from "./Header/Header.tsx";
import Generate from "./Generate/Generate.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Header />
    <Generate />
  </StrictMode>,
);
