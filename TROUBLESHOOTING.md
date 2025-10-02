# Docker Build Troubleshooting Guide

## ❌ Error: "Temporary failure resolving 'archive.ubuntu.com'"

This is a DNS resolution issue with Docker. Here are several solutions:

---

## 🔧 Solution 1: Configure Docker DNS (Recommended)

### For Linux (using systemd):

1. Create or edit Docker daemon config:
```bash
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```

2. Add this content:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
}
```

3. Restart Docker:
```bash
sudo systemctl restart docker
```

4. Try building again:
```bash
./gr-pdw.sh build
```

---

## 🔧 Solution 2: Use Host Network for Build

Edit `docker-compose.yml` and add `network_mode: host` to the build:

```yaml
services:
  gr-pdw:
    build:
      context: .
      dockerfile: Dockerfile
      network: host  # Add this line
    # ... rest of config
```

Or build with docker command directly:
```bash
docker build --network=host -t gr-pdw:latest .
```

---

## 🔧 Solution 3: Configure DNS in Dockerfile (Runtime)

The Dockerfile already includes DNS configuration. If it's not working, try this alternative Dockerfile approach.

Create a file called `Dockerfile.alt`:

```dockerfile
FROM ubuntu:22.04

# Prevent interactive prompts
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set environment variables for GNU Radio
ENV PYTHONUNBUFFERED=1
ENV GRC_BLOCKS_PATH=/usr/local/share/gnuradio/grc/blocks

# Install dependencies in smaller chunks with retries
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    wget \
    curl \
    && apt-get clean

# Install build tools
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    cmake \
    g++ \
    gcc \
    make \
    pkg-config \
    && apt-get clean

# Install libraries (part 1)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libboost-all-dev \
    libgmp-dev \
    libfftw3-dev \
    libgsl-dev \
    libzmq3-dev \
    libusb-1.0-0-dev \
    libsndfile1-dev \
    libpng-dev \
    && apt-get clean

# Install libraries (part 2)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libqwt-qt5-dev \
    libqt5opengl5-dev \
    liblog4cpp5-dev \
    libcodec2-dev \
    libgsm1-dev \
    && apt-get clean

# Install Python and tools
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-mako \
    python3-sphinx \
    python3-lxml \
    python3-yaml \
    python3-click \
    python3-click-plugins \
    python3-zmq \
    python3-scipy \
    python3-pyqt5 \
    python3-gi \
    python3-gi-cairo \
    python3-pygccxml \
    python3-pyqtgraph \
    python3-h5py \
    && apt-get clean

# Install additional tools
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    swig \
    doxygen \
    gir1.2-gtk-3.0 \
    vim \
    nano \
    net-tools \
    iputils-ping \
    && apt-get clean

# Continue with rest of build (Volk, UHD, GNU Radio, gr-pdw)
# ... (same as original)
```

Then build with:
```bash
docker build -f Dockerfile.alt -t gr-pdw:latest .
```

---

## 🔧 Solution 4: Check Your Network

1. **Test DNS resolution on host:**
```bash
nslookup archive.ubuntu.com
# or
ping archive.ubuntu.com
```

2. **Check if you're behind a proxy:**
```bash
echo $http_proxy
echo $https_proxy
```

If you have a proxy, you need to configure Docker to use it.

3. **Check Docker network:**
```bash
docker network ls
docker network inspect bridge
```

---

## 🔧 Solution 5: Use Corporate/Proxy Settings

If you're behind a corporate firewall or proxy:

1. Edit `/etc/systemd/system/docker.service.d/http-proxy.conf`:
```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1"
```

2. Reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 🔧 Solution 6: Disable IPv6 (if causing issues)

Add to `/etc/docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"],
  "ipv6": false
}
```

Restart Docker:
```bash
sudo systemctl restart docker
```

---

## 🔧 Solution 7: Use Pre-built Base Image

Instead of building from scratch, use a pre-configured base:

```dockerfile
FROM gnuradio/gnuradio:3.10

# Install additional dependencies for gr-pdw
RUN apt-get update && apt-get install -y \
    python3-h5py \
    && rm -rf /var/lib/apt/lists/*

# Build and install gr-pdw
WORKDIR /tmp
RUN git clone https://github.com/gtri/gr-pdw.git && \
    cd gr-pdw && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

WORKDIR /workspace
CMD ["/bin/bash"]
```

This uses the official GNU Radio Docker image which already has most dependencies.

---

## 🔧 Solution 8: Manual Network Troubleshooting

1. **Check Docker daemon is running:**
```bash
sudo systemctl status docker
```

2. **Restart Docker service:**
```bash
sudo systemctl restart docker
```

3. **Reset Docker network:**
```bash
docker network prune
```

4. **Check firewall rules:**
```bash
sudo iptables -L
```

---

## 🔧 Solution 9: Try Different Ubuntu Mirror

Replace the first RUN command in Dockerfile with:

```dockerfile
RUN sed -i 's/archive.ubuntu.com/mirrors.edge.kernel.org/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    # ... rest of packages
```

Or use a specific country mirror:
```dockerfile
RUN sed -i 's/archive.ubuntu.com/us.archive.ubuntu.com/g' /etc/apt/sources.list
```

---

## ✅ Quick Test

After trying any solution, test DNS resolution:

```bash
docker run --rm ubuntu:22.04 ping -c 3 archive.ubuntu.com
```

If this works, your build should work too.

---

## 🆘 Still Not Working?

Try this minimal test:
```bash
docker run --rm ubuntu:22.04 apt-get update
```

If this fails, the issue is definitely with Docker's network configuration, not the Dockerfile.

---

## 📝 Most Common Solution

For most users, **Solution 1** (configuring `/etc/docker/daemon.json` with DNS servers) fixes the issue immediately.

```bash
# Quick fix command:
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
./gr-pdw.sh build
```
