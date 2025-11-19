// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import useInterval from "react-useinterval";
import { toast } from "sonner";
import logo from "../assets/logo.png";
import logger, { message } from "../util/logger.ts";
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
  FolderOpenIcon,
} from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "../comp/ui/tooltip.tsx";

/**
 * View containing logo, help icon, and status popover
 *
 * ```tsx
 * <Header
 *   verStatus={verStatus}
 *   setVerStatus={(val) => setVerStatus(val)}
 *   LLMStatus={LLMStatus}
 *   setLLMStatus={(val) => setLLMStatus(val)}
 *   folderStatus={folderStatus}
 *   setFolderStatus={(val) => setFolderStatus(val)}
 * />
 * ```
 */
function Header({
  verStatus,
  setVerStatus,
  LLMStatus,
  setLLMStatus,
  folderStatus,
  setFolderStatus,
}: {
  verStatus: boolean | null;
  setVerStatus: (val: boolean | null) => void;
  LLMStatus: number;
  setLLMStatus: (val: number) => void;
  folderStatus: boolean;
  setFolderStatus: (val: boolean) => void;
}) {
  const baseURL = "http://127.0.0.1:8080/api";

  useInterval(() => health(), LLMStatus === 200 ? 5000 : 500);
  useInterval(() => files(), folderStatus ? 50000 : 500);

  async function health() {
    const url = baseURL + "/health";
    const response = await fetch(url);
    const result = response.status;
    setLLMStatus(result);
  }

  async function files() {
    const url = baseURL + "/files";
    try {
      const response = await fetch(url);
      const result = await response.json();
      setFolderStatus(result.present);
    } catch (error) {
      logger.error(message("get", "files", error));
    }
  }

  return (
    <header className="flex justify-between items-center h-14 pl-4 pr-2.5">
      <a
        href="https://edu-nation.org"
        target="_blank"
        className="cursor-default"
      >
        <img
          src={logo}
          alt="CENthia logo linking to edu-nation.org"
          width="100px"
        ></img>
      </a>

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
                  (LLMStatus === 200 && folderStatus
                    ? verStatus === true || verStatus === null
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

            {/* folderStatus */}
            <div className="flex items-end gap-1 pt-1.5 pb-1.5">
              <Tooltip>
                <TooltipTrigger asChild={true}>
                  <FolderOpenIcon size="24" strokeWidth="1.25"></FolderOpenIcon>
                </TooltipTrigger>
                <TooltipContent side="bottom">Folder status</TooltipContent>
              </Tooltip>
              <div
                className={
                  "inline-block size-2 rounded-xl " +
                  (folderStatus ? "bg-green-500" : "bg-red-500")
                }
              ></div>
            </div>

            {/* verStatus */}
            <div className="flex items-end gap-1 pt-1.5">
              <Tooltip>
                <TooltipTrigger asChild={true} className="flex">
                  <FileCheckIcon
                    size="24"
                    strokeWidth="1.25"
                    className={
                      verStatus === null
                        ? ""
                        : verStatus
                          ? ""
                          : "hover:fill-accent hover:text-accent-foreground"
                    }
                    onClick={
                      verStatus === null
                        ? () => void 0
                        : verStatus
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
                  ></FileCheckIcon>
                </TooltipTrigger>
                <TooltipContent side="bottom">Verified status</TooltipContent>
              </Tooltip>
              <div
                className={
                  "inline-block size-2 rounded-xl " +
                  (verStatus === null
                    ? "bg-neutral-500"
                    : verStatus
                      ? "bg-green-500"
                      : "bg-red-500")
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
