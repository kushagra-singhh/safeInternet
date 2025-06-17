"""
Scoring module for Internet security tests.
Replaces Django-specific scoring implementation.
"""
from enum import Enum, auto

# Constants for test scoring
MAX_SCORE = 100
MIN_SCORE = 0

# Scoring weights
class Weights:
    # Website tests
    IPV6_WEIGHT = 0.25
    DNSSEC_WEIGHT = 0.25
    TLS_WEIGHT = 0.25
    APPSECPRIV_WEIGHT = 0.25
    
    # Email tests
    SPF_WEIGHT = 0.25
    DKIM_WEIGHT = 0.25
    DMARC_WEIGHT = 0.25
    STARTTLS_WEIGHT = 0.25

# Enum for test status
class TestStatus(Enum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"
    SCHEDULED = "scheduled"

# Enum for test score
class Score(Enum):
    GOOD = 100
    SUFFICIENT = 75
    WARNING = 50
    BAD = 25
    FAILED = 0
    
    @classmethod
    def to_int(cls, score):
        """Convert Score enum to integer value"""
        if isinstance(score, cls):
            return score.value
        return score

def calculate_percentage_score(score_counts):
    """
    Calculate a percentage score based on counts of different score values
    
    Args:
        score_counts (dict): Dictionary with Score enum keys and count values
        
    Returns:
        float: Percentage score between 0 and 100
    """
    total_tests = sum(score_counts.values())
    if total_tests == 0:
        return 0
    
    weighted_sum = 0
    for score, count in score_counts.items():
        weighted_sum += Score.to_int(score) * count
    
    return round(weighted_sum / total_tests, 1)

def get_status_from_score(score):
    """
    Get a descriptive status based on numerical score
    
    Args:
        score (float): Numerical score between 0 and 100
        
    Returns:
        str: Status description ('excellent', 'good', 'sufficient', 'bad')
    """
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 50:
        return "sufficient"
    else:
        return "bad"
