import os
import shutil
from pprint import pprint
from books_class import MyBook
import json

class MyLibrary:
    def __init__(self):
        self.books_folder = r'h:\Библиотека\Аудиокниги'
        self.temp_path = r'h:\Библиотека\Temp'
        self.list_folder = []
        self.list_folder_book = []
        self.temp_folder = []
        self.list_books = []

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

    def scan_struct(self, path: str) -> dict:
        # Чтение каталога и проверка на наличие подпапок и отдельных файлов mp3
        answer = {}
        for dirpath, dirnames, filenames in os.walk(path):
            break
        if len(dirnames) > 0:
            answer['folders'] = dirnames
            dir_path = []
            for dir in dirnames:
                dir_path.append(os.path.join(path, dir))
            answer['folders_path'] = dir_path
        if len(filenames) > 0:
            # Учитываем только mp3 файлы
            audio_file = []
            file_path = []
            for file in filenames:
                if file.find('*.mp3') > 0:
                    audio_file.append(file)
                    file_path.append(os.path.join(path, file))
            answer['files'] = audio_file
            answer['files_path'] = file_path
        return answer

    def scan_dir_book(self, path: str):
        self.list_folder_book = []
        list_litera = os.listdir(path)
        # Перебор по каталогам букв
        path_author = []
        for dir in list_litera:
            litera_path = os.path.join(self.books_folder, dir)
            all_authors = self.scan_struct(litera_path)
            for i, author in enumerate(all_authors['folders']):
                buf = {}
                buf['author'] = author
                buf['path'] = all_authors['folders_path'][i]
                path_author.append(buf)
        # Перебор по списку авторов
        for author in path_author:
            struct_author = self.scan_struct(author['path'])
            if struct_author.get('folders'):
                # Запись полученных книг
                for k, dir in enumerate(struct_author['folders']):
                    # Проверка на наличие серий у автора
                    series_struct = self.scan_struct(struct_author['folders_path'][k])
                    # Если в папке есть подкаталоги
                    if series_struct.get('folders'):
                        for j, sub_dir in enumerate(series_struct['folders']):
                            elem = {}
                            elem['author'] = author['author']
                            elem['name_book'] = sub_dir.split('_')[-1]
                            elem['path'] = series_struct['folders_path'][j]
                            self.list_books.append(elem)
                    else:
                        elem = {}
                        elem['author'] = author['author']
                        elem['name_book'] = dir.split('_')[-1]
                        elem['path'] = struct_author['folders_path'][k]
                        self.list_books.append(elem)
            if struct_author.get('files'):
                for i, dir in enumerate(struct_author['files']):
                    elem = {}
                    elem['author'] = author['author']
                    elem['name_book'] = dir.split('_')[-1]
                    elem['path'] = struct_author['files_path'][i]
                    self.list_books.append(elem)

        with open('test.json', 'w') as file:
            json.dump(self.list_books, file)

        with open('test.json') as file:
            self.list_books = json.load(file)


    def scan_temp(self, path):
        os.chdir(path)
        list_dir = os.listdir()
        return list_dir

    def parse_dir_name(self, dir_name: str):
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
    # lib.scan_recursion(lib.books_folder)
    # pprint(lib.list_folder)







