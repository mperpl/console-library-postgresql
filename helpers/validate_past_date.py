from datetime import datetime

def validate_past_date(msg):
    while True:
        date_str = input(msg).strip()
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj >= datetime.date.today():
                print("[ERROR] The date must be time in the past.")
                continue
            return date_obj
        except ValueError:
            print("[ERROR] Improper date format.")