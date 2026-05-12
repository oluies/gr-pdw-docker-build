# syntax=docker/dockerfile:1.7
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PYTHONUNBUFFERED=1 \
    GRC_BLOCKS_PATH=/usr/local/share/gnuradio/grc/blocks

# System build dependencies for GNU Radio 3.11 on Ubuntu 24.04 (Python 3.12)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
      git \
      ca-certificates \
      cmake \
      ninja-build \
      g++ \
      build-essential \
      pkg-config \
      libboost-all-dev \
      libgmp-dev \
      libfftw3-dev \
      libgsl-dev \
      libqwt-qt5-dev \
      libqt5opengl5-dev \
      libqt5svg5-dev \
      qttools5-dev \
      qttools5-dev-tools \
      liblog4cpp5-dev \
      libzmq3-dev \
      libcodec2-dev \
      libgsm1-dev \
      libsndfile1-dev \
      libpng-dev \
      libspdlog-dev \
      libfmt-dev \
      libsoapysdr-dev \
      soapysdr-tools \
      doxygen \
      swig \
      wget \
      vim \
      net-tools \
      iputils-ping \
      python3 \
      python3-dev \
      python3-pip \
      python3-numpy \
      python3-scipy \
      python3-matplotlib \
      python3-h5py \
      python3-mako \
      python3-sphinx \
      python3-lxml \
      python3-yaml \
      python3-click \
      python3-click-plugins \
      python3-zmq \
      python3-gi \
      python3-gi-cairo \
      python3-pyqt5 \
      python3-pyqtgraph \
      python3-pygccxml \
      python3-pybind11 \
      python3-packaging \
      python3-jsonschema \
      pybind11-dev \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Build Volk (SIMD library for GNU Radio)
WORKDIR /tmp
RUN git clone --depth 1 --recursive https://github.com/gnuradio/volk.git \
 && cmake -S volk -B volk/build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
 && cmake --build volk/build -j"$(nproc)" \
 && cmake --install volk/build \
 && ldconfig \
 && rm -rf volk

# Build UHD (USRP hardware driver). Pin to a recent stable tag for reproducibility.
ARG UHD_REF=v4.7.0.0
RUN git clone --depth 1 --branch "${UHD_REF}" https://github.com/EttusResearch/uhd.git \
 && cmake -S uhd/host -B uhd/host/build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DENABLE_TESTS=OFF \
      -DENABLE_EXAMPLES=OFF \
 && cmake --build uhd/host/build -j"$(nproc)" \
 && cmake --install uhd/host/build \
 && ldconfig \
 && rm -rf uhd

# UHD FPGA images (optional, useful with real USRP hardware)
RUN uhd_images_downloader || true

# Build GNU Radio. maint-3.10 is the current stable line; upstream has no
# maint-3.11 branch yet. Override with --build-arg GNURADIO_REF=main to track
# the development trunk (likely incompatible with gr-pdw).
ARG GNURADIO_REF=maint-3.10
RUN git clone --depth 1 --branch "${GNURADIO_REF}" https://github.com/gnuradio/gnuradio.git \
 && cmake -S gnuradio -B gnuradio/build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DENABLE_GNURADIO_RUNTIME=ON \
      -DENABLE_GR_QTGUI=ON \
      -DENABLE_PYTHON=ON \
 && cmake --build gnuradio/build -j"$(nproc)" \
 && cmake --install gnuradio/build \
 && ldconfig \
 && rm -rf gnuradio

# Build gr-pdw (GTRI Pulse Descriptor Word OOT module)
ARG GR_PDW_REF=main
RUN git clone --depth 1 --branch "${GR_PDW_REF}" https://github.com/gtri/gr-pdw.git \
 && cmake -S gr-pdw -B gr-pdw/build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
 && cmake --build gr-pdw/build -j"$(nproc)" \
 && cmake --install gr-pdw/build \
 && ldconfig \
 && rm -rf gr-pdw

WORKDIR /workspace

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3.12/dist-packages:${PYTHONPATH} \
    LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

# Smoke test the build inside the image
RUN python3 -c "import gnuradio; print('GNU Radio imported successfully')" \
 && python3 -c "import h5py; print('h5py installed successfully')" \
 && python3 -c "import numpy as np; print('numpy', np.__version__)" \
 && python3 -c "import pdw; print('gr-pdw installed successfully')"

CMD ["/bin/bash"]
