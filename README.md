# E-Invoice Generator & QR Code Verification System

[![Django Version](https://img.shields.io/badge/Django-6.1-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![UI Theme](https://img.shields.io/badge/Design-Glassmorphism%20%2B%20Plus%20Jakarta%20Sans-indigo.svg)](#ui-design--theme-system)
[![Security Status](https://img.shields.io/badge/Security-Hardened%20%26%20Protected-brightgreen.svg)](#security--file-protection)

An enterprise-ready, responsive, and secure Web Application built using **Django** that empowers retail shop owners and businesses to generate digital e-invoices with embedded QR code verification, automated tax calculation, and multi-shop management.

---

## Key Features

- **Merchant Shop Registration**: Easy 2-step registration for shop owners with GST credentials, address details, and user credentials.
- **QR Code Verification**: Every invoice features an embedded cryptographic QR code payload allowing instant digital authenticity verification.
- **Automated Tax Calculation**: Automatic subtotals, GST, CGST, SGST, and total invoice amounts without manual error.
- **Glassmorphism UI Theme**: High-end modern design system built with custom CSS design tokens (`theme.css`), Google Font (*Plus Jakarta Sans*), micro-animations, and dynamic navbar elevations.
- **Shop Dashboard**: Real-time invoice counters, approval status indicators, and recent transaction history.
- **Security Hardened**: Built-in CSRF protection, secure HTTP headers, environment variable isolation, and password validation.

---

## Tech Stack

- **Backend**: Python 3.10+, Django 6.1
- **Database**: SQLite3 (Production ready for PostgreSQL / MySQL)
- **Frontend & UI**: HTML5, Vanilla CSS Design System, JavaScript (ES6), Bootstrap 5.3.3, Bootstrap Icons 1.11.3, Google Fonts (*Plus Jakarta Sans*)
- **Security**: Django Guard, Environment-driven Secret Key Management (`python-dotenv`), HTTP Strict Transport Security (HSTS), X-Frame & XSS Protection

---

## Project Structure

```text
Django_Invoice_genrater/
├── .env.example                # Template for environment variables
├── .gitignore                  # Excludes sensitive DB, keys, and cache
├── requirements.txt            # Python dependencies
├── README.md                   # Project Documentation & Setup Guide
└── InvoiceGenrater/
    ├── manage.py               # Django CLI management script
    ├── InvoiceGenrater/        # Core Project Configuration
    │   ├── settings.py         # Security hardened settings
    │   ├── urls.py             # Root URL routing
    │   ├── wsgi.py / asgi.py   # WSGI/ASGI application gateways
    ├── invoices/               # Main App Package
    │   ├── models.py           # ShopProfile, Product, Invoice models
    │   ├── views.py            # Authentication, About, Dashboard views
    │   ├── forms.py            # Shop registration & Bootstrap widgets
    │   ├── urls.py             # App route dispatchers
    │   ├── tests.py            # Automated test suite
    │   └── templates/          # App specific templates
    ├── static/                 # Global Static Assets
    │   ├── css/theme.css       # Design tokens, variables & glassmorphism
    │   └── js/theme.js         # Interactive counters, accordion & scroll logic
    └── templates/              # Site-wide Templates
        ├── base.html           # Master layout template (Navbar, Footer, Alerts)
        └── registration/       # Auth templates (login.html, register.html)
```

---

## Quick Setup & Installation Guide

Follow these step-by-step instructions to get the application running locally:

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.10+** (`python --version`)
- **Git** (`git --version`)

### 2. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/Django_Invoice_genrater.git
cd Django_Invoice_genrater
```

### 3. Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell / Command Prompt)
.\venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables & SQL Database

Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env
```

#### Switching to a Production SQL Database (PostgreSQL / MySQL):
By default, the project uses **SQLite**. To switch to **PostgreSQL** or **MySQL**, update your `.env` file:

**Option A: PostgreSQL Setup**
1. Install database driver: `pip install psycopg2-binary`
2. Update `.env`:
```env
DB_ENGINE=postgresql
DB_NAME=invoice_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**Option B: MySQL Setup**
1. Install database driver: `pip install mysqlclient`
2. Update `.env`:
```env
DB_ENGINE=mysql
DB_NAME=invoice_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Run Database Migrations
Navigate into `InvoiceGenrater` folder and apply schema migrations to your database:
```bash
cd InvoiceGenrater
python manage.py migrate
```


### 7. Create Admin Superuser (Optional)
To access the Django Admin Portal (`/admin/`), create a superuser:
```bash
python manage.py createsuperuser
```

### 8. Start Development Server
```bash
python manage.py runserver
```
Open your browser and visit: `http://127.0.0.1:8000/`

---

## Security & File Protection

All files in the project have been hardened and protected adhering to security best practices:

1. **Sensitive Secret Isolation**:
   - `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are configured via environment variables in `settings.py`.
2. **Version Control Security (`.gitignore`)**:
   - SQLite database (`db.sqlite3`), `.env` secrets file, virtual environment (`venv/`), Python cache (`__pycache__`), and media uploads are strictly excluded from version control.
3. **HTTP & Cookie Security Headers**:
   - `SECURE_BROWSER_XSS_FILTER = True`
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`
   - `X_FRAME_OPTIONS = 'DENY'`
   - `SESSION_COOKIE_HTTPONLY = True`
   - `CSRF_COOKIE_HTTPONLY = True`
   - `SESSION_COOKIE_SAMESITE = 'Lax'`
4. **Production Readiness**:
   - Automatic HSTS (`SECURE_HSTS_SECONDS`) and SSL redirects (`SECURE_SSL_REDIRECT`) trigger when `DEBUG = False`.

---

## Running Automated Tests

Run the test suite to verify views, routes, form validation, and template rendering:
```bash
python manage.py test
```
**Expected Output:**
```text
Ran 4 tests in 1.562s
OK
System check identified no issues (0 silenced).
```

---

## Contact & License

Developed with modern Django engineering practices. Free for commercial and retail distribution.
