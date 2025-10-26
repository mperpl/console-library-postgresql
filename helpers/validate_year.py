def validate_year(msg):
    while True:
        try:
            year = input(msg).strip()
            if not year: return None
            return int(year)
        except ValueError:
            print("[ERROR] Improper input. Integers only!")