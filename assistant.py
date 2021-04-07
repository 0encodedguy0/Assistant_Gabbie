# Голосовой ассистент НИКА 1.0 BETA
import os
import webbrowser
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('ника', 'николь', 'вероника', 'вероничка', 'никуля', 'ника',
              'ники', 'никита', 'ник', 'вероник'),
    "tbr": ('скажи', 'расскажи', 'сколько', 'произнеси', 'подскажи', 'напомни', 'включи', 'подключи', 'подруби',
            'воспроизведи', 'расскажи', 'знаешь', 'покажи', 'открой', 'загрузи', 'найди', 'поищи'),
    "cmds": {
        "time": ('текущее время', 'сейчас времени', 'который час', 'время', 'времечко', 'какой часик', 'часок',
                  'сколько сейчас', 'сколько сейчас времени'),
        "radio": ('музыку', 'радио', 'музычку', 'музло', 'музяку', 'музон', 'радиостанцию', 'плейлист'),
        "stupid": ('анекдот', 'рассмеши меня', ''),
        "web1": ('гугл', 'интернет'),
        "web2": ('в гугле', 'загугли', 'в интернете'),
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmds'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmds'] = c
                RC['percent'] = vrt

    return RC


def add_file(x):
    file = open('commands.txt', 'a',encoding = 'UTF-8')
    if x != '':
        file.write(x+'\n')
    file.close()


def check_searching(): # проверяет нужно-ли искать в интернете
    global text, wifi_name, add_file
    global adress
    global web_search
    if 'найди' in text:
        add_file('найди')
        adress = text.replace('найди','').strip()
        text = text.replace(adress,'').strip()
        web_search()
        text = ''
    elif 'найти' in text:
        add_file('найди')
        adress = text.replace('найти','').strip()
        text = text.replace(adress,'').strip()
        web_search()
        text = ''
    adress = ''


def execute_cmd(cmd):
    if cmd == 'time':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("D:\\Jarvis\\res\\radio_record.m3u")

    elif cmd == 'stupid':
        # рассказать анекдот
        speak("Василий Иванович, белые идут!! Ну белые же идут! — А как же красные? — А красные вас полнят")

    elif cmd == 'web1':
        webbrowser.open('https://google.ru')

    elif cmd == 'web2':
        def web_search():  # осуществляет поиск в интернете по запросу (adress)
            global adress
            webbrowser.open('https://www.google.com/'.format(adress))
    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

# forced cmd test
#speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Добрый день, повелитель")
speak("Ника слушает")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.0001) #infinity loop