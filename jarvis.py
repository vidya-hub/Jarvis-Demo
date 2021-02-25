
import speech_recognition as sr
import pyttsx3
import json
import requests

import geocoder

timetext="what is the time"
atenndtext="attend the meeting"
weathertext="weather"

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



def speak(text):
    engine = pyttsx3.init(driverName="espeak")   
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[11].id)
    
    engine.setProperty("rate", 150) 
    engine.say(text)   
    engine.runAndWait()  


def process_text(name, input):
    if input=="":
        speak(name+" say something dude ")
    else:
        speak(name + ', you said: "' + input + '".')
    return


def capture(timelimit):
    """Capture audio"""

    rec = sr.Recognizer()

    with sr.Microphone() as source:
        audio = rec.listen(source, phrase_time_limit=timelimit)

    try:
        text = rec.recognize_google(audio, language='en-US')
        return text

    except:
        return ""
    
    
    
    
if __name__ == "__main__":
    print("I am listning")
    initial_response = capture(2).lower()
    print(initial_response)
    if initial_response=="hai" or initial_response=="hello"  or initial_response=="hey" :
        speak('hello sagar what do you want')
        while 1:
            response = capture(2).lower()
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
        
            else:
                speak("i didnt get you vidya")
                continue
        