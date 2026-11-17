---
layout: page
title: RAG From Scratch in Python
permalink: /coding/rag-from-scratch/
---

## rag.py

A minimal RAG implementation using Ollama, NumPy, and Python.

Related notes: [261117 TIL - RAG Practice](/til/2026-11/261117_TIL/)

```python
import requests
import numpy as np
from pathlib import Path

# step 0. modeling

# call different AI models
OLLAMA = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:4b-instruct" # LLM

# defining functions for Ollama to call
# for sending a request to embed model
def embed(texts):
    r = requests.post(f"{OLLAMA}/api/embed", json={"model": EMBED_MODEL, "input": texts})
    return np.array(r.json()["embeddings"])

# for sending a request to our LLM
def ask_llm(prompt):
    r = requests.post(f"{OLLAMA}/api/chat", json={
        "model": CHAT_MODEL, "stream": False,
        "messages": [{"role": "user", "content": prompt}],
    })
    return r.json()["message"]["content"]

# step 1. chunking the information
chunks = []
for file in Path("docs").glob("*.md"): # bring out any document that ends in .md
    # split paragraphs into each chunkable paragraph, adding them in the chunks list.
    chunks += [p.strip() for p in file.read_text(encoding="UTF-8").split("\n\n") if p.strip()]

# step 2. embedding
# vectorizing the chunks
chunk_vectors = embed(chunks)

# result : Indexed 28 chunks
# careful to excute it on the RAG folder!
print(f"Indexed {len(chunks)} chunks\n")


# step 3. searching for similarity

# k defines how many chunks to return for any given question
# k=3 means it will return 3 closest chunks
def retrieve(question, k=3):
    q = embed([question])[0] # converting the prompt into vector
    # create score for every single distance between question and vector
    # searching for the cosign similarity
    scores = chunk_vectors @ q / (np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(q))
    return [chunks[i] for i in np.argsort(scores)[::-1][:k]]

# step 4. calling the LLM
while True:
    question = input("Ask: ")
    context = "\n\n".join(retrieve(question))
    print(context) # you can see 3 chunks found
    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't know".

Context:
{context}

Question: {question}"""
    print("\n" + ask_llm(prompt) + "\n")

```

