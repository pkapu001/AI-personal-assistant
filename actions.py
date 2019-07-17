import pyttsx3
import os
import random
import pyautogui as pya
import clipboard
from time import sleep
import smtplib
import config
import speech_recognition as sr
import keyboard


def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()


def stop_speak():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.stop()
    engine.say('')
    engine.runAndWait()


def takecommand():
    # it takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        r.energy_threshold = 1500
        print('Listening sir...')
        audio = r.listen(source)
    try:
        print("recoganizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f'sir u said : {query}')
    except Exception as e:
        # print(e)
        #  print("can u please repeat that!")
        return "None"
    return query.lower()


def play_music():
    speak("picking a song for you sir")
    music_dir = r'R:\Music'
    folders = os.listdir(music_dir)
    folder = random.choice(folders)

    songs_dir = os.path.join(music_dir, folder)
    songs = os.listdir(songs_dir)
    song = random.choice(songs)

    while 'mp3' not in song:
        song = random.choice(songs)

    songpath = os.path.join(songs_dir, song)
    speak(f'playing {song}')
    print(songpath)
    os.startfile(os.path.join(songs_dir, song))


def read_it():
    try:
        temp = clipboard.paste()
        pya.hotkey('ctrl', 'c')
        sleep(.01)
        x = clipboard.paste()
        print(x)
        speak(x)
        clipboard.copy(temp)
    except Exception as e:
        print(e)
        speak("sir can you please try it again")


def sendEmail(to, content, subject):
    msg = f'Subject: {subject}\n\n{content}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL, os.environ['gmail_password'])
    server.sendmail(config.EMAIL, to, msg)
    server.close()
    speak('email has been sent')


def process_email():
    try:
        speak("whom do you want to send email to?")
        name = takecommand()
        while name not in config.contacts:
            speak(f'{name} not in your contacts')
            name = takecommand()
        to = config.contacts.get(name)
        speak('what is the subject of the email?')
        subject = takecommand()
        while 'None' == subject:
            speak('please repeat the subject')
            subject = takecommand()

        speak(' what is your message sir')
        content = takecommand()
        while 'None' == content:
            speak('please repeat the message')
            content = takecommand()
        speak(
            f"do you want me to send the email with message: {content} ")
        conform = takecommand()
        while 'yes' not in conform and 'no' not in conform:
            speak('please say yes or no')
            conform = takecommand()

        if 'yes' in conform:
            speak('sending email sir')
            sendEmail(to, content, subject)
        elif 'no' == conform:
            speak('mission aborted')
    except Exception as e:
        print(e)
        speak('cudnt send email')
