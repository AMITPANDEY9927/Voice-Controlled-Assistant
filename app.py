from flask import Flask, render_template, jsonify, request
import webbrowser
import threading
import speech_recognition as sr
import pyttsx3
import subprocess
import queue
import time
import re

app = Flask(__name__)

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)
tts_engine.setProperty('volume', 0.9)

listening = False
command_mode = False
message_queue = queue.Queue()  # For logging messages

# Websites and apps
websites = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'amazon': 'https://www.amazon.com',
    'facebook': 'https://www.facebook.com',
    'linkedin': 'https://www.linkedin.com',
    'github': 'https://www.github.com',
    'netflix': 'https://www.netflix.com',
    'twitter': 'https://www.twitter.com',
    'instagram': 'https://www.instagram.com',
    'reddit': 'https://www.reddit.com',
    'stackoverflow': 'https://stackoverflow.com',
    'gmail': 'https://mail.google.com',
    'whatsapp': 'https://web.whatsapp.com',
    'quora': 'https://www.quora.com',
    'pinterest': 'https://www.pinterest.com'
}

applications = {
    'calculator': 'calc.exe',
    'notepad': 'notepad.exe',
    'paint': 'mspaint.exe',
    'word': 'winword.exe',
    'excel': 'excel.exe',
    'powerpoint': 'powerpnt.exe'
}

def log_message(text):
    """Log message to both console and message queue."""
    print(text)
    message_queue.put(text)

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            log_message(f"TTS Error: {e}")
        tts_queue.task_done()

tts_queue = queue.Queue()
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    log_message(f"JARVIS: {text}")
    tts_queue.put(text)

def open_website(url):
    webbrowser.open(url)

def open_application(app_path):
    subprocess.Popen(app_path)

def execute_command(command):
    global command_mode
    command = command.lower().strip()
    log_message(f"Executing command: {command}")
    
    for key, url in websites.items():
        if f'open {key}' in command:
            speak(f"Opening {key.capitalize()}")
            threading.Thread(target=open_website, args=(url,), daemon=True).start()
            command_mode = False
            return
    
    for key, app_path in applications.items():
        if f'open {key}' in command:
            try:
                speak(f"Opening {key.capitalize()}")
                threading.Thread(target=open_application, args=(app_path,), daemon=True).start()
            except Exception as e:
                log_message(f"Error opening app: {e}")
                speak(f"Sorry sir, I couldn't open {key}")
            command_mode = False
            return
    
    if any(word in command for word in ['hello', 'hi', 'hey']):
        speak("Hello sir! How can I help you?")
    elif 'how are you' in command:
        speak("I am functioning perfectly sir. How can I assist you?")
    elif any(word in command for word in ['thank you', 'thanks']):
        speak("You're welcome sir! Anything else I can help with?")
    elif 'stop listening' in command or 'sleep' in command:
        speak("Going to sleep sir. Say 'Hey Jarvis' to wake me up.")
        command_mode = False
    elif 'time' in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    else:
        speak("Command not recognized")
    command_mode = False


def listen_for_command():
    global command_mode
    command_mode = True
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            speak("I'm listening sir...")
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            log_message(f"Heard command: {command}")
            execute_command(command)
        except sr.WaitTimeoutError:
            speak("I didn't hear any command sir")
            command_mode = False
        except sr.UnknownValueError:
            speak("Sorry sir, I did not understand that")
            command_mode = False
        except Exception as e:
            log_message(f"Error in listen_for_command: {e}")
            speak("There was an error processing your command")
            command_mode = False

def listen_loop():
    global listening, command_mode
    speak("JARVIS is now online and listening for your commands sir")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while listening:
            try:
                if not command_mode:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio).lower()
                    log_message(f"Heard: {command}")
                    
                    if 'jarvis' in command:
                        if re.search(r'\bhey jarvis\b', command) or re.search(r'\bhello jarvis\b', command):
                            speak("Yes sir, how can I help you?")
                            listen_for_command()
                        elif re.search(r'^jarvis$', command) or re.search(r'\bjarvis\b', command):
                            speak("Yes sir?")
                            listen_for_command()
                else:
                    time.sleep(0.1)
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                log_message(f"Error in listen_loop: {e}")
                time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    global listening
    if not listening:
        listening = True
        threading.Thread(target=listen_loop, daemon=True).start()
        return jsonify({"status": "success", "message": "Started listening"})
    return jsonify({"status": "error", "message": "Already listening"})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global listening
    listening = False
    return jsonify({"status": "success", "message": "Stopped listening"})

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"listening": listening, "command_mode": command_mode})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = []
    while not message_queue.empty():
        logs.append(message_queue.get())
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(debug=True, port=5001, threaded=True)
