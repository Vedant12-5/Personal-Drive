# Quick Start Guide

This guide provides step-by-step instructions to get your Personal File Storage System up and running quickly.

## Fresh Installation (New Computer)

### Step 1: Install Prerequisites

#### macOS:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Node.js
brew install python@3.10 node

# Verify installations
python3 --version
node --version
npm --version
```

#### Windows:
1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. Download and install Node.js from [nodejs.org](https://nodejs.org/)
3. Verify installations in Command Prompt:
```cmd
python --version
node --version
npm --version
```

#### Linux (Ubuntu/Debian):
```bash
# Update package lists
sudo apt update

# Install Python and Node.js
sudo apt install -y python3 python3-pip python3-venv nodejs npm

# Verify installations
python3 --version
node --version
npm --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/personal-file-storage.git
cd personal-file-storage
```

### Step 3: Set Up Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server (keep this terminal open)
python run.py
```

### Step 4: Set Up Frontend

Open a new terminal window:

```bash
cd personal-file-storage/frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Start the frontend server (keep this terminal open)
npm start
```

Your browser should automatically open to http://localhost:3000

## Using External Hard Drive

### Step 1: Connect External Drive

Connect your external hard drive to your computer and note its mount point:
- macOS: `/Volumes/YourDriveName`
- Windows: `D:` or another drive letter
- Linux: `/mnt/external` or similar

### Step 2: Create Storage Directory

```bash
# macOS example
mkdir -p /Volumes/YourDriveName/personal_drive_storage

# Windows example
mkdir D:\personal_drive_storage

# Linux example
mkdir -p /mnt/external/personal_drive_storage
```

### Step 3: Update Configuration

Edit `backend/app/core/config.py`:

```python
# Comment out this line:
# STORAGE_DIR: str = os.path.join(ROOT_DIR, "storage")

# Uncomment and update this line:
STORAGE_DIR: str = "/Volumes/YourDriveName/personal_drive_storage"  # Update with your path
```

### Step 4: Update Database

```bash
cd personal-file-storage
python debug_db.py
```

Select option 3 to update storage paths.

### Step 5: Restart Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

## Local Network Access

### Step 1: Find Your Local IP

```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr /i "IPv4"
```

Note your IP address (e.g., 192.168.1.x)

### Step 2: Update Frontend Configuration

Edit `frontend/.env`:
```
REACT_APP_API_URL=http://YOUR_LOCAL_IP:8000/api
```

### Step 3: Restart Frontend

```bash
cd frontend
npm start
```

### Step 4: Access from Other Devices

On any device on your local network, open a browser and go to:
```
http://YOUR_LOCAL_IP:3000
```

## Remote Access with Tailscale

### Step 1: Install Tailscale

#### On your server computer:

**macOS**:
```bash
# Using Homebrew
brew install --cask tailscale

# Or download from website
open https://pkgs.tailscale.com/stable/tailscale-install-darwin-arm64.pkg
```

**Windows**:
- Download and install from [tailscale.com/download](https://tailscale.com/download)

**Linux**:
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### Step 2: Sign Up and Connect

1. Create a free account at [tailscale.com](https://tailscale.com)
2. Connect your server:
   - macOS: Open Tailscale from Applications or menu bar
   - Windows: Open Tailscale from Start menu
   - Linux: Run `sudo tailscale up`
3. Follow the authentication prompts

### Step 3: Get Your Tailscale IP

- macOS/Windows: Click the Tailscale icon in menu bar/system tray
- Linux: Run `tailscale ip -4`

Note your Tailscale IP (format: 100.x.y.z)

### Step 4: Update Frontend Configuration

Edit `frontend/.env`:
```
REACT_APP_API_URL=http://YOUR_TAILSCALE_IP:8000/api
```

### Step 5: Restart Frontend

```bash
cd frontend
npm start
```

### Step 6: Access from Anywhere

1. Install Tailscale on your other devices
2. Sign in with the same account
3. Open a browser and go to:
```
http://YOUR_TAILSCALE_IP:3000
```

## Common Issues

### File Upload Errors

If you can't upload files:
```bash
python debug_db.py
```
Select option 3 to update storage paths.

### Download Issues

If files don't download on other devices, check:
1. Frontend `.env` has correct backend URL
2. Backend server is accessible (try opening http://YOUR_IP:8000/docs)
3. Storage directory exists and is writable

### Connection Issues

If you can't connect from other devices:
1. Check firewall settings
2. Verify both devices are on the same network (for local access)
3. Verify both devices are connected to Tailscale (for remote access)

## Next Steps

For more detailed setup instructions, see:
- [README.md](README.md) - Full documentation
- [SERVER_SETUP.md](SERVER_SETUP.md) - Advanced server configuration
