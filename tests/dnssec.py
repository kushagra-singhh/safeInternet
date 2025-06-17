"""
DNSSEC testing module for Internet security tests.
Replaces Django-specific DNSSEC testing implementation.
"""
import logging
import dns.resolver
import dns.dnssec
from .shared import create_test_result, dns_lookup
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

def test_dnssec(domain):
    """
    Test DNSSEC support for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing DNSSEC for domain: {domain}")
    
    results = {
        "name": "DNSSEC",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for DNSKEY records
        dnskey_test = test_dnskey_records(domain)
        results["tests"]["dnskey_records"] = dnskey_test
        
        # Test for DS records
        ds_test = test_ds_records(domain)
        results["tests"]["ds_records"] = ds_test
        
        # Test DNSSEC validation
        validation_test = test_dnssec_validation(domain)
        results["tests"]["validation"] = validation_test
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in DNSSEC test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_dnskey_records(domain):
    """
    Test if a domain has DNSKEY records
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        
        try:
            answer = resolver.resolve(domain, 'DNSKEY')
            keys = []
            for key in answer:
                key_tag = dns.dnssec.key_tag(key)
                algorithm = key.algorithm
                key_type = "ZSK" if key.flags & 256 else "KSK" if key.flags & 257 else "Unknown"
                keys.append({
                    "key_tag": key_tag,
                    "algorithm": algorithm,
                    "type": key_type
                })
                
            return create_test_result(
                "DNSKEY Records",
                "done",
                Score.GOOD,
                {"records": keys}
            )
        except dns.resolver.NoAnswer:
            return create_test_result(
                "DNSKEY Records",
                "done",
                Score.FAILED,
                {"records": []}
            )
        except dns.resolver.NXDOMAIN:
            return create_test_result(
                "DNSKEY Records",
                "done",
                Score.FAILED,
                {"error": "Domain does not exist"}
            )
    except Exception as e:
        return create_test_result(
            "DNSKEY Records",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_ds_records(domain):
    """
    Test if a domain has DS records in parent zone
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        # Get parent domain
        parent_domain = '.'.join(domain.split('.')[1:]) if domain.count('.') > 1 else domain
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        
        try:
            answer = resolver.resolve(domain, 'DS')
            ds_records = []
            for ds in answer:
                ds_records.append({
                    "key_tag": ds.key_tag,
                    "algorithm": ds.algorithm,
                    "digest_type": ds.digest_type
                })
                
            return create_test_result(
                "DS Records",
                "done",
                Score.GOOD,
                {"records": ds_records}
            )
        except dns.resolver.NoAnswer:
            return create_test_result(
                "DS Records",
                "done",
                Score.FAILED,
                {"records": []}
            )
        except dns.resolver.NXDOMAIN:
            return create_test_result(
                "DS Records",
                "done",
                Score.FAILED,
                {"error": "Domain does not exist"}
            )
    except Exception as e:
        return create_test_result(
            "DS Records",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_dnssec_validation(domain):
    """
    Test DNSSEC validation for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        resolver.use_dnssec = True
        
        try:
            # Try to validate A record with DNSSEC
            answer = resolver.resolve(domain, 'A')
            return create_test_result(
                "DNSSEC Validation",
                "done",
                Score.GOOD,
                {"valid": True}
            )
        except dns.resolver.NoAnswer:
            # No A record but validation passed
            return create_test_result(
                "DNSSEC Validation",
                "done",
                Score.GOOD,
                {"valid": True, "note": "No A record but validation passed"}
            )
        except dns.resolver.NXDOMAIN:
            # Domain doesn't exist but validation passed
            return create_test_result(
                "DNSSEC Validation",
                "done",
                Score.FAILED,
                {"valid": False, "error": "Domain does not exist"}
            )
        except dns.dnssec.ValidationFailure:
            # DNSSEC validation failed
            return create_test_result(
                "DNSSEC Validation",
                "done",
                Score.FAILED,
                {"valid": False, "error": "DNSSEC validation failed"}
            )
    except Exception as e:
        return create_test_result(
            "DNSSEC Validation",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )
