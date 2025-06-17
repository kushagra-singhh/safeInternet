"""
Application security and privacy testing module for Internet security tests.
Replaces Django-specific security and privacy testing implementation.
"""
import logging
import requests
from urllib.parse import urlparse
from .shared import create_test_result
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

# Security headers to check
SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'description': 'Enforces secure (HTTPS) connections to the server',
        'recommended': 'max-age=31536000; includeSubDomains'
    },
    'Content-Security-Policy': {
        'description': 'Prevents cross-site scripting (XSS) and other code injection attacks',
        'recommended': 'default-src \'self\''
    },
    'X-Content-Type-Options': {
        'description': 'Prevents MIME-sniffing of the response from the declared content-type',
        'recommended': 'nosniff'
    },
    'X-Frame-Options': {
        'description': 'Protects against clickjacking attacks',
        'recommended': 'DENY or SAMEORIGIN'
    },
    'X-XSS-Protection': {
        'description': 'Enables cross-site scripting filtering in browsers',
        'recommended': '1; mode=block'
    },
    'Referrer-Policy': {
        'description': 'Controls how much referrer information is sent with requests',
        'recommended': 'strict-origin-when-cross-origin'
    }
}

def test_website_security(domain):
    """
    Test security and privacy features of a website
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing website security for domain: {domain}")
    
    results = {
        "name": "Security & Privacy",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test HTTPS redirection
        redirect_test = test_https_redirect(domain)
        results["tests"]["https_redirect"] = redirect_test
        
        # Test security headers
        headers_test = test_security_headers(domain)
        results["tests"]["security_headers"] = headers_test
        
        # Test cookie security
        cookie_test = test_cookie_security(domain)
        results["tests"]["cookie_security"] = cookie_test
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in security test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_https_redirect(domain):
    """
    Test if a domain redirects HTTP to HTTPS
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        response = requests.get(f"http://{domain}", timeout=10, allow_redirects=True)
        final_url = response.url
        
        redirects_to_https = final_url.startswith('https://')
        
        if redirects_to_https:
            return create_test_result(
                "HTTPS Redirect",
                "done",
                Score.GOOD,
                {"redirects": True, "final_url": final_url}
            )
        else:
            return create_test_result(
                "HTTPS Redirect",
                "done",
                Score.FAILED,
                {"redirects": False, "final_url": final_url}
            )
    except Exception as e:
        return create_test_result(
            "HTTPS Redirect",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_security_headers(domain):
    """
    Test security headers for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        response = requests.get(f"https://{domain}", timeout=10, verify=True)
        
        headers = response.headers
        security_headers_found = {}
        
        for header in SECURITY_HEADERS:
            security_headers_found[header] = header in headers
        
        # Count how many security headers are present
        headers_count = sum(1 for present in security_headers_found.values() if present)
        total_headers = len(SECURITY_HEADERS)
        
        # Determine score based on percentage of headers present
        if headers_count == total_headers:
            score = Score.GOOD
        elif headers_count >= total_headers * 0.7:
            score = Score.SUFFICIENT
        elif headers_count >= total_headers * 0.4:
            score = Score.WARNING
        else:
            score = Score.BAD
            
        return create_test_result(
            "Security Headers",
            "done",
            score,
            {
                "headers": security_headers_found,
                "found": headers_count,
                "total": total_headers
            }
        )
    except Exception as e:
        return create_test_result(
            "Security Headers",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_cookie_security(domain):
    """
    Test cookie security for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        response = requests.get(f"https://{domain}", timeout=10, verify=True)
        
        cookies = response.cookies
        cookie_count = len(cookies)
        
        if cookie_count == 0:
            return create_test_result(
                "Cookie Security",
                "done",
                Score.GOOD,
                {"cookies": 0, "note": "No cookies set"}
            )
        
        secure_count = 0
        httponly_count = 0
        samesite_count = 0
        
        for cookie in cookies:
            if cookie.secure:
                secure_count += 1
            if cookie.has_nonstandard_attr('httponly'):
                httponly_count += 1
            if cookie.has_nonstandard_attr('samesite'):
                samesite_count += 1
        
        secure_percent = secure_count / cookie_count
        httponly_percent = httponly_count / cookie_count
        samesite_percent = samesite_count / cookie_count
        
        # Calculate average security score
        security_score = (secure_percent + httponly_percent + samesite_percent) / 3
        
        if security_score >= 0.9:
            score = Score.GOOD
        elif security_score >= 0.7:
            score = Score.SUFFICIENT
        elif security_score >= 0.4:
            score = Score.WARNING
        else:
            score = Score.BAD
            
        return create_test_result(
            "Cookie Security",
            "done",
            score,
            {
                "cookies": cookie_count,
                "secure": secure_count,
                "httponly": httponly_count,
                "samesite": samesite_count,
                "security_score": round(security_score * 100, 1)
            }
        )
    except Exception as e:
        return create_test_result(
            "Cookie Security",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )
