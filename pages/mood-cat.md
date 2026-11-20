---
layout: page
title: "Mood Cat: 기분을 입력하면 고양이 밈이 나오는 생성기"
permalink: /coding/mood-cat/
nav_exclude: true
---

> “시험 망했어 ㅠㅠ” → 😿 슬픈 고양이 GIF + “괜찮아, 나도 츄르 놓쳤어”

**목표:** 11월 20일 수업 내용인 Runnable, LCEL, `@chain`, `assign`, `retry`와 `fallbacks`를 직접 사용하며 복습한다.

- 이 가이드에는 정답 코드가 없다. 방향, 힌트, 체크리스트를 따라 직접 구현한다.
- 한 단계를 끝내고 체크리스트를 모두 통과하면 다음 단계로 넘어간다.
- 막히면 “어느 단계에서, 무엇을 하다가, 어떤 오류가 발생했는지”를 정리해 질문한다.

---

## 전체 구조

```text
입력: "시험 망했어 ㅠㅠ"
   │
   ▼
[감정 분류]  자유 문장 → 정해진 감정 라벨 하나("sad")      ← LLM
   │
   ▼
[캡션 생성]  고양이 말투 한 줄("괜찮아, 나도 츄르 놓쳤어")  ← LLM
   │
   ▼
[GIF 검색]   "sad cat"으로 GIPHY 검색 → GIF 주소 하나       ← API 호출
   │
   ▼
출력: {text, mood, caption, image_url}
```

핵심은 **LLM을 감정 분류와 캡션 생성에만 사용하고, GIF는 정해진 API에서 가져오는 것**이다. LLM이 이미지를 직접 만들지 않고 GIPHY 검색에 사용할 감정 라벨을 고르므로 결과가 안정적이고 비용도 적게 든다.

## 고양이 이미지 출처

```text
Python 실습(0~5단계) → GIPHY   (.env에 API 키 보관)  ← 다양한 밈 GIF
블로그 JS(6단계)    → CATAAS  (API 키 불필요)       ← 브라우저에서 안전
                    ↳ 4단계에서 GIPHY 실패 시 대체
```

### GIPHY: Python 실습의 메인 GIF 소스

- `"sad cat"`, `"sleepy cat"`, `"hangry cat"` 같은 검색어로 밈 GIF를 찾는다.
- 무료 API 키가 필요하다. 키 없이 요청하면 `401 Unauthorized`가 발생한다.
- 검색 API 주소는 `https://api.giphy.com/v1/gifs/search`다.

| 항목 | 값 |
| --- | --- |
| 주요 파라미터 | `api_key`, `q`, `limit`, `rating` |
| 권장 등급 | `rating=g` |
| 응답 | `data` 리스트 안의 GIF 정보(JSON) |

