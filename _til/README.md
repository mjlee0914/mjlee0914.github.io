# KANT-2026-TIL

**August 4, 2026 - May 14, 2027**

> AI Engineer Bootcamp Learning and Project Records

## About

With the goal of becoming an **AI Engineer**, I study **Python, Git, SQL, Data Analysis, Machine Learning, Backend Development**, and more.

This repository documents my learning journey, practice notes, troubleshooting records, and project problem-solving process.

## Purpose

The TILs in this repository are not simply daily learning records.

They are intended to serve as a personal **Knowledge Base** that connects:

```text
Learning
→ Practice
→ Problem Solving
→ Project Application
→ Portfolio
→ Resume
```

## Blog Sync

This repository is the source repository for my TIL notes.

Daily TIL notes are written here first. Markdown files pushed to this repository can be synced to my GitHub Pages blog:

```text
KANT-2026-TIL
→ mjlee0914.github.io/_til/
→ https://mjlee0914.github.io/til/
```

The GitHub Pages repository already has a Jekyll `_til` collection ready for these notes.

## Structure

```text
00_meta/                         # Learning roadmap, tech stack, achievements
01_Git-GitHub/                   # Git and GitHub notes
02_python/                       # Python notes and practice files
03_numpy-pandas-matplotlib/      # Data analysis basics
04_machine-learning/             # Machine learning notes and experiments
05_SQL/                          # SQL and database notes
2026-09/                         # Monthly TIL markdown notes
supabase-team-study/             # Supabase team study materials
```

## TIL Format

Each TIL is generally organized using the following format:

```text
Today's Goal
Key Concepts
Practice
Daily Quest
Troubleshooting
Key Takeaways
Reflection
Evidence
```

## Blog Post Format

For TIL notes that should appear on the blog, use Markdown and include front matter at the top of the file.

```markdown
---
title: SQL Subquery 정리
date: 2026-09-14
tags: [SQL, Subquery]
style: fill
color: primary
description: WHERE절 서브쿼리를 공부하며 정리한 내용.
---

## Today's Goal

Write your note here.
```

Recommended location:

```text
2026-09/260914_sql-subquery.md
```

When synced to the blog, this note is copied into:

```text
mjlee0914.github.io/_til/2026-09/260914_sql-subquery.md
```

## File Naming

For Markdown TIL notes:

```text
YYMMDD_topic.md
```

For notebook practice files:

```text
YYMMDD_topic.ipynb
```

### Examples

```text
260908_sql-join.md
260914_sql-subquery.md
260812_python-function.ipynb
```

## Daily Workflow

```text
1. Write today's TIL in this repository.
2. Commit and push to main.
3. GitHub Actions syncs Markdown files to mjlee0914.github.io.
4. The note appears on the TIL page of the blog.
```

## Project Records

Project-related learning, decisions, and troubleshooting should be recorded with enough context to explain:

```text
What I tried
What failed
What I changed
What I learned
How it can be reused later
```
