
# 📘 JARVIS Voice Assistant

**JARVIS Voice Assistant** is a Python-based voice assistant powered by Flask, SpeechRecognition, and pyttsx3 libraries. It allows users to interact via voice commands to open popular websites and applications through a web interface.

This project demonstrates how voice recognition and text-to-speech functionality can be integrated into a web application for an interactive user experience.

## ✅ Features

✔ Recognizes voice commands such as "Open YouTube", "Open calculator", etc.  
✔ Opens websites like Google, YouTube, Amazon, and more.  
✔ Launches applications like Notepad, Calculator, and Word.  
✔ Provides real-time feedback in a web interface.  
✔ Uses Python libraries for speech recognition and text-to-speech.  
✔ Simple, extendable, and modular structure.

## 📂 Folder Structure

```
JARVIS-Voice-Assistant/
│
├── app.py                   # Main Flask backend application
├── requirements.txt         # List of required Python libraries
├── README.md                # This documentation file
│
├── templates/               # HTML templates for the web interface
│   └── index.html           # The main HTML file for the user interface
│
├── static/                  # Static files like CSS and JavaScript
│   └── style.css            # CSS styles for the web interface
│
└── JARVIS_Voice_Assistant_Report.docx   # Project report file
```

## 🛠 Libraries / Dependencies

You need the following Python libraries:

| Library            | Version   | Purpose                        |
|-------------------|-----------|--------------------------------|
| Flask             | 2.3.2     | Web framework                   |
| Flask-Cors        | 3.0.10    | Handles cross-origin requests  |
| SpeechRecognition | 3.8.1     | Recognizes voice commands      |
| pyttsx3           | 2.90      | Converts text to speech        |
| pypiwin32         | 223       | Windows API support for TTS    |

## ✅ How to Install

1. **Clone the repository** (or download the files):

   ```bash
   git clone <repository-url>
   cd JARVIS-Voice-Assistant
   ```

2. **Create a Python virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

3. **Activate the environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required libraries using pip:**

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the necessary libraries mentioned in `requirements.txt` including Flask, SpeechRecognition, pyttsx3, and others.

## ▶ How to Run

1. Ensure your microphone is connected and working.

2. Run the Flask application:

   ```bash
   python app.py
   ```

3. Open your web browser and go to:

   ```
   http://127.0.0.1:5001/
   ```

4. Click **Start Listening**, and say commands like:

   - "Open YouTube"
   - "Open Google"
   - "Open calculator"

5. View the recognized commands and responses on the webpage.

## 📂 About HTML and CSS

- The **templates/index.html** file is responsible for the web interface layout, buttons, status display, and examples of commands.
- The **static/style.css** file styles the web interface with colors, animations, and layout adjustments for better user experience.
- These files work together with Flask to provide a dynamic and interactive platform where the assistant listens for commands and displays the output in real-time.

## ⚙ Notes

✔ Works best on Windows because `pyttsx3` with `pypiwin32` is configured for it.  
✔ Requires microphone access permissions in the browser.  
✔ Ensure no other application is using the microphone.

## 📈 Future Improvements

- Add more commands for browsing and system tasks.
- Integrate AI models for smarter responses.
- Improve speech recognition accuracy and handle errors more gracefully.

Feel free to explore, contribute, and enhance this project!
