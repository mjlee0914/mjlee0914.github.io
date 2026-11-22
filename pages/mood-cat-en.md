---
layout: page
title: "Mood Cat: A Cat Meme Generator for Your Mood"
permalink: /coding/mood-cat/en/
nav_exclude: true
---

[한국어 버전](/coding/mood-cat/)

## What I Built

Mood Cat is a bilingual web app that turns a sentence about how you feel into a mood label, a cat-style caption, and a matching cat GIF.

> “I totally bombed my exam :(” → `sad` → a sad cat GIF + a one-line cat caption

[Try the live demo](https://mjlee0914.github.io/mood-cat/) · [View the GitHub repository](https://github.com/mjlee0914/mood-cat)

> The backend runs on Render's free plan, so the first request may take a moment while the server wakes up.

I built this mini project to turn the LangChain Runnable and LCEL concepts from class into a complete application. The intentionally janky interface is inspired by 2007 homepages and Korean school presentation slides.

---

## How It Works

```text
User's sentence
      │
      ▼
[LLM mood classifier]  free text → one fixed mood label
      │
      ▼
[LLM caption writer]   one line in the user's language
      │
      ▼
[GIPHY search]         "{mood} cat" → one GIF URL
      │
      ▼
{ text, mood, caption, image_url }
```

The LLM handles the two tasks that need an understanding of language: classifying the sentence and writing the caption. GIPHY supplies the image, which avoids the cost and delay of generating one.

The frontend sends a `POST /mood` request to the FastAPI server. The server runs the LCEL chain and returns a typed response containing the original text, mood, caption, and GIF URL.

## The LCEL Pipeline

The main chain starts with `{"text": "..."}` and uses `RunnablePassthrough.assign()` to add one value at a time without losing earlier data.

```python
mood_cat_chain = (
    RunnablePassthrough.assign(mood=mood_step)
    | RunnablePassthrough.assign(caption=caption_step)
    | RunnablePassthrough.assign(image_url=giphy_step)
)
```

This was the key reason to use `assign()`: the caption stage needs both `text` and `mood`, while the final response still needs every value created earlier in the pipeline.

The classifier uses a fixed label set shared with the keyword fallback:

`go_home` · `poop` · `hungry` · `sleepy` · `angry` · `sad` · `anxious` · `hurt` · `embarrassed` · `happy` · `neutral`

The LLM must return exactly one label. Any value outside the allowed list becomes `neutral`, keeping the following GIPHY query predictable.

## Resilience: Always Return a Cat

Each external step is wrapped with retry and fallback behavior, so a temporary API failure does not immediately break the entire experience.

| Step | Retry | Fallback |
| --- | --- | --- |
| Mood classification | Up to 3 attempts | Local Korean keyword classifier |
| Caption generation | Up to 3 attempts | `서버가 낮잠중이다냥` |
| GIPHY search | Up to 3 attempts | A fixed cat GIF |

The fallback classifier is deliberately simpler than the LLM. It cannot understand every sentence or handle all negations, but it has no API dependency and can still return a useful label when the smarter method is unavailable.

## Frontend Experience

The frontend is built with plain HTML, CSS, and JavaScript. It includes:

- English and Korean modes, initially selected from the browser language
- an intentionally annoying escape button, fake button, cookie dialogs, and nagging timer
- a mouse rainbow trail, click explosions, and typewriter captions
- generated “meow,” “boom,” and 8-bit background music using the Web Audio API
- a reduced-motion mode for users who disable animations in their system settings

No audio files are shipped with the site. The effects and music are synthesized in the browser.

## Tech Stack

| Part | Technology |
| --- | --- |
| AI pipeline | Python, LangChain Core, LangChain OpenAI, LCEL |
| Backend | FastAPI, Pydantic, Uvicorn |
| GIF search | GIPHY API |
| Frontend | HTML, CSS, JavaScript, GSAP, Web Audio API |
| Deployment | Render for the API, GitHub Pages for the frontend |

API keys remain on the backend in environment variables. The browser never receives the OpenAI or GIPHY key, and FastAPI CORS only allows the local development URLs and the deployed GitHub Pages origin.

## Deployment Architecture

```text
GitHub Pages frontend
        │  POST /mood
        ▼
Render FastAPI backend
        ├── OpenAI API: mood + caption
        └── GIPHY API: matching cat GIF
```

- Pushing frontend changes to `main` runs a GitHub Actions workflow that deploys only the `frontend/` directory.
- `render.yaml` defines the backend build command, start command, health check, and required environment variables.
- `GET /health` provides a lightweight deployment health check.

## What I Learned

- **LCEL became clearer after building a real data flow.** The pipe syntax is not only shorter code; it makes the input and output shape of every stage important.
- **`assign()` preserves context.** Replacing the whole value at each stage would lose fields needed by later prompts and by the API response.
- **Fallbacks should have fewer dependencies.** A local keyword classifier is less capable than an LLM but remains available when the network or model fails.
- **Secrets belong on the server.** Moving the LangChain pipeline behind FastAPI made it possible to publish the frontend without exposing API keys.
- **Deployment is part of the application.** CORS, cold starts, health checks, and separate frontend/backend URLs all affected the final user experience.

## Run It Locally

```bash
git clone https://github.com/mjlee0914/mood-cat.git
cd mood-cat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add `OPENAI_API_KEY` and `GIPHY_API_KEY` to `.env`, then run the backend and frontend in separate terminals:

```bash
# Terminal 1
uvicorn api:app --reload

# Terminal 2
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`. The FastAPI documentation is available at `http://127.0.0.1:8000/docs`.

## Links

- [Live demo](https://mjlee0914.github.io/mood-cat/)
- [GitHub repository](https://github.com/mjlee0914/mood-cat)
- [November 20 study notes](https://github.com/mjlee0914/ax_study/blob/main/12_rag/1120_note.md)
- [LangChain Runnable practice notebook](https://github.com/mjlee0914/ax_study/blob/main/12_rag/langchain-runnable/lecture.ipynb)
