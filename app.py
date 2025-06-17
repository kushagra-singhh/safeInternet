from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from config import Config
import logging
import os

# Import test modules
from tests import website_tests, email_tests, connection_tests

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("security_checker.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "name": "Internet Security Checker API",
        "version": "1.0.0",
        "endpoints": [
            "/api/test/website",
            "/api/test/email",
            "/api/test/connection"
        ]
    })

@app.route('/api/test/website', methods=['POST'])
def test_website():
    data = request.get_json()
    if not data or 'domain' not in data:
        return jsonify({"error": "Domain is required"}), 400
        
    domain = data['domain']
    logger.info(f"Starting website test for domain: {domain}")
    
    try:
        results = website_tests.run_website_tests(domain)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error testing website {domain}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test/email', methods=['POST'])
def test_email():
    data = request.get_json()
    if not data or 'domain' not in data:
        return jsonify({"error": "Domain is required"}), 400
        
    domain = data['domain']
    logger.info(f"Starting email test for domain: {domain}")
    
    try:
        results = email_tests.run_email_tests(domain)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error testing email {domain}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test/connection', methods=['GET'])
def test_connection():
    client_ip = request.remote_addr
    logger.info(f"Starting connection test for IP: {client_ip}")
    
    try:
        results = connection_tests.run_connection_tests(client_ip)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
