---
layout: page
title: Python으로 미니 RAG 직접 만들기
permalink: /coding/rag-from-scratch/ko/
nav_exclude: true
---

[English version](/coding/rag-from-scratch/)

## rag.py

Ollama, NumPy, Python만 사용해 RAG의 핵심 흐름을 최소한으로 구현한 예제다.

관련 학습 기록: [261117 TIL - RAG Practice](/til/2026-11/261117_TIL/)

```python
import requests
import numpy as np
from pathlib import Path

# 0단계: 모델 설정

# 서로 다른 AI 모델 호출
OLLAMA = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:4b-instruct"

# 텍스트 목록을 임베딩 벡터로 변환
def embed(texts):
    r = requests.post(
        f"{OLLAMA}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
    )
    return np.array(r.json()["embeddings"])

# 프롬프트를 LLM에 전달하고 응답 텍스트 반환
def ask_llm(prompt):
    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return r.json()["message"]["content"]

# 1단계: 문서 청킹
chunks = []
for file in Path("docs").glob("*.md"):
    chunks += [
        paragraph.strip()
        for paragraph in file.read_text(encoding="UTF-8").split("\n\n")
        if paragraph.strip()
    ]

# 2단계: 각 청크를 벡터로 변환
chunk_vectors = embed(chunks)
print(f"Indexed {len(chunks)} chunks\n")

# 3단계: 코사인 유사도로 관련 청크 검색
def retrieve(question, k=3):
    question_vector = embed([question])[0]
    scores = chunk_vectors @ question_vector / (
        np.linalg.norm(chunk_vectors, axis=1)
        * np.linalg.norm(question_vector)
    )
    return [chunks[i] for i in np.argsort(scores)[::-1][:k]]

# 4단계: 검색 결과를 문맥으로 넣어 LLM 호출
while True:
    question = input("Ask: ")
    context = "\n\n".join(retrieve(question))
    print(context)
    prompt = f"""아래 문맥만 사용해 질문에 답하세요.
문맥에 답이 없다면 '모르겠습니다'라고 답하세요.

문맥:
{context}

질문: {question}"""
    print("\n" + ask_llm(prompt) + "\n")
```

## 처리 흐름

```text
Markdown 문서
  → 문단 단위 청크
  → 임베딩 벡터
  → 질문과 코사인 유사도 비교
  → 관련 청크 3개 검색
  → 문맥과 질문을 LLM에 전달
  → 근거 기반 답변
```

- `embed()`는 문서 청크와 질문을 같은 벡터 공간으로 옮긴다.
- `retrieve()`는 코사인 유사도가 높은 청크 `k`개를 반환한다.
- 검색된 청크만 프롬프트의 문맥으로 넣어 LLM이 문서에 근거해 답하도록 제한한다.
- 문맥에 없는 내용은 모른다고 답하도록 지시해 근거 없는 생성을 줄인다.
