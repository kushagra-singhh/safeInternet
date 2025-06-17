import logging
from .scoring import Score, TestStatus
from . import ipv6

logger = logging.getLogger(__name__)

def run_connection_tests(client_ip):
    """
    Run connection tests for a client
    
    Args:
        client_ip (str): Client IP address
    
    Returns:
        dict: Results of all tests
    """
    logger.info(f"Running connection tests for IP: {client_ip}")
    
    # Initialize results dictionary
    results = {
        "client_ip": client_ip,
        "timestamp": _get_timestamp(),
        "status": TestStatus.RUNNING.value,
        "categories": {},
        "score": None
    }
    
    try:
        # Run tests
        ipv6_results = ipv6.test_client_ipv6(client_ip)
        
        # Combine results
        results["categories"] = {
            "ipv6": ipv6_results
        }
        
        # Calculate overall score
        results["score"] = calculate_connection_score(results["categories"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in connection test for {client_ip}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def calculate_connection_score(categories):
    """
    Calculate the overall score for connection tests
    
    Args:
        categories (dict): Dictionary containing test category results
    
    Returns:
        float: Overall score between 0 and 100
    """
    scores = []
    weights = {
        "ipv6": 1.0
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
