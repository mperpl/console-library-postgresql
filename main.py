# DROP TABLE IF EXISTS loans, book_copies, book_genres, books, users, authors, genres CASCADE;
# python -m db_config.db_setup

from db_config.db_config import engine
from display.display_books import display_books
from display.display_users import display_users
from display.display_authors import display_authors
from display.display_genres import display_genres
from books_management.issue_book import issue_book
from books_management.return_book import return_book
from addition.add_book import add_book
from addition.add_author import add_author
from addition.add_user import add_user
from addition.add_genre import add_genre
from removal.remove_book import remove_book
from removal.remove_author import remove_author
from removal.remove_user import remove_user
from removal.remove_genre import remove_genre
from modification.modify_book import modify_book
from modification.modify_author import modify_author
from modification.modify_user import modify_user
from modification.modify_genre import modify_genre

def print_instructions():
        print("\nPress one of the following keys:\n\n\
Issue book(I); Return book(G)\n\
DISPLAY(D); ADD NEW(A); REMOVE(R); MODIFY(M)\n\
SYSTEM: Quit program(X)")

while True:
    print_instructions()

    chosen_option = input("\nChosen option: ").strip().lower()

    # DISPLAY TAB
    if chosen_option == "d":
        print("You are in the DISPLAY tab\nWhat would you like to display?\nbooks(B), users(U), authors(A), genres(G), go back(X)")
        chosen_option = input("\nChosen option: ").strip().lower()
        if chosen_option == "b":
            display_books(engine)
        elif chosen_option == "u":
            display_users(engine)
        elif chosen_option == "a":
            display_authors(engine)
        elif chosen_option == "g":
            display_genres(engine)
        elif chosen_option == "x":
            continue
    
    # ADDITION TAB
    elif chosen_option == "a":
        print("You are in the ADDITION tab\nWhat would you like to ADD?\nbook(B), user(U), author(A), genre(G), go back(X)")
        chosen_option = input("\nChosen option: ").strip().lower()
        if chosen_option == "b":
            add_book(engine)
        elif chosen_option == "u":
            add_user(engine)
        elif chosen_option == "a":
            add_author(engine)
        elif chosen_option == "g":
            add_genre(engine)
        elif chosen_option == "x":
            continue

    # REMOVAL TAB
    elif chosen_option == "r":
        print("You are in the REMOVAL tab\nWhat would you like to REMOVE?\nbook(B), user(U), author(A), genre(G), go back(X)")
        chosen_option = input("\nChosen option: ").strip().lower()
        if chosen_option == "b":
            remove_book(engine)
        elif chosen_option == "u":
            remove_user(engine)
        elif chosen_option == "a":
            remove_author(engine)
        elif chosen_option == "g":
            remove_genre(engine)
        elif chosen_option == "x":
            continue

    # MODIFICATION TAB
    elif chosen_option == "m":
        print("You are in the MODIFICATION tab\nWhat would you like to MODIFY?\nbook(B), user(U), author(A), genre(G), go back(X)")
        chosen_option = input("\nChosen option: ").strip().lower()
        if chosen_option == "b":
            modify_book(engine)
        elif chosen_option == "u":
            modify_user(engine)
        elif chosen_option == "a":
            modify_author(engine)
        elif chosen_option == "g":
            modify_genre(engine)
        elif chosen_option == "x":
            continue

    elif chosen_option == "i":
        issue_book(engine)

    elif chosen_option == "g":
        return_book(engine)

    
    elif chosen_option == "x":
        break

    else:
        print("\n--------------\nNo such option\n--------------")
        continue