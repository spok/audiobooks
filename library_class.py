import os
import shutil
import pathlib
import datetime
from books_class import MyBook

class MyLibrary:
    def __init__(self):
        self.list_books = []
        self.list_authors = set()
        self.join_books = []

        self.books_path = r'h:\Библиотека\Аудиокниги'
        self.temp_path = r'h:\Библиотека\Temp'

    def parse_number(self, path: str) -> int:
        # обработка строки для нахождения первого вхождения цифр
        number = 0
        x = [int(i) for k, i in enumerate(path.split(' ')) if i.isdigit() and k < 2]
        if len(x) > 1:
            number = x[0]
        else:
            s = ''
            sl = []
            for i in path:
                if not i.isdigit():
                    if len(s) > 0:
                        sl.append(int(s))
                    s = ''
                else:
                    s = s + i
            if len(sl) > 0:
                number = int(sl[0])
        return number

    def parse_dir_name(self, path: str) -> dict:
        book = {}
        if path.find('_') > -1:
            parse = path.split('_')
            # Если книга из серии
            if len(parse) > 3:
                if parse[1].isdigit():
                    book['number'] = int(parse[1])
                else:
                    book['cycle'] = parse[1]
                if parse[-2].isdigit():
                    book['number'] = int(parse[-2])
                book['name'] = parse[-1]
            # если одиночная книга
            else:
                book['name'] = parse[-1]
        else:
            book['number'] = self.parse_number(path)
            book['name'] = path
        return book

    def parse_name_book(self, path: str) -> dict:
        book = {}
        if path.find('_') > -1:
            parse = path.split('_')
            # Если книга из серии
            if len(parse) > 2:
                book['author'] = parse[0]
                book['cycle'] = parse[1]
                if parse[2].isdigit():
                    book['number'] = int(parse[2])
                book['name'] = parse[3]
            # если одиночная книга
            else:
                book['author'] = parse[0]
                book['name'] = parse[1]
        else:
            book['author'] = 'Unknown'
            book['name'] = path
        return book

    def print_books(self):
        for b in self.list_books:
            print(b.author, b.name, b.name_cycle, b.number_cycle, b.count_file, b.total_duration, b.date_added)

    def scan_dir_book(self, library_path: str):
        """Сканирование каталога с аудиокнигами с заполнением списка книг"""
        self.list_books = []
        self.list_authors = set()
        all_folders = []

        for i in os.walk(library_path):
            if len(i[2]) > 0:
                all_folders.append(list(i))
        lit = 'A'
        tot = 0
        for dir in all_folders:
            if len(dir[2]) > 0:
                book = MyBook()
                relative_path = dir[0].replace(library_path, '')
                path = pathlib.PureWindowsPath(relative_path)
                s = ''
                l = len(path.parts)
                for i, k in enumerate(path.parts):
                    if i == 1:
                        if lit != k:
                            print('Обработаны авторы на букву - ', lit, datetime.datetime.now(), str(tot))
                            tot = 0
                            lit = k
                    if i == 2:
                        book.author = k
                        self.list_authors.add(k)
                    elif i == 3:
                        if l > 4:
                            # Если этот каталог с названием серии
                            s = self.parse_dir_name(k)
                            book.name_cycle = s['name']
                        else:
                            s = self.parse_dir_name(k)
                            book.name = s['name']
                    elif i == 4:
                        s = self.parse_dir_name(k)
                        book.name = s['name']
                        if 'number' in s:
                            book.number_cycle = s['number']
                if book.name == '':
                    book.name = ('Отдельные рассказы')

                book.path = relative_path

                # определение общей продолжительности звучания книги и количество mp3 файлов
                book.total_duration = 0.0
                book.count_file = 0
                for audio_file in dir[2]:
                    if audio_file.find('.mp3') > -1:
                        book.total_duration += book.get_duration_file(os.path.join(dir[0], audio_file))
                        book.count_file += 1
                        tot += 1

                # определение времени создания папки
                book.date_added = datetime.datetime.fromtimestamp(os.path.getmtime(dir[0]))
                self.list_books.append(book)

    def create_dir(self, name) -> bool:
        """проверка на существование и создание каталога"""
        if not os.path.isdir(name):
            os.mkdir(name)
            return True
        else:
            return False

    def scan_temp(self, path) -> list:
        list_dir = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
        return list_dir

    def copy_temp_dir(self):
        """Копирование аудиокниг из временного каталога в основной"""
        # поиск каталога с соответствующей бувой
        self.join_books = []
        litera_list = self.scan_temp(self.books_path)
        temp_list = self.scan_temp(self.temp_path)
        books_list = []
        for temp in temp_list:
            copy_path = ''
            book_property = self.parse_name_book(temp)
            if len(book_property['author']) > 0:
                # первая буква автора
                first_letter = book_property['author'][0].upper()
                find_first = ''
                # поиск каталога по первой букве
                for dname in litera_list:
                    if first_letter == dname:
                        find_first = dname
                # если такого каталога нет, то создается каталог с первой буквой
                if find_first == '':
                    copy_path = os.path.join(self.books_path, first_letter)
                    self.create_dir(copy_path)
                else:
                    copy_path = os.path.join(self.books_path, find_first)

                # поиск внутри каталога первой буквы каталога совпадающего с именем автора
                dirn = self.scan_temp(copy_path)
                # поиск среди каталогов авторов
                find_dir = ''
                for dname in dirn:
                    if dname.lower() == book_property['author'].lower():
                        find_dir = book_property['author']

                # если не найден каталог автора создать новый
                if find_dir == '':
                    copy_path = os.path.join(copy_path, book_property['author'])
                    self.create_dir(copy_path)
                else:
                    copy_path = os.path.join(copy_path, find_dir)

                # поиск в каталоге автора на наличие серии книг
                if 'number' in book_property:
                    dirn = self.scan_temp(copy_path)
                    # поиск среди каталогов авторов
                    find_dir = ''
                    serie_name = book_property['author'].lower() + '_' + book_property['cycle'].lower()
                    for dname in dirn:
                        if dname.lower() == serie_name:
                            find_dir = dname
                    # если не найден каталог серии создать новый
                    if find_dir == '':
                        copy_path = os.path.join(copy_path, book_property['author']) + '_' + book_property['cycle']
                        self.create_dir(copy_path)
                    else:
                        copy_path = os.path.join(copy_path, find_dir)

                # пермещение каталога из временной папки в библиотеку
                dir_from = os.path.join(self.temp_path, temp)
                to_path = os.path.join(copy_path, temp)
                if not os.path.isdir(to_path):
                    shutil.move(dir_from, copy_path)
                else:
                    print("Каталог существует -> ", to_path)
                    next
                print('Скопированы папки: ' + dir_from + ' -> ' + copy_path)

                # Создание класса книги
                book = MyBook()
                book.author = book_property['author']
                book.name = book_property['name']
                if 'cycle' in book_property:
                    book.name_cycle = book_property['cycle']
                else:
                    book.name_cycle = ''
                if 'number' in book_property:
                    book.number_cycle = book_property['number']
                else:
                    book.number_cycle = 0
                book.path = to_path.replace(self.books_path, '')
                book.date_added = datetime.datetime.fromtimestamp(os.path.getmtime(to_path))

                # определение общей продолжительности звучания книги и количество mp3 файлов
                book.total_duration = 0.0
                book.count_file = 0
                for dir in os.walk(to_path):
                    break
                for audio_file in dir[2]:
                    if audio_file.find('.mp3') > -1:
                        book.total_duration += book.get_duration_file(os.path.join(to_path, audio_file))
                        book.count_file += 1

                self.join_books.append(book)
