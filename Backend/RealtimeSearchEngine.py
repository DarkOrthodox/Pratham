from googlesearch import search
from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values
import os
from .utils import AnswerModifier

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to important directories
DATA_DIR = os.path.join(BASE_DIR, 'Data')
CHAT_LOG_PATH = os.path.join(DATA_DIR, 'ChatLog.json')

env_vars=dotenv_values(".env")

Username=env_vars.get("Username")
AssistantName=env_vars.get("AssistantName")
GroqAPIKey=env_vars.get("GroqAPIKey")

client=Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""


try:
    with open(CHAT_LOG_PATH,"r") as f:
        messages=load(f)
except:
    with open(CHAT_LOG_PATH,"w") as f:
        dump([],f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer=f"The search results for '{query}' are:\n[start]\n"
    for i in results:
       Answer+=f"Title: {i.title}\nDescription: {i.description}\n\n"
       
    Answer+="[end]"
    return Answer

SystemChatBot=[
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    data=""
    current_date_time=datetime.datetime.now()
    day=current_date_time.strftime("%A")
    date=current_date_time.strftime("%d")
    month=current_date_time.strftime("%B")
    year=current_date_time.strftime("%Y")
    hour=current_date_time.strftime("%H")
    minute=current_date_time.strftime("%M")
    second=current_date_time.strftime("%S")
    data +=f"Use This Real-Time Information: if needed:\n"
    data +=f"Day: {day}\n"
    data +=f"Date: {date}\n"
    data +=f"Month: {month}\n"
    data +=f"Year: {year}\n"
    data +=f"Hour: {hour}\n, {minute}\n, {second}\n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    with open(CHAT_LOG_PATH,"r") as f:
        messages=load(f)
    messages.append({"role": "user", "content": f"{prompt}"})
    
    SystemChatBot.append({"role": "user", "content": GoogleSearch(prompt)})
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=SystemChatBot + [{"role": "user", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    
    Answer = ""
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
            
    Answer=Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
        
    with open(CHAT_LOG_PATH,"w") as f:
        dump(messages, f, indent=4)
            
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)
    
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
           