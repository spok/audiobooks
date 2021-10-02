import pygame
from threading import Thread
import time

class AudioThread(Thread):
    def __init__(self, name, place=0.0):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.cur_position = place
        self.initmixer()

    def initmixer(self):
        pygame.mixer.init()
        buffer = 3072  # audio buffer size, number of samples since pygame 1.8.
        freq, size, chan = pygame.mixer.get_init()
        pygame.mixer.init(freq, size, chan, buffer)

    def playmusic(self):
        pygame.init()
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.name)
            pygame.mixer.music.play(loops=0, start=self.cur_position)
            old_position = self.cur_position
            while pygame.mixer.music.get_busy():
                self.cur_position = pygame.mixer.music.get_pos() / 1000 + old_position
        except FileNotFoundError:
            print('Не найден аудиофайл')

    def run(self):
        """Запуск воспроизведения"""
        msg = "%s is running\n" % self.name
        print(msg)
        self.playmusic()

    def stop(self):
        """Остановка воспроизведения"""
        pygame.mixer.music.stop()

# тестирование работы модуля
# if __name__ == "__main__":
#     b = AudioThread(name='00.mp3', place=100.0)
#     b.start()
#     print('Start')
#     time.sleep(20)
#     b.stop()
#     print(f'Stop play {b.cur_position}')
#     b.join()
#     print('Stop thread')
