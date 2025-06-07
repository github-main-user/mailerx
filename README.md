# MailerX 🚀

MailerX is a powerful, scalable Django-based mailing service designed to manage, send, and track mailings with ease. Built for reliability, flexibility, and performance, MailerX supports user authentication, role-based access, and scheduled mailing powered by **Celery**.

---

## Features

### Core Functionality
- **Client Management:** Add, view, edit, delete mailing recipients with unique emails.
- **Message Management:** CRUD for email templates with subject and body.
- **Mailing Campaigns:** Create, edit, delete, and start mailings.
- **Scheduling** Started Mailings scheduled by **Celery Beat**
- **Attempt Logs:** Detailed records of mailing attempts including timestamps, success status, and mail server responses.
- **Dashboard:** Overview of total campaigns, active mailings, and unique recipients.

### Extended Functionality
- **User Authentication & Registration:** Email confirmation, login/logout, password reset.
- **Role-Based Access Control:** Users manage their own data; Managers have read-only access to all with additional user management capabilities.
- **Detailed Statistics:** Success/failure rates and total messages sent per user.
- **Caching:** Server and client-side caching for improved performance.
- **Asynchronous Task Handling:** Celery integration for background task processing (mail sending, scheduling).
- **Logging:** Comprehensive logging of key events and errors in services and tasks.
- **Containerization:** Fully dockerized setup for easy deployment.

> [!INFO] Celery schedulers has set up 1 minute interval

---

## Tech Stack

- Django 5.x
- PostgreSQL 
- Celery + Celery Beat (for async task queue)
- Docker & Docker Compose
- Python 3.13+
- Redis (for caching and Celery broker)

---

## Quickstart

1. Clone the repo
```bash
git clone https://github.com/github-main-user/mailerx.git
```

2. Enter the cloned directory
```bash
cd mailerx
```

3. Build and start containers
```bash
docker compose up --build
```

4. Set up the .env file
```
cp .env.example .env
# then open in your editor end setup
```

> [!WARNING] If the DEBUG variable is True, there will be created 3 test users:
> - test@test.com
> - manager@manager.com
> - admin@admin.com
> - All of them have default password "12345678"

5. Access the application:
- Web UI: `http://localhost:8000/`
- Admin Panel: `http://localhost:8000/admin/`

---
Thanks for checking out MailerX — may your campaigns always land in inboxes, not spam! 😈🔥

