import speech_recognition as sr
import pyttsx3
import webbrowser
import psycopg2

#tts
engine = pyttsx3.init()

# engine.say('Hallo ich rede')
# engine.runAndWait()

# Creating the connection via the connection string to the database and the cursor to fetch the data 
connection = psycopg2.connect("dbname=AVA user=postgres password=postgres") # Connectionstring verbergen !!!
cur = connection.cursor()

# the query that gets all the altphrases, which will be used throughout the whole program
query = "select phrase from altphrases"    
cur.execute(query)         
# altphrases = cur.fetchall()                   # only .fetchall() returns a tuple, to use the "if term in list" method 
altphrases = [r[0] for r in cur.fetchall()] 	# the tuple is converted into a normal list via the code on the left





#stt
listener = sr.Recognizer()      # defining the listener object

print("Listenting...")

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
    voice = listener.listen(source)



# try catch block to give out error message, to filter out exceptions 
try:
    term = listener.recognize_google(voice, language="de-AT")
    for phrase in altphrases:
        if term in phrase:
            term = phrase


    if term in altphrases:
        query = "select k.phrase from keyphrases k join altphrases a on k.id = a.fid where a.phrase = " + term
        cur.execute(query)
        keyphrase = [r[0] for r in cur.fetchall()]

    print(keyphrase)
    

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

