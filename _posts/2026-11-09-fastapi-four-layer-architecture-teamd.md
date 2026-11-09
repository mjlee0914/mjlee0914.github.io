---
title: "FastAPI 4계층 구조: Team D 코드로 이해하는 Router, Service, Entity, Repository"
date: 2026-11-09
tags: [FastAPI, Python, DDD, SQLAlchemy, Architecture, Team D]
style: border
color: primary
description: Team D의 Festival·Performance 코드를 따라가며 표현·응용·도메인·인프라 4계층과 FastAPI wiring의 역할을 정리했다.
---

## 먼저 한 장으로 보기

Team D의 Performance 기능은 요청을 한 파일에서 모두 처리하지 않는다. HTTP 처리, 유스케이스 진행, 비즈니스 규칙, DB 접근을 서로 다른 계층에 맡긴다.

```text
클라이언트 요청
    ↓
Presentation ─ router.py
    ↓ PerformanceService 호출
Application  ─ service.py
    ↓ Entity의 행동 호출 / Repository 인터페이스 사용
Domain       ─ performance.py, repository.py
    ↑ Domain 객체로 변환             │ 추상 인터페이스
Infrastructure ─ models.py, repositories.py
    ↓ SQLAlchemy
PostgreSQL

wiring ─ 위 부품을 실제 객체로 조립
```

폴더 이름으로는 **Presentation → Application → Domain → Infrastructure**의 4계층이고, 실제 요청 흐름으로는 **Router → Service → Entity/Repository → SQLAlchemy**라고 읽을 수 있다. `wiring`은 다섯 번째 업무 계층이라기보다, 분리된 부품을 앱 시작 시 연결하는 **조립 지점(composition root)**이다.

