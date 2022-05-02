from email.policy import default
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
query = "select phrase from altphrases order by length(phrase) desc"    
cur.execute(query)         
# altphrases = cur.fetchall()                   # only .fetchall() returns a tuple, to use the "if term in list" method 
altphrases = [r[0] for r in cur.fetchall()] 	# the tuple is converted into a normal list via the code on the left





#stt
listener = sr.Recognizer()      # defining the listener object

print("Listenting...")

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
    voice = listener.listen(source)

print("Listening 2")

# try catch block to give out error message, to filter out exceptions 
try:
    term = " " + listener.recognize_google(voice, language="de-AT")+ " ".lower()
    
    for phrase in altphrases:   
        # term splitten und dann schauen ob phrase in dieser liste vorhanden ist

        if phrase in term:
            if phrase == " google " or phrase == " suche nach ":
                termToSearch = term.replace(phrase, "")
                altphraseToUseInQuery = phrase
            else:
                altphraseToUseInQuery = phrase
                break


    if altphraseToUseInQuery in altphrases:
        query = "select k.phrase from keyphrases k join altphrases a on k.id = a.fid where a.phrase = '" + altphraseToUseInQuery + "'"
        cur.execute(query)
        keyphrase = [r[0] for r in cur.fetchall()]


    print(keyphrase[0])
    
    print(term)


    match keyphrase[0]:
        case "google":
            link = "https://www.google.com/search?q=" + termToSearch
            webbrowser.open(link)
        case "classroom":
            webbrowser.open('https://classroom.google.com/u/1/h')
        case "erledigen":
            webbrowser.open('https://classroom.google.com/u/1/a/not-turned-in/all')
            
        case _:
            print("Kein Befehl")

    # if keyphrase[0] == "google":
    #     link = "https://www.google.com/search?q=" + termToSearch
    #     webbrowser.open(link)
    # elif keyphrase[0] == "classroom":
    #     webbrowser.open('https://classroom.google.com/u/1/h')
    # elif "erledigen" in term.lower():
    #     webbrowser.open('https://classroom.google.com/u/1/a/not-turned-in/all')
    # else:
    #     print("Kein Befehl")
     
     
except Exception as e:                           
    print(e)