키를 발급할 때 [GIPHY Developers](https://developers.giphy.com)에서 요청 한도와 출처 표시를 포함한 이용 약관을 직접 확인한다.

### CATAAS: fallback과 블로그 데모용

[CATAAS(Cat as a Service)](https://cataas.com)는 API 키 없이 사용할 수 있다.

| 주소 | 결과 |
| --- | --- |
| `https://cataas.com/cat/happy` | `happy` 태그가 붙은 무작위 고양이 사진 |
| `https://cataas.com/cat/sad/says/hi` | 사진 위에 `hi`를 표시한 사진 |
| `https://cataas.com/cat/happy?json=true` | 사진 정보(JSON) |
| `https://cataas.com/api/tags` | 사용 가능한 태그 목록 |

확인한 감정 태그는 다음과 같다.

`happy` `sad` `angry` `sleepy` `tired` `bored` `scared` `excited` `confused` `hungry` `love` `cute` `grumpy`

이 중 5~7개만 골라 앱의 감정 라벨로 사용한다. 라벨이 너무 많으면 분류가 모호해질 수 있다.

> 외부 무료 서비스는 느려지거나 중단될 수 있으므로 4단계에서 대비책을 만든다. 태그는 사용자가 붙인 것이므로 감정과 사진이 정확히 일치하지 않을 수 있다. `/says/` 뒤의 한글은 폰트 문제로 깨질 수 있으니, 문제가 생기면 캡션을 사진 밖에 별도로 표시한다.

## 전체 로드맵

| 단계 | 만들 것 | 연습하는 개념 | 예상 시간 |
| --- | --- | --- | --- |
| 0 | 환경 준비와 GIPHY 키 발급 | venv, `.env` | 15분 |
| 1 | 키워드 감정 분류기(LLM 없음) | `@chain`, `invoke`, `batch` | 20분 |
| 2 | LLM 감정 분류기 | `prompt \| llm \| parser` | 30분 |
| 3 | 감정·캡션·GIPHY GIF를 하나의 dict로 구성 | `RunnablePassthrough.assign()`, `requests` | 40분 |
| 4 | LLM과 GIPHY 실패에 대비한 fallback 구성 | `.with_retry()`, `.with_fallbacks()` | 25분 |
| 5 (선택) | 캡션 스트리밍 | `.stream()` | 15분 |
| 6 (선택) | 블로그에 데모 삽입 | HTML, JavaScript, Jekyll | 40분 |
| 7 | TIL 작성 | 학습 정리 | 20분 |

## 0단계: 환경 준비

### 할 일

- [ ] `12_rag/side_cat/` 폴더에서 작업하기
- [ ] `ax_study/.venv` 가상환경 사용하기
- [ ] VS Code의 Python 인터프리터가 `.venv`인지 확인하기
- [ ] `12_rag/.env`의 OpenAI API 키를 `load_dotenv()`로 불러오기
- [ ] [GIPHY Developers](https://developers.giphy.com)에서 앱을 만들고 API 키 발급하기
- [ ] `12_rag/.env`에 `GIPHY_API_KEY=발급받은키` 추가하기
- [ ] `.venv`에 이미 설치된 `requests` 확인하기
- [ ] 브라우저에서 `https://cataas.com/cat/happy`를 열어 fallback 이미지 확인하기

### 힌트

- 터미널에서 `which python`을 실행해 경로에 `.venv`가 포함되어 있는지 확인한다.
- `load_dotenv()`는 코드 파일의 폴더부터 상위 폴더로 올라가며 `.env`를 찾는다. 노트북에서는 동작이 다를 수 있으므로 직접 확인한다.

### 체크

- [ ] `import langchain_core`가 오류 없이 실행된다.
- [ ] `OPENAI_API_KEY`와 `GIPHY_API_KEY`가 모두 `None`이 아니다.
- [ ] `requests.get(..., params={...})`로 보낸 기본 GIPHY 요청의 상태 코드가 `200`이다.

> API 키 값 자체는 출력하지 않는다. `.env`는 반드시 `.gitignore`에 등록하고 절대 커밋하지 않는다.

## 1단계: 키워드 감정 분류기

파일: `step1_keyword.py`

### 목표

```text
invoke("happy")                            → "happy"
invoke("너무 졸려")                         → "sleepy"
invoke("asdfgh")                          → "confused"
batch(["happy", "배고파", "화나"])         → ["happy", "hungry", "angry"]
```

### 코드 작성 전에 정할 것

- [ ] 감정 라벨 5~7개 고르기
- [ ] 라벨마다 영어·한국어 키워드 목록 정하기
- [ ] 어떤 키워드도 일치하지 않을 때 사용할 기본 라벨 정하기
- [ ] 키워드가 여러 개 일치할 때 적용할 우선순위 정하기

### 힌트

```text
라벨 → 키워드 리스트를 dict로 정의
@chain을 붙인 함수
  └─ 입력을 소문자로 변환
  └─ dict를 순회하며 키워드 포함 여부 검사
  └─ 일치하면 라벨 반환, 끝까지 없으면 기본값 반환
```

### 체크

- [ ] `invoke()`가 동작한다.
- [ ] 직접 구현하지 않은 `batch()`도 동작하는 이유를 설명할 수 있다.
- [ ] “시험 망했어”를 제대로 분류하지 못하는지 확인하고, LLM이 필요한 이유를 이해한다.

## 2단계: LLM 감정 분류기

파일: `step2_llm_mood.py`

### 목표

```text
invoke({"text": "시험 망했어 ㅠㅠ"})      → "sad"
invoke({"text": "드디어 금요일이다!!"})  → "excited"
invoke({"text": "회의가 3시간째..."})    → "tired"
```

결과는 반드시 1단계에서 정한 라벨 중 하나여야 한다.

### 힌트

필요한 블록은 세 가지다.

1. `ChatPromptTemplate.from_messages([...])`
   - system: 감정 라벨 중 하나만 소문자로 답하도록 지시한다.
   - human: `{text}`
2. `ChatOpenAI(model=...)`
   - 수업에서 사용한 모델을 사용하고 분류 작업이므로 `temperature=0`을 권장한다.
3. `StrOutputParser()`

세 블록을 `|`로 연결한다. 프롬프트의 `{text}`와 `invoke({...})`의 key 이름이 같아야 한다.

### 실험과 체크

- [ ] `"Sad."`처럼 대문자나 문장부호가 붙으면 결과를 다듬는 단계를 추가한다.
- [ ] 라벨 목록에 없는 결과는 기본값으로 바꾼다.
- [ ] `with_structured_output()`과 `Literal`로 결과를 제한하는 방법을 찾아본다.
- [ ] GIPHY 검색어를 LLM이 직접 만들게 하고, 고정 라벨 방식보다 재미있는지·불안정한지 비교한다.
- [ ] 서로 다른 입력 5개를 `batch`로 테스트한다.
- [ ] 체인 `A | B | C`에서 각 요소의 역할을 설명할 수 있다.

## 3단계: 감정·캡션·GIPHY GIF 합치기

파일: `step3_assign.py`

### 목표

```python
{
    "text": "시험 망했어 ㅠㅠ",
    "mood": "sad",
    "caption": "괜찮아, 나도 츄르 놓쳤어",
    "image_url": "https://media.giphy.com/media/...",
}
```

### 힌트

- 시작 입력은 `{"text": "..."}` 형태의 dict다.
- `RunnablePassthrough.assign(mood=2단계_체인)`으로 원래 입력에 `mood`를 추가한다.
- 다음 `assign()`에서 캡션 체인을 연결하고 프롬프트에 `{text}`와 `{mood}`를 모두 사용한다.
- 마지막 `assign()`에는 `@chain`을 붙인 GIPHY 검색 함수를 연결한다. 평범한 함수도 Runnable로 만들어 체인에 넣을 수 있다.
- 검색 함수는 `mood`로 `f"{mood} cat"` 검색어를 만들고 `requests.get()`으로 API를 호출한다.
- 응답의 `data` 리스트에서 하나를 선택한 뒤 `images` 내부의 GIF 주소를 반환한다.
- 응답 구조를 모르면 `json.dumps(..., indent=2)`로 출력해 직접 확인한다.
- `limit=10~25`로 여러 결과를 받은 뒤 `random.choice()`를 사용하면 실행할 때마다 다른 GIF가 나온다.

### 실험과 체크

- [ ] `assign` 없이 `|`로만 연결했을 때 `text`가 사라지고 `KeyError`가 발생하는지 확인한다.
- [ ] 결과에 `text`, `mood`, `caption`, `image_url` 네 key가 모두 있다.
- [ ] URL을 열면 감정에 맞는 고양이 GIF가 나온다.
- [ ] 같은 문장을 세 번 입력했을 때 서로 다른 GIF가 선택된다.
- [ ] 전체 체인을 문장 세 개에 `batch()`로 실행한다.

## 4단계: 누가 실패해도 고양이는 나온다

파일: `step4_resilience.py`

### 목표

| 실패하는 부분 | 재시도 | 계속 실패할 때의 대체 수단 |
| --- | --- | --- |
| LLM 감정 분류 | 3번 | 1단계 키워드 분류기 |
| LLM 캡션 생성 | 3번 | `...냥? (서버가 낮잠 중)` |
| GIPHY 검색 | 3번 | `https://cataas.com/cat/{mood}` |

1단계에서 만든 단순한 분류기를 버리지 않고 fallback으로 재사용한다. 이는 “똑똑한 방법이 실패하면 단순하고 안정적인 방법으로 대체한다”는 실무 패턴이다.

### 힌트

- 존재하지 않는 모델 이름, 잘못된 GIPHY 키 또는 항상 `ConnectionError`를 발생시키는 `RunnableLambda`로 실패 상황을 만든다.
- `requests`는 `401`이나 `500` 응답만으로 예외를 던지지 않으므로 `response.raise_for_status()`를 호출한다.
- 검색 결과가 빈 리스트일 때도 실패로 처리할지 규칙을 정한다.
- 네트워크를 무한정 기다리지 않도록 `requests.get(..., timeout=5)`를 사용한다.
- `체인.with_retry(stop_after_attempt=3).with_fallbacks([대체_체인])` 형태를 사용한다.
- LLM 체인은 dict를 받고 키워드 분류기는 문자열을 받으므로, `RunnableLambda(lambda d: d["text"])` 등으로 입력 형태를 맞춘다.

### 체크

- [ ] 실패 함수가 정확히 3번 호출된다.
- [ ] LLM이 실패해도 간단한 입력은 키워드 분류기가 처리한다.
- [ ] GIPHY 키가 잘못되어도 CATAAS 고양이가 표시된다.
- [ ] `with_retry()`와 `with_fallbacks()`의 순서를 바꿨을 때 결과를 예측하고 확인한다.

## 5단계(선택): 캡션 스트리밍

캡션 체인에 `stream()`을 사용한다.

```python
for chunk in caption_chain.stream({...}):
    print(chunk, end="", flush=True)
```

### 체크

- [ ] 캡션이 타이핑하듯 출력된다.
- [ ] 문자열 체인과 전체 dict 체인에 각각 `stream()`을 사용해 결과 차이를 관찰한다.

## 6단계(선택): GitHub Pages에 데모 올리기

GitHub Pages에서는 Python을 실행할 수 없다. 블로그 데모는 1단계의 키워드 분류기를 JavaScript로 다시 구현한다. CATAAS는 API 키가 필요 없으므로 브라우저에서 바로 요청할 수 있다.

> OpenAI API 키와 GIPHY API 키를 브라우저 JavaScript에 넣으면 개발자 도구로 누구나 확인할 수 있으므로 절대 넣지 않는다.

### 할 일

- [ ] `assets/demos/mood-cat/index.html` 만들기
- [ ] HTML, CSS, JavaScript로 입력창·버튼·이미지·캡션 영역 구현하기
- [ ] Python의 키워드 분류 로직을 JavaScript로 번역하기
- [ ] 이미지 URL 끝에 `?t=${Date.now()}`를 붙여 브라우저 캐시 피하기
- [ ] `@media (prefers-color-scheme: dark)`로 다크 모드 대응하기
- [ ] 상세 페이지에 iframe 추가하기

```html
<iframe src="/assets/demos/mood-cat/index.html"
        width="100%" height="520"
        style="border: 0; border-radius: 8px;"
        loading="lazy"
        title="Mood Cat"></iframe>
```

### 체크

- [ ] 로컬 Jekyll에서 페이지가 정상적으로 보인다.
- [ ] 모바일 화면에서 이미지가 영역 밖으로 넘치지 않는다.
- [ ] GitHub Actions 빌드가 성공한다.
- [ ] 실제 GitHub.io 페이지에 데모가 표시된다.

LLM과 GIPHY 버전은 우선 로컬 실행 화면을 GIF나 스크린샷으로 기록해도 충분하다. 나중에 공개 서버가 필요하면 다음 방법을 검토한다.

| 방법 | 특징 |
| --- | --- |
| Hugging Face Spaces + Gradio | 무료 플랜과 간단한 설정 |
| Streamlit Community Cloud | Streamlit UI에 적합한 무료 플랜 |
| FastAPI + Render/AWS | 백엔드 배포 학습에 적합 |

배포 후에는 iframe 주소를 서비스 주소로 바꾸고 API 사용량 한도를 반드시 설정한다.

## 7단계: TIL 작성

- [ ] 단계마다 새로 알게 된 내용을 한 줄씩 적는다.
- [ ] 키워드 분류기와 LLM 분류기의 결과를 비교하고 LLM을 사용하는 이유를 설명한다.
- [ ] 가장 오래 막혔던 오류와 해결 과정을 오류 메시지 원문과 함께 기록한다.
- [ ] `A | B | C`의 흐름과 `assign`이 필요한 이유를 자신의 말로 설명한다.
- [ ] “Runnable을 왜 사용하는가?”에 대한 답을 적는다.
- [ ] 6단계를 구현했다면 데모 iframe을 넣는다.

## 자주 막히는 곳

| 증상 | 확인할 부분 |
| --- | --- |
| `ModuleNotFoundError` | Python 인터프리터가 `.venv`인지 확인 |
| API key 관련 오류 | `load_dotenv()` 호출 여부와 `.env` 위치 확인 |
| `KeyError` 또는 missing variables | 프롬프트 변수와 `invoke` key가 같은지, `assign` 없이 key가 사라지지 않았는지 확인 |
| LLM이 라벨 대신 문장을 출력 | system 프롬프트에서 “라벨 하나만”을 강조하고 `temperature=0` 사용 |
| 결과가 `AIMessage(...)` | `StrOutputParser`가 빠졌는지 확인 |
| fallback 타입 오류 | LLM 체인의 dict 입력과 키워드 분류기의 문자열 입력 형태 맞추기 |
| GIPHY `401` 또는 `403` | `GIPHY_API_KEY` 철자, `.env` 저장 여부와 키 주변 공백 확인 |
| 응답은 `200`이지만 GIF가 없음 | `data`가 빈 리스트인지 확인하고 `"sad cat"`처럼 단순한 검색어 사용 |
| `KeyError: 'images'` | 실제 JSON 구조와 리스트·dict 접근 방식을 확인 |
| retry/fallback이 GIPHY 실패를 감지하지 못함 | `raise_for_status()` 호출 여부 확인 |
| 고양이 사진이 표시되지 않음 | URL과 태그 철자를 브라우저에서 직접 확인 |
| 사진이 바뀌지 않음 | URL에 현재 시각을 query parameter로 붙여 캐시 방지 |
| iframe이 비어 있음 | `/assets/...` 경로를 확인하고 로컬 Jekyll에서 먼저 테스트 |

## 참고 자료

- [11월 20일 학습 노트](https://github.com/mjlee0914/ax_study/blob/main/12_rag/1120_note.md)
- [LangChain Runnable 실습 노트북](https://github.com/mjlee0914/ax_study/blob/main/12_rag/langchain-runnable/lecture.ipynb)
- [GIPHY Developers](https://developers.giphy.com)
- [CATAAS](https://cataas.com)
