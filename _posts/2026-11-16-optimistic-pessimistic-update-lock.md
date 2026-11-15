---
title: "낙관적·비관적 업데이트와 락: 수강신청 시스템으로 이해하기"
date: 2026-11-16 00:00:00 +0900
tags: [Database, Concurrency, Transaction, SQL, Backend]
style: border
color: primary
description: UI를 바꾸는 낙관적·비관적 업데이트와 데이터 충돌을 제어하는 낙관적·비관적 락을 구분하고, 수강신청 마지막 한 자리를 안전하게 처리하는 방법을 정리했다.
---

비슷한 이름 때문에 자주 헷갈리지만, **업데이트 전략**과 **락 전략**은 해결하려는 문제가 다르다.

- 낙관적·비관적 **업데이트**: 서버 응답 전후 중 언제 화면을 바꿀 것인가?
- 낙관적·비관적 **락**: 여러 요청이 같은 데이터를 수정할 때 충돌을 어떻게 제어할 것인가?

좋아요 버튼이 즉시 바뀌는 것은 프론트엔드의 사용자 경험 문제이고, 마지막 수강 가능 좌석을 두 학생이 동시에 가져가지 못하게 하는 것은 백엔드와 데이터베이스의 정합성 문제다.

## 먼저 한 장으로 보기

| 구분 | 낙관적 방식 | 비관적 방식 |
| --- | --- | --- |
| UI 업데이트 | 성공을 예상하고 화면부터 변경 | 서버 성공 후 화면 변경 |
| 실패했을 때 | 이전 화면으로 롤백 | 오류를 표시하고 화면은 유지 |
| DB 동시성 제어 | 충돌이 적다고 보고 수정 시 검증 | 충돌을 예상하고 먼저 잠금 |
| 대표 구현 | 임시 UI 상태, `version` 비교 | 로딩 상태, `SELECT ... FOR UPDATE` |

이름에 같은 단어가 붙었을 뿐, UI 업데이트만으로 DB의 동시성 문제를 막을 수는 없다.

## 1. 낙관적 업데이트: 화면부터 바꾼다

낙관적 업데이트(Optimistic Update)는 서버 요청이 성공할 것이라고 예상하고 UI를 먼저 변경한다. 좋아요나 북마크처럼 실패 가능성이 낮고 즉각적인 반응이 중요한 기능에 잘 맞는다.

```text
사용자 클릭
  → UI 즉시 변경
  → 서버에 요청
      ├─ 성공: 변경된 UI 유지
      └─ 실패: 이전 상태로 롤백하고 오류 안내
```

```javascript
async function handleLike() {
  const previousLiked = liked;
  setLiked(true);

  try {
    await likePost();
  } catch (error) {
    setLiked(previousLiked);
    showError("좋아요 처리에 실패했습니다.");
  }
}
```

사용자는 빠르다고 느끼지만, 실패 시 원래 상태를 복원해야 한다. 중복 클릭, 요청 순서 역전, 네트워크 재시도까지 고려하면 구현도 단순하지 않다.

## 2. 비관적 업데이트: 성공을 확인한 뒤 바꾼다

비관적 업데이트(Pessimistic Update)는 서버가 성공을 확인해 준 뒤 UI를 변경한다. 결제, 송금, 예약 확정처럼 성공 여부를 잘못 표시했을 때 문제가 큰 기능에 적합하다.

```text
사용자 클릭
  → 로딩 표시 및 중복 클릭 방지
  → 서버에 요청
      ├─ 성공: UI 변경
      └─ 실패: 오류 안내
```

```javascript
async function handlePayment() {
  setSubmitting(true);

  try {
    await pay();
    setPaymentStatus("completed");
  } catch (error) {
    showError("결제에 실패했습니다.");
  } finally {
    setSubmitting(false);
  }
}
```

화면이 서버의 실제 상태보다 앞서 나가지 않는다는 장점이 있지만, 응답을 기다리는 동안 로딩 상태를 명확하게 보여 줘야 한다.

## 3. 낙관적 락: 수정하는 순간 충돌을 검사한다

낙관적 락(Optimistic Lock)은 데이터를 읽을 때 DB 락을 오래 잡지 않는다. 대신 수정할 때 처음 읽은 `version`이 그대로인지 확인한다.

수강 정원이 30명이고 현재 29명, 버전이 5라고 가정해 보자. 학생 A와 B는 모두 다음 상태를 읽을 수 있다.

```text
capacity = 30
enrolled = 29
version = 5
```

두 학생이 같은 조건으로 갱신을 시도한다.

```sql
UPDATE courses
SET enrolled = enrolled + 1,
    version = version + 1
WHERE course_id = 101
  AND version = 5
  AND enrolled < capacity;
```

A의 요청이 먼저 성공하면 `enrolled`는 30, `version`은 6이 된다. 이후 B의 쿼리는 `version = 5` 조건을 만족하지 못하므로 영향을 받은 행이 0개다. 애플리케이션은 반드시 이 행 개수를 확인하고 B에게 충돌 또는 만석을 안내해야 한다.

낙관적 락은 충돌이 드문 일반 정보 수정에 효율적이다. 반대로 마지막 한 자리에 요청이 몰리면 실패와 재시도가 많아질 수 있다.

> `version` 컬럼이 존재하는 것만으로 낙관적 락이 완성되지는 않는다. 수정 쿼리의 조건에 기존 버전을 포함하고, 영향받은 행이 0개일 때 충돌로 처리해야 한다.

## 4. 비관적 락: 먼저 잠그고 처리한다

비관적 락(Pessimistic Lock)은 충돌 가능성이 높다고 보고 데이터를 읽을 때부터 잠근다. PostgreSQL 같은 관계형 DB에서는 보통 `SELECT ... FOR UPDATE`로 대상 행을 잠근다.

```sql
BEGIN;

SELECT enrolled, capacity
FROM courses
WHERE course_id = 101
FOR UPDATE;

-- 조회 결과가 enrolled < capacity일 때만 실행
UPDATE courses
SET enrolled = enrolled + 1
WHERE course_id = 101
  AND enrolled < capacity;

INSERT INTO enrollments (student_id, course_id)
VALUES (1001, 101);

COMMIT;
```

학생 A가 행 락을 얻으면 B의 충돌하는 요청은 A의 트랜잭션이 끝날 때까지 기다린다. A가 신청을 완료한 뒤 B가 락을 얻으면 이미 만석임을 확인하고 실패 처리한다.

이 방식은 처리 순서를 이해하기 쉽지만, 트랜잭션이 길어질수록 락 대기와 데드락 위험이 커진다. 락을 잡은 상태에서 외부 API를 호출하는 것처럼 오래 걸리는 작업은 피하고 트랜잭션을 짧게 유지해야 한다.

## 5. 수강신청에서는 원자적 UPDATE도 강력하다

좌석 한 자리의 확보만 필요하다면 먼저 조회한 뒤 수정하지 않고, 조건 확인과 증가를 한 쿼리로 묶을 수 있다.

```sql
UPDATE courses
SET enrolled = enrolled + 1
WHERE course_id = 101
  AND enrolled < capacity;
```

DB는 이 `UPDATE`를 원자적으로 처리한다. 영향을 받은 행이 1개면 좌석 확보 성공, 0개면 만석이다. 별도의 버전 비교나 사전 조회 없이도 정원 초과를 막을 수 있다.

하지만 좌석 수만 올리고 끝나는 것은 아니다. 실제 수강신청은 다음 조건도 함께 지켜야 한다.

```sql
ALTER TABLE enrollments
ADD CONSTRAINT uq_enrollments_student_course
UNIQUE (student_id, course_id);
```

- 좌석 증가와 신청 내역 저장을 **같은 트랜잭션**에서 처리한다.
- `(student_id, course_id)`에 `UNIQUE` 제약을 두어 중복 신청을 막는다.
- 신청 내역 저장이 실패하면 좌석 증가도 함께 `ROLLBACK`한다.
- 선수 과목, 시간표 중복, 최대 학점 같은 규칙도 확정 전에 검사한다.
- 순간 트래픽이 DB가 감당할 수준을 넘으면 대기열과 요청 제한을 함께 사용한다.

## 어떤 전략을 선택할까?

| 상황 | 우선 고려할 방법 |
| --- | --- |
| 좋아요·북마크 UI | 낙관적 업데이트 + 실패 시 롤백 |
| 결제·예약 확정 UI | 비관적 업데이트 + 로딩·오류 표시 |
| 충돌이 드문 데이터 수정 | 낙관적 락 |
| 짧은 트랜잭션에서 순차 처리가 필요한 경우 | 비관적 락 |
| 좌석·재고의 조건부 증감 | 원자적 `UPDATE` |
| 동일 사용자의 중복 신청 | DB `UNIQUE` 제약조건 |
| 매우 많은 동시 요청 | 원자적 처리 + 대기열·요청 제어 |

인기 강의라고 해서 무조건 비관적 락이 정답은 아니다. 경쟁률, 트랜잭션 길이, 허용 가능한 대기 시간, 실패 후 재시도 정책을 함께 보고 선택해야 한다. 실제로는 하나만 고르는 대신 원자적 쿼리, 트랜잭션, 제약조건과 트래픽 제어를 조합한다.

## 마무리

핵심은 다음 네 문장으로 정리할 수 있다.

1. **낙관적 업데이트**는 서버 성공 전에 화면부터 바꾼다.
2. **비관적 업데이트**는 서버 성공 후 화면을 바꾼다.
3. **낙관적 락**은 수정 시 버전을 비교해 충돌을 발견한다.
4. **비관적 락**은 먼저 행을 잠그고 충돌하는 요청을 기다리게 한다.

수강신청 시스템의 최종 목표는 특정 락을 사용하는 것이 아니라, 동시 요청에서도 **정원 초과와 중복 신청이 발생하지 않도록 불변식을 지키는 것**이다. 이를 위해서는 UI 전략과 별개로 DB 트랜잭션, 원자적 연산, 제약조건을 함께 설계해야 한다.

### 참고 자료

- [PostgreSQL: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [SQLAlchemy: Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html)
