from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    SetMicrophoneStatus,
    GetMicrophoneStatus,
    GetAssistantStatus)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.utils import AnswerModifier, QueryModifier
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to important directories
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FRONTEND_FILES_DIR = os.path.join(BASE_DIR, 'Frontend', 'Files')
BACKEND_DIR = os.path.join(BASE_DIR, 'Backend')

# Define paths to specific files
CHAT_LOG_PATH = os.path.join(DATA_DIR, 'ChatLog.json')
DATABASE_PATH = os.path.join(FRONTEND_FILES_DIR, 'Database.data')
RESPONSE_PATH = os.path.join(FRONTEND_FILES_DIR, 'Response.data')
IMAGE_GENERATION_DATA_PATH = os.path.join(FRONTEND_FILES_DIR, 'ImageGeneration.data')
IMAGE_GENERATION_SCRIPT_PATH = os.path.join(BACKEND_DIR, 'ImageGeneration.py')

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
DefaultMessage = f'''{Username}:Hello {AssistantName},How are yoU?
{AssistantName}: Welcome {Username}. I am doing well. How may I help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def TempDirectoryPath(filename):
    return os.path.join(FRONTEND_FILES_DIR, filename)

def ShowDefaultChatIfNoChats():
    with open(CHAT_LOG_PATH, "r", encoding='utf-8') as File:
        if len(File.read()) < 5:
            with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
                file.write("")
            with open(RESPONSE_PATH, 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)

def ReadChatLogJson():
    with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User:{entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant:{entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", AssistantName + " ")
    with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    with open(DATABASE_PATH, "r", encoding='utf-8') as File:
        Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        with open(RESPONSE_PATH, "w", encoding='utf-8') as File:
            File.write(result)

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}:{Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision:{Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    if ImageExecution == True:
        with open(IMAGE_GENERATION_DATA_PATH, "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:
            p1 = subprocess.Popen(['python', IMAGE_GENERATION_SCRIPT_PATH],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            subprocesses.append(p1)

        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:
        SetAssistantStatus("Searching... ")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{AssistantName}:{Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                SetMicrophoneStatus("Answering...")
                os._exit(1)

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()

        else:
            AIStatus = GetAssistantStatus()

            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()


