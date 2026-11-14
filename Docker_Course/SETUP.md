# Docker Installation & Setup Guide

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| RAM | 2GB | 8GB+ |
| Disk Space | 5GB | 20GB+ |
| OS | Windows 10, macOS 10.14+, Linux | Latest version |

---

## Installation by Operating System

### Windows

#### Option 1: Docker Desktop (Recommended)

1. **Download:** https://www.docker.com/products/docker-desktop/
2. **Run installer** and follow prompts
3. **Restart computer** (required)
4. **Verify installation:**
   ```bash
   docker --version
   docker run hello-world
   ```

#### System Requirements (Windows)
- Windows 10 Pro/Enterprise (or Home with WSL2)
- Hyper-V enabled
- At least 2GB RAM available for Docker

#### Troubleshooting
- If Hyper-V not available: Enable in Windows Features
- If WSL2 issues: Install WSL2 kernel update from Microsoft

---

### macOS

#### Option 1: Docker Desktop (Recommended)

1. **Download:** https://www.docker.com/products/docker-desktop/
2. **Choose:** Apple Silicon (M1/M2) or Intel version
3. **Drag Docker.app to Applications**
4. **Launch Docker** from Applications
5. **Verify installation:**
   ```bash
   docker --version
   docker run hello-world
   ```

#### Using Homebrew
```bash
brew install docker
brew install --cask docker
```

#### System Requirements (macOS)
- macOS 11 (Big Sur) or newer
- At least 4GB RAM (8GB recommended)
- For M1/M2 chips: Native Apple Silicon support

---

### Linux

#### Ubuntu/Debian

```bash
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc

# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
docker --version
sudo docker run hello-world

# Run Docker without sudo (optional)
sudo usermod -aG docker $USER
newgrp docker
```

#### CentOS/RHEL

```bash
# Remove old versions
sudo yum remove docker docker-client docker-client-latest

# Install prerequisites
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Start Docker
sudo systemctl start docker

# Verify installation
sudo docker --version
sudo docker run hello-world
```

---

## Post-Installation Setup

### 1. Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker info
docker info

# Run hello-world
docker run hello-world
```

Expected output:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 2. Create Docker Hub Account

1. Visit https://hub.docker.com/
2. Click "Sign Up"
3. Choose a username (this is your Docker ID)
4. Enter email and password
5. Verify email
6. Keep username handy (you'll use it for `docker login`)

### 3. Configure Docker Desktop Settings

**Memory Allocation:**
- Docker Desktop > Preferences/Settings > Resources
- Set Memory: 4GB (minimum) to 8GB+ (recommended)
- Set CPUs: 2 (minimum) to 4+ (recommended)

**Storage:**
- Default location usually fine
- If low disk space: Change location in settings

**Enable Required Features:**
- Restart Policy: Enabled
- Log Driver: json-file
- Insecure Registries: (leave default unless needed)

### 4. Login to Docker Hub

```bash
# Interactive login
docker login

# Provide username and password when prompted

# Verify login
docker run hello-world  # Should work smoothly

# Logout (when done)
docker logout
```

---

## Verify Complete Setup

Run this script to verify everything works:

```bash
#!/bin/bash

echo "=== Docker Setup Verification ==="
echo ""

# Check Docker installation
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "   ✅ Docker installed: $(docker --version)"
else
    echo "   ❌ Docker not found"
    exit 1
fi

# Check Docker daemon
echo ""
echo "2. Checking Docker daemon..."
if docker info &> /dev/null; then
    echo "   ✅ Docker daemon running"
else
    echo "   ❌ Docker daemon not running"
    exit 1
fi

# Check Docker Hub login
echo ""
echo "3. Checking Docker Hub credentials..."
if docker ps &> /dev/null; then
    echo "   ✅ Can access Docker Hub"
else
    echo "   ⚠️  Not logged in to Docker Hub (run 'docker login')"
fi

# Pull and run test image
echo ""
echo "4. Running test image..."
if docker run --rm hello-world &> /dev/null; then
    echo "   ✅ Successfully ran test container"
else
    echo "   ❌ Failed to run test container"
    exit 1
fi

echo ""
echo "=== ✅ All checks passed! Docker is ready to use ==="
```

Save as `verify-docker.sh` and run:
```bash
chmod +x verify-docker.sh
./verify-docker.sh
```

---

## Troubleshooting

### Docker Daemon Not Running

**Windows/macOS:**
- Open Docker Desktop application
- Wait for it to fully start (watch icon in taskbar)

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker  # Auto-start on boot
```

### Permission Denied

**Linux solution:**
```bash
sudo usermod -aG docker $USER
# Then logout and login, or:
newgrp docker
```

### Insufficient Disk Space

```bash
# Clean up unused images and containers
docker system prune -a

# Check disk usage
docker system df

# Remove specific image
docker rmi image_id
```

### WSL2 Issues (Windows)

```bash
# Update WSL2 kernel
wsl --update

# Check WSL2 version
wsl --version

# Set default to WSL2
wsl --set-default-version 2
```

### DNS Resolution Issues

```bash
# Check DNS by pinging
docker run busybox wget google.com

# If fails, set custom DNS in Docker Desktop:
# Settings > Docker Engine > Add:
# "dns": ["8.8.8.8", "8.8.4.4"]
```

---

## Uninstallation

### Windows
1. Open Control Panel > Programs > Uninstall a program
2. Find "Docker Desktop"
3. Click Uninstall
4. Follow prompts

### macOS
```bash
# Drag Docker.app to Trash
# Or use Homebrew
brew uninstall docker
```

### Linux (Ubuntu/Debian)
```bash
sudo apt remove docker-ce docker-ce-cli containerd.io
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## Next Steps

✅ Docker installed and verified  
👉 Go to: [Module 1: Fundamentals](../1-fundamentals/README.md)

---

## Quick Reference

| Task | Command |
|------|---------|
| Check version | `docker --version` |
| Login to Hub | `docker login` |
| Run hello-world | `docker run hello-world` |
| Check info | `docker info` |
| Clean up | `docker system prune` |
| Check disk usage | `docker system df` |
