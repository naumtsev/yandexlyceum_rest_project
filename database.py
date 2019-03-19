import sqlite3
import os.path


class DB:
    def __init__(self):
        conn = sqlite3.connect('db.db', check_same_thread=False)
        self.connection = conn

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.close()


class BookModel:
    def __init__(self, data_base):
        self.connection = data_base.get_connection()
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             book_title VARCHAR(50),
                             author VARCHAR(128),
                             content LONG ТЕХТ
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, book_title, author, content):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books 
                          (book_title, author, content) 
                          VALUES (?, ?, ?)''', (book_title, author, content))
        cursor.close()
        self.connection.commit()

    def get(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (str(book_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        return rows

    def delete(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM books WHERE id = ?''', (str(book_id),))
        cursor.close()
        self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM books')
        cursor.close()
        self.connection.commit()

    def __str__(self):
        data = []
        for i in self.get_all():
            data.append((i[0], i[1]))
        return str()

class UserModel:
    def __init__(self, data_base):
        self.connection = data_base.get_connection()
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             username VARCHAR(50),
                             password VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (username, password) 
                          VALUES (?, ?)''', (username, password,))
        cursor.close()
        self.connection.commit()

    def get(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (str(username),))
        row = cursor.fetchone()
        return row


    def exist(self, username):
        wp = self.get(username)
        if(wp):
            return wp
        else:
            return False

    def __str__(self):
        data = []
        for i in self.get_all():
            data.append((i[0], i[1]))
        return str()


my_db = DB()

BOOKS = BookModel(my_db)
USERS = UserModel(my_db)
