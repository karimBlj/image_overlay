import smtplib
import dns.resolver
import re

def is_valid_email(email):
    # Regular expression for validating an email address
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        return False
    
    # Extract domain from email address
    domain = email.split('@')[1]
    
    try:
        # Perform DNS lookup for MX records
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return False

    # SMTP setup
    try:
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('rimus@live.fr')
        code, message = server.rcpt(email)
        server.quit()

        # Check if the response code is 250 (means the email exists)
        return code == 250
    except Exception as e:
        return False

# Example usage
# is_valid = is_valid_email(email)
# print(f"The email address {email} is {'valid' if is_valid else 'invalid'}.")
