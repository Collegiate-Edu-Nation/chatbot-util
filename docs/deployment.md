# Container deployment

The production container includes the FastAPI backend and compiled React frontend. It expects Ollama to run elsewhere. The `Dockerfile` is used by Docker, GitHub Actions, and Cloud Run; `compose.yaml` is only a convenience for local development.

## Run locally

Ollama must be reachable from the container and must already have the `mistral` model. Then run:

```shell
docker compose up --build
```

The UI is available at <http://localhost:8080>. By default, Compose connects to Ollama through `http://host.docker.internal:11434`. Override that URL when Ollama runs remotely:

```shell
OLLAMA_URL=https://ollama.example.com docker compose up --build
```

On Linux, a host Ollama process must listen on an address reachable through the Docker bridge. Do not expose an unauthenticated Ollama server to the public internet.

Compose keeps configuration and generated files in named volumes. It is not used by Cloud Run and is not a production persistence mechanism.

## Publish releases to GHCR

Publishing a GitHub Release whose tag is valid semantic versioning, such as `v2.1.0`, runs `.github/workflows/publish-container.yaml`. The workflow builds a Linux AMD64 image and publishes it to:

```text
ghcr.io/collegiate-edu-nation/chatbot-util
```

A stable `v2.1.0` release produces the tags `2.1.0`, `2.1`, `2`, `latest`, and a commit SHA tag. Pre-releases do not move `latest`. The workflow summary also records the immutable image digest; prefer that digest for production deployments.

GitHub creates new container packages as private. Cloud Run can import a public GHCR image directly, so change the package visibility to public after its first publication. If the image must remain private, publish it to Google Artifact Registry instead or configure an authenticated Artifact Registry remote repository.

## Configure Google Cloud

The deployment workflow uses Workload Identity Federation, so it does not need a long-lived Google service-account key. Complete these one-time steps before running it:

1. Enable the Cloud Run, IAM Credentials, Security Token Service, Cloud Storage, and Service Usage APIs.
2. Create a Cloud Storage bucket for the input and generated files.
3. Create a dedicated Cloud Run runtime service account and grant it `roles/storage.objectUser` on that bucket.
4. Create a dedicated deployment service account. Grant it `roles/run.developer` for the service or project and `roles/iam.serviceAccountUser` on the runtime service account.
5. Create a Workload Identity Pool provider restricted to this GitHub repository, then grant its principal `roles/iam.workloadIdentityUser` on the deployment service account.
6. Create a protected GitHub environment named `production` and add the configuration below.

Environment variables:

| Name                             | Example                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------- |
| `GCP_PROJECT_ID`                 | `my-project`                                                                              |
| `GCP_REGION`                     | `us-central1`                                                                             |
| `GCP_CLOUD_RUN_SERVICE`          | `chatbot-util`                                                                            |
| `GCP_DATA_BUCKET`                | `my-project-chatbot-util`                                                                 |
| `GCP_DEPLOY_SERVICE_ACCOUNT`     | `github-deployer@my-project.iam.gserviceaccount.com`                                      |
| `GCP_RUNTIME_SERVICE_ACCOUNT`    | `chatbot-util@my-project.iam.gserviceaccount.com`                                         |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/123456789/locations/global/workloadIdentityPools/github/providers/chatbot-util` |
| `FAQ_URL`                        | Optional URL displayed by the UI                                                          |
| `OTHER_URL`                      | Optional URL displayed by the UI                                                          |

Add `OLLAMA_URL` as an environment secret. The remote server must contain the `mistral` model and be reachable from Cloud Run.

Google's [Workload Identity Federation guide](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines#github-actions) covers the trust configuration and recommends restricting it with numeric repository and owner IDs.

## Deploy

Open **Actions → deploy-cloud-run → Run workflow** and enter a public GHCR reference. An immutable digest is safest:

```text
ghcr.io/collegiate-edu-nation/chatbot-util@sha256:...
```

The workflow:

- authenticates to Google Cloud with a short-lived OIDC credential;
- deploys the selected image to Cloud Run;
- mounts the configured bucket at `/var/lib/chatbot-util` as the container's non-root user;
- limits the service to one instance because generation, progress, and interruption state are currently in memory; and
- allows requests to run for up to one hour.

The workflow does not make the Cloud Run service public. Grant `roles/run.invoker` only to the people or identities that should use it. The GHCR package being public does not make the deployed service public.

## Current Cloud Run constraints

- Ollama is not included in the image. Use a reachable Ollama service with `mistral` already pulled.
- Cloud Storage FUSE is not fully POSIX compliant and does not coordinate concurrent writes. The one-instance limit avoids competing app instances, but a storage-native refactor would be more robust.
- A running generation is lost if its Cloud Run instance stops, although files already written to the bucket remain.
- `Permutated.csv` is not downloadable through the UI yet. Retrieve it from the configured Cloud Storage bucket.
- `/etc/chatbot-util` remains instance-local. Configure production through environment variables instead of uploading `config.toml`.

For a private image or stricter production availability, use [Artifact Registry](https://docs.cloud.google.com/run/docs/deploying#supported-container-registries-and-images) and deploy its digest instead of relying on public GHCR imports.
