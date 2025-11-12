// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import pino from "pino";

const logger = pino();

export function message(method: string, endpoint: string, error: unknown) {
  return "Failed to " + method + " " + endpoint + ": " +
          (error instanceof Error ? error.message : error);
}

export default logger;
