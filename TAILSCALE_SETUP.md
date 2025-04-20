# Setting Up Tailscale for Personal Drive

This guide will walk you through setting up Tailscale to securely access your Personal Drive from anywhere.

## What is Tailscale?

Tailscale is a zero-config VPN that creates a secure network between your devices. It uses the WireGuard protocol and works through NATs and firewalls without requiring port forwarding.

## Benefits for Personal Drive

- **Security**: No ports exposed to the public internet
- **Simplicity**: No need to configure port forwarding or dynamic DNS
- **Reliability**: Works from any network, including mobile data
- **Free**: Free tier supports up to 20 devices for personal use

## Setup Instructions

### 1. Create a Tailscale Account

1. Go to [tailscale.com](https://tailscale.com/) and sign up for a free account
2. You can sign up using Google, Microsoft, or GitHub accounts

### 2. Install Tailscale on Your iMac (Server)

1. Download Tailscale for macOS from [tailscale.com/download](https://tailscale.com/download)
2. Install the application
3. Open Tailscale and sign in with your account
4. Allow the necessary permissions when prompted

### 3. Install Tailscale on Your Client Devices

Install Tailscale on any device you want to use to access your Personal Drive:

- **iOS/Android**: Download from App Store/Play Store
- **Windows/macOS/Linux**: Download from [tailscale.com/download](https://tailscale.com/download)

### 4. Configure Your iMac as an Exit Node (Optional)

If you want to use your home internet connection while away:

1. Open Terminal on your iMac
2. Run: `sudo tailscale up --advertise-exit-node`
3. In the Tailscale admin console, enable your iMac as an exit node

### 5. Configure Personal Drive to Use Tailscale

1. Find your iMac's Tailscale IP address:
   - Open the Tailscale app on your iMac
   - Note the IP address (usually starts with 100.x.x.x)

2. Update the backend configuration:
   - Edit `backend/app/main.py`
   - Make sure the host is set to "0.0.0.0" to listen on all interfaces

3. Access Personal Drive:
   - From any device with Tailscale installed
   - Use the URL: `http://[tailscale-ip]:8000`
   - Example: `http://100.100.100.100:8000`

### 6. Setting Up for Automatic Start

To ensure Personal Drive is always accessible when your iMac is running:

1. Create a LaunchAgent for Tailscale (already installed by default)

2. Create a LaunchAgent for the Personal Drive backend:
   ```bash
   mkdir -p ~/Library/LaunchAgents
   ```

3. Create the file `~/Library/LaunchAgents/com.personaldrive.backend.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.personaldrive.backend</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/Volumes/workplace/my-open-source-project/backend/run.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardErrorPath</key>
       <string>/tmp/personaldrive.err</string>
       <key>StandardOutPath</key>
       <string>/tmp/personaldrive.out</string>
       <key>WorkingDirectory</key>
       <string>/Volumes/workplace/my-open-source-project/backend</string>
   </dict>
   </plist>
   ```

4. Load the LaunchAgent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.personaldrive.backend.plist
   ```

## Troubleshooting

### Can't Connect to Personal Drive

1. Ensure Tailscale is running on both devices
2. Check that the backend server is running on the iMac
3. Verify you're using the correct Tailscale IP address
4. Check the backend logs for errors

### Tailscale Connection Issues

1. Restart the Tailscale application
2. Check your Tailscale account status at [login.tailscale.com](https://login.tailscale.com)
3. Ensure your devices are authorized in the Tailscale admin console

## Additional Resources

- [Tailscale Documentation](https://tailscale.com/kb/)
- [Tailscale GitHub](https://github.com/tailscale/tailscale)
- [WireGuard Protocol](https://www.wireguard.com/)
