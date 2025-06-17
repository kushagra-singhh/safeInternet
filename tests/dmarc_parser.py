"""
DMARC (Domain-based Message Authentication, Reporting, and Conformance) parser and testing module.
Replaces Django-specific DMARC implementation.
"""
import logging
import re
from urllib.parse import parse_qs
from .shared import create_test_result, dns_lookup
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

def test_dmarc(domain):
    """
    Test DMARC configuration for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing DMARC for domain: {domain}")
    
    results = {
        "name": "DMARC",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for DMARC record
        record_test = test_dmarc_record(domain)
        results["tests"]["dmarc_record"] = record_test
        
        if record_test["score"] > 0:
            # Parse and validate DMARC policy
            policy_test = test_dmarc_policy(domain)
            results["tests"]["policy"] = policy_test
        else:
            # Skip policy test if no DMARC record
            results["tests"]["policy"] = create_test_result(
                "DMARC Policy",
                "skipped",
                Score.FAILED,
                {"reason": "No DMARC record found"}
            )
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in DMARC test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_dmarc_record(domain):
    """
    Test if a domain has a DMARC record
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        dmarc_domain = f"_dmarc.{domain}"
        txt_records = dns_lookup(dmarc_domain, 'TXT')
        
        dmarc_records = [record for record in txt_records if record.startswith('v=DMARC1')]
        
        if dmarc_records:
            if len(dmarc_records) > 1:
                return create_test_result(
                    "DMARC Record",
                    "done",
                    Score.WARNING,
                    {"records": dmarc_records, "note": "Multiple DMARC records found"}
                )
            else:
                return create_test_result(
                    "DMARC Record",
                    "done",
                    Score.GOOD,
                    {"record": dmarc_records[0]}
                )
        else:
            return create_test_result(
                "DMARC Record",
                "done",
                Score.FAILED,
                {"records": []}
            )
    except Exception as e:
        return create_test_result(
            "DMARC Record",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_dmarc_policy(domain):
    """
    Test DMARC policy for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        dmarc_domain = f"_dmarc.{domain}"
        txt_records = dns_lookup(dmarc_domain, 'TXT')
        
        dmarc_records = [record for record in txt_records if record.startswith('v=DMARC1')]
        
        if not dmarc_records:
            return create_test_result(
                "DMARC Policy",
                "skipped",
                Score.FAILED,
                {"reason": "No DMARC record found"}
            )
        
        # Use the first DMARC record
        dmarc_record = dmarc_records[0]
        
        # Parse DMARC record
        tags = {}
        for tag_pair in dmarc_record.split(';'):
            tag_pair = tag_pair.strip()
            if '=' in tag_pair:
                key, value = tag_pair.split('=', 1)
                tags[key.strip()] = value.strip()
        
        # Check policy
        policy = tags.get('p', 'none')
        
        # Evaluate policy strength
        if policy == 'reject':
            policy_score = Score.GOOD
            policy_note = "Strong policy (reject)"
        elif policy == 'quarantine':
            policy_score = Score.SUFFICIENT
            policy_note = "Medium policy (quarantine)"
        else:  # none or other
            policy_score = Score.WARNING
            policy_note = "Weak policy (none)"
        
        # Check reporting
        has_reporting = 'rua' in tags or 'ruf' in tags
        
        # Check if both SPF and DKIM alignment is required
        aspf = tags.get('aspf', 'r')
        adkim = tags.get('adkim', 'r')
        strict_alignment = aspf == 's' and adkim == 's'
        
        # Create details dictionary
        details = {
            "record": dmarc_record,
            "policy": policy,
            "has_reporting": has_reporting,
            "strict_alignment": strict_alignment,
            "tags": tags
        }
        
        return create_test_result(
            "DMARC Policy",
            "done",
            policy_score,
            details
        )
    except Exception as e:
        return create_test_result(
            "DMARC Policy",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )
