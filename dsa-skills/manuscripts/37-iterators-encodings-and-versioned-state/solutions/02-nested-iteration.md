<!-- solutions-for: 02-nested-iteration -->
### Solutions For Nested Iteration

#### Solution: [Build] Flatten 2D Vector (LeetCode 251)
<!-- id: it37-flatten-2d-vector -->

**Approach.**
The state is the pair `(row, col)`. The invariant is that, after `settle`, either `col` is a valid column of row `row`, or `row` equals the number of rows. The private method `settle` moves `row` forward while the current row has no unread element, and it resets `col` to 0 at each move. Because an empty row has `col == length` from the start, the same test passes empty and used-up rows. The method `hasNext` settles and compares `row` with the row count. The method `next` settles, throws when the end is reached, and otherwise returns the element and advances `col`. A second call to `hasNext` finds the position already settled and changes nothing.

The program compares the class with a flat list built by the oracle on random jagged arrays, and it calls `hasNext` repeatedly to check that those calls change nothing.

**Complexity.**
- **Time** is O(1) amortized per call, because each row boundary is passed once over the whole life of the iterator.
- **Space** is O(1) beyond the caller's rows, because the class stores the reference and two integers.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class Flatten2DVectorBuild {
    static final class Vector2D {
        private final int[][] vec;
        private int row, col;

        Vector2D(int[][] vec) { this.vec = vec; }

        /**
         * Moves the position past rows that hold no unread element.
         * Time: O(skipped rows). Space: O(1).
         * Invariant: afterwards row is the row count or col < vec[row].length.
         */
        private void settle() {
            // An empty row has col == length at once, so it is passed like a finished row.
            while (row < vec.length && col == vec[row].length) { row++; col = 0; }
        }

        /**
         * Tells whether an element remains.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: repeated calls leave the settled position unchanged.
         */
        boolean hasNext() {
            settle();
            // Past the last row means no element is left.
            return row < vec.length;
        }

        /**
         * Returns the next element.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: exhaustion throws before any write except the settle, which is logical state only.
         */
        int next() {
            settle();
            if (row == vec.length) throw new NoSuchElementException();
            // One read and one increment consume one element.
            return vec[row][col++];
        }
    }

    public static void main(String[] args) {
        // Example 1: the empty middle row is passed lazily.
        Vector2D a = new Vector2D(new int[][]{{1, 2}, {}, {3}});
        if (a.next() != 1 || a.next() != 2 || !a.hasNext() || a.next() != 3 || a.hasNext()) throw new AssertionError("example 1");
        // Example 2: repeated hasNext does not consume, and the end throws.
        Vector2D b = new Vector2D(new int[][]{{}, {5}, {}});
        if (!b.hasNext() || !b.hasNext() || b.next() != 5 || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // No rows at all is exhausted from the start.
        if (new Vector2D(new int[0][]).hasNext()) throw new AssertionError("no rows");
        // Random jagged arrays compare with the flat oracle.
        Random rnd = new Random(3711L);
        for (int t = 0; t < 3000; t++) {
            int rows = rnd.nextInt(6);
            int[][] vec = new int[rows][];
            List<Integer> flat = new ArrayList<>();
            for (int r = 0; r < rows; r++) {
                vec[r] = new int[rnd.nextInt(4)];
                for (int c = 0; c < vec[r].length; c++) { vec[r][c] = rnd.nextInt(50); flat.add(vec[r][c]); }
            }
            Vector2D it = new Vector2D(vec);
            for (int i = 0; i < flat.size(); i++) {
                // Two hasNext calls in a row must agree and must not skip an element.
                if (!it.hasNext() || !it.hasNext() || it.next() != flat.get(i)) throw new AssertionError("element " + i);
            }
            if (it.hasNext()) throw new AssertionError("extra element");
        }
    }
}
```

#### Solution: [Vary] Zigzag Iterator Over K Lists (LeetCode 281)
<!-- id: it37-zigzag-k-lists -->

**Approach.**
The new decision is the order of turns. The iterator keeps a queue of local cursors, and each cursor is a pair of a list index and the position of that list's next element. The constructor enqueues one cursor for each nonempty list, in list order. The method `next` removes the cursor at the front, reads its element, and enqueues the cursor again with the position plus one when the list has more elements. A finished list is not enqueued and takes no further turn. The queue order is therefore the order of the current round, followed by the lists that already took their turn in the next round.

The invariant is that the queue holds exactly the lists with an unread element, each once, in turn order. `hasNext` is `!queue.isEmpty()`. The program checks the class against an oracle that runs rounds explicitly over copies of the lists.

**Complexity.**
- **Time** is O(k) for the constructor with k lists, and O(1) per call afterward, because one dequeue and at most one enqueue run.
- **Space** is O(k) for the queue, independent of the total number of elements.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class ZigzagKListsVary {
    static final class ZigzagIterator {
        private final List<int[]> lists;
        private final ArrayDeque<int[]> queue = new ArrayDeque<>();   // entries are {list index, position}

        ZigzagIterator(List<int[]> lists) {
            this.lists = lists;
            // Only nonempty lists get a turn, in list order.
            for (int i = 0; i < lists.size(); i++) if (lists.get(i).length > 0) queue.add(new int[]{i, 0});
        }

        /**
         * Returns the next element in round-robin order.
         * Time: O(1). Space: O(1) beyond the queue.
         * Invariant: the queue holds exactly the lists with an unread element, in turn order.
         */
        int next() {
            // An empty queue means every list is finished.
            if (queue.isEmpty()) throw new NoSuchElementException();
            int[] cur = queue.poll();
            int[] list = lists.get(cur[0]);
            int value = list[cur[1]];
            // The list rejoins the back of the queue only if it still has an element.
            if (cur[1] + 1 < list.length) { cur[1]++; queue.add(cur); }
            return value;
        }

        /**
         * Tells whether any list has an unread element.
         * Time: O(1). Space: O(1).
         * Invariant: the answer is queue non-emptiness and consumes nothing.
         */
        boolean hasNext() { return !queue.isEmpty(); }
    }

    /** Oracle: runs explicit rounds over the lists. */
    static List<Integer> oracle(List<int[]> lists) {
        List<Integer> out = new ArrayList<>();
        for (int round = 0; ; round++) {
            boolean any = false;
            for (int[] l : lists) if (round < l.length) { out.add(l[round]); any = true; }
            if (!any) return out;
        }
    }

    public static void main(String[] args) {
        // Example 1: three lists of different lengths interleave in rounds.
        ZigzagIterator a = new ZigzagIterator(List.of(new int[]{1, 2, 3}, new int[]{4}, new int[]{5, 6}));
        int[] want = {1, 4, 5, 2, 6, 3};
        for (int w : want) if (!a.hasNext() || a.next() != w) throw new AssertionError("example 1");
        if (a.hasNext()) throw new AssertionError("example 1 end");
        // Example 2: empty lists never take a turn.
        ZigzagIterator b = new ZigzagIterator(List.of(new int[0], new int[]{7, 8}, new int[0]));
        if (b.next() != 7 || b.next() != 8 || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // No lists at all is exhausted.
        if (new ZigzagIterator(List.of()).hasNext()) throw new AssertionError("no lists");
        // Random lists compare with the round-by-round oracle.
        Random rnd = new Random(3712L);
        for (int t = 0; t < 3000; t++) {
            int k = rnd.nextInt(6);
            List<int[]> lists = new ArrayList<>();
            for (int i = 0; i < k; i++) {
                int[] l = new int[rnd.nextInt(5)];
                for (int j = 0; j < l.length; j++) l[j] = rnd.nextInt(100);
                lists.add(l);
            }
            List<Integer> expected = oracle(lists);
            ZigzagIterator it = new ZigzagIterator(lists);
            for (int v : expected) if (!it.hasNext() || it.next() != v) throw new AssertionError("order");
            if (it.hasNext()) throw new AssertionError("extra");
        }
    }
}
```

