// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import { useSessionStorage } from "usehooks-ts";
import useInterval from "react-useinterval";
import { toast } from "sonner";
import logger, { message } from "../util/logger.ts";
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

/**
 * View containing generate card and page body
 *
 * ```tsx
 * <Generate
 *   setVerStatus={(val) => setVerStatus(val)}
 *   LLMStatus={LLMStatus}
 *   folderStatus={folderStatus}
 * />
 * ```
 */
function Generate({
  setVerStatus,
  LLMStatus,
  folderStatus,
}: {
  setVerStatus: (val: boolean | null) => void;
  LLMStatus: number;
  folderStatus: boolean;
}) {
  const baseURL = "http://127.0.0.1:8080/api";

  const [files, setFiles] = useState<File[] | undefined>();
  const [appConfig, setAppConfig] = useState(["", ""]);
  const [genStatus, setGenStatus] = useSessionStorage("genStatus", false);
  const [progStatus, setProgStatus] = useSessionStorage("progStatus", [0, 0]);
  const [interruptStatus, setInterruptStatus] = useSessionStorage(
    "interruptStatus",
    false,
  );

  // config isn't actually dependent on folderStatus since its primary
  // purpose is preventing generating w/ missing data files (which causes
  // crashes). however, since it defaults to false, this is a decent hack
  // for ensuring the config is always read on startup w/o polling nonstop
  useInterval(() => progress(), 500);
  useInterval(() => config(), folderStatus ? 50000 : 500);
  const handleDrop = (files: File[]) => setFiles(files);

  // reset status if interruption completed while refreshing to avoid getting stuck
  if (
    genStatus &&
    interruptStatus &&
    progStatus[0] === 0 &&
    progStatus[1] === 0
  ) {
    setInterruptStatus(false);
    setGenStatus(false);
  }

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

    try {
      const response = await fetch(url, settings);
      const status = response.status;
      const result = await response.json();
      setVerStatus(result.verified);

      if (status === 429)
        toast("Rate-limited", {
          description: "You've been rate-limited. Try again in a few minutes",
          action: {
            label: "Okay",
            onClick: () => void 0,
          },
        });

      if (result.verified === false)
        toast("Unverified", {
          description: "Newly generated Permutated.csv is missing entries",
          action: {
            label: "Okay",
            onClick: () => setVerStatus(true),
          },
        });
    } catch (error) {
      logger.error(message("post", "generate", error));
    }

    setGenStatus(false);
  }

  async function progress() {
    if (genStatus) {
      const url = baseURL + "/progress";
      const response = await fetch(url);
      const result = await response.json();
      setProgStatus([result.index, result.total]);
    } else if (!genStatus && progStatus[0] !== 0) {
      setProgStatus([0, 0]);
      setInterruptStatus(false);
    }
  }

  async function interrupt() {
    setInterruptStatus(true);
    const url = baseURL + "/interrupt";
    await fetch(url);
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

      try {
        const response = await fetch(url, settings);
        const result = await response.json();

        // toast based on upload success of ALL files before resetting files
        const title = result.uploaded
          ? "Updated file(s)"
          : "Failed to update file(s)";
        const desc = result.uploaded
          ? "The data file(s) you uploaded have been saved to ~/.chatbot-util/"
          : "The data file(s) you uploaded have NOT been saved to ~/.chatbot-util/";
        toast(title, { description: desc });
      } catch (error) {
        logger.error(message("post", "upload", error));
      }
      setFiles(undefined);
    }
  }

  async function config() {
    const url = baseURL + "/config";
    const response = await fetch(url);
    const result = await response.json();
    setAppConfig([result.faq, result.other]);
  }

  function links() {
    if (appConfig[0] === "") {
      return false;
    }

    return (
      <CardAction className="flex flex-col">
        <Button variant="link" asChild>
          <a href={appConfig[0]} target="_blank" className="cursor-default">
            FAQ
          </a>
        </Button>
        <Button variant="link" asChild>
          <a href={appConfig[1]} target="_blank" className="cursor-default">
            Other
          </a>
        </Button>
      </CardAction>
    );
  }

  return (
    <div className="flex flex-grow justify-center items-center dark:bg-neutral-900  bg-neutral-100 gap-2.5">
      <Card className="w-full max-w-sm">
        {/* info and links */}
        <CardHeader>
          <CardTitle>Upload and Generate</CardTitle>
          <CardDescription>
            Upload 'FAQ - Enter Here.csv' + 'Other.txt' and generate
            'Permutated.csv'
          </CardDescription>
          {links()}
        </CardHeader>

        {/* upload */}
        <CardContent>
          <Dropzone
            accept={{ "text/*": [".txt", ".csv"], "application/*": [".toml"] }}
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

        {/* buttons */}
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
            <Button
              onClick={generate}
              variant="outline"
              disabled={!(folderStatus && LLMStatus === 200)}
              className="w-auto"
            >
              Generate
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}

export default Generate;
