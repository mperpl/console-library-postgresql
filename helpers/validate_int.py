def validate_int(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("[ERROR] Improper input. Integers only!")