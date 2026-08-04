<div align="center">

# Hospital Management System

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.2-092E20?logo=django)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/docs/Web/CSS)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A web-based Hospital Management System built with **Django** that streamlines interactions between patients and doctors. The application provides appointment scheduling, patient records, prescriptions, and role-based dashboards through a clean server-rendered interface.

</div>

## Features

- User authentication
- Doctor and patient roles
- Appointment scheduling
- Doctor dashboard
- Patient dashboard
- Prescription management
- Medical history
- Role-based authorization
- Server-rendered interface using Django Templates

## Tech Stack

- Python
- Django
- HTML
- CSS
- Django Templates

## Getting Started

### Clone the repository

```bash
git clone https://github.com/zoanig/HMS
cd HMS
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Create an administrator account

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

## User Roles

### Doctor

- View appointments
- Manage appointments
- Create prescriptions
- View prescription history

### Patient

- Manage profile
- Book appointments
- View appointment history
- Browse doctors
- View prescriptions

## Project Structure

```text
.
├── HMS/
├── accounts/
├── doctors/
├── patients/
├── templates/
├── static/
├── requirements.txt
└── manage.py
```

## Highlights

- Authentication and authorization
- Role-based access control
- Appointment scheduling workflow
- Prescription management
- Modular Django application structure
- Server-side rendering with Django Templates

## Future Improvements

- Email notifications
- Search and filtering
- Medical report uploads
- REST API
- Automated tests

## License

This project is licensed under the MIT License.