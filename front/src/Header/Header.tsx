// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import React, { useState } from "react";
import useInterval from "@use-it/interval";
import "./Header.css";
import logo from "../logo.png";

function Header() {
  const [status, setStatus] = useState(0);
  const baseURL = "http://127.0.0.1:8080/api";

  useInterval(() => health(), 500);

  async function health() {
    const url = baseURL + "/health";
    let response = await fetch(url);
    let result = await response.json();
    console.log(result);
    setStatus(result.detail);
  }

  return (
    <header className="App-header">
      <img src={logo} alt="Logo" width="100px"></img>
      {status === 200 ? (
        <div className="green-circle"></div>
      ) : (
        <>
          <div className="red-circle"></div>
        </>
      )}
    </header>
  );
}

export default Header;
