---
layout: page
title: "Mood Cat: A Cat Meme Generator for Your Mood"
permalink: /coding/mood-cat/en/
nav_exclude: true
---

[한국어 버전](/coding/mood-cat/)

> “I failed my exam 😭” → 😿 a sad cat GIF + “It’s okay. I missed my treat too.”

**Goal:** Review the November 20 lesson by building with Runnable, LCEL, `@chain`, `assign`, `retry`, and `fallbacks`.

- This guide does not include the final answer code. It provides directions, hints, and checklists.
- Complete each checklist before moving on to the next step.
- When asking for help, explain the step, what you attempted, and the exact error.

---

## How It Works

```text
Input: "I failed my exam 😭"
   │
   ▼
[Mood classification] Free-form text → one mood label ("sad")  ← LLM
   │
   ▼
[Caption generation]  One line in a cat's voice                 ← LLM
   │
   ▼
[GIF search]          Search GIPHY for "sad cat" → one GIF URL  ← API call
   │
   ▼
Output: {text, mood, caption, image_url}
```

The key idea is to use the LLM only for mood classification and caption generation, while retrieving the GIF from a dedicated API. The LLM chooses a reliable mood label for the GIPHY search instead of generating an image itself.

## Image Sources

```text
Python practice (steps 0–5) → GIPHY   (API key stored in .env)  ← varied meme GIFs
Blog demo (step 6)          → CATAAS  (no API key required)    ← safe in a browser
                              ↳ also the fallback when GIPHY fails in step 4
```

### GIPHY: Main GIF Source for Python

- Search for memes with queries such as `"sad cat"`, `"sleepy cat"`, and `"hangry cat"`.
- A free API key is required. A request without a key returns `401 Unauthorized`.
- The search endpoint is `https://api.giphy.com/v1/gifs/search`.

| Item | Value |
| --- | --- |
| Main parameters | `api_key`, `q`, `limit`, `rating` |
| Recommended rating | `g` |
| Response | GIF data inside the JSON `data` list |

