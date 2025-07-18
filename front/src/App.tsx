// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React, { useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState(0);
  const [genStatus, setGenStatus] = useState(0);
  const [progStatus, setProgStatus] = useState([0, 0]);

  async function generate() {
    const settings = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    };
    const url = "http://127.0.0.1:8080/generate";
    let response = await fetch(url, settings);
    let result = await response.json();
    console.log(result);
    setGenStatus(result.detail);
  }

  async function health() {
    const url = "http://127.0.0.1:8080/health";
    let response = await fetch(url);
    let result = await response.json();
    console.log(result);
    setStatus(result.detail);
  }

  async function progress() {
    const url = "http://127.0.0.1:8080/progress";
    let response = await fetch(url);
    let result = await response.json();
    console.log(result);
    setProgStatus([result.index, result.total]);
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={generate}>Generate</button>
        <button onClick={health}>Health</button>
        <button onClick={progress}>Progress</button>
        <p>Server Status: {status}</p>
        <p>Generation Status: {genStatus}</p>
        <p>
          Progress Status: {progStatus[0]}/{progStatus[1]}
        </p>
      </header>
    </div>
  );
}

export default App;
