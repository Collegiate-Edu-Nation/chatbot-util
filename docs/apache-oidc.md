# Apache OIDC deployment

`chatbot-util` can run behind Apache while Apache authenticates users with Google
Workspace through OpenID Connect. Apache owns the browser session and access
policy; the application trusts only the identity header Apache creates after a
successful login.

```text
browser -> Apache/mod_auth_openidc -> chatbot-util on loopback
                    |
                    +-> Google Workspace
```

The application contains no Google client secret and does not validate Google
tokens itself. This keeps the identity-provider configuration at the reverse
proxy boundary.

## Enable the application-side boundary

For NixOS or nix-darwin, enable proxy authentication and keep the listener on
loopback:

```nix
services.chatbot-util = {
  enable = true;
  host = "127.0.0.1";
  port = 8080;

  proxyAuth = {
    enable = true;
    userHeader = "X-Authenticated-User";
  };
};
```

For another service manager, set the equivalent environment variables:

```text
HOST=127.0.0.1
PORT=8080
CHATBOT_UTIL_PROXY_AUTH=true
CHATBOT_UTIL_AUTH_HEADER=X-Authenticated-User
```

Proxy authentication is disabled by default so local development continues to
work without an identity provider. When enabled, every application route,
including the frontend, API, health endpoint, and generated API documentation,
returns `401` unless the configured identity header contains one unambiguous
value.

The identity header is not a bearer token or a secret. Its trust comes entirely
from making the backend unreachable to clients and allowing only Apache to
connect to it. Do not bind the service to a public interface in this mode.

## Apache contract

The final Apache virtual host must:

1. Terminate HTTPS and protect the entire origin with `mod_auth_openidc`.
2. Authenticate against the Google Workspace OIDC provider.
3. Authorize the intended IT accounts, rather than merely accepting every user
   in the Workspace domain.
4. Remove any client-supplied `X-Authenticated-User` header and set that header
   from Apache's authenticated `REMOTE_USER`, for example with
   `OIDCAuthNHeader X-Authenticated-User`.
5. Proxy only to the loopback listener, such as `http://127.0.0.1:8080/`.
6. Return `401` rather than an HTML login redirect for unauthenticated
   `/api/*` requests. With `mod_auth_openidc`, this is configured with
   `OIDCUnAuthAction 401` in the protected API location.
7. Redirect an unauthenticated document request to Google. When an API request
   returns `401`, the frontend reloads the document to start that interactive
   flow.
8. Avoid adding permissive CORS headers. The application's request-marker CSRF
   control assumes production API requests remain same-origin.

The Apache and application header names must match. Claims and tokens should not
be forwarded to the application unless a future feature explicitly requires
them.

## Request and audit behavior

- `GET /api/session` returns the asserted identity. It reports an unauthenticated
  local session when proxy authentication is disabled.
- The frontend adds `X-Chatbot-Util-Request: 1` to state-changing requests. The
  API requires this non-simple header to prevent cross-origin form submissions.
- `POST /api/interrupt` replaces the previous state-changing `GET` endpoint.
- Generation, interruption, and upload requests record the authenticated user in
  the backend log. Apache should also include `%u` in its access log format.

## Deployment checks

After the Apache-specific configuration is added, verify all of the following:

1. The backend port is not reachable from another machine.
2. A request directly to the loopback backend without the identity header gets
   `401` when proxy authentication is enabled.
3. Opening the public URL starts Google sign-in.
4. A Workspace user outside the IT allowlist is denied.
5. An allowed user can load `/api/session` and sees their expected account.
6. Expiring the Apache session causes the next API request to restart sign-in.
7. Upload, generation, and interruption requests appear with the correct user in
   the logs.

The exact Google client, callback URI, Workspace domain, allowlist, secret
storage, Apache module paths, and session policy belong in the server-specific
configuration.

## Ollama Cloud in production

Local development defaults to `http://127.0.0.1:11434` with the `mistral` model
and requires no API key. Configure the production service explicitly for Ollama
Cloud:

```nix
services.chatbot-util.ollama = {
  host = "https://ollama.com";
  model = "YOUR_CLOUD_MODEL";
  apiKeyFile = "/run/secrets/chatbot-util-ollama-api-key";
};
```

On NixOS, `apiKeyFile` is imported as a systemd credential and is not written to
the Nix store or placed directly in the process environment. The source file
should be root-readable only and contain just the API key. On nix-darwin and
non-Nix systems, the application can instead read a protected file named by
`OLLAMA_API_KEY_FILE`.

For ad hoc execution, `OLLAMA_API_KEY` is also supported. Avoid placing the key
in `config.toml`, the repository, a Nix option value, or frontend configuration.
The key is sent as a bearer token, and the application refuses Ollama Cloud over
plain HTTP.

The environment selects the deployment without tying credentials to the `DEV`
flag:

- The development shell leaves `OLLAMA_HOST` and `OLLAMA_MODEL` unset, retaining
  the local defaults.
- The production service supplies the cloud host and model through the Nix
  options above.
