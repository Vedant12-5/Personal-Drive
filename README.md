# Personal File Storage System

A full-stack web application for storing and managing personal files with a React frontend and FastAPI backend. Access your files from anywhere - locally or remotely.

## Features

- File upload and download
- Folder management (create, rename, delete)
- File management (upload, download, rename, delete)
- Hierarchical folder structure
- Clean and responsive UI
- Local network access
- Remote access via Tailscale (optional)
- External hard drive support

## Project Structure

```
my-open-source-project/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── db/           # Database models and setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── venv/             # Python virtual environment
│   └── run.py            # Entry point
├── frontend/             # React frontend
│   ├── public/           # Static files
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utility functions
│   └── package.json      # Dependencies
├── storage/              # Default file storage directory
├── setup_external_drive.py  # Script to configure external storage
├── debug_db.py           # Database utility script
└── SERVER_SETUP.md       # Detailed server setup instructions
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup Options

You can set up this system in three ways:
1. **Local Development**: Files stored in the project directory (default)
2. **Local Server**: Files stored on an external drive, accessible on your local network
3. **Remote Access**: Files accessible from anywhere using Tailscale (optional)

## Option 1: Local Development Setup

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-file-storage.git
   cd personal-file-storage
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```bash
   python run.py
   ```

   The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with the backend URL:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```bash
   npm start
   ```

   The frontend will be available at http://localhost:3000

## Option 2: Local Server with External Drive

### Step 1: Set Up External Drive

1. Connect your external hard drive to your computer

2. Create a directory on the external drive for file storage:
   ```bash
   # For macOS (replace ExternalDrive with your drive name)
   mkdir -p /Volumes/ExternalDrive/personal_drive_storage
   
   # For Windows (replace D: with your drive letter)
   mkdir D:\personal_drive_storage
   
   # For Linux
   mkdir -p /mnt/external/personal_drive_storage
   ```

### Step 2: Configure the Application

1. Update the storage path in `backend/app/core/config.py`:
   ```python
   # Comment out this line:
   # STORAGE_DIR: str = os.path.join(ROOT_DIR, "storage")
   
   # Uncomment and update this line with your external drive path:
   STORAGE_DIR: str = "/Volumes/ExternalDrive/personal_drive_storage"  # macOS example
   # STORAGE_DIR: str = "D:\\personal_drive_storage"  # Windows example
   # STORAGE_DIR: str = "/mnt/external/personal_drive_storage"  # Linux example
   ```

2. Run the database update script:
   ```bash
   python debug_db.py
   ```
   
   Select option 3 to update storage paths.

### Step 3: Start the Server

1. Start the backend:
   ```bash
   cd backend
   source venv/bin/activate
   python run.py
   ```

2. Find your computer's local IP address:
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows
   ipconfig | findstr /i "IPv4"
   ```

3. Update the frontend configuration:
   ```bash
   cd ../frontend
   ```
   
   Edit the `.env` file:
   ```
   REACT_APP_API_URL=http://YOUR_LOCAL_IP:8000/api
   ```
   Replace `YOUR_LOCAL_IP` with the IP address you found.

4. Start the frontend:
   ```bash
   npm start
   ```

### Step 4: Access from Other Devices

1. On any device connected to your local network, open a browser
2. Navigate to:
   ```
   http://YOUR_LOCAL_IP:3000
   ```
   Replace `YOUR_LOCAL_IP` with your computer's local IP address.

## Option 3: Remote Access with Tailscale (Optional)

Tailscale allows you to access your file storage from anywhere, even when you're away from your home network.

### Step 1: Install Tailscale

1. Install Tailscale on your server computer:
   - **macOS**: Download from [tailscale.com/download](https://tailscale.com/download) or use:
     ```bash
     brew install --cask tailscale
     ```
   - **Windows**: Download from [tailscale.com/download](https://tailscale.com/download)
   - **Linux**: Follow instructions at [tailscale.com/download](https://tailscale.com/download)

2. Sign up for a free Tailscale account at [tailscale.com](https://tailscale.com)

3. Connect your server to Tailscale:
   - **macOS**: Open the Tailscale app from Applications or menu bar
   - **Windows**: Open the Tailscale app from Start menu
   - **Linux**: Run `sudo tailscale up`

4. Note your Tailscale IP address:
   - **macOS/Windows**: Click on the Tailscale menu bar/system tray icon
   - **Linux**: Run `tailscale ip -4`

### Step 2: Update Frontend Configuration

1. Edit the frontend `.env` file:
   ```
   REACT_APP_API_URL=http://YOUR_TAILSCALE_IP:8000/api
   ```
   Replace `YOUR_TAILSCALE_IP` with your Tailscale IP address (usually starts with 100.x.y.z).

2. Rebuild the frontend:
   ```bash
   npm run build
   npm start
   ```

### Step 3: Access from Anywhere

1. Install Tailscale on your other devices (phones, laptops, etc.)
2. Sign in with the same Tailscale account
3. Open a browser and navigate to:
   ```
   http://YOUR_TAILSCALE_IP:3000
   ```
4. You can now access your files from anywhere, even on mobile data!

## Usage

1. Open your browser and navigate to the frontend URL
2. Use the sidebar to navigate between folders
3. Use the "New Folder" button to create folders
4. Use the "Upload Files" button to upload files
5. Click on a file to download it
6. Use the context menu (three dots) for additional options

## Troubleshooting

### File Upload Issues

If you encounter issues with file uploads:

1. Check the storage path in `backend/app/core/config.py`
2. Make sure the directory exists and is writable
3. Run `python debug_db.py` and use option 4 to check file existence

### Download Issues

If files don't download on other devices:

1. Make sure the frontend `.env` file has the correct backend URL
2. Check that the backend server is accessible from other devices
3. Verify that the storage directory is accessible to the backend

### Database Path Issues

If you see errors about missing files:

1. Run `python debug_db.py`
2. Use option 3 to update storage paths
3. Use option 4 to check file existence

## Advanced Configuration

For more advanced setup options, including:
- Setting up a dedicated server
- Configuring automatic startup
- Network configuration options
- Security considerations

See the [SERVER_SETUP.md](SERVER_SETUP.md) file.

## API Documentation

The API documentation is available at http://YOUR_SERVER_IP:8000/docs when the backend is running.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
