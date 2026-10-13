<!-- solutions-for: 91-iterator-traversal-state -->
### Solutions For Iterator Traversal State

#### Solution: [Build] Peeking Iterator With Lookahead Offset (LeetCode 284)
<!-- id: it37-lookahead-peeking -->

**Approach.**
The class keeps a queue `buf` of elements already pulled from the source and not yet consumed. The private method `fill(m)` pulls from the source until the buffer holds `m` elements or the source ends. The method `peek(offset)` rejects a negative offset, fills the buffer to `offset + 1` elements, and throws `NoSuchElementException` when the buffer is still shorter. Otherwise it walks `offset` steps from the front of the buffer and returns that element. The pulled elements stay in the buffer when the peek fails, so the sequence is intact for later calls. The method `next` fills the buffer to one element and removes the front. The method `hasNext` fills to one element and tests that the buffer is nonempty.

The invariant is that the buffer holds a prefix of the unread sequence in order, and the source holds the rest. The source is therefore pulled once for each element, and never more than the largest window a caller has asked for. The program counts pulls and checks the bound `pulled <= min(n, consumed + largestWindow)`, where the window is `offset + 1` for a peek and 1 for the other calls.

**Complexity.**
- **Time** is O(offset) for a peek, because the walk to the offset visits that many buffer entries, and O(1) amortized for `next` and `hasNext`.
- **Space** is O(w) for the largest window `w` requested so far, and no more.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class LookaheadIteratorBuild {
    /** Source that counts pulls. */
    static final class Counting implements Iterator<Integer> {
        private final Iterator<Integer> inner;
        int pulled;
        Counting(List<Integer> items) { inner = items.iterator(); }
        public boolean hasNext() { return inner.hasNext(); }
        public Integer next() { pulled++; return inner.next(); }
    }

    static final class LookaheadIterator {
        private final Iterator<Integer> source;
        private final ArrayDeque<Integer> buf = new ArrayDeque<>();

        LookaheadIterator(Iterator<Integer> source) { this.source = source; }

        /**
         * Pulls from the source until the buffer holds m elements or the source ends.
         * Time: O(pulled elements). Space: O(m).
         * Invariant: buf is a prefix of the unread sequence, in order.
         */
        private void fill(int m) {
            // Each element moves from the source to the buffer once, never twice.
            while (buf.size() < m && source.hasNext()) buf.add(source.next());
        }

        /**
         * Returns the element offset positions after the next one without consuming anything.
         * Time: O(offset). Space: O(offset) buffer.
         * Invariant: a failing call leaves every pulled element in the buffer.
         */
        int peek(int offset) {
            // A negative offset is a caller error and reads nothing.
            if (offset < 0) throw new IllegalArgumentException();
            fill(offset + 1);
            // The source ended before the requested position.
            if (buf.size() <= offset) throw new NoSuchElementException();
            Iterator<Integer> it = buf.iterator();
            // Walk offset entries from the front to reach the requested element.
            for (int i = 0; i < offset; i++) it.next();
            return it.next();
        }

        /**
         * Consumes and returns the next element.
         * Time: O(1) amortized. Space: O(1) beyond the buffer.
         * Invariant: exactly one element leaves the buffer.
         */
        int next() {
            fill(1);
            if (buf.isEmpty()) throw new NoSuchElementException();
            return buf.poll();
        }

        /**
         * Tells whether an element remains.
         * Time: O(1). Space: O(1).
         * Invariant: the call consumes nothing.
         */
        boolean hasNext() {
            fill(1);
            return !buf.isEmpty();
        }
    }

    static String outcome(java.util.function.IntSupplier call) {
        try { return Integer.toString(call.getAsInt()); }
        catch (NoSuchElementException e) { return "NSE"; }
        catch (IllegalArgumentException e) { return "IAE"; }
    }

    public static void main(String[] args) {
        // Example 1: peek(2) reads 30, and a peek past the end fails but loses nothing.
        LookaheadIterator a = new LookaheadIterator(List.of(10, 20, 30, 40).iterator());
        if (a.peek(2) != 30 || a.peek(0) != 10 || a.next() != 10 || a.peek(2) != 40) throw new AssertionError("example 1 reads");
        boolean threw = false;
        try { a.peek(3); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || !a.hasNext() || a.next() != 20 || a.next() != 30 || a.next() != 40 || a.hasNext())
            throw new AssertionError("example 1 intact after failed peek");
        // Example 2: an empty source and a negative offset.
        LookaheadIterator e = new LookaheadIterator(List.<Integer>of().iterator());
        boolean nse = false, iae = false;
        if (e.hasNext()) throw new AssertionError("empty hasNext");
        try { e.peek(0); } catch (NoSuchElementException x) { nse = true; }
        try { e.peek(-1); } catch (IllegalArgumentException x) { iae = true; }
        if (!nse || !iae) throw new AssertionError("example 2");
        // A new iterator pulls nothing until a call needs an element.
        Counting idle = new Counting(List.of(1, 2, 3));
        new LookaheadIterator(idle);
        if (idle.pulled != 0) throw new AssertionError("constructor must not pull");
        // Random call sequences compare with a list model and bound the pulls by the largest window.
        Random rnd = new Random(3791L);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(7);
            List<Integer> items = new ArrayList<>();
            for (int i = 0; i < n; i++) items.add(rnd.nextInt(9) - 4);
            Counting src = new Counting(items);
            LookaheadIterator real = new LookaheadIterator(src);
            int taken = 0, window = 0;
            for (int step = rnd.nextInt(14); step > 0; step--) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    int off = rnd.nextInt(8) - 1;
                    window = Math.max(window, Math.max(off + 1, 1));
                    String want = off < 0 ? "IAE" : taken + off < n ? Integer.toString(items.get(taken + off)) : "NSE";
                    if (!outcome(() -> real.peek(off)).equals(want)) throw new AssertionError("peek " + off);
                } else if (op == 1) {
                    window = Math.max(window, 1);
                    if (real.hasNext() != (taken < n)) throw new AssertionError("hasNext");
                } else {
                    window = Math.max(window, 1);
                    String want = taken < n ? Integer.toString(items.get(taken)) : "NSE";
                    if (!outcome(real::next).equals(want)) throw new AssertionError("next");
                    if (taken < n) taken++;
                }
                if (src.pulled > Math.min(n, taken + window)) throw new AssertionError("pulled too far");
            }
        }
    }
}
```

#### Solution: [Vary] Run Skipper (LeetCode 900)
<!-- id: it37-run-skipper -->

**Approach.**
The class keeps the arrays, the index `run` of the current run, and the `long` value `used`, the number of elements already taken from that run. The private method `settle` moves past runs whose elements are all used, which includes runs of count 0. The method `skip(n)` keeps a `long` called `left` that starts at `n`. Each round settles, stops if the runs are exhausted, takes `take = min(counts[run] - used, left)`, adds `take` to `used` and subtracts it from `left`. The method returns `n - left`. A round never adds two counts, so the sum of all counts, which can exceed `Long.MAX_VALUE`, is never computed. The methods `peek` and `next` settle first and throw `NoSuchElementException` at the end, and `next` adds 1 to `used`.

The invariant is that `used <= counts[run]` whenever `run` is a valid index, and that every element before the cursor is consumed. The test harness checks the class against a reference that expands small counts, and a direct test covers counts of 10^18.

**Complexity.**
- **Time** is O(R) per call in the worst case for R runs, and O(R + C) over C calls in total, because the cursor never moves backward.
- **Space** is O(1) beyond the stored arrays, independent of the counts.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class RunSkipperVary {
    static final class RunSkipper {
        private final long[] counts;
        private final int[] values;
        private int run;
        private long used;

        RunSkipper(long[] counts, int[] values) { this.counts = counts; this.values = values; }

        /**
         * Moves the cursor past runs with no unread element.
         * Time: O(skipped runs). Space: O(1).
         * Invariant: afterwards run is the run count or used < counts[run].
         */
        private void settle() {
            // A run of count 0 and a used-up run both satisfy used == counts[run].
            while (run < counts.length && used == counts[run]) { run++; used = 0; }
        }

        /**
         * Consumes up to n elements and returns how many it consumed.
         * Time: O(R) for R runs passed. Space: O(1).
         * Invariant: only differences are computed, so no sum of counts can overflow.
         */
        long skip(long n) {
            long left = n;
            // Each round takes from one run, so the loop ends when n is used or the runs end.
            while (left > 0) {
                settle();
                if (run == counts.length) break;
                long take = Math.min(counts[run] - used, left);
                used += take;
                left -= take;
            }
            return n - left;
        }

        /**
         * Returns the next element without consuming it.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: settling changes only the cursor representation, not the position.
         */
        int peek() {
            settle();
            if (run == counts.length) throw new NoSuchElementException();
            return values[run];
        }

        /**
         * Consumes and returns the next element.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: exhaustion throws before any write.
         */
        int next() {
            int v = peek();
            // One element leaves the current run.
            used++;
            return v;
        }

        /**
         * Tells whether an element remains.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: the call consumes nothing.
         */
        boolean hasNext() {
            settle();
            return run < counts.length;
        }
    }

    static final class Oracle {
        private final List<Integer> items = new ArrayList<>();
        private int pos;
        Oracle(long[] counts, int[] values) {
            for (int i = 0; i < counts.length; i++) for (long k = 0; k < counts[i]; k++) items.add(values[i]);
        }
        long skip(long n) { long m = Math.min(n, items.size() - pos); pos += (int) m; return m; }
        boolean hasNext() { return pos < items.size(); }
        int peek() { if (pos == items.size()) throw new NoSuchElementException(); return items.get(pos); }
        int next() { int v = peek(); pos++; return v; }
    }

    public static void main(String[] args) {
        // Example 1: a count of 10^18 is skipped into without expansion.
        RunSkipper a = new RunSkipper(new long[]{4, 2, 1000000000000000000L}, new int[]{1, 2, 3});
        if (a.skip(5) != 5 || a.peek() != 2 || a.next() != 2 || a.skip(7) != 7 || a.peek() != 3 || !a.hasNext())
            throw new AssertionError("example 1");
        // Example 2: a skip past the end consumes only what remains.
        RunSkipper b = new RunSkipper(new long[]{2, 1}, new int[]{6, 7});
        if (b.skip(5) != 3 || b.hasNext() || b.skip(1) != 0) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.peek(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted peek must throw");
        // The counts sum to more than Long.MAX_VALUE, yet a huge skip stays correct.
        long big = 1000000000000000000L;
        RunSkipper c = new RunSkipper(new long[]{big, big, big, big, big, big, big, big, big, big}, new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9});
        if (c.skip(big) != big || c.peek() != 1) throw new AssertionError("run boundary at 10^18");
        // Random runs compare with the expanded oracle, including zero counts and over-long skips.
        Random rnd = new Random(3792L);
        for (int t = 0; t < 4000; t++) {
            int runs = rnd.nextInt(5);
            long[] counts = new long[runs];
            int[] values = new int[runs];
            for (int i = 0; i < runs; i++) { counts[i] = rnd.nextInt(5); values[i] = rnd.nextInt(7); }
            RunSkipper real = new RunSkipper(counts, values);
            Oracle model = new Oracle(counts, values);
            for (int step = rnd.nextInt(9); step > 0; step--) {
                int op = rnd.nextInt(4);
                if (op == 0) { long n = rnd.nextInt(7); if (real.skip(n) != model.skip(n)) throw new AssertionError("skip"); }
                if (op == 1 && real.hasNext() != model.hasNext()) throw new AssertionError("hasNext");
                if (op == 2 || op == 3) {
                    boolean has = model.hasNext();
                    try {
                        int got = op == 2 ? real.peek() : real.next();
                        int want = op == 2 ? model.peek() : model.next();
                        if (!has || got != want) throw new AssertionError("value");
                    } catch (NoSuchElementException ex) {
                        if (has) throw new AssertionError("early exhaustion");
                    }
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Depth-Weighted Nested Iterator (LeetCode 341)
<!-- id: it37-depth-weighted-nested -->

**Approach.**
The iterator keeps a stack of Java iterators, one for each open list, as in the plain nested iterator. The new rule is that the size of the stack at the moment an integer is found equals that integer's depth. The stack holds the top-level list and every list opened beneath it, and the integer belongs to the list on top. The iterator therefore computes `value * depth` as a `long` at discovery time and stores it in `ready`, together with the flag `hasReady`. A flag is necessary because every `long` value, including 0, can be a result.

The method `hasNext` loops while no result is ready and the stack is not empty. It pops finished iterators, pushes an iterator for each inner list, and stops at the first integer. Empty lists at any depth push and pop without producing anything. The invariant is that the stack holds only open, unfinished lists, and that `ready` is set only between `hasNext` and the `next` that consumes it. The program checks a depth of 100000 with a value of 10^9, whose product 10^14 does not fit in `int`, and it compares random shallow structures with a recursive oracle.

**Complexity.**
- **Time** is O(1) amortized per integer plus O(1) per list, so a full traversal costs O(N + L) for N integers and L lists.
- **Space** is O(d) for nesting depth d, because the stack holds one iterator for each open list.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class DepthWeightedNestedBoundary {
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

    static final class DepthWeightedIterator {
        private final ArrayDeque<Iterator<NestedInteger>> open = new ArrayDeque<>();
        private long ready;
        private boolean hasReady;

        DepthWeightedIterator(List<NestedInteger> top) { open.push(top.iterator()); }

        /**
         * Finds the next integer and stores its weighted value.
         * Time: O(1) amortized per integer plus O(1) per list. Space: O(d).
         * Invariant: open holds only unfinished lists, and open.size() is the depth of the top list.
         */
        boolean hasNext() {
            // The loop ends with a stored result or with no open list.
            while (!hasReady && !open.isEmpty()) {
                Iterator<NestedInteger> top = open.peek();
                // A finished list leaves the stack.
                if (!top.hasNext()) { open.pop(); continue; }
                NestedInteger item = top.next();
                if (item.isInteger()) {
                    // The stack size is the depth, and long arithmetic avoids int overflow.
                    ready = (long) item.getInteger() * open.size();
                    hasReady = true;
                } else {
                    // An inner list opens one level deeper.
                    open.push(item.getList().iterator());
                }
            }
            return hasReady;
        }

        /**
         * Returns the next weighted integer.
         * Time: O(1) amortized. Space: O(1) beyond the stack.
         * Invariant: the flag is cleared, so each integer comes back once.
         */
        long next() {
            if (!hasNext()) throw new NoSuchElementException();
            hasReady = false;
            return ready;
        }
    }

    static void weigh(List<NestedInteger> items, int depth, List<Long> out) {
        for (NestedInteger n : items) {
            if (n.isInteger()) out.add((long) n.getInteger() * depth);
            else weigh(n.getList(), depth + 1, out);
        }
    }

    static List<NestedInteger> random(Random rnd, int depth) {
        List<NestedInteger> items = new ArrayList<>();
        for (int i = rnd.nextInt(4); i > 0; i--) {
            if (depth < 4 && rnd.nextInt(3) == 0) items.add(list(random(rnd, depth + 1)));
            else items.add(num(rnd.nextInt(41) - 20));
        }
        return items;
    }

    public static void main(String[] args) {
        // Example 1: [[1,[2]],[],3] gives 1*2, 2*3 and 3*1.
        DepthWeightedIterator a = new DepthWeightedIterator(List.of(list(List.of(num(1), list(List.of(num(2))))), list(List.of()), num(3)));
        if (a.next() != 2 || a.next() != 6 || a.next() != 3 || a.hasNext()) throw new AssertionError("example 1");
        // Example 2: [[],[[-4]]] gives -4 at depth 3.
        DepthWeightedIterator b = new DepthWeightedIterator(List.of(list(List.of()), list(List.of(list(List.of(num(-4)))))));
        if (b.next() != -12 || b.hasNext()) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        // Depth 100000 and value 10^9 give 10^14, which needs long, and the stack handles the depth.
        NestedInteger deep = num(1000000000);
        for (int i = 0; i < 99999; i++) deep = list(List.of(deep));
        DepthWeightedIterator d = new DepthWeightedIterator(List.of(deep));
        if (d.next() != 1000000000L * 100000L || d.hasNext()) throw new AssertionError("deep product");
        // Random shallow structures compare with the recursive oracle.
        Random rnd = new Random(3793L);
        for (int t = 0; t < 3000; t++) {
            List<NestedInteger> in = random(rnd, 0);
            List<Long> want = new ArrayList<>();
            weigh(in, 1, want);
            DepthWeightedIterator it = new DepthWeightedIterator(in);
            for (long v : want) if (!it.hasNext() || !it.hasNext() || it.next() != v) throw new AssertionError("order");
            if (it.hasNext()) throw new AssertionError("extra");
        }
    }
}
```

