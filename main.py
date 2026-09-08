import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai

# -------------------------
# CONFIGURATION
# -------------------------
NEWS_API_KEY = "95242417ed364467be81abdc1da2c53e"
GEMINI_API_KEY = "AIzaSyDSKLcWL-NRuLhGIZt6BLZPFFH4fGQzJkA"

genai.configure(api_key=GEMINI_API_KEY)

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------
# GEMINI CHAT FUNCTION
# -------------------------
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry boss, Gemini is not responding right now."

# -------------------------
# COMMAND PROCESSOR
# -------------------------
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    # 🎵 PLAY MUSIC (IMPROVED SEARCH)
    elif c.startswith("play"):
        song = c.replace("play", "").strip()

        found = False
        for key in musicLibrary.music:
            if song in key.lower():
                webbrowser.open(musicLibrary.music[key])
                found = True
                break

        if not found:
            speak("Playing on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    # 📰 NEWS
    elif "news" in c:
        speak("Fetching the latest news for you, boss...")
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
            r = requests.get(url)

            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])

                if articles:
                    headlines = []

                    for a in articles[:5]:
                        title = a.get("title", "No title")
                        headlines.append(title)
                        print("📰", title)
                        speak(title)

                    # Gemini summary
                    summary = ask_gemini(
                        "Summarize these news headlines in short: " + ", ".join(headlines)
                    )
                    speak("Here is a quick summary")
                    speak(summary)

                else:
                    speak("No news available right now.")
            else:
                speak("Failed to fetch news.")

        except Exception as e:
            print(e)
            speak("Something went wrong while fetching news.")

    # 🤖 GEMINI DEFAULT CHAT
    else:
        speak("Let me think...")
        reply = ask_gemini(c)
        print("Gemini:", reply)
        speak(reply)

# -------------------------
# MAIN PROGRAM LOOP
# -------------------------
if __name__ == "__main__":
    speak("Initializing Jarvis with Gemini AI...")

    while True:
        command = input("You: ")

        if command.lower() in ["exit", "stop"]:
            speak("Goodbye bhai")
            break

        processCommand(command)