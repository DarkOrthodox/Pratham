from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import threading
import time

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to important directories
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FRONTEND_FILES_DIR = os.path.join(BASE_DIR, 'Frontend', 'Files')
WAKE_WORD_HTML_PATH = os.path.join(DATA_DIR, 'WakeWord.html')
STATUS_DATA_PATH = os.path.join(FRONTEND_FILES_DIR, 'Status.data')
WAKE_WORD_STATUS_PATH = os.path.join(FRONTEND_FILES_DIR, 'WakeWordMode.data')

env_vars = dotenv_values(".env") 
InputLanguage = env_vars.get("InputLanguage")

# HTML for wake word detection
WakeWordHtml = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Wake Word Detection</title>
</head>
<body>
    <button id="start" onclick="startWakeWordDetection()">Start Wake Word Detection</button>
    <button id="stop" onclick="stopWakeWordDetection()">Stop Wake Word Detection</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let isListening = false;

        function startWakeWordDetection() {
            if (isListening) return;
            
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '<<LANG>>';
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent = transcript;
                
                // Check for wake word "Pratham" in various forms
                const lowerTranscript = transcript.toLowerCase();
                if (lowerTranscript.includes('pratham') || 
                    lowerTranscript.includes('प्रथम') || 
                    lowerTranscript.includes('pratam') ||
                    lowerTranscript.includes('prathum')) {
                    output.textContent = "WAKE_WORD_DETECTED:" + transcript;
                }
            };

            recognition.onend = function() {
                if (isListening) {
                    setTimeout(() => {
                        recognition.start();
                    }, 100);
                }
            };
            
            recognition.onerror = function(event) {
                if (isListening) {
                    setTimeout(() => {
                        recognition.start();
                    }, 1000);
                }
            };

            isListening = true;
            recognition.start();
        }

        function stopWakeWordDetection() {
            isListening = false;
            if (recognition) {
                recognition.stop();
            }
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

WakeWordHtml = WakeWordHtml.replace("<<LANG>>", InputLanguage)

with open(WAKE_WORD_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(WakeWordHtml)

Link = f"file:///{WAKE_WORD_HTML_PATH}"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Global variables for wake word detection
wake_word_driver = None
wake_word_active = False

def GetWakeWordMode():
    """Check if wake word mode is enabled"""
    try:
        with open(WAKE_WORD_STATUS_PATH, "r", encoding='utf-8') as file:
            status = file.read().strip()
        return status == "True"
    except FileNotFoundError:
        SetWakeWordMode(False)
        return False

def SetWakeWordMode(enabled):
    """Set wake word mode on/off"""
    with open(WAKE_WORD_STATUS_PATH, "w", encoding='utf-8') as file:
        file.write("True" if enabled else "False")

def SetAssistantStatus(Status):
    with open(STATUS_DATA_PATH, "w", encoding="utf-8") as file:
        file.write(Status)

def InitializeWakeWordDetection():
    """Initialize the wake word detection browser instance"""
    global wake_word_driver
    
    try:
        service = Service(ChromeDriverManager().install())
        wake_word_driver = webdriver.Chrome(service=service, options=chrome_options)
        wake_word_driver.get(Link)
        return True
    except Exception as e:
        print(f"Error initializing wake word detection: {e}")
        return False

def StartWakeWordDetection():
    """Start continuous wake word detection"""
    global wake_word_driver, wake_word_active
    
    if not wake_word_driver:
        if not InitializeWakeWordDetection():
            return False
    
    try:
        wake_word_driver.find_element(by=By.ID, value="start").click()
        wake_word_active = True
        return True
    except Exception as e:
        print(f"Error starting wake word detection: {e}")
        return False

def StopWakeWordDetection():
    """Stop wake word detection"""
    global wake_word_driver, wake_word_active
    
    try:
        if wake_word_driver and wake_word_active:
            wake_word_driver.find_element(by=By.ID, value="stop").click()
            wake_word_active = False
        return True
    except Exception as e:
        print(f"Error stopping wake word detection: {e}")
        return False

def CheckForWakeWord():
    """Check if wake word was detected"""
    global wake_word_driver
    
    if not wake_word_driver or not wake_word_active:
        return False
        
    try:
        text = wake_word_driver.find_element(by=By.ID, value="output").text
        
        if text and "WAKE_WORD_DETECTED:" in text:
            # Clear the output
            wake_word_driver.execute_script("document.getElementById('output').textContent = '';")
            return True
            
    except Exception as e:
        pass
    
    return False

def WakeWordDetectionLoop():
    """Main loop for wake word detection - runs in separate thread"""
    global wake_word_active
    
    while True:
        try:
            if GetWakeWordMode() and not wake_word_active:
                SetAssistantStatus("Wake word listening...")
                StartWakeWordDetection()
            elif not GetWakeWordMode() and wake_word_active:
                StopWakeWordDetection()
                SetAssistantStatus("Available...")
            
            if wake_word_active and CheckForWakeWord():
                # Wake word detected! Set microphone to active
                from Frontend.GUI import SetMicrophoneStatus
                SetMicrophoneStatus("True")
                SetAssistantStatus("Wake word detected!")
                time.sleep(0.5)  # Brief pause before processing
                
            time.sleep(0.1)  # Check every 100ms
            
        except Exception as e:
            print(f"Wake word detection error: {e}")
            time.sleep(1)

def CleanupWakeWordDetection():
    """Cleanup wake word detection resources"""
    global wake_word_driver
    
    try:
        if wake_word_driver:
            wake_word_driver.quit()
            wake_word_driver = None
    except Exception as e:
        print(f"Error cleaning up wake word detection: {e}")

if __name__ == "__main__":
    # Test wake word detection
    SetWakeWordMode(True)
    InitializeWakeWordDetection()
    
    detection_thread = threading.Thread(target=WakeWordDetectionLoop, daemon=True)
    detection_thread.start()
    
    try:
        while True:
            if CheckForWakeWord():
                print("Wake word 'Pratham' detected!")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping wake word detection...")
        CleanupWakeWordDetection()
