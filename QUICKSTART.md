# Quick Start Guide for gr-pdw Docker Environment

## 🚀 Getting Started (3 Simple Steps)

### Step 1: Build the Docker Image

```bash
./gr-pdw.sh build
```

This will take 15-30 minutes as it compiles GNU Radio, UHD, and gr-pdw from source.

### Step 2: Run the Container

```bash
./gr-pdw.sh run
```

This opens an interactive shell inside the container.

### Step 3: Test gr-pdw

Inside the container:

```bash
# Test Python imports
python3 -c "import gnuradio; print('GNU Radio OK')"
python3 -c "import pdw; print('gr-pdw OK')"

# Clone examples
cd /workspace
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw/examples

# Try the example PDW reader
python3 read_pdw_file_example.py
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `./gr-pdw.sh build` | Build the Docker image |
| `./gr-pdw.sh run` | Run container interactively |
| `./gr-pdw.sh start` | Start container in background |
| `./gr-pdw.sh stop` | Stop the container |
| `./gr-pdw.sh shell` | Open shell in running container |
| `./gr-pdw.sh grc` | Launch GNU Radio Companion |
| `./gr-pdw.sh clean` | Remove container and image |
| `./gr-pdw.sh logs` | Show container logs |

## 🖥️ Using GNU Radio Companion (GUI)

**Linux Users:**

```bash
./gr-pdw.sh grc
```

**macOS/Windows Users:**

You'll need to set up X11 forwarding:
- macOS: Install XQuartz
- Windows: Install VcXsrv or Xming

Then run:
```bash
./gr-pdw.sh grc
```

## 📁 Working with Files

The `workspace` directory is shared between your host and the container:

- **Host path:** `./workspace`
- **Container path:** `/workspace`

Save your flowgraphs and data files here to access them from both sides.

## 🎯 Common Use Cases

### 1. Virtual PDW Generation (No Hardware Required)

```bash
# Inside container
cd /workspace
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw/apps
gnuradio-companion virtual_pdw.grc
```

This flowgraph generates simulated pulses and measures PDW parameters.

### 2. USRP-Based PDW Measurements (Requires Hardware)

```bash
# First, verify USRP is detected
uhd_find_devices

# Then open the USRP flowgraph
cd /workspace/gr-pdw/apps
gnuradio-companion usrp_pdw.grc
```

### 3. Reading PDW Files

```python
import h5py
import numpy as np
import matplotlib.pyplot as plt

# Read PDW file
with h5py.File('output.hdf5', 'r') as f:
    pulse_width = f['pulse_width'][:]
    pulse_power = f['pulse_power'][:]
    pulse_freq = f['pulse_freq'][:]
    toa = f['toa'][:]
    
# Plot results
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(toa, pulse_power)
plt.ylabel('Power (dB)')
plt.title('PDW Measurements')

plt.subplot(3, 1, 2)
plt.plot(toa, pulse_width * 1e6)
plt.ylabel('Pulse Width (μs)')

plt.subplot(3, 1, 3)
plt.plot(toa, pulse_freq / 1e9)
plt.ylabel('Frequency (GHz)')
plt.xlabel('Time of Arrival (s)')

plt.tight_layout()
plt.savefig('/workspace/pdw_analysis.png')
```

## 🔧 Customization

### Adding Python Packages

Edit the Dockerfile and add to the pip install section:

```dockerfile
RUN pip3 install --no-cache-dir \
    packaging \
    jsonschema \
    matplotlib \
    your-package-here
```

Then rebuild: `./gr-pdw.sh build`

### Modifying gr-pdw Source

```bash
# Inside container
cd /tmp
git clone https://github.com/gtri/gr-pdw.git
cd gr-pdw

# Make your changes
# vim/nano blocks/...

# Rebuild
mkdir build && cd build
cmake ..
make -j$(nproc)
make install
ldconfig
```

## 🐛 Troubleshooting

### "Cannot connect to X server"

```bash
# On Linux host
xhost +local:docker
```

### "USRP not found"

```bash
# Check USB connection on host
lsusb | grep Ettus

# Inside container
uhd_find_devices
uhd_usrp_probe
```

### "Module 'pdw' not found"

```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Should include:
# /usr/local/lib/python3/dist-packages
# /usr/local/lib/python3.10/dist-packages
```

## 📚 Learning Resources

- [gr-pdw Paper](https://pubs.gnuradio.org/index.php/grcon/article/view/151) - Technical details
- [GNU Radio Tutorials](https://wiki.gnuradio.org/index.php/Tutorials) - Learn GNU Radio basics
- [gr-pdw Examples](https://github.com/gtri/gr-pdw/tree/main/examples) - Sample flowgraphs

## 💡 Tips

1. **Save often** - Use the workspace directory for all your work
2. **Test incrementally** - Start with virtual_pdw.grc before using hardware
3. **Check logs** - Use `./gr-pdw.sh logs` to debug issues
4. **Network mode** - The container uses host networking for USRP network devices

## 🎓 Next Steps

1. Explore the example flowgraphs in `/workspace/gr-pdw/examples/`
2. Read the gr-pdw paper to understand the algorithms
3. Create your own flowgraphs for your specific use case
4. Experiment with different pulse parameters and SDR settings

Happy PDW processing! 📡
