"""
Mail testing module for Internet security tests.
Replaces Django-specific mail testing implementation.
"""
import logging
import socket
import smtplib
import ssl
from .shared import create_test_result, dns_lookup
from .scoring import Score, TestStatus

logger = logging.getLogger(__name__)

def test_mail(domain):
    """
    Test mail server configuration for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test results
    """
    logger.info(f"Testing mail server for domain: {domain}")
    
    results = {
        "name": "Mail",
        "status": TestStatus.RUNNING.value,
        "tests": {},
        "score": None
    }
    
    try:
        # Test for MX records
        mx_test = test_mx_records(domain)
        results["tests"]["mx_records"] = mx_test
        
        if mx_test["score"] > 0:
            # Test STARTTLS
            starttls_test = test_starttls(domain)
            results["tests"]["starttls"] = starttls_test
            
            # Test DKIM
            dkim_test = test_dkim(domain)
            results["tests"]["dkim"] = dkim_test
        else:
            # Skip other tests if no MX records
            for test_name in ["starttls", "dkim"]:
                results["tests"][test_name] = create_test_result(
                    test_name.replace("_", " ").title(),
                    "skipped",
                    Score.FAILED,
                    {"reason": "No MX records found"}
                )
        
        # Calculate overall score
        score_sum = sum(test["score"] for test in results["tests"].values())
        results["score"] = score_sum / len(results["tests"])
        results["status"] = TestStatus.DONE.value
        
    except Exception as e:
        logger.error(f"Error in mail test for {domain}: {str(e)}")
        results["status"] = TestStatus.ERROR.value
        results["error"] = str(e)
    
    return results

def test_mx_records(domain):
    """
    Test MX records for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        mx_records = dns_lookup(domain, 'MX')
        
        if mx_records and len(mx_records) > 0:
            return create_test_result(
                "MX Records",
                "done",
                Score.GOOD,
                {"records": mx_records}
            )
        else:
            return create_test_result(
                "MX Records",
                "done",
                Score.FAILED,
                {"records": []}
            )
    except Exception as e:
        return create_test_result(
            "MX Records",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_starttls(domain):
    """
    Test STARTTLS support for a domain's mail servers
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        mx_records = dns_lookup(domain, 'MX')
        
        if not mx_records or len(mx_records) == 0:
            return create_test_result(
                "STARTTLS",
                "skipped",
                Score.FAILED,
                {"reason": "No MX records found"}
            )
        
        # Test each MX server
        results = []
        for mx in mx_records:
            try:
                smtp = smtplib.SMTP(mx, 25, timeout=10)
                smtp.ehlo()
                starttls_supported = smtp.has_extn('STARTTLS')
                
                if starttls_supported:
                    # Try to establish STARTTLS connection
                    context = ssl.create_default_context()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                    results.append({
                        "server": mx,
                        "starttls": True,
                        "protocol": smtp.sock.version()
                    })
                else:
                    results.append({
                        "server": mx,
                        "starttls": False
                    })
                
                smtp.quit()
            except Exception as e:
                results.append({
                    "server": mx,
                    "starttls": False,
                    "error": str(e)
                })
        
        # Check if all servers support STARTTLS
        all_support_starttls = all(result.get("starttls", False) for result in results)
        
        if all_support_starttls:
            return create_test_result(
                "STARTTLS",
                "done",
                Score.GOOD,
                {"servers": results}
            )
        elif any(result.get("starttls", False) for result in results):
            return create_test_result(
                "STARTTLS",
                "done",
                Score.WARNING,
                {"servers": results, "note": "Some servers don't support STARTTLS"}
            )
        else:
            return create_test_result(
                "STARTTLS",
                "done",
                Score.FAILED,
                {"servers": results, "note": "No servers support STARTTLS"}
            )
    except Exception as e:
        return create_test_result(
            "STARTTLS",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )

def test_dkim(domain):
    """
    Test DKIM configuration for a domain
    
    Args:
        domain (str): Domain name to test
        
    Returns:
        dict: Test result
    """
    try:
        # Check for DKIM records (common selectors)
        selectors = ['default', 'mail', 'email', 'dkim', 'selector1', 'selector2']
        dkim_records = []
        
        for selector in selectors:
            try:
                records = dns_lookup(f"{selector}._domainkey.{domain}", 'TXT')
                if records and any('v=DKIM1' in record for record in records):
                    dkim_records.append({
                        "selector": selector,
                        "record": records[0]
                    })
            except:
                continue
        
        if dkim_records:
            return create_test_result(
                "DKIM",
                "done",
                Score.GOOD,
                {"records": dkim_records}
            )
        else:
            return create_test_result(
                "DKIM",
                "done",
                Score.FAILED,
                {"records": [], "note": "No DKIM records found with common selectors"}
            )
    except Exception as e:
        return create_test_result(
            "DKIM",
            "error",
            Score.FAILED,
            {"error": str(e)}
        )
