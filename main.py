import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os
import datetime
import smtplib
import requests
import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

def say(text, speed=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

def takeInput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source, timeout=5)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"{query}")
            return query
        except Exception as e:
            return "Error occurred"

def getWeather(city):
    api_key = "dab60c0c204a0f2dd6fe19fcb8abb280"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]["description"]
        temperature = main["temp"] - 273.15
        weather_report = f"The temperature in {city} is {temperature:.2f}°C with {weather}."
        return weather_report
    else:
        return "City not found."

def sendEmail(to, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("saifyssk04@gmail.com", "Saify@4565")
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail("saifyssk04@gmail.com", to, message)
    server.quit()

def writeLetter(topic):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write a formal letter about {topic}.",
        max_tokens=200
    )
    letter = response.choices[0].text.strip()
    return letter

if __name__ == '__main__':
    say("I am Jarvis A.I")
    print("listening")
    query = takeInput()

    if "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"sir the time is {time}")

    elif "open music" in query:
        say("Opening music sir")
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

    sites = [["google", "https://www.google.com/"],
             ["youtube", "https://www.youtube.com/"],
             ["chatgpt", "https://openai.com/"]]

    for site in sites:
        if f"open {site[0].lower()}" in query.lower():
            say(f"opening {site[0]} sir...")
            webbrowser.open(site[1])
            break

    if "open telegram" in query.lower():
        path = r'C:\Users\LENOVO\AppData\Roaming\Telegram Desktop\Telegram.exe'
        os.system(path)

    if "weather" in query.lower():
        say("Which city's weather would you like to know?")
        city = takeInput()
        weather_report = getWeather(city)
        say(weather_report)

    if "send email" in query.lower() or "send an email" in query.lower():
        try:
            say("What is the recipient's email address?")
            to = takeInput()
            say("What is the subject of the email?")
            subject = takeInput()
            say("What should I say in the email?")
            body = takeInput()
            sendEmail(to, subject, body)
            say("Email has been sent successfully.")
        except Exception as e:
            say("Sorry, I am not able to send the email at the moment.")

    if "to do list" in query.lower():
        todo_list = []
        while True:
            say("What would you like to add to your to-do list?")
            item = takeInput()
            if "stop" in item.lower():
                break
            todo_list.append(item)
            say(f"{item} has been added to your to-do list.")
        say("Here is your to-do list:")
        for item in todo_list:
            say(item)
    
    if "write a letter" in query.lower():
        say("What is the topic of the letter?")
        topic = takeInput()
        letter = writeLetter(topic)
        say("Here is your letter:")
        say(letter)
        print(letter)
