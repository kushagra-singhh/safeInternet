# tests package
# Import all test modules to make them available to the application

from . import (
    scoring,
    shared,
    ipv6,
    dnssec,
    tls,
    appsecpriv,
    mail,
    spf_parser,
    dmarc_parser,
    website_tests,
    email_tests,
    connection_tests
)
