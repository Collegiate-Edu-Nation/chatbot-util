// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { StrictMode, useState } from "react";
import { useSessionStorage } from "usehooks-ts";
import { createRoot } from "react-dom/client";
import "./index.css";
import { ThemeProvider } from "./comp/theme-provider.tsx";
import { Toaster } from "./comp/ui/sonner";
import Header from "./view/header.tsx";
import Generate from "./view/generate.tsx";

// lift the state from children
export default function App() {
  const [LLMStatus, setLLMStatus] = useState(0);
  const [fileStatus, setFileStatus] = useState(false);
  const [verStatus, setVerStatus] = useSessionStorage<boolean | null>(
    "verStatus",
    null,
  );

  return (
    <ThemeProvider>
      <Toaster position="top-center" visibleToasts={1} />
      <div className="flex flex-col min-h-screen">
        <Header
          verStatus={verStatus}
          setVerStatus={(val) => setVerStatus(val)}
          LLMStatus={LLMStatus}
          setLLMStatus={(val) => setLLMStatus(val)}
          fileStatus={fileStatus}
          setFileStatus={(val) => setFileStatus(val)}
        />
        <Generate
          setVerStatus={(val) => setVerStatus(val)}
          LLMStatus={LLMStatus}
          fileStatus={fileStatus}
        />
      </div>
    </ThemeProvider>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
