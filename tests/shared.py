"""
Shared utility functions for Internet security tests.
Replaces Django-specific utility functions.
"""
import logging
import socket
import dns.resolver
import dns.exception
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers
from .scoring import Score

logger = logging.getLogger(__name__)

def dns_lookup(domain, record_type='A', timeout=5, nameservers=None):
    """
    Perform a DNS lookup for a specific record type
    
    Args:
        domain (str): Domain name to query
        record_type (str): DNS record type (A, AAAA, MX, TXT, etc.)
        timeout (int): Timeout in seconds
        nameservers (list): Optional list of nameservers to use
        
    Returns:
        list: List of record values
        
    Raises:
        NXDOMAIN: If domain does not exist
        NoAnswer: If no records exist for the requested type
        Exception: For other errors
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        resolver.lifetime = timeout
        
        if nameservers:
            resolver.nameservers = nameservers
        
        answer = resolver.resolve(domain, record_type)
        results = []
        
        for rdata in answer:
            if record_type in ('A', 'AAAA'):
                results.append(str(rdata.address))
            elif record_type == 'MX':
                results.append(str(rdata.exchange))
            elif record_type == 'TXT':
                results.append(str(rdata.strings[0].decode('utf-8')))
            else:
                results.append(str(rdata))
                
        return results
    
    except (NXDOMAIN, NoAnswer, NoNameservers) as e:
        logger.debug(f"DNS lookup failed for {domain} ({record_type}): {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in DNS lookup for {domain} ({record_type}): {str(e)}")
        raise

def is_domain_valid(domain):
    """
    Check if a domain is valid
    
    Args:
        domain (str): Domain name to check
        
    Returns:
        bool: True if domain is valid, False otherwise
    """
    try:
        # Check for valid domain format
        if not domain or len(domain) > 253:
            return False
        
        # Check if domain resolves
        dns_lookup(domain, 'A')
        return True
    except:
        return False

def is_ipv6_enabled(domain):
    """
    Check if IPv6 is enabled for a domain
    
    Args:
        domain (str): Domain name to check
        
    Returns:
        bool: True if IPv6 is enabled, False otherwise
    """
    try:
        records = dns_lookup(domain, 'AAAA')
        return len(records) > 0
    except:
        return False

def get_domain_ip_addresses(domain):
    """
    Get all IP addresses for a domain (both IPv4 and IPv6)
    
    Args:
        domain (str): Domain name to query
        
    Returns:
        dict: Dictionary with 'ipv4' and 'ipv6' keys containing lists of addresses
    """
    result = {
        'ipv4': [],
        'ipv6': []
    }
    
    try:
        result['ipv4'] = dns_lookup(domain, 'A')
    except:
        pass
    
    try:
        result['ipv6'] = dns_lookup(domain, 'AAAA')
    except:
        pass
        
    return result

def is_port_open(host, port, timeout=5):
    """
    Check if a port is open on a host
    
    Args:
        host (str): Hostname or IP address
        port (int): Port number
        timeout (int): Timeout in seconds
        
    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def create_test_result(name, status, score, details=None):
    """
    Create a standardized test result dictionary
    
    Args:
        name (str): Test name
        status (str): Test status
        score (Score): Test score (enum or int)
        details (dict): Optional details
        
    Returns:
        dict: Standardized test result
    """
    result = {
        "name": name,
        "status": status,
        "score": Score.to_int(score)
    }
    
    if details:
        result["details"] = details
        
    return result
