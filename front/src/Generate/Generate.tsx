// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React, { useState } from "react";
import useInterval from "@use-it/interval";
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
    let response = await fetch(url, settings);
    let result = await response.json();
    if (genStatus) setGenStatus(false);
    console.log(result);
  }

  async function progress() {
    if (genStatus) {
      const url = baseURL + "/progress";
      let response = await fetch(url);
      let result = await response.json();
      setProgStatus([result.index, result.total]);
      console.log(result);
    } else if (!genStatus && progStatus[0] !== 0) {
      setProgStatus([0, 0]);
    }
  }

  async function interrupt() {
    const url = baseURL + "/interrupt";
    let response = await fetch(url);
    let result = await response.json();
    setGenStatus(false);
    console.log(result);
  }

  return (
    <div className="Generate">
      {progStatus[0] !== 0 ? (
        <>
          <button className="Button" onClick={interrupt}>
            Interrupt
          </button>
          <progress value={progStatus[0] / progStatus[1]}></progress>
        </>
      ) : (
        <>
          <button className="Button" onClick={generate}>
            Generate
          </button>
        </>
      )}
    </div>
  );
}

export default Generate;
