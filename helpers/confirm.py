def confirm(msg):
    answer = input(msg).strip().lower()
    if answer == 'y': return True
    return False