---
layout: page
title: AI Voice Clone Agent in Python
permalink: /coding/voice-clone-agent/
---

## 무엇을 만들었나

내 목소리를 클론한 AI와 음성으로 대화하는 터미널 앱이다. 흐름은 세 단계다.

```text
🎙️ listen()  →  🧠 think()  →  🔊 speak()
  마이크 녹음        LLM 응답         클론 음성으로 재생
  + STT 변환        (대화 기록 유지)   (TTS 스트리밍)
```

- **STT (Speech-to-Text):** AssemblyAI `Transcriber`가 녹음 파일을 텍스트로 바꾼다.
- **LLM:** AssemblyAI LLM Gateway로 대화 기록(`messages`)을 보내고 답변을 받는다.
- **TTS (Text-to-Speech):** 클론한 voice ID로 답변을 읽고, 받은 오디오 조각(chunk)을 바로 스피커로 흘려보낸다.

> 출처: [YouTube 튜토리얼](https://www.youtube.com/watch?v=fpnKkmfApIg)을 따라 만들고, 직접 디버깅하며 내용을 덧붙였다.

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

---

## 코드 설명

### 1. `listen()`: 녹음 → wav 저장 → 텍스트 변환

- `sd.RawInputStream`은 마이크 소리를 작은 조각으로 나눠 계속 `callback`에 넘겨준다. 받은 조각은 `frames` 리스트에 쌓는다.
  - 녹음기가 테이프 대신 리스트에 소리를 이어 붙인다고 생각하면 된다.
- `with` 블록 안의 `input()`이 끝나면(= Enter를 누르면) 블록을 빠져나가면서 스트림이 자동으로 닫히고 녹음이 멈춘다.
- `wave` 모듈로 wav 헤더를 쓴다. 이때 녹음 설정과 값이 **정확히 일치**해야 한다.

| 녹음 설정 | wav 헤더 | 의미 |
|---|---|---|
| `channels=1` | `setnchannels(1)` | 모노 |
| `dtype="int16"` | `setsampwidth(2)` | 샘플 하나 = 16bit = 2byte |
| `samplerate=16000` | `setframerate(16000)` | 1초에 16,000개 샘플 |

> `setsampwidth()`를 빠뜨리면 `wave.Error: sample width not specified`가 난다. 헤더에 "숫자 하나가 몇 바이트인지"를 적지 않으면 파일을 만들 수 없기 때문이다.

### 2. `think()`: 대화 기록을 통째로 보내기

- LLM은 이전 대화를 기억하지 못한다(stateless). 그래서 `messages` 리스트에 `system → user → assistant → user ...` 순서로 쌓고, 매번 **전체 기록**을 보낸다.
- `SYSTEM_PROMPT`에 "1~3문장, 마크다운·이모지 금지"를 넣었다. 답변을 소리로 읽을 것이기 때문에 `**굵게**`나 목록 기호가 섞이면 어색하게 들린다.
- `raise_for_status()`는 HTTP 4xx/5xx 응답이면 예외를 던진다. 실패를 조용히 넘기지 않는다.

### 3. `speak()`: 스트리밍 재생

- `session.speak(text)`는 오디오 전체가 아니라 **조각(chunk)** 을 차례로 돌려준다. 받는 즉시 `speaker.write(chunk)`로 재생하므로, 전체를 기다리지 않고 바로 말하기 시작한다.
- TTS 출력은 `samplerate=24000`이다. 입력(16000)과 다르다. 출력 샘플레이트를 틀리게 쓰면 목소리가 빨라지거나 느려진다.

### 4. `main()`: 대화 루프

- 빈 텍스트면 `continue`로 다시 듣는다.
- `"goodbye"`가 포함되면 작별 인사를 하고 `break`로 끝낸다.

---

## 🐛 트러블슈팅: "소리가 안 들려요"

### 증상

실행하면 계속 이 메시지만 반복됐다.

```text
Press Enter and start talking...
Listening... press Enter when you're done.
(Didn't catch that, try again.)
```

### 원인 추적 과정

**① 재생이 아니라 인식 단계에서 막혀 있었다.**
`(Didn't catch that)` 뒤에 `continue`가 실행되므로 `speak()`는 **한 번도 호출되지 않았다**. 파이프라인은 앞 단계가 실패하면 뒤 단계가 실행되지 않는다. 그래서 "소리가 안 난다"의 원인이 출력이 아니라 **입력**에 있을 수 있다.

**② 에러가 숨겨져 있었다.**
처음 코드는 이랬다.

```python
return aai.Transcriber().transcribe("you.wav").text or ""
```

API가 실패해도 `None or ""` → 빈 문자열이 된다. 그러면 "말을 못 알아들음"과 "API 에러"를 구분할 수 없다. 그래서 `status`를 먼저 확인하도록 바꿨다(위 코드 참고).
→ 결과는 `status: completed`, `error: None`, `text: ''`였다. API는 정상이었다.

**③ 녹음 파일을 직접 열어봤다.**

```python
import wave, array
w = wave.open("you.wav")
a = array.array("h", w.readframes(w.getnframes()))
print("peak amplitude:", max(abs(x) for x in a))
```

```text
peak amplitude: 0
```

3초짜리 파일인데 **최대 진폭이 0**, 즉 완전한 무음이었다. 마이크 장치(`sd.query_devices()`)는 정상으로 잡혀 있었고, 입력 볼륨도 0이 아니었다.

**④ 실행 환경을 바꿔봤다.**
VS Code 통합 터미널 대신 **macOS 기본 터미널 앱**에서 실행하니 정상으로 작동했다. ✅

### 진짜 원인: macOS 마이크 권한

macOS는 앱에 마이크 권한이 없으면 **에러를 내지 않고 0(무음)만 보낸다**. 스트림은 정상으로 열리기 때문에 코드만 봐서는 알 수 없다.

VS Code에서 실행한 python은 VS Code의 권한을 물려받는다. VS Code에 마이크 권한이 없어서 무음이 녹음됐던 것이다.

### 해결 방법

- **방법 A:** 시스템 설정 → 개인정보 보호 및 보안 → **마이크** → **Visual Studio Code** 켜기 → VS Code 완전히 종료(⌘Q) 후 재실행
- **방법 B:** macOS 기본 **터미널** 앱에서 실행 (`uv run main.py`) → 처음 실행할 때 뜨는 권한 팝업에서 허용

### 같이 고친 버그 2개

| 위치 | 문제 | 수정 |
|---|---|---|
| 모듈 최상단 | 테스트용 `print(think(listen()))`가 남아 있어 `main()`보다 먼저 한 번 실행됨 | 삭제 |
| `speak()` | `speaker.wrtie(chunk)` 오타. 인식이 안 돼서 이 줄까지 오지 않았기 때문에 숨어 있었음 | `speaker.write(chunk)` |

---

## 배운 점

- **증상이 나타난 곳과 원인이 있는 곳은 다를 수 있다.** 소리가 안 나는 문제의 원인은 스피커가 아니라 마이크였다.
- **`x or ""` 같은 기본값 처리는 에러를 숨길 수 있다.** 외부 API 결과는 `status`부터 확인하자.
- **데이터를 직접 열어보자.** 진폭을 찍어본 한 줄이 원인을 바로 보여줬다.
- **환경을 바꿔서 원인을 좁히자.** 같은 코드가 터미널 앱에서는 되고 VS Code에서는 안 된다면, 코드가 아니라 환경(권한) 문제다.
