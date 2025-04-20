# Getting Started with Personal File Storage System

This guide will help you set up and run the Personal File Storage System on your local machine.

## Local Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/personal-file-storage.git
cd personal-file-storage
```

### Step 2: Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python run.py
   ```

   The backend will be available at http://localhost:8000

### Step 3: Set Up the Frontend

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create a `.env` file with the backend URL:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

   The frontend will be available at http://localhost:3000

## Remote Access with Tailscale

If you want to access your Personal File Storage System from anywhere, you can use Tailscale to create a secure network.

### Step 1: Install Tailscale

1. Install Tailscale on your server:
   ```bash
   # For Ubuntu/Debian
   curl -fsSL https://tailscale.com/install.sh | sh

   # For macOS
   brew install tailscale

   # For Windows
   # Download and install from https://tailscale.com/download
   ```

2. Install Tailscale on your client devices (laptops, phones, etc.) from [tailscale.com/download](https://tailscale.com/download)

### Step 2: Set Up Tailscale

1. Start and authenticate Tailscale on your server:
   ```bash
   sudo tailscale up
   ```

2. Follow the authentication link to connect your server to your Tailscale network

3. Note the Tailscale IP address of your server:
   ```bash
   tailscale ip -4
   ```

### Step 3: Configure Your Application

1. Update the frontend `.env` file to use the Tailscale IP:
   ```
   REACT_APP_API_URL=http://YOUR_TAILSCALE_IP:8000/api
   ```

2. Rebuild the frontend if needed:
   ```bash
   npm run build
   # or
   yarn build
   ```

### Step 4: Access Your Application

1. Start both the backend and frontend servers as described in the local setup

2. On any device connected to your Tailscale network, you can access:
   - Frontend: http://YOUR_TAILSCALE_IP:3000
   - Backend API: http://YOUR_TAILSCALE_IP:8000
   - API Documentation: http://YOUR_TAILSCALE_IP:8000/docs

## Production Deployment

For a production deployment, consider:

1. Using a production ASGI server like Gunicorn with Uvicorn workers for the backend
2. Setting up a reverse proxy like Nginx
3. Configuring HTTPS with Let's Encrypt
4. Using a process manager like Supervisor or systemd
5. Deploying the frontend to a CDN or static file server

A basic production setup might look like:

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

For more detailed production deployment instructions, please refer to the documentation for FastAPI and React.
