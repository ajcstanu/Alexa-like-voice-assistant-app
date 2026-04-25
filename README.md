# 🔵 AI Voice Assistant — Alexa-like

A Python voice assistant that works just like Amazon Alexa — wake word activation, real-time streaming AI responses, and text-to-speech output. 
---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ Wake Word | Say `"hey assistant"` to activate |
| 🧠 Real-time AI | Streams responses as they generate |
| 🔊 Text-to-Speech | Speaks responses sentence-by-sentence (low latency) |
| ⌨️ Text Mode | Keyboard fallback if no microphone |
| 💬 Conversation Memory | Remembers context across turns |
| 🔄 Reset | Say `"reset"` to clear history |
| 🚪 Exit | Say `"quit"` or `"goodbye"` |

---
## 📁 Project Structure

```
alexa_assistant/
├── assistant.py       # Main application (all logic)
├── requirements.txt   # Python dependencies
├── setup.sh           # Linux/Mac one-click setup
├── setup.bat          # Windows one-click setup
└── README.md          # This file
```

---

---

## 🚀 Quick Start

### Step 1 — Get an API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Create an API key under **API Keys**

---

### Step 2 — Install

**Linux / Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```
Double-click setup.bat
```

**Manual (any OS):**
```bash
pip install -r requirements.txt
```

> **Linux extra step** (for microphone):
> ```bash
> sudo apt-get install portaudio19-dev python3-pyaudio espeak
> ```

> **Mac extra step:**
> ```bash
> brew install portaudio
> ```

---

### Step 3 — Set API Key

**Linux / Mac:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

---

### Step 4 — Run

```bash
python assistant.py
```

You'll be asked to choose:
- **[1] Voice mode** — Uses your microphone + wake word
- **[2] Text mode** — Keyboard input (no microphone needed)

---

## 🗣️ How to Use

### Voice Mode

1. Run the app → it calibrates your microphone
2. Say: **"Hey assistant"**
3. Wait for the chime/confirmation
4. Ask your question: *"What's the capital of France?"*
5. Listen to the spoken response

### Text Mode

Just type your question and press **Enter**.

---

## 🛠️ Built-in Commands

| Say / Type | Action |
|---|---|
| `hey assistant` | Wake word (voice mode) |
| `reset` | Clear conversation history |
| `help` | Show help |
| `quit` / `exit` / `goodbye` | Exit the app |

---

## ⚙️ Configuration

Edit these constants at the top of `assistant.py`:

```python
WAKE_WORDS = ["hey assistant", "okay assistant", "hi assistant"]
# Add your own wake words ↑

MODEL = "claude-sonnet-4-20250514"
# Change model here ↑

MAX_HISTORY = 10
# How many conversation turns to remember ↑

SYSTEM_PROMPT = """You are a helpful, friendly voice assistant..."""
# Customize the assistant's personality ↑
```

---

## 🔧 Troubleshooting

### ❌ `ANTHROPIC_API_KEY not set`
You forgot to export the key. See **Step 3** above.

### ❌ `speech_recognition not installed`
```bash
pip install SpeechRecognition PyAudio
```

On Linux, also:
```bash
sudo apt-get install portaudio19-dev
```

### ❌ `pyttsx3` error on Linux
```bash
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
pip install pyttsx3
```

### ❌ `PyAudio` install fails on Mac
```bash
brew install portaudio
pip install pyaudio
```

### ❌ Microphone not detected
- Check system permissions (microphone access)
- Try plugging in an external USB microphone
- The app automatically falls back to text mode if mic isn't available

### ❌ Speech recognition wrong language
Google Speech Recognition defaults to English. To change it, edit `assistant.py`:
```python
text = self.recognizer.recognize_google(audio, language="hi-IN")  # Hindi
text = self.recognizer.recognize_google(audio, language="fr-FR")  # French
```

---

## 🌐 Requirements

- Python 3.10+
- Internet connection (for Claude API + Google Speech Recognition)
- Microphone (optional — text mode works without it)

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `anthropic` | Claude AI API client |
| `SpeechRecognition` | Microphone → text transcription |
| `pyttsx3` | Text → speech (offline TTS engine) |
| `PyAudio` | Microphone audio capture |

---

## 💡 Example Conversations

```
You:  hey assistant
Bot:  Yes?

You:  What's the weather like on Mars?
Bot:  Mars has an average temperature of about -60°C, with thin carbon 
      dioxide atmosphere and frequent dust storms...

You:  Tell me a joke
Bot:  Why don't scientists trust atoms? Because they make up everything!

You:  reset
Bot:  Done! I've cleared our conversation history.

You:  quit
Bot:  Goodbye! Have a great day!
```


