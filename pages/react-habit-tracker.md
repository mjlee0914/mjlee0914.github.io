---
layout: page
title: React Habit Tracker Practice
permalink: /coding/react-habit-tracker/
---

## What this project is

This is a weekly habit tracker I made by following [Learn React With This One Project](https://www.youtube.com/watch?v=9aTRnV6g0eQ&t=4138s). It is a practice project for seeing how React components fit together and how state moves through an app. The [source repository](https://github.com/mjlee0914/react-practice-habit-tracker) is private, so its file links require repository access.

The app lets you add or delete habits, mark them complete on dates in the displayed week, review today's completion count, and see a streak. The project saves habits in this browser's `localStorage`, so it does not need an account or server.

## Try the preview

The embedded preview is a small React demo with the same main UI and an operational completion toggle. The repository is the source to study; there is one bug in its current toggle code, explained below.

<div class="my-4">
  <iframe
    src="/coding/react-habit-tracker-demo/"
    title="Interactive React habit tracker practice preview"
    loading="lazy"
    style="display:block; width:100%; height:620px; border:0; border-radius:14px; background:#f7f7fb;"
  ></iframe>
</div>

If the embedded preview does not load, [open it in a new tab](/coding/react-habit-tracker-demo/).

## How the component tree connects

`main.tsx` mounts `App` into the page. `App` is the parent that puts the main UI together. It owns the week selector and sends the calculated dates and week-navigation callbacks to the components that need them.

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

`HabitProvider` wraps the three sibling UI components. In JSX, everything placed between its opening and closing tags is passed to it as `children`:

```tsx
<HabitProvider>
  <Header visibleDates={visibleDates} onPrev={goToPreviousWeek} onNext={goToNextWeek} />
  <HabitForm />
  <HabitList visibleDates={visibleDates} />
  </HabitProvider>
```

The provider renders those children inside the habit Context. That gives descendants access to shared habit data without passing the same `habits` and handler props through every level.

### Props: values and callbacks from App

`App` creates seven dates for the selected week. It passes those dates to `Header` and `HabitList`. It also passes functions that change its own week state:

```tsx
<Header
  visibleDates={visibleDates}
  onNext={() => setWeekOffset((offset) => offset + 1)}
  onPrev={() => setWeekOffset((offset) => offset - 1)}
/>
<HabitList visibleDates={visibleDates} />
```

The callback lets `Header` request a change while `App` remains the owner of `weekOffset`. This is the common React pattern of keeping state in a parent and passing a value or callback to a child.

### Context: shared habit values and actions

The provider stores the habit list and publishes four values: `habits`, `addHabit`, `deleteHabit`, and `toggleHabit`. `HabitForm` calls `addHabit`; `Header` and `HabitList` read `habits`; each `HabitItem` calls `deleteHabit` or `toggleHabit`.

```tsx
<HabitContext value={{ habits, addHabit, toggleHabit, deleteHabit }}>
  {children}
</HabitContext>
```

This project uses React 19's Context provider syntax, `<HabitContext value={...}>`. In older React versions, the equivalent is `<HabitContext.Provider value={...}>`.

## Source files, one by one

The notes below follow the actual file names and component responsibilities in the repository.

### [`src/main.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/main.tsx) — the entry point

This file imports React's DOM renderer, global CSS, and `App`. `createRoot(document.getElementById("root")!)` finds the empty `root` element in `index.html`; `.render(...)` tells React to draw the component tree there. `StrictMode` helps surface some mistakes during development.

### [`src/App.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/App.tsx) — parent layout and week state

`App` owns `weekOffset`. The initial value `0` means the current week; adding or subtracting one moves the displayed week. It uses date-fns to derive Monday through Sunday, then renders the header, form, and list inside the provider.

```tsx
const [weekOffset, setWeekOffset] = useState(0);
const week = addWeeks(new Date(), weekOffset);

const visibleDates = eachDayOfInterval({
  start: startOfWeek(week, { weekStartsOn: 1 }),
  end: endOfWeek(week, { weekStartsOn: 1 }),
});
```

The `useEffect` in this file registers a document click listener and returns a cleanup function that removes the listener. Its dependency is `weekOffset`, so React cleans up the previous listener and runs the effect again when that value changes. In this project the listener only logs the current offset; it is a practice example, not required for the visible tracker behavior.

### [`src/components/Header.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/components/Header.tsx) — status and week controls

`Header` receives `visibleDates`, `onPrev`, and `onNext` as props. It reads `habits` from Context to count habits completed today. It formats the first and last date as the displayed week range, then calls the callbacks when the navigation buttons are clicked. The Next button is disabled if the visible week already contains today.

### [`src/components/HabitForm.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/components/HabitForm.tsx) — controlled input

The form uses `useState("")` for the current input value. Because the input's `value` comes from React state and `onChange` updates that state, it is a **controlled input**. When the user submits, the handler prevents the browser's default page reload, ignores an empty name, clears the field, and calls `addHabit(name)` from Context.

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

### [`src/components/HabitList.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/components/HabitList.tsx) — rendering each habit and day

`HabitList` gets the habits from Context and the week dates from props. If the list is empty, it returns the empty-state message. Otherwise, it maps each habit to a `HabitItem` and gives it a stable `key` based on the habit ID.

Each `HabitItem` displays the habit name and streak, then maps the seven dates to buttons. A button's style reflects whether that date is in the completion list. Clicking it calls `toggleHabit(id, date)`; clicking Delete calls `deleteHabit(id)`. The `getStreak` helper counts consecutive completed dates going backward from today.

### A small state-update bug to notice

In [`src/context/HabitProvider.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/context/HabitProvider.tsx), `toggleHabit` is meant to remove a date if it is already complete. The current branch filters *for* the same day, though, which keeps that date and drops other dates in the habit's completion list:

```tsx
// Current source: this condition keeps the selected date.
h.completions.filter((completion) => isSameDay(completion, date))
```

For a true toggle, the filter should keep dates that are **not** the selected day:

```tsx
h.completions.filter((completion) => !isSameDay(completion, date))
```

The preview implements that intended behavior. I left the repository code unchanged so this page documents what is there and points out the exact correction to study.

### [`src/context/HabitProvider.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/context/HabitProvider.tsx) — habit state and update functions

This provider is the source of truth for the habit list. It initializes habits with the custom `useLocalStorage` Hook and defines three state updates:

- `addHabit` appends a new habit with a unique ID and an empty completion list.
- `deleteHabit` keeps every habit except the one with the selected ID.
- `toggleHabit` finds the matching habit and adds or removes the selected date. See the bug note above for the current removal-condition issue.

The update callbacks use functional state updates (`setHabits((current) => ...)`) so each update starts from the latest value. They create new arrays and objects instead of mutating existing React state.

### [`src/context/useHabits.ts`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/context/useHabits.ts) — Context type and consumer Hook

This file defines the `Habit` and `Context` TypeScript types, creates the Context, and exports `useHabits()`. That custom Hook calls React's `useContext(HabitContext)`. If a component is rendered outside `HabitProvider`, it throws an error instead of letting a missing Context value fail silently.

The custom Hook is a convenience: components can write `const { habits } = useHabits()` instead of repeating the Context lookup and null check.

### [`src/hooks/useLocalStorage.ts`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/hooks/useLocalStorage.ts) — reusable persistence Hook

`useLocalStorage<T>` combines React state with the browser's storage API. Its lazy `useState` initializer reads the saved value when the Hook is initialized. Its `useEffect` writes the latest state to `localStorage` when either the value or storage key changes.

The JSON reviver converts saved ISO date strings back into `Date` objects. Without that step, JSON would restore completions as strings, which would break date comparisons in the tracker.

### [`src/components/Button.tsx`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/components/Button.tsx) — reusable button

`Button` accepts the normal HTML button properties plus a `variant`. It spreads those properties onto the native `<button>`, selects style classes for the requested variant, and combines the classes with `twMerge`. The other components reuse it for the form, day controls, navigation, and deletion.

### [`src/index.css`](https://github.com/mjlee0914/react-practice-habit-tracker/blob/main/src/index.css) — global styles

This file imports Tailwind CSS and sets the page's dark background and light text colors. Most layout and color choices in the components are Tailwind utility classes; Vite's Tailwind plugin processes them for the app.

## Hooks in plain language

Hooks are React functions that let function components use React features. Built-in Hook names start with `use`; custom Hooks follow that naming rule too. Hooks are called at the top level of a component or another Hook, not inside loops or conditional branches.

| Hook | Plain-language purpose | Used here? |
| --- | --- | --- |
| `useState` | Stores a value that can change. Updating it asks React to render the component again with the new value. | Yes: week, form input, and saved habits. |
| `useEffect` | Runs synchronization code after rendering, such as saving to storage or connecting a browser event. Its cleanup undoes a connection. | Yes: storage persistence and the click-listener example. |
| `useContext` | Reads a value from a matching Context provider above the component. | Yes, inside `useHabits`. |
| `useRef` | Holds a mutable value between renders without causing a re-render when `.current` changes. It is often used for DOM references or timer IDs. | No. There is no `useRef` call in this repository. |
| `useLocalStorage` | A custom Hook that combines state, storage reads/writes, and date restoration. | Yes. |
| `useHabits` | A custom Hook that reads the habit Context and checks that the provider exists. | Yes. |

There is no built-in Hook named `useStatus`. If you meant the Hook for storing a changing value, it is `useState`. “Status” can be a state variable name, for example `const [status, setStatus] = useState("idle")`, but React's Hook is still called `useState`.

## Data and storage notes

- The app saves data under the `Habits` key in this browser's `localStorage`.
- Clearing browser storage removes the saved habits. Data is not shared with another browser or device.
- Completion dates are serialized to JSON and restored to `Date` objects by `dateReviver`.
- There is no account, remote database, API, or cross-device sync in this practice app.

## Run the repository locally

```bash
npm install
npm run dev
```

Useful project scripts are `npm run build`, `npm run preview`, and `npm run lint`.

## Try it in the coding menu

Open [Coding Practice](/coding/) to find this page and use the embedded preview. The preview is served as a separate React page so GitHub Pages can frame it; the repository remains the source for studying the components discussed here.
