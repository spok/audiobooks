import requests
import wave
import pygame


class SpeechGenerator:
    def __init__(self):
        self.key = 'AQVNzLJrizP3pU9S1bFmk4K4HktOVRRSnh5ISmsL'
        self.folder_id = 'b1gvf14g88gtdrsuh1hm'
        self.url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        self.headers = {
                        'Authorization': 'Api-Key {}'.format(self.key),
                        }
        self.text = ''

    def get_audio_file(self, text):
        a = b''
        for audio_content in self.synthesize(text):
            a = a + audio_content
        data = a
        with wave.open("answer.wav", "wb") as out_f:
            out_f.setnchannels(1)
            out_f.setsampwidth(2)
            out_f.setframerate(44100)
            out_f.writeframesraw(data)
        pygame.mixer.init()
        pygame.mixer.music.load("answer.wav")
        pygame.mixer.music.play()

    def synthesize(self, text):
        data = {
            'text': text,
            'lang': 'ru-RU',
            'folderId': self.folder_id,
            'format': 'lpcm',
            'sampleRateHertz': 48000,
        }

        with requests.post(self.url, headers=self.headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk


# тестирование класса
if __name__ == "__main__":
    b = SpeechGenerator()
    b.get_audio_file('Привет')
