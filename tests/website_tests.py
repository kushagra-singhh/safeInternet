import logging
from .scoring import Score, TestStatus
from .shared import dns_lookup
from . import tls, ipv6, dnssec, appsecpriv

logger = logging.getLogger(__name__)

def run_website_tests(domain):
    """
    Run all website tests for a given domain
    
    Args:
        domain (str): Domain name to test
    
    Returns:
        dict: Results of all tests
    """
    logger.info(f"Running website tests for domain: {domain}")
    
    # Initialize results dictionary
    results = {
        "domain": domain,
        "timestamp": _get_timestamp(),
        "status": TestStatus.RUNNING.value,
        "categories": {},
        "score": None
    }
    
    try:
        # Run tests for each category
        ipv6_results = ipv6.test_ipv6_website(domain)
        dnssec_results = dnssec.test_dnssec(domain)
        tls_results = tls.test_tls_website(domain)
        appsecpriv_results = appsecpriv.test_website_security(domain)
        
        # Combine results
        results["categories"] = {
            "ipv6": ipv6_results,
            "dnssec": dnssec_results,
            "tls": tls_results,
            "appsecpriv": appsecpriv_results
        }
        
        # Calculate overall score
        results["score"] = calculate_website_score(results["categories"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in website test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def calculate_website_score(categories):
    """
    Calculate the overall score for website tests
    
    Args:
        categories (dict): Dictionary containing test category results
    
    Returns:
        float: Overall score between 0 and 100
    """
    scores = []
    weights = {
        "ipv6": 0.25,
        "dnssec": 0.25,
        "tls": 0.25,
        "appsecpriv": 0.25
    }
    
    for category, result in categories.items():
        if "score" in result:
            scores.append(result["score"] * weights[category])
    
    if not scores:
        return 0
    
    return round(sum(scores), 1)

def _get_timestamp():
    """Get current timestamp in ISO format"""
    from datetime import datetime
    return datetime.utcnow().isoformat()
