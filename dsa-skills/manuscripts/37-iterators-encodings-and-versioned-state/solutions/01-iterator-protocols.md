<!-- solutions-for: 01-iterator-protocols -->
### Solutions For Iterator Protocols

#### Solution: [Build] Array Iterator (Author exercise)
<!-- id: it37-array-iterator -->

**Approach.**
The class keeps the array reference and one integer `pos`, the index of the next element. The invariant is `0 <= pos <= length`. The methods `hasNext` and `remaining` only read `pos`, so repeated calls give the same answer. The method `next` tests `pos == length` first and throws before it writes anything, so a failed call leaves the state unchanged. Only after the test passes does it read the element and add 1 to `pos`.

The program compares the class with the iterator of an `ArrayList` on random call sequences, including calls after the end. It also checks that `remaining` equals the number of elements the model still holds.

**Complexity.**
- **Time** is O(1) per call, because each method performs one comparison and at most one increment.
- **Space** is O(1) beyond the caller's array, because the class stores a reference and one index.

```java run
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class ArrayIteratorBuild {
    static final class ArrayIterator {
        private final int[] data;
        private int pos;

        ArrayIterator(int[] data) {
            // The array is shared, not copied, so construction costs O(1).
            this.data = data;
        }

        /**
         * Tells whether an element remains.
         * Time: O(1). Space: O(1).
         * Invariant: the method only reads pos, so repeated calls agree.
         */
        boolean hasNext() {
            // pos stays within 0..length, so equality means exhausted.
            return pos < data.length;
        }

        /**
         * Returns the next element and moves the cursor once.
         * Time: O(1). Space: O(1).
         * Invariant: a failing call writes no field.
         */
        int next() {
            // The test runs before the write, so the exception leaves pos unchanged.
            if (pos == data.length) throw new NoSuchElementException();
            // One read and one increment consume exactly one element.
            return data[pos++];
        }

        /**
         * Counts the elements not yet returned.
         * Time: O(1). Space: O(1).
         * Invariant: the result equals length minus pos, never negative.
         */
        int remaining() {
            // Subtraction of the cursor from the length needs no loop.
            return data.length - pos;
        }
    }

    public static void main(String[] args) {
        // Example 1: two elements, then exhaustion throws.
        ArrayIterator a = new ArrayIterator(new int[]{4, 7});
        if (!a.hasNext() || a.next() != 4 || a.next() != 7 || a.hasNext()) throw new AssertionError("example 1");
        boolean threw = false;
        try { a.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || a.remaining() != 0) throw new AssertionError("exhausted next must throw and keep state");
        // Example 2: an empty array has nothing to return.
        ArrayIterator e = new ArrayIterator(new int[0]);
        if (e.hasNext() || e.remaining() != 0 || e.hasNext()) throw new AssertionError("example 2");
        // Random sequences compare every answer with the iterator of an ArrayList.
        Random rnd = new Random(3701L);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(7);
            int[] arr = new int[n];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) { arr[i] = rnd.nextInt(21) - 10; list.add(arr[i]); }
            ArrayIterator real = new ArrayIterator(arr);
            Iterator<Integer> model = list.iterator();
            int taken = 0;
            for (int step = rnd.nextInt(15); step > 0; step--) {
                int op = rnd.nextInt(3);
                if (op == 0 && real.hasNext() != model.hasNext()) throw new AssertionError("hasNext");
                if (op == 1) {
                    boolean modelHas = model.hasNext();
                    try {
                        int got = real.next();
                        if (!modelHas || got != model.next()) throw new AssertionError("next value");
                        taken++;
                    } catch (NoSuchElementException ex) {
                        if (modelHas) throw new AssertionError("unexpected exhaustion");
                    }
                }
                if (real.remaining() != n - taken) throw new AssertionError("remaining");
            }
        }
    }
}
```

#### Solution: [Vary] Peeking Iterator (LeetCode 284)
<!-- id: it37-peeking-iterator -->

**Approach.**
The wrapper holds the source iterator, one cached element `cache` and a flag `cached` that says whether the cache is full. The flag is necessary because every `Integer` value, including 0 and negative numbers, is a legal element, so no value can mean "empty". The private method `fill` pulls from the source only when the cache is empty and the source has an element. The method `peek` fills the cache and returns it without clearing the flag. The method `next` fills the cache, clears the flag and returns the element. The method `hasNext` fills the cache and reports the flag.

