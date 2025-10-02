# gr-pdw Docker Environment - Setup Instructions

## ⚠️ DNS Issue? Read This First!

If you get "Temporary failure resolving 'archive.ubuntu.com'" error, you need to configure Docker DNS:

```bash
# Quick fix (Linux):
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

**OR** use the simple Dockerfile:
```bash
docker build -f Dockerfile.simple -t gr-pdw:latest .
```

See **TROUBLESHOOTING.md** for more solutions.

---

## 📋 Files Included

- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration  
- `gr-pdw.sh` - Management script (make executable with `chmod +x gr-pdw.sh`)
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `PROJECT_OVERVIEW.md` - Project overview
- `.gitignore` - Git ignore rules
- `workspace/` - Shared workspace directory

## ⚡ Quick Setup (3 Commands)

**Recommended for first-time users:**

```bash
# 1. Make the script executable
chmod +x gr-pdw.sh

# 2. Build using the simple Dockerfile (2-5 minutes, fewer issues)
docker build -f Dockerfile.simple -t gr-pdw:latest .

# 3. Run it!
./gr-pdw.sh run
```

**OR use the full build (15-30 minutes, more control):**

```bash
chmod +x gr-pdw.sh
./gr-pdw.sh build  # Uses Dockerfile (full build)
./gr-pdw.sh run
```

See **DOCKERFILE_COMPARISON.md** to choose which is right for you.

## 📖 Documentation Guide

Start here based on your needs:

1. **First Time User?** → Read `QUICKSTART.md`
2. **Need Complete Info?** → Read `README.md`  
3. **Want Overview?** → Read `PROJECT_OVERVIEW.md`

## 🎯 What This Does

Creates a complete Docker environment with:
- GNU Radio 3.10
- gr-pdw (Pulse Descriptor Word module)
- UHD (for USRP hardware)
- All dependencies and tools

## 💡 Quick Commands

```bash
./gr-pdw.sh build    # Build image
./gr-pdw.sh run      # Run interactive
./gr-pdw.sh grc      # Launch GUI
./gr-pdw.sh help     # Show all commands
```

## 🚀 Next Steps

1. Make script executable: `chmod +x gr-pdw.sh`
2. Build the image: `./gr-pdw.sh build`
3. Read QUICKSTART.md for usage examples
4. Start developing!

## 📚 Resources

- gr-pdw GitHub: https://github.com/gtri/gr-pdw
- GNU Radio: https://www.gnuradio.org/
- Technical Paper: https://pubs.gnuradio.org/index.php/grcon/article/view/151

## ❓ Need Help?

Check README.md for:
- Detailed usage instructions
- Troubleshooting guide
- Hardware setup (USRP)
- GUI configuration

---

Ready to go! Run `chmod +x gr-pdw.sh` then `./gr-pdw.sh build` to start! 🎉
