// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { useState } from "react";
import useInterval from "react-useinterval";
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
    <header className="flex justify-between items-center h-[7vh] pl-3 pr-1.5 dark:bg-black light:bg-white text-black dark:text-white">
      <img src={logo} alt="Logo" width="100px"></img>
      <button className="bg-neutral-100 dark:bg-neutral-900">
        Status &nbsp;
        {status === 200 ? (
          <div className="inline-block w-[1.25vh] h-[1.25vh] rounded-xl  bg-green-500"></div>
        ) : (
          <>
            <div className="inline-block w-[1.25vh] h-[1.25vh] rounded-xl  bg-red-500"></div>
          </>
        )}
      </button>
    </header>
  );
}

export default Header;
