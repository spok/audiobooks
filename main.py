import os
import shutil
import pygame
import datetime

from pprint import pprint

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class MyBase:
    def __init__(self):
        self.db_name = 'audibooks.db'

        self.books_folder = r'h:\Библиотека\Аудиокниги'
        self.temp_path = r'h:\Библиотека\Temp'
        self.list_folder = []
        self.list_folder_book = []
        self.temp_folder = []
        self.list_books = []
        self.list_authors = []

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
                                  (ID INT PRIMARY KEY     NOT NULL,
                                  AUTHOR             TEXT    NOT NULL,
                                  NAME               TEXT    NOT NULL,
                                  NAME_SERIES        TEXT,
                                  NUMBER_SERIES      INTEGER,
                                  PATH               TEXT,
                                  COUNT_FILE         INTEGER,
                                  CURENT_FILE        INTEGER,
                                  TOTAL_DURATION     REAL,
                                  TOTAL_PLAY         REAL,
                                  RATING             INTEGER,
                                  DESCRIPTION        TEXT,
                                  DATE_ADDED         TIMESTAMP); '''

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

    def save_base(self, base: list):
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
            for i, author in enumerate(base):
                create_table_query = '''CREATE TABLE audiobooks
                                      (ID                INT     PRIMARY KEY     NOT NULL,
                                      AUTHOR             TEXT    NOT NULL,
                                      NAME               TEXT    NOT NULL,
                                      NAME_SERIES        TEXT,
                                      NUMBER_SERIES      INTEGER,
                                      PATH               TEXT    NOT NULL,
                                      COUNT_FILE         INTEGER,
                                      CURENT_FILE        INTEGER,
                                      TOTAL_DURATION     REAL,
                                      TOTAL_PLAY         REAL,
                                      RATING             INTEGER,
                                      DESCRIPTION        TEXT,
                                      DATE_ADDED         TIMESTAMP    NOT NULL); '''

                insert_query = """ INSERT INTO audiobooks (ID, AUTHOR, NAME, NAME_SERIES, NUMBER_SERIES, PATH, 
                                    COUNT_FILE, TOTAL_DURATION) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                item_tuple = (i, author['author'],
                              author['name_book'],
                              author['name_series'],
                              author['number_series'],
                              author['path'],
                              author['count_file'],
                              author['total_duration']
                              )
                cursor.execute(insert_query, item_tuple)
                connection.commit()
                print(str(i+1) + " элемент успешно добавлен")

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def create_dir(self, name):
        if not os.path.isdir(name):
             os.mkdir(name)

    def scan_dir(self, path: str) -> list:
        for dirpath, dirnames, filenames in os.walk(path):
            break
        list2 = []
        for folder in dirnames:
            path2 = os.path.join(path, folder)
            list2 = list2 + (os.listdir(path=path2))
        return list2

    def scan_all_dir(self, path):
        list2 = []
        for dirpath, dirnames, filenames in os.walk(path):
            for folder in dirnames:
                list2.append(folder)
        return list2

    def scan_temp(self, path):
        os.chdir(path)
        list_dir = os.listdir()
        return list_dir

    def copy_temp_dir(self, path: str):
        # поиск каталога с соответствующей бувой
        for dirpath, dirnames, filenames in os.walk(self.books_folder):
            break
        temp_folder = self.scan_temp(path)
        for temp in temp_folder:
            copy_path = ''
            book = self.parse_dir_name(temp)
            if len(book['author']) > 0:
                # первая буква автора
                first_letter = book['author'][0].upper()
                find_first = ''
                # поиск каталога по первой букве
                for dname in dirnames:
                    if first_letter == dname:
                        find_first = dname
                # если такого каталога нет, то создается каталог с первой буквой
                if find_first == '':
                    copy_path = os.path.join(self.books_folder, first_letter)
                    self.create_dir(copy_path)
                else:
                    copy_path = os.path.join(self.books_folder, find_first)

                # поиск внутри каталога первой буквы каталога совпадающего с именем автора
                for dirp, dirn, filen in os.walk(copy_path):
                    break
                # поиск среди каталогов авторов
                find_dir = ''
                for dname in dirn:
                    if dname.lower() == book['author'].lower():
                        find_dir = book['author']
                # если не найден каталог автора создать новый
                if find_dir == '':
                    copy_path = os.path.join(copy_path, book['author'])
                    self.create_dir(copy_path)
                else:
                    copy_path = os.path.join(copy_path, find_dir)

                # поиск в каталоге автора на наличие серии книг
                if book['number'] > 0:
                    for dirp, dirn, filen in os.walk(copy_path):
                        break
                    # поиск среди каталогов авторов
                    find_dir = ''
                    series = book['author'].lower() + '_' + book['series'].lower()
                    for dname in dirn:
                        if dname.lower() == series:
                            find_dir = dname
                    # если не найден каталог серии создать новый
                    if find_dir == '':
                        copy_path = os.path.join(copy_path, book['author']) + '_' + book['series']
                        self.create_dir(copy_path)
                    else:
                        copy_path = os.path.join(copy_path, find_dir)

                # пермещение каталога из временной папки в библиотеку
                dir_from = os.path.join(self.temp_path, temp)
                shutil.move(dir_from, copy_path)
                print('Скопированы папки: ' + dir_from + ' -> ' + copy_path)


if __name__ == '__main__':
    lib = MyBase()
    # mode = input('Введите режим работы (scan, copy, find): ')
    # if mode == 'scan':
    #     # сканирование каталогов и создание списков
    #     list_folder = lib.scan_dir(lib.books_folder)
    # elif mode == 'copy':
    #     # копирование каталогов из временной папки
    #     lib.copy_temp_dir(lib.temp_path)
    # elif mode == 'find':
    #     # Поиск по ключевому слову аудикниг в библиотеке
    #     list_folder = lib.scan_all(lib.books_folder)
    #     while True:
    #         finding = input('Введите ключевое слово для поиска: ').lower()
    #         for folder in list_folder:
    #             fold = folder.lower()
    #             if fold.find(finding) >= 0:
    #                 print(folder)
    # else:
    #     pass
    lib.scan_dir_book(lib.books_folder)
    lib.save_base(lib.list_books)







