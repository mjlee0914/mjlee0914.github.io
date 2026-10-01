---
title: "stopPropagation()과 stopImmediatePropagation() 제대로 이해하기"
date: 2026-10-01
tags: [JavaScript, DOM, Events]
style: border
color: primary
description: 이벤트 전파와 기본 동작의 차이, 두 전파 중단 메서드의 동작을 예제로 정리합니다.
---

# `stopPropagation()`과 `stopImmediatePropagation()` 정리

> 원문: [stopPropagation vs stopImmediatePropagation 제대로 이해하기](https://medium.com/%EC%98%A4%EB%8A%98%EC%9D%98-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/stoppropagation-vs-stopimmediatepropagation-%EC%A0%9C%EB%8C%80%EB%A1%9C-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-75edaaed7841)

이 글은 원문의 주제를 바탕으로 다시 구성한 학습 노트입니다. Medium에서 전체 본문을 확인할 수 없어 원문 코드와 대조할 수는 없었고, 아래 코드는 핵심 동작을 설명하기 위해 새로 만든 예시입니다. 바닐라 JavaScript의 DOM 이벤트를 기준으로 살펴봅니다.

## 한눈에 보는 차이

| 메서드 | 같은 요소의 뒤이은 리스너 | 조상 요소로 전파 | 기본 동작 취소 |
|---|---|---|---|
| `stopPropagation()` | 계속 실행 | 중단 | 아니요 |
| `stopImmediatePropagation()` | 중단 | 중단 | 아니요 |
| `preventDefault()` | 계속 실행 | 계속 | 예(취소 가능한 경우) |

전파와 기본 동작은 별개입니다. 이벤트가 부모까지 올라가는 것을 막는 메서드는 `stopPropagation()` 계열이고, 링크 이동이나 폼 제출을 막는 메서드는 `preventDefault()`입니다.

## 이벤트 리스너 등록

`addEventListener(type, listener)`는 요소에 이벤트 리스너를 등록합니다. 한 요소에 여러 리스너를 등록할 수 있으며, 같은 단계에 등록된 리스너는 등록 순서대로 실행됩니다.

```javascript
const button = document.querySelector("button");

function sayHi() {
  console.log("hi");
}

button.addEventListener("click", sayHi);
```

이벤트는 DOM 트리에서 캡처링 단계(조상에서 타깃으로), 타깃 단계, 버블링 단계(타깃에서 조상으로)를 거칠 수 있습니다. 기본 등록은 버블링 단계에서 처리하며, `{ capture: true }`를 주면 캡처링 단계에서 처리합니다.

```javascript
const parent = document.querySelector("#parent");
const child = document.querySelector("#child");

parent.addEventListener("click", () => {
  console.log("parent bubble");
});

parent.addEventListener("click", () => {
  console.log("parent capture");
}, { capture: true });

child.addEventListener("click", () => {
  console.log("child");
});
```

## `stopPropagation()`: 조상으로의 전파 중단

자식 요소에서 이 메서드를 호출하면 이벤트가 부모나 다른 조상 리스너로 전파되지 않습니다. 하지만 같은 요소에 등록된 다른 리스너까지 취소하지는 않습니다.

```javascript
const parent = document.querySelector("#parent");
const child = document.querySelector("#child");

parent.addEventListener("click", () => {
  console.log("parent listener");
});

child.addEventListener("click", (event) => {
  console.log("child listener");
  event.stopPropagation();
});
```

자식을 클릭하면 `child listener`만 출력됩니다. 반면 같은 버튼에 두 리스너를 달고 첫 번째에서 `stopPropagation()`을 호출하면 두 번째 리스너도 실행됩니다.

```javascript
button.addEventListener("click", (event) => {
  console.log("first listener");
  event.stopPropagation();
});

button.addEventListener("click", () => {
  console.log("second listener");
});
```

## `stopImmediatePropagation()`: 현재 요소의 다음 리스너도 중단

이 메서드는 조상으로의 전파를 막는 동시에, 현재 요소에서 아직 실행되지 않은 뒤이은 리스너도 멈춥니다.

```javascript
button.addEventListener("click", (event) => {
  console.log("first listener");
  event.stopImmediatePropagation();
});

button.addEventListener("click", () => {
  console.log("second listener");
});

document.body.addEventListener("click", () => {
  console.log("body listener");
});
```

버튼을 클릭하면 첫 번째 리스너만 실행됩니다. 두 번째 리스너와 조상인 `body`의 리스너는 실행되지 않습니다.

## `preventDefault()`는 다른 역할

링크 이동이나 폼 제출처럼 브라우저가 제공하는 기본 동작을 취소할 때 사용합니다. 이벤트 전파는 그대로 둘 수 있습니다.

```javascript
const link = document.querySelector("a");

link.addEventListener("click", (event) => {
  event.preventDefault(); // 링크 이동을 취소
  event.stopPropagation(); // 부모 리스너로 가는 전파도 중단
});
```

## 선택 기준

- 조상 요소의 리스너로 이벤트가 올라가지 않게 하려면 `stopPropagation()`.
- 같은 요소의 뒤이은 리스너까지 실행을 멈춰야 한다면 `stopImmediatePropagation()`.
- 링크 이동이나 폼 제출 같은 기본 동작을 취소하려면 `preventDefault()`.

전파를 막으면 이벤트 위임이나 다른 코드의 리스너에 영향을 줄 수 있으므로, 필요한 범위에서만 사용하세요. 프레임워크는 자체 이벤트 시스템을 둘 수 있어 바닐라 DOM 이벤트와 세부 동작이 다를 수 있습니다.
