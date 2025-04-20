# Personal Drive - Setup Guide

This guide will walk you through setting up the development environment and deploying the Personal Drive application.

## Development Environment Setup

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- Git
- Code editor (VS Code recommended)
- iMac with sufficient storage

### Frontend Setup

1. **Create React App with TypeScript**
   ```bash
   npx create-react-app frontend --template typescript
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install react-router-dom axios @mui/material @mui/icons-material @emotion/react @emotion/styled react-query
   ```

3. **Project Structure**
   ```
   frontend/
   ├── public/
   ├── src/
   │   ├── components/
   │   │   ├── Auth/
   │   │   ├── FileExplorer/
   │   │   ├── Layout/
   │   │   └── common/
   │   ├── hooks/
   │   ├── services/
   │   ├── types/
   │   ├── utils/
   │   ├── App.tsx
   │   └── index.tsx
   └── package.json
   ```

### Backend Setup

1. **Create Python Virtual Environment**
   ```bash
   python -m venv backend/venv
   source backend/venv/bin/activate  # On Windows: backend\venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart
   pip freeze > backend/requirements.txt
   ```

3. **Project Structure**
   ```
   backend/
   ├── app/
   │   ├── api/
   │   │   ├── endpoints/
   │   │   │   ├── auth.py
   │   │   │   ├── files.py
   │   │   │   └── folders.py
   │   │   └── api.py
   │   ├── core/
   │   │   ├── config.py
   │   │   └── security.py
   │   ├── db/
   │   │   ├── base.py
   │   │   └── session.py
   │   ├── models/
   │   │   ├── user.py
   │   │   ├── file.py
   │   │   └── folder.py
   │   ├── schemas/
   │   │   ├── user.py
   │   │   ├── file.py
   │   │   └── folder.py
   │   ├── services/
   │   │   └── file_service.py
   │   └── main.py
   ├── storage/
   └── requirements.txt
   ```

## Database Setup

1. **SQLite Setup (Simple Option)**
   ```bash
   # No additional installation needed, just configure in code
   ```

2. **PostgreSQL Setup (Advanced Option)**
   ```bash
   # Install PostgreSQL
   # Create database and user
   # Update connection string in config.py
   ```

## iMac Server Configuration

1. **System Configuration**
   - Set up energy settings to prevent sleep
   - Configure automatic login
   - Set up automatic startup of the backend service

2. **Network Configuration**
   - Assign static IP on local network
   - Configure port forwarding on router (port 8000 to iMac's IP)
   - Set up dynamic DNS service if no static IP is available

3. **Storage Configuration**
   - Create dedicated storage directory
   - Set appropriate permissions
   - Configure backup solution

## Deployment

### Backend Deployment

1. **Create Systemd Service (Linux) or LaunchAgent (macOS)**
   ```bash
   # Example for macOS LaunchAgent
   # Create ~/Library/LaunchAgents/com.personaldrive.backend.plist
   ```

2. **Configure Nginx as Reverse Proxy**
   ```bash
   # Install Nginx
   # Configure virtual host
   # Set up SSL with Let's Encrypt
   ```

### Frontend Deployment

1. **Build React App**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to GitHub Pages**
   ```bash
   npm install --save-dev gh-pages
   # Add deploy scripts to package.json
   npm run deploy
   ```

## Testing the Setup

1. **Local Testing**
   - Start backend: `uvicorn app.main:app --reload`
   - Start frontend: `npm start`
   - Access at http://localhost:3000

2. **Remote Testing**
   - Access frontend via GitHub Pages URL
   - Ensure API calls to backend are working
   - Test file upload and download

## Troubleshooting

1. **CORS Issues**
   - Ensure backend has proper CORS configuration
   - Check frontend API URL configuration

2. **Network Access Issues**
   - Verify port forwarding configuration
   - Check firewall settings
   - Test with curl or Postman

3. **File Permission Issues**
   - Check storage directory permissions
   - Ensure backend service has appropriate access
