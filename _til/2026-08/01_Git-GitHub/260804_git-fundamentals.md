# Day 1 — Git 기초

> **강사:** 이용교 (LEE, YONGGYO)  
> **GitHub:** [yonggyo1125](https://github.com/yonggyo1125)

---

## 1. Git이란?

**Git = 형상관리(Configuration Management) / 버전관리 시스템**

작업 내용을 버전별로 기록하여 특정 시점의 상태를 확인하거나 이전 상태로 되돌릴 수 있도록 하는 도구.

### Git의 특징

- 작업 내용을 **commit 단위**로 기록
- 각 commit은 프로젝트의 특정 시점에 대한 **snapshot**을 가짐
- commit은 **SHA 해시값**으로 식별
- 로컬 저장소에 전체 이력이 존재하는 **분산형 버전관리 시스템**
- `diff`를 통해 변경된 내용을 확인할 수 있음
- 이전 commit으로 이동하거나 복구할 수 있음
- `branch`를 이용해 여러 작업 흐름을 독립적으로 관리할 수 있음

### Git 이전의 버전관리 시스템과 비교

| SVN / CVS | Git |
|---|---|
| 변경 내용(diff) 중심 | Snapshot 중심 |
| 중앙 서버 중심 | 분산형 |
| 이전 버전 복원 시 변경 내역을 적용 | 원하는 commit을 직접 참조 |
| 서버 의존도가 높음 | 로컬에도 전체 이력 보관 |
| Branch 작업이 상대적으로 무거움 | Branch 생성 및 이동이 빠름 |

> **Note:** Git도 변경 내용을 추적하지만, 사용자 관점에서는 각 commit을 프로젝트의 특정 시점에 대한 **snapshot**으로 이해하면 편리하다.

---

## 2. DOS / CMD 기본 명령어

| 명령어 | 의미 |
|---|---|
| `cd` | 디렉터리 이동 |
| `mkdir` | 디렉터리 생성 |
| `dir` | 파일 / 디렉터리 목록 확인 |
| `dir /w` | 목록을 가로로 넓게 표시 |
| `type` | 파일 내용 확인 |
| `cls` | 화면 지우기 |

### 경로 관련

```text
.   → 현재 디렉터리
..  → 부모 디렉터리
```

### 예시

```bash
cd Documents
mkdir study
cd study
```

결과:

```text
Documents/
└── study/
```

---

## 3. Git Configuration

### `git config`

Git의 사용자 정보 및 환경설정을 관리하는 명령어.

Git 설정은 크게 3가지 범위로 나뉜다.

```text
local > global > system
```

### `--system`

현재 컴퓨터의 시스템 전체에 적용.

### `--global`

현재 사용자의 모든 Git repository에 적용.

### `--local`

현재 repository에만 적용.

가장 우선순위가 높기 때문에 `local` 설정이 `global` 설정보다 우선한다.

```text
local
  ↓
global
  ↓
system
```

---

## 4. SSH Key

GitHub에 안전하게 인증하기 위해 **SSH Key**를 사용할 수 있다.

```bash
ssh-keygen -t ed25519 -C "myungjilee0914@gmail.com"
```

### 기본 개념

```text
Private Key
→ 내 컴퓨터에 보관
→ 다른 사람에게 공유하면 안 됨

Public Key
→ GitHub에 등록
```

SSH를 사용하면 GitHub에 접근할 때 비밀번호 대신 SSH Key를 이용해 인증할 수 있다.

---

## 5. Git Repository 생성 — `git init`

`git init`은 특정 디렉터리를 **Git이 관리하는 repository로 초기화**하는 명령어.

```bash
git init
```

### 예시

```bash
mkdir study
cd study
git init
```

그러면 `study` 디렉터리가 Git repository로 초기화된다.

```text
study/
└── .git/
```

`.git` 디렉터리에는 Git repository를 관리하기 위한 정보가 저장된다.

---

## 6. Working Directory

**Working Directory**는 현재 실제로 파일을 생성하고 수정하는 작업 공간.

예:

```text
study/
├── member.md
└── login.py
```

Git에서는 변경사항을 관리하는 첫 번째 영역이다.

---

## 7. Git의 3가지 영역

Git의 기본적인 작업 흐름:

```text
Working Directory
       │
       │ git add
       ↓
Staging Area
       │
       │ git commit
       ↓
Repository
```

### ① Working Directory

실제로 파일을 생성하거나 수정하는 공간.

### ② Staging Area

다음 commit에 포함할 변경사항을 선택하는 공간.

Git에서는 **Index**라고도 한다.

#### 특정 파일 staging

```bash
git add 파일명
```

#### 변경사항 전체 staging

```bash
git add .
```

### ③ Repository

commit이 실제로 기록되는 저장소.

```bash
git commit -m "메시지"
```

commit을 생성하면 해당 시점의 변경사항이 Git history에 기록된다.

---

## 8. Commit

**Commit = 특정 시점의 프로젝트 상태를 기록한 snapshot**

```bash
git commit -m "회원가입 기능 추가"
```

Commit message는 해당 commit을 설명하기 위한 **메타데이터**다.

### 중요한 점

**Commit message와 실제 파일 내용은 별개다.**

예를 들어:

```text
Commit message:
"회원가입 기능 완성"
```

이라고 작성했다고 해서 Git이 실제 파일의 내용을 자동으로 "회원가입 기능"이라고 판단하는 것은 아니다.

실제로 commit되는 파일 내용은 **Staging Area에 올라간 변경사항**을 기준으로 결정된다.

```text
Working Directory
       ↓
    git add
       ↓
Staging Area
       ↓
  git commit
       ↓
Repository
```

---

## 9. Git History 확인

### 기본 log

```bash
git log
```

commit history 확인.

### 한 줄로 보기

```bash
git log --oneline
```

예:

```text
a31f2d1 회원가입 기능 추가
72bc911 로그인 기능 추가
91ae203 프로젝트 초기화
```

### 그래프로 보기

```bash
git log --graph
```

branch의 시간적 흐름을 시각적으로 확인할 수 있다.

### 모든 branch 확인

```bash
git log --all
```

### 여러 옵션 조합

```bash
git log --oneline --graph --decorate --all
```

commit history와 branch 구조를 한눈에 확인할 때 유용하다.

---

## 10. Commit Hash

각 commit에는 고유한 **Hash 값**이 부여된다.

예:

```text
a31f2d1
```

실제 hash는 더 길지만 `git log --oneline`에서는 앞부분을 표시할 수 있다.

이 hash를 이용하여 특정 commit을 참조할 수 있다.

---

## 11. 특정 시점으로 이동

```bash
git checkout <commit-id>
```

예:

```bash
git checkout a31f2d1
```

이 명령을 실행하면 `HEAD`가 해당 commit을 가리키게 되고, 해당 시점의 프로젝트 상태를 확인할 수 있다.

### 이전 위치로 돌아가기

```bash
git checkout -
```

`-`는 이전 checkout 위치로 돌아가는 데 사용할 수 있다.

> **Modern Git:** Branch 이동에는 `git switch`를 사용하는 것이 권장된다. 특정 과거 commit을 확인할 때는 `git switch --detach <commit>`을 사용할 수 있다.

---

## 12. HEAD

**HEAD = 현재 내가 checkout한 위치를 가리키는 포인터**

예:

```text
A ← B ← C
        ↑
       main
        ↑
       HEAD
```

현재 `C` commit을 checkout한 상태라면:

```text
HEAD → C
```

특정 commit으로 이동하면:

```bash
git checkout B
```

```text
A ← B ← C
    ↑
   HEAD
```

즉, **HEAD가 현재 작업 위치를 결정한다.**

---

## 13. Branch

**Branch = 특정 commit을 가리키는 포인터**

예:

```text
A ← B ← C
        ↑
       main
```

`main`은 실제 commit 자체가 아니라 **C commit을 가리키는 포인터**다.

새로운 commit이 생성되면:

```text
A ← B ← C ← D
            ↑
           main
```

`main` 포인터도 새로운 commit으로 이동한다.

---

## 14. Commit / Branch / HEAD 관계

세 개념을 구분하는 것이 중요하다.

| 개념 | 의미 |
|---|---|
| **Commit** | 특정 시점의 프로젝트 상태를 기록한 snapshot |
| **Branch** | 특정 commit을 가리키는 포인터 |
| **HEAD** | 현재 checkout된 위치를 가리키는 포인터 |

예:

```text
A ← B ← C
        ↑
       main
        ↑
       HEAD
```

현재 상태:

```text
HEAD → main → C
```

즉,

- `C` = Commit
- `main` = C를 가리키는 Branch
- `HEAD` = 현재 `main`을 가리키는 포인터

---

## 15. 변경사항 확인

### `git diff`

Working Directory의 변경사항을 확인.

```bash
git diff
```

```text
Last Commit
     ↓
Working Directory
     ↑
   git diff
```

### `git diff --staged`

Staging Area에 올라간 변경사항과 마지막 commit의 차이를 확인.

```bash
git diff --staged
```

```text
Last Commit
     ↓
Staging Area
     ↑
git diff --staged
```

### 차이 정리

| 명령어 | 확인 대상 |
|---|---|
| `git diff` | Working Directory의 변경사항 |
| `git diff --staged` | Staging Area에 올라간 변경사항 |

---

## 16. 전체 Git Workflow

Day 1에서 배운 가장 중요한 Git workflow:

```text
① 작업

Working Directory
        │
        │ git add
        ↓
② Staging

Staging Area (Index)
        │
        │ git commit
        ↓
③ Repository

Repository
        │
        │ git log
        ↓
④ History 확인
        │
        │ git checkout <commit>
        ↓
⑤ 과거 시점 확인
```

### 핵심 명령어

```bash
git init
git status
git add .
git commit -m "message"
git log
git log --oneline
git log --graph
git diff
git diff --staged
git checkout <commit-id>
git checkout -
```

---

# 17. Day 1 핵심 정리

### Git

프로젝트의 변경사항을 **버전 단위로 관리하는 분산형 버전관리 시스템**.

### Repository

Git이 프로젝트의 버전 정보를 저장하고 관리하는 공간.

### Working Directory

실제 파일을 생성하고 수정하는 작업 공간.

### Staging Area / Index

다음 commit에 포함할 변경사항을 선택해 올려두는 공간.

### Commit

특정 시점의 프로젝트 상태를 기록한 **snapshot**.

### Commit Hash

각 commit을 식별하는 고유한 **hash 값**.

### Branch

특정 commit을 가리키는 **포인터**.

### HEAD

현재 checkout된 위치를 가리키는 **포인터**.

---

## ⭐ Day 1에서 반드시 이해할 것

### Git의 3가지 영역

```text
Working Directory
      │
      │ git add
      ↓
Staging Area
      │
      │ git commit
      ↓
Repository
      ↓
Commit History
```

### Commit / Branch / HEAD

```text
Branch → 특정 Commit을 가리킴

HEAD → 현재 위치를 가리킴
```

예:

```text
A ← B ← C
        ↑
       main
        ↑
       HEAD
```

```text
HEAD → main → C
```

### 핵심 개념

> **Git의 핵심은 단순히 파일을 저장하는 것이 아니라, 프로젝트의 상태를 commit이라는 단위로 기록하고 Branch와 HEAD 등의 포인터를 이용해 그 상태들을 이동하며 관리하는 것.**