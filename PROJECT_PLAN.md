# Personal Drive - Project Plan

## Project Overview
A full-stack web application that provides a folder-like structure for file storage, accessible from anywhere via a web interface. The system will use a React TypeScript frontend and Python backend, with files physically stored on an external hard drive connected to a dedicated computer that runs 24/7.

## Architecture

### Frontend
- React with TypeScript
- File/folder navigation interface
- File upload/download capabilities
- No authentication (single user system)
- Responsive design for mobile/desktop

### Backend
- Python (FastAPI)
- RESTful API endpoints
- Simple file system operations
- Metadata database

### Storage
- Physical storage on external hard drive (utilizing up to 1TB)
- Database for file/folder metadata
- Primarily for laptop and phone backups

### Deployment
- Frontend: GitHub Pages or local server
- Backend: Running on dedicated computer
- Network configuration for remote access

## Implementation Steps

### 1. Project Setup
- [x] Initialize Git repository
- [x] Set up frontend project structure with React and TypeScript
- [x] Set up backend project structure with Python and FastAPI
- [x] Configure development environment

### 2. Backend Development
- [x] Design database schema for file/folder metadata
- [x] Create API endpoints for file operations (upload, download, delete, rename)
- [x] Create API endpoints for folder operations (create, delete, list contents)
- [x] Implement file storage management
- [x] Add basic security measures (input validation)

### 3. Frontend Development
- [x] Design and implement file browser interface
- [x] Implement file operations (upload, download, delete, rename)
- [x] Implement folder operations (create, delete, navigate)
- [x] Add drag-and-drop functionality
- [x] Ensure responsive design for different devices

### 4. Integration
- [x] Connect frontend to backend API
- [x] Test end-to-end functionality
- [ ] Optimize performance

### 5. Deployment
- [ ] Configure dedicated computer for 24/7 operation
- [ ] Set up external hard drive as storage location
- [ ] Update storage paths in application
- [ ] Set up port forwarding on router
- [ ] Configure domain name or dynamic DNS
- [ ] Deploy backend on dedicated computer
- [ ] Deploy frontend to GitHub Pages or local server
- [ ] Set up basic HTTP access

### 6. Additional Features (Future)
- [ ] Search functionality
- [ ] Automatic backup organization
- [ ] Simple file categorization
- [ ] Mobile-optimized interface

## Current Status (June 2025)
- Basic functionality is working (file/folder operations)
- Storage path configuration needs updating to use external hard drive
- Database paths need to be updated from previous development environment
- Ready for deployment setup on dedicated computer

## Requirements Summary

### User Access
- Single user system (personal use only)
- No authentication required

### Storage
- Target capacity: 1TB (with room to grow)
- Primary use: Laptop and phone backups
- File types: Images and documents
- Location: External hard drive connected to dedicated computer

### Network Access
- Options to be determined:
  1. Local network access only
  2. Internet access via port forwarding
  3. Internet access via Dynamic DNS

### Security
- Minimal security requirements
- Basic input validation
- No user authentication needed

## Next Steps
1. Update storage configuration to use external hard drive
2. Fix database path references
3. Set up dedicated computer for 24/7 operation
4. Configure network access method
5. Deploy and test remote access
