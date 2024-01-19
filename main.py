import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os

def say(text, speed=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

def takeInput():
    r = sr.Recognizer()
    with sr.Microphone() as source:   #speech recognition using microphone
        r.pause_threshold = 0.8
        audio = r.listen(source, timeout=5)    #audio pura listel hoke bnegi
        print(audio)

        try:
            query = r.recognize_google(audio, language="en-in")   #audio ko recognize krenge toh query bnegi
            print(f"{query}")
            return query
        except Exception as e:
            return "Error occurred"

if __name__ == '__main__':
    say("I am Jarvis A.I")
    print("listening")
    query = takeInput()

    sites = [["google", "https://www.google.com/"],
             ["youtube", "https://www.youtube.com/"],
             ["chatgpt", "https://openai.com/"]]

    for site in sites:
        print(site)
        if f"open {site[0].lower()}" in query.lower():
            say(f"opening {site[0]} sir...")
            webbrowser.open(site[1])
            break

        elif "open music" in query:
            musicPath = r"C:\Users\LENOVO\Downloads\music.mp3"

        if os.path.exists(musicPath):
            if sys.platform == "win32":
                subprocess.Popen(["start", musicPath], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", musicPath])
            else:
                subprocess.Popen(["xdg-open", musicPath])
        else:
            say("Music file not found.")

