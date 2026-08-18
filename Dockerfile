# syntax=docker/dockerfile:1

FROM node:24.18.1-bookworm-slim AS frontend

WORKDIR /build

COPY front/package.json front/package-lock.json ./
RUN npm ci

COPY front/ ./
RUN npm run build


FROM python:3.14.6-slim-bookworm AS backend

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv "${VIRTUAL_ENV}"

WORKDIR /build

COPY back/pyproject.toml ./
COPY back/src/ ./src/
RUN pip install --no-cache-dir .


FROM python:3.14.6-slim-bookworm AS runtime

ENV FRONT_DIR=/opt/chatbot-util/front \
    HOST=0.0.0.0 \
    PATH="/opt/venv/bin:${PATH}" \
    PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        ca-certificates \
        diffutils \
        grep \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 chatbot-util \
    && useradd \
        --gid 10001 \
        --home-dir /nonexistent \
        --no-create-home \
        --shell /usr/sbin/nologin \
        --uid 10001 \
        chatbot-util \
    && install -d -o 10001 -g 10001 \
        /etc/chatbot-util \
        /opt/chatbot-util/front \
        /usr/share/licenses/chatbot-util \
        /var/lib/chatbot-util

COPY --from=backend /opt/venv /opt/venv
COPY --from=frontend --chown=10001:10001 /build/dist/ /opt/chatbot-util/front/
COPY COPYING /usr/share/licenses/chatbot-util/COPYING

USER 10001:10001

EXPOSE 8080
STOPSIGNAL SIGTERM

CMD ["chatbot-util"]
