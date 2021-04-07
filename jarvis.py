
import speech_recognition as sr
from datetime import datetime
import json
import requests
import pyautogui
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS as tts
import geocoder

# timetext="what is the time"
# atenndtext="attend the meeting"
# weathertext="weather"


"""
 
   ____                  _               
  / ___|  ___ _ ____   _(_) ___ ___  ___ 
  \___ \ / _ \ '__\ \ / / |/ __/ _ \/ __|
   ___) |  __/ |   \ V /| | (_|  __/\__ \
  |____/ \___|_|    \_/ |_|\___\___||___/
                                         
 
"""

def getapikey():
    with open("config.env") as f:
        for line in f:
            key, value = line.strip().split('=', 1)
    f.close()
    return value


def getweather():
    g = geocoder.ip('me')
    apikey=getapikey()
    base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={g.latlng[0]}&lon={g.latlng[1]}&units=metric&appid={apikey}"
    r = requests.get(base_url)
    weathertext=json.loads(r.text)["main"]
    return str(weathertext["temp"])


def attendMeeting():
    driver=webdriver.Chrome(r"./chromedriver")
    driver.get("https://us02web.zoom.us/j/81189911538?pwd=dWcrZFp5cHRwNHljRk1LeS9mbWVsQT09#success")
    action=ActionChains(driver)
    login_button=driver.find_element_by_xpath('//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div')
    action.click(on_element=login_button)
    action.perform()
    time.sleep(1)
    pyautogui.hotkey("left")
    pyautogui.hotkey("enter")

    time.sleep(10)
    print("opened")

    for i in range(0,3):
        pyautogui.hotkey("tab")
    pyautogui.hotkey("enter")
    return "You Attended the Meeting"


def gettime():
    now = datetime.now()
    hour=int(now.strftime("%H"))

    min = str(now.strftime("%M"))
    if hour>12:
        return f"{hour-12} {min} PM"
    else:
        return f"{hour} {min} PM"

# def speak(text):
#     engine = pyttsx3.init(driverName="espeak")   
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[11].id)
    
#     engine.setProperty("rate", 150) 
#     engine.say(text)   
#     engine.runAndWait()  


"""
 
     ____            _                                    _ _       
    / ___|__ _ _ __ | |_ _   _ _ __ ___    __ _ _   _  __| (_) ___  
   | |   / _` | '_ \| __| | | | '__/ _ \  / _` | | | |/ _` | |/ _ \ 
   | |__| (_| | |_) | |_| |_| | | |  __/ | (_| | |_| | (_| | | (_) |
    \____\__,_| .__/ \__|\__,_|_|  \___|  \__,_|\__,_|\__,_|_|\___/ 
              |_|                                                   
 
"""

def capture(timelimit):

    rec = sr.Recognizer()

    with sr.Microphone() as source:
        audio = rec.listen(source, phrase_time_limit=timelimit)

    try:
        text = rec.recognize_google(audio, language='en-US')
        return text

    except:
        return ""

"""
 
   ____                   _                      _ _       
  / ___| _ __   ___  __ _| | __   __ _ _   _  __| (_) ___  
  \___ \| '_ \ / _ \/ _` | |/ /  / _` | | | |/ _` | |/ _ \ 
   ___) | |_) |  __/ (_| |   <  | (_| | |_| | (_| | | (_) |
  |____/| .__/ \___|\__,_|_|\_\  \__,_|\__,_|\__,_|_|\___/ 
        |_|                                                
 
"""
# def speak(text):
#     print(text)
#     speech = tts(text=text, lang='en')
#     speech_file = 'input.mp3'
#     speech.save(speech_file)
#     sound = AudioSegment.from_mp3(speech_file)
#     play(sound)
#     os.remove(speech_file)
import boto3
import os
from pydub import AudioSegment
from pydub.playback import play

client = boto3.client('polly')


def speak(text):
    res=client.synthesize_speech(Text=text,VoiceId="Matthew",OutputFormat="mp3")
    audio=res["AudioStream"].read()
    speech_file = 'input.mp3'

    with open(speech_file,"wb") as file:
        file.write(audio)
        file.close()
    sound = AudioSegment.from_mp3(speech_file)
    play(sound)
    os.remove(speech_file)

# 

# def process_text(name, input):
#     if input=="":
#         speak(name+" say something dude ")
#     else:
#         speak(name + ', you said: "' + input + '".')
#     return



"""
 
   __  __       _          ____          _      
  |  \/  | __ _(_)_ __    / ___|___   __| | ___ 
  | |\/| |/ _` | | '_ \  | |   / _ \ / _` |/ _ \
  | |  | | (_| | | | | | | |__| (_) | (_| |  __/
  |_|  |_|\__,_|_|_| |_|  \____\___/ \__,_|\___|
                                                
 
"""


if __name__ == "__main__":
    print("I am listning")
    initial_response = capture(2).lower()
    print(initial_response)
    if initial_response=="hai" or initial_response=="hello"  or initial_response=="hey" :
        speak('hello sagar what do you want')
        while 1:
            response = capture(3).lower()
            print(response)
            if response=="weather at outside":
                speak(f"you need weather report ?")
                response = capture(1).lower()
                if response=="yes":
                    speak("Ok just a moment")
                    weathervalue=getweather()
                    speak("the temparature at out side is "+str(weathervalue) +"celsius")
                    break
                elif response=="no":
                    speak("ok thank you bye")
                    break
            elif response=="bye":
                speak("okay thank you")
                break
            elif response=="attend the meeting":
                speak("okay wait a moment")
                response=attendMeeting()
                speak(response)
                break
            elif response=="what is the time":
                speak("okay wait a moment")
                response=gettime()
                speak(response)
                break  
            else:
                speak("i did not get you vidya")
                continue
        