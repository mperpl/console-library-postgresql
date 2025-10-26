import re

def validate_phone_number(msg):
    phone_pattern = re.compile(r'^\+?\d{9,15}$') 
    while True:
        phone_number = input(msg).strip().replace('-', '').replace(' ', '')
        if phone_pattern.match(phone_number):
            return phone_number
        else:
            print('[ERROR] Improper number')