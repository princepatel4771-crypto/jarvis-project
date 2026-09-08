import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
from openai import OpenAI

# -------------------- SETUP --------------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# 👉 Apni OpenAI API key yaha daal
client = OpenAI(api_key="z6fNxsZJvZRhWHhzGtqzdDJB4tD74A")

# 👉 Apni News API key yaha daal
NEWS_API_KEY = "95242417ed364467be81abdc1da2c53e"

# -------------------- SPEAK FUNCTION --------------------
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------- AI FUNCTION --------------------
def aiProcess(command):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short answers."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "AI error aa gaya"

# -------------------- COMMAND PROCESS --------------------
def processCommand(command):
    command = command.lower()
    print("Command:", command)

    if "open google" in command:
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    elif "play" in command:
        song = command.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    elif "news" in command:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
            r = requests.get(url)
            data = r.json()

            articles = data.get("articles", [])[:5]

            if not articles:
                speak("Koi news nahi mili")
                return

            speak("Top news suno")
            for article in articles:
                speak(article["title"])

        except:
            speak("News fetch nahi ho paayi")

    elif "exit" in command or "stop" in command:
        speak("Goodbye bhai")
        exit()

    else:
        # AI se answer
        response = aiProcess(command)
        speak(response)

# -------------------- MAIN LOOP --------------------
if __name__ == "__main__":
    speak("Jarvis starting...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)

                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

                print("You said:", word)

                if "jarvis" in word.lower():
                    speak("Yes")

                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(audio)

                        processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout...")

        except sr.UnknownValueError:
            print("Samajh nahi aaya...")

        except Exception as e:
            print("Error:", e)