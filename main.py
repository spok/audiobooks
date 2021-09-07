import os
import shutil
import pygame
import datetime
from mutagen.mp3 import MP3
from pprint import pprint
from books_class import MyBook
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class MyLibrary:
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

    def parse_dir_name(self, dir_name: str) -> dict:
        book = {
            'author': '',
            'series': '',
            'number': 0,
            'name': ''
        }
        parse = dir_name.split('_')
        # Если книга из серии
        if len(parse)>2:
            book['author'] = parse[0]
            book['series'] = parse[1]
            book['number'] = int(parse[2])
            book['name'] = parse[3]
        # если одиночная книга
        else:
            book['author'] = parse[0]
            book['name'] = parse[1]
        return book

    def get_duration_file(self, path: str) -> float:
        """Определение длительности аудифайла"""
        audio = MP3(path)
        return audio.info.length

    def scan_struct(self, path: str) -> dict:
        """Чтение каталога и проверка на наличие подпапок и отдельных файлов mp3
        возвращает словарь содержащий списки с названиями папок и путей"""
        answer = {}
        for dirpath, dirnames, filenames in os.walk(path):
            break
        if len(dirnames) > 0:
            answer['folders'] = dirnames
            dir_path = []
            dir_time = []
            for dir in dirnames:
                buf_path = os.path.join(path, dir)
                dir_path.append(buf_path)
                dir_time.append(datetime.datetime.fromtimestamp(os.path.getmtime(buf_path)))
            answer['folders_path'] = dir_path
            answer['time'] = dir_time
        if len(filenames) > 0:
            # Учитываем только mp3 файлы
            audio_file = []
            file_path = []
            file_time = []
            duration_audio = []
            for file in filenames:
                if file.find('*.mp3') > 0:
                    buf_path = os.path.join(path, file)
                    audio_file.append(file)
                    duration_audio.append(self.get_duration_file(buf_path))
                    file_path.append(buf_path)
                    file_time.append(datetime.datetime.fromtimestamp(os.path.getmtime(buf_path)))
            answer['files'] = audio_file
            answer['files_path'] = file_path
            answer['files_duration'] = duration_audio
            answer['files_time'] = file_time
        return answer

    def scan_dir_book(self, path: str):
        """Сканирование каталога с аудиокнигами с заполнением списка книг"""
        self.list_books = []
        self.list_authors = []
        list_litera = os.listdir(path)

        # Перебор по каталогам букв
        for dir in list_litera:
            litera_path = os.path.join(self.books_folder, dir)
            if os.path.isdir(litera_path):
                all_authors = self.scan_struct(litera_path)
                for i, author in enumerate(all_authors['folders']):
                    # Проверка является ли каталог отдельной аудикнигой автора
                    if author.find('_') > -1:
                        # сканирование содержимого каталога с аудикнигой
                        one_book = self.scan_struct(all_authors['folders_path'][i])

                        # Добавление папки как аудиокниги
                        elem = {}
                        elem['author'] = author.split('_')[0]
                        elem['name_book'] = author.split('_')[-1]
                        elem['path'] = all_authors['folders_path'][i]
                        elem['date_added'] = all_authors['time'][i]
                        elem['count_file'] = len(one_book['files'])
                        elem['total_duration'] = sum(one_book['files_duration'])
                        self.list_books.append(elem)

                        # Добавление записи об авторе
                        buf = {}
                        buf['author'] = author.split('_')[0]
                        buf['path'] = all_authors['folders_path'][i]
                        self.list_authors.append(buf)
                    else:
                        # добавление папки как название автора в список
                        buf = {}
                        buf['author'] = author
                        buf['path'] = all_authors['folders_path'][i]
                        self.list_authors.append(buf)

        # Перебор по списку авторов
        for author in self.list_authors:
            struct_author = self.scan_struct(author['path'])
            if struct_author.get('folders'):
                # Запись полученных книг
                for k, dir in enumerate(struct_author['folders']):
                    # Проверка на наличие серий аудикниг (подпапок у каталогов) в каталоге автора
                    series_struct = self.scan_struct(struct_author['folders_path'][k])
                    # Если в папке есть подкаталоги
                    if series_struct.get('folders'):
                        # определение названия серия по названию папки
                        if dir.find('_') > -1:
                            str_serie = dir.split('_')[-1]
                        else:
                            str_serie = dir
                        for j, sub_dir in enumerate(series_struct['folders']):
                            elem = {}
                            elem['author'] = author['author']
                            if sub_dir.find('_') > -1:
                                elem['name_book'] = sub_dir.split('_')[-1]
                                elem['number_series'] = int(sub_dir.split('_')[-2])
                            elem['name_series'] = str_serie
                            elem['path'] = series_struct['folders_path'][j]
                            elem['date_added'] = series_struct['time'][j]
                            one_book = self.scan_struct(series_struct['folders_path'][j])
                            elem['count_file'] = len(one_book['files'])
                            elem['total_duration'] = sum(one_book['files_duration'])
                            self.list_books.append(elem)
                    else:
                        elem = {}
                        elem['author'] = author['author']
                        # Присвоение названия книги в зависимости от наличия или отсутствия разделителя
                        if dir.find('_') > -1:
                            elem['name_book'] = dir.split('_')[-1]
                        else:
                            elem['name_book'] = dir
                        elem['path'] = struct_author['folders_path'][k]
                        elem['date_added'] = struct_author['time'][k]
                        one_book = self.scan_struct(struct_author['folders_path'][k])
                        elem['count_file'] = len(one_book['files'])
                        elem['total_duration'] = sum(one_book['files_duration'])
                        self.list_books.append(elem)
            if struct_author.get('files'):
                for i, dir in enumerate(struct_author['files']):
                    elem = {}
                    elem['author'] = author['author']
                    if dir.find('_') > -1:
                        elem['name_book'] = dir.split('_')[-1]
                    else:
                        elem['name_book'] = dir
                    elem['path'] = struct_author['files_path'][i]
                    elem['date_added'] = struct_author['file_time'][i]
                    elem['count_file'] = 1
                    elem['total_duration'] = struct_author['files_duration'][i]
                    self.list_books.append(elem)

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
    lib = MyLibrary()
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







