import speech_recognition as sr  
import pyttsx3  
import datetime
import requests
import webbrowser
import re
import smtplib
from email.message import EmailMessage

# Voice assistant setup
recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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
                set_reminder(reminder, time)   # type: ignore
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
                make_whatsapp_call(contact) # type: ignore
            else:
                speak("Sorry, I couldn't understand the contact. Please try again.")
        elif "exit" in command:
            speak("Goodbye! Have a great day.")
            exit()
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
        "units": "metric"
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

# Add a button to activate the voice assistant
def activate_voice_assistant():
    speak("Hi, I'm your college assistant. How can I help you?")
    while True:
        voice_query = listen()
        if voice_query:
            process_command(voice_query)
        else:
            text_query = input("Enter a command: ")
            process_command(text_query)

activate_voice_assistant()
