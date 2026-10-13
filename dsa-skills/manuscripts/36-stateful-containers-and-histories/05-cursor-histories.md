<!-- lesson-kind: standard -->
<!-- lesson-id: cursor-histories -->
## Cut Forward History After A Write

<!-- stage: context -->
### A Forward Button That Shows Deleted Pages

A user opens a browser on the homepage, visits pages A, B and C, and presses the back button twice. The browser now shows page A. The user then types the address of page D and opens it. The forward button must now be disabled, because the user left the old path. A buggy history still offers B, and pressing it jumps to a page that no longer belongs to the visible path.

The same failure appears in a text editor that offers undo and redo. After two undo steps, a new keystroke must erase the redo steps. Each of these classes receives a long sequence of calls, and every answer depends on the calls that came before it. The lesson asks one question. Which stored values must the class keep so that back, forward and a new visit stay correct and cheap?

<!-- stage: naive -->
### Copying The Path On Every Visit

The direct method keeps a list of pages and an index of the current page. A visit that only appends to the end of the list is wrong, because the new page lands after C while the index still points at A. A correct version rebuilds the list from the pages up to the current one, adds the new page, and moves the index to it.

```java
final class SnapshotHistory {
    private java.util.List<String> pages = new java.util.ArrayList<>();
    private int at; // index of the page on screen

    SnapshotHistory(String homepage) { pages.add(homepage); }

    void visit(String url) {
        java.util.List<String> next = new java.util.ArrayList<>(pages.subList(0, at + 1));
        next.add(url);
        pages = next;
        at++;
    }

    String back(int steps) { at = Math.max(0, at - steps); return pages.get(at); }

    String forward(int steps) { at = Math.min(pages.size() - 1, at + steps); return pages.get(at); }
}
```

For the visit sequence above, the list after the second back press is `[home, A, B, C]` with `at = 1`. The visit of D builds `[home, A, D]`, so forward from D finds nothing. The method is correct and easy to read.

<!-- stage: bottleneck -->
### Counting The Copied Entries

```predict
A user visits 100 000 pages in a row and never presses back. About how many list entries does the copying visit method move in total, and are any of those copies ever read again?

About 5 billion entries, because the visit number `i` copies `i` entries and the sum of 1 to 100 000 is roughly 5 * 10^9. The old list is discarded after each copy, so none of the copied entries is read again.
```

A history with `n` pages makes every visit copy up to `n` entries, so `n` visits cost O(n^2) time. A text editor that stores a full snapshot of the text after each keystroke is worse. A document of length `L` costs O(L) per keystroke and O(L) extra memory per kept snapshot.

The work has a precise waste. The pages after the current index are the ones the visit discards, and nothing reads them again. The pages before the current index do not change at all, yet the method copies them. Removing the discarded pages one by one also costs time proportional to how many were discarded. The next section shows that the class needs neither the copy nor the removal.

<!-- stage: insight -->
### One Array And Two Numbers

#### Keep Elements And A Cursor

Store the pages in one array that never gets rebuilt. Keep one integer called the **cursor**, which is the index of the page on screen. The array and the cursor together define what the user sees, so back and forward only change the cursor and write nothing.

<!-- names: cursor, live length, clamp -->

#### Hide The Dead Future With A Count

Keep a second integer called the **live length**, which is the number of array slots that belong to the current path. Slots at index `live length` and above are dead: they hold old pages that no call may return. A visit moves the cursor one slot to the right, writes the new page into that slot, and sets the live length to cursor plus 1. The write overwrites one old slot, and the new live length hides every slot after it. Nothing is deleted, so a visit costs O(1) time.

#### Clamp Every Move

A request to go back 100 steps from slot 2 cannot move past slot 0. The **clamp** limits a target index to the legal range. Back uses the larger of 0 and cursor minus steps. Forward uses the smaller of live length minus 1 and cursor plus steps. The clamp never touches the array, so an oversized request cannot corrupt the history. The stored array and the cursor keep describing one consistent path after every call.

<!-- stage: variables -->
### State Kept Between Calls

The class keeps three fields and one rule that connects them.

- **items** is the array of pages; slots from live length upward may hold stale pages.
- **cursor** is the index of the page on screen, always between 0 and live length minus 1.
- **live length** is the count of slots that belong to the current path, at least 1 after the constructor.

The state invariant is that the visible path is exactly `items[0..live length)`, the page on screen is `items[cursor]`, and no public call reads a slot at index live length or above. Visit, back and forward each end with this statement true again.

