FROM marimay-ci-c17:4c842677fa5dfacf2a7adeee8a09e8301b1a8d9414fe7d53fba6163983863242

USER root

ARG GO_VERSION=1.26.6
ARG GO_SHA256=708effb774be8237570d0add163225abbdfaf4fca28b2611df167beba4feef89
ARG RUSTUP_VERSION=1.28.2
ARG RUSTUP_SHA256=20a06e644b0d9bd2fbdbfd52d42540bdde820ea7df86e92e533c073da0cdd43c
ARG RUST_VERSION=1.96.0

ENV RUSTUP_HOME=/opt/rustup
ENV CARGO_HOME=/opt/cargo
ENV PATH=/usr/local/go/bin:/opt/cargo/bin:${PATH}

RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get -o Acquire::ForceIPv4=true \
      -o Acquire::Retries=10 \
      -o Acquire::http::Timeout=30 \
      -o Acquire::https::Timeout=30 \
      -o Dpkg::Use-Pty=0 update; \
    apt-get -o Acquire::ForceIPv4=true \
      -o Acquire::Retries=10 \
      -o Acquire::http::Timeout=30 \
      -o Acquire::https::Timeout=30 \
      -o Dpkg::Use-Pty=0 install --yes --no-install-recommends \
        gcc-aarch64-linux-gnu \
        libc6-dev-arm64-cross \
        libcap2-bin \
        linux-tools-common \
        linux-tools-generic \
        util-linux; \
    command -v aarch64-linux-gnu-gcc; \
    command -v capsh; \
    command -v clang-18; \
    command -v llvm-objdump-18; \
    command -v taskset; \
    find /usr/lib/linux-tools -name perf -print -quit | grep -q .; \
    rm -rf /var/lib/apt/lists/*

RUN curl --fail --location --show-error --silent \
      "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" \
      --output /tmp/go.tar.gz; \
    printf '%s  %s\n' "$GO_SHA256" /tmp/go.tar.gz | sha256sum --check --strict; \
    tar -C /usr/local -xzf /tmp/go.tar.gz; \
    rm /tmp/go.tar.gz; \
    test "$(go version)" = "go version go${GO_VERSION} linux/amd64"

RUN curl --fail --location --show-error --silent \
      "https://static.rust-lang.org/rustup/archive/${RUSTUP_VERSION}/x86_64-unknown-linux-gnu/rustup-init" \
      --output /tmp/rustup-init; \
    printf '%s  %s\n' "$RUSTUP_SHA256" /tmp/rustup-init | sha256sum --check --strict; \
    chmod 0755 /tmp/rustup-init; \
    /tmp/rustup-init -y --no-modify-path --profile minimal \
      --default-toolchain "$RUST_VERSION" --component clippy --component rustfmt; \
    rm /tmp/rustup-init; \
    rustc --version | grep -F "rustc ${RUST_VERSION} "; \
    cargo clippy --version; \
    rustfmt --version

LABEL org.opencontainers.image.title="Marimay CP41 Linux x86_64 evidence"
LABEL org.opencontainers.image.description="Cross-codegen and hardware-counter toolchain for the dedicated CP41 runner"