#### Solution: [Boundary] Flatten Nested List Iterator (LeetCode 341)
<!-- id: it37-nested-list-iterator -->

**Approach.**
The iterator keeps a stack of Java iterators, one for each list that is open, and one field `ready` that holds an integer already found but not yet returned. The method `hasNext` loops while `ready` is empty and the stack is not. It looks at the top iterator. An exhausted top is popped, because its list holds nothing more. Otherwise the loop takes the next item. A list item gets its iterator pushed, and an integer item goes into `ready`, which ends the loop. Empty lists therefore cost one push and one pop each, at any depth, and no case needs special handling.

The invariant has two parts. Every iterator on the stack belongs to a list that is open and unfinished. The field `ready` holds a value only between a `hasNext` call and the `next` call that consumes it. The method `next` calls `hasNext`, throws when it returns `false`, and otherwise clears `ready` and returns the value. The loop replaces recursion, so depth 10^5 uses heap memory and not call stack. The program runs a depth of 100000 as a direct check, and it compares random shallow structures with a recursive oracle.

**Complexity.**
- **Time** is O(1) amortized per integer plus O(1) for each list opened, so a full traversal costs O(N + L) for N integers and L lists.
- **Space** is O(d) for nesting depth d, because the stack holds one iterator for each open list.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class NestedListIteratorBoundary {
    interface NestedInteger {
        boolean isInteger();
        int getInteger();
        List<NestedInteger> getList();
    }

    static NestedInteger num(int v) {
        return new NestedInteger() {
            public boolean isInteger() { return true; }
            public int getInteger() { return v; }
            public List<NestedInteger> getList() { throw new IllegalStateException(); }
        };
    }

    static NestedInteger list(List<NestedInteger> items) {
        return new NestedInteger() {
            public boolean isInteger() { return false; }
            public int getInteger() { throw new IllegalStateException(); }
            public List<NestedInteger> getList() { return items; }
        };
    }

    static final class NestedIterator {
        private final ArrayDeque<Iterator<NestedInteger>> stack = new ArrayDeque<>();
        private Integer ready;

        NestedIterator(List<NestedInteger> nestedList) { stack.push(nestedList.iterator()); }

        /**
         * Finds the next integer, opening and closing lists as needed.
         * Time: O(1) amortized per integer plus O(1) per list. Space: O(d) for depth d.
         * Invariant: the stack holds only opened, unfinished lists, and ready is empty while the loop runs.
         */
        boolean hasNext() {
            // The loop ends when an integer is ready or no open list remains.
            while (ready == null && !stack.isEmpty()) {
                Iterator<NestedInteger> top = stack.peek();
                // A finished list leaves the stack, whatever its depth.
                if (!top.hasNext()) { stack.pop(); continue; }
                NestedInteger item = top.next();
                // An inner list opens one more level; an integer ends the search.
                if (item.isInteger()) ready = item.getInteger();
                else stack.push(item.getList().iterator());
            }
            return ready != null;
        }

        /**
         * Returns the next integer.
         * Time: O(1) amortized. Space: O(1) beyond the stack.
         * Invariant: ready is cleared, so each integer is returned once.
         */
        int next() {
            // The same search answers both calls, so hasNext can be repeated freely.
            if (!hasNext()) throw new NoSuchElementException();
            int v = ready;
            ready = null;
            return v;
        }
    }

    /** Recursive oracle, used only on shallow random structures. */
    static void flatten(List<NestedInteger> items, List<Integer> out) {
        for (NestedInteger n : items) {
            if (n.isInteger()) out.add(n.getInteger());
            else flatten(n.getList(), out);
        }
    }

    static List<NestedInteger> random(Random rnd, int depth) {
        List<NestedInteger> items = new ArrayList<>();
        for (int i = rnd.nextInt(4); i > 0; i--) {
            if (depth < 4 && rnd.nextInt(3) == 0) items.add(list(random(rnd, depth + 1)));
            else items.add(num(rnd.nextInt(100)));
        }
        return items;
    }

    public static void main(String[] args) {
        // Example 1: [[1,[2]],[],3] flattens to 1, 2, 3.
        NestedIterator a = new NestedIterator(List.of(list(List.of(num(1), list(List.of(num(2))))), list(List.of()), num(3)));
        if (a.next() != 1 || a.next() != 2 || a.next() != 3 || a.hasNext()) throw new AssertionError("example 1");
        // Example 2: [[[]],[4,[]],[]] holds only the integer 4.
        NestedIterator b = new NestedIterator(List.of(list(List.of(list(List.of()))), list(List.of(num(4), list(List.of()))), list(List.of())));
        if (!b.hasNext() || b.next() != 4 || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // A nesting depth of 100000 would overflow a recursive flattener; the stack on the heap handles it.
        NestedInteger deep = num(42);
        for (int i = 0; i < 100000; i++) deep = list(List.of(deep));
        NestedIterator d = new NestedIterator(List.of(deep));
        if (!d.hasNext() || d.next() != 42 || d.hasNext()) throw new AssertionError("deep nesting");
        // Random shallow structures compare with the recursive oracle.
        Random rnd = new Random(3713L);
        for (int t = 0; t < 3000; t++) {
            List<NestedInteger> in = random(rnd, 0);
            List<Integer> want = new ArrayList<>();
            flatten(in, want);
            NestedIterator it = new NestedIterator(in);
            for (int v : want) if (!it.hasNext() || !it.hasNext() || it.next() != v) throw new AssertionError("order");
            if (it.hasNext()) throw new AssertionError("extra");
        }
    }
}
```

#### Solution: [Recognize] Iterator For Combination (LeetCode 1286)
<!-- id: it37-combination-iterator -->

**Approach.**
The state is an array `idx` of `k` strictly increasing indexes into `characters`, plus a flag `more`. The first combination uses indexes `0` to `k - 1`. The method `next` builds the string from the current indexes and then computes the successor in place. The successor step searches from the right for the largest position `i` whose index is below its maximum, which is `n - k + i`. That index is increased by one, and every position to its right is reset to the smallest legal run, the previous index plus one. When no position can grow, the current combination was the last one, and `more` becomes false.

Lexicographic order holds because the rightmost index that can grow changes the smallest possible suffix of the combination. The class never creates the list of combinations, so memory is O(k). The test harness checks each answer against a reference that enumerates all subsets by bitmask and sorts them as strings.

**Complexity.**
- **Time** is O(k) per call, because building the string and computing the successor each scan at most `k` positions.
- **Space** is O(k) for the index array, independent of the binomial coefficient.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class CombinationIteratorRecognize {
    static final class CombinationIterator {
        private final String chars;
        private final int[] idx;
        private boolean more = true;

        CombinationIterator(String characters, int combinationLength) {
            this.chars = characters;
            this.idx = new int[combinationLength];
            // The first combination takes the first k letters.
            for (int i = 0; i < idx.length; i++) idx[i] = i;
        }

        /**
         * Returns the current combination and moves to its lexicographic successor.
         * Time: O(k). Space: O(k).
         * Invariant: idx is strictly increasing and idx[i] <= n - k + i whenever more is true.
         */
        String next() {
            // After the last combination more is false, and nothing changes.
            if (!more) throw new NoSuchElementException();
            StringBuilder sb = new StringBuilder();
            // The string is built from the stored indexes, one letter per position.
            for (int i : idx) sb.append(chars.charAt(i));
            int n = chars.length(), k = idx.length;
            int i = k - 1;
            // Find the rightmost position that can still grow.
            while (i >= 0 && idx[i] == n - k + i) i--;
            if (i < 0) more = false;
            else {
                idx[i]++;
                // Reset the suffix to the smallest increasing run after the grown index.
                for (int j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
            }
            return sb.toString();
        }

        /**
         * Tells whether a combination remains.
         * Time: O(1). Space: O(1).
         * Invariant: the flag changes only inside next.
         */
        boolean hasNext() { return more; }
    }

    /** Oracle: every subset of size k by bitmask, sorted as strings. */
    static List<String> oracle(String s, int k) {
        List<String> out = new ArrayList<>();
        int n = s.length();
        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sb.append(s.charAt(i));
            out.add(sb.toString());
        }
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: abc choose 2.
        CombinationIterator a = new CombinationIterator("abc", 2);
        if (!a.next().equals("ab") || !a.hasNext() || !a.next().equals("ac") || !a.next().equals("bc") || a.hasNext())
            throw new AssertionError("example 1");
        // Example 2: k equals n gives one combination, then exhaustion throws.
        CombinationIterator b = new CombinationIterator("xyz", 3);
        if (!b.hasNext() || !b.next().equals("xyz") || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // n = 15 and k = 7 gives 6435 combinations without storing them.
        CombinationIterator big = new CombinationIterator("abcdefghijklmno", 7);
        int count = 0;
        while (big.hasNext()) { big.next(); count++; }
        if (count != 6435) throw new AssertionError("count of 15 choose 7");
        // Random strings and lengths compare with the bitmask oracle.
        Random rnd = new Random(3714L);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(8);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + i * 2 + rnd.nextInt(2)));
            String s = sb.toString();
            int k = 1 + rnd.nextInt(n);
            CombinationIterator it = new CombinationIterator(s, k);
            for (String w : oracle(s, k)) if (!it.hasNext() || !it.next().equals(w)) throw new AssertionError("combination " + w);
            if (it.hasNext()) throw new AssertionError("extra");
        }
    }
}
```
