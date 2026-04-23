"""
Voice Assistant - Alexa-like AI powered by Claude API
Real-time voice input + streaming text-to-speech output

INSTALL:
    pip install anthropic SpeechRecognition pyttsx3 PyAudio

SET API KEY:
    Linux/Mac:  export ANTHROPIC_API_KEY="sk-ant-..."
    Windows:    set ANTHROPIC_API_KEY=sk-ant-...

RUN:
    python assistant.py
"""

import os
import sys
import queue
import threading
import anthropic

# ─── Optional voice/audio imports ─────────────────────────────────────────────

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("[WARNING] speech_recognition not installed. Voice input disabled.")
    print("         Fix: pip install SpeechRecognition PyAudio\n")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[WARNING] pyttsx3 not installed. Text-to-speech disabled.")
    print("         Fix: pip install pyttsx3\n")

# ─── Configuration ─────────────────────────────────────────────────────────────

WAKE_WORDS    = ["hey assistant", "okay assistant", "hi assistant", "hello assistant"]
MODEL         = "claude-sonnet-4-20250514"
MAX_TOKENS    = 512
MAX_HISTORY   = 10   # conversation turns to remember

SYSTEM_PROMPT = (
    "You are a helpful, friendly voice assistant — like Alexa but smarter. "
    "Keep responses concise and conversational (2-4 sentences max unless asked for detail). "
    "Avoid markdown, bullet points, or any special formatting — speak naturally as if talking. "
    "Be warm, helpful, and direct."
)

# ─── Text-to-Speech Engine ─────────────────────────────────────────────────────

class TTSEngine:
    """Wraps pyttsx3 for offline text-to-speech."""

    def __init__(self):
        self.engine    = None
        self.available = TTS_AVAILABLE
        if not self.available:
            return
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate",   175)   # words per minute
            self.engine.setProperty("volume", 0.9)
            voices = self.engine.getProperty("voices")
            if voices:
                # Prefer second voice (often female) if available
                self.engine.setProperty("voice", voices[min(1, len(voices) - 1)].id)
        except Exception as e:
            print(f"[TTS] Init error: {e}")
            self.available = False

    def speak(self, text: str):
        """Speak text aloud and also print it."""
        print(f"\n🤖  Assistant: {text}\n")
        if self.available and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[TTS] Speak error: {e}")

    def stop(self):
        if self.available and self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass


# ─── Voice Listener (Speech-to-Text) ──────────────────────────────────────────

class VoiceListener:
    """Wraps SpeechRecognition for microphone input → text."""

    def __init__(self):
        self.available   = SPEECH_AVAILABLE
        self.recognizer  = None
        self.microphone  = None

        if not self.available:
            return
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.pause_threshold        = 1.0
            self.recognizer.energy_threshold       = 300
            self.recognizer.dynamic_energy_threshold = True
            self.microphone = sr.Microphone()

            print("🎙️   Calibrating microphone for ambient noise (1 sec)...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅   Microphone ready.\n")
        except Exception as e:
            print(f"[MIC] Init error: {e}")
            self.available = False

    def listen(self, timeout: int = 10, phrase_limit: int = 15) -> str | None:
        """
        Listen for one spoken phrase and return it as lowercase text.
        Returns None on silence, noise, or error.
        """
        if not self.available:
            return None
        try:
            with self.microphone as source:
                print("🎙️   Listening...", end="", flush=True)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit,
                )
            print(" transcribing...", end="", flush=True)
            text = self.recognizer.recognize_google(audio)
            print(f"\r🗣️   You said: {text}               ")
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("\r⚠️   Could not understand audio.      ")
            return None
        except sr.RequestError as e:
            print(f"\r❌   Speech service error: {e}")
            return None
        except Exception as e:
            print(f"\r❌   Listener error: {e}")
            return None


# ─── Claude AI Brain ───────────────────────────────────────────────────────────

class AIBrain:
    """
    Manages conversation history and streams responses from Claude.
    """

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is not set.\n"
                "  Linux/Mac: export ANTHROPIC_API_KEY='sk-ant-...'\n"
                "  Windows:   set ANTHROPIC_API_KEY=sk-ant-..."
            )
        self.client  = anthropic.Anthropic(api_key=api_key)
        self.history: list[dict] = []

    def ask(self, user_input: str, on_chunk=None) -> str:
        """
        Send user_input to Claude and return the full response.
        If on_chunk is provided, it is called with each streamed text chunk
        as they arrive (for real-time TTS / printing).
        """
        self.history.append({"role": "user", "content": user_input})

        # Keep history within token-safe limits
        if len(self.history) > MAX_HISTORY * 2:
            self.history = self.history[-(MAX_HISTORY * 2):]

        full_response = ""
        try:
            with self.client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=self.history,
            ) as stream:
                for chunk in stream.text_stream:
                    full_response += chunk
                    if on_chunk:
                        on_chunk(chunk)

        except anthropic.APIConnectionError:
            full_response = "I'm having trouble reaching the internet right now."
        except anthropic.AuthenticationError:
            full_response = "There's an API key issue. Please check your ANTHROPIC_API_KEY."
        except anthropic.RateLimitError:
            full_response = "I'm being rate-limited right now. Please try again in a moment."
        except Exception as e:
            full_response = f"Sorry, something went wrong: {e}"

        self.history.append({"role": "assistant", "content": full_response})
        return full_response

    def reset(self):
        """Wipe conversation history."""
        self.history.clear()


# ─── Main Voice Assistant ──────────────────────────────────────────────────────

