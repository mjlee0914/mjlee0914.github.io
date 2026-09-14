# Day 2 — Git Workflow, Branch & Remote Repository

> **학습 주제:** Staging, Commit, Reset, Revert, Branch, Merge, Rebase, Stash, Remote Repository

---

## 1. Staging + Commit Workflow

Git에서 변경사항을 commit하기 전에 현재 파일 상태를 확인하고, 필요한 변경사항만 staging한 뒤 commit한다.

### 전체 Workflow

```text
Working Directory
       │
       │ git status
       ↓
변경사항 확인
       │
       │ git add / git add -p
       ↓
Staging Area
       │
       │ git diff --staged
       ↓
Staged 변경사항 확인
       │
       │ git commit
       ↓
Repository
```

### ① 현재 상태 확인

`git add`하기 전에 `git status`로 현재 파일 상태를 확인한다.

```bash
git status
```

### ② Staging

전체 변경사항을 staging:

```bash
git add .
```

특정 파일만 staging:

```bash
git add 파일명
```

변경사항의 일부만 staging:

```bash
git add -p
```

> `git add -p`는 파일 전체가 아니라 변경사항의 일부를 선택하여 staging할 수 있다.

### ③ Staging된 변경사항 확인

```bash
git diff --staged
```

마지막 commit인 `HEAD`와 Staging Area의 차이를 확인한다.

```text
Last Commit (HEAD)
        │
        │ 비교
        ↓
Staging Area
```

### ④ Commit

```bash
git commit -m "메시지"
```

Commit message에는 해당 commit에서 **어떤 작업을 했는지** 명확하게 작성하는 것이 관례다.

---

# 2. Commit Message Convention

Commit message는 작업의 성격을 나타내는 prefix를 사용하는 것이 일반적이다.

| Prefix | 의미 | 예시 |
|---|---|---|
| `feat` | 새로운 기능 추가 | `feat: add order form` |
| `fix` | 버그 수정 | `fix: resolve login error` |
| `docs` | 문서 수정 | `docs: update README` |
| `refactor` | 코드 리팩토링 | `refactor: simplify login logic` |
| `chore` | 기타 작업 / 설정 변경 | `chore: update dependencies` |
| `test` | 테스트 추가 / 수정 | `test: add login test` |

### 예시

```text
feat: 회원가입 기능 추가
fix: 로그인 오류 수정
docs: README 작성
refactor: 로그인 로직 개선
chore: 프로젝트 설정 변경
test: 회원가입 테스트 추가
```

### Commit 작성 원칙

> **Commit은 기능 단위로 작게 쪼개서 작성한다.**

예:

```text
feat: 회원가입 API 추가
feat: 회원가입 유효성 검사 추가
test: 회원가입 API 테스트 추가
docs: 회원가입 API 문서 작성
```

---

# 3. 변경사항 되돌리기

Git에서 변경사항을 되돌리는 방법은 목적에 따라 다르다.

주요 명령어:

```text
git reset
git reflog
git revert
git restore
```

---

## 3-1. `git reset`

특정 commit 이후의 상태를 이전으로 되돌린다.

```bash
git reset <옵션> <commit>
```

### `--soft`

**Commit만 취소**

```bash
git reset --soft HEAD~
```

- Commit 취소
- Staging Area 유지
- Working Directory 유지
- 파일 내용 유지

```text
Commit       ❌ 취소
Staging      ✅ 유지
Working Dir  ✅ 유지
```

---

### `--mixed`

**Commit + Staging 취소**

```bash
git reset --mixed HEAD~
```

`--mixed`는 `git reset`의 기본 옵션이다.

- Commit 취소
- Staging Area 취소
- Working Directory의 파일 내용은 유지

```text
Commit       ❌ 취소
Staging      ❌ 취소
Working Dir  ✅ 유지
```

---

### `--hard`

**Commit + Staging + Working Directory 변경사항까지 되돌림**

```bash
git reset --hard HEAD~
```

- Commit 취소
- Staging Area 취소
- Working Directory 변경사항 취소

