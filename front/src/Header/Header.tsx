// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import logo from "../assets/logo.png";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../components/ui/popover.tsx";
import { Button } from "../components/ui/button.tsx";

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
      <Popover>
        <PopoverTrigger>
          <Button variant="outline">
            Status
            <div
              className={
                "inline-block w-[1.25vh] h-[1.25vh] rounded-xl " +
                (LLMStatus === 200
                  ? verStatus === true
                    ? "bg-green-500"
                    : "bg-yellow-500"
                  : "bg-red-500")
              }
            ></div>
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto">
          <div className="flex items-center justify-between">
            Ollama
            <div
              className={
                "inline-block w-[1.25vh] h-[1.25vh] rounded-xl " +
                (LLMStatus === 200 ? "bg-green-500" : "bg-red-500")
              }
            ></div>
          </div>
          <div className="flex items-center justify-between gap-2">
            Verified
            <div
              className={
                "inline-block w-[1.25vh] h-[1.25vh] rounded-xl " +
                (verStatus === true ? "bg-green-500" : "bg-red-500")
              }
            ></div>
          </div>
        </PopoverContent>
      </Popover>
    </header>
  );
}

export default Header;
