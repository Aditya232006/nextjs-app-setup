# Old Age Home Management System - Backend API

A comprehensive FastAPI-based backend system for managing old age home operations, including resident management, medical records, staff coordination, and administrative tasks.

## Features

### Core Functionality
- **Resident Management**: Complete CRUD operations for resident records
- **Medical Management**: Medication tracking, checkup scheduling, medical history
- **Bed Management**: Room and bed allocation system
- **Staff Management**: Staff records and role-based access control
- **Event Management**: Activities, celebrations, and scheduled events
- **Document Management**: File upload and organization system
- **Visitor Management**: Visitor tracking and check-in/out system
- **Billing System**: Financial management and billing records

### Dashboard Features
- Real-time statistics (total residents, medications, vacant beds, birthdays)
- Recent residents overview
- Upcoming birthdays tracking
- Today's schedule (checkups, events)
- Search and filter capabilities

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy ORM (SQLite default, PostgreSQL/MySQL supported)
- **Authentication**: JWT tokens with role-based access control
- **File Handling**: Multipart file uploads with type validation
- **Database Migrations**: Alembic
- **Environment Management**: python-decouple
- **Password Security**: bcrypt hashing

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize database**
   ```bash
   # Initialize Alembic (first time only)
   alembic init alembic
   
   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migrations
   alembic upgrade head
   ```

6. **Seed sample data (optional)**
   ```bash
   python seed_data.py
   ```

7. **Run the application**
   ```bash
   # Using the run script
   python run.py
   
   # Or directly with uvicorn
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

Once the server is running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

### Residents
- `POST /api/residents/` - Create new resident
- `GET /api/residents/` - List all residents
- `GET /api/residents/recent` - Get recently added residents
- `GET /api/residents/search?query={query}` - Search residents
- `GET /api/residents/{id}` - Get specific resident
- `PUT /api/residents/{id}` - Update resident
- `DELETE /api/residents/{id}` - Delete resident

### Medications
- `POST /api/medications/` - Add medication
- `GET /api/medications/resident/{resident_id}` - Get resident medications

### Checkups
- `POST /api/checkups/` - Schedule checkup
- `GET /api/checkups/` - List all checkups
- `GET /api/checkups/today` - Get today's checkups
- `GET /api/checkups/resident/{resident_id}` - Get resident checkups

### Events
- `POST /api/events/` - Create event
- `GET /api/events/` - List all events
- `GET /api/events/upcoming` - Get upcoming events

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - List all documents
- `GET /api/documents/resident/{resident_id}` - Get resident documents

### Beds
- `GET /api/beds/` - List all beds
- `GET /api/beds/vacant` - Get vacant beds
- `POST /api/beds/` - Create new bed
- `PUT /api/beds/{bed_id}/assign/{resident_id}` - Assign bed
- `PUT /api/beds/{bed_id}/release` - Release bed

### Birthdays
- `GET /api/birthdays/upcoming` - Get upcoming birthdays
- `GET /api/birthdays/today` - Get today's birthdays

## Database Schema

### Core Models
- **Resident**: Personal information, medical conditions, room assignment
- **Bed**: Room and bed management with status tracking
- **Staff**: Employee records with role-based permissions
- **Medication**: Prescription tracking and dosage information
- **Checkup**: Medical appointment scheduling and results
- **Event**: Activities and celebrations management
- **Document**: File storage with categorization
- **Visitor**: Guest tracking and visit logs
- **Billing**: Financial records and payment tracking

### Enums
- **ResidentStatus**: active, inactive, discharged, deceased
- **BedStatus**: occupied, vacant, maintenance
- **CheckupStatus**: scheduled, completed, cancelled
- **EventStatus**: planned, ongoing, completed, cancelled

## Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=sqlite:///./old_age_home.db

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
ALLOWED_FILE_TYPES=pdf,doc,docx,jpg,jpeg,png,txt
```

### Database Options
- **SQLite** (default): `sqlite:///./old_age_home.db`
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql://user:password@localhost/dbname`

## File Upload System

The system supports document uploads with the following features:
- File type validation
- Size limits (configurable)
- Organized storage by document type
- Database tracking with metadata
- Support for resident-specific and general documents

### Supported File Types
- Documents: PDF, DOC, DOCX, TXT
- Images: JPG, JPEG, PNG
- Configurable via environment variables

## Authentication & Authorization

### Role-Based Access Control
- **Admin**: Full system access
- **Doctor**: Medical records and checkups
- **Nurse**: Patient care and medications
- **Caregiver**: Basic resident information

### JWT Token Authentication
- Secure token-based authentication
- Configurable expiration times
- Role-based endpoint protection

## Development

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Adding New Features
1. Update models in `app/models.py`
2. Create corresponding schemas in `app/schemas.py`
3. Implement CRUD operations in `app/crud.py`
4. Add API endpoints in `app/main.py`
5. Create and apply database migration

### Testing
```bash
# Run with test database
DATABASE_URL=sqlite:///./test.db python -m pytest

# Seed test data
python seed_data.py
```

## Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

### Environment Setup
- Use PostgreSQL for production database
- Set strong SECRET_KEY
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Configure file storage (local/cloud)

### Performance Considerations
- Database indexing on frequently queried fields
- Pagination for large datasets
- File upload size limits
- Connection pooling for database
- Caching for dashboard statistics

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the database schema
3. Check environment configuration
4. Verify database migrations are applied

## License

This project is licensed under the MIT License.
