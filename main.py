from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
from termcolor import colored  # вывод цветных логов (для выделения распознанной речи)
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
import traceback  # вывод traceback без остановки работы программы при отлове исключений
import wave  # создание и чтение аудиофайлов формата wav
import os  # работа с файловой системой
import random
from base_class import MyBase


lib = MyBase()

class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    Примечание: для мультиязычных голосовых ассистентов лучше создать отдельный класс,
    который будет брать перевод из JSON-файла с нужным языком
    """
    name = ""
    sex = ""
    speech_language = "ru-RU"
    recognition_language = "ru-RU"


def setup_assistant_voice():
    """
    Установка голоса по умолчанию (индекс может меняться в зависимости от настроек операционной системы)
    """
    voices = ttsEngine.getProperty("voices")

    assistant.recognition_language = "ru-RU"
    # Microsoft Irina Desktop - Russian
    ttsEngine.setProperty("voice", voices[0].id)

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # запоминание шумов окружения для последующей очистки звука от них
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 0, 0)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech(("Can you check if your microphone is on, please?"))
            traceback.print_exc()
            return

        # использование online-распознавания через Google (высокое качество распознавания)
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()

        except speech_recognition.UnknownValueError:
            pass  # play_voice_assistant_speech("What did you say again?")

        # в случае проблем с доступом в Интернет происходит попытка использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print(colored("Trying to use offline recognition...", "cyan"))
            recognized_data = use_offline_recognition()

        return recognized_data

def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("model"):
            print(colored("Please download the model from:\n"
                          "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.",
                          "red"))
            exit(1)

        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("model")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()
                recognized_data = recognized_data["text"]
    except:
        traceback.print_exc()
        print(colored("Sorry, speech service is unavailable. Try again later", "red"))

    return recognized_data

def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def view_by_litera(*args: tuple):
    litera = "".join(args[0])
    lib.select_by_litera(litera)
    play_voice_assistant_speech("Найдено " + str(len(lib.find_author)) + "авторов на букву: " + litera)
    i = 0
    while i < len(lib.find_author):
        play_voice_assistant_speech(lib.find_author[i])
        if i % 5 == 0 and i > 0:
            play_voice_assistant_speech("Зачитать следующих авторов?")
            v_input = record_and_recognize_audio()
            os.remove("microphone-results.wav")
            print(colored(v_input, "blue"))
            if v_input == 'нет':
                break
        i += 1

def view_by_author(*args: tuple):
    name = "".join(args[0])
    lib.select_by_author(name)
    play_voice_assistant_speech("Найдено " + str(len(lib.find_author)) + "авторов: " + name)
    i = 0
    while i < len(lib.find_author):
        play_voice_assistant_speech(lib.find_author[i])
        if i % 5 == 0 and i > 0:
            play_voice_assistant_speech("Зачитать следующих авторов?")
            v_input = record_and_recognize_audio()
            os.remove("microphone-results.wav")
            print(colored(v_input, "blue"))
            if v_input == 'нет':
                break
        i += 1

def view_by_book(*args: tuple):
    name = "".join(args[0])
    lib.select_by_name(name)
    play_voice_assistant_speech("Найдено " + str(len(lib.find_element)) + "книги")
    i = 0
    while i < len(lib.find_element):
        play_voice_assistant_speech(lib.find_element[i][2])
        if i % 5 == 0 and i > 0:
            play_voice_assistant_speech("Прочитать названия следующих книг?")
            v_input = record_and_recognize_audio()
            os.remove("microphone-results.wav")
            print(colored(v_input, "blue"))
            if v_input == 'нет':
                break
        i += 1

def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды и аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в метод
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass  # print("Command not found")

# перечень команд для использования (качестве ключей словаря используется hashable-тип tuple)
commands = {
    ("буква", "на букву", "литера"): view_by_litera,
    ("автор", "автора", "писатель"): view_by_author,
    ("книга", "произведение", "книги"): view_by_book
}

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # установка голоса по умолчанию
    setup_assistant_voice()

    while True:
        # старт записи речи с последующим выводом распознанной речи и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(colored(voice_input, "blue"))

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)


