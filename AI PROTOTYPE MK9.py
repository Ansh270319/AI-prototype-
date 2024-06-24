import speech_recognition as sr  
import pyttsx3  
import datetime
import requests
import webbrowser
import re
import time
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, ttk
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification  
import torch  

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
        print(f"User: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that. Can you please repeat?")
        return listen()
    except sr.RequestError:
        speak("Sorry, I'm facing some technical issues. Please try again later.")
        return None

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def open_website(query):
    query = query.replace("open", "").strip()
    url = f"https://{query}"
    try:
        webbrowser.open(url)
    except webbrowser.Error as e:
        speak(f"Sorry, I couldn't open the website because of error: {e}")

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

def make_whatsapp_call(contact):
    # Assuming you have a way to make WhatsApp calls programmatically
    # This could involve using WhatsApp's API or an automation tool
    # For the sake of this example, we'll assume a function call like below
    call_contact(contact)
    speak(f"Calling {contact} on WhatsApp.")

def handle_query(query):
    if "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "weather" in query:
        get_weather()
    elif "search" in query:
        search_query = re.search("search (.+)", query).group(1)
        search_web(search_query)
    elif "reminder" in query and "at" in query:
        reminder_match = re.search("reminder (.+) at (.+)", query)
        if reminder_match:
            reminder = reminder_match.group(1)
            time = reminder_match.group(2)
            set_reminder(reminder, time)  
            speak("Reminder set.")
        else:
            speak("Sorry, I couldn't understand the reminder. Please try again.")
    elif "send email" in query:
        send_email(recipient="john@example.com", subject="Subject", body="Body")
    elif "tell a joke" in query:
        tell_joke()
    elif "make whatsapp call" in query:
        contact_match = re.search("call (.+) on whatsapp", query)
        if contact_match:
            contact = contact_match.group(1)
            make_whatsapp_call(contact)
        else:
            speak("Sorry, I couldn't understand the contact. Please try again.")
    elif "exit" in query:
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("Sorry, I can't help with that.")

# Sentiment analysis setup
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment():
    """Analyze the sentiment of the text entered in the GUI"""
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        sentiment = "POSITIVE" if torch.argmax(probabilities) == 1 else "NEGATIVE"
        score = probabilities[0][torch.argmax(probabilities)].item()
        messagebox.showinfo("Sentiment Analysis Result", f"Sentiment: {sentiment}, Score: {score:.2f}")
        speak(f"The sentiment is {sentiment} with a score of {score:.2f}")
    else:
        messagebox.showwarning("Warning", "Please enter text to analyze.")
        speak("Please enter text to analyze.")

def open_website_gui():
    """Open the website URL entered in the GUI using the selected browser"""
    url = website_entry.get().strip()
    browser_choice = browser_var.get()
    if url:
        try:
            if browser_choice == "Default":
                webbrowser.open(url)
            elif browser_choice == "Chrome":
                webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(url)
            elif browser_choice == "Edge":
                webbrowser.get("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s").open(url)
            elif browser_choice == "Brave":
                webbrowser.get("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s").open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {url}. Error: {e}")
            speak(f"Failed to open {url}. Error: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter a website URL.")
        speak("Please enter a website URL.")

# Create the main window
root = tk.Tk()
root.title("AI Application")

# Customize the GUI
root.configure(bg="cyan")
root.geometry("800x600")

# Create widgets
text_label = tk.Label(root, text="Enter text:", bg="lightgray", font=("Arial", 12))
text_entry = tk.Text(root, height=5, width=50, bg="white", fg="black", font=("Arial", 12))

analyze_button = tk.Button(root, text="Analyze Sentiment", command=analyze_sentiment, bg="blue", fg="white", font=("Arial", 12))

website_label = tk.Label(root, text="Enter website URL:", bg="lightgray", font=("Arial", 12))
website_entry = tk.Entry(root, width=50, bg="white", fg="black", font=("Arial", 12))

browser_label = tk.Label(root, text="Select Browser:", bg="lightgray", font=("Arial", 12))
browser_var = tk.StringVar(value="Default")
browser_menu = ttk.Combobox(root, textvariable=browser_var, values=["Default", "Chrome", "Firefox", "Edge"], state="readonly")

open_button = tk.Button(root, text="Open Website", command=open_website_gui, bg="green", fg="white", font=("Arial", 12))

# Layout widgets
text_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
analyze_button.grid(row=2, column=0, padx=10, pady=10)

website_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
website_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

browser_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
browser_menu.grid(row=6, column=0, padx=10, pady=10)

open_button.grid(row=7, column=0, padx=10, pady=10)

# Add a button to activate the voice assistant
def activate_voice_assistant():
    speak("Hi, I'm your college assistant. How can I help you?")
    while True:
        query = listen()
        if query:
            if "open" in query:
                open_website(query)
            else:
                handle_query(query)
        time.sleep(1)

activate_button = tk.Button(root, text="Activate Voice Assistant", command=activate_voice_assistant, bg="purple", fg="white", font=("Arial", 12))
activate_button.grid(row=8, column=0, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
