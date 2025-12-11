// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/** Utility for merging tw classes */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