<!-- stage: trace -->
### Tracing Back, Visit And Clamping

#### Visit After Going Back

The first trace follows the opening story with six slots. In the trace below, the pointer `cursor` marks the page on screen, and the pointer `live` marks the first dead slot. Each cell is one slot index, and the `slots` value lists the stored pages, with a dash for a slot never written.

The homepage `H` sits in slot 0. The visits of A, B and C each move the cursor one slot right and raise the live length to 4. Then back(2) moves the cursor from slot 3 to slot 1 and changes no slot. The visit of D writes into slot 2 and sets the live length to 3. Slot 3 still holds C, but the live length of 3 hides it, so forward from D stays on D. The step count here is small, and each call changes at most one slot and two integers.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["cursor","live"],"steps":[{"at":{"cursor":0,"live":1},"vars":{"slots":"H,-,-,-,-,-"},"note":"The history starts with the homepage in slot 0, so the cursor is 0 and the live length is 1."},{"at":{"cursor":1,"live":2},"vars":{"slots":"H,A,-,-,-,-"},"note":"visit(A): the cursor moves to slot 1, the page is written there, and the live length becomes 2."},{"at":{"cursor":2,"live":3},"vars":{"slots":"H,A,B,-,-,-"},"note":"visit(B): the cursor moves to slot 2, the page is written there, and the live length becomes 3."},{"at":{"cursor":3,"live":4},"vars":{"slots":"H,A,B,C,-,-"},"note":"visit(C): the cursor moves to slot 3, the page is written there, and the live length becomes 4."},{"at":{"cursor":1,"live":4},"vars":{"slots":"H,A,B,C,-,-"},"note":"back(2): the target 1 is inside the live range. The cursor moves from 3 to 1; no slot changes."},{"at":{"cursor":2,"live":3},"vars":{"slots":"H,A,D,C,-,-"},"note":"visit(D): the cursor moves to slot 2, the page is written there, and the live length becomes 3. Slot 3 still holds C, but the live length 3 hides it."}]}
```

#### Oversized Moves On The Same State

The second trace starts from the final state of the first one. A forward(5) request would target slot 7, so the clamp stops the cursor at slot 2, the last live slot. A back(9) request would target a negative slot, so the clamp stops the cursor at slot 0. A forward(1) then moves to slot 1, and a visit of E overwrites slot 2.

The trace shows the stale page C in slot 3 through every step. The clamp never lets the cursor reach it, and the visit never needs to erase it. Both facts follow from the same rule: the cursor stays below the live length.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["cursor","live"],"steps":[{"at":{"cursor":2,"live":3},"vars":{"slots":"H,A,D,C,-,-"},"note":"The state after the first trace: cursor 2, live length 3, and the old page C still sits in slot 3."},{"at":{"cursor":2,"live":3},"vars":{"slots":"H,A,D,C,-,-"},"note":"forward(5): the target 7 is past the last live slot, so the clamp stops the cursor at 2. The cursor moves from 2 to 2; the live length stays 3."},{"at":{"cursor":0,"live":3},"vars":{"slots":"H,A,D,C,-,-"},"note":"back(9): the target -7 is below 0, so the clamp stops the cursor at 0. The cursor moves from 2 to 0; no slot changes."},{"at":{"cursor":1,"live":3},"vars":{"slots":"H,A,D,C,-,-"},"note":"forward(1): the target 1 is inside the live range. The cursor moves from 0 to 1; the live length stays 3."},{"at":{"cursor":2,"live":3},"vars":{"slots":"H,A,E,C,-,-"},"note":"visit(E): the cursor moves to slot 2, the page is written there, and the live length becomes 3. The write replaced D in slot 2; slot 3 is still unreachable."}]}
```

<!-- stage: code -->
### Browser History With A Cursor

#### The Class

The class stores the pages in a growable array. The field `liveLength` holds the live length from the trace, and `cursor` holds the cursor. Growing the array when it is full costs O(1) amortized per visit.

```java
final class CursorHistory {
    private String[] items = new String[8];
    private int cursor;      // slot of the page on screen
    private int liveLength;  // slots 0..liveLength-1 form the current path

    CursorHistory(String homepage) { items[0] = homepage; liveLength = 1; }

    void visit(String url) {
        if (cursor + 1 == items.length) items = java.util.Arrays.copyOf(items, items.length * 2);
        items[++cursor] = url;   // overwrite one old slot
        liveLength = cursor + 1; // everything after it becomes dead
    }

    String back(int steps) { cursor = Math.max(0, cursor - steps); return items[cursor]; }

    String forward(int steps) { cursor = Math.min(liveLength - 1, cursor + steps); return items[cursor]; }
}
```

