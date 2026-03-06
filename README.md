# Hospital Management System

A comprehensive web-based hospital management system built with Flask (backend) and Vue.js (frontend) that enables efficient management of hospital operations for administrators, doctors, and patients.

## Features

### For Administrators
- **Dashboard**: Overview of hospital statistics and operations
- **Department Management**: Add, view, and manage hospital departments
- **Doctor Management**: Register new doctors, edit doctor information, view all doctors
- **Patient Management**: View registered patients and manage patient records
- **Appointment Oversight**: Monitor upcoming appointments across the hospital
- **Treatment Records**: Access all treatment records and patient histories

### For Doctors
- **Dashboard**: Personal dashboard with schedule and patient information
- **Availability Management**: Set and manage appointment availability slots
- **Treatment Management**: Record and update patient treatments
- **Patient Care**: Access patient information and treatment history

### For Patients
- **Department Browsing**: View available hospital departments
- **Doctor Search**: Search and view doctor profiles and specialties
- **Appointment Booking**: Schedule appointments with preferred doctors
- **Medical History**: Access personal treatment history and records
- **Profile Management**: Update personal information and contact details

## Technology Stack

### Backend
- **Flask**: Python web framework for REST API development
- **SQLAlchemy**: ORM for database operations
- **Flask-Security**: Authentication and authorization
- **SQLite**: Database for data persistence
- **Redis**: Caching and session storage
- **Celery**: Background task processing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Vite**: Fast build tool and development server
- **Vue Router**: Client-side routing
- **Pinia**: State management
- **Bootstrap 5**: CSS framework for responsive design
- **Axios**: HTTP client for API communication
- **Chart.js**: Data visualization for dashboards

## Project Structure

```
hospital-management-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── routes.py              # API endpoints and route handlers
│   ├── model.py               # Database models
│   ├── database.py            # Database configuration
│   ├── config.py              # Application configuration
│   ├── task.py                # Celery tasks
│   ├── celery_config.py       # Celery configuration
│   ├── celery_init.py         # Celery initialization
│   ├── mail.py                # Email functionality
│   ├── requirement.txt        # Python dependencies
│   ├── README                 # Backend setup instructions
│   └── static/                # Static files (CSV reports)
├── frontend/
│   ├── src/
│   │   ├── main.js            # Vue app entry point
│   │   ├── App.vue            # Root component
│   │   ├── components/        # Reusable Vue components
│   │   ├── pages/             # Page components by user role
│   │   ├── router/            # Vue Router configuration
│   │   └── stores/            # Pinia state management
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── README.md              # Frontend setup instructions
└── README.md                  # Main project README (this file)
```

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- Redis server
- Virtual environment (recommended)

### Frontend Requirements
- Node.js 20.19.0 or higher (or 22.12.0+)
- npm or yarn package manager

## Installation and Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # On Windows
   python -m venv myenv
   .\myenv\Scripts\activate

   # On Linux/Mac
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

4. **Start Redis server (WSL):**
   ```bash
   redis-server
   ```

5. **Stop Redis server (WSL):**
   ```bash
   redis-server
   ```   

5. **Initialize the database:**
   ```bash
   python3 app.py
   ```
   This will create the database tables and default roles.

6. **Start Celery worker (in a new WSL terminal and after activating you virtual environment):**
   ```bash
   celery -A app.celery worker --loglevel=info
   ```

7. **Start the Flask development server (WSL):**
   ```bash
   python3 app.py
   ```
   The backend will be available at `http://localhost:5000`

8. **Start Celery beat server (in a new WSL terminal and after activating you virtual environment):**
   ```bash
   celery -A app.celery beat --loglevel=info
   ```   

9. **Start Mailhog server (in a new WSL terminal and after activating you virtual environment):**
   ```bash
   mailhog
   ```   





### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## Usage

1. **Access the application** at `http://localhost:5173`
2. **Register** as a new user or **login** with existing credentials
3. **Role-based access** will redirect you to the appropriate dashboard:
   - Admin users: Full hospital management capabilities
   - Doctors: Patient care and schedule management
   - Patients: Appointment booking and medical history access

## API Documentation

The backend provides RESTful APIs for all operations. Key endpoints include:

- `POST /api/login` - User authentication
- `GET /api/departments` - List all departments
- `GET /api/doctors` - List all doctors
- `POST /api/appointments` - Book appointments
- `GET /api/patients/{id}/history` - Patient medical history

## Database Schema

The system uses SQLite with the following main entities:
- **Users**: Authentication and role management
- **Roles**: User roles (admin, doctor, patient)
- **Patients**: Patient information and demographics
- **Doctors**: Doctor profiles and specialties
- **Departments**: Hospital department structure
- **Appointments**: Scheduled patient appointments
- **Treatments**: Medical treatment records

## Background Tasks

The system uses Celery for automated tasks:
- **Monthly Reports**: Generate CSV reports of hospital activities
- **Email Notifications**: Send periodic updates and reminders

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm run test
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
Configure production settings in `config.py` and use a WSGI server like Gunicorn.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository.

## Acknowledgments

- Built with Flask and Vue.js frameworks
- UI components powered by Bootstrap
- Icons from Bootstrap Icons
- Charts powered by Chart.js