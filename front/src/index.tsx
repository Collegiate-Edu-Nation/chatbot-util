// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { ThemeProvider } from "./comp/theme-provider.tsx";
import Header from "./view/header.tsx";
import Generate from "./view/generate.tsx";

// lift the state from children
export default function App() {
  const [verStatus, setVerStatus] = useState(true);
  return (
    <ThemeProvider>
      <Header verStatus={verStatus} />
      <Generate setVerStatus={(val) => setVerStatus(val)} />
    </ThemeProvider>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
