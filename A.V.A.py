import speech_recognition as sr
import pyttsx3
import webbrowser

#tts
engine = pyttsx3.init()

#engine.say('Jutta Gefluegel')
#engine.runAndWait()

#stt
listener = sr.Recognizer()

with sr.Microphone() as source:
    voice = listener.listen(source)

try:
    term = listener.recognize_google(voice, language="de-AT")
    print(term)

    if "suche" in term.lower():
        searchterm = term.replace(" ", "+")
        link = "https://www.google.com/search?q=" + searchterm
        webbrowser.open(link)
    elif "classroom" in term.lower():
        webbrowser.open('https://classroom.google.com/u/1/h')
    elif "erledigen" in term.lower():
        webbrowser.open('https://classroom.google.com/u/1/a/not-turned-in/all')
    else:
        print("Kein Befehl") 
except:                           
    print("Could not understand audio")