// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import "./Generate.css";

function Generate() {
  const [genStatus, setGenStatus] = useState(false);
  const [progStatus, setProgStatus] = useState([0, 0]);
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
    if (genStatus) setGenStatus(false);
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
    }
  }

  async function interrupt() {
    const url = baseURL + "/interrupt";
    const response = await fetch(url);
    const result = await response.json();
    setGenStatus(false);
    console.log(result);
  }

  return (
    <div className="Generate">
      {progStatus[0] !== 0 ? (
        <>
          <button className="button" onClick={interrupt}>
            Interrupt
          </button>
          <progress value={progStatus[0] / progStatus[1]}></progress>
        </>
      ) : (
        <>
          <button className="button" onClick={generate}>
            Generate
          </button>
        </>
      )}
    </div>
  );
}

export default Generate;
