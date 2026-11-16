## git - GitHub process

1. git init (in /localWorkingDir)
2. git add . (to Staging Area)
3. git commit -m "message" (to local repo)
4. git push --> push it to github (remote repo)


   
## local working directory vs local repo
### local working directory
- the folder youre currently working on files.
- changes are made here before being saved as commits.
ex) 
- editing 'main.py'
- adding a new file
- deleting a file

### local repo
- the git database inside your pc that stores committed changes
- contains your commit history
ex)
- git commit -> save changes to the local repo
- git log -> show the commit history









## before git add
- git status : check the current state
- git add -p : parital staging
- git diff --staged : diff between staged vs last commit(head) after partial staging


## git commit messaging convention 
- feat: ______
- fix: ______
- docs: ______
- refactor: ______
- chore: ______
- test: ______


## reseting the changes, cancel commit
1. git reset
   - soft : cancle only the commit, origin file remains, history deleted
   - mixed (default) : cancle commit & add, origin file remains, history deleted
   - hard : cancle commit & add, original file + history deleted
  
2. git reflog
   - shows the history of HEAD movements
   - to recover commits after reset
   - ex) git reset --hard
  
3. git revert
   - creates a new commit that reverses a previous commit
   - original commit history remains
   - ex)
   - before: a -> b -> c
   - after: a -> b -> c -> c'
   - c' reverts c, canceling the changes made in c
  
4. git restore
   - to discard changes in files
   - doesnt change commit history
   - throws away the file changes after the last commit, not store a commit itself


## branch
- git branch: view current brances
- git branch <branchname>: make new branch
- git checkout <branchname>: head pointer to <branchname>
- git checkout <branchname>: branch add & head move to it
- git switch <branchname> : head pointer to <branchname>
- git swtich -c <branchname> : branch add & head move to it


### branch name convention
- feature/
- fix/
- bugfix/
- hotfix/
- chore/
- release/
- test/
- docs/
- dev/

### delete branch
- git branch -d
- git branch -D
- restore -> git refrog -> git branch <new-branch-name> commitID

### change branch name
- git branch -m <newname>
- git branch -M 

## stash
- commit 하지 않은 상태로 branch switching 하면 오류남
- git stash 이후 git swtich 
- 임시 저장
- git stash list : 저장 목록
- git stash pop : 임시 공간 삭제

## merge
- combiends two branches together
- keeps original history
- fast-forward : no new commit created, branch pointer move forward
- 3-way merge : creates a new commit tied to both branches


## rebase
- cleaner commit history rewritten
- Avoid rebasing commits that others may have already pulled.(someone else might be using the commits)
- rebase -- skip
- rebase -- abort

## GitHub
1. git remote add origin SHHaddress
2. git push origin <remote branch name> : local to remote
   git push -u <origin remote branch name>
3. git pull origin <remote branch name> : remote to local
   git pull -u 


## GitHub flow 6
1️⃣ main은 항상 배포 가능한 상태를 유지한다

2️⃣ 새 작업은 반드시 main에서 기능 브랜치를 만들어 진행한다

3️⃣ 기능 브랜치에서 커밋을 쌓아 원격에 push한다

4️⃣ 작업 완료 후 main으로의 PR을 생성한다

5️⃣ 팀원이 코드 리뷰 후 Approve하면 머지한다

6️⃣ 머지 즉시 배포(또는 CI/CD 자동 배포)하고 브랜치를 삭제한다

***github flow operates around only one branch --- ***name***


## git tag / git release ---> version


## .gitignore
.gitignore 파일 안에 아래 형식처럼 작성 
	HELP.md
    .gradle
    build/
    !gradle/wrapper/gradle-wrapper.jar
    !**/src/main/**/build/
    !**/src/test/**/build/

    .apt_generated
    .classpath
    .factorypath
    .project
    .settings
    .springBeans
    .sts4-cache
    bin/
    !**/src/main/**/bin/
    !**/src/test/**/bin/



# 오늘 teamwork 하면서 발견한 오류!
- Feature/카테고리 필터- #28를 PR 하면서 팀원에게 reviewer로서 accept 요청
- 그러나 반복적으로 "mjlee0914 dismissed kimtaeyang88’s stale review", "The merge-base changed after approval."
- stale review로 자동 dismiss
- 저장소 관리자 권한에서(Settings → Branches → Branch protection rule → main)

	Dismiss stale pull request approvals when new commits are pushed
	--> 위 옵션이 체크되어 있다면 main 변경 or PR branch update시 기존 승인 무효화
	
	Require branches to be up to date before merging
	--> 위 옵션이 체크되어 있다면 feature/category-filter가 현재 (1 commit ahead
	21 commits behind main) 상태이므로, 최신 main 반영 후 merge 가능.

- 다음 작업 시 다음 순서로 진행해보기.
	git checkout main
	git pull origin main
	
	git checkout feature/category-filter
	git merge main # 또는 팀 규칙이 rebase라면 git rebase main
	
	git push
	
	그 다음
	
	리뷰어가 한 번 더 Approve
	그 이후에는 아무것도 push하지 않고
	바로 Merge

- **인식한 상황: commit 후 push → PR 생성 → 리뷰 대기 중 → 그 사이 main에 다른 팀원들의 PR이 여러 개 merge됨
- main과 feature branch의 "뒤처짐" 문제, 즉 main에 최신 변경된 커밋보다 내 커밋이 old함



# job seminar 인상 깊었던 점.
- 비전공자로서, 무수히 많은 지원자들 중 가장 경쟁력이 있는 개발자가 되려면?
- "geek" 이 되어라
- ex) 컴퓨터 바탕화면의 폴더를 클릭하고, 그 안의 파일을 열 때, 컴퓨터 안에서 (software 개념으로) 일어나는 과정을 정확히, 자세히 설명할 수 있는지? 또는 그 수준으로 deep한 지식을 가졌는지?
- 공부하면서 "왜" 이렇게 되는지를 누군가에게 정확히 설명할 수 있을 정도로 공부하는 것이 중요해 보임.
- 실제 배포 서비스 경험 및 사용자 받은 경험이 있다면 아주 좋음. insta ad
- 단순한 결과가 아닌 "수치"적인 결과를 만들어 보여주기
- 어떤 마음가짐을 갖고 준비해야 하는지, 나에게 어떤 직무/기업이 맞는지 생각할 재료를 주었던 세미나
