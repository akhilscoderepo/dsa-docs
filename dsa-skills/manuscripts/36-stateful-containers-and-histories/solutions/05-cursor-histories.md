<!-- solutions-for: 05-cursor-histories -->
### Solutions For Cursor Histories

#### Solution: [Build] Undoable String Cursor (Author exercise)
<!-- id: sc-cursor-histories-undo-string -->

**Approach.**
The class stores characters in one array and keeps two integers. The `cursor` counts the visible characters, and the `liveLength` counts the characters that undo may still bring back. Undo lowers the cursor and writes nothing. Redo raises the cursor and writes nothing. An append writes into the slot at the cursor, raises the cursor, and sets the live length equal to the cursor, which hides every character that undo had hidden.

The invariant is that `0 <= cursor <= liveLength <= size of the array`, the visible text is `items[0..cursor)`, and the redo candidates are `items[cursor..liveLength)`. The input contract promises legal step counts, so no method needs a clamp here.

**Complexity.**
- **Time** is O(1) amortized for append, undo and redo, and O(cursor) for `text()` because it copies the visible characters.
- **Space** is O(n) for n appended characters, since stale characters stay in the array until a later append overwrites them.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class UndoStringBuild {
    /** Stores characters once; the visible text is items[0..cursor) and redo candidates are items[cursor..liveLength). */
    static final class UndoString {
        private char[] items = new char[4];
        // Number of visible characters, also the next slot to write.
        private int cursor;
        // Number of slots that undo may still restore.
        private int liveLength;

        /** Time: O(1) amortized, because doubling happens after every doubling number of appends. Space: O(1) extra. Invariant: afterwards liveLength == cursor. */
        void append(char c) {
            // Grow only when the next slot does not exist; this is the only source of copying.
            if (cursor == items.length) items = java.util.Arrays.copyOf(items, items.length * 2);
            // Overwrite the slot at the cursor; a stale character there is lost on purpose.
            items[cursor++] = c;
            // Everything after the new character becomes dead, so redo has nothing to show.
            liveLength = cursor;
        }

        /** Time: O(1). Space: O(1). Invariant: the stored characters do not change. */
        void undo(int k) { cursor -= k; }

        /** Time: O(1). Space: O(1). Invariant: cursor never exceeds liveLength for legal k. */
        void redo(int k) { cursor += k; }

        /** Time: O(cursor) for the copy. Space: O(cursor) for the returned string. Invariant: reads only slots below cursor. */
        String text() { return new String(items, 0, cursor); }
    }

    /**
     * Brute-force oracle that stores a complete snapshot of the text after every append.
     * Time: O(L) per append for the copy. Space: O(n * L) for n snapshots.
     * Invariant: snapshots.get(pos) is the visible text, and snapshots after pos are the redo candidates.
     */
    static final class Oracle {
        // Snapshot 0 is the empty text.
        private List<String> snapshots = new ArrayList<>(List.of(""));
        private int pos;
        void append(char c) {
            // Drop the redo candidates, then add the new snapshot built by concatenation.
            snapshots = new ArrayList<>(snapshots.subList(0, pos + 1));
            snapshots.add(snapshots.get(pos) + c);
            pos++;
        }
        void undo(int k) { pos -= k; }
        void redo(int k) { pos += k; }
        String text() { return snapshots.get(pos); }
    }

    public static void main(String[] args) {
        // First worked example: append after undo drops the hidden characters.
        UndoString u = new UndoString();
        for (char c : "hi!".toCharArray()) u.append(c);
        u.undo(2);
        if (!u.text().equals("h")) throw new AssertionError("undo 2");
        u.append('o');
        if (!u.text().equals("ho")) throw new AssertionError("append after undo");
        u.undo(1);
        u.redo(1);
        if (!u.text().equals("ho")) throw new AssertionError("redo");
        // Second worked example: redo restores part of the hidden text, then an append hides the rest.
        u = new UndoString();
        for (char c : "abcd".toCharArray()) u.append(c);
        u.undo(3);
        u.redo(2);
        if (!u.text().equals("abc")) throw new AssertionError("partial redo");
        u.append('e');
        if (!u.text().equals("abce")) throw new AssertionError("append e");
        u.undo(4);
        if (!u.text().isEmpty()) throw new AssertionError("empty after full undo");
        // Random sequences with legal step counts compared against the snapshot oracle.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 3000; t++) {
            UndoString fast = new UndoString();
            Oracle slow = new Oracle();
            // Shadow counters supply the legal ranges for undo and redo.
            int visible = 0, live = 0;
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    char c = (char) ('a' + rnd.nextInt(3));
                    fast.append(c); slow.append(c);
                    visible++; live = visible;
                } else if (op == 1) {
                    int k = rnd.nextInt(visible + 1);
                    fast.undo(k); slow.undo(k);
                    visible -= k;
                } else {
                    int k = rnd.nextInt(live - visible + 1);
                    fast.redo(k); slow.redo(k);
                    visible += k;
                }
                if (!fast.text().equals(slow.text())) throw new AssertionError("mismatch at trial " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Design Browser History (LeetCode 1472)
<!-- id: sc-cursor-histories-browser -->

**Approach.**
The pages sit in one array. The `cursor` is the slot of the page on screen, and the `liveLength` is the number of slots that belong to the current path. Back lowers the cursor but not below 0, and forward raises it but not above `liveLength - 1`. A visit moves the cursor right by one, writes the url into that slot, and sets the live length to `cursor + 1`. The write replaces one old page, and the new live length hides every page after it, so the removed forward path needs no deletion.

The invariant is that the shown page is `items[cursor]`, the path is `items[0..liveLength)`, and `0 <= cursor < liveLength` after every call. Back and forward cannot break it, because each result is clamped into that range. The visit restores it because the cursor and the live length both end on the same new slot. The array doubles when the next slot does not exist.

**Complexity.**
- **Time** is O(1) amortized per call, because each call changes two integers and at most one slot, and doubling is paid by earlier visits.
- **Space** is O(n) for n visited pages, since the array keeps stale pages until later visits overwrite them.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class BrowserHistoryAnchor {
    /** Array plus cursor plus live length; no call deletes or copies the path. */
    static final class BrowserHistory {
        private String[] items = new String[4];
        // Slot of the page on screen.
        private int cursor;
        // Slots 0..liveLength-1 form the current path.
        private int liveLength;

        BrowserHistory(String homepage) { items[0] = homepage; liveLength = 1; }

        /** Time: O(1) amortized. Space: O(1) extra. Invariant: afterwards cursor == liveLength - 1. */
        void visit(String url) {
            // Double the array when the next slot does not exist; this is the only copying.
            if (cursor + 1 == items.length) items = Arrays.copyOf(items, items.length * 2);
            // Move right and overwrite one old slot.
            items[++cursor] = url;
            // Pages that were ahead of the old cursor become unreachable.
            liveLength = cursor + 1;
        }

        /** Time: O(1). Space: O(1). Invariant: the result lies in [0, cursor]. */
        String back(int steps) {
            // Clamp at the oldest page.
            cursor = Math.max(0, cursor - steps);
            return items[cursor];
        }

        /** Time: O(1). Space: O(1). Invariant: the result lies in [cursor, liveLength - 1]. */
        String forward(int steps) {
            // Clamp at the newest live page, never at a stale slot.
            cursor = Math.min(liveLength - 1, cursor + steps);
            return items[cursor];
        }
    }

    /**
     * Brute-force oracle that deletes the forward pages from a list on every visit.
     * Time: O(n) per visit for the removal. Space: O(n).
     * Invariant: the list holds exactly the current path and index is the page on screen.
     */
    static final class Oracle {
        private final List<String> path = new ArrayList<>();
        private int index;
        Oracle(String home) { path.add(home); }
        void visit(String url) {
            // Remove every page after the current one, then append.
            while (path.size() > index + 1) path.remove(path.size() - 1);
            path.add(url);
            index++;
        }
        String back(int steps) { while (steps-- > 0 && index > 0) index--; return path.get(index); }
        String forward(int steps) { while (steps-- > 0 && index < path.size() - 1) index++; return path.get(index); }
    }

    public static void main(String[] args) {
        // First worked example: the visit of d.com removes the forward pages b.com and c.com.
        BrowserHistory h = new BrowserHistory("start.com");
        h.visit("a.com"); h.visit("b.com"); h.visit("c.com");
        if (!h.back(1).equals("b.com") || !h.back(1).equals("a.com")) throw new AssertionError("back twice");
        h.visit("d.com");
        if (!h.forward(2).equals("d.com")) throw new AssertionError("forward after visit");
        if (!h.back(3).equals("start.com")) throw new AssertionError("back clamp");
        if (!h.forward(1).equals("a.com")) throw new AssertionError("forward one");
        // Second worked example: oversized steps stop at the ends of the live path, not at stale slots.
        h = new BrowserHistory("x");
        h.visit("y"); h.visit("z");
        if (!h.back(5).equals("x") || !h.forward(1).equals("y")) throw new AssertionError("x then y");
        h.visit("w");
        if (!h.forward(1).equals("w") || !h.back(1).equals("y") || !h.forward(9).equals("w")) throw new AssertionError("w path");
        // Random sequences compared against the oracle; many visits after back calls exercise truncation.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 3000; t++) {
            BrowserHistory fast = new BrowserHistory("h");
            Oracle slow = new Oracle("h");
            for (int step = 0; step < 60; step++) {
                int op = rnd.nextInt(3);
                int steps = 1 + rnd.nextInt(6);
                if (op == 0) {
                    String url = "p" + rnd.nextInt(1000);
                    fast.visit(url); slow.visit(url);
                } else if (op == 1) {
                    if (!fast.back(steps).equals(slow.back(steps))) throw new AssertionError("back mismatch " + t);
                } else {
                    if (!fast.forward(steps).equals(slow.forward(steps))) throw new AssertionError("forward mismatch " + t);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Oversized Navigation (Author exercise)
<!-- id: sc-cursor-histories-oversized -->

**Approach.**
Each move computes the distance it can travel before it changes anything. Undo can travel at most `cursor` characters, and redo can travel at most `liveLength - cursor`. The moved distance is the smaller of `k` and that limit. Comparing `k` with the limit avoids the sum `cursor + k`, which wraps to a negative `int` when `k` is `Integer.MAX_VALUE` and the cursor is positive. The method then adds or subtracts the moved distance and returns it.

This invariant matches the Build exercise: `0 <= cursor <= liveLength`. A move touches only the cursor, so the stored characters and the live length keep their values, and a later append or redo behaves as after an exact request.

**Complexity.**
- **Time** is O(1) per move and amortized O(1) per append.
- **Space** is O(n) for n appended characters, because stale slots stay until overwritten.

```java run
import java.util.Random;

public final class OversizedNavigation {
    /** Same storage as the Build solution, but moves report the distance actually travelled. */
    static final class UndoString {
        private char[] items = new char[2];
        private int cursor;
        private int liveLength;

        void append(char c) {
            if (cursor == items.length) items = java.util.Arrays.copyOf(items, items.length * 2);
            items[cursor++] = c;
            liveLength = cursor;
        }

        /** Time: O(1). Space: O(1). Invariant: the result is min(k, cursor) and the array is untouched. */
        int undo(int k) {
            // Compare k with the limit instead of computing cursor - k, so no arithmetic can wrap.
            int moved = Math.min(k, cursor);
            cursor -= moved;
            return moved;
        }

        /** Time: O(1). Space: O(1). Invariant: the result is min(k, liveLength - cursor). */
        int redo(int k) {
            // The limit is a small non-negative int; comparing it with k never overflows.
            int moved = Math.min(k, liveLength - cursor);
            cursor += moved;
            return moved;
        }

        String text() { return new String(items, 0, cursor); }
    }

    /**
     * Brute-force oracle that moves one character at a time on a string snapshot list.
     * Time: O(min(k, n)) per move. Space: O(n * L) for the snapshots.
     * Invariant: the loop stops at the edge of the stored range, so the count equals the legal distance.
     */
    static final class Oracle {
        private java.util.List<String> snaps = new java.util.ArrayList<>(java.util.List.of(""));
        private int pos;
        void append(char c) {
            snaps = new java.util.ArrayList<>(snaps.subList(0, pos + 1));
            snaps.add(snaps.get(pos) + c);
            pos++;
        }
        int undo(int k) { int m = 0; while (m < k && pos > 0) { pos--; m++; } return m; }
        int redo(int k) { int m = 0; while (m < k && pos < snaps.size() - 1) { pos++; m++; } return m; }
        String text() { return snaps.get(pos); }
    }

    public static void main(String[] args) {
        // The overflow that the exercise warns about: a positive int plus Integer.MAX_VALUE wraps negative.
        int c = 2;
        if (c + Integer.MAX_VALUE >= 0) throw new AssertionError("expected wraparound");
        // First worked example.
        UndoString u = new UndoString();
        u.append('a'); u.append('b');
        if (u.undo(Integer.MAX_VALUE) != 2 || !u.text().isEmpty()) throw new AssertionError("undo max");
        if (u.redo(Integer.MAX_VALUE) != 2 || !u.text().equals("ab")) throw new AssertionError("redo max");
        if (u.undo(1) != 1) throw new AssertionError("undo 1");
        u.append('c');
        if (u.redo(5) != 0 || !u.text().equals("ac")) throw new AssertionError("redo after append");
        // Second worked example: empty text and zero steps.
        u = new UndoString();
        if (u.undo(5) != 0) throw new AssertionError("undo on empty");
        u.append('z');
        if (u.redo(Integer.MAX_VALUE) != 0 || !u.text().equals("z") || u.undo(0) != 0) throw new AssertionError("redo on live end");
        // Random sequences that mix oversized and small steps compared against the oracle.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 3000; t++) {
            UndoString fast = new UndoString();
            Oracle slow = new Oracle();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                // Oversized steps are common, and Integer.MAX_VALUE appears often enough to hit the wrap case.
                int k = rnd.nextInt(4) == 0 ? Integer.MAX_VALUE : rnd.nextInt(6);
                if (op == 0) {
                    char ch = (char) ('a' + rnd.nextInt(3));
                    fast.append(ch); slow.append(ch);
                } else if (op == 1) {
                    if (fast.undo(k) != slow.undo(k)) throw new AssertionError("undo count " + t);
                } else {
                    if (fast.redo(k) != slow.redo(k)) throw new AssertionError("redo count " + t);
                }
                if (!fast.text().equals(slow.text())) throw new AssertionError("text mismatch " + t);
            }
        }
    }
}
```

#### Solution: [Recognize] Design a Text Editor (LeetCode 2296)
<!-- id: sc-cursor-histories-text-editor -->

**Approach.**
The editor keeps the text in two parts: `left` holds the characters before the caret in reading order, and `right` holds the characters after the caret in reverse order. Every operation touches only the end of one part or moves characters between the two ends. Insertion appends to `left`. Deletion shortens `left`. Moving the caret left pops characters from the end of `left` and pushes them onto `right`, and moving right does the reverse. After a move, the returned context is the last ten characters of `left`.

The invariant is that `left + reverse(right)` is the whole text and the caret sits where the two parts meet. Each call preserves it, because a move transfers a character without changing the order of the whole text. The cost of a call is proportional to the characters it moves, which the constraints bound by 40.

**Complexity.**
- **Time** is O(k) for each move and delete, O(length of the added text) for insertion, and O(10) for the returned context.
- **Space** is O(n) for the n characters currently held in the two parts.

```java run
import java.util.Random;

public final class TextEditorAnchor {
    /** Two StringBuilders; the caret sits between left and the reversed right. */
    static final class TextEditor {
        // Characters before the caret in reading order.
        private final StringBuilder left = new StringBuilder();
        // Characters after the caret, stored in reverse so the nearest one is last.
        private final StringBuilder right = new StringBuilder();

        /** Time: O(len(text)). Space: O(len(text)). Invariant: the caret ends after the new text. */
        void addText(String text) { left.append(text); }

        /** Time: O(1). Space: O(1). Invariant: only characters before the caret are removed. */
        int deleteText(int k) {
            // Cannot remove more than exist before the caret.
            int removed = Math.min(k, left.length());
            // setLength drops the last characters in constant time.
            left.setLength(left.length() - removed);
            return removed;
        }

        /** Time: O(k). Space: O(1) besides the answer. Invariant: left + reverse(right) is unchanged. */
        String cursorLeft(int k) {
            int moved = Math.min(k, left.length());
            // Move one character at a time from the end of left to the end of right.
            for (int i = 0; i < moved; i++) {
                right.append(left.charAt(left.length() - 1));
                left.setLength(left.length() - 1);
            }
            return context();
        }

        /** Time: O(k). Space: O(1) besides the answer. Invariant: left + reverse(right) is unchanged. */
        String cursorRight(int k) {
            int moved = Math.min(k, right.length());
            for (int i = 0; i < moved; i++) {
                left.append(right.charAt(right.length() - 1));
                right.setLength(right.length() - 1);
            }
            return context();
        }

        // The context is at most ten characters, so this copy costs O(10).
        private String context() { return left.substring(Math.max(0, left.length() - 10)); }
    }

    /**
     * Brute-force oracle with one string and an integer caret.
     * Time: O(n) per call for string rebuilding. Space: O(n).
     * Invariant: text.substring(0, caret) is the part before the caret.
     */
    static final class Oracle {
        private String text = "";
        private int caret;
        void addText(String s) { text = text.substring(0, caret) + s + text.substring(caret); caret += s.length(); }
        int deleteText(int k) {
            int m = Math.min(k, caret);
            text = text.substring(0, caret - m) + text.substring(caret);
            caret -= m;
            return m;
        }
        String cursorLeft(int k) { caret -= Math.min(k, caret); return ctx(); }
        String cursorRight(int k) { caret += Math.min(k, text.length() - caret); return ctx(); }
        private String ctx() { return text.substring(Math.max(0, caret - 10), caret); }
    }

    public static void main(String[] args) {
        // First worked example, including a delete larger than the text before the caret.
        TextEditor e = new TextEditor();
        e.addText("hello"); e.addText("world");
        if (!e.cursorLeft(3).equals("hellowo")) throw new AssertionError("left 3");
        if (e.deleteText(4) != 4) throw new AssertionError("delete 4");
        e.addText("xyz");
        if (!e.cursorRight(20).equals("helxyzrld")) throw new AssertionError("right 20");
        if (!e.cursorLeft(2).equals("helxyzr")) throw new AssertionError("left 2");
        if (e.deleteText(50) != 7 || !e.cursorLeft(5).isEmpty()) throw new AssertionError("delete 50");
        // Second worked example: the context shows only ten characters.
        e = new TextEditor();
        e.addText("abcdefghijklmn");
        if (!e.cursorLeft(1).equals("defghijklm")) throw new AssertionError("ten chars");
        if (!e.cursorLeft(12).equals("a")) throw new AssertionError("left 12");
        if (!e.cursorRight(100).equals("efghijklmn")) throw new AssertionError("right 100");
        if (e.deleteText(3) != 3 || !e.cursorLeft(2).equals("abcdefghi")) throw new AssertionError("delete 3");
        // Java behaviour: setLength truncates a StringBuilder in place.
        StringBuilder sb = new StringBuilder("abc");
        sb.setLength(1);
        if (!sb.toString().equals("a")) throw new AssertionError("setLength");
        // Random sequences compared against the oracle.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 3000; t++) {
            TextEditor fast = new TextEditor();
            Oracle slow = new Oracle();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(4);
                int k = 1 + rnd.nextInt(14);
                if (op == 0) {
                    StringBuilder s = new StringBuilder();
                    for (int i = 1 + rnd.nextInt(8); i > 0; i--) s.append((char) ('a' + rnd.nextInt(4)));
                    fast.addText(s.toString()); slow.addText(s.toString());
                } else if (op == 1) {
                    if (fast.deleteText(k) != slow.deleteText(k)) throw new AssertionError("delete " + t);
                } else if (op == 2) {
                    if (!fast.cursorLeft(k).equals(slow.cursorLeft(k))) throw new AssertionError("left " + t);
                } else {
                    if (!fast.cursorRight(k).equals(slow.cursorRight(k))) throw new AssertionError("right " + t);
                }
            }
        }
    }
}
```