class VoiceAssistant:
    """
    Ties together TTSEngine, VoiceListener, and AIBrain.
    Supports both voice mode (wake-word) and text mode (keyboard).
    Streams AI responses and speaks each sentence as it arrives.
    """

    def __init__(self):
        print("=" * 58)
        print("  🔵  AI Voice Assistant  —  Claude-powered, Alexa-style")
        print("=" * 58 + "\n")

        self.tts      = TTSEngine()
        self.listener = VoiceListener()
        self.brain    = AIBrain()
        self.running  = False

        # Streaming / TTS pipeline state
        self._stream_buffer = ""
        self._tts_queue: queue.Queue = queue.Queue()
        self._tts_thread: threading.Thread | None = None

    # ── Sentence-streaming TTS pipeline ────────────────────────────────────────

    def _tts_worker(self):
        """
        Background thread that dequeues sentences and speaks them.
        Receives None as a poison pill to stop.
        """
        while True:
            sentence = self._tts_queue.get()
            if sentence is None:
                self._tts_queue.task_done()
                break
            if sentence.strip():
                self.tts.speak(sentence.strip())
            self._tts_queue.task_done()

    def _on_chunk(self, chunk: str):
        """
        Called for every streamed text chunk from Claude.
        Accumulates text and enqueues complete sentences to the TTS worker
        so speech starts before the full response is done.
        """
        self._stream_buffer += chunk
        print(chunk, end="", flush=True)

        # Drain any complete sentences from the buffer
        while True:
            cut = -1
            for sep in (".", "!", "?", "\n"):
                pos = self._stream_buffer.find(sep)
                if pos != -1 and (cut == -1 or pos < cut):
                    cut = pos
            if cut == -1:
                break
            sentence = self._stream_buffer[: cut + 1]
            self._stream_buffer = self._stream_buffer[cut + 1:]
            if self.tts.available:
                self._tts_queue.put(sentence)

    def _flush_tts(self):
        """Flush any remaining buffered text and wait for TTS to finish."""
        if self._stream_buffer.strip() and self.tts.available:
            self._tts_queue.put(self._stream_buffer.strip())
        self._stream_buffer = ""
        # Send poison pill and wait
        self._tts_queue.put(None)
        if self._tts_thread:
            self._tts_thread.join(timeout=60)

    # ── Response handler ────────────────────────────────────────────────────────

    def respond(self, user_input: str):
        """Stream a Claude response and speak it in real time."""
        print("\n🤖  Assistant: ", end="", flush=True)

        # Spin up the TTS worker
        self._tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self._tts_thread.start()

        # Stream Claude's reply (on_chunk feeds TTS queue in real time)
        self.brain.ask(user_input, on_chunk=self._on_chunk)

        # Flush any leftover text, then wait for speech to finish
        self._flush_tts()
        print()  # tidy newline after streaming output

    # ── Built-in commands ───────────────────────────────────────────────────────

    def handle_command(self, text: str) -> bool:
        """
        Check for built-in commands.
        Returns True if the text was a command (so the caller skips AI lookup).
        """
        t = text.lower().strip()

        if t in {"quit", "exit", "goodbye", "bye", "stop"}:
            self.tts.speak("Goodbye! Have a great day!")
            self.running = False
            return True

        if t in {"reset", "clear", "clear history", "forget everything", "start over"}:
            self.brain.reset()
            self.tts.speak("Done! Conversation history cleared.")
            return True

        if t in {"help"}:
            self.tts.speak(
                "You can ask me anything. "
                "Say reset to clear history, or quit to exit."
            )
            return True

        return False

    # ── Run modes ───────────────────────────────────────────────────────────────

    def run_voice_mode(self):
        """
        Continuous loop:
          1. Listen for wake word
          2. On wake → listen for command
          3. Respond via Claude + TTS
        """
        self.running = True
        self.tts.speak("Hello! Say 'hey assistant' any time to talk to me.")
        print("💡  Wake words:", ", ".join(f'"{w}"' for w in WAKE_WORDS))
        print("    Press Ctrl+C to quit.\n")

        while self.running:
            heard = self.listener.listen(timeout=5, phrase_limit=5)
            if not heard:
                continue
            if not any(w in heard for w in WAKE_WORDS):
                continue

            print("\n🔔  Wake word detected!")
            self.tts.speak("Yes?")

            command = self.listener.listen(timeout=8, phrase_limit=15)
            if not command:
                self.tts.speak("I didn't catch that. Try saying hey assistant again.")
                continue

            if not self.handle_command(command):
                self.respond(command)

    def run_text_mode(self):
        """Keyboard-driven interaction loop (fallback if no mic)."""
        self.running = True
        print("💬  TEXT MODE — type a message and press Enter.")
        print("    Commands: quit | reset | help\n")
        self.tts.speak("Hello! I'm your AI assistant. How can I help you today?")

        while self.running:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_input:
                continue

            if not self.handle_command(user_input):
                self.respond(user_input)

        print("\n👋  Goodbye!\n")

    def run(self):
        """Pick voice or text mode and start."""
        if self.listener.available:
            print("✅  Microphone detected.")
            print("    [1] Voice mode  (wake word + mic)")
            print("    [2] Text mode   (keyboard)\n")
            try:
                choice = input("    Enter 1 or 2 (default 2): ").strip()
            except (EOFError, KeyboardInterrupt):
                choice = "2"
            if choice == "1":
                self.run_voice_mode()
            else:
                self.run_text_mode()
        else:
            print("⚠️   No microphone found — switching to text mode.\n")
            self.run_text_mode()


# ─── Entry Point ───────────────────────────────────────────────────────────────

def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except ValueError as e:
        print(f"\n❌  Setup error:\n    {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋  Interrupted. Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
