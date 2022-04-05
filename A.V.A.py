import speech_recognition as sr
import pyttsx3
import webbrowser
import psycopg2

#tts
engine = pyttsx3.init()

#engine.say('Jutta Gefluegel')
#engine.runAndWait()


# connection = psycopg2.connect("dbname=AVA user=postgres password=postgres")
# cur = connection.cursor()

# query = "select phrase from altphrases"
# cur.execute(query)
# altphrases = cur.fetchall()



#stt
listener = sr.Recognizer()

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source, duration=1)
    voice = listener.listen(source)

print("Listenting...")


try:
    term = listener.recognize_google(voice, language="de-AT")
    # if term in altphrases:


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

