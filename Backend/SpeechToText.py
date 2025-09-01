from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
from .utils import QueryModifier

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to important directories
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FRONTEND_FILES_DIR = os.path.join(BASE_DIR, 'Frontend', 'Files')
VOICE_HTML_PATH = os.path.join(DATA_DIR, 'Voice.html')
STATUS_DATA_PATH = os.path.join(FRONTEND_FILES_DIR, 'Status.data')

env_vars = dotenv_values(".env") 
InputLanguage = env_vars.get("InputLanguage")
#print("Loaded input language:", InputLanguage)  # ✅ Debug print

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '<<LANG>>';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = HtmlCode.replace("<<LANG>>", InputLanguage)  # ✅ Reliable replacement

with open(VOICE_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

Link = f"file:///{VOICE_HTML_PATH}"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def SetAssistantStatus(Status):
    with open(STATUS_DATA_PATH, "w", encoding="utf-8") as file:
        file.write(Status)
        
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    driver.get(Link)
    driver.find_element(by=By.ID, value="start").click()
    
    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text
            
            if Text:
                driver.find_element(by=By.ID, value="end").click()
                
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating")
                    return QueryModifier(UniversalTranslator(Text))
                
        except Exception as e:
            pass

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)
