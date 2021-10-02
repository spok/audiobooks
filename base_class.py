import sqlite3
import datetime
from library_class import MyLibrary


class MyBase:
    def __init__(self):
        self.db_name = 'audibooks.db'
        self.library = MyLibrary()
        self.find_element = []
        self.find_author = set()

    def create_base_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # создание основной таблицы с книгами
            create_table_query = """CREATE TABLE IF NOT EXISTS books
                                  (ID                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  author             TEXT    NOT NULL,
                                  name_book               TEXT    NOT NULL,
                                  name_cycle        TEXT,
                                  number_cycle      INTEGER,
                                  path               TEXT,
                                  count_file         INTEGER,
                                  current_file        INTEGER,
                                  total_duration     REAL,
                                  total_play         REAL,
                                  rating             INTEGER,
                                  description        TEXT,
                                  date_added         REAL);"""
            cursor.execute(create_table_query)
            conn.commit()
            # создание таблицы с новыми книгами, связь таблиц по ID
            create_table_query = """CREATE TABLE IF NOT EXISTS new_books
                                  (ID                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  base_ID             INTEGER    NOT NULL,
                                  author             TEXT    NOT NULL,
                                  name_book               TEXT    NOT NULL);"""
            cursor.execute(create_table_query)
            conn.commit()
            # создание таблицы с последними прочитанными книгами, связь таблиц по ID
            create_table_query = """CREATE TABLE IF NOT EXISTS play_books
                                  (ID                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  base_ID             INTEGER    NOT NULL,
                                  author             TEXT    NOT NULL,
                                  name_book               TEXT    NOT NULL);"""
            cursor.execute(create_table_query)
            conn.commit()
        except Exception as error:
            print("Ошибка при работе с базой данной", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def delete_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            delete_table_query = """DROP TABLE IF EXISTS books;"""
            cursor.execute(delete_table_query)
            conn.commit()
            delete_table_query = """DROP TABLE IF EXISTS new_books;"""
            cursor.execute(delete_table_query)
            conn.commit()
            delete_table_query = """DROP TABLE IF EXISTS play_books;"""
            cursor.execute(delete_table_query)
            conn.commit()
            print("Таблицы успешно удалены")

        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def save_base(self, books_list: list, mode='update'):
        try:
            # Подключиться к существующей базе данных
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            if mode == 'add':
                cursor2 = conn.cursor()

            # Выполнение SQL-запроса для вставки данных
            for book in books_list:
                # проверка на наличие записи в базе
                insert_query = """SELECT * FROM books WHERE author=? and name_book=?"""
                item_tuple = (book.author, book.name,)
                cursor.execute(insert_query, item_tuple)
                record = cursor.fetchall()
                if len(record) == 0:
                    # Добавление записи
                    insert_query = """INSERT INTO books(author, name_book, name_cycle, number_cycle, path, count_file, 
                    total_duration, date_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    item_tuple = (book.author,
                                   book.name,
                                   book.name_cycle,
                                   book.number_cycle,
                                   book.path,
                                   book.count_file,
                                   book.total_duration,
                                   book.date_added,
                                   )
                    cursor.execute(insert_query, item_tuple)
                    curid = cursor.lastrowid
                    if mode == 'add':
                        insert_query = """INSERT INTO new_books(base_ID, author, name_book) VALUES (?, ?, ?)"""
                        item_tuple = (curid, book.author, book.name,)
                        cursor2.execute(insert_query, item_tuple)
            conn.commit()

        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def select_by_date(self, day: int):
        try:
            # Подключиться к существующей базе данных
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = """SELECT * FROM books WHERE date_added>? AND date_added<?"""
            cur_time = datetime.datetime.now()
            delta_time = datetime.timedelta(days=day)
            item_tuple = (datetime.datetime.timestamp(cur_time - delta_time), datetime.datetime.timestamp(cur_time),)
            cursor.execute(insert_query, item_tuple)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                print(i)
        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def select_by_litera(self, litera: str):
        self.find_element = []
        self.find_author = set()
        try:
            # Подключиться к существующей базе данных
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = f"""SELECT * FROM books WHERE ((author LIKE '{litera}%') OR 
                            (author LIKE'{litera.lower()}%'))"""
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                self.find_element.append(i)
                if i[1] not in self.find_author:
                    self.find_author.add(i[1])
            print(self.find_author)

        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def select_by_author(self, litera: str):
        self.find_element = []
        self.find_author = set()
        try:
            # Подключиться к существующей базе данных
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = f"""SELECT * FROM books WHERE ((author LIKE '%{litera}%') OR 
                            (author LIKE'%{litera.capitalize()}%'))"""
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                if i[1] not in self.find_author:
                    self.find_author.add(i[1])
            print(self.find_author)
        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def select_by_name(self, litera: str):
        self.find_element = []
        try:
            # Подключиться к существующей базе данных
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = f"""SELECT * FROM books WHERE ((name_book LIKE '%{litera}%') OR 
                            (name_book LIKE'%{litera.capitalize()}%'))"""
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                self.find_element.append(i[2])
            print(self.find_element)
        except Exception as error:
            print("Ошибка при работе с базой данных", error)
        finally:
            conn.close()
            print("Соединение с базой закрыто")

    def update_base(self):
        self.library.scan_dir_book(self.library.books_path)
        self.save_base(books_list=self.library.list_books, mode='update')

    def upgrade_base(self):
        self.library.copy_temp_dir()
        self.save_base(books_list=self.library.join_books, mode='add')


# тестирование работы модуля
# if __name__ == "__main__":
#     b = MyBase()
    # тест создания базы
    # b.create_base_table()
    # b.update_base()
    # b.upgrade_base()
    # b.delete_table()
    # тест запросов из базы по букве
    # b.select_by_litera('А')
    # тест запросов по автору
    # b.select_by_author('азимов')
    # тест запросов по названию книги
    # b.select_by_name('ангел')
    # тест запроса по дате добавления
    # b.select_by_date(30)
