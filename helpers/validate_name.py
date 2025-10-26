import re

def validate_name(msg):
    NAME_REGEX = re.compile(r'^[a-zA-Z\s\-]+$')
    
    while True:
        name = input(msg).strip()
        
        if not name:
            print('Name field can\'t be empty')
            continue

        if NAME_REGEX.match(name):
            return name
        else:
            print('Improper input.')