```text
Commit       ❌
Staging      ❌
Working Dir  ❌
```

> ⚠️ `--hard`는 작업 중이던 파일 변경사항까지 삭제할 수 있으므로 주의해서 사용한다.

### Reset 비교

| 옵션 | Commit | Staging | Working Directory |
|---|---|---|---|
| `--soft` | 취소 | 유지 | 유지 |
| `--mixed` | 취소 | 취소 | 유지 |
| `--hard` | 취소 | 취소 | 취소 |

---

## 3-2. `git reflog`

```bash
git reflog
```

`reset`이나 branch 이동 등으로 `HEAD`가 이동한 기록을 확인할 수 있다.

삭제하거나 되돌린 commit도 **reflog를 이용해 다시 찾을 수 있는 경우가 있다.**

예:

```text
HEAD@{0}
HEAD@{1}
HEAD@{2}
```

### 복구 예시

```bash
git reflog
git reset --hard <commit-id>
```

또는 branch를 특정 commit으로 복구:

```bash
git branch 새브랜치명 <commit-id>
```

---

## 3-3. `HEAD~`

`HEAD~`는 현재 HEAD의 **직전 commit**을 의미한다.

```bash
git reset --soft HEAD~
```

### 여러 단계 이동

```text
HEAD~1
→ 직전 commit

HEAD~2
→ 2단계 전 commit

HEAD~3
→ 3단계 전 commit
```

---

## 3-4. `git revert`

기존 commit을 삭제하거나 history를 변경하지 않고, 해당 commit의 변경사항을 **반대로 적용하는 새로운 commit**을 생성한다.

```bash
git revert <commit-id>
```

예:

```text
A ← B ← C
        ↑
      revert
```

revert 후:

```text
A ← B ← C ← D
```

`D`가 `C`의 변경사항을 반대로 적용한 새로운 commit이다.

### 언제 사용하는가?

특히 이미 원격 repository에 push되어 다른 사람과 공유된 commit을 되돌릴 때 안전하다.

> **공유된 history를 변경하지 않고 새로운 commit으로 되돌린다.**

---

## 3-5. `git restore`

파일의 변경사항을 복구하거나 staging을 취소할 때 사용한다.

### Working Directory 변경사항 복구

```bash
git restore 파일명
```

### Staging 취소

```bash
git restore --staged 파일명
```

### 역할

```text
git restore
→ 파일의 변경사항 복구
→ staging 취소
```

> Git 2.23부터 `git switch`와 `git restore`가 도입되어 branch 전환과 파일 복구의 역할이 명확하게 분리되었다.

---

# 4. Branch

Branch는 독립적인 작업 흐름을 만들기 위해 사용한다.

```text
main
 │
 └── feature/login
```

기능별로 branch를 생성하여 작업한 뒤 완성되면 `main` 또는 `dev`에 merge할 수 있다.

---

## 4-1. Branch 생성

```bash
git branch 브랜치명
```

예:

```bash
git branch feature/login
```

---

## 4-2. 현재 Branch 확인

```bash
git branch
```

현재 checkout된 branch에는 `*`가 표시된다.

예:

```text
* main
  feature/login
  feature/signup
```

---

## 4-3. Branch 이동

```bash
git checkout 브랜치명
```

예:

```bash
git checkout feature/login
```

`HEAD`가 해당 branch로 이동한다.

---

## 4-4. Branch 생성 + 이동

```bash
git checkout -b 브랜치명
```

예:

```bash
git checkout -b feature/login
```

Branch를 생성하고 바로 해당 branch로 이동한다.

---

## 4-5. `git switch`

최신 Git에서는 branch 전환에 `git switch` 사용을 권장한다.

```bash
git switch 브랜치명
```

예:

```bash
git switch feature/login
```

### Branch 생성 + 이동

```bash
git switch -c 브랜치명
```

예:

```bash
git switch -c feature/login
```

### `checkout` vs `switch`

```text
git checkout
→ 여러 기능을 수행하는 기존 명령어

git switch
→ Branch 전환에 특화된 명령어

git restore
→ 파일 복구에 특화된 명령어
```