#### Solution: [Recognize] Range-Bounded BST Iterator (LeetCode 1586)
<!-- id: it37-bst-iterator-range -->

**Approach.**
The iterator keeps the three stores from the lesson: a pending stack of nodes, a visited list of keys, and the history position `pos`. The pending stack is ascending from the top. The range changes only how nodes enter the stack. The private method `spine(node)` walks down from `node`. A node with a key at least `lo` is pushed, and the walk continues to its left child. A node with a key below `lo` is skipped, together with its whole left subtree, and the walk continues to its right child. After a pop, the new nodes come from `spine(popped.right)`. Every key there exceeds the popped key, and the same `lo` test filters them.

The upper bound uses the ascending order of the stack. When the top has a key above `hi`, every other entry is larger, so the pending stack holds no key in range. The method `hasNext` therefore tests a visited key after `pos`, or a nonempty stack whose top is at most `hi`. The method `next` replays when a visited key lies after `pos`, and otherwise pops the top, pushes the spine of its right child, appends the key and moves `pos`. The method `prev` moves only `pos`. The invariant is that `visited` is a prefix of the in-range keys and `pending` yields the following in-range keys in order. No recursion occurs, so a height of 10^5 is safe. The program compares the class with a filtered sorted list on random trees and random call sequences, and it runs a chain of 10^5 nodes.

