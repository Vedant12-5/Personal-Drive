# Personal File Storage System

A full-stack web application for storing and managing personal files with a React frontend and FastAPI backend.

## Features

- File upload and download
- Folder management (create, rename, delete)
- File management (upload, download, rename, delete)
- Hierarchical folder structure
- Clean and responsive UI

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
└── storage/              # File storage directory
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd my-open-source-project/backend
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

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd my-open-source-project/frontend
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

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Use the sidebar to navigate between folders
3. Use the "New Folder" button to create folders
4. Use the "Upload Files" button to upload files
5. Click on a file to download it
6. Use the context menu (three dots) for additional options

## API Documentation

The API documentation is available at http://localhost:8000/docs when the backend is running.

## Deployment

### Backend Deployment

1. Set up a production server with Python installed
2. Clone the repository
3. Install dependencies
4. Configure environment variables
5. Run with a production ASGI server like Uvicorn or Gunicorn

### Frontend Deployment

1. Build the frontend:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. Deploy the built files to a static file server or CDN

## License

This project is licensed under the MIT License - see the LICENSE file for details.
