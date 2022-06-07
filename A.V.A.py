from ast import operator
from email.policy import default
import string
from tokenize import String

# speechrecognition library for speechrecognition
import speech_recognition as sr

# Text to speach library for tts
import pyttsx3

# webbrowser library for working with webbrowsers
import webbrowser

# psycopg2 library for working with databases
import psycopg2

# wikipediaapi library for working with wikipedia
import wikipediaapi

# regular expression library to work with regex
import re
import urllib.request
import urllib.parse

# pandas, pyplot, sklearn librarys for simple prediction
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# decouple library for working with environment variables
from decouple import config

# GUI Libraries
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.animation import Animation
Window.size = (300, 300)
import _thread
from kivy.clock import Clock
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen

# create GUI
class AVA(MDApp):
    def build(self):
        self.icon = 'ava.png'
        self.theme_cls.material_style = "M3"
        return Builder.load_string(

            '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
FloatLayout: 
    orientation: 'vertical'

    MDIconButton:
        icon: "ava.png"
        icon_size: "150sp"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: app.foo2()

    MDIcon:
        id: box
        source: "white.png"
        valign: "bottom"
        halign: "left"
'''
        )

    def foo1(self):
        # create speaker object
        speaker = pyttsx3.init()

        # getting credentials from environment variables for the database
        db_name = config('db_name')
        db_user = config('db_user')
        db_pass = config('db_pass')

        # Creating the connection via the connection string to the database and the cursor to fetch the data 
        connection = psycopg2.connect(f"dbname={db_name} user={db_user} password={db_pass}") # Connectionstring verbergen !!!
        cur = connection.cursor()

        # the query that gets all the altphrases, which will be used throughout the whole program
        query = "select phrase from altphrases order by length(phrase) desc"    
        cur.execute(query)         
        # altphrases = cur.fetchall()                   # only .fetchall() returns a tuple, to use the "if term in list" method 
        altphrases = [r[0] for r in cur.fetchall()] 	# the tuple is converted into a normal list via the code on the left

        #stt
        listener = sr.Recognizer()      # defining the listener object

        print("Listening...")

        # listen via microphone
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
            self.root.ids.box.source = "green.png"
            voice = listener.listen(source, phrase_time_limit=5)
            self.root.ids.box.source = "white.png"
        
        # try catch block to give out error message, to filter out exceptions 
        #try:
            # recognize said words via google recognizer API
            # add whitespace before and after said term, to match the data in database
            saidterm = " suche test  " #" " + listener.recognize_google(voice, language="de-AT") +  " "
            term = saidterm.lower()
            
            # go over every altphrase
            for phrase in altphrases:   
                # check if an altphrase is present in the said term
                if phrase in term:
                    # get the keyphrase according to the determined altphrase via the database
                    query = "select k.phrase from keyphrases k join altphrases a on k.id = a.fid where a.phrase = '" + phrase + "'"
                    cur.execute(query)
                    keyphrase = [r[0] for r in cur.fetchall()]

                    # Case Statement for cutting out termToSearch
                    match keyphrase[0]:
                        case "google": 
                            termToSearch = term.replace(phrase, "")
                            break
                        
                        case "youtube":
                            termToSearch = term.replace(phrase, "")
                            break

                        case "youtube abspielen":
                            termToSearch = term.replace(phrase, "")
                            break
                        
                        case "wikipedia":
                            termToSearch = term.replace(phrase, "")
                            break
                        
                        case "wetter":
                            termToSearch = term.replace(phrase, "")
                            break
                    break

                    # if keyphrase[0] == "google":
                    #     termToSearch = term.replace(phrase, "")
                    #     break

                    # # if it is a youtube search, create the term to search
                    # # create a variable for the phrase to search by in the query
                    # elif keyphrase[0] == "youtube": 
                    #     termToSearch = term.replace(phrase, "")
                    #     break

                    # elif keyphrase[0] == "youtube abspielen":
                    #     termToSearch = term.replace(phrase, "")
                    #     break

                    # # if it is a youtube search, create the term to search
                    # # create a variable for the phrase to search by in the query
                    # elif keyphrase[0] == "wikipedia":
                    #     termToSearch = term.replace(phrase, "")
                    #     break
                    
                    # # if it is a weather search, create the term to search
                    # # create a variable for the phrase to search by in the query
                    # elif keyphrase[0] == "wetter":
                    #     termToSearch = term.replace(phrase, "")
                    #     break

                    # break

            print(f"Said term = {term}")

            # print(f"Triggered keyphrase = {keyphrase[0]}") 
            
            # function to open websites
            # bool parameter to say if there is an extra term to search by
            def openWebsite(link, voiceAnswer, is_extraTerm: bool ):
                if is_extraTerm:
                    google_link = link + termToSearch
                    webbrowser.open(google_link)
                    speaker.say(voiceAnswer)
                    speaker.runAndWait()

                else:
                    webbrowser.open(link)
                    speaker.say(voiceAnswer)
                    speaker.runAndWait()
                    
            # function for calculation
            def calculate(splittetTerm, operator):
                # get position of operator in term to get the two numbers to calculate
                operationPos = splittetTerm.index(operator)
                firstNum = splittetTerm[operationPos-1]
                secondNum = splittetTerm[operationPos+1]

                # do the correct operation depending on the said operator
                match operator:
                    case "plus":
                        result = int(firstNum) + int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} plus {secondNum} ergibt {result}")

                    case "minus":
                        result = int(firstNum) - int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} minus {secondNum} ergibt {result}")

                    case "mal":
                        result = int(firstNum) * int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} multipliziert mit {secondNum} ergibt {result}")

                    case "multipliziert mit":
                        result = int(firstNum) * int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} multipliziert mit {secondNum} ergibt {result}")

                    case "x":
                        result = int(firstNum) * int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} multipliziert mit {secondNum} ergibt {result}")

                    case "diviert durch":
                        result = int(firstNum) / int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} dividiert durch {secondNum} ergibt {result}")

                    case "durch":
                        result = int(firstNum) / int(secondNum)
                        speaker.say(f"Das Ergebnis von {firstNum} dividiert durch {secondNum} ergibt {result}")
                
                speaker.runAndWait()

            # switch-case to get the correct code via command
            match keyphrase[0]:
                # google search
                case "google":
                    openWebsite("https://www.google.com/search?q=", f"Das habe ich im Internet zu {termToSearch} gefunden.", True)

                case "wetter":
                    openWebsite("https://www.google.com/search?q=Wetter ", f"Das ist das Wetter in {termToSearch}.", True)
                
                # open google classroom
                case "classroom":
                    openWebsite('https://classroom.google.com/u/1/h', "Ich habe Google Classroom für dich geöffnet", False)
                
                # open the not finished tasks in google classroom
                case "erledigen":
                    openWebsite('https://classroom.google.com/u/1/a/not-turned-in/all', "Diese Sachen hast du noch zu erledigen", False)

                # search on youtube
                case "youtube":
                    openWebsite("https://www.youtube.com/results?search_query=", "Das hab ich auf Youtube gefunden", False)
                
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
                    # split said term to better define the operation       
                    termSplittet = term.split(" ")

                    if "plus" in term:
                        operator = "plus"

                    elif "minus" in term:
                        operator = "minus"

                    elif "dividiert durch" in term:
                        operator = "dividiert durch"

                    elif "durch" in term:
                        operator = "durch"

                    elif "x" in term:
                        operator = "x"
                    
                    elif "multipliziert mit" in term:
                        operator = "multipliziert mit"

                    elif "mal" in term:
                        operator = "mal"

                    calculate(termSplittet, operator)

                # read summary of wikipedia article
                case "wikipedia":         
                    # set the language and get the first 250 characters of wikipedia page, if it exists                                                          
                    wiki_wiki = wikipediaapi.Wikipedia('de')
                    page_py = wiki_wiki.page(termToSearch)
                    if page_py.exists() == True: 
                        speaker.say(page_py.summary[0:250])
                        speaker.runAndWait()

                        # ask user if they want to open the wikipedia page, if first 250 characters was not enough
                        speaker.say(f"Wenn du mehr dazu hören willst, kann ich gerne die Wikipedia Seite zu {termToSearch} öffnen")
                        speaker.runAndWait()
                        
                        print("Warte auf antwort.")
                        # listen via microphone
                        with sr.Microphone() as source:
                            listener.adjust_for_ambient_noise(source, duration=1)   # adjustment of the listener, to cut out ambient noise
                            voice = listener.listen(source)

                        # get users answer
                        answer = " " + listener.recognize_google(voice, language="de-AT") +  " ".lower()
                        print(answer)

                        query = "select k.phrase from keyphrases k join altphrases a on k.id = a.fid where a.phrase = '" + answer + "'"
                        cur.execute(query)
                        keyphrase = [r[0] for r in cur.fetchall()]

                        # open the according wikipedia page, if user wants to
                        if keyphrase[0] == "ja":
                            termToSearch = termToSearch.title()
                            termForWikipedia = termToSearch.replace(" ", "_")
                            google_link = "https://de.wikipedia.org/wiki/" + termForWikipedia
                            webbrowser.open(google_link)

                    # tell the user, if the searched wikipedia page was not found        
                    else:
                        speaker.say(f"Zu diesem Thema habe ich leider keine Wikipedia Seite finden können.")
                        speaker.runAndWait()
                        
                # AI prediction
                case "prediction":
                    termSplittet = term.split(" ")

                    data = pandas.read_csv('schuljahr_schueler.csv')
                    # plt.scatter(data['schuljahr'], data['schueleranzahl'])
                    # plt.show()
                    model = LinearRegression()
                    model.fit(data[['schuljahr']], data[['schueleranzahl']])
                    jahrPos = termSplittet.index("Jahren")
                    anzahlJahre = termSplittet[jahrPos-1]
                    anzahl = int(anzahlJahre)
                    prediction = model.predict([[anzahl]])
                    anzahlSchueler = round(prediction[0][0])
                    print(f"In {anzahlJahre} Jahren gibt es voraussichtlich {anzahlSchueler} Schüler*innen an der Schule.")
                    speaker.say(f"In {anzahlJahre} Jahren gibt es voraussichtlich {anzahlSchueler} Schüler*innen an der Schule.")
                    speaker.runAndWait()

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
            
        # except Exception as e:                           
        #     print(e)
    
    def foo2(self):
        try:
            _thread.start_new_thread(self.foo1)
        except:
            print("error")

AVA().run()