// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
import "./Header.css";
import logo from "../assets/logo.png";

function Header() {
  const [status, setStatus] = useState(0);
  const baseURL = "http://127.0.0.1:8080/api";

  const delay = status === 200 ? 5000 : 500;
  useInterval(() => health(), delay);

  async function health() {
    const url = baseURL + "/health";
    const response = await fetch(url);
    const result = await response.json();
    console.log(result);
    setStatus(result.detail);
  }

  return (
    <header className="App-header">
      <img src={logo} alt="Logo" width="100px"></img>
      <button className="button">
        Status &nbsp;
        {status === 200 ? (
          <div className="circle green-circle"></div>
        ) : (
          <>
            <div className="circle red-circle"></div>
          </>
        )}
      </button>
    </header>
  );
}

export default Header;
