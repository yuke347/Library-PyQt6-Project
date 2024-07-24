from sql_queries import *
import datetime
import time
altn = "\n \n \n \n"
#funkcie pre connection
def create_tables(tbls:list):
    with connection:
        with connection.cursor() as cursor:
            for tbl in tbls:
                cursor.execute(tbl)
def insert_users_f(username,first_name,surname,password,DOB):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(insert_users_Q,(username,first_name,surname,password,DOB))

def truncate_t():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(delete_content)

def login_f(name:str,password:str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(check_login,(name,password))
            return cursor.fetchone()

def list_books_f():
    with connection:
        with connection.cursor() as cursor: 
            cursor.execute(return_movies_selection)
            return cursor.fetchall() 
        
# def insert_book_f(Name,Author,Published,Genre):
#     try:
#         cur = connection.cursor()
#         cur.execute(insert_book_Q,(Name,Author,Published,Genre))
#         connection.commit()
#         cur.close()        
#         # connection.close()        

#     except psycopg2.errors.UniqueViolation:
#         cur.execute("ROLLBACK")
#         cursor = connection.cursor()
#         cursor.execute(update_amount_Q,(Name,))
#         connection.commit()
#         cursor.close()
#         # connection.close()  
def insert_existing_book_f(id):
    with connection:
        with connection.cursor() as cursor: 
            cursor.execute("select amount from books where id = %s",(id,))
            if cursor.fetchone() != None:
                cursor.execute(update_amount_return_Q,(id,))
                print(altn)
                print("---------------------------------------------")
                print("Book was added!")
            else:
                print(altn)
                print("---------------------------------------------")
                print("Probably wrong ID!")


def remove_book_f(id):
    with connection:
        with connection.cursor() as cursor: 
            cursor.execute(remove_book_Q,(id,id))
            return cursor.fetchone()


def returnBookID_f(username_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(returnBooksID,(username_id,))
            return cursor.fetchall()
        
def returnReturnedBooks_f(username_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(returnReturnedBooks_Q,(username_id,))
            return cursor.fetchall()
