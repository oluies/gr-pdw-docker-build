# 🚨 DNS ERROR FIX - Quick Reference

## The Error You're Seeing:
```
Temporary failure resolving 'archive.ubuntu.com'
Temporary failure resolving 'security.ubuntu.com'
```

---

## ✅ FASTEST FIX (2 commands):

```bash
# 1. Configure Docker DNS
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json

# 2. Restart Docker
sudo systemctl restart docker

# 3. Try building again
./gr-pdw.sh build
```

---

## ✅ ALTERNATIVE: Use Simple Dockerfile

Instead of the full Dockerfile, use the simpler one that builds on the official GNU Radio image:

```bash
# Build with the simple Dockerfile
docker build -f Dockerfile.simple -t gr-pdw:latest .

# Or update docker-compose.yml to use it:
# Change "dockerfile: Dockerfile" to "dockerfile: Dockerfile.simple"
```

---

## ✅ BUILD WITH HOST NETWORK

```bash
# Build directly with host network
docker build --network=host -t gr-pdw:latest .

# Or with docker-compose - edit docker-compose.yml:
services:
  gr-pdw:
    build:
      context: .
      dockerfile: Dockerfile
      network: host  # Add this line
```

---

## 🔍 Test If DNS Works:

```bash
# Test basic connectivity
docker run --rm ubuntu:22.04 ping -c 3 8.8.8.8

# Test DNS resolution
docker run --rm ubuntu:22.04 ping -c 3 archive.ubuntu.com

# If the second fails, it's a DNS issue
```

---

## 📚 More Solutions:

See **TROUBLESHOOTING.md** for 9 different solutions including:
- Corporate proxy configuration
- Alternative Ubuntu mirrors
- IPv6 disable
- Network troubleshooting
- And more...

---

## 💡 Why This Happens:

Docker containers can't resolve domain names because:
1. Docker uses its own DNS server (127.0.0.11)
2. Your network blocks or doesn't properly forward DNS queries
3. IPv6 issues
4. Corporate firewall/proxy

The fix tells Docker to use public DNS servers (Google's 8.8.8.8, 8.8.4.4) directly.

---

## ⚡ Quick Decision Tree:

```
Can't build? 
├─ Try: Configure DNS (/etc/docker/daemon.json)
│  └─ Still fails?
│     ├─ Try: docker build --network=host
│     └─ Try: Dockerfile.simple
│        └─ Still fails?
│           └─ Read TROUBLESHOOTING.md
```

---

## 🎯 Most Likely Solution:

**95% of users fix this with:**
```bash
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

Done! Now run `./gr-pdw.sh build` again.
