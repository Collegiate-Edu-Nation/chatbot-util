// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://127.0.0.1:5173",
    allowCypressEnv: false,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
