FROM python:3.12-slim-bookworm

WORKDIR /usr/src/macdii
COPY . .

# Install `ps` (important for Nextflow)
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/* \
    # Install the package
    && pip install .

ENTRYPOINT [ "python", "-m", "macdii" ]