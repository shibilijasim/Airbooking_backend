# # AirBooking — Backend (Django REST Framework)

REST API and asynchronous worker service for **AirBooking**, built with Django, Django REST Framework, SimpleJWT, PostgreSQL, Celery, and Redis.

## Features

- **JWT Authentication & Role-Based Access Control**: User registration, login, token refresh (`SimpleJWT`), and admin permission enforcement (`IsAdminUser`).
- **Admin User Approval Queue**: Filter user registrations (`Pending`, `Approved`, `Rejected`, `All`) and approve or reject accounts (`GET /api/auth/admin/users/`, `POST /api/auth/admin/users/<id>/review/`).
- **Asynchronous Activation Emails**: Queues account activation emails via Celery and Redis upon admin approval.
- **Live Flight Schedules & Radar Tracking**: Proxies AirLabs schedules and live radar tracking endpoints (`GET /api/flights/live-search/`, `GET /api/flights/live/<flight_iata>/`) and persists flight records in PostgreSQL.
- **Admin Flight Management**: Lists managed flights (`GET /api/admin/flights/`) and updates operational status (`PUT /api/admin/flights/<id>/status/`) across `On-Time`, `Delayed`, `Boarding`, `Cancelled`, and `Landed`.
- **Bookings API**: Creates and manages passenger flight reservations.

## Tech Stack

- **Language & Framework**: Python, Django, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: PostgreSQL
- **Task Queue & Broker**: Celery, Redis
- **External API**: AirLabs Schedules & Live Flight Tracking API

## Setup & Installation

### 1. Clone the Repository and Create a Virtual Environment

```bash
git clone <your-backend-repo-url>
cd D:\Django\Projects\Airbooking
python -m venv myenv
myenv\Scripts\activate

## Install dependencies
cd D:\Django\Projects\Airbooking\backend
pip install -r requirements.txt
pip install packaging

# Terminal 1 — Start Redis Server
redis-server

# Terminal 2 — Start Celery Worker (Windows)
cd D:\Django\Projects\Airbooking\backend
..\myenv\Scripts\celery.exe -A config worker --loglevel=info --pool=solo

# Terminal 3 — Start Django API Server
cd D:\Django\Projects\Airbooking\backend
..\myenv\Scripts\python.exe manage.py runserver
