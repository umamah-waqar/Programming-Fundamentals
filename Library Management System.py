def add_book():
    print("\nAdd Book:")
    book_title = input("Enter book title: ")
    book_author = input("Enter author name: ")
    book_id = input("Enter book ID: ")
    book = {"title": book_title, "author": book_author, "book_id": book_id, "status": "available"}
    books_list.append(book)
    print("Book added successfully.")

def register_borrower():
    print("\nRegister Borrower:")
    name = input("Enter borrower name: ")
    contact_info = input("Enter contact number: ")
    borrower_id = input("Enter borrower ID: ")
    borrower = {"name": name, "contact_info": contact_info, "borrower_id": borrower_id}
    borrowers_list.append(borrower)
    print("Borrower registered successfully.")

def borrow_book():
    if len(books_list) == 0:
        print("Please Add Book First")
        add_book()
        return
    if len(borrowers_list) == 0:
        print("Please Register First")
        register_borrower()
        return
    print("\nBorrow Book:")
    book_id = input("Enter book ID: ")
    borrower_id = input("Enter borrower ID: ")
    current_book = find_book(book_id)
    current_borrower = find_borrower(borrower_id)
    if current_book is None:
        print("Book not found.")
    elif current_borrower is None:
        print("Borrower not found.")
    elif current_book["status"] == "borrowed":
        print("Book is already borrowed.")
    else:
        borrower_transactions = get_borrower_limit(borrower_id)
        if len(borrower_transactions) >= borrow_limit:
            print("Borrower has reached the borrowing limit.")
        else:
            transaction = {"book_id": book_id, "borrower_id": borrower_id, "status": "borrowed"}
            transactions_list.append(transaction)
            current_book["status"] = "borrowed"
            print("Book borrowed successfully.")

def return_book():
    print("\nReturn Book:")
    book_id = input("Enter book ID: ")
    borrower_id = input("Enter borrower ID: ")
    current_book = find_book(book_id)
    current_borrower = find_borrower(borrower_id)
    if current_book is None:
        print("Book not found.")
    elif current_borrower is None:
        print("Borrower not found.")
    else:
        transaction = find_transaction(book_id, borrower_id)
        if transaction is None:
            print("Book was not borrowed by this borrower.")
        else:
            transactions_list.remove(transaction)
            current_book["status"] = "available"
            print("Book returned successfully.")

def generate_reports():
    print("\n----------------------------------------")
    print("-----------Generate Reports-------------")
    print("----------------------------------------")
    print("-   1. All Books                       -")
    print("-   2. Borrowed Books                  -")
    print("-   3. Available Books                 -")
    print("-   4. Borrower Transaction History    -")
    print("----------------------------------------")
    option = input("Enter option: ")
    if option == "1":
        print("\nAll Books:")
        if len(books_list) == 0:
            print("No books available.")
        else:
            for book in books_list:
                print(f"Title: {book['title']}, Author: {book['author']}, ID: {book['book_id']}")
    elif option == "2":
        print("\nBorrowed Books:")
        borrowed_books = get_borrowed_books()
        if len(borrowed_books) == 0:
            print("No books borrowed.")
        else:
            for book in borrowed_books:
                borrower = find_borrower(book["borrower_id"])
                print(f"Title: {book['title']}, Author: {book['author']}, Borrower: {borrower['name']}")
    elif option == "3":
        print("\nAvailable Books:")
        available_books = get_available_books()
        if len(available_books) == 0:
            print("All books are currently borrowed.")
        else:
            for book in available_books:
                print(f"Title: {book['title']}, Author: {book['author']}, ID: {book['book_id']}")
    elif option == "4":
        print("\nBorrower Transaction History:")
        borrower_id = input("Enter borrower ID: ")
        borrower = find_borrower(borrower_id)
        if borrower is None:
            print("Borrower not found.")
        else:
            borrower_transactions = get_borrower_limit(borrower_id)
            if len(borrower_transactions) == 0:
                print("No transaction history found for this borrower.")
            else:
                print(f"Transaction History for Borrower: {borrower['name']}")
                for transaction in borrower_transactions:
                    book = find_book(transaction["book_id"])
                    status = "Borrowed" if transaction["status"] == "borrowed" else "Returned"
                    print(f"Title: {book['title']}, Author: {book['author']}, Status: {status}")
    else:
        print("Invalid option.")

def search_books():
    print("\nSearch Books:")
    keyword = input("Enter keyword to search: ")
    matching_books = []
    for book in books_list:
        if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower():
            matching_books.append(book)
    if len(matching_books) == 0:
        print("No matching books.")
    else:
        print("Matching Books:")
        for book in matching_books:
            print(f"Title: {book['title']}, Author: {book['author']}, ID: {book['book_id']}")

def search_borrowers():
    print("\nSearch Borrowers:")
    keyword = input("Enter Borrower Details: ")
    matching_borrowers = []
    for borrower in borrowers_list:
        if keyword.lower() in borrower["name"].lower() or keyword.lower() in borrower[
            "contact_info"].lower() or keyword.lower() in borrower["borrower_id"].lower():
            matching_borrowers.append(borrower)
    if len(matching_borrowers) == 0:
        print("No borrowers found.")
    else:
        print("Matching Borrowers:")
        for borrower in matching_borrowers:
            print(
                f"Name: {borrower['name']}, Contact Info: {borrower['contact_info']}, Borrower ID: {borrower['borrower_id']}")

def find_book(book_id):
    for book in books_list:
        if book["book_id"] == book_id:
            return book
    return None

def find_borrower(borrower_id):
    for borrower in borrowers_list:
        if borrower["borrower_id"] == borrower_id:
            return borrower
    return None

def find_transaction(book_id, borrower_id):
    for transaction in transactions_list:
        if transaction["book_id"] == book_id and transaction["borrower_id"] == borrower_id:
            return transaction
    return None

def get_borrowed_books():
    borrowed_books = []
    for transaction in transactions_list:
        if transaction["status"] == "borrowed":
            book = find_book(transaction["book_id"])
            if book:
                borrowed_books.append(book)
    return borrowed_books

def get_available_books():
    available_books = []
    for book in books_list:
        if book["status"] == "available":
            available_books.append(book)
    return available_books

def get_borrower_limit(borrower_id):
    borrower_transactions = []
    for transaction in transactions_list:
        if transaction["borrower_id"] == borrower_id:
            borrower_transactions.append(transaction)
    return borrower_transactions

books_list = []
borrowers_list = []
transactions_list = []
borrow_limit = 3
run_forever = True
while run_forever:
    print("\n***************************************")
    print("** COMSATS Library Management System **")
    print("***************************************")
    print("*    1. Add Book                      *")
    print("*    2. Register Borrower             *")
    print("*    3. Borrow Book                   *")
    print("*    4. Return Book                   *")
    print("*    5. Generate Reports              *")
    print("*    6. Search Books                  *")
    print("*    7. Search Borrowers              *")
    print("*    8. Exit                         *")
    print("***************************************")
    user_input = input("\nEnter option: ")

    if user_input == "1":
        add_book()
    elif user_input == "2":
        register_borrower()
    elif user_input == "3":
        borrow_book()
    elif user_input == "4":
        return_book()
    elif user_input == "5":
        generate_reports()
    elif user_input == "6":
        search_books()
    elif user_input == "7":
        search_borrowers()
    elif user_input == "8":
        run_forever = False
    else:
        print("Invalid option.")
