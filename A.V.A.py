from email.policy import default
import speech_recognition as sr
import pyttsx3
import webbrowser
import psycopg2
import urllib.request
import urllib.parse
import wikipediaapi
import re

#tts
speaker = pyttsx3.init()

# speaker.say('Hallo ich rede')
# speaker.runAndWait()

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
with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
    voice = listener.listen(source)


# try catch block to give out error message, to filter out exceptions 
try:
    # recognize said words via google recognizer API
    # add whitespace before and after said term, to match the data in database
    term = " " + listener.recognize_google(voice, language="de-AT") +  " ".lower()
    
    # go over every altphrase
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
            # if it is a youtube search, create the term to search
            # create a a variable for the phrase to search by in the query
            elif keyphrase[0] == "youtube" or keyphrase[0] == "youtube abspielen":
                termToSearch = term.replace(phrase, "")
                break
            break

    print(keyphrase[0]) 
    
    print(term)

    # switch-case to get the correct code via command
    match keyphrase[0]:
        # google search
        case "google":
            google_link = "https://www.google.com/search?q=" + termToSearch
            webbrowser.open(google_link)
            speaker.say("Das habe ich im Internet zu " + termToSearch + "gefunden.")
            speaker.runAndWait()
        # open google classroom
        case "classroom":
            webbrowser.open('https://classroom.google.com/u/1/h')
            speaker.say("Ich habe Google Classroom für dich geöffnet")
            speaker.runAndWait()
        # open the not finished tasks in google classroom
        case "erledigen":
            webbrowser.open('https://classroom.google.com/u/1/a/not-turned-in/all')
            speaker.say("Diese Sachen hast du noch zu erledigen")
            speaker.runAndWait()
        # search on youtube
        case "youtube":
            youtube_link = "https://www.youtube.com/results?search_query=" + termToSearch
            webbrowser.open(youtube_link)
            speaker.say("Das hab ich auf Youtube gefunden")
            speaker.runAndWait()
        # open first video on yoututbe
        case "youtube abspielen":
            query_string = urllib.parse.urlencode({"search_query" : termToSearch})
            html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?"+query_string)
            search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
            if search_results:
                print("http://www.youtube.com/watch?v=" + search_results[0])
                webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            speaker.say("Das ist das erste Video zu" + termToSearch)
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
        # default no command
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