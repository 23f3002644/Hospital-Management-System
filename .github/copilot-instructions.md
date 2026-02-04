# Copilot Instructions for Hospital Management System

## Overview
This project is a web application for managing hospital operations, allowing interaction among Admins, Doctors, and Patients. The architecture is based on a Flask backend and a VueJS frontend, utilizing SQLite for data storage and Redis for caching and background jobs.

## Architecture
- **Backend**: Built with Flask, serving RESTful APIs.
- **Frontend**: Developed using VueJS, with Bootstrap for styling.
- **Database**: SQLite for persistent storage.
- **Caching**: Redis for improved performance.
- **Background Jobs**: Managed with Celery and Redis.

## Developer Workflows
- **Running the Application**: Use the following command to start the Flask server:
  ```bash
  flask run
  ```
- **Building the Frontend**: Navigate to the frontend directory and run:
  ```bash
  npm run serve
  ```
- **Testing**: Ensure to run tests after making changes. Use:
  ```bash
  pytest
  ```

## Project Conventions
- **File Structure**: Follow the established directory structure for backend and frontend components.
- **Naming Conventions**: Use camelCase for JavaScript variables and snake_case for Python variables.

## Integration Points
- **API Endpoints**: Documented in the Flask application, accessible via `/api`.
- **Cross-Component Communication**: Handled through RESTful API calls from the VueJS frontend to the Flask backend.

## External Dependencies
- **Flask**: For the backend API.
- **VueJS**: For the frontend UI.
- **Redis**: For caching and background processing.
- **Celery**: For managing asynchronous tasks.

## Examples
- **Creating a New Patient**: Use the POST method on `/api/patients` with the required patient data.
- **Fetching Patient Data**: Use the GET method on `/api/patients/{id}` to retrieve patient information.

## Conclusion
This document serves as a guide for AI agents to understand the structure and workflows of the Hospital Management System. For further details, refer to the README.md and the respective backend and frontend documentation.