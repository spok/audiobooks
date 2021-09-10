import datetime
from base_class import MyBase

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

    # lib.delete_table()
    # lib.create_table()
    #
    # lib.update_base()

    # lib.upgrade_base()
    # lib.select_by_date(2)

    lib.select_by_name('ангел')






