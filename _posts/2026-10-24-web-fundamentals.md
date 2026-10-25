---
title: "웹기초: HTTP 요청과 응답의 전체 흐름"
date: 2026-10-24
tags: [Web, HTTP, Network]
style: border
color: primary
description: 클라이언트와 서버부터 HTTP 메시지, 쿠키와 세션, CORS, Ajax까지 웹의 기본 동작을 정리합니다.
---

# 웹은 요청과 응답으로 동작한다

웹의 기본 흐름은 단순하다. 클라이언트가 서버에 필요한 자원을 **요청(Request)** 하고, 서버는 처리 결과를 **응답(Response)** 한다. 브라우저는 HTML을 받은 뒤 필요한 CSS, JavaScript, 이미지도 각각 요청해서 화면을 구성한다. 그래서 개발자 도구의 Network 탭에는 한 페이지를 열어도 여러 요청이 보인다.

```text
클라이언트 → Request → 서버
클라이언트 ← Response ← 서버
```

HTTP는 이 요청과 응답을 주고받기 위한 통신 규칙이고, HTTPS는 그 통신을 암호화한다. HTTP 메시지는 보통 첫 줄, Header, 빈 줄, Body로 나뉜다. 요청의 첫 줄에는 `GET`, `POST` 같은 메서드가 있고, 응답의 첫 줄에는 `200`, `404` 같은 상태 코드가 있다.

## URL과 요청 메서드

```text
https://example.com/search?subject=HTTP&page=2
```

- `https`: 통신 방식
- `example.com`: 도메인
- `/search`: 자원의 경로
- `subject=HTTP&page=2`: Query String

자주 사용하는 메서드는 다음과 같다.

- `GET`: 자원 조회
- `POST`: 데이터를 보내 서버가 처리하도록 요청
- `PUT`: 대상 전체 교체
- `PATCH`: 대상 일부 수정
- `DELETE`: 자원 삭제
- `HEAD`: 응답 Body 없이 Header만 확인
- `OPTIONS`: 통신 옵션 확인, CORS 사전 요청 등에 사용

## Stateless, Cookie, Session

HTTP는 이전 요청의 사용자 상태를 자동으로 기억하지 않는 **Stateless(무상태)** 방식이다. 로그인 상태처럼 여러 요청 사이에서 사용자를 구별해야 할 때는 Cookie와 Session 등을 사용한다.

```text
브라우저 → 로그인 요청 → 서버
브라우저 ← Set-Cookie ← 서버
브라우저 → Cookie를 포함한 다음 요청 → 서버
서버 → Session 정보로 사용자 확인
```

`Set-Cookie`는 서버가 브라우저에 쿠키 저장을 요청하는 응답 Header이고, `Cookie`는 브라우저가 저장된 쿠키를 서버 요청에 포함할 때 사용하는 요청 Header다.

## Origin과 CORS

Origin은 **프로토콜 + 도메인 + 포트**의 조합이다. 하나라도 다르면 다른 출처다. CORS는 다른 출처의 응답을 브라우저 JavaScript가 사용할 수 있도록 서버가 허용 여부를 알려주는 방식이다.

일부 요청은 실제 요청 전에 `OPTIONS` 메서드로 Preflight 요청을 보낸다. 다만 모든 교차 출처 요청에 Preflight가 발생하는 것은 아니며, CORS 오류가 항상 서버에 요청이 도착하지 않았다는 뜻도 아니다.

## 상태 코드와 캐시

- `200 OK`: 요청 처리 성공
- `201 Created`: 새 자원 생성 성공
- `301 Moved Permanently`: 자원의 주소가 영구적으로 변경됨
- `304 Not Modified`: 기존에 저장한 캐시를 다시 사용
- `400 Bad Request`: 요청 형식 등에 문제가 있음
- `401 Unauthorized`: 유효한 인증 정보가 필요함
- `403 Forbidden`: 접근이 거부됨
- `404 Not Found`: 자원을 찾지 못함
- `500 Internal Server Error`: 서버 내부 오류

`304 Not Modified`는 오류가 아니다. 브라우저가 이미 받은 자원이 바뀌지 않았음을 확인하고 저장된 데이터를 다시 사용하는 정상적인 응답이다.

## Ajax와 CSR의 차이

Ajax는 페이지 전체를 새로 불러오지 않고 서버와 데이터를 주고받아 필요한 부분만 갱신하는 방식이다. CSR은 브라우저에서 JavaScript로 화면을 만드는 렌더링 방식이다. 둘은 관련될 수 있지만 같은 뜻은 아니다.

```text
Ajax → 서버와 데이터를 어떻게 주고받는가
CSR  → 화면을 어디에서 만드는가
```

## 프로젝트 발표 피드백

발표 첫 부분에서 **어떤 문제를 해결했는지** 보여주면 관심을 끌기 좋다. 설명은 **문제 → 해결 방법 → 달라진 결과** 순서로 구성한다.

```text
문제
→ 댓글 작성 때마다 전체 페이지가 새로고침됨.

해결
→ Ajax로 댓글을 전송하고 목록만 갱신.

결과
→ 페이지 전체를 다시 불러오지 않고 댓글 확인.
```

- [프로젝트 발표 PPT](https://docs.google.com/presentation/d/1W6LVvYJaRfGo2mhWDVaqMYNADKjFyb9HRm3XAZGlNZw/edit?usp=drivesdk)
- [웹기초 전체 TIL 보기](/til/2026-10/261024_TIL/)

이번 정리를 통해 브라우저에서 보이는 화면 뒤에서는 URL, Method, Header, Body로 요청을 만들고, 서버가 Status Code, Header, Body로 응답한다는 흐름을 연결해서 이해할 수 있었다.