#### Cost And Java Details

- **visit** costs O(1) amortized time, because a doubling copy happens after every doubling number of visits.
- **back** and **forward** cost O(1) time and read one slot.

Stale references stay in memory until a later visit overwrites them, so a very long history that shrinks holds pages longer than needed. Setting dead slots to `null` would free them but costs time proportional to the number discarded, so the design keeps them. The expression `cursor + steps` can overflow when `steps` is near `Integer.MAX_VALUE`, which the Boundary exercise below addresses.

<!-- stage: applicability -->
### When Cursor And Live Length Apply

#### Recognizing The Pattern

Use this design when a class supports moving through past states and a new write must discard part of the future. The statement usually says back, forward, undo or redo, and it says that a new action clears what lies ahead. The invariant to state before coding is that the stored elements and the cursor jointly define the visible state, with every slot at or above the live length unreadable.

#### Two False Friends

A stack looks like the natural tool for back, because back pops the latest page. It is a false friend here, since forward needs the popped pages, which forces a second stack that a visit must empty. The array with a cursor expresses the same behavior with two integers and no moving of elements.

A text editor with a movable caret is a second false friend. Its caret also sits inside stored elements, yet the caret divides the text into a part before it and a part after it, and an insert at the caret changes the middle of the sequence. No slot range plus one cursor describes that state, so the Recognize exercise below keeps the text in two parts.

#### When Not To Use It

Do not use it when the user can branch, because a version tree keeps both futures, and truncation would lose one of them. Do not use it when the history must stay bounded by memory, since the array never shrinks without a separate eviction rule. Do not use it for a concurrent class, because two threads can change the cursor and the live length between two reads.

<!-- stage: exercises -->
### Exercises

#### [Build] Undoable String Cursor (Author exercise)
<!-- id: sc-cursor-histories-undo-string -->

**Prerequisites.** The cursor and live length fields from this lesson.

**Problem.** Design a class `UndoString` that stores a text built one character at a time. The constructor takes no arguments and starts with the empty text. `append(char c)` adds `c` to the end of the visible text and discards every character that undo had hidden. `undo(int k)` hides the last `k` visible characters. `redo(int k)` shows the `k` most recently hidden characters again, if no append happened after they were hidden. `text()` returns the visible text as a `String`.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Undo** receives `0 <= k <=` the number of visible characters.
- **Redo** receives `0 <= k <=` the number of hidden characters that may be shown.
- **Characters** are lowercase English letters and `!`.
- **Mutation** does not occur outside the class.

**Example 1.** Input calls `append('h')`, `append('i')`, `append('!')`, `undo(2)`, `text()`, `append('o')`, `text()`, `undo(1)`, `redo(1)`, `text()`. Output of the three `text()` calls is `"h"`, `"ho"` and `"ho"`.

**Example 2.** Input calls `append('a')`, `append('b')`, `append('c')`, `append('d')`, `undo(3)`, `redo(2)`, `text()`, `append('e')`, `text()`, `undo(4)`, `text()`. Output of the three `text()` calls is `"abc"`, `"abce"` and `""`.

**Hint.** Which slot does an append write after an undo, and which number hides the characters that were undone earlier?

**Changed decision.** Basic case: the stored characters stay in place on undo, and an append overwrites one slot instead of building a new copy of the text.

#### [Vary] Design Browser History (LeetCode 1472)
<!-- id: sc-cursor-histories-browser -->

**Prerequisites.** The Undoable String Cursor exercise above.

**Problem.** Design a class `BrowserHistory`. The constructor takes a `homepage` string and shows it. `visit(String url)` opens `url` from the current page and removes every page that lay ahead of the current page. `back(int steps)` moves back by at most `steps` pages and returns the page now shown. `forward(int steps)` moves ahead by at most `steps` pages and returns the page now shown. Movement stops at the oldest or the newest page that is still part of the path.

**Constraints.** The limits are:
- **Homepage and urls** have `1 <= length <= 20` lowercase letters, digits and dots.
- **Steps** satisfy `1 <= steps <= 100`.
- **Calls** number at most `5000`.
- **Return** is the page shown after the call; `visit` returns nothing.

