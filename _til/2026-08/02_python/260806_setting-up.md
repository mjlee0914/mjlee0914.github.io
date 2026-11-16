# python

## 가상환경 build method
1. python -m venv "~" : 느림
2. anaconda
3. uv: .venv 보다 간단함, 하나로 통합됨 (version managing, venv create, package install, dependency&lock file managing)
## .venv
to make virtual environment to isolate environments
## uv
tools that hlep create/manage venv, versions, and dependencies
- rust 기반
- project 단위 관리
- 의존성 트리
- 패키지 별 요구하는 버전을 uv가 계산하여 설치함.
- uv.lock에 정확한 버전 기록

**dependencies?
: external libraries/code package

## uv 프로젝트 생성 + 가상환경 구축 process
1. uv init -- python 3.13(version num)
2. pyproject.toml 확인
3. uv add pandas
4. uv sync (pyproject.toml 명세와 현재 가상환경의 설치 상태 일치)
5. .venv\Scripts\activate
or .venv\Scripts\deactivate.bat

*requires-python 제약조건

*uv python pin <변경하고자 하는 버전 넘버>  로 이미 생성된 프로젝트 버전 변경

*버전 변경 후 uv sync까지 해야 반영됨


## 변수와 동적 타이핑
- 변수 variable: 객체의 이름표, "참조"
- 객체 object: 메모리에 생성된/존재하는 실제 데이터
- 값 value: 객체가 표현하는 내용/데이터
- id(): 객체의 메모리상 식별자(객체의 정체성).
- 변수는 값이 할당될 때마다 변수가 참조하는 객체의 id가 바뀜
- 동일한 객체를 다시 참조하면 id() 유지
- *리스트의 경우 같은 내용이라도 새로 생성하면 새로운 객체가 만들어져 id()가 달라짐

- GC: garbage collector, 참조가 끊긴 데이터를 삭제 

ex) 변수 x 이름표 [int 객체/값 10]

## type() 자료형 확인
- 숫자형 - int: 정수형, float: 실수형
- 문자형 str
- 논리형 bool : True/False

