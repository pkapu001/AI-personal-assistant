import datetime

import wikipedia
import webbrowser
import os
import smtplib
import config
import random
from googletrans import Translator
from gtts import gTTS
import winsound
import pyglet
import sys
from time import sleep

import actions as asistant


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if(hour >= 0 and hour < 12):
        asistant.speak("good morning!")
    elif hour >= 12 and hour < 18:
        asistant.speak("good afternoon!")
    else:
        asistant.speak("Good evening!")

    asistant.speak(" Jarvis at your service SIR!")


if __name__ == "__main__":
    wishMe()
    browser = webbrowser.get(chrome_path)
    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        query = asistant.takecommand()

        if 'wikipedia' in query:
            query = query.replace('wikipedia', '')
            asistant.speak(f'Searching wikipedia... for {query}')
            results = wikipedia.summary(query, sentences=2)
            asistant.speak("according to wikipedia")
            print(results)
            asistant.speak(results)
        elif 'read it' == query:
            asistant.read_it()
        elif 'calculate' in query:
            query = query.replace('calculate', '')
            try:
                result = eval(query)
                asistant.speak(f'answer is, {result}')
            except Exception as e:
                asistant.speak("sorry sir i cant calculate that")

        elif 'search google for' in query:
            query = query.replace('search google for', "")
            asistant.speak(f'opening google search for {query}')
            url = "http://www.google.com/search?q="+query
            browser.open_new_tab(url)
        elif 'search images of' in query:
            query = query.replace('search images of', '')
            asistant.speak(f'searching google for images of {query}')
            url = f'https://www.google.com/search?tbm=isch&q={query}'
            browser.open_new_tab(url)
        elif 'search youtube for' in query:
            query = query.replace('search youtube for', '')
            asistant.speak(f'opening youtube search for {query}')
            url = 'https://www.youtube.com/results?search_query='+query
            browser.open_new_tab(url)
        elif 'translate to' in query:
            query = query.replace('translate to ', '')
            asistant.speak("what is the text")
            msg = asistant.takecommand()
            while msg == 'None':
                asistant.speak('sir can you please repeat')
                msg = asistant.takecommand()
            try:
                result = Translator().translate(msg, config.LANGCODES.get(query))
            except Exception as e:
                print(e)
                asistant.speak(f'cant find the language {query}')
                continue

            tts = gTTS(result.text, config.LANGCODES.get(query), True)
            filename = 'temp.mp3'
            tts.save(filename)
            music = pyglet.media.load(filename, streaming=False)
            music.play()

            sleep(music.duration)  # prevent from killing
            os.remove(filename)  # remove temperory file

            # asistant.speak(f'{msg} in {query} is {result.pronunciation}')

        elif 'open youtube' in query:
            asistant.speak('opening youtube for you sir')
            browser.open_new_tab('youtube.com')
        elif 'open google' in query:
            asistant.speak('opening google for you sir')
            browser.open_new_tab('google.com')
        elif 'open facebook' in query:
            asistant.speak('opening facebook for you sir')
            browser.open_new_tab('facebook.com')
        elif 'open whatsapp' in query:
            asistant.speak('opening whatsapp web for you sir')
            browser.open_new_tab('https://web.whatsapp.com/')
        elif 'open messages' in query:
            asistant.speak('opening messages for you sir')
            browser.open_new_tab(
                'https://messages.google.com/web/conversations')
        elif 'play music' in query:
            asistant.play_music()
        elif 'what is the time' in query:
            srtTime = datetime.datetime.now().strftime('%H:%M:%M')
            asistant.speak('sir the is')
            asistant.speak(srtTime)
        elif 'open game' in query:
            asistant.speak('opening PUBG for you sir')
            pubg_path = "R:/GAMES/pubg Lite/PUBGLite/Launcher.exe"
            os.startfile(pubg_path)
        elif 'open my computer' in query:
            os.startfile("R:/")
        elif 'send email' in query:
            asistant.process_email()
        elif 'exit' == query:
            asistant.speak('it was pleasure helping you sir')
            break
