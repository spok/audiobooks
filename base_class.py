import psycopg2
import datetime
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from library_class import MyLibrary

class MyBase:
    def __init__(self):
        self.db_name = 'audibooks.db'
        self.library = MyLibrary()
        self.find_element = []
        self.find_author = []

    def create_base(self):
        try:
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            sql_create_database = 'create database postgres_db'
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def create_table(self):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            # Создайте курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # SQL-запрос для создания новой таблицы
            create_table_query = '''CREATE TABLE audiobooks
                                  (ID                SERIAL     PRIMARY KEY,
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
                                  date_added         TIMESTAMP); '''

            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            connection.commit()
            print("Таблица успешно создана в PostgreSQL")

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def delete_table(self):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            # Создайте курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # SQL-запрос для создания новой таблицы
            delete_table_query = '''DROP TABLE audiobooks'''

            # Выполнение команды: это создает новую таблицу
            cursor.execute(delete_table_query)
            connection.commit()
            print("Таблица успешно удалена в PostgreSQL")

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def save_base(self, books_list: list):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных
            for book in books_list:
                # проверка на наличие записи в базе
                insert_query = """SELECT * FROM audiobooks WHERE author=%s and name_book=%s"""

                item_tuple = (book.author, book.name, )
                cursor.execute(insert_query, item_tuple)
                record = cursor.fetchall()
                if len(record) == 0:
                    # Добавление записи
                    insert_query = """ INSERT INTO audiobooks (author, name_book, name_cycle, number_cycle, path, 
                                        count_file, total_duration, date_added) VALUES 
                                        (%s, %s, %s, %s, %s, %s, %s, %s)"""
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
                    connection.commit()
                    print("Книга успешно добавлена")

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def select_by_date(self, day: int):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = """SELECT * FROM audiobooks WHERE date_added>%s and date_added<%s"""
            cur_time = datetime.datetime.now()
            delta_time = datetime.timedelta(days=day)
            item_tuple = (cur_time-delta_time, cur_time, )
            cursor.execute(insert_query, item_tuple)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                print(i)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def select_by_litera(self, litera: str):
        self.find_element = []
        self.find_author = []
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = """SELECT * FROM audiobooks WHERE LOWER(author) LIKE '{}%'""".format(litera.lower())
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                self.find_element.append(i)
                if i[1] not in self.find_author:
                    self.find_author.append(i[1])
                print(i)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def select_by_author(self, litera: str):
        self.find_element = []
        self.find_author = []
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = """SELECT * FROM audiobooks WHERE LOWER(author) LIKE '%{n}%'""".format(n=litera.lower())
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                if i[1] not in self.find_author:
                    self.find_author.append(i[1])
                print(i)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def select_by_name(self, litera: str):
        self.find_element = []
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="krevedko78",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres_db")

            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных
            # проверка на наличие записи в базе
            insert_query = """SELECT * FROM audiobooks WHERE LOWER(name_book) LIKE '%{n}%'""".format(n=litera.lower())
            cursor.execute(insert_query)
            record = cursor.fetchall()
            for i in record:
                # Отображение результата запроса
                self.find_element.append(i)
                print(i)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def update_base(self):
        self.library.scan_dir_book(self.library.books_path)
        self.save_base(books_list=self.library.list_books)

    def upgrade_base(self):
        self.library.copy_temp_dir()
        self.save_base(books_list=self.library.join_books)