> Git 2.23부터 `git switch`와 `git restore`를 통해 branch 전환과 파일 복구의 역할이 분리되었다.

---

# 5. Branch Naming Convention

Branch 이름은 작업 목적을 명확하게 표현하도록 작성한다.

| Prefix | 용도 | 예시 |
|---|---|---|
| `feature/` | 새로운 기능 | `feature/order-form` |
| `fix/` | 일반적인 버그 수정 | `fix/login-error` |
| `bugfix/` | 버그 수정 | `bugfix/payment-error` |
| `hotfix/` | 긴급 수정 | `hotfix/server-error` |
| `chore/` | 기타 작업 | `chore/update-config` |
| `release/` | 배포 준비 | `release/v1.0.0` |
| `test/` | 테스트 작업 | `test/login` |
| `docs/` | 문서 작업 | `docs/readme` |
| `dev/` | 개발 통합 branch | `dev` |

### 예시

```text
feature/order-form
feature/login
feature/rag-pipeline

fix/login-error
fix/api-timeout

docs/readme
test/login
chore/update-dependencies
```

---

# 6. Branch와 Commit 관계

Branch는 commit 자체가 아니라 **특정 commit을 가리키는 포인터**다.

```text
A ← B ← C
        ↑
       main
```

새로운 commit을 생성하면:

```text
A ← B ← C ← D
            ↑
           main
```

Branch pointer가 새로운 commit으로 이동한다.

---

# 7. Branch Merge

다른 branch에서 작업한 내용을 현재 branch에 합친다.

```bash
git merge 병합할_브랜치명
```

예:

```bash
git switch main
git merge feature/login
```

의미:

```text
feature/login
      │
      │ merge
      ↓
     main
```

---

## 7-1. Fast-Forward Merge

현재 branch에 별도의 commit이 없고, 단순히 branch pointer를 앞으로 이동할 수 있는 경우.

```text
A ← B ← C
         ↑
    feature/login

main → B
```

merge 후:

```text
A ← B ← C
        ↑
       main
```

별도의 merge commit이 생성되지 않는다.

---

## 7-2. Merge Commit

두 branch에서 각각 새로운 commit이 발생하여 history가 갈라진 경우.

```text
      ← C
     /
A ← B
     \
      ← D
```

merge 후:

```text
      ← C
     /   \
A ← B     M
     \   /
      ← D
```

`M`이라는 새로운 merge commit이 생성된다.

두 branch의 history가 모두 유지된다.

---

## 7-3. Conflict

두 branch에서 동일한 부분을 다르게 수정하면 merge 과정에서 **conflict**가 발생할 수 있다.

```text
Branch A
   ↓
같은 코드 수정

Branch B
   ↓
같은 코드 수정

      ↓

   CONFLICT
```

### Conflict 해결 과정

1. 충돌 파일 확인
2. 충돌 부분 직접 수정
3. 수정된 파일 staging
4. merge 완료

```bash
git status
git add .
git commit
```

---

## 7-4. Branch 삭제

merge가 완료된 branch는 삭제할 수 있다.

### 일반 삭제

```bash
git branch -d 브랜치명
```

### 강제 삭제

```bash
git branch -D 브랜치명
```

`-D`는 merge 여부와 관계없이 branch를 강제로 삭제한다.

### 삭제한 Branch 복구

```bash
git reflog
```

commit ID 확인 후:

```bash
git branch 새브랜치명 <commit-id>
```

---

# 8. Branch 이름 변경

현재 checkout된 branch의 이름 변경:

```bash
git branch -m 변경할_브랜치명
```

강제 변경:

```bash
git branch -M 변경할_브랜치명
```

예:

```bash
git switch main
git branch -m master
```

> `-m`은 일반적인 이름 변경, `-M`은 강제 이름 변경이다.

---

# 9. Rebase

**Rebase = 현재 branch의 commit들을 다른 최신 commit 위에 다시 쌓는 것**

예:

```text
      C ← D   feature
     /
A ← B
     \
      E       main
```

