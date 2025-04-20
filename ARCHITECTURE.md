# Personal Drive - Architecture

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Browser    │◄────┤  GitHub Pages   │     │     iMac        │
│  (User Access)  │     │  (Frontend)     │     │  (File Server)  │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐             │
         └─────────────►│   Python API    │◄────────────┘
                        │   (Backend)     │
                        │                 │
                        └────────┬────────┘
                                 │
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Database      │
                        │  (Metadata)     │
                        │                 │
                        └─────────────────┘
```

## Component Details

### Frontend (React + TypeScript)
- **Hosting**: GitHub Pages
- **Key Libraries**:
  - React Router for navigation
  - Axios for API calls
  - Material-UI or Tailwind CSS for UI components
  - React Query for data fetching
  - Redux or Context API for state management

### Backend (Python)
- **Framework**: FastAPI
- **Hosting**: Running on the iMac
- **Key Components**:
  - RESTful API endpoints
  - JWT authentication
  - File system operations
  - Database ORM (SQLAlchemy)

### Database
- **Options**:
  - SQLite (simplest setup)
  - PostgreSQL (more robust)
- **Tables**:
  - Users
  - Files
  - Folders
  - Permissions

### Storage
- **Physical**: iMac hard drive
- **Organization**: 
  - Structured directories
  - Unique file identifiers
  - Metadata in database

### Network Configuration
- **Options**:
  - Port forwarding
  - Dynamic DNS service
  - Reverse proxy (Nginx)
  - SSL certificate (Let's Encrypt)

## Security Considerations

1. **Authentication**:
   - JWT tokens
   - Secure password storage
   - Session management

2. **Authorization**:
   - Role-based access control
   - File/folder permissions

3. **Data Protection**:
   - HTTPS for all connections
   - Input validation
   - Protection against common attacks (XSS, CSRF)

4. **Network Security**:
   - Firewall configuration
   - Rate limiting
   - IP filtering if needed

## Scalability Considerations

1. **Storage Expansion**:
   - External drives
   - Network storage

2. **Performance**:
   - Caching strategies
   - Pagination for large directories
   - Thumbnail generation for media files

3. **Backup Strategy**:
   - Regular automated backups
   - Offsite backup options
