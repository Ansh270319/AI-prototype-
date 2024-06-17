import tkinter as tk
from tkinter import messagebox
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import webbrowser

# Load the sentiment analysis model and tokenizer
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
    else:
        messagebox.showwarning("Warning", "Please enter text to analyze.")

def open_website():
    """Open the website URL entered in the GUI"""
    url = website_entry.get().strip()
    if url:
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {url}. Error: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter a website URL.")

# Create the main window
root = tk.Tk()
root.title("AI Application")

# Customize the GUI
root.configure(bg="blue")
root.geometry("1600x860")

# Create widgets
text_label = tk.Label(root, text="Enter text:", bg="lightgray", font=("Arial", 12))
text_entry = tk.Text(root, height=5, width=50, bg="white", fg="black", font=("Arial", 12))

analyze_button = tk.Button(root, text="Analyze Sentiment", command=analyze_sentiment, bg="blue", fg="white", font=("Arial", 12))

website_label = tk.Label(root, text="Enter website URL:", bg="lightgray", font=("Arial", 12))
website_entry = tk.Entry(root, width=50, bg="white", fg="black", font=("Arial", 12))

open_button = tk.Button(root, text="Open Website", command=open_website, bg="green", fg="white", font=("Arial", 12))

# Layout widgets
text_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
analyze_button.grid(row=2, column=0, padx=10, pady=10)

website_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
website_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
open_button.grid(row=5, column=0, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()