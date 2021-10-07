import json
import queue
import sounddevice as sd
import vosk
from config import BOT_CONFIG
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC

X_texts = []
y = []
# подготовка датасета
for intent, intent_date in BOT_CONFIG['intents'].items():
    for example in intent_date['examples']:
        X_texts.append(example)
        y.append(intent)
# векторизация датасета
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_texts)
# обучение
clf = LinearSVC().fit(X, y)

q = queue.Queue()
devices = sd.query_devices()
print(devices)
dev_id = 2
samplerate = int(sd.query_devices(dev_id, 'input')['default_samplerate'])
model = vosk.Model("model")
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=dev_id, dtype='int16', channels=1,
                       callback=(lambda i, f, t, s: q.put(bytes(i)))):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())["text"]
            print("Распознано: " + data)
            if len(data) > 0:
                key = ''
                answer = clf.predict(vectorizer.transform([data]))
                # разделение фразы на команды и параметра команды
                fraza_list = data.split()
                if answer == 'find_author_letter':
                    if len(fraza_list[-1]) == 1:
                        key = fraza_list[-1]
                if answer == 'find_author':
                    key = fraza_list[-1]
                if answer == 'find_books':
                    key = fraza_list[-1]

                print(f'Ответ: {answer} {key}')
        else:
            data = json.loads(rec.PartialResult())["partial"]
            if data != "":
                pass
