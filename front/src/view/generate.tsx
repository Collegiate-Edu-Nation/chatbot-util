// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import { toast } from "sonner";
import { Button } from "../comp/ui/button.tsx";
import { Progress } from "../comp/ui/progress.tsx";
import {
  Dropzone,
  DropzoneContent,
  DropzoneEmptyState,
} from "../comp/ui/dropzone.tsx";
import { Loader2Icon } from "lucide-react";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/comp/ui/card.tsx";

function Generate({ setVerStatus }: { setVerStatus: (val: boolean) => void }) {
  const baseURL = "http://127.0.0.1:8080/api";

  const [genStatus, setGenStatus] = useState(false);
  const [progStatus, setProgStatus] = useState([0, 0]);
  const [interruptStatus, setInterruptStatus] = useState(false);
  const [files, setFiles] = useState<File[] | undefined>();

  useInterval(() => progress(), 500);
  const handleDrop = (files: File[]) => {
    console.log(files);
    setFiles(files);
  };

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
    const verified = result.verified === 201 ? true : false;
    setVerStatus(verified);
    if (!verified)
      toast("Unverified", {
        description: "Newly generated Permutated.csv is missing entries",
        action: {
          label: "Okay",
          onClick: () => setVerStatus(true),
        },
      });
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

  async function upload() {
    if (files !== undefined) {
      // convert files to FormData() so we can send them to the endpoint
      const data = new FormData();
      for (const f of files) data.append("files", f);
      const settings = {
        method: "POST",
        body: data,
      };
      const url = baseURL + "/upload";
      const response = await fetch(url, settings);
      const result = await response.json();

      // toast based on upload success of ALL files before resetting files
      let success = true;
      for (const s of result.detail) if (s !== 201) success = false;
      const title = success ? "Updated file(s)" : "Failed to update file(s)";
      const desc = success
        ? "The data file(s) you uploaded have been saved to ~/.chatbot-util/"
        : "The data file(s) you uploaded have NOT been saved to ~/.chatbot-util/";
      toast(title, { description: desc });
      setFiles(undefined);
      console.log("Upload received " + JSON.stringify(result));
    }
  }

  return (
    <div className="flex justify-center items-center h-[93vh] dark:bg-neutral-900  bg-neutral-100 gap-2.5">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Upload and Generate</CardTitle>
          <CardDescription>
            Upload 'FAQ - Enter Here.csv' + 'Other.txt' and generate
            'Permutated.csv'
          </CardDescription>
          <CardAction className="flex flex-col">
            <Button variant="link" asChild>
              <a
                href="https://docs.google.com/spreadsheets/d/1hQ1oN2r6J-03jDaF0-ol7Cof6kv_6De8N7icbi7dmv8/edit?usp=drive_link"
                target="_blank"
                className="cursor-default"
              >
                FAQ
              </a>
            </Button>
            <Button variant="link" asChild>
              <a
                href="https://drive.google.com/file/d/1CsRu9C-xpROe9OhvENCAJ3uAZ79rjUXW/view?usp=drive_link"
                target="_blank"
                className="cursor-default"
              >
                Other
              </a>
            </Button>
          </CardAction>
        </CardHeader>
        <CardContent>
          <Dropzone
            accept={{ "text/*": [] }}
            maxFiles={10}
            maxSize={1024 * 1024 * 10}
            minSize={1}
            onDrop={handleDrop}
            onError={console.error}
            src={files}
          >
            <DropzoneEmptyState />
            <DropzoneContent />
          </Dropzone>
        </CardContent>
        <CardFooter className="flex-col gap-2">
          {files !== undefined ? (
            <Button onClick={upload} variant="outline" className="w-auto">
              Replace
            </Button>
          ) : (
            <></>
          )}
          {genStatus ? (
            <div className="flex w-full items-center gap-2">
              <Button
                onClick={interrupt}
                variant="outline"
                disabled={interruptStatus}
                className="w-auto"
              >
                Interrupt
                {interruptStatus ? (
                  <Loader2Icon className="animate-spin" />
                ) : (
                  <></>
                )}
              </Button>
              <div className="text-xs w-full">
                <div className="flex justify-center">
                  {progStatus[0]} / {progStatus[1]}
                </div>
                <Progress
                  value={(progStatus[0] / progStatus[1]) * 100}
                ></Progress>
              </div>
            </div>
          ) : (
            <Button onClick={generate} variant="outline" className="w-auto">
              Generate
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}

export default Generate;
