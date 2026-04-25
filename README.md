# 🔵 AI Voice Assistant — Alexa-style

A real-time voice assistant powered by the **Anthropic Claude API**.  
Supports wake-word voice input, streaming AI responses, and text-to-speech output.  
Falls back gracefully to text/keyboard mode if no microphone is available.

---

## ✨ Features

- 🎙️ Wake-word voice activation (`hey assistant`, `hi assistant`, etc.)
- 🤖 Claude AI brain with multi-turn conversation memory
- 🔊 Real-time streaming TTS — speaks each sentence as it arrives
- ⌨️ Text mode fallback (keyboard input)
- ⚙️ Fully configurable via environment variables — **zero hardcoded secrets**
- 🧹 Built-in commands: `reset`, `help`, `quit`

---

## 📦 Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

---

## 🚀 Installation

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/voice-assistant.git
cd voice-assistant
```

### 2. Install dependencies

```bash
pip install anthropic SpeechRecognition pyttsx3 PyAudio
```

> **Note for Linux users:** You may need system packages first:
> ```bash
> sudo apt install python3-pyaudio portaudio19-dev espeak
> ```

> **Note for Mac users:**
> ```bash
> brew install portaudio
> ```

---

## 🔑 Set Your API Key

**Linux / Mac:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

> ⚠️ Never paste your API key directly into the code.

---

## ▶️ Run

```bash
python assistant.py
```

On startup you will be asked to choose:
- **[1] Voice mode** — uses your microphone with wake-word detection
- **[2] Text mode** — type messages via keyboard (no mic required)

---

## ⚙️ Configuration (Environment Variables)

All settings are controlled via environment variables. None are hardcoded.

| Variable | Description | Default |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (**required**) | — |
| `CLAUDE_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `MAX_TOKENS` | Maximum tokens in each response | `512` |
| `MAX_HISTORY` | Number of conversation turns to remember | `10` |
| `WAKE_WORDS` | Comma-separated list of wake words | `hey assistant,okay assistant,hi assistant,hello assistant` |
| `TTS_RATE` | Text-to-speech speed (words per minute) | `175` |
| `TTS_VOLUME` | Text-to-speech volume (`0.0` – `1.0`) | `0.9` |
| `ASSISTANT_SYSTEM_PROMPT` | Custom personality/instructions for the AI | Built-in friendly assistant prompt |

### Example — custom configuration

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_MODEL="claude-opus-4-20250514"
export WAKE_WORDS="hey claude,okay claude"
export TTS_RATE="160"
export MAX_HISTORY="20"
python assistant.py
```

---

## 🗣️ Built-in Voice / Text Commands

| Command | What it does |
|---|---|
| `reset` / `clear` / `start over` | Clears conversation history |
| `help` | Explains available commands |
| `quit` / `exit` / `bye` / `goodbye` | Exits the assistant |

---

## 🏗️ Project Structure

```
alexa_assistant/
├── assistant.py       # Main application (all logic)
├── requirements.txt   # Python dependencies
├── setup.sh           # Linux/Mac one-click setup
├── setup.bat          # Windows one-click setup
└── README.md          # This file
```

---

## 🧠 How It Works

```
You speak / type
      ↓
VoiceListener  (SpeechRecognition + Google STT)
      ↓
AIBrain        (Claude API — streaming)
      ↓
TTSEngine      (pyttsx3 — speaks each sentence in real time)
```

1. **VoiceListener** captures audio and converts it to text using Google Speech Recognition.
2. **AIBrain** sends the text to Claude with full conversation history and streams the reply token by token.
3. **TTSEngine** speaks each complete sentence as soon as it arrives — no waiting for the full response.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `PyAudio` install fails | Install `portaudio` first (see Installation above) |
| `ANTHROPIC_API_KEY not set` error | Export the variable in your terminal session |
| No sound / TTS silent | Install `pyttsx3` and `espeak` (Linux) |
| Speech not recognized | Check microphone permissions; reduce background noise |
| Rate limit error | Wait a moment and retry; or reduce `MAX_TOKENS` |

---

## 📄 License

MIT License — free to use, modify, and distribute.
