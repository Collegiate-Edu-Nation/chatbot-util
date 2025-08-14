// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import { toast } from "sonner";
import logo from "../assets/logo.png";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../comp/ui/popover.tsx";
import {
  CheckCircle2Icon,
  HelpCircleIcon,
  BrainIcon,
  FileCheckIcon,
  ListChecksIcon,
} from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "../comp/ui/tooltip.tsx";

function Header({
  verStatus,
  setVerStatus,
}: {
  verStatus: boolean;
  setVerStatus: (val: boolean) => void;
}) {
  const baseURL = "http://127.0.0.1:8080/api";

  const [LLMStatus, setLLMStatus] = useState(0);
  const [fileStatus, setFileStatus] = useState(0);

  useInterval(() => health(), LLMStatus === 200 ? 5000 : 500);
  useInterval(() => files(), fileStatus === 200 ? 50000 : 500);

  async function health() {
    const url = baseURL + "/health";
    const response = await fetch(url);
    const result = await response.json();
    console.log(result);
    setLLMStatus(result.detail);
  }

  async function files() {
    const url = baseURL + "/files";
    const response = await fetch(url);
    const result = await response.json();
    console.log(result);
    setFileStatus(result.detail);
  }

  return (
    <header className="flex justify-between items-center h-[7vh] pl-4 pr-2.5">
      <img src={logo} alt="Logo" width="100px"></img>

      {/* help */}
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

        {/* statusMenu */}
        <Popover>
          <PopoverTrigger>
            {/* overview */}
            <div className="flex items-end">
              <CheckCircle2Icon
                size="32"
                strokeWidth="1.25"
                className="hover:fill-accent hover:text-accent-foreground"
              ></CheckCircle2Icon>
              <div
                className={
                  "size-2 rounded-xl " +
                  (LLMStatus === 200 && fileStatus === 200
                    ? verStatus === true
                      ? "bg-green-500"
                      : "bg-yellow-500"
                    : "bg-red-500")
                }
              ></div>
            </div>
          </PopoverTrigger>
          <PopoverContent className="w-auto">
            {/* LLMStatus */}
            <div className="flex items-end gap-1 pb-1.5">
              <Tooltip>
                <TooltipTrigger asChild={true}>
                  <BrainIcon size="24" strokeWidth="1.25"></BrainIcon>
                </TooltipTrigger>
                <TooltipContent side="bottom">Ollama status</TooltipContent>
              </Tooltip>
              <div
                className={
                  "inline-block size-2 rounded-xl " +
                  (LLMStatus === 200 ? "bg-green-500" : "bg-red-500")
                }
              ></div>
            </div>

            {/* fileStatus */}
            <div className="flex items-end gap-1 pt-1.5 pb-1.5">
              <Tooltip>
                <TooltipTrigger asChild={true}>
                  <FileCheckIcon size="24" strokeWidth="1.25"></FileCheckIcon>
                </TooltipTrigger>
                <TooltipContent side="bottom">File status</TooltipContent>
              </Tooltip>
              <div
                className={
                  "inline-block size-2 rounded-xl " +
                  (fileStatus === 200 ? "bg-green-500" : "bg-red-500")
                }
              ></div>
            </div>

            {/* verStatus */}
            <div className="flex items-end gap-1 pt-1.5">
              <Tooltip>
                <TooltipTrigger asChild={true} className="flex">
                  <ListChecksIcon
                    size="24"
                    strokeWidth="1.25"
                    className={
                      verStatus
                        ? ""
                        : "hover:fill-accent hover:text-accent-foreground"
                    }
                    onClick={
                      verStatus
                        ? () => void 0
                        : () =>
                            toast("Unverified", {
                              description:
                                "Newly generated Permutated.csv is missing entries",
                              action: {
                                label: "Okay",
                                onClick: () => setVerStatus(true),
                              },
                            })
                    }
                  ></ListChecksIcon>
                </TooltipTrigger>
                <TooltipContent side="bottom">Verified status</TooltipContent>
              </Tooltip>
              <div
                className={
                  "inline-block size-2 rounded-xl " +
                  (verStatus ? "bg-green-500" : "bg-red-500")
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
