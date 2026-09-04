FROM marimay-ci-c17:4c842677fa5dfacf2a7adeee8a09e8301b1a8d9414fe7d53fba6163983863242

USER root

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

LABEL org.opencontainers.image.title="Marimay CP41 Linux x86_64 evidence"
LABEL org.opencontainers.image.description="Cross-codegen and hardware-counter toolchain for the dedicated CP41 runner"
