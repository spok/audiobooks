import os
import shutil

books_folder = r"h:\Библиотека\Аудиокниги"
temp_path = r"h:\Библиотека\Temp"
list_folder = []
temp_folder = []

def create_dir(name):
    if not os.path.isdir(name):
         os.mkdir(name)

def scan_dir(path):
    for dirpath, dirnames, filenames in os.walk(path):
        break
    list2 = []
    for folder in dirnames:
        path2 = path + '\\' + folder
        list2 = list2 + (os.listdir(path=path2))
    return list2

def scan_all(path):
    list2 = []
    for dirpath, dirnames, filenames in os.walk(path):
        for folder in dirnames:
            list2.append(folder)
    return list2

def scan_temp(path):
    os.chdir(path)
    list_dir = os.listdir()
    return list_dir

def parse_dir_name(dir_name: str):
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

def copy_temp_dir(path):
    # поиск каталога с соответствующей бувой
    for dirpath, dirnames, filenames in os.walk(books_folder):
        break
    temp_folder = scan_temp(path)
    for temp in temp_folder:
        copy_path = ''
        book = parse_dir_name(temp)
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
                copy_path = books_folder + "\\" + first_letter
                create_dir(copy_path)
            else:
                copy_path = books_folder + "\\" + find_first

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
                copy_path = copy_path + "\\" + book['author']
                create_dir(copy_path)
            else:
                copy_path = copy_path + "\\" + find_dir

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
                    copy_path = copy_path + "\\" + book['author'] + '_' + book['series']
                    create_dir(copy_path)
                else:
                    copy_path = copy_path + "\\" + find_dir

            # пермещение каталога из временной папки в библиотеку
            dir_from = temp_path + '\\' + temp
            shutil.move(dir_from, copy_path)
            print('Скопированы папки: ' + dir_from + ' -> ' + copy_path)


if __name__ == '__main__':
    mode = input('Введите режим работы (scan, copy, find): ')
    if mode == 'scan':
        # сканирование каталогов и создание списков
        list_folder = scan_dir(books_folder)
    elif mode == 'copy':
        # копирование каталогов из временной папки
        copy_temp_dir(temp_path)
    elif mode == 'find':
        # Поиск по ключевому слову аудикниг в библиотеке
        list_folder = scan_all(books_folder)
        while True:
            finding = input('Введите ключевое слово для поиска: ').lower()
            for folder in list_folder:
                fold = folder.lower()
                if fold.find(finding) >= 0:
                    print(folder)
    else:
        pass






