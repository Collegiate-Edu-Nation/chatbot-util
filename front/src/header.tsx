// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import logo from "./assets/logo.png";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "./components/ui/popover.tsx";
import {
  CheckCircle2Icon,
  HelpCircleIcon,
  BrainIcon,
  FileCheckIcon,
} from "lucide-react";

function Header({ verStatus }: { verStatus: boolean }) {
  const [LLMStatus, setLLMStatus] = useState(0);
  const baseURL = "http://127.0.0.1:8080/api";
  const delay = LLMStatus === 200 ? 5000 : 500;

  useInterval(() => health(), delay);

  async function health() {
    const url = baseURL + "/health";
    const response = await fetch(url);
    const result = await response.json();
    console.log(result);
    setLLMStatus(result.detail);
  }

  return (
    <header className="flex justify-between items-center h-[7vh] pl-4 pr-2.5">
      <img src={logo} alt="Logo" width="100px"></img>
      <div className="flex items-center gap-2">
        <a
          href="https://collegiate-edu-nation.github.io/chatbot-util/instructions/"
          target="_blank"
          className="cursor-default"
        >
          <HelpCircleIcon
            size="32"
            strokeWidth="1.25"
            className="hover:fill-accent hover:text-accent-foreground"
          ></HelpCircleIcon>
        </a>
        <Popover>
          <PopoverTrigger>
            <div className="flex items-end">
              <CheckCircle2Icon
                size="32"
                strokeWidth="1.25"
                className="hover:fill-accent hover:text-accent-foreground"
              ></CheckCircle2Icon>
              <div
                className={
                  "w-[1vh] h-[1vh] rounded-xl " +
                  (LLMStatus === 200
                    ? verStatus === true
                      ? "bg-green-500"
                      : "bg-yellow-500"
                    : "bg-red-500")
                }
              ></div>
            </div>
          </PopoverTrigger>
          <PopoverContent className="w-auto">
            <div title="Ollama status" className="flex items-end gap-1 pb-1.5">
              <BrainIcon size="24" strokeWidth="1.25"></BrainIcon>
              <div
                className={
                  "inline-block w-[1vh] h-[1vh] rounded-xl " +
                  (LLMStatus === 200 ? "bg-green-500" : "bg-red-500")
                }
              ></div>
            </div>
            <div
              title="Verified status"
              className="flex items-end gap-1 pt-1.5"
            >
              <FileCheckIcon size="24" strokeWidth="1.25"></FileCheckIcon>
              <div
                className={
                  "inline-block w-[1vh] h-[1vh] rounded-xl " +
                  (verStatus === true ? "bg-green-500" : "bg-red-500")
                }
              ></div>
            </div>
          </PopoverContent>
        </Popover>
      </div>
    </header>
  );
}

export default Header;
