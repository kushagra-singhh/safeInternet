"""
SPF (Sender Policy Framework) parser and testing module.
Replaces Django-specific SPF implementation.
"""
import logging
import re
from .shared import create_test_result, dns_lookup
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

def test_spf(domain):
    """
    Test SPF configuration for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing SPF for domain: {domain}")
    
    results = {
        "name": "SPF",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for SPF record
        record_test = test_spf_record(domain)
        results["tests"]["spf_record"] = record_test
        
        if record_test["score"] > 0:
            # Test SPF syntax
            syntax_test = test_spf_syntax(domain)
            results["tests"]["syntax"] = syntax_test
        else:
            # Skip syntax test if no SPF record
            results["tests"]["syntax"] = create_test_result(
                "SPF Syntax",
                "skipped",
                Score.FAILED,
                {"reason": "No SPF record found"}
            )
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in SPF test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_spf_record(domain):
    """
    Test if a domain has an SPF record
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        txt_records = dns_lookup(domain, 'TXT')
        
        spf_records = [record for record in txt_records if record.startswith('v=spf1')]
        
        if spf_records:
            if len(spf_records) > 1:
                return create_test_result(
                    "SPF Record",
                    "done",
                    Score.WARNING,
                    {"records": spf_records, "note": "Multiple SPF records found"}
                )
            else:
                return create_test_result(
                    "SPF Record",
                    "done",
                    Score.GOOD,
                    {"record": spf_records[0]}
                )
        else:
            return create_test_result(
                "SPF Record",
                "done",
                Score.FAILED,
                {"records": []}
            )
    except Exception as e:
        return create_test_result(
            "SPF Record",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_spf_syntax(domain):
    """
    Test SPF syntax for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        txt_records = dns_lookup(domain, 'TXT')
        
        spf_records = [record for record in txt_records if record.startswith('v=spf1')]
        
        if not spf_records:
            return create_test_result(
                "SPF Syntax",
                "skipped",
                Score.FAILED,
                {"reason": "No SPF record found"}
            )
        
        # Use the first SPF record
        spf_record = spf_records[0]
        
        # Check for common syntax errors
        errors = []
        
        # Check for missing all mechanism
        if not re.search(r'\s(?:[-~+?])?all\b', spf_record):
            errors.append("Missing 'all' mechanism")
        
        # Check for too many DNS lookups (max 10 allowed)
        lookups = 0
        for mechanism in re.finditer(r'\b(?:include|exists|a|mx):[^\s]+', spf_record):
            lookups += 1
        
        if lookups > 10:
            errors.append(f"Too many DNS lookups ({lookups}), maximum is 10")
        
        # Check for nested includes (can cause issues)
        if 'include:' in spf_record:
            for include_match in re.finditer(r'include:([^\s]+)', spf_record):
                included_domain = include_match.group(1)
                try:
                    included_txt = dns_lookup(included_domain, 'TXT')
                    for record in included_txt:
                        if 'include:' in record:
                            errors.append(f"Nested includes detected: {included_domain}")
                            break
                except:
                    errors.append(f"Cannot resolve included domain: {included_domain}")
        
        if errors:
            return create_test_result(
                "SPF Syntax",
                "done",
                Score.WARNING,
                {"record": spf_record, "errors": errors}
            )
        else:
            return create_test_result(
                "SPF Syntax",
                "done",
                Score.GOOD,
                {"record": spf_record, "valid": True}
            )
    except Exception as e:
        return create_test_result(
            "SPF Syntax",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )
