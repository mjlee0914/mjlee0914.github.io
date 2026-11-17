---
name: What's in my cart?
tools: [Python, FastAPI, PostgreSQL, SQLAlchemy, JWT, Docker]
image: /assets/images/projects/fastapi-board-api.png
description: JWT 인증·친구 공개 범위를 구현한 FastAPI 게시판 API를 직접 읽으며 계층 구조, 권한, 동시성, ORM 성능을 복습하는 진행형 학습 프로젝트
permalink: /projects/fastapi-board-api
---

## 프로젝트 소개

사진으로 일상을 공유하는 익명 커뮤니티를 위해 만든 RESTful 게시판 API다. 기능 구현을 마친 뒤에도 이해하지 못한 코드를 그냥 넘기지 않기 위해, 코드를 다시 읽으며 **왜 이런 구조와 쿼리를 사용했는지** 정리하고 있다.

> **학습 상태:** 진행 중 — 공부할 때마다 이 페이지에 내용을 추가할 예정이다.

[GitHub 저장소에서 코드 보기](https://github.com/mjlee0914/fastapi-board-api)

## 1. 요청 흐름과 계층 구조

```text
요청 → [스키마: 입력 검증] → 라우터 → 서비스 → 모델 → (세션) → DB
응답 ← [스키마: 응답 모양] ← 라우터 ← 서비스 ←───────────────┘
```

- **라우터** (`api/routes/`): 요청을 받아 서비스를 호출한다. 라우터의 몸통은 거의 한 줄이다.
- **서비스** (`services/`): 누가 글을 볼 수 있는지, 조회수를 어떻게 증가시킬지 같은 비즈니스 규칙을 처리한다.
- **스키마** (`schemas/`): 입구에서 요청을 검증하고 출구에서 응답 모양을 정한다.
  - 입력: `PostCreateForm`, `PostUpdate`
  - 출력: `response_model=PostResponse`
  - 검증에 실패하면 라우터 함수가 실행되기 전에 `422` 응답이 반환된다.
- **모델** (`models/`): DB 테이블의 구조를 표현하는 클래스다. 모델 자체가 DB에 쿼리를 보내는 것은 아니다.
- **세션** (`db/session.py`): `db.add()`, `db.commit()` 등을 통해 실제 DB 작업을 수행한다.

## 2. 로그인 의존성 사슬

`api/deps.py`의 인증 의존성은 한 함수가 모든 일을 하지 않고 단계별로 이어진다.

```text
Authorization 헤더
  → bearer_scheme       토큰 문자열 추출(없으면 None)
  → get_optional_user   토큰 해독 → user_id → DB에서 User 조회
  → get_current_user    None이면 401, 아니면 User 반환
```

- `OptionalUser`: 비회원도 접근할 수 있는 피드와 글 상세에 사용한다.
- `CurrentUser`: 글쓰기와 내 정보처럼 로그인이 필수인 곳에 사용한다.
- `get_current_user`는 토큰을 직접 처리하지 않고, optional 단계의 결과가 `None`인지 검사하는 책임만 더한다.

| 상황 | OptionalUser | CurrentUser |
| --- | --- | --- |
| 토큰 없음 | `None`으로 통과 | `401` |
| 토큰 만료 | `401 TOKEN_EXPIRED` | `401 TOKEN_EXPIRED` |
| 토큰은 있지만 사용자가 없음 | `401` 유효하지 않은 토큰 | `401` |

만료된 토큰을 비회원으로 조용히 처리하지 않아야 프론트엔드가 사용자를 다시 로그인 화면으로 보낼 수 있다.

## 3. ForeignKey와 relationship

```python
post_id: Mapped[int] = mapped_column(
    ForeignKey("posts.id", ondelete="CASCADE"),
    index=True,
)
post: Mapped["Post"] = relationship(back_populates="comments")
author: Mapped["User"] = relationship()
```

- `post_id`는 실제 DB 컬럼이며 값은 숫자다. 예: `comment.post_id == 5`
- `post`는 DB 컬럼이 아니라 Python에서 연관 객체로 접근하는 통로다. 예: `comment.post.title`
- `back_populates`는 반대쪽 관계와 짝을 맺어 `post.comments`처럼 역방향으로도 접근할 수 있게 한다.
- `author`에는 `back_populates`가 없으므로 `comment.author` 방향으로만 접근한다.

`relationship()`은 편리하지만, 언제 SQL이 실행되는지 이해하지 못하면 N+1 문제나 async 환경의 `MissingGreenlet` 오류로 이어질 수 있다.

## 4. `ondelete="CASCADE"`

| 설정 | 댓글이 달린 글을 삭제하면 |
| --- | --- |
| Foreign Key 없음 | 글은 삭제되고 댓글은 고아 데이터로 남을 수 있음 |
| Foreign Key만 있음 | 참조 무결성 때문에 삭제가 거절됨 |
| Foreign Key + `CASCADE` | 글과 연결된 댓글이 함께 삭제됨 |

서비스 코드만으로 연관 데이터를 정리하는 대신 DB 제약조건으로 데이터 정합성을 지킨다.

## 5. 경쟁 상태: 조회수 증가

Python에서 현재 값을 읽고 1을 더한 뒤 저장하면 갱신 손실이 발생할 수 있다.

```text
A: 10 읽음 → B: 10 읽음 → A: 11 저장 → B: 11 저장
결과: 두 명이 조회했지만 조회수는 11
```

DB가 현재 저장된 값에 직접 1을 더하도록 만들면 하나의 원자적 `UPDATE`로 처리할 수 있다.

```python
update(Post).where(Post.id == post_id).values(
    pull_count=Post.pull_count + 1,
).returning(Post.pull_count)
```

```sql
UPDATE posts
SET pull_count = pull_count + 1
WHERE id = 5
RETURNING pull_count;
```

같은 행을 수정하는 쿼리는 DB가 순서대로 처리하므로 두 요청의 증가가 모두 반영된다. `RETURNING`을 사용하면 증가한 결과도 같은 쿼리에서 바로 받을 수 있다.

## 6. 권한 없는 글에 `403` 대신 `404`

`403 Forbidden`을 반환하면 사용자가 볼 수 없는 글이 그 ID에 존재한다는 사실이 드러난다. 익명 커뮤니티에서 글의 존재 자체를 숨겨야 한다면, 없는 글과 권한 없는 글을 모두 `404 Not Found`로 처리할 수 있다.

이를 위해 `can_view(viewer)` 조건을 조회 쿼리의 `WHERE`에 포함한다. 그러면 두 경우 모두 조회 결과가 `None`이 되어 같은 응답을 반환한다.

## 7. `can_view` 규칙

```python
if viewer is None:
    return Post.visibility == Visibility.PUBLIC

return or_(
    Post.visibility == Visibility.PUBLIC,
    Post.author_id == viewer.id,
    and_(
        Post.visibility == Visibility.FRIENDS,
        Post.author_id.in_(friend_ids_query(viewer.id)),
    ),
)
```

- 비회원은 `PUBLIC` 글만 볼 수 있다.
- 로그인 사용자는 공개 글과 자신이 작성한 글을 볼 수 있다.
- 다른 사람의 `FRIENDS` 글은 작성자가 내 `ACCEPTED` 친구일 때만 볼 수 있다.
- `PENDING` 상태의 친구 요청은 친구 목록에 포함되지 않는다.
- `Post.visibility == FRIENDS`는 “내가 친구인가?”를 검사하는 코드가 아니라, 글에 저장된 공개 범위가 `FRIENDS`인지 확인하는 조건이다.

예를 들어 kim이 로그인했고 lee는 `ACCEPTED`, park은 `PENDING`인 상태라면 다음과 같다.

| 글 | 작성자 / 공개 범위 | 보임? | 이유 |
| --- | --- | --- | --- |
| A | park / PUBLIC | O | 공개 글 |
| B | park / FRIENDS | X | park은 아직 PENDING |
| C | lee / FRIENDS | O | lee는 ACCEPTED 친구 |
| D | kim / FRIENDS | O | 본인이 작성한 글 |

## 8. N+1 문제

목록을 한 번 조회한 뒤 각 글의 좋아요 수를 다시 조회하면 글 개수만큼 쿼리가 추가된다.

```python
posts = await db.scalars(select(Post).limit(20))

for post in posts:
    await db.scalar(
        select(func.count()).where(Like.post_id == post.id)
    )
```

목록 1번과 글마다 1번씩, 총 `1 + N`번의 쿼리가 실행된다. 글이 20개면 21번, 100개면 101번이다.

### 해결 1: 상관 서브쿼리

좋아요 수와 댓글 수는 목록 쿼리 안의 scalar subquery로 계산한다.

```python
like_count = (
    select(func.count())
    .select_from(Like)
    .where(Like.post_id == Post.id)
    .correlate(Post)
    .scalar_subquery()
)

stmt = select(Post, like_count, comment_count)
```

`.correlate(Post)`는 서브쿼리를 바깥 쿼리의 “현재 Post”와 연결한다.

### 해결 2: `selectinload`

작성자를 글마다 한 명씩 조회하는 대신, 필요한 작성자 ID를 모아 한 번에 가져온다.

```sql
SELECT * FROM users WHERE id IN (3, 7, 12, ...);
```

현재 `list_posts`는 글 개수와 상관없이 다음 3번의 쿼리로 목록을 구성한다.

1. 전체 글 개수 조회
2. 글과 좋아요·댓글 수 조회
3. `selectinload`가 실행하는 작성자 `IN` 조회

`selectinload`를 제거하면 작성자 조회에서 N+1 문제가 다시 발생하고, SQLAlchemy async 환경에서는 지연 로딩 과정에서 `MissingGreenlet` 오류가 날 수도 있다.

## 다음 복습 주제

- 트랜잭션의 `commit`, `flush`, `refresh` 차이
- 좋아요 토글과 중복 좋아요 방지 제약조건
- 친구 요청 상태 전이와 양방향 관계
- 테스트에서 인증 사용자와 DB 세션을 교체하는 방법
- 페이지네이션 쿼리와 인덱스 확인
