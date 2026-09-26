# TrackFlow

TrackFlow is a backend API for a lightweight issue tracker built for small
development teams. Users register, create projects, invite teammates by
adding them as members, file issues against a project, assign issues to a
teammate to fix, and discuss issues through comments.

This project is built with **Django** and **Django REST Framework**,
authenticated via **JWT** (`djangorestframework-simplejwt`), backed by
**PostgreSQL**.

---

## Tech stack

- Python 3.13
- Django 6.0
- Django REST Framework 3.17
- djangorestframework-simplejwt 5.5 (JWT authentication)
- PostgreSQL 17
- python-dotenv (environment variable management)

---

## Project structure

```
trackflow/
├── core/                  # Django project settings, root urls
├── auth_app/               # Custom User model, registration, login, token refresh
├── projects_app/           # Project model, membership management
├── issues_app/              # Issue and Comment models
├── manage.py
├── requirements.txt
├── .env.template            # Copy this to .env and fill in your own values
└── .env                     # Your local secrets (never committed)
```

Each app has its own `api/` folder containing `serializers.py`, `views.py`,
`urls.py`, and `permissions.py`.

---

## Prerequisites

- Python 3.11+ installed
- PostgreSQL available, either:
  - **Option A — installed locally** on your machine, or
  - **Option B — running in Docker**

You only need one of the two PostgreSQL options below, not both.

---

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd trackflow
```

## 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script with an execution policy error, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```
then try activating again.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Set up PostgreSQL

### Option A — Local PostgreSQL install

1. Install PostgreSQL if you haven't already (postgresql.org/download).
2. Open a terminal and connect as the default superuser:
   ```bash
   psql -U postgres
   ```
3. Create the database, a dedicated user, and grant privileges:
   ```sql
   CREATE DATABASE trackflow_db;
   CREATE USER trackflow_user WITH PASSWORD 'your_chosen_password';
   GRANT ALL PRIVILEGES ON DATABASE trackflow_db TO trackflow_user;
   ```
4. **Important (PostgreSQL 15+):** grant schema privileges too, or migrations
   will fail with a "permission denied for schema public" error. Reconnect
   specifically to the new database first:
   ```bash
   psql -U postgres -d trackflow_db
   ```
   Then run:
   ```sql
   GRANT ALL ON SCHEMA public TO trackflow_user;
   ```

### Option B — PostgreSQL via Docker

```bash
docker run --name trackflow-postgres \
  -e POSTGRES_DB=trackflow_db \
  -e POSTGRES_USER=trackflow_user \
  -e POSTGRES_PASSWORD=your_chosen_password \
  -p 5432:5432 \
  -d postgres:17
```

This creates the database and user in one step; Docker's official Postgres
image handles schema privileges automatically, so no extra grant step is
needed here.

## 5. Configure environment variables

Copy the template and fill in your own values:

```bash
cp .env.template .env
```

Open `.env` and set:
- `SECRET_KEY` — any long random string (Django generates one automatically
  in `settings.py` on `startproject`; you can reuse that value)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` — matching whatever you set up in step 4
- `DB_HOST` — `localhost` for either option above
- `DB_PORT` — `5432` (PostgreSQL's default)

## 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Create an admin superuser

```bash
python manage.py createsuperuser
```

You'll be prompted for `email`, `complete name`, and `password` (this
project uses email as the login field instead of username).

## 8. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`, and the Django
admin panel at `http://127.0.0.1:8000/admin/`.

---

## Authentication

Every endpoint except registration, login, and token refresh requires a
JWT access token, sent as a header:

```
Authorization: Bearer <your_access_token>
```

Access tokens expire after 30 minutes; use `POST /api/token/refresh/` with
a valid refresh token to get a new one without logging in again.

---

## API overview

| Resource | Endpoints |
|---|---|
| Auth | `POST /api/registration/`, `POST /api/login/`, `POST /api/token/refresh/` |
| Projects | `GET/POST /api/projects/`, `GET/PATCH/DELETE /api/projects/{id}/` |
| Issues | `POST /api/issues/`, `PATCH/DELETE /api/issues/{id}/`, `GET /api/issues/assigned-to-me/`, `GET /api/issues/reported-by-me/` |
| Comments | `GET/POST /api/issues/{issueId}/comments/`, `DELETE /api/issues/{issueId}/comments/{commentId}/` |

Full field names, request/response shapes, and status codes are defined in
the project's API documentation.

---

## Notes

- There is no endpoint to search or list all registered users — adding
  someone to a project requires already knowing their numeric user ID
  (visible via the Django admin panel).
- Editing a comment after creation is not supported; comments can only be
  created or deleted.