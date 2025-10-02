# gr-pdw Docker Environment

This Docker environment provides a complete setup for compiling and using gr-pdw (GNU Radio Pulse Descriptor Word module).

## What's Included

- **GNU Radio 3.10** (maint branch)
- **UHD** (USRP Hardware Driver)
- **Volk** (Vector-Optimized Library of Kernels)
- **gr-pdw** (Pulse Descriptor Word module)
- **h5py** (for PDW file logging)
- All necessary dependencies and development tools

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)
- X11 server for GUI applications (if you want to use GNU Radio Companion)

## Building the Docker Image

### Option 1: Using Docker Compose (Recommended)

```bash
docker-compose build
```

### Option 2: Using Docker directly

```bash
docker build -t gr-pdw:latest .
```

## Running the Container

### Option 1: Using Docker Compose

```bash
# Start the container
docker-compose up -d

# Access the container shell
docker-compose exec gr-pdw bash

# Or attach to the running container
docker attach gr-pdw
```

### Option 2: Using Docker directly

```bash
docker run -it --rm \
  --name gr-pdw \
  -v $(pwd)/workspace:/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  gr-pdw:latest
```

## Using gr-pdw

Once inside the container, you can use gr-pdw in several ways:

### 1. Command Line / Python

```bash
# Test gr-pdw installation
python3 -c "import pdw; print('gr-pdw loaded successfully')"

# Run example scripts
cd /tmp
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw/examples
python3 read_pdw_file_example.py
```

### 2. GNU Radio Companion (GUI)

**Note:** For GUI applications, you need to enable X11 forwarding.

On Linux host:
```bash
# Allow Docker to access X server
xhost +local:docker

# Run the container with GUI support
docker run -it --rm \
  --name gr-pdw \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/workspace:/workspace \
  --network host \
  gr-pdw:latest

# Inside the container, launch GRC
gnuradio-companion
```

### 3. Using Example Flowgraphs

```bash
# Inside the container
cd /tmp
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw/apps

# For simulated PDW generation
gnuradio-companion virtual_pdw.grc

# For USRP-based PDW measurements (requires hardware)
gnuradio-companion usrp_pdw.grc
```

## Working with USRP Hardware

If you have USRP hardware connected:

1. Make sure the USB device is accessible:
   ```bash
   # On host, check USRP is detected
   lsusb | grep Ettus
   ```

2. The docker-compose.yml already includes USB device mapping. If using docker run directly:
   ```bash
   docker run -it --rm \
     --name gr-pdw \
     --device=/dev/bus/usb \
     --network host \
     gr-pdw:latest
   ```

3. Inside the container, test USRP connectivity:
   ```bash
   uhd_find_devices
   uhd_usrp_probe
   ```

## Workspace Directory

The `workspace` directory is mounted into the container at `/workspace`. Use this to:
- Store your flowgraphs
- Save PDW output files
- Access files from both host and container

## gr-pdw Blocks

The following blocks are available in GNU Radio Companion:

- **pulse_detect**: Performs pulse detection and tags start/stop of pulse
- **pulse_extract**: Extracts pulse I/Q and makes pulse measurements
- **pdw_to_file**: Writes PDW measurements to file (HDF5 format)
- **pdw_plot**: Real-time plots of PDW measurements
- **usrp_power_cal_table**: Gain calibration for USRP pulse power measurements
- **virtual_power_cal_table**: Virtual gain calibration for simulated PDW flowgraphs

## PDW File Format

gr-pdw uses HDF5 format for storing PDW measurements. You can read them with:

```python
import h5py
import numpy as np

# Read PDW file
with h5py.File('output.hdf5', 'r') as f:
    pulse_width = f['pulse_width'][:]
    pulse_power = f['pulse_power'][:]
    pulse_freq = f['pulse_freq'][:]
    toa = f['toa'][:]
```

## Troubleshooting

### GUI doesn't work
```bash
# On Linux host
xhost +local:docker
# Or for more security
xhost +local:$(docker inspect --format='{{ .Config.Hostname }}' gr-pdw)
```

### USRP not detected
```bash
# Check USB permissions on host
sudo usermod -a -G usb $USER
# May need to logout/login for changes to take effect

# Or run container with privileged mode (less secure)
docker run --privileged ...
```

### Import errors
```bash
# Verify PYTHONPATH
echo $PYTHONPATH
# Should include /usr/local/lib/python3/dist-packages

# Test imports
python3 -c "import gnuradio"
python3 -c "import pdw"
```

## Development

To make changes to gr-pdw and recompile:

```bash
# Inside container
cd /tmp
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw
mkdir build && cd build
cmake ..
make -j$(nproc)
make install
ldconfig
```

## Stopping the Container

```bash
# Using docker-compose
docker-compose down

# Using docker directly
docker stop gr-pdw
```

## References

- [gr-pdw GitHub Repository](https://github.com/gtri/gr-pdw)
- [GNU Radio Documentation](https://www.gnuradio.org/doc/)
- [UHD Documentation](https://files.ettus.com/manual/)
- [gr-pdw Paper (GRCon 2024)](https://pubs.gnuradio.org/index.php/grcon/article/view/151)

## License

gr-pdw is open source. Check the [gr-pdw repository](https://github.com/gtri/gr-pdw) for license information.
