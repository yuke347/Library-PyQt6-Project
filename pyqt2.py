from pyqt import *
from sql_exe import *
from psycopg2 import errors
# from table_inputs_handler import *
#zmena
class returnIsNone(Exception):
    pass

class Login(MainWindow):
    
    def __init__(self):
        super().__init__()
        create_tables(CT)
    def pause(self,time,setL1):
        QTimer.singleShot(time, self.loop.quit)
        self.loop.exec()
        if setL1 == 1:
            self.label1.setText("") 

    def clickLogin(self):
        self.lgn = login_f(self.inputLine1.text(),self.inputLine2.text())
        if self.lgn != None and self.lgn[6] == 1:
            self.adminPage()
        elif self.lgn != None:
            self.login_page()
        else:
            self.label1.setText("Invalid username or password, try again!")
            self.layout.addWidget(self.label1)
            self.setLayout(self.layout)
            
    def logout(self):
        self.lgn = None
        self.main_page()

    def borrowB(self):   
        try:
            self.borrow_book_f(self.lgn[0],int(self.comboBox1.currentItem().text().partition(".")[0]))
        except AttributeError:
            self.label1.setText("Select one of the books!")
        self.pause(1000,1)

    def returnB(self):
        try:
            self.return_book_f(self.comboBox2.currentItem().text().partition("ID:")[2],int(self.comboBox2.currentItem().text().partition(".")[0]),self.lgn[0])
            self.comboBox2.clear()
            if (books := returnBookID_f(self.lgn[0])) != []:

                for book in books:
                    self.comboBox2.addItem(f"{book[0]}. {book[1]}, {book[2]} ID:{book[6]}")
        except AttributeError:
            self.label1.setText("Please select a book to be removed!")
            
    def insertB(self): 
        try:
            self.insert_book_f(self.inputLine1.text(),self.inputLine2.text(),self.inputLine3.text(),self.inputLine4.text())
            
            self.pause(1000,1)
        except psycopg2.errors.InvalidDatetimeFormat:
            self.label1.setText("Wrong date format, try again")
            self.pause(1000,1)
        except psycopg2.errors.UniqueViolation:
            self.label1.setText("Username already in use")
            self.pause(1000,1)

    def removeB(self): 

        try: 
            if remove_book_f(self.comboBox1.currentItem().text().partition(".")[0]) == None:
                raise returnIsNone
            self.label1.setText("Book was removed")
            self.comboBox1.clear() 
            for book in list_books_f():
                self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]}")
            self.pause(1000,1)
        except returnIsNone:
            self.label1.setText("The book is still borrowed, return before deletion from DB!")
            self.pause(1000,1)
        except AttributeError:
            self.label1.setText("No book to be removed!")

    def setB(self):
        try:    
            self.set_book_f(int(self.inputLine1.text()),self.comboBox1.currentItem().text().partition(".")[0])
        except AttributeError:
            self.label1.setText("Please select a book.")
        except ValueError:
            self.label1.setText("Did not select a book or Invalid amount input.")

    def clickSignIn(self):
        try:
            insert_users_f(self.inputLine1.text().strip(),self.inputLine2.text().strip(),self.inputLine3.text().strip(),self.inputLine4.text().strip(),self.inputLine5.text().strip())
            self.label1.setText("Successfull sign in!")
            self.pause(1000,0)
            self.main_page()    
        except psycopg2.errors.InvalidDatetimeFormat:
            self.label1.setText("Wrong date format, try again")
            self.pause(1000,1)
        except psycopg2.errors.UniqueViolation:
            self.label1.setText("Username already in use")
            self.pause(1000,1)
            
    def borrow_book_f(self,username_id,book_id):
        with connection:
            with connection.cursor() as cursor: 
                try:
                    cursor.execute(borrow_book_Q,(username_id,book_id,datetime.date.today()))
                    cursor.execute(update_amount_minus_Q,(book_id,))
                    self.label1.setText("Book borrowed!")

                except psycopg2.errors.CheckViolation:
                    self.label1.setText("Book is not available")
    
    def return_book_f(self,id,book_id,username_id):
        with connection:
            with connection.cursor() as cursor: 
                cursor.execute(f"select * from borrowings where book_id = {book_id} and username_id = {username_id}")
                if cursor.fetchall() != []:
                    cursor.execute(return_book_Q,(id,book_id,username_id))
                    cursor.execute(update_amount_return_Q,(book_id,))  
                    self.label2.setText("Book returned")
                else:
                    self.label1.setText("Book was not returned")

    def insert_book_f(self,book_name,author,published,genre):
        with connection:
            with connection.cursor() as cursor: 
                try:
                    cursor.execute(insert_book_Q,(book_name,author,published,genre))
                    # cursor.execute(update_amount_Q,(book_name,))
    
                    self.label1.setText("Book inserted!")
                except psycopg2.errors.CheckViolation:
                    self.label1.setText("Book was not inserted, wrong input(Date)")
        with connection:    
            with connection.cursor() as cursor:
                try: 
                        cursor.execute("select id from books where name = %s",(book_name,))
                        id = cursor.fetchone()
                        cursor.execute(insert_book_Qarchive,(id,book_name,author,published,genre))
                except psycopg2.errors.UniqueViolation:
                    pass
    def set_book_f(self,amount,id):
        with connection:
            with connection.cursor() as cursor: 
                cursor.execute(set_book_Q,(amount,id))
                self.label1.setText("Amount was set")     
        
app = QApplication([])

window = Login()

window.main_page()
window.show()

app.exec()