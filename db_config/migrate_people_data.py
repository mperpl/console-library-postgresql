from sqlalchemy import text

def migrate_people_data(engine):
    try:
        with engine.begin() as con:
            with open('./db_config/people_data.txt', 'r', encoding='utf-8') as data:
                lines = data.readlines()
                for line in lines:
                    if not line:
                        continue
                    line = line.strip()

                    split_line = line.split("|")

                    first_name = split_line[1]
                    last_name = split_line[2]
                    phone = split_line[0][2:]
                    phone_standardized = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
                    if len(split_line) > 4:
                        books = split_line[4].split("[]")
                    else: books = []

                    print('first_name',first_name)
                    print('last_name',last_name)
                    print('phone',phone)
                    print('phone_standardized',phone_standardized)
                    print('books',books)

                    # add user
                    user_id = None

                    insert_user = con.execute(text("""
                            INSERT INTO users (first_name, last_name, phone_number) VALUES (:first_name, :last_name, :phone_number) ON CONFLICT (first_name, last_name, phone_number) DO NOTHING RETURNING id;"""),
                            {'first_name': first_name, 'last_name': last_name, 'phone_number': phone_standardized}).fetchone()
                    if insert_user:
                        user_id = insert_user[0]
                    else:
                        select_user_id = con.execute(text("""
                            SELECT id FROM users WHERE first_name = :first_name AND last_name = :last_name AND phone_number = :phone_standardized;"""),
                            {'first_name': first_name, 'last_name': last_name, 'phone_standardized': phone_standardized}).fetchone()
                        if select_user_id:
                            user_id = select_user_id[0]

                    
                    print('user_id:', user_id)

                    # add loan
                    if user_id and books:
                        for title in books: 
                            select_book_copy_id = con.execute(text("""
                                SELECT bc.id 
                                FROM book_copies bc
                                JOIN books b ON bc.book_id = b.id
                                WHERE b.title = :title
                                AND NOT EXISTS (
                                    SELECT 1 FROM loans l WHERE l.book_copy_id = bc.id
                                )
                                LIMIT 1;"""),
                                {'title': title}).fetchone()

                            if select_book_copy_id:
                                book_copy_id = select_book_copy_id[0]
                                
                                con.execute(text("""
                                    INSERT INTO loans (user_id, book_copy_id, loan_date) VALUES (:user_id, :book_copy_id, NULL);"""),
                                    {'user_id': user_id, 'book_copy_id': book_copy_id})
                                
                                print(f"Wypożyczenie dodane: Użytkownik {user_id} wypożyczył '{title}' (ID egzemplarza: {book_copy_id})")
                            else:
                                print(f"Brak dostępnego egzemplarza dla '{title}'. Wypożyczenie nie zostało dodane.")
                            

                        

    except Exception as e:
        print("Error during migration:", e)