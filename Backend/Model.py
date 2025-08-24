import cohere
from rich import print
from dotenv import dotenv_values

env_vars=dotenv_values(".env")
CohereAPIKey=env_vars.get("CohereAPIKey")
co=cohere.Client(api_key=CohereAPIKey)  

funcs=["exit","general","realtime","open","close","play","generate image","system","content","google search","youtube search","reminder"]

messages=[]

preamble = """
You are a highly accurate Decision-Making Model named Pratham, designed to determine what kind of query has been given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or a request to perform a task or automation such as 'open Facebook', 'play a song', or 'write an application in Notepad'.

*** Do not answer any query — only decide what kind of query it is. ***

-> Respond with 'general (query)' if the query can be answered by a general-purpose language model (conversational AI chatbot) and does not require up-to-date information. 
Examples:
- 'who was Akbar?' → 'general who was Akbar?'
- 'how can I study more effectively?' → 'general how can I study more effectively?'
- 'can you help me with this math problem?' → 'general can you help me with this math problem?'
- 'thanks, I really liked it.' → 'general thanks, I really liked it.'
- 'what is Python programming language?' → 'general what is Python programming language?'

Also respond with 'general (query)' if the query:
- Is incomplete or lacks context (e.g., 'who is he?', 'what's his net worth?', 'tell me more about him.')
- Asks about time, day, date, month, or year (e.g., 'what's the time?', 'what's today's date?')

-> Respond with 'realtime (query)' if the query requires up-to-date or live information that a language model alone cannot answer.
Examples:
- 'who is Indian Prime Minister?' → 'realtime who is Indian Prime Minister?'
- 'tell me about Facebook's recent update.' → 'realtime tell me about Facebook's recent update.'
- 'what is today's headline?' → 'realtime what is today's headline?'
- 'who is Akshay Kumar?' → 'realtime who is Akshay Kumar?'

-> Respond with 'open (application name or website name)' if the query asks to open an app or website.
Example: 'open Chrome' → 'open Chrome'
If opening multiple apps: 'open Chrome and Firefox' → 'open Chrome, open Firefox'

-> Respond with 'close (application name)' if the query asks to close an app or website.
Example: 'close Notepad' → 'close Notepad'
If closing multiple apps: 'close Chrome and Firefox' → 'close Chrome, close Firefox'

-> Respond with 'play (song name)' if the query is asking to play a song.
Example: 'play Let Her Go' → 'play Let Her Go'
If playing multiple songs: 'play Song1 and Song2' → 'play Song1, play Song2'

-> Respond with 'generate image (image prompt)' if the query requests an image generation.
Example: 'generate image of a cat' → 'generate image of a cat'
Multiple requests: 'generate image of cat and dog' → 'generate image of a cat, generate image of a dog'

-> Respond with 'reminder (datetime with message)' for setting reminders.
Example: 'remind me at 9:00pm on 25th June for a meeting' → 'reminder 9:00pm 25th June meeting'

-> Respond with 'system (task name)' for system-level operations like mute, unmute, volume up/down.
Example: 'mute PC' → 'system mute PC'
Multiple tasks: 'mute PC and reduce brightness' → 'system mute PC, system reduce brightness'

-> Respond with 'content (topic)' if the query is asking to generate any type of content such as code, email, poem, or story.
Example: 'write a poem about space' → 'content poem about space'

-> Respond with 'google search (topic)' for Google-specific searches.
Example: 'search Google for AI news' → 'google search AI news'

-> Respond with 'youtube search (topic)' for YouTube-specific searches.
Example: 'search YouTube for relaxing music' → 'youtube search relaxing music'

*** If a query involves multiple tasks like 'open Facebook and close WhatsApp', respond with: 'open Facebook, close WhatsApp' ***

*** If the user says goodbye or indicates the end of the session (e.g., 'bye Pratham'), respond with 'exit' ***

*** If you are unsure about the classification or the query does not fit any category, respond with 'general (query)' ***

As a beautifully designed model, Pratham is built to make accurate decisions and fallback gracefully when uncertain.
"""