The invariant is that the cache holds the element that the source would return next, or the flag is false and the source itself holds it. The source's `next()` therefore runs once per element. The program wraps each source in a counting iterator and asserts that the source never runs more than one element ahead of the consumed count.

**Complexity.**
- **Time** is O(1) per call plus the cost of one call to the source, because `fill` calls the source at most once.
- **Space** is O(1), because the wrapper stores one element and one flag.

```java run
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class PeekingIteratorVary {
    /** Source that counts how many elements it has handed out. */
    static final class Counting implements Iterator<Integer> {
        private final Iterator<Integer> inner;
        int pulled;
        Counting(List<Integer> items) { inner = items.iterator(); }
        public boolean hasNext() { return inner.hasNext(); }
        public Integer next() { pulled++; return inner.next(); }
    }

    static final class PeekingIterator {
        private final Iterator<Integer> source;
        private Integer cache;
        private boolean cached;

        PeekingIterator(Iterator<Integer> source) { this.source = source; }

        /**
         * Moves one element from the source into the cache when the cache is empty.
         * Time: O(1) plus one source call. Space: O(1).
         * Invariant: the source's next() runs at most once for each element.
         */
        private void fill() {
            // A full cache needs no source call; an empty source leaves the flag false.
            if (!cached && source.hasNext()) {
                cache = source.next();
                cached = true;
            }
        }

        /**
         * Returns the next element without consuming it.
         * Time: O(1). Space: O(1).
         * Invariant: the flag and the cache do not change after the first fill.
         */
        int peek() {
            fill();
            // An empty cache after fill means the source is exhausted.
            if (!cached) throw new NoSuchElementException();
            return cache;
        }

        /**
         * Returns the next element and consumes it.
         * Time: O(1). Space: O(1).
         * Invariant: afterwards the cache is empty, so the next element comes from the source.
         */
        int next() {
            int v = peek();
            // Clearing the flag consumes the element exactly once.
            cached = false;
            return v;
        }

        /**
         * Tells whether an element remains.
         * Time: O(1). Space: O(1).
         * Invariant: the answer does not consume anything.
         */
        boolean hasNext() {
            fill();
            // The flag is true exactly when an element waits in the cache.
            return cached;
        }
    }

    public static void main(String[] args) {
        // Example 1: next and peek alternate and each element is handed out once.
        PeekingIterator p = new PeekingIterator(List.of(1, 2, 3).iterator());
        if (p.next() != 1 || p.peek() != 2 || p.next() != 2 || p.peek() != 3 || p.next() != 3 || p.hasNext())
            throw new AssertionError("example 1");
        // Example 2: repeated peek is stable, and 0 is an ordinary element.
        PeekingIterator q = new PeekingIterator(List.of(5, 0).iterator());
        if (q.peek() != 5 || q.peek() != 5 || q.next() != 5 || q.peek() != 0 || q.next() != 0)
            throw new AssertionError("example 2");
        boolean threw = false;
        try { q.peek(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("peek after the end must throw");
        // Random sequences compare with a list model and bound the source read-ahead to one element.
        Random rnd = new Random(3702L);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(6);
            List<Integer> items = new ArrayList<>();
            for (int i = 0; i < n; i++) items.add(rnd.nextInt(5) - 2);
            Counting src = new Counting(items);
            PeekingIterator real = new PeekingIterator(src);
            int taken = 0;
            for (int step = rnd.nextInt(14); step > 0; step--) {
                int op = rnd.nextInt(3);
                boolean has = taken < n;
                if (op == 0 && real.hasNext() != has) throw new AssertionError("hasNext");
                if (op == 1) {
                    try {
                        int got = real.peek();
                        if (!has || got != items.get(taken)) throw new AssertionError("peek");
                    } catch (NoSuchElementException ex) {
                        if (has) throw new AssertionError("peek threw early");
                    }
                }
                if (op == 2) {
                    try {
                        int got = real.next();
                        if (!has || got != items.get(taken)) throw new AssertionError("next");
                        taken++;
                    } catch (NoSuchElementException ex) {
                        if (has) throw new AssertionError("next threw early");
                    }
                }
                // The source is never more than one element ahead of the consumed count.
                if (src.pulled > taken + 1) throw new AssertionError("read ahead");
            }
        }
    }
}
```

#### Solution: [Boundary] Compressed String Iterator (LeetCode 604)
<!-- id: it37-compressed-string-iterator -->

