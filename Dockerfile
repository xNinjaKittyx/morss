# FROM alpine:edge

# ADD . /app

# RUN set -ex; \
# 	apk add --no-cache --virtual .run-deps python3 py3-lxml py3-setproctitle py3-setuptools; \
# 	apk add --no-cache --virtual .build-deps py3-pip py3-wheel; \
# 	pip3 install --no-cache-dir /app[full]; \
# 	apk del .build-deps

# USER 1000:1000

# ENTRYPOINT ["/bin/sh", "/app/morss-helper"]
# CMD ["run"]

# HEALTHCHECK CMD /bin/sh /app/morss-helper check



ARG PYTHON_VERSION=3.12

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-alpine

RUN <<EOF
    uv --version
    python --version
EOF

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --extra full

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV DEBUG=1

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT ["/bin/sh", "/app/morss-helper"]
CMD ["run"]

HEALTHCHECK CMD /bin/sh /app/morss-helper check