rebase를 수행하면 feature branch의 commit들이 최신 main 위에 다시 적용된다.

```text
A ← B ← E ← C' ← D'
             ↑
          feature
```

기존 `C`, `D`와 새로 만들어진 `C'`, `D'`는 서로 다른 commit이다.

### Rebase의 특징

- History를 직선형으로 정리할 수 있음
- 불필요한 merge commit을 줄일 수 있음
- Commit hash가 새로 생성됨
- 기존 commit history가 변경됨

---

## 9-1. Merge vs Rebase

### Merge

```text
      C
     / \
A ← B   M
     \ /
      D
```

- 두 branch의 history를 모두 유지
- merge commit이 생성될 수 있음
- history가 복잡해질 수 있음

### Rebase

```text
A ← B ← D ← C' ← D'
```

- history가 직선적으로 정리됨
- merge commit을 줄일 수 있음
- commit이 새로운 hash로 다시 생성됨

### 핵심 차이

```text
merge
→ 두 history를 하나로 연결

rebase
→ 내 commit들을 최신 위치 위에 다시 쌓음
```

---

## 9-2. Rebase의 황금률

> **다른 사람이 이미 가져갔거나(pull) 공유하고 있는 commit에는 rebase하지 않는다.**

Rebase는 기존 commit을 새로운 commit으로 다시 만들기 때문에 commit history가 변경된다.

따라서 이미 원격 repository에 push했고 다른 사람이 해당 commit을 사용하고 있다면 rebase를 피하는 것이 안전하다.

```text
공유되지 않은 개인 branch
→ rebase 가능

이미 다른 사람이 사용하는 branch
→ rebase 지양
```

---

## 9-3. Rebase Conflict

Rebase 과정에서 conflict가 발생할 수 있다.

### ① 충돌 해결

충돌 파일을 직접 수정한다.

### ② Staging

```bash
git add .
```

### ③ Rebase 계속 진행

```bash
git rebase --continue
```

### 현재 commit 건너뛰기

```bash
git rebase --skip
```

### Rebase 취소

```bash
git rebase --abort
```

---

# 10. `git commit -a`

파일을 수정한 경우 `add`와 `commit`을 한 번에 수행할 수 있다.

```bash
git commit -a -m "메시지"
```

또는:

```bash
git commit -am "메시지"
```

> ⚠️ `git commit -a`는 이미 Git이 추적하고 있는(tracked) 파일의 수정/삭제만 자동으로 staging한다. 새로 생성한 untracked 파일은 포함하지 않는다.

---

# 11. Commit하지 않은 상태에서 Branch 전환

작업 중인 변경사항이 있는 상태에서 branch를 전환하면 충돌이나 오류가 발생할 수 있다.

이때 `git stash`를 사용하여 작업 내용을 임시 저장할 수 있다.

---

## 11-1. `git stash`

```bash
git stash
```

현재 작업 중인 변경사항을 임시 저장한다.

이후 branch를 전환할 수 있다.

```bash
git stash
git switch 다른브랜치
```

---

## 11-2. Stash 목록 확인

```bash
git stash list
```

저장된 stash 목록을 확인한다.

예:

```text
stash@{0}
stash@{1}
stash@{2}
```

---

## 11-3. Stash 복원

```bash
git stash pop
```

가장 최근 stash를 복원하고 stash 목록에서 제거한다.

```text
git stash
    ↓
임시 저장
    ↓
branch 전환
    ↓
git stash pop
    ↓
작업 복원
```

---

# 12. Git 도움말

Git 명령어의 사용법을 확인할 수 있다.

```bash
git help <명령어>
```

예:

```bash
git help commit
git help branch
git help rebase
```

터미널에서 Git 명령어의 상세한 documentation을 확인할 수 있다.

---

# 13. Local Repository ↔ Remote Repository

Git은 로컬 repository와 원격 repository를 연결하여 사용할 수 있다.

```text
Local Repository
       │
       │ push
       ↓
Remote Repository
(GitHub)
       │
       │ pull
       ↓
Local Repository
```

### Local → Remote

