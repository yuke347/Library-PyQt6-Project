import psycopg2
import socket
#check the name of the PC
pc = socket.gethostname()
print(pc)
# exit()
#based on PC name insert right arguments
if pc == "DESKTOP-B5O3UD4":
    connection = psycopg2.connect(dbname="Library_ass",user="postgres",password="2540",host="localhost",port=5432)
else:
    connection = psycopg2.connect(dbname="test",user="postgres",password="postgres",host="localhost",port=5432)
# if pc == "DESKTOP-B5O3UD4":
#     connection = psycopg2.connect(dbname="Library_ass",user="postgres",password="2540",host="localhost",port=5432)
# else:
# connection = psycopg2.connect(dbname="postgres",user="postgres",password="choddocertaaa3",host="database1.clcqugmg2721.us-east-1.rds.amazonaws.com",port=5432)

#tables creation
CT =["""create table if not exists books(
        ID serial primary key,
        Name text,
        Author text,
        Published date,
        Genre text,
        amount int default 0 check(amount>-1),
        Constraint unique_text Unique (Name))
        """,
    """create table if not exists users(
        ID serial primary key,
        UserName text,
        First_name text,
        Surname text,
        Password text,
        DOB Date,
        admin int default 0,
        Constraint unique_name Unique(UserName)
    )""","""create table if not exists borrowings(
            ID serial primary key,
            username_id int,
            book_id int,
            borrow_date date,
            return_date date)""",
            """create table if not exists booksArchive(
            book_id integer,
            Name text,
            Author text,
            Published date,
        Genre text,Constraint unique_book Unique(Name))"""]
# vloženie hodnot
insert_users_Q = """insert into users(username,first_name,surname,password,dob) values(
                    %s,%s,%s,%s,%s)"""
insert_book_Q = """insert into books(Name,Author,Published,Genre) values
                    (%s,%s,%s,%s)"""
insert_book_Qarchive = """insert into booksArchive(book_id,Name,Author,Published,Genre) values
                    (%s,%s,%s,%s,%s)"""
borrow_book_Q = """insert into borrowings(username_id,book_id,borrow_date)values(
                    %s,%s,%s)"""


update_amount_Q = """update books set amount = amount + 1 where name = %s"""
update_amount_minus_Q = """update books set amount = amount - 1 where id = %s"""
update_amount_return_Q = """update books set amount = amount + 1 where id = %s"""

# return queries
check_login = """select * from users where username = %s and password = %s"""
return_movies_selection = """select * from books"""
returnBooksID = """select * from books
                    inner join borrowings
                    on books.id = borrowings.book_id
                    where borrowings.username_id = %s and borrowings.return_date is NULL"""
returnReturnedBooks_Q = """select * from booksarchive where book_id in (select book_id from borrowings where username_id = 2 and return_date is not NULL)"""


#remove a thing 
delete_content = """truncate table users"""
remove_book_Q = """delete from books b using borrowings bo
where ((b.id = bo.book_id  and bo.return_date is not NULL) or  (SELECT exists (
select 1 from borrowings where book_id = %s ))= false ) and b.id = %s returning b.id"""
return_book_Q = """DELETE FROM borrowings
WHERE ctid IN (
    SELECT ctid
    FROM borrowings
	where book_id = %s and username_id = %s
    ORDER BY id
    LIMIT 1
)"""
return_book_Q = "update borrowings set return_date = current_date where id=%s and book_id = %s and username_id= %s"
set_book_Q = "update books set amount = %s where id = %s"



