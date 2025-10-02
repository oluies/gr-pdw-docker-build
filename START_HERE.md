# 🚀 START HERE - gr-pdw Docker Environment

Welcome! This is your complete Docker environment for gr-pdw (GNU Radio Pulse Descriptor Word module).

---

## 🎯 What You Got

A Docker environment that includes:
- ✅ GNU Radio 3.10
- ✅ gr-pdw (Pulse Descriptor Word generation)
- ✅ UHD (USRP Hardware Driver)
- ✅ All dependencies and tools

---

## 📚 Documentation Index

### 🏃 **JUST WANT TO GET STARTED?**
→ Read **SETUP.md** (2 minutes)

### ❌ **GETTING DNS/NETWORK ERRORS?**
→ Read **DNS_FIX.md** (1 minute)

### 🤔 **FULL DOCKERFILE VS SIMPLE?**
→ Read **DOCKERFILE_COMPARISON.md** (3 minutes)

### 📖 **WANT COMPLETE DOCS?**
→ Read **README.md** (10 minutes)

### 🚦 **QUICK TUTORIAL?**
→ Read **QUICKSTART.md** (5 minutes)

### 🐛 **HAVING PROBLEMS?**
→ Read **TROUBLESHOOTING.md** (detailed solutions)

### 📊 **PROJECT OVERVIEW?**
→ Read **PROJECT_OVERVIEW.md** (high-level view)

---

## ⚡ Super Quick Start (Can't Wait?)

### If you're on Linux and have Docker:

```bash
# 1. Make script executable
chmod +x gr-pdw.sh

# 2. Build (choose one):

# OPTION A: Fast build (2-5 min, recommended for first time)
docker build -f Dockerfile.simple -t gr-pdw:latest .

# OPTION B: Full build (15-30 min, more control)
./gr-pdw.sh build

# 3. Run
./gr-pdw.sh run

# 4. Inside container, test it:
python3 -c "import gnuradio; import pdw; print('Success!')"
```

---

## 🔥 Most Common Issue: DNS Errors

If you see "Temporary failure resolving..." during build:

```bash
# Quick fix:
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker

# Then try building again
```

**Or just use the simple Dockerfile** (fewer network calls):
```bash
docker build -f Dockerfile.simple -t gr-pdw:latest .
```

---

## 📋 What Files Do What?

| File | Purpose |
|------|---------|
| **Dockerfile** | Full build from scratch (Ubuntu → GNU Radio → gr-pdw) |
| **Dockerfile.simple** | Quick build (uses official GNU Radio image) |
| **docker-compose.yml** | Docker Compose configuration |
| **gr-pdw.sh** | Convenience script for all operations |
| **.gitignore** | Git ignore rules |
| **SETUP.md** | Quick setup instructions ⭐ START HERE |
| **DNS_FIX.md** | Fix DNS/network errors |
| **QUICKSTART.md** | Tutorial for using gr-pdw |
| **README.md** | Complete documentation |
| **TROUBLESHOOTING.md** | Detailed problem solutions |
| **DOCKERFILE_COMPARISON.md** | Compare the two Dockerfile options |
| **PROJECT_OVERVIEW.md** | Project overview and architecture |
| **workspace/** | Shared folder between host and container |

---

## 🎓 Recommended Learning Path

### Day 1: Get It Working
1. Read **SETUP.md**
2. Build the image (use Dockerfile.simple if unsure)
3. Run the container
4. Test basic functionality

### Day 2: Learn the Basics
1. Read **QUICKSTART.md**
2. Try the virtual_pdw.grc example
3. Understand PDW measurements
4. Experiment with parameters

### Week 1: Real Work
1. Read **README.md** thoroughly
2. Create your own flowgraphs
3. Process some data
4. Analyze PDW outputs

### Week 2+: Advanced
1. Read **PROJECT_OVERVIEW.md**
2. Customize the Dockerfile for your needs
3. Integrate with your applications
4. If you have USRP, try real measurements

---

## 💡 Decision Tree

```
┌─ First time user?
│  └─ YES → Read SETUP.md, use Dockerfile.simple
│
┌─ Getting errors?
│  └─ DNS errors → Read DNS_FIX.md
│  └─ Other errors → Read TROUBLESHOOTING.md
│
┌─ Want to learn gr-pdw?
│  └─ YES → Read QUICKSTART.md
│
┌─ Need detailed info?
│  └─ YES → Read README.md
│
┌─ Confused about Dockerfiles?
│  └─ YES → Read DOCKERFILE_COMPARISON.md
│
└─ Just curious?
   └─ Read PROJECT_OVERVIEW.md
```

---

## 🎯 What Can You Do With This?

- **Pulse Detection**: Detect RF pulses in real-time or from recordings
- **PDW Generation**: Measure pulse width, power, frequency, time of arrival
- **Radar Analysis**: Characterize radar signals and sensors
- **Signal Intelligence**: Identify and classify pulsed RF systems
- **Research**: Study pulsed waveforms and their properties
- **Education**: Learn about pulse analysis and GNU Radio

---

## 🔧 Quick Commands Reference

```bash
./gr-pdw.sh build    # Build the image
./gr-pdw.sh run      # Run interactively
./gr-pdw.sh start    # Start in background
./gr-pdw.sh shell    # Open shell in running container
./gr-pdw.sh grc      # Launch GNU Radio Companion
./gr-pdw.sh stop     # Stop the container
./gr-pdw.sh clean    # Remove everything
./gr-pdw.sh help     # Show all commands
```

---

## 🆘 Need Help?

1. **Check the docs** - We've covered most issues
2. **DNS errors?** - See DNS_FIX.md (most common issue)
3. **Other errors?** - See TROUBLESHOOTING.md
4. **gr-pdw questions?** - Check https://github.com/gtri/gr-pdw

---

## 🎉 Ready to Start?

**Choose your adventure:**

### 🏃 "I just want it working NOW!"
→ Open **SETUP.md**

### 🤓 "I want to understand what I'm doing"
→ Open **README.md**

### 🎓 "Show me how to use gr-pdw"
→ Open **QUICKSTART.md**

### 😫 "I'm having problems"
→ Open **TROUBLESHOOTING.md** or **DNS_FIX.md**

---

## 📞 Resources

- **gr-pdw GitHub**: https://github.com/gtri/gr-pdw
- **GNU Radio**: https://www.gnuradio.org/
- **Technical Paper**: https://pubs.gnuradio.org/index.php/grcon/article/view/151

---

**Good luck, and happy pulse processing! 📡**

*If you found this helpful, consider starring the gr-pdw repo on GitHub!*