```bash
git push
```

### Remote → Local

```bash
git pull
```

---

# 14. Remote Repository 연결

### 현재 Remote 확인

```bash
git remote
```

더 자세히 확인:

```bash
git remote -v
```

---

## 14-1. Remote 최초 연결

```bash
git remote add origin <SSH 주소>
```

예:

```bash
git remote add origin git@github.com:mjlee0914/KANT-2026-TIL.git
```

### `origin`

`origin`은 원격 repository를 가리키는 **관습적인 별칭(alias)**이다.

```text
origin
  ↓
GitHub Repository
```

---

## 14-2. Remote URL 변경

```bash
git remote set-url origin <SSH 주소>
```

예:

```bash
git remote set-url origin git@github.com:mjlee0914/KANT-2026-TIL.git
```

---

# 15. Local → Remote : `git push`

원격 repository로 변경사항을 업로드한다.

```bash
git push origin 브랜치명
```

예:

```bash
git push origin main
```

---

## 15-1. Upstream 설정

처음 push할 때 로컬 branch와 원격 branch를 연결할 수 있다.

```bash
git push -u origin main
```

`-u`는 upstream branch를 설정한다.

이후에는:

```bash
git push
```

만 입력해도 연결된 원격 branch로 push할 수 있다.

```text
Local main
    │
    │ upstream
    ↓
origin/main
```

---

# 16. Remote → Local : `git pull`

원격 repository의 변경사항을 가져와 현재 branch에 반영한다.

```bash
git pull origin 브랜치명
```

예:

```bash
git pull origin main
```

upstream이 설정되어 있다면:

```bash
git pull
```

만으로도 가능하다.

---

# 17. `git fetch` vs `git pull`

둘은 비슷해 보이지만 역할이 다르다.

### `git fetch`

원격 repository의 최신 정보를 가져오지만 **현재 작업 branch에 자동으로 반영하지 않는다.**

```bash
git fetch
```

### `git pull`

원격 repository의 변경사항을 가져온 후 현재 branch에 반영한다.

```bash
git pull
```

개념적으로:

```text
git pull
≈
git fetch
+
git merge
```

또는 설정에 따라 fetch 후 rebase 방식으로 동작할 수도 있다.

### 핵심 차이

| 명령어 | 역할 |
|---|---|
| `git fetch` | 원격 변경사항 확인 / 가져오기 |
| `git pull` | 원격 변경사항을 가져와 현재 branch에 반영 |

---

# 18. Git vs GitHub

Git과 GitHub는 서로 다른 개념이다.

| Git | GitHub |
|---|---|
| Version Control System | Git Repository Hosting Service |
| 로컬에서 실행되는 소프트웨어 | 웹 기반 서비스 |
| 프로젝트의 버전과 history 관리 | Git repository를 원격에서 호스팅 |
| Linus Torvalds가 개발 | Microsoft가 소유 / 운영 |
| 로컬 컴퓨터에 설치 | 인터넷을 통해 사용 |
| `commit`, `branch`, `merge` 등 제공 | Repository 공유, collaboration, PR, issue 등 제공 |

### Git

**Git = 버전 관리 소프트웨어**

```text
내 컴퓨터
   ↓
Git
   ↓
Commit / Branch / Merge / History
```

### GitHub

**GitHub = Git repository를 저장하고 협업할 수 있는 호스팅 서비스**

```text
내 컴퓨터
   │
   │ push
   ↓
GitHub
   │
   │ pull / clone
   ↓
다른 컴퓨터
```

### 핵심

> **Git은 버전 관리 도구이고, GitHub는 Git repository를 원격으로 저장하고 공유하기 위한 서비스다.**

---

# 19. Daily Quest

## Q1. `git diff --staged`가 비교하는 대상으로 옳은 것은?

**Answer:**

```text
Staging Area ↔ 마지막 Commit (HEAD)
```

즉, staging된 변경사항이 마지막 commit과 어떻게 다른지 확인한다.

---

## Q2. 현재 작업 중인 브랜치 또는 커밋을 가리키며, 브랜치 전환 시 함께 이동하는 Git의 특수 포인터는?

