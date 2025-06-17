"""
IPv6 testing module for Internet security tests.
Replaces Django-specific IPv6 testing implementation.
"""
import logging
import socket
from .shared import dns_lookup, create_test_result, get_domain_ip_addresses
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

def test_ipv6_website(domain):
    """
    Test IPv6 support for a website
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing IPv6 for website: {domain}")
    
    results = {
        "name": "IPv6",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for AAAA records
        aaaa_test = test_aaaa_records(domain)
        results["tests"]["aaaa_records"] = aaaa_test
        
        # Test for IPv6 reachability
        if aaaa_test["score"] > 0:
            reach_test = test_ipv6_reachability(domain)
            results["tests"]["reachability"] = reach_test
        else:
            reach_test = create_test_result(
                "IPv6 Reachability",
                "skipped",
                Score.FAILED,
                {"reason": "No AAAA records found"}
            )
            results["tests"]["reachability"] = reach_test
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in IPv6 test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_aaaa_records(domain):
    """
    Test if a domain has AAAA records
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        records = dns_lookup(domain, 'AAAA')
        
        if records and len(records) > 0:
            return create_test_result(
                "AAAA Records",
                "done",
                Score.GOOD,
                {"records": records}
            )
        else:
            return create_test_result(
                "AAAA Records",
                "done",
                Score.FAILED,
                {"records": []}
            )
    except Exception as e:
        return create_test_result(
            "AAAA Records",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_ipv6_reachability(domain):
    """
    Test if a domain is reachable over IPv6
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        ips = get_domain_ip_addresses(domain)
        ipv6_addresses = ips.get('ipv6', [])
        
        if not ipv6_addresses:
            return create_test_result(
                "IPv6 Reachability",
                "done",
                Score.FAILED,
                {"reachable": False, "reason": "No IPv6 addresses found"}
            )
        
        # Try to connect to port 80 (HTTP) on each IPv6 address
        reachable = False
        for ip in ipv6_addresses:
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, 80, 0, 0))  # IPv6 socket requires flow and scope ID
                sock.close()
                reachable = True
                break
            except:
                continue
        
        if reachable:
            return create_test_result(
                "IPv6 Reachability",
                "done",
                Score.GOOD,
                {"reachable": True}
            )
        else:
            return create_test_result(
                "IPv6 Reachability",
                "done",
                Score.FAILED,
                {"reachable": False, "reason": "Cannot connect to IPv6 addresses"}
            )
    except Exception as e:
        return create_test_result(
            "IPv6 Reachability",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_client_ipv6(client_ip):
    """
    Test if a client has IPv6 connectivity
    
    Args:
        client_ip (str): Client IP address
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing IPv6 for client: {client_ip}")
    
    results = {
        "name": "IPv6",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Check if client IP is IPv6
        is_ipv6 = ":" in client_ip
        
        if is_ipv6:
            client_test = create_test_result(
                "IPv6 Connection",
                "done",
                Score.GOOD,
                {"has_ipv6": True}
            )
        else:
            client_test = create_test_result(
                "IPv6 Connection",
                "done",
                Score.FAILED,
                {"has_ipv6": False}
            )
        
        results["tests"]["client_ipv6"] = client_test
        results["score"] = client_test["score"]
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in client IPv6 test: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results
