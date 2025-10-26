import re

def validate_email(msg):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    while True:
        email = input(msg).strip()
        if email_pattern.match(email):
            return email
        else:
            print('[ERROR] Improper format of e-mail. Must be user@domain.com')