**Complexity.**
- **Time** is O(h) for the constructor with tree height h, and O(1) amortized per `next` and O(1) per `prev`, because each node enters and leaves the stack once.
- **Space** is O(h + k) for the stack and the k keys reached so far.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class RangeBstIteratorRecognize {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static final class RangeBstIterator {
        private final int lo, hi;
        private final ArrayDeque<Node> pending = new ArrayDeque<>();
        private final List<Integer> visited = new ArrayList<>();
        private int pos = -1;

        RangeBstIterator(Node root, int lo, int hi) {
            this.lo = lo;
            this.hi = hi;
            spine(root);
        }

        /**
         * Pushes the nodes with keys at least lo along the leftmost path from n.
         * Time: O(height of the path). Space: O(1) beyond the stack.
         * Invariant: the stack stays ascending from the top.
         */
        private void spine(Node n) {
            // Walk down; a node below lo and its left subtree hold no key in range, so go right.
            while (n != null) {
                if (n.val >= lo) { pending.push(n); n = n.left; }
                else n = n.right;
            }
        }

        /**
         * Tells whether a key lies to the right of the current position.
         * Time: O(1). Space: O(1).
         * Invariant: an ascending stack with a top above hi holds no key in range.
         */
        boolean hasNext() {
            // A visited key after pos is replayed; otherwise the stack top must be in range.
            return pos + 1 < visited.size() || (!pending.isEmpty() && pending.peek().val <= hi);
        }

        /**
         * Tells whether a key lies to the left of the current key.
         * Time: O(1). Space: O(1).
         * Invariant: pos is -1 before the first key, so hasPrev is false there.
         */
        boolean hasPrev() { return pos > 0; }

        /**
         * Moves one key right and returns it.
         * Time: O(1) amortized. Space: O(1) beyond the stack and list.
         * Invariant: a failing call changes no field.
         */
        int next() {
            if (!hasNext()) throw new NoSuchElementException();
            // At the end of the history the call extends it from the stack.
            if (pos + 1 == visited.size()) {
                Node n = pending.pop();
                spine(n.right);
                visited.add(n.val);
            }
            return visited.get(++pos);
        }

        /**
         * Moves one key left and returns it.
         * Time: O(1). Space: O(1).
         * Invariant: only pos changes, and visited never shrinks.
         */
        int prev() {
            if (!hasPrev()) throw new NoSuchElementException();
            return visited.get(--pos);
        }
    }

    static Node build(Integer[] level) {
        if (level.length == 0 || level[0] == null) return null;
        Node root = new Node(level[0]);
        ArrayDeque<Node> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < level.length) {
            Node n = q.poll();
            if (i < level.length && level[i] != null) { n.left = new Node(level[i]); q.add(n.left); }
            i++;
            if (i < level.length && level[i] != null) { n.right = new Node(level[i]); q.add(n.right); }
            i++;
        }
        return root;
    }

    static Node insert(Node root, int key) {
        if (root == null) return new Node(key);
        Node cur = root;
        while (true) {
            if (key < cur.val) { if (cur.left == null) { cur.left = new Node(key); break; } cur = cur.left; }
            else { if (cur.right == null) { cur.right = new Node(key); break; } cur = cur.right; }
        }
        return root;
    }

    /** Oracle: sorted in-range keys with the same position rules. */
    static final class Oracle {
        private final List<Integer> keys = new ArrayList<>();
        private int pos = -1;
        Oracle(List<Integer> all, int lo, int hi) {
            for (int k : all) if (k >= lo && k <= hi) keys.add(k);
            Collections.sort(keys);
        }
        boolean hasNext() { return pos + 1 < keys.size(); }
        boolean hasPrev() { return pos > 0; }
        int next() { if (!hasNext()) throw new NoSuchElementException(); return keys.get(++pos); }
        int prev() { if (!hasPrev()) throw new NoSuchElementException(); return keys.get(--pos); }
    }

    public static void main(String[] args) {
        // Example 1: keys 7, 9, 15 lie in [5, 16], and 3 and 20 are outside.
        RangeBstIterator a = new RangeBstIterator(build(new Integer[]{7, 3, 15, null, null, 9, 20}), 5, 16);
        if (a.next() != 7 || a.next() != 9 || a.prev() != 7 || a.hasPrev() || !a.hasNext()
                || a.next() != 9 || a.next() != 15 || a.hasNext()) throw new AssertionError("example 1");
        // Example 2: no key of [2,1,3] lies in [4, 9].
        RangeBstIterator b = new RangeBstIterator(build(new Integer[]{2, 1, 3}), 4, 9);
        boolean threw = false;
        if (b.hasNext() || b.hasPrev()) throw new AssertionError("example 2 flags");
        try { b.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("example 2 next must throw");
        // prev before the first key throws and keeps the position.
        RangeBstIterator c = new RangeBstIterator(build(new Integer[]{2, 1, 3}), 0, 9);
        threw = false;
        try { c.prev(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || c.next() != 1) throw new AssertionError("prev at start");
        // An empty tree has no keys.
        if (new RangeBstIterator(null, 0, 5).hasNext()) throw new AssertionError("empty tree");
        // Chains of 100000 nodes in both directions need no recursion.
        Node left = null, right = null;
        for (int k = 1; k <= 100000; k++) { Node n = new Node(k); n.left = left; left = n; }
        for (int k = 100000; k >= 1; k--) { Node n = new Node(k); n.right = right; right = n; }
        for (Node root : new Node[]{left, right}) {
            RangeBstIterator it = new RangeBstIterator(root, 1, 100000);
            for (int k = 1; k <= 100000; k++) if (it.next() != k) throw new AssertionError("chain order");
            if (it.hasNext() || it.prev() != 99999) throw new AssertionError("chain end");
        }
        // Random trees, ranges and call sequences compare with the filtered sorted list.
        Random rnd = new Random(3794L);
        for (int t = 0; t < 3000; t++) {
            List<Integer> keys = new ArrayList<>();
            Node root = null;
            for (int i = rnd.nextInt(9); i > 0; i--) {
                int k = rnd.nextInt(20);
                if (keys.contains(k)) continue;
                keys.add(k);
                root = insert(root, k);
            }
            int lo = rnd.nextInt(20), hi = lo + rnd.nextInt(20 - lo);
            RangeBstIterator real = new RangeBstIterator(root, lo, hi);
            Oracle model = new Oracle(keys, lo, hi);
            for (int step = rnd.nextInt(16); step > 0; step--) {
                int op = rnd.nextInt(4);
                if (op == 0 && real.hasNext() != model.hasNext()) throw new AssertionError("hasNext");
                if (op == 1 && real.hasPrev() != model.hasPrev()) throw new AssertionError("hasPrev");
                if (op == 2) {
                    boolean has = model.hasNext();
                    try { int got = real.next(); if (!has || got != model.next()) throw new AssertionError("next"); }
                    catch (NoSuchElementException ex) { if (has) throw new AssertionError("next threw early"); }
                }
                if (op == 3) {
                    boolean has = model.hasPrev();
                    try { int got = real.prev(); if (!has || got != model.prev()) throw new AssertionError("prev"); }
                    catch (NoSuchElementException ex) { if (has) throw new AssertionError("prev threw early"); }
                }
            }
        }
    }
}
```
