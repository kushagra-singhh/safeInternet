# 🛡️ Internet Security Checker

<div align="center">

![Internet Security Checker](https://img.shields.io/badge/Security-Testing-blue?style=for-the-badge&logo=security)
![Flask](https://img.shields.io/badge/Flask-2.2.3-lightgrey?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

<p align="center">A modern, lightweight tool to evaluate website, email, and connection security against industry standards</p>

---

## 📋 Overview

Internet Security Checker is a comprehensive API and web application for testing your internet presence against modern security standards. Inspired by Internet.nl, this tool provides detailed security assessments of websites, email configurations, and internet connections with an intuitive user interface and detailed scoring reports.

<div align="center">
  <img src="https://i.imgur.com/6oCNT9C.png" alt="Internet Security Checker Screenshot" width="800px" />
</div>

## ✨ Features

### 🌐 Website Security Tests

- **IPv6 Support** - Test if websites are accessible over IPv6
- **DNSSEC Validation** - Verify domain name security extensions
- **TLS/HTTPS Security** - Check for secure HTTPS implementation
  - Certificate validity and trust
  - Modern cipher suite support
  - TLS version analysis
- **Security Headers** - Scan for critical security headers
  - Content Security Policy
  - Strict Transport Security
  - Frame protection
  - XSS prevention
- **Cookie Security** - Evaluate cookie configurations for security best practices

### 📧 Email Security Tests

- **SPF (Sender Policy Framework)** - Validate email sender authentication
- **DKIM (DomainKeys Identified Mail)** - Check email signature verification
- **DMARC Policy** - Test domain-based message authentication
- **STARTTLS Support** - Verify encryption for email transmission
- **MX Records** - Analyze mail exchanger configuration

### 🔌 Connection Tests

- **IPv6 Connectivity** - Test client IPv6 support
- **Connectivity Analysis** - Evaluate network connection security

## 🚀 Quick Start

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/internet-security-checker.git
   cd internet-security-checker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Running the Application

**Using Provided Scripts:**
```bash
# Linux/Mac
./setup.sh  # First-time setup
./run.sh    # Start the application

# Windows
setup.bat   # First-time setup
run.bat     # Start the application
```

**Manual Start:**
```bash
python app.py
```

The application will be accessible at http://localhost:5000

## 📊 Testing Your Internet Security

### 🔍 Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Choose the test type: Website, Email, or Connection
3. Enter the domain to test (or use automatic detection for connection tests)
4. Click "Start Test" and view the comprehensive results

### 🔧 API Usage

#### Website Security Test
```bash
curl -X POST http://localhost:5000/api/test/website \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

#### Email Security Test
```bash
curl -X POST http://localhost:5000/api/test/email \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

#### Connection Test
```bash
curl -X GET http://localhost:5000/api/test/connection
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example` with the following settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-key-for-security-checker` |
| `DEBUG` | Enable debug mode | `False` |
| `DATABASE_URL` | Database connection string | `sqlite:///security_checker.db` |
| `CONN_TEST_DOMAIN` | Domain used for connection tests | `internet.nl` |
| `SMTP_EHLO_DOMAIN` | Domain used for SMTP EHLO commands | `internet.nl` |
| `CHECK_SUPPORT_IPV6` | Enable IPv6 tests | `True` |
| `CHECK_SUPPORT_DNSSEC` | Enable DNSSEC tests | `True` |
| `CHECK_SUPPORT_MAIL` | Enable mail tests | `True` |
| `CHECK_SUPPORT_TLS` | Enable TLS tests | `True` |
| `CHECK_SUPPORT_APPSECPRIV` | Enable app security tests | `True` |

## 🔧 Troubleshooting

If you encounter dependency issues (especially with Flask and Werkzeug), see the [Dependency Fix Guide](DEPENDENCY_FIX.md) for detailed instructions on resolving these issues.

Common issues include:
- Flask and Werkzeug version compatibility
- Missing DNS libraries
- SSL/TLS configuration problems

## 🏗️ Architecture

This application is a Flask port of the Internet.nl security testing functionality, replacing Django-specific components:

| Django Component | Replacement |
|------------------|-------------|
| Django ORM | SQLAlchemy |
| Celery tasks | Flask background tasks |
| Django settings | Flask configuration |
| Django cache | Flask-Caching |
| Django logging | Python standard logging |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by the [Internet.nl](https://internet.nl/) project
- Built with [Flask](https://flask.palletsprojects.com/)
- Special thanks to the open-source security testing community

---

<div align="center">
  <p>Made with ❤️ for a safer internet</p>
</div>
