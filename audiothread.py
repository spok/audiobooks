import pygame
from threading import Thread


class AudioThread(Thread):
    def __init__(self, name, place):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.cur_position = place

    def initmixer(self):
        pygame.mixer.init()
        buffer = 3072  # audio buffer size, number of samples since pygame 1.8.
        freq, size, chan = pygame.mixer.get_init()
        pygame.mixer.init(freq, size, chan, buffer)

    def playmusic(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.name)
        pygame.mixer.music.play(loops=0, start=self.cur_position)
        old_position = self.cur_position
        while pygame.mixer.music.get_busy():
            self.cur_position = pygame.mixer.music.get_pos() / 1000 + old_position

    def run(self):
        """Запуск потока"""
        msg = "%s is running\n" % self.name
        print(msg)
        self.initmixer()
        self.playmusic()

    def stop(self):
        """Остановка миксера и воспроизведения"""
        pygame.mixer.music.stop()
