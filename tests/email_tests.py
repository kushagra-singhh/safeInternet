import logging
from .scoring import Score, TestStatus
from .shared import dns_lookup
from . import tls, mail, spf_parser, dmarc_parser

logger = logging.getLogger(__name__)

def run_email_tests(domain):
    """
    Run all email tests for a given domain
    
    Args:
        domain (str): Domain name to test
    
    Returns:
        dict: Results of all tests
    """
    logger.info(f"Running email tests for domain: {domain}")
    
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
        spf_results = spf_parser.test_spf(domain)
        dkim_results = mail.test_dkim(domain)
        dmarc_results = dmarc_parser.test_dmarc(domain)
        starttls_results = mail.test_starttls(domain)
        
        # Combine results
        results["categories"] = {
            "spf": spf_results,
            "dkim": dkim_results,
            "dmarc": dmarc_results,
            "starttls": starttls_results
        }
        
        # Calculate overall score
        results["score"] = calculate_email_score(results["categories"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in email test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def calculate_email_score(categories):
    """
    Calculate the overall score for email tests
    
    Args:
        categories (dict): Dictionary containing test category results
    
    Returns:
        float: Overall score between 0 and 100
    """
    scores = []
    weights = {
        "spf": 0.25,
        "dkim": 0.25,
        "dmarc": 0.25,
        "starttls": 0.25
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
