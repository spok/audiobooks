import json
import queue
import sounddevice as sd
import vosk
import pygame

class Recognizer:
    def __init__(self):
        self.q = queue.Queue()
        self.devices = sd.query_devices()
        self.dev_id = 1
        self.samplerate = int(sd.query_devices(self.dev_id, 'input')['default_samplerate'])
        self.model = vosk.Model("model")
        self.record_fraze = ''

    def start_recognize(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=self.dev_id, dtype='int16',
                               channels=1, callback=(lambda i, f, t, s: self.q.put(bytes(i)))):
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    self.record_fraze = json.loads(rec.Result())["text"]
                    print("Распознано: " + self.record_fraze)
                    # if len(data) > 0:
                    #     key = ''
                    #     answer = clf.predict(vectorizer.transform([data]))
                    #     # разделение фразы на команды и параметра команды
                    #     fraza_list = data.split()
                    #     if answer == 'find_author_letter':
                    #         if len(fraza_list[-1]) == 1:
                    #             key = fraza_list[-1]
                    #     if answer == 'find_author':
                    #         key = fraza_list[-1]
                    #     if answer == 'find_books':
                    #         key = fraza_list[-1]
                    #
                    #     print(f'Ответ: {answer} {key}')
                # else:
                #     data = json.loads(rec.PartialResult())["partial"]
                #     if data != "":
                #         pass


# тестирвоание модуля
if __name__ == '__main__':
    b = Recognizer()
    b.start_recognize()

