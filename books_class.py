import datetime
import os
from tinytag import TinyTag

class MyBook:
    def __init__(self):
        self.name = ''
        self.author = ''
        self.name_cycle = ''
        self.number_cycle = 0
        self.path = ''
        self.count_file = 0
        self.current_file = 0
        self.total_duration = 0.0
        self.total_play = 0.0
        self.percent_play = 0.0
        self.rating = 0
        self.description = ''
        self.date_added = 0.0

    def get_abs_path(self, path: str) -> str:
        return os.path.join(path, self.path)

    def get_percent(self) -> float:
        self.percent_play = self.total_play/self.total_duration * 100
        return self.percent_play

    def get_duration_file(self, path: str) -> float:
        """Определение длительности аудифайла"""
        try:
            tag = TinyTag.get(path)
            total = tag.duration
        except:
            total = 0
            print('Ошибка чтения - ', path)
        return tag.duration