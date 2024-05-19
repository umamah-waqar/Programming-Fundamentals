# this function is used to add a book
def add_book():
    print("\nAdd Book:")
    book_title = input("Enter book title: ")
    book_author = input("Enter author name: ")
    book_id = input("Enter book ID: ")

    # creating a book dictionary, so we can store book related data
    book = {"title": book_title, "author": book_author, "book_id": book_id, "status": "available"}
    # add book to our list
    books_list.append(book)
    print("Book added successfully.")


# register a borrower, so he can borrow/return a book
def register_borrower():
    print("\nRegister Borrower:")
    name = input("Enter borrower name: ")
    contact_info = input("Enter contact information: ")
    borrower_id = input("Enter borrower ID: ")
    # creating a borrower dictionary, so we can store borrower related data
    borrower = {"name": name, "contact_info": contact_info, "borrower_id": borrower_id}
    borrowers_list.append(borrower)
    print("Borrower registered successfully.")


# function used to borrow a book
def borrow_book():
    # check if we have minimum one book
    if len(books_list) == 0:
        print("Please Add Book First")
        add_book()
        return

    # check if there is minimum one borrower in our system
    if len(borrowers_list) == 0:
        print("Please Register Borrower First")
        register_borrower()
        return

    print("\nBorrow Book:")
    book_id = input("Enter book ID: ")
    borrower_id = input("Enter borrower ID: ")

    # get book data based on book id.
    current_book = find_book(book_id)
    # also get borrower data based on borrower id.
    current_borrower = find_borrower(borrower_id)

    if current_book is None:
        print("Book not found.")
    elif current_borrower is None:
        print("Borrower not found.")
    elif current_book["status"] == "borrowed":
        print("Book is already borrowed.")
    else:
        # Check if borrower has reached the borrowing limit
        borrower_transactions = get_borrower_limit(borrower_id)
        if len(borrower_transactions) >= borrow_limit:
            print("Borrower has reached the borrowing limit.")
        else:
            # creating a borrowed transaction and set the book status to borrowed.
            transaction = {"book_id": book_id, "borrower_id": borrower_id, "status": "borrowed"}
            transactions_list.append(transaction)
            current_book["status"] = "borrowed"
            print("Book borrowed successfully.")


# this function is used to return a book
def return_book():
    print("\nReturn Book:")
    book_id = input("Enter book ID: ")
    borrower_id = input("Enter borrower ID: ")

    # get book and borrower detail based in given id.
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
            # remove the book from borrowed transaction list and set book as available.
            transactions_list.remove(transaction)
            current_book["status"] = "available"
            print("Book returned successfully.")


# a report method which consist more menu.
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
            print("No books are currently borrowed.")
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


# search a book by title or author and get all those book based on keyword.
def search_books():
    print("\nSearch Books:")
    keyword = input("Enter keyword to search: ")

    matching_books = []
    for book in books_list:
        if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower():
            matching_books.append(book)

    if len(matching_books) == 0:
        print("No books found matching the keyword.")
    else:
        print("Matching Books:")
        for book in matching_books:
            print(f"Title: {book['title']}, Author: {book['author']}, ID: {book['book_id']}")


# get all borrower detail based on keyword. keyword will be used to search it from name, contact info or id.
def search_borrowers():
    print("\nSearch Borrowers:")
    keyword = input("Enter keyword to search: ")

    matching_borrowers = []
    for borrower in borrowers_list:
        if keyword.lower() in borrower["name"].lower() or keyword.lower() in borrower[
            "contact_info"].lower() or keyword.lower() in borrower["borrower_id"].lower():
            matching_borrowers.append(borrower)

    if len(matching_borrowers) == 0:
        print("No borrowers found matching the keyword.")
    else:
        print("Matching Borrowers:")
        for borrower in matching_borrowers:
            print(
                f"Name: {borrower['name']}, Contact Info: {borrower['contact_info']}, Borrower ID: {borrower['borrower_id']}")


# check if there is book in our system based on its id.
def find_book(book_id):
    for book in books_list:
        if book["book_id"] == book_id:
            return book
    return None


# check if there is borrower in our system based on his id.
def find_borrower(borrower_id):
    for borrower in borrowers_list:
        if borrower["borrower_id"] == borrower_id:
            return borrower
    return None


# check if there is borrowed book based on borrower id. this will return borrowed data
def find_transaction(book_id, borrower_id):
    for transaction in transactions_list:
        if transaction["book_id"] == book_id and transaction["borrower_id"] == borrower_id:
            return transaction
    return None


# get all those book which has borrowed status.
def get_borrowed_books():
    borrowed_books = []
    for transaction in transactions_list:
        if transaction["status"] == "borrowed":
            book = find_book(transaction["book_id"])
            if book:
                borrowed_books.append(book)
    return borrowed_books


# get only those book which has status as available mean user can borrow these book
def get_available_books():
    available_books = []
    for book in books_list:
        if book["status"] == "available":
            available_books.append(book)
    return available_books


# method which is used to get the limit a user can borrow the book
def get_borrower_limit(borrower_id):
    borrower_transactions = []
    for transaction in transactions_list:
        if transaction["borrower_id"] == borrower_id:
            borrower_transactions.append(transaction)
    return borrower_transactions


# this method is used to sort the books alphabetically.
def sort_books():
    sorted_books = sorted(books_list, key=lambda x: x['title'])
    print("\nBooks Sorted Alphabetically by Title:")
    if len(sorted_books) == 0:
        print("No books available.")
    else:
        for book in sorted_books:
            print(f"Title: {book['title']}, Author: {book['author']}, ID: {book['book_id']}")


# this method is used to get most borrowed books
def most_borrowed_books():
    borrowed_counts = {}
    for transaction in transactions_list:
        book_id = transaction['book_id']
        borrowed_counts[book_id] = borrowed_counts.get(book_id, 0) + 1

    sorted_books = sorted(books_list, key=lambda x: borrowed_counts.get(x['book_id'], 0), reverse=True)
    print("\nMost Borrowed Books:")
    if len(sorted_books) == 0:
        print("No books are currently borrowed.")
    else:
        for book in sorted_books:
            borrow_count = borrowed_counts.get(book['book_id'], 0)
            print(f"Title: {book['title']}, Author: {book['author']}, Borrow Count: {borrow_count}")


# variables to store data at runtime
books_list = []
borrowers_list = []
transactions_list = []
borrow_limit = 3

# code starts from here.

run_forever = True
while run_forever:

    # showing menu so user can pick desired
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
    print("*    8. Sort Books by Title           *")
    print("*    9. Most Borrowed Books           *")
    print("*    10. Exit                         *")
    print("***************************************")
    # take input from user
    user_input = input("\nEnter option: ")

    # run code based on user selection
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
        sort_books()
    elif user_input == "9":
        most_borrowed_books()
    elif user_input == "10":
        run_forever = False
        print("Exiting...")
    else:
        print("Invalid option.")
