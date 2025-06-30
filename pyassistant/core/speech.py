import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time
from googlesearch import search
import openai
import os
from dotenv import load_dotenv

# ================= CONFIGURATION =================
# Load environment variables (create .env file)
load_dotenv()
OPENAI_API_KEY = os.getenv("d604d586-5f4d-4366-b92d-aaa42dabf779")  # Set in .env or replace directly

openai.api_key = OPENAI_API_KEY


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            speak("Network error.")
            return None


def gpt_query(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"AI Error: {str(e)}"


def search_web(query):
    try:
        result = list(search(query, num=1, stop=1, pause=2))
        return result[0] if result else "No results found."
    except:
        return "Web search failed."


reminders = []

def set_reminder(reminder_text, delay_seconds):
    reminders.append((reminder_text, time.time() + delay_seconds))
    return f"Reminder set for {delay_seconds} seconds."


def process_command(command):
    command = command.lower()

    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    elif 'date' in command:
        current_date = datetime.date.today().strftime("%B %d, %Y")
        return f"Today's date is {current_date}"

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com ")
        return "Opening YouTube..."

    elif 'open google' in command:
        webbrowser.open("https://www.google.com ")
        return "Opening Google..."

    elif 'set reminder' in command:
        try:
            parts = command.split("for")[1].strip().split()
            seconds = int(parts[0])
            text = " ".join(parts[2:])
            return set_reminder(text, seconds)
        except:
            return "Please specify how many seconds until the reminder."

    elif 'exit' in command or 'stop' in command:
        return "Goodbye!"

    else:
        # Try GPT first
        gpt_response = gpt_query(command)
        if "error" not in gpt_response.lower():
            return gpt_response
        else:
            return search_web(command)

# ================= MAIN LOOP =================
speak("Hi, I'm PyAssistant. How can I help you today?")

while True:
    command = listen()
    if not command:
        continue

    print(f"You said: {command}")
    response = process_command(command)

    if response == "Goodbye!":
        speak(response)
        break

    elif response.startswith("http"):
        speak("I found this link for you.")
        print("Result:", response)

    else:
        speak(response)
        print("Response:", response)