---
layout: page
title: AI Voice Clone Agent in Python
permalink: /coding/voice-clone-agent/en/
nav_exclude: true
---

[한국어 버전](/coding/voice-clone-agent/)

## What I Built

This is a terminal app for having a voice conversation with an AI that speaks in my cloned voice. The pipeline has three stages.

```text
🎙️ listen()  →  🧠 think()  →  🔊 speak()
  record mic       LLM reply       play cloned voice
  + STT            with history    with TTS streaming
```

- **STT (Speech-to-Text):** AssemblyAI `Transcriber` converts the recording into text.
- **LLM:** The app sends the conversation history in `messages` to the AssemblyAI LLM Gateway.
- **TTS (Text-to-Speech):** It reads the reply with my cloned voice ID and sends each audio chunk directly to the speaker.

> Source: I followed a [YouTube tutorial](https://www.youtube.com/watch?v=fpnKkmfApIg), then debugged the project and expanded the notes myself.

---

## main.py

```python
import os
import wave

import assemblyai as aai
import httpx
import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
VOICE_ID = os.environ["ASSEMBLYAI_VOICE_ID"]
MODEL = "qwen3.5-4b-32k-fast"

SYSTEM_PROMPT = """You are AI Mj and you love to talk about programming, Python and AI. Your replies are read out loud,
so keep them to 1-3 short sentences and never use markdown, lists or emojis."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]
aai.settings.api_key = API_KEY

def listen():
    """Record from the mic until Enter is pressed, then transcribe it with AssemblyAI."""
    frames = []
    input("\nPress Enter and start talking...")
    with sd.RawInputStream(samplerate=16000, channels=1, dtype="int16",
                           callback=lambda data, *_: frames.append(bytes(data))):
        input("Listening... press Enter when you're done.")
    with wave.open("you.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b"".join(frames))
    transcript = aai.Transcriber().transcribe("you.wav")
    if transcript.status == aai.TranscriptStatus.error:
        print(f"(Transcription error: {transcript.error})")
        return ""
    return transcript.text or ""


def think(user_text):
    """Send the conversation to the LLM and return its reply."""
    messages.append({"role": "user", "content": user_text})
    response = httpx.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers={"Authorization": API_KEY},
        json={"model": MODEL, "messages": messages, "max_tokens": 200},
        timeout=30,
    )
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"].strip()
    messages.append({"role": "assistant", "content": reply})
    return reply


def speak(text):
    """Read the text out loud in the cloned voice, playing audio as it streams in."""
    config = aai.TTSConfig(voice_id=VOICE_ID)
    with aai.TTSSession(config, api_key=API_KEY) as session:
        with sd.RawOutputStream(samplerate=24000, channels=1, dtype="int16") as speaker:
            for chunk in session.speak(text):
                speaker.write(chunk)


def main():
    print("AI MJ is ready. Say 'goodbye' to exit.")
    while True:
        user_text = listen().strip()
        if not user_text:
            print("(Didn't catch that, try again.)")
            continue
        print(f"You: {user_text}")
        if "goodbye" in user_text.lower():
            speak("Later! Thanks for hanging out.")
            break
        reply = think(user_text)
        print(f"AI MJ: {reply}")
        speak(reply)

if __name__ == "__main__":
    main()
```

## How the Code Works

### 1. `listen()`: record → save WAV → transcribe

- `sd.RawInputStream` continuously sends small pieces of microphone audio to the callback, which appends them to the `frames` list.
- When the inner `input()` ends, the `with` block closes the stream and stops recording.
- The `wave` module writes a WAV header. Its values must match the recording settings exactly.

| Recording setting | WAV header | Meaning |
| --- | --- | --- |
| `channels=1` | `setnchannels(1)` | Mono |
| `dtype="int16"` | `setsampwidth(2)` | One sample = 16 bits = 2 bytes |
| `samplerate=16000` | `setframerate(16000)` | 16,000 samples per second |

If `setsampwidth()` is missing, Python raises `wave.Error: sample width not specified` because the file header does not know how many bytes belong to each sample.

### 2. `think()`: send the full conversation

The LLM does not remember previous calls by itself. The app appends `system → user → assistant → user ...` messages and sends the entire list every time.

The system prompt asks for one to three short sentences without Markdown, lists, or emoji because formatting symbols sound unnatural when read aloud. `raise_for_status()` raises an exception for HTTP 4xx or 5xx responses instead of hiding a failed request.

### 3. `speak()`: stream the generated voice

`session.speak(text)` yields audio chunks instead of waiting for the entire recording. Each chunk is immediately passed to `speaker.write(chunk)`, so playback starts quickly.

TTS output uses a 24,000 Hz sample rate, which is different from the 16,000 Hz microphone input. Using the wrong output rate makes speech play too fast or too slowly.

### 4. `main()`: conversation loop

- Empty transcription uses `continue` to listen again.
- A message containing `"goodbye"` plays a farewell and exits with `break`.

---

## Troubleshooting: “I Can't Hear Anything”

### Symptom

The app repeatedly printed this message:

```text
Press Enter and start talking...
Listening... press Enter when you're done.
(Didn't catch that, try again.)
```

### Investigation

**1. The failure happened before playback.**

`continue` runs after `(Didn't catch that)`, so `speak()` is never called. The cause of “no sound” could therefore be microphone input rather than speaker output. A failure early in the pipeline prevents later stages from running.

**2. The original code hid API errors.**

```python
return aai.Transcriber().transcribe("you.wav").text or ""
```

Even an API failure could turn into an empty string through `None or ""`. That made it impossible to distinguish an unrecognized recording from an API error. I changed the code to inspect `status` first. The result was `status: completed`, `error: None`, and `text: ''`, which showed that the API itself worked.

**3. I inspected the recording directly.**

```python
import wave, array
w = wave.open("you.wav")
a = array.array("h", w.readframes(w.getnframes()))
print("peak amplitude:", max(abs(x) for x in a))
```

```text
peak amplitude: 0
```

The three-second file had a maximum amplitude of zero: complete silence. The microphone appeared in `sd.query_devices()` and its input level was not zero.

**4. I changed the execution environment.**

The same code worked in the macOS Terminal app instead of VS Code's integrated terminal.

### Root Cause: macOS Microphone Permission

When an app lacks microphone permission, macOS can provide zeros instead of raising an error. The audio stream still opens normally, which makes the problem difficult to identify from the Python code alone.

Python launched from VS Code inherits VS Code's permission. VS Code did not have microphone access, so it recorded silence.

### Fix

- **Option A:** System Settings → Privacy & Security → Microphone → enable Visual Studio Code, then fully quit and reopen VS Code.
- **Option B:** Run `uv run main.py` from the macOS Terminal app and allow microphone access when prompted.

### Two More Bugs Fixed

| Location | Problem | Fix |
| --- | --- | --- |
| Module top level | A test call, `print(think(listen()))`, ran once before `main()` | Removed it |
| `speak()` | Typo: `speaker.wrtie(chunk)`; the earlier input failure had prevented this line from running | Changed it to `speaker.write(chunk)` |

## What I Learned

- **The symptom and root cause can be in different places.** The missing output sound was caused by microphone input.
- **A default such as `x or ""` can hide failures.** Inspect the status of external API results first.
- **Inspect the actual data.** One amplitude check immediately proved that the recording was silent.
- **Change the environment to narrow the cause.** If identical code works in Terminal but not VS Code, investigate permissions and environment rather than only the code.
