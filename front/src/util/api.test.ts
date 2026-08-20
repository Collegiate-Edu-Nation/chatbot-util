// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

import { afterEach, describe, expect, test, vi } from "vitest";
import {
  apiFetch,
  applicationRequestHeader,
  applicationRequestValue,
  AuthenticationRequiredError,
} from "./api.ts";

describe("apiFetch", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("adds the application marker to mutating requests", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 204 }));

    await apiFetch("/api/upload", { method: "POST" });

    const requestHeaders = new Headers(fetchMock.mock.calls[0]?.[1]?.headers);
    expect(requestHeaders.get(applicationRequestHeader)).toBe(
      applicationRequestValue,
    );
  });

  test("does not add the application marker to safe requests", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 200 }));

    await apiFetch("/api/health");

    const requestHeaders = new Headers(fetchMock.mock.calls[0]?.[1]?.headers);
    expect(requestHeaders.has(applicationRequestHeader)).toBe(false);
  });

  test("starts reauthentication after a 401 response", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 401 }),
    );
    const reauthenticate = vi.fn();

    await expect(
      apiFetch("/api/session", {}, reauthenticate),
    ).rejects.toBeInstanceOf(AuthenticationRequiredError);
    expect(reauthenticate).toHaveBeenCalledOnce();
  });
});
