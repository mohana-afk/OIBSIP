import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import importlib

try:
    pyjokes = importlib.import_module("pyjokes")
except ImportError:
    pyjokes = None

engine = pyttsx3.init()

def speak(text):
    chat.insert(tk.END, f"Nova: {text}\n")
    chat.see(tk.END)

    engine.say(text)
    engine.runAndWait()

def process_command(command):
    command = command.lower()

    if "hello" in command or "hi" in command or "hey" in command:
        speak("Hello!")

    elif "time" in command:
        current = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current}")

    elif "date" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today}")

    elif "your name" in command:
        speak("My name is Nova. I am your AI assistant.")

    elif "who created you" in command:
        speak("I was created by Mohana Sri Sai Deepa.")

    elif "thank you" in command:
        speak("You're welcome.")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()

        try:
            result = wikipedia.summary(topic, sentences=2, auto_suggest=True)
            speak(result)

        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Please be more specific. For example {e.options[0]}")

        except:
            speak("I could not find that topic.")

    elif "youtube" in command:
        topic = command.replace("youtube", "").strip()

        if topic == "":
            speak("Please tell me what to search on YouTube.")
        else:
            pywhatkit.playonyt(topic)
            speak("Opening YouTube")

    elif "search" in command:
        topic = command.replace("search", "").strip()

        if topic == "":
            speak("Please tell me what to search.")
        else:
            pywhatkit.search(topic)
            speak("Searching Google")

    elif "save note" in command:
        note = command.replace("save note", "").strip()

        with open("notes.txt", "a") as f:
            f.write(note + "\n")

        speak("Note saved.")
    
    elif "show notes" in command:
        try:
            with open("notes.txt", "r") as f:
                notes = f.read()

            if notes:
                speak(notes)
            else:
                speak("No notes found.")

        except:
            speak("No notes found.")

    elif "how are you" in command or "how r u" in command:
        speak("I am doing great. Thank you for asking.")

    elif "good morning" in command:
         speak("Good morning. Have a productive day.")

    elif "good night" in command:
         speak("Good night. Sleep well.")

    elif "bye" in command:
         speak("Goodbye.")
    
    elif "joke" in command:
         if pyjokes:
             speak(pyjokes.get_joke())
         else:
             speak("Joke feature is unavailable because pyjokes is not installed.")
    
    else:
         speak("Sorry, I don't understand.")
 

def send_text():
    user_text = entry.get()

    if user_text.strip() == "":
        return

    chat.insert(tk.END, f"You: {user_text}\n")

    process_command(user_text)

    entry.delete(0, tk.END)

def listen_voice():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            speak("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        command = recognizer.recognize_google(audio)

        chat.insert(tk.END, f"You: {command}\n")

        process_command(command)

    except Exception:
        speak("Could not recognize your voice.")

root = tk.Tk()
root.title("Nova AI Assistant")
root.geometry("800x650")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="NOVA AI ASSISTANT",
    font=("Arial", 24, "bold")
)
title.pack(pady=10)

title.config(
    bg="#1e1e1e",
    fg="cyan"
)

chat = scrolledtext.ScrolledText(
    root,
    width=80,
    height=20
)
chat.pack(pady=10, fill="both", expand=True)

chat.config(
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)

entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 12)
)
entry.pack(pady=10)

send_btn = tk.Button(
    root,
    text="Send",
    command=send_text,
    width=15
)
send_btn.pack(pady=5)

voice_btn = tk.Button(
    root,
    text="🎤 Speak",
    command=listen_voice,
    width=15
)
voice_btn.pack(pady=5)

speak("Welcome to Nova A I Assistant")

root.mainloop()