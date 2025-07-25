// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import Header from "./Header/Header.tsx";
import Generate from "./Generate/Generate.tsx";

// lift the state from children
export default function App() {
  const [verStatus, setVerStatus] = useState(true);
  return (
    <>
      <Header verStatus={verStatus} />
      <Generate setVerStatus={(val) => setVerStatus(val)} />
    </>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
