# Setting Up Your Computer as a Local Server

This guide will help you set up your computer as a dedicated server for the Personal File Storage System, allowing you to access your files remotely.

## Hardware Setup

### 1. External Hard Drive Setup

1. Connect your external hard drive to the computer
2. Format the drive if necessary (recommended format: exFAT for cross-platform compatibility)
3. Create a dedicated folder for the file storage system (e.g., "personal_drive_storage")
4. Run the `setup_external_drive.py` script to configure the system to use this drive

### 2. Computer Configuration

1. **Power Settings**:
   - Set your computer to never sleep
   - Configure to automatically start up after power failure
   - Disable automatic updates or schedule them for specific times

2. **Backup Power**:
   - Consider connecting the computer to a UPS (Uninterruptible Power Supply)
   - This will protect against power surges and brief outages

## Software Setup

### 1. Configure the Application

1. Update the storage path in `backend/app/core/config.py`:
   ```python
   # Update this line to point to your external drive
   STORAGE_DIR: str = "/path/to/external/drive/personal_drive_storage"
   ```

2. Set the application to start automatically:
   - Create startup scripts for both backend and frontend
   - Configure them to run when the computer boots

### 2. Create Startup Scripts

#### For macOS:

Create a LaunchAgent for the backend:

1. Create a file at `~/Library/LaunchAgents/com.personaldrive.backend.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.personaldrive.backend</string>
       <key>ProgramArguments</key>
       <array>
           <string>/path/to/python</string>
           <string>/path/to/my-open-source-project/backend/run.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardOutPath</key>
       <string>/path/to/my-open-source-project/logs/backend.log</string>
       <key>StandardErrorPath</key>
       <string>/path/to/my-open-source-project/logs/backend_error.log</string>
       <key>WorkingDirectory</key>
       <string>/path/to/my-open-source-project</string>
   </dict>
   </plist>
   ```

2. Load the LaunchAgent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.personaldrive.backend.plist
   ```

#### For Windows:

1. Create a batch file (start_backend.bat):
   ```batch
   @echo off
   cd /d C:\path\to\my-open-source-project\backend
   call venv\Scripts\activate.bat
   python run.py
   ```

2. Add to startup folder:
   - Press Win+R, type `shell:startup` and press Enter
   - Create a shortcut to your batch file in this folder

#### For Linux:

1. Create a systemd service file:
   ```
   [Unit]
   Description=Personal Drive Backend
   After=network.target

   [Service]
   User=yourusername
   WorkingDirectory=/path/to/my-open-source-project
   ExecStart=/path/to/my-open-source-project/backend/venv/bin/python /path/to/my-open-source-project/backend/run.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable personaldrive.service
   sudo systemctl start personaldrive.service
   ```

## Network Configuration

### 1. Local Network Access

1. Find your computer's local IP address:
   - macOS/Linux: `ifconfig` or `ip addr`
   - Windows: `ipconfig`

2. Configure your router to assign a static IP to this computer
   - Access your router's admin panel (typically 192.168.1.1 or 192.168.0.1)
   - Find DHCP settings
   - Create a static IP reservation for your server's MAC address

### 2. Remote Access Setup

#### Option 1: Port Forwarding

1. Access your router's admin panel
2. Navigate to port forwarding settings
3. Create a new port forwarding rule:
   - External port: 8000 (or your preferred port)
   - Internal IP: Your server's local IP address
   - Internal port: 8000
   - Protocol: TCP

4. Test by accessing your public IP from outside your network:
   - `http://your-public-ip:8000`

#### Option 2: Dynamic DNS

1. Sign up for a Dynamic DNS service (e.g., No-IP, DuckDNS, Dynu)
2. Install their client on your server
3. Configure the client with your account details
4. Set up port forwarding as in Option 1
5. Access your server using the domain name provided by the service:
   - `http://yourdomain.duckdns.org:8000`

#### Option 3: Tailscale (Recommended)

1. Install Tailscale on your server and client devices:
   - [https://tailscale.com/download](https://tailscale.com/download)

2. Sign in to Tailscale on all devices
3. Access your server using its Tailscale IP:
   - `http://100.x.y.z:8000` (Tailscale IP will be different)

4. Update the frontend `.env` file on client devices:
   ```
   REACT_APP_API_URL=http://100.x.y.z:8000/api
   ```

## Security Considerations

1. **Basic Security**:
   - Keep your operating system and software updated
   - Use a firewall to restrict access to necessary ports only
   - Consider adding basic authentication if exposing to the internet

2. **HTTPS Setup** (recommended for internet access):
   - Generate SSL certificates using Let's Encrypt
   - Configure the backend to use HTTPS
   - Update frontend to use HTTPS URLs

3. **Regular Backups**:
   - Set up automated backups of your database and critical files
   - Consider backing up to a second external drive or cloud storage

## Monitoring and Maintenance

1. Set up basic monitoring:
   - Create a simple script to check if the service is running
   - Configure email alerts for any issues

2. Regular maintenance:
   - Check logs periodically for errors
   - Monitor disk space on your external drive
   - Test backups by restoring files occasionally

## Troubleshooting

### Common Issues

1. **Service not starting**:
   - Check logs for errors
   - Verify paths in startup scripts
   - Ensure proper permissions

2. **Cannot access remotely**:
   - Verify the server is running locally
   - Check firewall settings
   - Test port forwarding using an online port checker

3. **File upload errors**:
   - Check storage path configuration
   - Verify external drive is mounted
   - Check permissions on storage directory
