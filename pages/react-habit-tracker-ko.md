---
layout: page
title: React Habit Tracker 실습
permalink: /coding/react-habit-tracker/ko/
nav_exclude: true
---

[English version](/coding/react-habit-tracker/)

## 프로젝트 소개

[Learn React With This One Project](https://www.youtube.com/watch?v=9aTRnV6g0eQ&t=4138s) 튜토리얼을 따라 만든 주간 습관 추적기다. React 컴포넌트가 어떻게 연결되고 상태가 어떻게 이동하는지 이해하기 위한 실습 프로젝트다. [소스 저장소](https://github.com/mjlee0914/react-practice-habit-tracker)는 비공개이므로 파일 링크를 열려면 저장소 접근 권한이 필요하다.

습관 추가·삭제, 날짜별 완료 처리, 오늘의 완료 개수, 연속 달성일을 확인할 수 있다. 데이터는 현재 브라우저의 `localStorage`에 저장되므로 계정이나 서버가 필요하지 않다.

## 미리보기

아래 미리보기는 같은 핵심 UI와 완료 토글 동작을 구현한 작은 React 데모다. 실제 저장소의 토글 코드에는 아래에서 설명하는 버그가 하나 있으며, 미리보기에서는 의도한 동작으로 수정했다.

<div class="my-4">
  <iframe
    src="/coding/react-habit-tracker-demo/"
    title="React 습관 추적기 실습 미리보기"
    loading="lazy"
    style="display:block; width:100%; height:620px; border:0; border-radius:14px; background:#f7f7fb;"
  ></iframe>
</div>

미리보기가 표시되지 않으면 [새 탭에서 열기](/coding/react-habit-tracker-demo/).

## 컴포넌트 연결 구조

`main.tsx`가 `App`을 화면에 마운트한다. `App`은 전체 UI를 구성하는 부모이며 주 선택 상태를 소유한다. 계산한 날짜와 주 이동 콜백을 필요한 자식에게 전달한다.

```text
main.tsx
└── App
    └── HabitProvider
        ├── Header       props: visibleDates, onPrev, onNext
        ├── HabitForm    Context: addHabit
        └── HabitList    props: visibleDates; Context: habits
            └── HabitItem Context: deleteHabit, toggleHabit
                └── Button
```

`HabitProvider`는 세 개의 형제 UI 컴포넌트를 감싼다. 여는 태그와 닫는 태그 사이의 JSX는 `children`으로 전달된다.

```tsx
<HabitProvider>
  <Header visibleDates={visibleDates} onPrev={goToPreviousWeek} onNext={goToNextWeek} />
  <HabitForm />
  <HabitList visibleDates={visibleDates} />
</HabitProvider>
```

Provider가 자식들을 Habit Context 안에서 렌더링하므로 모든 단계에 같은 `habits`와 handler props를 전달하지 않아도 하위 컴포넌트가 공유 데이터에 접근할 수 있다.

### Props: App에서 전달하는 값과 콜백

`App`은 선택한 주의 일곱 날짜를 만들고 `Header`와 `HabitList`에 전달한다. 자신의 주 상태를 바꾸는 함수도 함께 넘긴다.

```tsx
<Header
  visibleDates={visibleDates}
  onNext={() => setWeekOffset((offset) => offset + 1)}
  onPrev={() => setWeekOffset((offset) => offset - 1)}
/>
<HabitList visibleDates={visibleDates} />
```

자식인 `Header`는 콜백으로 변경을 요청하고, 실제 `weekOffset` 상태의 소유권은 부모 `App`에 남는다.

### Context: 공유하는 습관 데이터와 동작

Provider는 습관 목록을 저장하고 `habits`, `addHabit`, `deleteHabit`, `toggleHabit`을 공개한다. `HabitForm`은 `addHabit`을 호출하고, `Header`와 `HabitList`는 `habits`를 읽으며, 각 `HabitItem`은 삭제나 완료 토글을 호출한다.

```tsx
<HabitContext value={{ habits, addHabit, toggleHabit, deleteHabit }}>
  {children}
</HabitContext>
```

이 프로젝트는 React 19의 `<HabitContext value={...}>` 문법을 사용한다. 이전 React 버전에서는 `<HabitContext.Provider value={...}>`를 사용한다.

## 파일별 역할

### `src/main.tsx`: 진입점

React DOM 렌더러, 전역 CSS, `App`을 가져온다. `createRoot(document.getElementById("root")!)`로 `index.html`의 빈 root 요소를 찾고 컴포넌트 트리를 렌더링한다. `StrictMode`는 개발 중 일부 실수를 발견하는 데 도움을 준다.

### `src/App.tsx`: 부모 레이아웃과 주 상태

`App`이 `weekOffset`을 소유한다. `0`은 이번 주이며 값을 더하거나 빼서 표시할 주를 이동한다. date-fns로 월요일부터 일요일까지 계산한다.

```tsx
const [weekOffset, setWeekOffset] = useState(0);
const week = addWeeks(new Date(), weekOffset);

const visibleDates = eachDayOfInterval({
  start: startOfWeek(week, { weekStartsOn: 1 }),
  end: endOfWeek(week, { weekStartsOn: 1 }),
});
```

이 파일의 `useEffect`는 document click listener를 등록하고 cleanup 함수에서 제거한다. 화면 동작에 필요한 기능이라기보다 Effect 연습용 예제다.

### `src/components/Header.tsx`: 상태와 주 이동

`visibleDates`, `onPrev`, `onNext`를 props로 받고 Context에서 `habits`를 읽어 오늘 완료한 습관 수를 계산한다. 이전·다음 버튼은 부모가 전달한 콜백을 호출한다. 표시 중인 주에 오늘이 포함되면 Next 버튼을 비활성화한다.

### `src/components/HabitForm.tsx`: 제어 컴포넌트

입력값을 `useState("")`로 관리한다. `value`가 React 상태에서 오고 `onChange`가 그 상태를 바꾸므로 제어 입력이다. 제출 시 기본 새로고침을 막고 빈 이름을 무시한 뒤 `addHabit(name)`을 호출한다.

```tsx
const [name, setName] = useState("");
const { addHabit } = useHabits();

function handleSubmit(event: SubmitEvent) {
  event.preventDefault();
  if (name.trim() === "") return;
  setName("");
  addHabit(name);
}
```

### `src/components/HabitList.tsx`: 목록과 날짜 렌더링

Context에서 습관을, props에서 주간 날짜를 받는다. 습관이 없으면 빈 상태를 반환하고, 있으면 안정적인 habit ID를 `key`로 사용해 `HabitItem`을 렌더링한다. 각 날짜 버튼은 완료 여부에 따라 스타일이 바뀌며 클릭 시 `toggleHabit(id, date)`를 호출한다.

### 확인할 상태 업데이트 버그

`src/context/HabitProvider.tsx`의 `toggleHabit`은 이미 완료한 날짜를 다시 누르면 제거해야 한다. 현재 코드는 선택한 날짜와 같은 항목만 남겨 다른 완료 날짜를 버린다.

```tsx
// 현재 코드: 선택한 날짜를 계속 유지한다.
h.completions.filter((completion) => isSameDay(completion, date))
```

올바른 토글은 선택한 날짜가 **아닌** 항목을 남겨야 한다.

```tsx
h.completions.filter((completion) => !isSameDay(completion, date))
```

미리보기는 올바른 동작을 구현하지만 저장소 코드는 학습을 위해 그대로 두었다.

### `src/context/HabitProvider.tsx`: 상태의 단일 출처

`useLocalStorage` Hook으로 습관을 초기화하고 세 가지 업데이트를 정의한다.

- `addHabit`: 고유 ID와 빈 완료 목록을 가진 습관 추가
- `deleteHabit`: 선택한 ID를 제외한 습관 유지
- `toggleHabit`: 해당 습관의 날짜를 추가하거나 제거

함수형 상태 업데이트를 사용해 항상 최신 값에서 계산하고, 기존 상태를 직접 변경하지 않고 새 배열과 객체를 만든다.

### `src/context/useHabits.ts`: Context 타입과 소비 Hook

`Habit`과 Context 타입을 정의하고 `useHabits()`를 제공한다. 이 Hook은 `useContext(HabitContext)`를 호출하고 Provider 밖에서 사용되면 명확한 오류를 던진다.

### `src/hooks/useLocalStorage.ts`: 저장 Hook

React 상태와 브라우저 저장소를 결합한다. 지연 초기화 함수가 저장값을 읽고 `useEffect`가 값이나 저장 key가 바뀔 때 최신 상태를 기록한다. JSON reviver는 저장된 ISO 날짜 문자열을 다시 `Date` 객체로 바꾼다.

### `src/components/Button.tsx`와 `src/index.css`

`Button`은 일반 HTML button 속성과 `variant`를 받고 `twMerge`로 스타일 클래스를 합친다. 전역 CSS는 Tailwind CSS를 가져오며, 대부분의 레이아웃과 색상은 컴포넌트의 utility class로 작성되어 있다.

## Hooks를 쉬운 말로 정리하기

| Hook | 역할 | 이 프로젝트 |
| --- | --- | --- |
| `useState` | 바뀔 수 있는 값을 저장하고 변경 시 다시 렌더링 | 주, 폼 입력, 습관 |
| `useEffect` | 렌더링 후 저장·이벤트 연결 같은 동기화 작업 실행 | localStorage, click listener |
| `useContext` | 상위 Provider가 제공하는 값 읽기 | `useHabits` 내부 |
| `useRef` | 다시 렌더링하지 않고 렌더 사이의 값 유지 | 사용하지 않음 |
| `useLocalStorage` | 상태와 브라우저 저장·날짜 복원을 결합한 custom Hook | 사용 |
| `useHabits` | Habit Context를 읽고 Provider 존재 여부 확인 | 사용 |

React에는 `useStatus`라는 기본 Hook이 없다. 상태를 저장하는 Hook은 `useState`이며 `status`는 변수 이름으로 사용할 수 있다.

## 데이터와 저장 방식

- 현재 브라우저의 `localStorage`에서 `Habits` key를 사용한다.
- 브라우저 저장소를 지우면 습관도 사라진다.
- 다른 브라우저나 기기와 데이터가 동기화되지 않는다.
- 완료 날짜는 JSON으로 저장되고 `dateReviver`가 `Date` 객체로 복원한다.
- 계정, 원격 DB, API는 사용하지 않는다.

## 로컬 실행

```bash
npm install
npm run dev
```

그 밖의 명령은 `npm run build`, `npm run preview`, `npm run lint`다.