ChatHistory=[
    {"role": "User","message":"how are you?"},
    {"role": "Chatbot","message":"general how are you?"},
    {"role": "User","message":"do you like pizza?"},
    {"role": "Chatbot","message":"general do you like pizza?"},
    {"role":"User","message":"open chrome and tell me about mahatma gandhi"},
    {"role":"Chatbot","message":"open chrome, realtime tell me about mahatma gandhi"},
    {"role":"User","message":"open chrome and firefox"},
    {"role":"Chatbot","message":"open chrome, open firefox"},
    {"role":"User","message":"what is today's date and by the way remind me that I have a dancing performance on 5th aug at 11 pm"},
    {"role":"Chatbot","message":"realtime what is today's date, reminder 11:00 pm 5th aug dancing performance"},
    {"role":"User","message":"chat with me"},
    {"role":"Chatbot","message":"general chat with me"},
    {"role": "User", "message": "what is the weather like today?"},
    {"role": "Chatbot", "message": "realtime what is the weather like today?"},
    {"role": "User", "message": "what is Elon Musk's networth?"},
    {"role": "Chatbot", "message": "realtime what is Elon Musk's networth?"},
    {"role": "User", "message": "can you play some music?"},
    {"role": "Chatbot", "message": "play some music"},
    {"role": "User", "message": "generate image of a sunset"},
    {"role": "Chatbot", "message": "generate image of a sunset"},
    {"role": "User", "message": "open youtube and search for funny cat videos"},
    {"role": "Chatbot", "message": "open youtube, google search funny cat videos"},
    {"role": "User", "message": "write a python script to calculate factorial"},
    {"role": "Chatbot", "message": "system write a python script to calculate factorial"},
    {"role": "User", "message":"Who is Elon Musk?"},
    {"role": "Chatbot", "message": "realtime who is Elon Musk?"},
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},

    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},

    {"role": "User", "message": "chat with me"},
    {"role": "Chatbot", "message": "general chat with me"},

    {"role": "User", "message": "write a python script to calculate factorial"},
    {"role": "Chatbot", "message": "system write a python script to calculate factorial"},

    {"role": "User", "message": "generate image of a sunset"},
    {"role": "Chatbot", "message": "generate image of a sunset"},

    {"role": "User", "message": "can you play some music?"},
    {"role": "Chatbot", "message": "play some music"},

    {"role": "User", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "Chatbot", "message": "open chrome, realtime tell me about mahatma gandhi"},

    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},

    {"role": "User", "message": "what is today's date and by the way remind me that I have a dancing performance on 5th aug at 11 pm"},
    {"role": "Chatbot", "message": "realtime what is today's date, reminder 11:00 pm 5th aug dancing performance"},

    {"role": "User", "message": "what is the weather like today?"},
    {"role": "Chatbot", "message": "realtime what is the weather like today?"},

    {"role": "User", "message": "what is Elon Musk's networth?"},
    {"role": "Chatbot", "message": "realtime what is Elon Musk's networth?"},

    {"role": "User", "message": "Who is Elon Musk?"},
    {"role": "Chatbot", "message": "realtime who is Elon Musk?"},

    {"role": "User", "message": "open youtube and search for funny cat videos"},
    {"role": "Chatbot", "message": "open youtube, youtube search funny cat videos"},

    {"role": "User", "message": "search google for AI generated videos"},
    {"role": "Chatbot", "message": "google search AI generated videos"},

    {"role": "User", "message": "remind me to call mom at 7 pm today"},
    {"role": "Chatbot", "message": "reminder 7:00 pm today call mom"},
    
    {"role": "User", "message": "exit the program"},
    {"role": "Chatbot", "message": "exit the program"},
    
    {"role": "User", "message": "close chrome"},
    {"role": "Chatbot", "message": "close chrome"},
    
    {"role": "User", "message": "write a poem about space"},
    {"role": "Chatbot", "message": "content write a poem about space"},
    
    {"role": "User", "message": "can you increase the volume of pc?"},
    {"role": "Chatbot", "message": "system can you increase the volume of pc?"},

    {"role": "User", "message": "can you decrease the brightness of my screen?"},
    {"role": "Chatbot", "message": "system can you decrease the brightness of my screen?"},

    {"role": "User", "message": "open spotify and play my favorite playlist"},
    {"role": "Chatbot", "message": "open spotify, play my favorite playlist"},

    {"role": "User", "message": "search for the latest news on AI"},
    {"role": "Chatbot", "message": "google search latest news on AI"}

]

def FirstLayerDMM(prompt:str ="test"):
    messages.append({"role": "User", "message": f"{prompt}"})
    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,  
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )
    
    response = ""
    
    for event in stream:
        if event.event_type == "text-generation":
            response+= event.text
    
    response= response.replace("\n","")
    response=response.split(",")
    
    response=[i.strip() for i in response]
    
    temp=[]
    
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
                
    response=temp
    
    if"(query)" in response:
        newresponse= FirstLayerDMM(prompt=prompt)
        return newresponse
    else:
        return response
    
if __name__ == "__main__":
    print(FirstLayerDMM(input(">>> ")))