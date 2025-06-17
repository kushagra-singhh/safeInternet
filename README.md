# Internet Security Checker

A Flask-based API for testing website, email, and connection security standards. This is a lightweight version of Internet.nl's security testing functionality.

## Features

- Website Security Tests
  - IPv6 connectivity
  - DNSSEC validation
  - TLS/HTTPS configuration
  - Security headers and privacy features

- Email Security Tests
  - SPF configuration
  - DKIM setup
  - DMARC policies
  - STARTTLS support

- Connection Tests
  - IPv6 support detection

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

Alternatively, use the provided setup scripts:
```bash
# Linux/Mac
./setup.sh
./run.sh

# Windows
setup.bat
run.bat
```

## Troubleshooting

If you encounter dependency issues (especially with Flask and Werkzeug), see the [Dependency Fix Guide](DEPENDENCY_FIX.md) for detailed instructions on resolving these issues.

## API Endpoints

- `GET /`: API information
- `POST /api/test/website`: Test website security
  - Request body: `{"domain": "example.com"}`
- `POST /api/test/email`: Test email security
  - Request body: `{"domain": "example.com"}`
- `GET /api/test/connection`: Test connection security (automatically detects client IP)

## Environment Variables

You can customize the application using environment variables:

- `SECRET_KEY`: Flask secret key
- `DEBUG`: Enable debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `CONN_TEST_DOMAIN`: Domain used for connection tests
- `SMTP_EHLO_DOMAIN`: Domain used for SMTP EHLO commands

## Architecture

This application is a Flask port of the Internet.nl security testing functionality, replacing Django-specific components:

- Django ORM → SQLAlchemy
- Celery tasks → Flask background tasks
- Django settings → Flask configuration
- Django cache → Flask-Caching
- Django logging → Python standard logging

## License

This project is licensed under the MIT License - see the LICENSE file for details.
