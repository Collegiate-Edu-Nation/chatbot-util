// SPDX-FileCopyrightText: Collegiate Edu-Nation
// SPDX-License-Identifier: GPL-3.0-or-later

export const applicationRequestHeader = "X-Chatbot-Util-Request";
export const applicationRequestValue = "1";

const safeMethods = new Set(["GET", "HEAD", "OPTIONS"]);
let reauthenticationStarted = false;

/** Error raised after an API response indicates that the SSO session expired. */
export class AuthenticationRequiredError extends Error {
  constructor() {
    super("Authentication required");
    this.name = "AuthenticationRequiredError";
  }
}

function reloadForAuthentication() {
  if (!reauthenticationStarted) {
    reauthenticationStarted = true;
    window.location.reload();
  }
}

/**
 * Fetch an API resource using the application's reverse-proxy auth contract.
 *
 * Mutating requests receive a non-simple marker header for CSRF resistance. A
 * `401` reloads the document so Apache can restart the interactive OIDC flow.
 */
export async function apiFetch(
  input: RequestInfo | URL,
  init: RequestInit = {},
  reauthenticate: () => void = reloadForAuthentication,
): Promise<Response> {
  const method = (init.method ?? "GET").toUpperCase();
  const headers = new Headers(init.headers);

  if (!safeMethods.has(method)) {
    headers.set(applicationRequestHeader, applicationRequestValue);
  }

  const response = await fetch(input, { ...init, headers });
  if (response.status === 401) {
    reauthenticate();
    throw new AuthenticationRequiredError();
  }

  return response;
}

/** Identify expected API failures caused by an expired SSO session. */
export function isAuthenticationRequired(error: unknown): boolean {
  return error instanceof AuthenticationRequiredError;
}
