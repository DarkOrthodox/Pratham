# Pratham AI Assistant

Pratham is an advanced AI-powered desktop assistant featuring real-time search, voice interaction, image generation, and automation capabilities. It combines large language models, speech recognition, and a modern GUI to deliver a seamless user experience.

## Features

- **Conversational AI**: Chat with Pratham using natural language.
- **Real-Time Search**: Get up-to-date answers from the internet.
- **Voice Recognition**: Speak your queries and commands.
- **Text-to-Speech**: Pratham responds with synthesized speech.
- **Image Generation**: Generate images from text prompts using Stable Diffusion.
- **Automation**: Open/close apps, search Google/YouTube, play music, and more.
- **Customizable GUI**: Modern PyQt5-based interface.

## Directory Structure

```
.
├── .env
├── Main.py
├── Requirements.txt
├── Backend/
│   ├── Automation.py
│   ├── Chatbot.py
│   ├── ImageGeneration.py
│   ├── Model.py
│   ├── RealtimeSearchEngine.py
│   ├── SpeechToText.py
│   ├── TextToSpeech.py
│   └── ...
├── Data/
│   ├── ChatLog.json
│   ├── Voice.html
│   └── ...
├── Frontend/
│   ├── GUI.py
│   └── ...
└── ...
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/pratham-ai-assistant.git
   cd pratham-ai-assistant
   ```

2. **Install dependencies:**
   ```sh
   pip install -r Requirements.txt
   ```

3. **Configure environment variables:**
   - Edit `.env` and add your API keys for Cohere, Groq, and HuggingFace.

4. **Run the application:**
   ```sh
   python Main.py
   ```

## Requirements

- Python 3.8+
- [See Requirements.txt](Requirements.txt) for all Python dependencies.

## Usage

- Launch the assistant with `python Main.py`.
- Use the GUI to interact via text or voice.
- Pratham can answer questions, search the web, generate images, and automate tasks.

## Customization

- **Assistant Name & Voice**: Change `AssistantName` and `AssistantVoice` in `.env`.
- **Input Language**: Set `InputLanguage` in `.env` for speech recognition.

## Credits

- [Cohere](https://cohere.com/) for language model APIs
- [Groq](https://groq.com/) for LLM inference
- [HuggingFace](https://huggingface.co/) for image generation
- [PyQt5](https://riverbankcomputing.com/software/pyqt/) for GUI

## License

This project is for educational and personal use. See [LICENSE](LICENSE) for details.

---

**Note:** Some features (like voice and image generation) require internet access and valid