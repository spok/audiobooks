import os
import pathlib
import datetime
from books_class import MyBook

class MyLibrary:
    def __init__(self):
        self.list_books = []
        self.list_authors = set()

    def parse_dir_name(self, path: str) -> dict:
        book = {}
        if path.find('_') > -1:
            parse = path.split('_')
            # Если книга из серии
            if len(parse) > 3:
                book['author'] = parse[0]
                if parse[1].isdigit():
                    book['number'] = int(parse[1])
                else:
                    book['cycle'] = parse[1]
                if parse[2].isdigit():
                    book['number'] = int(parse[2])
                book['name'] = parse[3]
            # если одиночная книга
            else:
                book['author'] = parse[0]
                book['name'] = parse[1]
        else:
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
                    book.name = dir[2][0].replace('.mp3', '')

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


path = r'h:\Библиотека\Аудиокниги'
test = MyLibrary()
test.scan_dir_book(path)
test.print_books()

