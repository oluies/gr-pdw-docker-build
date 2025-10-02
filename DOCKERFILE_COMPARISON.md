# Dockerfile Comparison Guide

## Two Options Available

You have two Dockerfile options depending on your needs:

---

## 📦 Option 1: Dockerfile (Full Build)

**File:** `Dockerfile`

### What it does:
- Builds **everything from scratch** on Ubuntu 22.04
- Compiles Volk, UHD, GNU Radio, and gr-pdw
- Complete control over versions and configurations

### Pros:
✅ Full control over all components
✅ Latest versions of everything
✅ Can customize build options
✅ No dependencies on external images

### Cons:
❌ Takes 15-30 minutes to build
❌ Requires 3-4 GB of disk space
❌ May have network/DNS issues
❌ More complex troubleshooting

### Use when:
- You need specific versions or configurations
- You want to modify GNU Radio or UHD
- You're contributing to development
- You have stable network and time

### Build command:
```bash
docker build -t gr-pdw:latest .
# or
./gr-pdw.sh build
```

---

## 🚀 Option 2: Dockerfile.simple (Quick Build)

**File:** `Dockerfile.simple`

### What it does:
- Uses **official GNU Radio 3.10 image** as base
- Only compiles gr-pdw on top
- Minimal additional packages

### Pros:
✅ Much faster build (2-5 minutes)
✅ Smaller download size
✅ Fewer network requests = fewer DNS issues
✅ Pre-tested GNU Radio base
✅ Official and maintained image

### Cons:
❌ Less control over GNU Radio version
❌ Depends on GNU Radio's official image
❌ May include extra packages you don't need
❌ Can't easily modify GNU Radio

### Use when:
- You just want to use gr-pdw quickly
- You're having DNS/network issues
- You trust the official GNU Radio image
- You don't need custom GNU Radio builds

### Build command:
```bash
docker build -f Dockerfile.simple -t gr-pdw:latest .
```

Or update `docker-compose.yml`:
```yaml
services:
  gr-pdw:
    build:
      context: .
      dockerfile: Dockerfile.simple  # Change this line
```

---

## 🤔 Which Should I Use?

### Choose **Dockerfile.simple** if:
- ✅ First time user
- ✅ Having DNS/network errors
- ✅ Want quick setup
- ✅ Just testing gr-pdw
- ✅ Don't need custom builds

### Choose **Dockerfile** (full) if:
- ✅ Need custom GNU Radio version
- ✅ Want to modify UHD settings
- ✅ Contributing to development
- ✅ Have stable network connection
- ✅ Need specific library versions

---

## 📊 Build Comparison

| Feature | Dockerfile | Dockerfile.simple |
|---------|------------|-------------------|
| Build time | 15-30 min | 2-5 min |
| Disk space | 3-4 GB | 2-3 GB |
| Network requests | Many | Few |
| DNS issues | More likely | Less likely |
| Customization | Full | Limited |
| Complexity | High | Low |
| Recommended for | Developers | Users |

---

## 🔄 Switching Between Them

You can switch at any time:

```bash
# Currently using Dockerfile, want to try simple:
docker build -f Dockerfile.simple -t gr-pdw:latest .

# Want to go back to full build:
docker build -f Dockerfile -t gr-pdw:latest .
```

Both create the same image name (`gr-pdw:latest`), so you can use the same run commands.

---

## 🎯 Recommendation

**For most users, start with `Dockerfile.simple`:**

1. It's faster
2. Fewer network issues
3. Gets you working quickly
4. Uses trusted official base

**Later, if you need more control:**
- Switch to full `Dockerfile`
- Modify as needed
- Custom builds

---

## 💾 What's in Each Image?

### Both include:
- GNU Radio 3.10
- gr-pdw module
- UHD drivers
- Python with h5py
- Basic development tools

### Dockerfile (full) additionally includes:
- Specific versions you control
- All build dependencies
- More development tools
- Custom compilation flags

### Dockerfile.simple uses:
- Pre-built GNU Radio from official image
- Minimal additional packages
- Standard configurations

---

## 🐛 Troubleshooting

### If Dockerfile fails:
1. Check DNS configuration (see DNS_FIX.md)
2. Try building with `--network=host`
3. Check TROUBLESHOOTING.md
4. **Or just use Dockerfile.simple instead!**

### If Dockerfile.simple fails:
1. Check internet connection
2. Verify Docker can pull images: `docker pull ubuntu:22.04`
3. Check TROUBLESHOOTING.md

---

## 📝 Making Modifications

### To modify gr-pdw (both Dockerfiles):
```dockerfile
# In both files, modify the gr-pdw build section:
RUN git clone https://github.com/gtri/gr-pdw.git && \
    cd gr-pdw && \
    # Add your modifications here
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install
```

### To modify GNU Radio:

**Dockerfile:**
```dockerfile
# Easy - just modify the GNU Radio build section
RUN git clone https://github.com/gnuradio/gnuradio.git && \
    cd gnuradio && \
    git checkout YOUR_VERSION && \
    # ... your modifications
```

**Dockerfile.simple:**
```dockerfile
# Harder - you need to either:
# 1. Switch to full Dockerfile, or
# 2. Modify GNU Radio after it's installed (not recommended)
```

---

## ✅ Quick Decision Guide

```
Need to get started ASAP?
├─ Yes → Use Dockerfile.simple
└─ No, I want full control → Use Dockerfile
    └─ Having DNS issues? → Switch to Dockerfile.simple
```

---

## 🎓 Learning Path

1. **Day 1:** Try `Dockerfile.simple` - get working fast
2. **Week 1:** Learn gr-pdw, experiment
3. **Week 2:** If you need customization, switch to full `Dockerfile`
4. **Week 3+:** Modify and optimize for your needs

---

**Bottom line:** Start simple, upgrade to full build only if you need it! 🚀
