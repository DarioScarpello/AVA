from email.policy import default
import speech_recognition as sr
import pyttsx3
import webbrowser
import psycopg2
import wikipediaapi
import re

#tts
speaker = pyttsx3.init()

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

# listen via microphone
##with sr.Microphone() as source:
##    listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
##    voice = listener.listen(source)


# try catch block to give out error message, to filter out exceptions 
try:
    # recognize said words wia google recognizer API
    # add whitespace before and after said term, to match the data in database
    term = " wikipedia " #" " + listener.recognize_google(voice, language="de-AT") +  " ".lower()
    
    # go over ever altphrase
    for phrase in altphrases:   
        # check if an altphrase is present in the said term
        if phrase in term:
            # get the keyphrase according to the determined altphrase via the database
            query = "select k.phrase from keyphrases k join altphrases a on k.id = a.fid where a.phrase = '" + phrase + "'"
            cur.execute(query)
            keyphrase = [r[0] for r in cur.fetchall()]

            # if it is a google search, create the term to search 
            # create a variable for the phrase to search by in the query
            if keyphrase[0] == "google":
                termToSearch = term.replace(phrase, "")
                break

            break


    print("Said term = " + term)
            
    print("Keyphrase = " + keyphrase[0]) 
    

    # switch-case to get the correct code via command
    match keyphrase[0]:
        # google search
        case "google":                                                                      
            link = "https://www.google.com/search?q=" + termToSearch
            webbrowser.open(link)

            speaker.say(f"Das habe ich im Internet zu {termToSearch} gefunden.")
            speaker.runAndWait()

        # open google classroom
        case "classroom":                                                                   
            webbrowser.open('https://classroom.google.com/u/2/h')

            speaker.say("Ich habe Google Classroom für dich geöffnet")
            speaker.runAndWait()

        # open the not finished tasks in google classroom
        case "erledigen":                                                                   
            webbrowser.open('https://classroom.google.com/u/2/a/not-turned-in/all')

            speaker.say("Diese Sachen hast du noch zu erledigen")
            speaker.runAndWait()

        # calculate said equasion 
        case "rechner":      
            termSplittet = term.split(" ")
            for word in termSplittet:
                print("bruh")

            if "plus" in term:
                print("bruh")

            elif "minus" in term:
                print("bruh")

            elif "dividiert durch" in term:
                print("bruh")
            
            elif "mal" in term:
                print("bruh")

        # read summary of wikipedia article
        case "wikipedia":                                                                   
            wiki_wiki = wikipediaapi.Wikipedia('de')
            page_py = wiki_wiki.page('HTL Wien West')
            if page_py.exists() == True: 
                print(page_py.summary[0:500])
            else:
                print("Diesen Artikel gibt es leider nicht")

        # Default case / No Command
        case _:                                                                              
            print("Kein Befehl")
            speaker.say("Tut mir leid, das habe ich nicht verstanden.")
            speaker.runAndWait()


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