**Example 1.** Input: homepage `"start.com"`, then `visit("a.com")`, `visit("b.com")`, `visit("c.com")`, `back(1)`, `back(1)`, `visit("d.com")`, `forward(2)`, `back(3)`, `forward(1)`. Output of the five navigation calls is `"b.com"`, `"a.com"`, `"d.com"`, `"start.com"` and `"a.com"`, in that order, with `d.com` coming from `forward(2)`.

**Example 2.** Input: homepage `"x"`, then `visit("y")`, `visit("z")`, `back(5)`, `forward(1)`, `visit("w")`, `forward(1)`, `back(1)`, `forward(9)`. Output of the five navigation calls is `"x"`, `"y"`, `"w"`, `"y"` and `"w"`.

**Hint.** After a visit from the middle of the path, which single integer makes the old forward pages unreachable without deleting them?

**Changed decision.** The class stores pages and must discard the forward path on a visit, so a live length joins the cursor.

#### [Boundary] Oversized Navigation (Author exercise)
<!-- id: sc-cursor-histories-oversized -->

**Prerequisites.** The Undoable String Cursor and Design Browser History exercises above.

**Problem.** Extend `UndoString` so that `undo(int k)` and `redo(int k)` accept any `k` from `0` to `Integer.MAX_VALUE`. Each method moves as far as the legal range allows and returns the number of characters it actually hid or showed. An oversized request must not change the stored characters and must not make a later `redo` or `append` behave differently from a request of the exact legal size.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Steps** satisfy `0 <= k <= 2147483647`.
- **Return** is an `int` between 0 and the legal range, inclusive.
- **Characters** are lowercase English letters.
- **Empty text** accepts `undo` with a return of 0.

**Example 1.** Input calls `append('a')`, `append('b')`, `undo(2147483647)`, `text()`, `redo(2147483647)`, `text()`, `undo(1)`, `append('c')`, `redo(5)`, `text()`. Output is `2`, `""`, `2`, `"ab"`, `1`, `0` and `"ac"` for the calls that return a value.

**Example 2.** Input calls `undo(5)` on the empty text, `append('z')`, `redo(2147483647)`, `text()`, `undo(0)`. Output is `0`, `0`, `"z"` and `0` for the calls that return a value.

**Hint.** What does `cursor + k` produce in `int` arithmetic when `k` is `2147483647`, and how can the comparison avoid that sum?

**Changed decision.** The call returns the distance moved and the arithmetic compares `k` against the available distance, so no sum overflows.

#### [Recognize] Design a Text Editor (LeetCode 2296)
<!-- id: sc-cursor-histories-text-editor -->

**Prerequisites.** The Design Browser History and Oversized Navigation exercises above.

**Problem.** Design a class `TextEditor` that holds a text and a caret between two characters. It starts empty with the caret at position 0. `addText(String text)` inserts `text` at the caret and leaves the caret after the inserted characters. `deleteText(int k)` removes up to `k` characters before the caret and returns the number removed. `cursorLeft(int k)` and `cursorRight(int k)` move the caret by up to `k` positions and return the last `min(10, p)` characters before the caret, where `p` is the number of characters before the caret after the move.

**Constraints.** The limits are:
- **Calls** number at most `2 * 10^4`.
- **Text** per `addText` has `1 <= length <= 40` lowercase letters and digits.
- **Steps** satisfy `1 <= k <= 40`.
- **Return** of the move methods is a `String` of length at most 10.

**Example 1.** Input calls `addText("hello")`, `addText("world")`, `cursorLeft(3)`, `deleteText(4)`, `addText("xyz")`, `cursorRight(20)`, `cursorLeft(2)`, `deleteText(50)`, `cursorLeft(5)`. Output is `"hellowo"`, `4`, `"helxyzrld"`, `"helxyzr"`, `7` and `""` for the calls that return a value.

**Example 2.** Input calls `addText("abcdefghijklmn")`, `cursorLeft(1)`, `cursorLeft(12)`, `cursorRight(100)`, `deleteText(3)`, `cursorLeft(2)`. Output is `"defghijklm"`, `"a"`, `"efghijklmn"`, `3` and `"abcdefghi"` for the calls that return a value.

**Hint.** If the caret splits the text into a left part and a right part, which end of each part does every operation touch?

**Changed decision.** The visible state is no longer a prefix of one array; the caret splits the text into two parts, and every call touches only the ends beside the caret.
