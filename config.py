import os

class Config:
    """Flask application configuration"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-security-checker'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # API Settings
    API_TITLE = 'Internet Security Checker API'
    API_VERSION = '1.0'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///security_checker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache settings
    CACHE_TYPE = "SimpleCache"  # Flask-Caching default
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Test settings
    CONN_TEST_DOMAIN = os.environ.get('CONN_TEST_DOMAIN') or 'internet.nl'
    SMTP_EHLO_DOMAIN = os.environ.get('SMTP_EHLO_DOMAIN') or 'internet.nl'
    
    # Feature flags - which tests to enable
    CHECK_SUPPORT_IPV6 = os.environ.get('CHECK_SUPPORT_IPV6', 'True').lower() == 'true'
    CHECK_SUPPORT_DNSSEC = os.environ.get('CHECK_SUPPORT_DNSSEC', 'True').lower() == 'true'
    CHECK_SUPPORT_MAIL = os.environ.get('CHECK_SUPPORT_MAIL', 'True').lower() == 'true'
    CHECK_SUPPORT_TLS = os.environ.get('CHECK_SUPPORT_TLS', 'True').lower() == 'true'
    CHECK_SUPPORT_APPSECPRIV = os.environ.get('CHECK_SUPPORT_APPSECPRIV', 'True').lower() == 'true'
    CHECK_SUPPORT_RPKI = os.environ.get('CHECK_SUPPORT_RPKI', 'True').lower() == 'true'
    
    # Timeout settings
    DEFAULT_TIMEOUT = 10  # seconds
    TLS_TIMEOUT = 10  # seconds
    DNS_TIMEOUT = 5  # seconds
    HTTP_TIMEOUT = 10  # seconds
    
    # Security Headers
    SECURITY_HEADERS = [
        'Strict-Transport-Security',
        'Content-Security-Policy',
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection',
        'Referrer-Policy'
    ]
