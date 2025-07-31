// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import { Button } from "../comp/ui/button.tsx";
import { Progress } from "../comp/ui/progress.tsx";
import { Loader2Icon } from "lucide-react";

function Generate({ setVerStatus }: { setVerStatus: (val: boolean) => void }) {
  const [genStatus, setGenStatus] = useState(false);
  const [progStatus, setProgStatus] = useState([0, 0]);
  const [interruptStatus, setInterruptStatus] = useState(false);
  const baseURL = "http://127.0.0.1:8080/api";

  useInterval(() => progress(), 500);

  async function generate() {
    setGenStatus(true);
    const settings = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    };
    const url = baseURL + "/generate";
    const response = await fetch(url, settings);
    const result = await response.json();
    setVerStatus(result.verified === 201 ? true : false);
    setGenStatus(false);
    console.log(result);
  }

  async function progress() {
    if (genStatus) {
      const url = baseURL + "/progress";
      const response = await fetch(url);
      const result = await response.json();
      setProgStatus([result.index, result.total]);
      console.log(result);
    } else if (!genStatus && progStatus[0] !== 0) {
      setProgStatus([0, 0]);
      setInterruptStatus(false);
    }
  }

  async function interrupt() {
    setInterruptStatus(true);
    const url = baseURL + "/interrupt";
    const response = await fetch(url);
    const result = await response.json();
    console.log(result);
  }

  return (
    <div className="flex justify-center items-center h-[93vh] dark:bg-neutral-900  bg-neutral-100 gap-2.5">
      {genStatus ? (
        <>
          <Button
            onClick={interrupt}
            variant="outline"
            disabled={interruptStatus}
          >
            Interrupt
            {interruptStatus ? <Loader2Icon className="animate-spin" /> : <></>}
          </Button>
          <div className="text-xs w-1/8">
            <div className="flex justify-center">
              {progStatus[0]} / {progStatus[1]}
            </div>
            <Progress value={(progStatus[0] / progStatus[1]) * 100}></Progress>
          </div>
        </>
      ) : (
        <Button onClick={generate} variant="outline">
          Generate
        </Button>
      )}
    </div>
  );
}

export default Generate;
