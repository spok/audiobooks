import soundfile as sf
import pyaudio
import wave
from yandex_recognize import Recognize


class GetCommand:
    def __init__(self):
        self.filename = "recorded.wav"
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.record_seconds = 5
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk)

    def get_recognize_command(self) -> str:
        print('Начало записи')
        frames = []
        for i in range(int(44100 / self.chunk * self.record_seconds)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # запись в формате wav
        wf = wave.open(self.filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        # конвертация в формат ogg
        data, samplerate = sf.read(self.filename)
        sf.write('recorded.ogg', data, samplerate)
        # распознование записи
        print('Распознование речи')
        rec = Recognize()
        return rec.get_recognize()


# тестирование работы модуля
if __name__ == "__main__":
    g = GetCommand()
    answer = g.get_recognize_command()
    print(answer)
