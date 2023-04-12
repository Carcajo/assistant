import datetime
import re
import requests
from googletrans import Translator, constants
import webbrowser
import speech_recognition as sr
import pyttsx3
from user import User

def extract_city_function(command: str):
    pattern = r"погода в ([\w\s]+)"
    match = re.search(pattern, command.lower())
    if match:
        return match.group(1)
    else:
        return None


def get_weather_function(city: str):
    translator = Translator()
    result = translator.translate(city, src='ru', dest='en')
    # замените на свой API ключ OpenWeatherMap
    api_key = "d3b9ddd02bf307000417e311a213a7f4"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={result.text}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return translator.translate(
            f"In {city} {weather}, temperature {int(temperature)} degrees celsius, humidity {int(humidity)} percents, and wind speed {int(wind_speed)} meters per second.",
            dest="ru").text  # type: ignore
    else:
        return "Извините, я не смог получить информацию о погоде в этом городе."


def hello_function(a) -> str:
    return "Хабар принес?"


def doing_function(a) -> str:
    return "Можно и передохнуть маленько"


def time_function(a) -> str:
    now = datetime.datetime.now()
    return "Сейчас " + str(now.hour) + ":" + str(now.minute)


def stop_function(a) -> str:
    return "Ну, удачной охоты, сталкер."


def default_function(a) -> str:
    return "Не удалось распознать команду."


def mood_function(a) -> str:
    return "Какие дела могут быть у робота? Не крашнулся и то хорошо"


def joke_function(a) -> str:
    return "Колобок повесился, ахаххаха"


def commands_function(a) -> str:
    return "Пока что я могу: найти информацию в интернете, рассказать анектод, сказать сколько сейчас времени, поприветсвовать вас, попрощаться с кожанным, также вы можете поинтересоваться как у меня дела"


def search_function(a) -> str:  # type: ignore
    sentence = ' '.join(a)
    try:
        webbrowser.open_new_tab("https://www.google.com/search?q="+str(a))
        return "Открываю браузер"
    except:
        return "Не удалось открыть"
    
def youtube_function(a)->str:
    sentence = ' '.join(a)
    print(sentence)
    url = "https://www.youtube.com/results?search_query=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю ютуб"
    except:
        return "Не удалось открыть"

def settings_function(a)->str:
    engine = pyttsx3.init()
    engine.say("Скажите как вас зовут")
    engine.runAndWait()
    audio = recognize_speech()
    name = audio_to_text(audio)

    engine.say("Скажите какого вы пола")
    engine.runAndWait()
    audio = recognize_speech()
    sex = audio_to_text(audio)

    engine.say("Каким будет ваш основной язык")
    engine.runAndWait()
    audio = recognize_speech()
    language = audio_to_text(audio)


    engine.say("Каким будет ваш дополнительный язык")
    engine.runAndWait()
    audio = recognize_speech()
    second_language = audio_to_text(audio)

    user = User(name, sex, language, second_language)

    engine.say("Пользователь успешно добавлен")
    engine.runAndWait()

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source, phrase_time_limit=5)
        return audio

def audio_to_text(audio):
    r = sr.Recognizer()
    text = r.recognize_google(audio, language="ru-Ru")
    return str(text)

  
