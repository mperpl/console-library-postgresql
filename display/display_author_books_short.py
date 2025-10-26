from helpers.get_author_books import get_author_books

def display_author_books_short(engine, author_id):
    data = get_author_books(engine, author_id)

    if data:
        print(f"{data[4]} (id: {data[3]})")
        print("\ndisplay_author_books_short ran\n")
        return True
    else:
        print('No book data')
        return False
            