**Approach.**
The constructor parses the string once into two parallel arrays, `letters` and `counts`. A group starts at a letter, and the digits that follow form its count as a `long` built by `count * 10 + digit`. Fifteen digits stay below 10^15, which fits in `long` and does not fit in `int`. The expanded text never exists, so memory depends on the length of the compressed string.

The iterator keeps the pair `group` and `used`. The private method `settle` advances `group` while the current group is used up, and a group of count 0 is used up from the start. Both `hasNext` and `next` call `settle` first, so the move across empty groups happens inside the call that needs a letter. The method `next` throws before any write when `settle` reaches the end.

**Complexity.**
- **Time** is O(L) for the constructor with L the length of the string, and O(1) amortized per call, because each group boundary is passed once.
- **Space** is O(L) for the parsed groups, independent of the counts.

```java run
import java.util.NoSuchElementException;
import java.util.Random;

public final class CompressedStringIteratorBoundary {
    static final class StringIterator {
        private final char[] letters;
        private final long[] counts;
        private int group;
        private long used;

        StringIterator(String s) {
            int groups = 0;
            // One pass counts the letters, which start the groups.
            for (int i = 0; i < s.length(); i++) if (Character.isLetter(s.charAt(i))) groups++;
            letters = new char[groups];
            counts = new long[groups];
            int g = -1;
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                // A letter opens a new group with count 0.
                if (Character.isLetter(c)) { g++; letters[g] = c; }
                // A digit extends the count of the current group; long avoids int overflow.
                else counts[g] = counts[g] * 10 + (c - '0');
            }
        }

        /**
         * Skips groups that hold no unread letter.
         * Time: O(skipped groups). Space: O(1).
         * Invariant: afterwards group is the end or used < counts[group].
         */
        private void settle() {
            // A used-up group and a group of count 0 both satisfy used == counts[group].
            while (group < letters.length && used == counts[group]) { group++; used = 0; }
        }

        /**
         * Tells whether a letter remains.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: settling does not change the logical position.
         */
        boolean hasNext() {
            settle();
            return group < letters.length;
        }

        /**
         * Returns the next letter.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: exhaustion throws before any write.
         */
        char next() {
            settle();
            // Past the last group nothing remains, and the call writes nothing.
            if (group == letters.length) throw new NoSuchElementException();
            // One letter is taken from the current group.
            used++;
            return letters[group];
        }
    }

    /** Oracle that expands the string, which is safe for the small counts used in tests. */
    static String expand(String s) {
        StringBuilder out = new StringBuilder();
        int i = 0;
        while (i < s.length()) {
            char c = s.charAt(i++);
            int n = 0;
            while (i < s.length() && Character.isDigit(s.charAt(i))) n = n * 10 + (s.charAt(i++) - '0');
            for (int k = 0; k < n; k++) out.append(c);
        }
        return out.toString();
    }

    public static void main(String[] args) {
        // Example 1: the count 13 has two digits, and the zero group is skipped.
        StringIterator a = new StringIterator("a2b0c13");
        if (a.next() != 'a' || a.next() != 'a' || a.next() != 'c' || !a.hasNext()) throw new AssertionError("example 1");
        // Example 2: a leading zero group is skipped and the end throws.
        StringIterator b = new StringIterator("p0q1");
        if (!b.hasNext() || b.next() != 'q' || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // A count with 15 digits does not fit in int and does not allocate anything.
        StringIterator big = new StringIterator("z999999999999999");
        if (big.next() != 'z' || !big.hasNext()) throw new AssertionError("long count");
        // Random strings compare with the expanded oracle, including zero and multi-digit counts.
        Random rnd = new Random(3703L);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int groups = 1 + rnd.nextInt(4);
            for (int g = 0; g < groups; g++) {
                sb.append((char) ('a' + rnd.nextInt(3)));
                sb.append(rnd.nextInt(4) == 0 ? rnd.nextInt(3) : rnd.nextInt(13));
            }
            String s = sb.toString();
            String want = expand(s);
            StringIterator it = new StringIterator(s);
            for (int i = 0; i < want.length(); i++) {
                if (!it.hasNext() || it.next() != want.charAt(i)) throw new AssertionError("letter " + i + " of " + s);
            }
            if (it.hasNext()) throw new AssertionError("extra letters " + s);
        }
    }
}
```

#### Solution: [Recognize] RLE Iterator (LeetCode 900)
<!-- id: it37-rle-iterator -->

