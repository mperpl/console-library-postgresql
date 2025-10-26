def validate_genre(msg):
    while True:
        genre_input = input(msg).strip().lower()
        if not genre_input:
            print('Input can\'t be empty.')
            continue

        temp_genre = genre_input.replace('-', '')

        if temp_genre.isalpha():
            return genre_input
        else: 
            print('Improper input.')