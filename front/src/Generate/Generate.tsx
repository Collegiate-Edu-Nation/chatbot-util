// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React, { useState } from "react";
import useInterval from "@use-it/interval";
import "./Generate.css";

function Generate() {
  const [genStatus, setGenStatus] = useState(0);
  const [progStatus, setProgStatus] = useState([0, 0]);
  const baseURL = "http://127.0.0.1:8080/api";

  useInterval(() => progress(), 500);

  async function generate() {
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
    console.log(result);
    setGenStatus(result.detail);
  }

  async function progress() {
    const url = baseURL + "/progress";
    let response = await fetch(url);
    let result = await response.json();
    console.log(result);
    setProgStatus([result.index, result.total]);
  }

  async function interrupt() {
    const url = baseURL + "/interrupt";
    let response = await fetch(url);
    let result = await response.json();
    console.log(result);
    progress();
  }

  return (
    <div className="Generate">
      {progStatus[0] !== 0 ? (
        <>
          <button onClick={interrupt}>Interrupt</button>
          <progress value={progStatus[0] / progStatus[1]}></progress>
        </>
      ) : (
        <>
          <button onClick={generate}>Generate</button>
        </>
      )}
    </div>
  );
}

export default Generate;