**Approach.**
The iterator keeps the encoding array and the index `run` of the run that holds the next element. It also keeps `used`, a `long` that counts the elements already taken from that run. A call `exhaust(n)` turns `n` into a `long` called `need` and loops over runs. In each round it compares `need` with `left = counts[run] - used`. When `left >= need`, the target element lies in this run, so the call adds `need` to `used` and returns that run's value. Otherwise the call subtracts `left` from `need`, moves to the next run and resets `used`. When the loop runs past the last run, fewer than `n` elements remained, so the cursor is at the end and the call returns -1.

The invariant is that `used` never exceeds the count of run `run`, and that every element before the cursor is consumed. The call never builds a sum of counts, because the sum can reach 5 * 10^11, so the loop works with differences instead. The program checks the class against a list that expands the encoding for small counts.

**Complexity.**
- **Time** is O(R) per call in the worst case with R runs. Across all calls it is O(R + C) for C calls, because the cursor never moves backward and each run boundary is crossed once.
- **Space** is O(1) beyond the stored encoding, independent of the counts.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RleIteratorRecognize {
    static final class RLEIterator {
        private final int[] enc;
        private int run;      // index of the count in enc, always even
        private long used;    // elements already taken from the run at index run

        RLEIterator(int[] encoding) { this.enc = encoding; }

        /**
         * Consumes n logical elements and returns the last one, or -1 when fewer remain.
         * Time: O(R) for R runs passed. Space: O(1).
         * Invariant: used <= enc[run] and the cursor never moves backward.
         */
        int exhaust(int n) {
            // long need keeps the subtraction safe, since the counts can be as large as an int.
            long need = n;
            // Each round either finishes inside the current run or passes the whole run.
            while (run < enc.length) {
                long left = (long) enc[run] - used;
                // The target element lies in this run, so only the used count changes.
                if (left >= need) {
                    used += need;
                    return enc[run + 1];
                }
                // The whole rest of the run is consumed, and the loop moves to the next run.
                need -= left;
                run += 2;
                used = 0;
            }
            // The cursor passed the last run, so fewer than n elements remained.
            return -1;
        }
    }

    /** Oracle that expands the encoding into a list and walks it. */
    static final class Oracle {
        private final List<Integer> items = new ArrayList<>();
        private int pos;
        Oracle(int[] enc) {
            for (int i = 0; i < enc.length; i += 2) for (int k = 0; k < enc[i]; k++) items.add(enc[i + 1]);
        }
        int exhaust(int n) {
            // Fewer than n elements: consume them all and answer -1.
            if (pos + n > items.size()) { pos = items.size(); return -1; }
            pos += n;
            return items.get(pos - 1);
        }
    }

    public static void main(String[] args) {
        // Example 1: the zero-count run is passed, and the last call finds one element for a request of two.
        RLEIterator a = new RLEIterator(new int[]{3, 8, 0, 9, 2, 5});
        if (a.exhaust(2) != 8 || a.exhaust(1) != 8 || a.exhaust(1) != 5 || a.exhaust(2) != -1) throw new AssertionError("example 1");
        // Example 2: the final request finds nothing left.
        RLEIterator b = new RLEIterator(new int[]{1, 4, 2, 6});
        if (b.exhaust(1) != 4 || b.exhaust(2) != 6 || b.exhaust(1) != -1) throw new AssertionError("example 2");
        // Counts near the int limit are handled without expansion or int overflow.
        RLEIterator big = new RLEIterator(new int[]{1000000000, 7, 1000000000, 9});
        if (big.exhaust(1000000000) != 7 || big.exhaust(1000000000) != 9 || big.exhaust(1) != -1) throw new AssertionError("large counts");
        // Random encodings compare with the expanded oracle.
        Random rnd = new Random(3704L);
        for (int t = 0; t < 4000; t++) {
            int runs = 1 + rnd.nextInt(4);
            int[] enc = new int[runs * 2];
            for (int i = 0; i < runs; i++) { enc[2 * i] = rnd.nextInt(5); enc[2 * i + 1] = rnd.nextInt(6); }
            RLEIterator real = new RLEIterator(enc);
            Oracle model = new Oracle(enc);
            for (int step = 1 + rnd.nextInt(7); step > 0; step--) {
                int n = 1 + rnd.nextInt(6);
                if (real.exhaust(n) != model.exhaust(n)) throw new AssertionError("exhaust " + n);
            }
        }
    }
}
```
