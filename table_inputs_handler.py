from sql_exe import login_f,insert_book_f,insert_users_f,remove_book_f,borrow_book_f,return_book_f,insert_existing_book_f

import sys
sys.path.append(r"C:\\Users\\User\\OneDrive\\Dokumenty\\programovanie\\python\\learning\\python-postgresql\\app3\\")
sys.path.append(r"C:\Users\Dusan\OneDrive\Dokumenty\programovanie\python\learning\python-postgresql\app3")
# from helper import valid_date # type: ignore

#modul, ktorý handluje login
def login_I():
    username = input("Username: ") 
    password = input("Password: ")
    return login_f(username,password)

# def signin_I():
#     username = input("Username: ") 
#     first_name = input("First name: ").title()
#     surname = input("Surname: ").title()
#     password = input("Password: ")
#     DOB = valid_date()
#     insert_users_f( username,first_name,surname,password,DOB)

def insert_book_I():
    name = input("Book name: ") 
    author = input("Author name: ").title()
    # published = valid_date()
    genre = input("Genre: ")  
    insert_book_f(name,author,published,genre) 
def insert_existing_book_I():
    id = input("Book ID: ")
    insert_existing_book_f(id)

def remove_book_I():
    id = input("Book ID to be removed: ")
    remove_book_f(id)

def borrow_book_I(username_id):
    book_id = input("Book ID to be borrowed: ")
    borrow_book_f(username_id,book_id)

def return_book_I(username_id):
    book_id = input("Book ID to be returned: ")
    return_book_f(book_id,username_id)




