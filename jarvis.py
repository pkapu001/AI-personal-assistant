import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import config
import random
from googletrans import Translator
import gtts
from gtts import gTTS
import playsound
import winsound
import pyglet
import sys
from time import sleep
import clipboard
import pyautogui as pya


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
print(voices[1].id)


def speak(audio):

    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if(hour >= 0 and hour < 12):
        speak("good morning!")
    elif hour >= 12 and hour < 18:
        speak("good afternoon!")
    else:
        speak("Good evening!")

    speak(" Jarvis at your service SIR!")


def takecommand():
    # it takes microphone input from user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 1000
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


def sendEmail(to, content, subject):
    msg = f'Subject: {subject}\n\n{content}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL, config.Password)
    server.sendmail(config.EMAIL, to, msg)
    server.close()
    speak('email has been sent')


if __name__ == "__main__":
    wishMe()
    browser = webbrowser.get(chrome_path)
    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        query = takecommand()

        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)
        elif 'read it' == query:
            temp = clipboard.paste()
            pya.hotkey('ctrl', 'c')
            sleep(.01)
            x = clipboard.paste()
            print(x)
            speak(x)
            clipboard.copy(temp)
        elif 'search google for' in query:
            query = query.replace('search google for', "")
            speak(f'opening google search for {query}')
            url = "http://www.google.com/search?q="+query
            browser.open_new_tab(url)
        elif 'search youtube for' in query:
            query = query.replace('search youtube for', '')
            speak(f'opening youtube search for {query}')
            url = 'https://www.youtube.com/results?search_query='+query
            browser.open_new_tab(url)
        elif 'translate to' in query:
            query = query.replace('translate to ', '')
            speak("what is the text")
            msg = takecommand()
            while msg == 'None':
                speak('sir can you please repeat')
                msg = takecommand()
            try:
                result = Translator().translate(msg, config.LANGCODES.get(query))
            except Exception as e:
                print(e)
                speak(f'cant find the language {query}')
                continue

            tts = gTTS(result.text, config.LANGCODES.get(query), True)
            filename = 'temp.mp3'
            tts.save(filename)
            music = pyglet.media.load(filename, streaming=False)
            music.play()

            sleep(music.duration)  # prevent from killing
            os.remove(filename)  # remove temperory file

            # speak(f'{msg} in {query} is {result.pronunciation}')

        elif 'open youtube' in query:
            speak('opening youtube for you sir')
            browser.open_new_tab('youtube.com')
        elif 'open google' in query:
            speak('opening google for you sir')
            browser.open_new_tab('google.com')
        elif 'open facebook' in query:
            speak('opening facebook for you sir')
            browser.open_new_tab('facebook.com')
        elif 'open whatsapp' in query:
            speak('opening whatsapp web for you sir')
            browser.open_new_tab('https://web.whatsapp.com/')
        elif 'open messages' in query:
            speak('opening messages for you sir')
            browser.open_new_tab(
                'https://messages.google.com/web/conversations')
        elif 'play music' in query:
            speak("picking a song for you sir")
            music_dir = 'R:/Music'
            folders = os.listdir(music_dir)
            folder = folders[random.randint(0, len(folders)-1)]
            songs_dir = os.path.join(music_dir, folder)
            songs = os.listdir(songs_dir)
            song = songs[random.randint(0, len(songs)-1)]
            while 'mp3' not in song:
                song = songs[random.randint(0, len(songs)-1)]

            s = os.startfile(os.path.join(
                songs_dir, song))
        elif 'stop music' in query:
            os.close(s)
        elif 'what is the time' in query:
            srtTime = datetime.datetime.now().strftime('%H:%M:%M')
            speak('sir the is')
            speak(srtTime)
        elif 'open game' in query:
            speak('opening PUBG for you sir')
            pubg_path = "R:/GAMES/pubg Lite/PUBGLite/Launcher.exe"
            os.startfile(pubg_path)
        elif 'open my computer' in query:
            os.startfile("R:/")
        elif 'send email' in query:
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
        elif 'exit' == query:
            speak('it was pleasure helping you sir')
            break
