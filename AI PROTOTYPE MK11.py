import speech_recognition as sr  
import pyttsx3  
import datetime
import requests
import webbrowser
import re
import smtplib
from email.message import EmailMessage
import os
import json
import time
import random

# Voice assistant setup
recognizer = sr.Recognizer()

engine = pyttsx3.init() 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Setting female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User (Voice): {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Voice command not recognized. Trying text input...")
        return None
    except sr.RequestError:
        speak("Sorry, I'm facing some technical issues. Please try again later.")
        return None

def process_command(command):
    if command:
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")
        elif "weather" in command:
            get_weather()
        elif "search" in command:
            search_query = re.search("search (.+)", command).group(1)
            search_web(search_query)
        elif "reminder" in command and "at" in command:
            reminder_match = re.search("reminder (.+) at (.+)", command)
            if reminder_match:
                reminder = reminder_match.group(1)
                time = reminder_match.group(2)
                set_reminder(reminder, time)
                speak("Reminder set.")
            else:
                speak("Sorry, I couldn't understand the reminder. Please try again.")
        elif "send email" in command:
            send_email(recipient="john@example.com", subject="Subject", body="Body")
        elif "tell a joke" in command:
            tell_joke()
        elif "make whatsapp call" in command:
            contact_match = re.search("call (.+) on whatsapp", command)
            if contact_match:
                contact = contact_match.group(1)
                make_whatsapp_call(contact)
            else:
                speak("Sorry, I couldn't understand the contact. Please try again.")
        elif "exit" in command:
            speak("Goodbye! Have a great day.")
            exit()
        elif "take note" in command:
            note = re.search("take note (.+)", command).group(1)
            take_note(note)
        elif "show notes" in command:
            show_notes()
        elif "news" in command:
            get_news()
        elif "motivation" in command:
            get_motivational_quote()
        elif "timer" in command:
            timer_match = re.search("timer for (.+) minutes", command)
            if timer_match:
                minutes = int(timer_match.group(1))
                set_timer(minutes)
            else:
                speak("Sorry, I couldn't understand the duration. Please try again.")
        elif "math" in command:
            math_operation = re.search("math (.+)", command).group(1)
            solve_math(math_operation)
        elif "define" in command:
            word = re.search("define (.+)", command).group(1)
            define_word(word)
        elif "play" in command:
            song = re.search("play (.+)", command).group(1)
            play_music(song)
        else:
            speak("Sorry, I can't help with that.")
    else:
        speak("No command recognized.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "pune",
        "appid": "64de586459821453dfe08c1c72939119",
        "units": "square foots"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather is {weather_description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

def send_email(recipient, subject, body):
    try:
        message = EmailMessage()
        message["From"] = "anshtandale9804@gmail.com"
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("anshtandale9804@gmail.com", "Anannya@9804")
            server.send_message(message)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Sorry, there was an error sending the email: {e}")

def tell_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        joke = response.json()["joke"]
        speak(joke)
    else:
        speak("Sorry, I couldn't fetch a joke at the moment.")

def take_note(note):
    notes_file = "notes.json"
    if os.path.exists(notes_file):
        with open(notes_file, "r") as file:
            notes = json.load(file)
    else:
        notes = []

    notes.append({"note": note, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    with open(notes_file, "w") as file:
        json.dump(notes, file)

    speak("Note taken.")

def show_notes():
    notes_file = "notes.json"
    if os.path.exists(notes_file):
        with open(notes_file, "r") as file:
            notes = json.load(file)
            for i, note in enumerate(notes):
                speak(f"Note {i + 1}: {note['note']} taken on {note['timestamp']}")
    else:
        speak("You have no notes.")

def get_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",
        "apiKey": "your_api_key_here"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "ok":
        speak("Here are the top news headlines:")
        for article in data["articles"][:5]:
            speak(article["title"])
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

def get_motivational_quote():
    url = "https://type.fit/api/quotes"
    response = requests.get(url)
    if response.status_code == 200:
        quotes = response.json()
        quote = random.choice(quotes)
        speak(f"Here is a motivational quote for you: {quote['text']} by {quote.get('author', 'Unknown')}")
    else:
        speak("Sorry, I couldn't fetch a quote at the moment.")

def set_timer(minutes):
    speak(f"Setting a timer for {minutes} minutes.")
    time.sleep(minutes * 60)
    speak("Time's up!")

def solve_math(operation):
    try:
        result = eval(operation)
        speak(f"The result of {operation} is {result}")
    except Exception as e:
        speak(f"Sorry, I couldn't solve the math operation: {e}")

def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            definition = data[0]["meanings"][0]["definitions"][0]["definition"]
            speak(f"The definition of {word} is: {definition}")
        else:
            speak(f"Sorry, I couldn't find the definition for {word}.")
    else:
        speak(f"Sorry, I couldn't fetch the definition for {word}.")

def play_music(song):
    url = f"https://www.youtube.com/results?search_query={song}"
    webbrowser.open(url)
    speak(f"Playing {song} on YouTube")

def make_whatsapp_call(contact):
    # Implementation of WhatsApp call (pseudo)
    speak(f"Making a WhatsApp call to {contact}")

def set_reminder(reminder, time_str):
    # Pseudo implementation for setting a reminder
    speak(f"Setting a reminder for {reminder} at {time_str}")

def activate_voice_assistant():
    speak("Hi, I'm your college assistant. How can I help you?")
    while True:
        voice_query = listen()
        if voice_query:
            process_command(voice_query)
        else:
            text_query = input("Enter a command: ")
            process_command(text_query)

if __name__ == "__main__":
    activate_voice_assistant()
