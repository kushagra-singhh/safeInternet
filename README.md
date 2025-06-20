# 🛡️ Internet Security Checker

<div align="center">

![Internet Security Checker](https://img.shields.io/badge/Security-Testing-blue?style=for-the-badge&logo=security)
![Flask](https://img.shields.io/badge/Flask-2.2.3-lightgrey?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Bilingual](https://img.shields.io/badge/Bilingual-EN|HI-orange?style=for-the-badge)

</div>

<p align="center">A modern, responsive tool to evaluate website, email, and connection security against industry standards</p>

---

## 📋 Overview

Internet Security Checker is a comprehensive web application for testing your internet presence against modern security standards. This tool provides detailed security assessments of websites, email configurations, and internet connections with an intuitive, responsive user interface and detailed scoring reports. Available in both English and Hindi, with light and dark themes.

<div align="center">
  <img src="screenshots/main-light.png" alt="Internet Security Checker Light Theme" width="45%" />
  <img src="screenshots/main-dark.png" alt="Internet Security Checker Dark Theme" width="45%" />
</div>

## ✨ Key Features

- **Responsive Design** - Optimized for desktop and mobile devices
- **Bilingual Support** - Full English and Hindi language support
- **Theme Switching** - Toggle between light and dark themes
- **Comprehensive Testing** - Website, email, and connection security analysis
- **Interactive Results** - Detailed, easy-to-understand test cards
- **Modern UI/UX** - Clean, intuitive interface with visual feedback

## 🔒 Security Test Categories

### 🌐 Website Security

- **IPv6 Support** - Verify websites are accessible over IPv6
- **DNSSEC Validation** - Check domain name security extensions
- **TLS/HTTPS Security** - Analyze HTTPS implementation quality
- **Security Headers** - Scan for critical security headers
- **Cookie Security** - Evaluate cookie configuration best practices

### 📧 Email Security

- **SPF, DKIM, DMARC** - Check email authentication protocols
- **STARTTLS Support** - Verify email transmission encryption
- **MX Records** - Analyze mail exchanger configuration

### 🔌 Connection Security

- **IPv6 Connectivity** - Test client IPv6 support
- **Network Security** - Evaluate connection security measures

<div align="center">
  <img src="screenshots/results-mobile.png" alt="Mobile Results View" width="30%" />
  <img src="screenshots/results-desktop.png" alt="Desktop Results View" width="60%" />
</div>

## 🚀 Quick Start Guide

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/internet-security-checker.git
   cd internet-security-checker
   ```

2. **Set up environment (using provided scripts)**
   ```bash
   # On Windows
   setup.bat
   
   # On macOS/Linux
   ./setup.sh
   ```

3. **Or manually set up**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Running the Application

```bash
# On Windows
run.bat

# On macOS/Linux
./run.sh

# Or manually
python app.py
```

The application will be accessible at http://localhost:5000

## �️ Usage Instructions

1. Open your browser and navigate to `http://localhost:5000`
2. Choose your preferred language (English or Hindi) using the language toggle
3. Select your preferred theme (Light or Dark) using the theme toggle
4. Enter a domain name in the input field
5. Select the test type: Website, Email, or Connection
6. Click "Start Test" to begin the security analysis
7. Review the detailed test results organized in test cards

<div align="center">
  <img src="screenshots/input-form.png" alt="Input Form" width="80%" />
</div>

## 🌐 API Documentation

The application provides a RESTful API for programmatic access to security tests.

### Website Security Test
```bash
curl -X POST http://localhost:5000/api/test/website \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### Email Security Test
```bash
curl -X POST http://localhost:5000/api/test/email \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### Connection Test
```bash
curl -X GET http://localhost:5000/api/test/connection
```

## 🚢 Deployment Guide

### Deploying to Render

1. **Create a Render account** at [render.com](https://render.com/)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure your service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Add the required environment variables (see Configuration section)

### Deploying to Other Platforms

The application can be deployed to any platform that supports Python applications:

- **Heroku**: Use a Procfile with `web: gunicorn app:app`
- **AWS**: Deploy using Elastic Beanstalk or containerize with Docker
- **Azure**: Use App Service for Python
- **Digital Ocean**: Deploy via App Platform

## ⚙️ Configuration

Create a `.env` file based on `.env.example` with the following settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-key-for-security-checker` |
| `DEBUG` | Enable debug mode | `False` |
| `DATABASE_URL` | Database connection string | `sqlite:///security_checker.db` |
| `CONN_TEST_DOMAIN` | Domain for connection tests | `internet.nl` |
| `SMTP_EHLO_DOMAIN` | Domain for SMTP EHLO commands | `internet.nl` |
| `API_URL` | URL for API endpoint | Set automatically based on host |
| `CHECK_SUPPORT_IPV6` | Enable IPv6 tests | `True` |
| `CHECK_SUPPORT_DNSSEC` | Enable DNSSEC tests | `True` |
| `CHECK_SUPPORT_MAIL` | Enable mail tests | `True` |
| `CHECK_SUPPORT_TLS` | Enable TLS tests | `True` |
| `CHECK_SUPPORT_APPSECPRIV` | Enable app security tests | `True` |

## 🔧 Troubleshooting

If you encounter dependency issues, use the provided fix scripts:

```bash
# On Windows
fix_deps.bat

# On macOS/Linux
./fix_deps.sh
```

For more detailed troubleshooting, see the [Dependency Fix Guide](DEPENDENCY_FIX.md).

## 🏗️ Project Structure

```
internet-security-checker/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
├── templates/             # HTML templates
│   └── index.html         # Main application template
├── tests/                 # Test modules
│   ├── website_tests.py   # Website security tests
│   ├── email_tests.py     # Email security tests
│   ├── connection_tests.py# Connection security tests
│   └── ...                # Other test modules
└── scripts/               # Utility scripts
    ├── setup.sh/bat       # Setup scripts
    └── run.sh/bat         # Run scripts
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by the [Internet.nl](https://internet.nl/) project
- Built with [Flask](https://flask.palletsprojects.com/)
- Special thanks to all contributors and the open-source security testing community

---

<div align="center">
  <p>Made with ❤️ for a safer internet</p>
</div>