When creating a key, read the request limits and attribution requirements on [GIPHY Developers](https://developers.giphy.com).

### CATAAS: Fallback and Browser Demo

[CATAAS (Cat as a Service)](https://cataas.com) does not require an API key.

| URL | Result |
| --- | --- |
| `https://cataas.com/cat/happy` | A random cat tagged `happy` |
| `https://cataas.com/cat/sad/says/hi` | A cat image with `hi` overlaid |
| `https://cataas.com/cat/happy?json=true` | Image information as JSON |
| `https://cataas.com/api/tags` | All available tags |

Verified mood tags:

`happy` `sad` `angry` `sleepy` `tired` `bored` `scared` `excited` `confused` `hungry` `love` `cute` `grumpy`

Choose only five to seven labels for the app. Too many labels can make classification ambiguous.

> Free external services can become slow or unavailable, so step 4 adds fallbacks. User-created tags may not match an image perfectly. Korean text after `/says/` may also render incorrectly, so display the caption outside the image when necessary.

## Roadmap

| Step | Build | Concepts | Time |
| --- | --- | --- | --- |
| 0 | Prepare the environment and get a GIPHY key | venv, `.env` | 15 min |
| 1 | Keyword mood classifier without an LLM | `@chain`, `invoke`, `batch` | 20 min |
| 2 | LLM mood classifier | `prompt \| llm \| parser` | 30 min |
| 3 | Combine the mood, caption, and GIPHY GIF | `RunnablePassthrough.assign()`, `requests` | 40 min |
| 4 | Add LLM and GIPHY fallbacks | `.with_retry()`, `.with_fallbacks()` | 25 min |
| 5 (optional) | Stream the caption | `.stream()` | 15 min |
| 6 (optional) | Embed a browser demo in the blog | HTML, JavaScript, Jekyll | 40 min |
| 7 | Write a TIL | Review and reflection | 20 min |

## Step 0: Prepare the Environment

### Tasks

- [ ] Work inside `12_rag/side_cat/`.
- [ ] Use the existing `ax_study/.venv` environment.
- [ ] Confirm that VS Code uses `.venv` as its Python interpreter.
- [ ] Load the OpenAI API key from `12_rag/.env` with `load_dotenv()`.
- [ ] Create an API app at [GIPHY Developers](https://developers.giphy.com) and get a key.
- [ ] Add `GIPHY_API_KEY=your-key` to `12_rag/.env`.
- [ ] Confirm that `requests` is installed in `.venv`.
- [ ] Open `https://cataas.com/cat/happy` to test the fallback image service.

### Hints and Checks

- Run `which python` and verify that the path contains `.venv`.
- `load_dotenv()` searches from the current file's directory toward its parents. Test this behavior because notebooks may behave differently.
- [ ] `import langchain_core` runs without an error.
- [ ] Both `OPENAI_API_KEY` and `GIPHY_API_KEY` are not `None`.
- [ ] A basic GIPHY request made with `requests.get(..., params={...})` returns status `200`.

> Never print API key values. Keep `.env` in `.gitignore`, never commit it, and never paste a key into source code.

## Step 1: Keyword Mood Classifier

File: `step1_keyword.py`

### Target Behavior

```text
invoke("happy")                         → "happy"
invoke("I'm so sleepy")                 → "sleepy"
invoke("asdfgh")                        → "confused"
batch(["happy", "hungry", "angry"])   → ["happy", "hungry", "angry"]
```

### Decide Before Coding

- [ ] Choose five to seven mood labels.
- [ ] Define Korean and English keywords for each label.
- [ ] Choose a default label when nothing matches.
- [ ] Define a priority rule when multiple keywords match.

### Hint

```text
Create a dict: label → list of keywords
Function decorated with @chain
  └─ convert the input to lowercase
  └─ loop through labels and check for matching keywords
  └─ return the matching label, or the default at the end
```

### Checklist

- [ ] `invoke()` works.
- [ ] `batch()` works even though you did not implement it yourself.
- [ ] You can explain why a phrase such as “I failed my exam” may defeat the keyword classifier and motivate step 2.

## Step 2: LLM Mood Classifier

File: `step2_llm_mood.py`

### Target Behavior

```text
invoke({"text": "I failed my exam 😭"})       → "sad"
invoke({"text": "It's finally Friday!!"})    → "excited"
invoke({"text": "This meeting is endless"}) → "tired"
```

The result must be one of the labels chosen in step 1.

### Hints

Build three blocks:

1. `ChatPromptTemplate.from_messages([...])`
   - System: return exactly one lowercase label.
   - Human: `{text}`
2. `ChatOpenAI(model=...)`
   - Use the model from class and prefer `temperature=0` for classification.
3. `StrOutputParser()`

Connect the blocks with `|`. The `{text}` prompt variable must match the key passed to `invoke()`.

### Experiments and Checks

- [ ] Add a cleanup stage for values such as `"Sad."`.
- [ ] Replace results outside the allowed labels with a default.
- [ ] Explore `with_structured_output()` and `Literal` to constrain the output.
- [ ] Let the LLM create a GIPHY query directly and compare its humor and reliability with fixed labels.
- [ ] Test five inputs with `batch()`.
- [ ] Explain the role of every component in `A | B | C`.

## Step 3: Combine Mood, Caption, and GIPHY GIF

File: `step3_assign.py`

### Target Output

```python
{
    "text": "I failed my exam 😭",
    "mood": "sad",
    "caption": "It's okay. I missed my treat too.",
    "image_url": "https://media.giphy.com/media/...",
}
```

### Hints

- Start with a dict: `{"text": "..."}`.
- Add the mood with `RunnablePassthrough.assign(mood=step_2_chain)`.
- Add the caption with another `assign()`, using both `{text}` and `{mood}` in its prompt.
- Add a GIPHY search function decorated with `@chain` as the final `assign()` stage. An ordinary function can become a Runnable and join the chain.
- Build `f"{mood} cat"`, call the API with `requests.get()`, choose an item from `data`, and return a URL from its `images` object.
- Pretty-print one response with `json.dumps(..., indent=2)` to inspect its structure.
- Request 10–25 results and use `random.choice()` to vary the GIF.

### Experiments and Checks

- [ ] Replace `assign()` with a plain `|` and observe how losing `text` can cause a `KeyError`.
- [ ] The result contains `text`, `mood`, `caption`, and `image_url`.
- [ ] The URL opens a cat GIF appropriate for the mood.
- [ ] The same text produces different GIFs across three runs.
- [ ] The complete chain works with three sentences through `batch()`.

## Step 4: Always Return a Cat

File: `step4_resilience.py`

| Failure | Retry | Fallback after retries fail |
| --- | --- | --- |
| LLM mood classification | 3 times | Step 1 keyword classifier |
| LLM caption generation | 3 times | `...meow? (The server is napping.)` |
| GIPHY search | 3 times | `https://cataas.com/cat/{mood}` |

This reuses the simple classifier from step 1 instead of throwing it away. It follows a practical pattern: try the smarter method first, then fall back to a simpler and more reliable method.

### Hints

- Simulate failures with a nonexistent model, an invalid GIPHY key, or a `RunnableLambda` that always raises `ConnectionError`.
- `requests` does not raise an exception for `401` or `500` responses automatically. Call `response.raise_for_status()` so retry and fallback can detect the failure.
- Decide whether an empty `data` list counts as failure.
- Add `timeout=5` to avoid waiting forever.
- Use `chain.with_retry(stop_after_attempt=3).with_fallbacks([fallback_chain])`.
- Match input shapes: the LLM chain receives a dict while the keyword classifier receives a string. Adapt the input with a stage such as `RunnableLambda(lambda d: d["text"])`.

### Checklist

- [ ] The failing function is called exactly three times.
- [ ] Simple inputs still work through the keyword classifier when the LLM fails.
- [ ] An invalid GIPHY key still produces a CATAAS cat.
- [ ] You can predict and test what changes when retry and fallback are reversed.

## Step 5 (Optional): Stream the Caption

Use `stream()` on the caption chain.

```python
for chunk in caption_chain.stream({...}):
    print(chunk, end="", flush=True)
```

- [ ] The caption appears as if it is being typed.
- [ ] Compare streaming a string chain with streaming the complete dict chain.

## Step 6 (Optional): Publish a Browser Demo

GitHub Pages cannot run Python. Rebuild the step 1 keyword classifier in JavaScript and use CATAAS because it does not require a key.

> Never put an OpenAI or GIPHY API key in browser JavaScript. Anyone can read it through developer tools.

### Tasks

- [ ] Create `assets/demos/mood-cat/index.html` without Jekyll front matter.
- [ ] Build the input, button, image, and caption in one HTML/CSS/JavaScript file.
- [ ] Translate the Python keyword logic into JavaScript.
- [ ] Append `?t=${Date.now()}` to the image URL to avoid browser caching.
- [ ] Support dark mode with `@media (prefers-color-scheme: dark)`.
- [ ] Embed the demo in the study page.

```html
<iframe src="/assets/demos/mood-cat/index.html"
        width="100%" height="520"
        style="border: 0; border-radius: 8px;"
        loading="lazy"
        title="Mood Cat"></iframe>
```

For a future hosted LLM and GIPHY version, consider:

| Option | Notes |
| --- | --- |
| Hugging Face Spaces + Gradio | Free plan and simple setup |
| Streamlit Community Cloud | Useful for a Streamlit UI |
| FastAPI + Render/AWS | Useful for backend deployment practice |

Replace the iframe URL after deployment and always configure an API spending limit.

## Step 7: Write a TIL

- [ ] Write one new lesson from each step.
- [ ] Compare the keyword and LLM classifiers and explain why the LLM helps.
- [ ] Record the hardest error and the solution, including the original error message.
- [ ] Explain `A | B | C` and why `assign()` is necessary in your own words.
- [ ] Answer: “Why use Runnable?”
- [ ] Add the demo iframe if you completed step 6.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `ModuleNotFoundError` | Confirm that the interpreter is `.venv` |
| API key error | Check `load_dotenv()` and the `.env` location |
| `KeyError` or missing variables | Match prompt variables and `invoke` keys; make sure a key was not lost without `assign()` |
| LLM returns a sentence instead of a label | Emphasize “one label only” and use `temperature=0` |
| Result is `AIMessage(...)` | Add `StrOutputParser` |
| Fallback type error | Match the dict input and string input shapes |
| GIPHY `401` or `403` | Check the `GIPHY_API_KEY` name, `.env`, and surrounding whitespace |
| Status `200` but no GIF | Check for an empty `data` list and simplify the query |
| `KeyError: 'images'` | Inspect the JSON structure and list/dict access |
| Retry does not detect a GIPHY failure | Call `raise_for_status()` |
| Cat image does not load | Open the URL directly and check the tag spelling |
| Image does not change in the blog | Add `?t=Date.now()` to avoid caching |
| Empty iframe | Check the `/assets/...` path and test with local Jekyll |

## References

- [November 20 study notes](https://github.com/mjlee0914/ax_study/blob/main/12_rag/1120_note.md)
- [LangChain Runnable practice notebook](https://github.com/mjlee0914/ax_study/blob/main/12_rag/langchain-runnable/lecture.ipynb)
- [GIPHY Developers](https://developers.giphy.com)
- [CATAAS](https://cataas.com)
