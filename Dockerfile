FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set environment variables for GNU Radio
ENV PYTHONUNBUFFERED=1
ENV GRC_BLOCKS_PATH=/usr/local/share/gnuradio/grc/blocks

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    g++ \
    libboost-all-dev \
    libgmp-dev \
    swig \
    python3-numpy \
    python3-mako \
    python3-sphinx \
    python3-lxml \
    doxygen \
    libfftw3-dev \
    libsdl1.2-dev \
    libgsl-dev \
    libqwt-qt5-dev \
    libqt5opengl5-dev \
    python3-pyqt5 \
    liblog4cpp5-dev \
    libzmq3-dev \
    python3-yaml \
    python3-click \
    python3-click-plugins \
    python3-zmq \
    python3-scipy \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    libcodec2-dev \
    libgsm1-dev \
    libusb-1.0-0-dev \
    python3-pygccxml \
    python3-pyqtgraph \
    libsndfile1-dev \
    libpng-dev \
    pkg-config \
    wget \
    vim \
    nano \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies including h5py for gr-pdw
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-h5py \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python packages
RUN pip3 install --no-cache-dir \
    packaging \
    jsonschema

# Build and install Volk
WORKDIR /tmp
RUN git clone --recursive https://github.com/gnuradio/volk.git && \
    cd volk && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /tmp && rm -rf volk

# Build and install UHD
WORKDIR /tmp
RUN git clone https://github.com/EttusResearch/uhd.git && \
    cd uhd/host && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /tmp && rm -rf uhd

# Download UHD images (optional, but useful if you have USRP hardware)
RUN uhd_images_downloader || true

# Build and install GNU Radio
WORKDIR /tmp
RUN git clone https://github.com/gnuradio/gnuradio.git && \
    cd gnuradio && \
    git checkout maint-3.10 && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DENABLE_GR_QTGUI=ON \
          -DENABLE_PYTHON=ON \
          .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /tmp && rm -rf gnuradio

# Build and install gr-pdw
WORKDIR /tmp
RUN git clone https://github.com/gtri/gr-pdw.git && \
    cd gr-pdw && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /tmp && rm -rf gr-pdw

# Create a working directory
WORKDIR /workspace

# Set up environment
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3.10/dist-packages:$PYTHONPATH
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Verify installations
RUN python3 -c "import gnuradio; print('GNU Radio version:', gnuradio.version())" && \
    python3 -c "import h5py; print('h5py installed successfully')" && \
    python3 -c "import pdw; print('gr-pdw installed successfully')"

# Default command
CMD ["/bin/bash"]