**Answer:**

```text
HEAD
```

HEAD는 현재 checkout된 위치를 가리킨다.

```text
HEAD → main → Commit
```

---

## Q3. `git reset`의 세 가지 모드 중 commit history, staging area, working directory의 변경사항을 모두 되돌리는 모드는?

**Answer:**

```bash
git reset --hard
```

```text
Commit       ❌
Staging      ❌
Working Dir  ❌
```

---

## Q4. 이미 원격 저장소에 push되어 공유된 commit을 안전하게 되돌리는 명령어는?

**Answer:**

```bash
git revert
```

기존 commit을 삭제하는 대신 **반대 변경을 담은 새로운 commit을 생성**한다.

---

## Q5. Rebase의 황금률에 따라 rebase를 수행해도 비교적 안전한 경우는?

**Answer:**

> **다른 사람과 공유하지 않은 개인 branch의 commit을 정리할 때**

이미 원격에 push되어 다른 사람이 pull한 commit에는 rebase를 피하는 것이 안전하다.

---

# 20. Day 2 핵심 정리

## Staging / Commit

```text
Working Directory
       ↓
   git status
       ↓
변경사항 확인
       ↓
git add / git add -p
       ↓
Staging Area
       ↓
git diff --staged
       ↓
변경사항 확인
       ↓
git commit
       ↓
Repository
```

---

## Reset / Revert / Restore

```text
git reset
→ commit history를 되돌림

git revert
→ 기존 history를 유지하면서 반대 변경을 새로운 commit으로 추가

git restore
→ 파일 변경사항 또는 staging 상태를 복구
```

### Reset 옵션

```text
--soft
→ commit만 취소

--mixed
→ commit + staging 취소

--hard
→ commit + staging + working directory 변경 취소
```

---

## Branch

```text
git branch
→ branch 확인 / 생성

git switch
→ branch 이동

git switch -c
→ branch 생성 + 이동

git merge
→ branch 병합

git branch -d
→ branch 삭제
```

---

## Merge vs Rebase

```text
Merge
→ 두 branch의 history를 연결
→ merge commit이 생성될 수 있음
→ 기존 history 유지

Rebase
→ 내 commit을 최신 위치 위에 다시 쌓음
→ history를 직선적으로 만들 수 있음
→ commit hash가 변경됨
→ 공유된 commit에는 사용하지 않는 것이 안전
```

---

## Local ↔ Remote

```text
Local Repository
       │
       │ git push
       ↓
GitHub / Remote Repository
       │
       │ git pull
       ↓
Local Repository
```

### 핵심 명령어

```bash
git remote -v
git remote add origin <SSH 주소>
git remote set-url origin <SSH 주소>

git push origin main
git push -u origin main

git fetch
git pull origin main
```

---

# ⭐ Day 2에서 반드시 이해할 것

## ① 변경사항을 Commit하는 과정

```text
Working Directory
       ↓
   git status
       ↓
git add / git add -p
       ↓
Staging Area
       ↓
git diff --staged
       ↓
   git commit
       ↓
Repository
```

## ② 되돌리기 명령어의 차이

```text
reset
→ history 자체를 되돌림

revert
→ history를 유지하고 새로운 commit으로 되돌림

restore
→ 파일 또는 staging 상태를 복구
```

## ③ Branch의 기본 흐름

```text
main
  │
  ├── feature/login
  │       ↓
  │     작업
  │       ↓
  │     commit
  │       ↓
  └── merge → main
```

## ④ Remote Repository

```text
Local
  │
  │ push
  ↓
GitHub
  │
  │ pull
  ↓
Local
```

## 핵심 개념

> **Git workflow의 핵심은 변경사항을 Working Directory에서 관리하고, 필요한 변경만 Staging Area에 올린 뒤 의미 있는 단위로 Commit하는 것이다. Branch를 이용해 작업을 분리하고, Merge 또는 Rebase를 통해 history를 관리하며, Remote Repository와 Push/Pull을 통해 협업한다.**