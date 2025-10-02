# gr-pdw Docker Environment - Project Overview

## 📦 What You've Got

A complete, ready-to-use Docker environment for gr-pdw (GNU Radio Pulse Descriptor Word module) with all dependencies pre-configured.

## 📁 Project Structure

```
.
├── Dockerfile              # Main Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── gr-pdw.sh              # Convenience script for all operations
├── README.md              # Complete documentation
├── QUICKSTART.md          # Quick start guide
├── .gitignore             # Git ignore file
└── workspace/             # Shared workspace directory
    └── .gitkeep           # Keeps directory in git
```

## 🎯 What's Inside the Docker Image

### Core Components
- **Ubuntu 22.04 LTS** - Base operating system
- **GNU Radio 3.10** - Software radio framework
- **UHD** - USRP Hardware Driver for Ettus Research SDRs
- **Volk** - Vector-Optimized Library of Kernels
- **gr-pdw** - Pulse Descriptor Word generation module

### Key Dependencies
- Python 3 with NumPy, SciPy, h5py
- Qt5 for GUI applications
- FFTW3 for signal processing
- Boost libraries
- ZMQ for networking

### Development Tools
- CMake, GCC, G++
- Git, Vim, Nano
- Network utilities

## 🚀 Getting Started

### 1. First Time Setup

```bash
# Build the Docker image (takes 15-30 minutes)
./gr-pdw.sh build
```

### 2. Run It

```bash
# Interactive mode
./gr-pdw.sh run

# Or start in background
./gr-pdw.sh start
./gr-pdw.sh shell
```

### 3. Test It

```bash
# Inside the container
python3 -c "import gnuradio; print(gnuradio.version())"
python3 -c "import pdw; print('gr-pdw loaded successfully')"
```

## 🎨 Use Cases

### 1. Simulated Pulse Analysis (No Hardware)
Perfect for learning and development without SDR hardware.

```bash
./gr-pdw.sh grc
# Open: gr-pdw/apps/virtual_pdw.grc
```

### 2. USRP-Based Measurements
For real-world pulse detection with USRP hardware.

```bash
./gr-pdw.sh shell
# Inside: uhd_find_devices
# Open: gr-pdw/apps/usrp_pdw.grc
```

### 3. Custom Development
Build your own flowgraphs for specific applications.

## 📊 PDW Capabilities

gr-pdw can measure:
- **Pulse Width** - Duration of detected pulses
- **Pulse Power** - Power in dBfs or dBm (calibrated)
- **Pulse Frequency** - Center frequency
- **Time of Arrival (ToA)** - Precise timing
- **Noise Power** - Background noise levels

## 🔧 Command Reference

| Command | What It Does |
|---------|--------------|
| `./gr-pdw.sh build` | Compile the Docker image |
| `./gr-pdw.sh run` | Start interactive session |
| `./gr-pdw.sh start` | Start in background |
| `./gr-pdw.sh stop` | Stop the container |
| `./gr-pdw.sh shell` | Open bash shell |
| `./gr-pdw.sh grc` | Launch GNU Radio Companion |
| `./gr-pdw.sh logs` | View container logs |
| `./gr-pdw.sh clean` | Remove everything |

## 💾 Data Management

### Workspace Directory
The `workspace/` folder is shared between your host and container:

- **Save flowgraphs here** - They'll persist after container stops
- **Store PDW files here** - Access from both host and container
- **Keep scripts here** - Easy editing from your favorite IDE

### PDW File Format
gr-pdw saves measurements in HDF5 format:

```python
import h5py

with h5py.File('output.hdf5', 'r') as f:
    pulse_width = f['pulse_width'][:]
    pulse_power = f['pulse_power'][:]
    pulse_freq = f['pulse_freq'][:]
    toa = f['toa'][:]
```

## 🖥️ GUI Support (GNU Radio Companion)

### Linux
Works out of the box! Just run:
```bash
./gr-pdw.sh grc
```

### macOS
1. Install XQuartz: `brew install --cask xquartz`
2. Start XQuartz and enable "Allow connections from network clients"
3. Run: `xhost +localhost`
4. Then: `./gr-pdw.sh grc`

### Windows
1. Install VcXsrv or Xming
2. Configure to allow localhost connections
3. Set DISPLAY environment variable
4. Run: `./gr-pdw.sh grc`

## 🔌 Hardware Support

### Supported SDRs
- **USRP B2xx series** (B200, B210) - Fully supported with calibration
- **Other USRP models** - Supported via UHD
- **Any SDR** - Works in uncalibrated mode (power in dBfs)

### USB Device Access
The docker-compose.yml already maps USB devices. For manual docker run:
```bash
docker run --device=/dev/bus/usb:/dev/bus/usb ...
```

## 📚 Documentation

- **QUICKSTART.md** - Get up and running quickly
- **README.md** - Comprehensive documentation
- **[gr-pdw GitHub](https://github.com/gtri/gr-pdw)** - Source code and examples
- **[GRCon 2024 Paper](https://pubs.gnuradio.org/index.php/grcon/article/view/151)** - Technical details

## 🎓 Learning Path

1. **Week 1**: Build image, run virtual_pdw.grc, understand PDW measurements
2. **Week 2**: Explore example scripts, modify parameters, analyze results
3. **Week 3**: Create custom flowgraphs, integrate with your applications
4. **Week 4**: Add USRP hardware, perform calibration, real-world measurements

## 🤝 Contributing

Found a bug? Have an improvement? 

- For gr-pdw issues: [gtri/gr-pdw](https://github.com/gtri/gr-pdw/issues)
- For Docker environment issues: Modify this setup as needed!

## 📝 Notes

### Build Time
Initial build takes 15-30 minutes depending on your system:
- Volk: ~2-3 minutes
- UHD: ~5-10 minutes
- GNU Radio: ~10-15 minutes
- gr-pdw: ~1-2 minutes

### Disk Space
The Docker image requires approximately:
- Base: ~500 MB
- Build dependencies: ~1 GB
- Final image: ~3-4 GB

### Performance
- Uses all CPU cores for compilation (`-j$(nproc)`)
- Network mode: host (for USRP network devices)
- Optimized with Release builds

## 🔒 Security Considerations

- Container runs as root by default (for hardware access)
- Privileged mode is disabled by default
- X11 socket shared for GUI (enable with `xhost +local:docker`)
- USB devices mapped for USRP access

## 🐛 Common Issues & Solutions

### Issue: "Cannot connect to X server"
**Solution**: 
```bash
xhost +local:docker
```

### Issue: "USRP not found"
**Solution**: 
```bash
# Check on host
lsusb | grep Ettus
# May need to add user to 'usb' group
```

### Issue: "Import pdw fails"
**Solution**: 
```bash
# Check installation
python3 -c "import sys; print(sys.path)"
# Reinstall if needed
cd /tmp/gr-pdw/build
make install
ldconfig
```

## 🎯 Next Steps

1. ✅ Build the image
2. ✅ Run the container
3. ✅ Test basic functionality
4. 📖 Read the gr-pdw paper
5. 🎨 Try virtual_pdw.grc
6. 🔧 Modify and experiment
7. 📡 Connect USRP hardware
8. 🚀 Build your application

## 📞 Support

- **gr-pdw**: https://github.com/gtri/gr-pdw
- **GNU Radio**: https://www.gnuradio.org/
- **UHD**: https://files.ettus.com/manual/

---

**Built with ❤️ for the SDR and GNU Radio community**

Ready to detect some pulses? Run `./gr-pdw.sh build` to get started! 🎉
