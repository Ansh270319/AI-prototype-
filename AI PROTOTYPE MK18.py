import json
import os
import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser
import re
import smtplib
from email.message import EmailMessage
import time
import random
from textblob import TextBlob

# Voice assistant setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Setting Male Voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=5):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("No audio input. Trying text input...")
            return None

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

def log_conversation(user_input, response, emotion):
    log_file = "conversation_log.json"
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "response": response,
        "emotion": emotion
    }
    
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(logs, file, indent=4)

def detect_emotion(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

def process_command(command):
    response = ""
    emotion = "neutral"  # Default emotion if command is None
    if command:
        emotion = detect_emotion(command)
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            speak(response)
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Today's date is {current_date}"
            speak(response)
        elif "weather" in command:
            response = get_weather()
        elif "search" in command:
            search_query = re.search("search (.+)", command).group(1)
            response = search_web(search_query)
        elif "reminder" in command and "at" in command:
            reminder_match = re.search("reminder (.+) at (.+)", command)
            if reminder_match:
                reminder = reminder_match.group(1)
                time = reminder_match.group(2)
                response = set_reminder(reminder, time) # type: ignore
                speak(response)
            else:
                response = "Sorry, I couldn't understand the reminder. Please try again."
                speak(response)
        elif "send email" in command:
            response = send_email(recipient="john@example.com", subject="Subject", body="Body")
        elif "tell a joke" in command:
            response = tell_joke()
        elif "make whatsapp call" in command:
            contact_match = re.search("call (.+) on whatsapp", command)
            if contact_match:
                contact = contact_match.group(1)
                response = make_whatsapp_call(contact) # type: ignore
            else:
                response = "Sorry, I couldn't understand the contact. Please try again."
                speak(response)
        elif "exit" in command:
            response = "Goodbye! Have a great day."
            speak(response)
            exit()
        elif "take note" in command:
            note = re.search("take note (.+)", command).group(1)
            response = take_note(note)
        elif "show notes" in command:
            response = show_notes()
        elif "news" in command:
            response = get_news()
        elif "motivation" in command:
            response = get_motivational_quote()
        elif "timer" in command:
            timer_match = re.search("timer for (.+) minutes", command)
            if timer_match:
                minutes = int(timer_match.group(1))
                response = set_timer(minutes)
            else:
                response = "Sorry, I couldn't understand the duration. Please try again."
                speak(response)
        elif "math" in command:
            math_operation = re.search("math (.+)", command).group(1)
            result = eval(math_operation)
            response = f"The solution for this problem is {result}"
            speak(response)
        elif "define" in command:
            word = re.search("define (.+)", command).group(1)
            response = define_word(word)
        elif "play" in command:
            song = re.search("play (.+)", command).group(1)
            response = play_music(song)
        else:
            response = "Sorry, I can't help with that."
            speak(response)
    else:
        response = "No command recognized."
        speak(response)

    log_conversation(command, response, emotion)
    return response

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on Google."

def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "pune",
        "appid": "64de586459821453dfe08c1c72939119",
        "units": "metric"  # Changed to metric units
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather is {weather_description} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, I couldn't fetch the weather information."

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
        return "Email sent successfully."
    except Exception as e:
        return f"Sorry, there was an error sending the email: {e}"

def tell_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        joke = response.json()["joke"]
        speak(joke)
        return joke
    else:
        return "Sorry, I couldn't fetch a joke at the moment."

def take_note(note):
    notes_file = "notes.json"
    if os.path.exists(notes_file):
        with open(notes_file, "r") as file:
            notes = json.load(file)
    else:
        notes = []

    notes.append({"note": note, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    with open(notes_file, "w") as file:
        json.dump(notes, file, indent=4)

    return "Note taken."

def show_notes():
    notes_file = "notes.json"
    if os.path.exists(notes_file):
        with open(notes_file, "r") as file:
            notes = json.load(file)
        if notes:
            note_list = "\n".join([f"{note['timestamp']}: {note['note']}" for note in notes])
            return f"Here are your notes:\n{note_list}"
        else:
            return "You don't have any notes yet."
    else:
        return "You don't have any notes yet."

def get_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",
        "apiKey": "ebc33b48452e42e48c3bb30fc7eb9a05"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "ok":
        speak("Here are the top news headlines:")
        news_text = "Here are the top news headlines:\n"
        for article in data["articles"][:5]:
            speak(article["title"])
            news_text += article["title"] + "\n"
        return news_text
    else:
        return "Sorry, I couldn't fetch the news at the moment."

def get_motivational_quote():
    url = "https://type.fit/api/quotes"
    response = requests.get(url)
    if response.status_code == 200:
        quotes = response.json()
        quote = random.choice(quotes)
        speak(f"Here is a motivational quote for you: {quote['text']} by {quote.get('author', 'Unknown')}")
        return f"Here is a motivational quote for you: {quote['text']} by {quote.get('author', 'Unknown')}"
    else:
        return "Sorry, I couldn't fetch a quote at the moment."

def set_timer(minutes):
    speak(f"Setting a timer for {minutes} minutes.")
    time.sleep(minutes * 60)
    speak("Time's up!")
    return "Timer is up!"

def solve_math(math_operation):
    try:
        result = eval(math_operation)
        return f"The solution for this problem is {result}"
    except Exception as e:
        return f"Sorry, I couldn't calculate that. Error: {e}"

def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        word_definition = data["meanings"][0]["definitions"][0]["definition"]
        return f"The definition of {word} is: {word_definition}"
    else:
        return f"Sorry, I couldn't find the definition for {word}."

def play_music(song):
    url = f"https://api.deezer.com/search?q={song}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["total"] > 0:
            song_url = data["data"][0]["preview"]
            webbrowser.open(song_url)
            return "Playing the song."
        else:
            return "Sorry, I couldn't find that song."
    else:
        return "Sorry, I couldn't play the song."

def get_user_input():
    user_input = input("User (Text): ")
    return user_input

def main():
    while True:
        command = listen()
        if not command:
            command = get_user_input()
        response = process_command(command)

# Main loop
if __name__ == "__main__":
    main()