이 글의 코드 링크는 작성 시점의 [`dev` 커밋 `4545611`](https://github.com/mjlee0914/BE-project-teamD/tree/4545611e325e4d825bf02ad0a50dbd45910f5e88)을 기준으로 한다.

## 예시: 공연 취소 요청은 어디를 지나갈까?

`PATCH /v1/performances/{performance_id}/cancel` 요청을 따라가면 각 계층의 책임이 보인다.

```text
1. Router
   URL의 performance_id를 받고 service.cancel_performance() 호출

2. Service
   Repository로 공연을 조회 → Entity의 cancel(now) 호출 → 다시 저장

3. Entity
   이미 취소됐는지, 이미 종료됐는지 검사하고 상태를 CANCELED로 변경

4. Repository 구현체
   Domain 객체의 변경을 SQLAlchemy 모델에 옮기고 flush

5. 요청 종료
   get_db가 트랜잭션을 commit 또는 rollback
```

핵심은 “취소할 수 있는가?”가 Router나 SQLAlchemy 모델이 아니라 `Performance.cancel()`에 있다는 점이다. HTTP 경로가 바뀌거나 DB 기술이 바뀌어도 공연 취소 규칙은 그대로 남는다.

## 1. Presentation: HTTP만 이해하는 Router

Presentation 계층은 외부 요청을 애플리케이션이 이해할 값으로 바꾸고, 결과를 응답 스키마로 변환한다.

Team D의 [`performances/presentation/routers/v1/router.py`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/performances/presentation/routers/v1/router.py)는 다음을 담당한다.

- `APIRouter`로 URL과 HTTP method를 정의한다.
- Path, Query, JSON body를 받는다.
- `PerformanceService`의 메서드를 호출한다.
- Domain 객체를 `PerformanceResponse`로 바꿔 반환한다.

```python
@router.patch("/performances/{performance_id}/cancel")
async def cancel_performance(
    performance_id: int,
    service: PerformanceServiceDep,
):
    performance = await service.cancel_performance(performance_id)
    return APIResponse.ok(
        data=PerformanceResponse.model_validate(performance)
    )
```

Router가 알아도 되는 것은 “어떤 요청을 받았고 어떤 응답을 보낼지”다. SQL 쿼리, 상태 전이 규칙, 트랜잭션 세부사항까지 넣기 시작하면 HTTP 코드와 업무 규칙이 엉킨다.

FastAPI 공식 문서에서는 이 역할을 [`APIRouter`와 `include_router`](https://fastapi.tiangolo.com/tutorial/bigger-applications/)로 여러 파일에 나누는 방법을 설명한다.

## 2. Application: 유스케이스의 순서를 정하는 Service

Application 계층은 한 요청을 완료하기 위해 필요한 작업의 순서를 조정한다. Team D 코드의 표현대로 **꺼내기 → 처리 → 저장**이다.

[`PerformanceService.cancel_performance()`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/performances/application/service.py)는 다음 세 줄로 흐름을 완성한다.

```python
async def cancel_performance(self, performance_id: int) -> Performance:
    performance = await self.get_performance(performance_id)  # 꺼내기
    performance.cancel(now_utc())                             # 처리
    return await self._performance_repo.save(performance)     # 저장
```

공연 생성은 조금 더 복합적이다. Service는 Festival을 조회하고, 취소된 축제인지 확인하고, 같은 축제 안에 제목이 중복되는지 Repository에 묻고, 마지막으로 `Performance.create()`를 호출한다.

여기서 책임을 나누는 기준은 다음과 같다.

- 여러 객체와 저장소를 조율하는 **유스케이스의 순서**: Service
- 하나의 Performance가 항상 지켜야 하는 **자기 규칙**: Entity
- 다른 행의 존재나 중복처럼 DB 조회가 필요한 판단: Service가 Repository를 통해 확인

[Cosmic Python의 Service Layer 장](https://www.cosmicpython.com/book/chapter_04_service_layer)은 이를 “orchestration logic”과 “business logic”의 분리로 설명한다. 책의 Flask 예제에서 웹 진입점만 FastAPI Router로 바꾸면 Team D 구조와 거의 같은 모양이다.

## 3. Domain: 규칙을 지키는 Entity와 Repository 인터페이스

Domain은 프레임워크나 DB보다 공연이라는 문제 자체를 표현하는 중심 계층이다.

### Entity는 데이터 묶음이 아니라 행동을 가진다

[`Performance` 엔티티](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/performances/domain/performance.py)는 `@dataclass`이지만 필드만 보관하지 않는다.

- 공연 시작은 종료보다 빨라야 한다.
- 예매 기간은 공연 시작 전에 끝나야 한다.
- 공연 일정은 축제 기간 안에 있어야 한다.
- `SCHEDULED → OPEN` 같은 허용된 상태 전이만 가능하다.
- 이미 취소됐거나 종료된 공연은 다시 취소할 수 없다.
- 잔여 수량은 `0`보다 작거나 수용 인원보다 클 수 없다.

```python
def cancel(self, now: datetime) -> None:
    if self.status == PerformanceStatus.CANCELED:
        raise InvalidPerformanceStatus("이미 취소된 공연입니다.")
    if self.status == PerformanceStatus.COMPLETED or now >= self.ends_at:
        raise InvalidPerformanceStatus("이미 종료된 공연입니다.")

    self.status = PerformanceStatus.CANCELED
```

이 클래스에는 FastAPI의 `Depends`, Pydantic의 `BaseModel`, SQLAlchemy의 `AsyncSession`이 없다. 그래서 서버나 DB를 띄우지 않고도 순수 Python 단위 테스트로 규칙을 확인할 수 있다.

[Cosmic Python Ch.1](https://www.cosmicpython.com/book/chapter_01_domain_model)은 Entity, Value Object, Domain Service를 이용해 업무 언어와 규칙을 코드 중심에 두는 방법을 설명한다.

### Domain의 Repository는 SQL 코드가 아니라 약속이다

[`PerformanceRepository`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/performances/domain/repository.py)는 `ABC`와 `abstractmethod`로 “저장소가 할 수 있어야 하는 일”만 정한다.

```python
class PerformanceRepository(ABC):
    @abstractmethod
    async def find_by_id(self, performance_id: int) -> Performance | None:
        ...

    @abstractmethod
    async def save(self, performance: Performance) -> Performance:
        ...
```

Service는 이 인터페이스만 의존한다. 실제 저장소가 PostgreSQL인지, 테스트용 메모리 저장소인지 알 필요가 없다. [Cosmic Python Ch.2](https://www.cosmicpython.com/book/chapter_02_repository)는 Repository를 Domain Model과 데이터 저장 기술 사이의 추상화로 설명한다.

## 4. Infrastructure: SQLAlchemy로 약속을 구현한다

Infrastructure 계층은 Domain이 정한 Repository 인터페이스를 구체적인 기술로 구현한다.

Team D의 [`SqlAlchemyPerformanceRepository`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/performances/infrastructure/repositories.py)는 다음을 담당한다.

- `AsyncSession`으로 `SELECT`, `COUNT`, `EXISTS`를 실행한다.
- SQLAlchemy Model과 순수 Domain Entity를 서로 변환한다.
- `flush()`와 `refresh()`로 변경을 DB 세션에 반영한다.
- 버전이 달라진 동시 수정과 SQLAlchemy 예외를 Domain 예외로 바꾼다.

```python
class SqlAlchemyPerformanceRepository(PerformanceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, performance_id: int) -> Performance | None:
        stmt = select(PerformanceModel).where(
            PerformanceModel.id == performance_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else _to_domain(model)
```

SQLAlchemy의 `PerformanceModel`은 테이블 구조와 제약을 표현하고, Domain의 `Performance`는 업무 행동과 규칙을 표현한다. 이름은 같아도 책임이 다르므로 변환 함수 `_to_domain()`, `_to_model()`이 둘 사이의 경계가 된다.

## Wiring: 분리한 계층을 누가 연결할까?

계층을 분리했지만 실제 요청에서는 구체적인 객체가 필요하다. 이 연결을 [`wiring/performance.py`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/wiring/performance.py)가 담당한다.

먼저 Presentation의 기본 의존성 함수는 아직 실제 구현을 모른다는 뜻으로 예외를 던진다.

```python
def get_performance_service() -> PerformanceService:
    raise NotImplementedError("wiring/performance.py에서 연결되지 않았습니다.")
```

Wiring에서는 DB 세션을 받아 구체 Repository들을 만들고 Service에 주입한다.

```python
def build_performance_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PerformanceService:
    return PerformanceService(
        SqlAlchemyPerformanceRepository(session),
        SqlAlchemyFestivalRepository(session),
    )
```

그리고 `app.dependency_overrides`로 기본 의존성을 실제 팩토리로 교체한다.

```python
app.dependency_overrides.update({
    get_performance_service: build_performance_service,
})
```

[`main.py`](https://github.com/mjlee0914/BE-project-teamD/blob/4545611e325e4d825bf02ad0a50dbd45910f5e88/src/main.py)가 `wire_dependencies(app)`을 호출한 뒤 Router를 등록하므로, 요청 시 다음 객체 그래프가 만들어진다.

```text
Performance Router
    └─ PerformanceService
        ├─ SqlAlchemyPerformanceRepository
        │   └─ 요청 단위 AsyncSession
        └─ SqlAlchemyFestivalRepository
            └─ 같은 AsyncSession
```

FastAPI의 [`Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/)는 필요한 객체를 선언하는 DI 기능이다. [`dependency_overrides`](https://fastapi.tiangolo.com/advanced/testing-dependencies/)는 공식 문서에서 주로 테스트 대역 교체 방법으로 소개하지만, Team D는 같은 메커니즘을 앱의 실제 구현체 조립에도 사용한다. 즉, 이것은 FastAPI가 강제한 유일한 구조가 아니라 **우리 프로젝트가 선택한 wiring 방식**이다.

## 의존성 방향과 실행 방향은 다르다

요청은 바깥에서 안으로 실행되지만, 코드 의존성의 핵심은 Domain을 보호하는 방향이다.

```text
실행 흐름: Client → Router → Service → Repository 구현 → DB

코드 의존:
Router ───────→ Service
Service ──────→ Domain Entity + Repository 인터페이스
SQLAlchemy Repo ─→ Domain Repository 인터페이스를 구현
Wiring ───────→ 모든 구체 구현을 알고 조립
```

Domain은 FastAPI와 SQLAlchemy를 import하지 않는다. 반대로 Infrastructure가 Domain의 인터페이스를 구현한다. 이것이 의존성 역전(DIP)의 실제 모습이다. [Clean Architecture 원문](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)의 핵심도 소스 코드 의존성이 안쪽의 정책을 향해야 한다는 것이다.

Martin Fowler의 [Presentation-Domain-Data Layering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html)은 웹 처리, 업무 로직, 데이터 접근을 나누는 출발점을 설명하고, Team D는 그 사이에 Application Service를 명시적으로 둔 형태로 볼 수 있다. Fowler의 [Repository](https://martinfowler.com/eaaCatalog/repository.html)와 [Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html) 설명도 각 경계의 역할을 짧게 확인하기 좋다.

## 자주 헷갈리는 부분

### Service와 Entity 중 어디에 규칙을 둘까?

- 한 Performance가 스스로 지켜야 하는 규칙: Entity
- 여러 객체·Repository가 필요한 작업 순서: Service
- HTTP 입력·출력 변환: Router
- SQL과 ORM 처리: Infrastructure Repository

예를 들어 “이미 종료된 공연은 취소할 수 없다”는 Entity 규칙이다. 반면 “ID로 공연을 조회한 뒤 취소하고 저장한다”는 Service의 유스케이스다.

### Domain Repository와 SQLAlchemy Repository는 왜 둘 다 있을까?

Domain Repository는 **무엇을 할 수 있어야 하는가**를 정하고, SQLAlchemy Repository는 **그 일을 이 기술로 어떻게 할 것인가**를 구현한다. 둘을 분리하면 Service 테스트에서 DB 대신 Fake Repository를 넣을 수 있고, 저장 기술의 변화가 업무 규칙까지 번지는 것을 줄일 수 있다.

### `dependency_overrides`는 테스트 전용 아닌가?

FastAPI 문서의 대표 사용처는 테스트지만 속성 자체는 의존성 함수를 다른 callable로 치환한다. Team D는 프로덕션 wiring에도 사용한다. 테스트에서는 같은 경계를 다시 이용해 가짜 Service나 Repository를 넣을 수 있다.

### 4계층이면 항상 모든 요청이 네 계층을 전부 지나야 할까?

아니다. 단순 조회와 복잡한 상태 변경은 필요한 로직이 다르다. 중요한 것은 파일 수를 맞추는 것이 아니라 책임의 경계를 지키는 것이다.

## 추천 학습 순서

1. [Fowler의 Presentation-Domain-Data Layering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html)으로 계층 분리의 이유를 먼저 읽는다.
2. 한국어로는 [DDD Start! 아키텍처 개요](https://velog.io/@freesky/DDD-Start-Architecture)에서 표현·응용·도메인·인프라 용어를 익힌다.
3. [Cosmic Python Ch.1 Domain Model](https://www.cosmicpython.com/book/chapter_01_domain_model), [Ch.2 Repository](https://www.cosmicpython.com/book/chapter_02_repository), [Ch.4 Service Layer](https://www.cosmicpython.com/book/chapter_04_service_layer) 순서로 읽는다.
4. FastAPI의 [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/), [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)을 Team D의 wiring과 맞춰 본다.
5. 마지막으로 Team D의 `cancel_performance` 또는 `create_performance`를 골라 Router부터 Repository까지 직접 따라간다.

책의 예제가 Flask여도 걱정할 필요는 없다. Framework의 이름보다 **입구 → 유스케이스 → 도메인 규칙 → 저장소**, 그리고 **구체 구현은 바깥에서 주입한다**는 구조를 보는 것이 핵심이다.

## 한 문장 정리

Team D의 4계층 구조는 코드를 폴더 네 개로 나눈 것이 아니라, **Router는 HTTP, Service는 유스케이스, Entity는 업무 규칙, Repository 구현은 DB를 맡기고, wiring이 이들을 조립해 Domain을 프레임워크와 저장 기술로부터 보호하는 설계**다.

## 참고 자료

- [Architecture Patterns with Python (Cosmic Python)](https://www.cosmicpython.com/)
- [Cosmic Python 예제 코드](https://github.com/cosmicpython/code)
- [Martin Fowler: Presentation-Domain-Data Layering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html)
- [Martin Fowler: Repository](https://martinfowler.com/eaaCatalog/repository.html), [Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Robert C. Martin: The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [DDD Start! 아키텍처 개요](https://velog.io/@freesky/DDD-Start-Architecture)
- [Chapter 2. 아키텍처 개요](https://velog.io/@rolroralra/Chapter2.-아키텍처-개요)
