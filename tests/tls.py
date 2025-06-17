"""
TLS testing module for Internet security tests.
Replaces Django-specific TLS testing implementation.
"""
import logging
import ssl
import socket
import datetime
from OpenSSL import SSL, crypto
from .shared import create_test_result, is_port_open
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

# Secure cipher suites (simplified list for example)
SECURE_CIPHER_SUITES = [
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'TLS_AES_128_GCM_SHA256',
    'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-CHACHA20-POLY1305',
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES128-GCM-SHA256'
]

# Strong TLS protocols
SECURE_PROTOCOLS = [
    'TLSv1.2',
    'TLSv1.3'
]

def test_tls_website(domain):
    """
    Test TLS support for a website
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing TLS for website: {domain}")
    
    results = {
        "name": "TLS",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for HTTPS availability
        https_test = test_https_availability(domain)
        results["tests"]["https_availability"] = https_test
        
        if https_test["score"] > 0:
            # Test certificate
            cert_test = test_certificate(domain)
            results["tests"]["certificate"] = cert_test
            
            # Test TLS version
            tls_version_test = test_tls_version(domain)
            results["tests"]["tls_version"] = tls_version_test
            
            # Test cipher suites
            cipher_test = test_cipher_suites(domain)
            results["tests"]["cipher_suites"] = cipher_test
        else:
            # Skip other tests if HTTPS is not available
            for test_name in ["certificate", "tls_version", "cipher_suites"]:
                results["tests"][test_name] = create_test_result(
                    test_name.replace("_", " ").title(),
                    "skipped",
                    Score.FAILED,
                    {"reason": "HTTPS not available"}
                )
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in TLS test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_https_availability(domain):
    """
    Test if a domain has HTTPS available
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        # Check if port 443 is open
        is_https_available = is_port_open(domain, 443)
        
        if is_https_available:
            return create_test_result(
                "HTTPS Availability",
                "done",
                Score.GOOD,
                {"available": True}
            )
        else:
            return create_test_result(
                "HTTPS Availability",
                "done",
                Score.FAILED,
                {"available": False}
            )
    except Exception as e:
        return create_test_result(
            "HTTPS Availability",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_certificate(domain):
    """
    Test the SSL certificate for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        # Create SSL connection
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.set_verify(SSL.VERIFY_PEER, lambda *args: True)
        
        conn = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        conn.settimeout(5)
        conn.connect((domain, 443))
        conn.setblocking(1)
        conn.do_handshake()
        conn.set_tlsext_host_name(domain.encode())
        
        # Get certificate
        cert = conn.get_peer_certificate()
        conn.close()
        
        if not cert:
            return create_test_result(
                "Certificate",
                "done",
                Score.FAILED,
                {"valid": False, "reason": "No certificate found"}
            )
        
        # Check certificate validity
        not_before = datetime.datetime.strptime(cert.get_notBefore().decode('ascii'), "%Y%m%d%H%M%SZ")
        not_after = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), "%Y%m%d%H%M%SZ")
        now = datetime.datetime.utcnow()
        
        is_valid = now >= not_before and now <= not_after
        
        # Check if certificate matches domain
        common_name = cert.get_subject().CN
        is_domain_match = common_name == domain or (common_name.startswith('*.') and domain.endswith(common_name[2:]))
        
        # Get all SANs (Subject Alternative Names)
        alt_names = []
        for i in range(cert.get_extension_count()):
            ext = cert.get_extension(i)
            if ext.get_short_name() == b'subjectAltName':
                alt_names = str(ext).split(', ')
                break
        
        # Check if domain is in SANs
        has_san_match = False
        for name in alt_names:
            if name.startswith('DNS:'):
                san = name[4:]
                if san == domain or (san.startswith('*.') and domain.endswith(san[2:])):
                    has_san_match = True
                    break
        
        domain_match = is_domain_match or has_san_match
        
        if is_valid and domain_match:
            return create_test_result(
                "Certificate",
                "done",
                Score.GOOD,
                {
                    "valid": True,
                    "issuer": cert.get_issuer().CN,
                    "expires": not_after.isoformat(),
                    "subject": common_name,
                    "alt_names": alt_names
                }
            )
        else:
            reasons = []
            if not is_valid:
                reasons.append("Certificate is not valid")
            if not domain_match:
                reasons.append("Certificate does not match domain")
                
            return create_test_result(
                "Certificate",
                "done",
                Score.FAILED,
                {
                    "valid": False,
                    "reason": ", ".join(reasons),
                    "issuer": cert.get_issuer().CN,
                    "expires": not_after.isoformat(),
                    "subject": common_name
                }
            )
    except Exception as e:
        return create_test_result(
            "Certificate",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_tls_version(domain):
    """
    Test supported TLS versions for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        supported_versions = []
        
        # Test TLSv1.2
        try:
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_2
            
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    supported_versions.append(ssock.version())
        except:
            pass
            
        # Test TLSv1.3
        try:
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    supported_versions.append(ssock.version())
        except:
            pass
        
        if 'TLSv1.3' in supported_versions:
            score = Score.GOOD
        elif 'TLSv1.2' in supported_versions:
            score = Score.SUFFICIENT
        else:
            score = Score.FAILED
            
        return create_test_result(
            "TLS Version",
            "done",
            score,
            {"supported_versions": supported_versions}
        )
    except Exception as e:
        return create_test_result(
            "TLS Version",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_cipher_suites(domain):
    """
    Test supported cipher suites for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        context = SSL.Context(SSL.SSLv23_METHOD)
        
        conn = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        conn.settimeout(5)
        conn.connect((domain, 443))
        conn.setblocking(1)
        conn.do_handshake()
        
        # Get cipher used
        cipher = conn.get_cipher_name()
        protocol = conn.get_protocol_version_name()
        conn.close()
        
        # Check if cipher is secure
        is_secure_cipher = any(secure in cipher for secure in SECURE_CIPHER_SUITES)
        is_secure_protocol = protocol in SECURE_PROTOCOLS
        
        if is_secure_cipher and is_secure_protocol:
            return create_test_result(
                "Cipher Suites",
                "done",
                Score.GOOD,
                {
                    "cipher": cipher,
                    "protocol": protocol,
                    "secure": True
                }
            )
        else:
            reasons = []
            if not is_secure_cipher:
                reasons.append("Insecure cipher suite")
            if not is_secure_protocol:
                reasons.append("Insecure protocol")
                
            return create_test_result(
                "Cipher Suites",
                "done",
                Score.WARNING if is_secure_protocol else Score.FAILED,
                {
                    "cipher": cipher,
                    "protocol": protocol,
                    "secure": False,
                    "reason": ", ".join(reasons)
                }
            )
    except Exception as e:
        return create_test_result(
            "Cipher Suites",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

# Function to test STARTTLS for email servers (used in email_tests.py)
def test_starttls(domain):
    """
    Test STARTTLS support for a mail server
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing STARTTLS for email server: {domain}")
    
    results = {
        "name": "STARTTLS",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for MX records
        import socket
        import ssl
        import smtplib
        
        # Get MX records
        import dns.resolver
        mx_records = []
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            for rdata in answers:
                mx_records.append(str(rdata.exchange))
        except:
            pass
        
        if not mx_records:
            results["tests"]["mx_records"] = create_test_result(
                "MX Records",
                "done",
                Score.FAILED,
                {"records": []}
            )
            results["score"] = Score.FAILED.value
            results["status"] = TestStatus.DONE.value
            return results
            
        results["tests"]["mx_records"] = create_test_result(
            "MX Records",
            "done",
            Score.GOOD,
            {"records": mx_records}
        )
        
        # Test STARTTLS on each MX server
        starttls_supported = False
        for mx in mx_records:
            try:
                smtp = smtplib.SMTP(mx, 25, timeout=10)
                smtp.ehlo()
                if smtp.has_extn('STARTTLS'):
                    starttls_supported = True
                    smtp.starttls()
                    # Test TLS version and cipher after STARTTLS
                    cipher = smtp.sock.cipher()
                    smtp.quit()
                    break
                smtp.quit()
            except:
                continue
        
        if starttls_supported:
            results["tests"]["starttls_support"] = create_test_result(
                "STARTTLS Support",
                "done",
                Score.GOOD,
                {"supported": True}
            )
        else:
            results["tests"]["starttls_support"] = create_test_result(
                "STARTTLS Support",
                "done",
                Score.FAILED,
                {"supported": False}
            )
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in STARTTLS test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results
