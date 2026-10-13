<!-- solutions-for: 93-iterator-api-state -->
### Solutions For Iterator State

#### Solution: [Build] Tree Iterator Over A Node Pool (LeetCode 173)
<!-- id: ds-pool-tree-iterator -->

**Approach.**
The stack holds node indexes in an int array whose size is the pool length, since a path never has more nodes than the pool. The constructor walks from the root through `left` links and pushes every index on the way. The invariant is that the stack holds exactly the nodes on the path from the root to the next node to return that are not yet returned, with the next node on top. The operation `next()` pops the top, pushes the left spine of its right child to restore the invariant, and returns the popped value. The operation `hasNext()` tests `top > 0` and changes nothing. The operation `peekDepth()` returns `top`, which equals the number of unfinished ancestors plus the next node. An exhausted `next()` throws before it touches any field, so the state stays valid.

**Complexity.**
- **Time** is O(1) amortized for `next()`, because each node is pushed once and popped once across a full traversal, and O(h) for a single call in the worst case.
- **Space** is O(h) in use, because the stack never holds more than one root-to-node path, and the array is allocated at the pool length for simplicity.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class PoolTreeIteratorDemo {
    static final class PoolTreeIterator {
        private final int[] left, right, val;
        // Stack of node indexes; top is the count of used slots.
        private final int[] stack;
        private int top = 0;

        PoolTreeIterator(int[] left, int[] right, int[] val, int root) {
            this.left = left;
            this.right = right;
            this.val = val;
            this.stack = new int[val.length];
            pushLeftSpine(root);
        }

        /** Pushes node and every left descendant; each node enters the stack once, so the total cost is O(n). */
        private void pushLeftSpine(int node) {
            // Walk down the left links until the index -1 marks the end of the spine.
            while (node != -1) {
                stack[top++] = node;
                node = left[node];
            }
        }

        /** Time: O(1). Space: O(1). Reads state only. */
        boolean hasNext() {
            // The stack is empty exactly when every value was returned.
            return top > 0;
        }

        /** Time: O(1) amortized, O(h) worst case. Space: O(h). Invariant: the top is the next node after the call. */
        int next() {
            // Throw before any write so the failure leaves the state valid.
            if (top == 0) throw new NoSuchElementException();
            // The top node holds the next value in increasing order.
            int node = stack[--top];
            // Restore the invariant: the left spine of the right child comes before everything still on the stack.
            pushLeftSpine(right[node]);
            return val[node];
        }

        /** Time: O(1). Space: O(1). Returns the stack size. */
        int peekDepth() {
            return top;
        }
    }

    /** Oracle: in-order values by recursion over the pool. */
    static void inorder(int[] l, int[] r, int[] v, int node, List<Integer> out) {
        if (node == -1) return;
        inorder(l, r, v, l[node], out);
        out.add(v[node]);
        inorder(l, r, v, r[node], out);
    }

    /** Oracle for the depth: nodes on the search path to the next value whose value is at least that value. */
    static int expectedDepth(int[] l, int[] r, int[] v, int root, int nextValue) {
        int depth = 0;
        int node = root;
        // Search for the next value like a normal tree lookup and count nodes not smaller than it.
        while (node != -1) {
            if (v[node] >= nextValue) depth++;
            if (v[node] == nextValue) break;
            node = nextValue < v[node] ? l[node] : r[node];
        }
        return depth;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise: the depths and values are recomputed here.
        int[] val = {8, 3, 10, 1, 6, 14, 4};
        int[] left = {1, 3, -1, -1, 6, -1, -1};
        int[] right = {2, 4, 5, -1, -1, -1, -1};
        PoolTreeIterator it = new PoolTreeIterator(left, right, val, 0);
        int[] depths = {3, 2, 3, 2, 1, 1, 1, 0};
        int[] values = {1, 3, 4, 6, 8, 10, 14};
        if (it.peekDepth() != depths[0]) throw new AssertionError("initial depth");
        for (int i = 0; i < values.length; i++) {
            if (!it.hasNext()) throw new AssertionError("hasNext " + i);
            if (it.next() != values[i]) throw new AssertionError("value " + i);
            if (it.peekDepth() != depths[i + 1]) throw new AssertionError("depth " + i);
        }
        if (it.hasNext()) throw new AssertionError("should be exhausted");
        boolean threw = false;
        try { it.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");
        if (it.peekDepth() != 0) throw new AssertionError("failed next changed the state");

        // Example 2: a chain that leans right never holds more than one node.
        PoolTreeIterator chain = new PoolTreeIterator(new int[] {-1, -1, -1}, new int[] {1, 2, -1}, new int[] {5, 6, 7}, 0);
        int[] chainDepths = {1, 1, 1, 0};
        int[] chainValues = {5, 6, 7};
        if (chain.peekDepth() != chainDepths[0]) throw new AssertionError("chain initial");
        for (int i = 0; i < 3; i++) {
            if (chain.next() != chainValues[i]) throw new AssertionError("chain value");
            if (chain.peekDepth() != chainDepths[i + 1]) throw new AssertionError("chain depth");
        }
        // A left-leaning chain holds every node at once; an empty tree holds none.
        PoolTreeIterator lean = new PoolTreeIterator(new int[] {1, 2, -1}, new int[] {-1, -1, -1}, new int[] {9, 8, 7}, 0);
        if (lean.peekDepth() != 3) throw new AssertionError("left chain");
        PoolTreeIterator empty = new PoolTreeIterator(new int[0], new int[0], new int[0], -1);
        if (empty.hasNext() || empty.peekDepth() != 0) throw new AssertionError("empty tree");

        // Random check: insert distinct values into a pool, replay random calls, compare with the oracle.
        Random rnd = new Random(173);
        for (int trial = 0; trial < 300; trial++) {
            int n = rnd.nextInt(40);
            int[] l = new int[n], r = new int[n], v = new int[n];
            java.util.Arrays.fill(l, -1);
            java.util.Arrays.fill(r, -1);
            java.util.HashSet<Integer> used = new java.util.HashSet<>();
            int count = 0;
            int root = -1;
            while (count < n) {
                int x = rnd.nextInt(1000);
                if (!used.add(x)) continue;
                v[count] = x;
                if (root == -1) root = count;
                else {
                    int cur = root;
                    // Standard binary search tree insertion into the pool.
                    while (true) {
                        if (x < v[cur]) { if (l[cur] == -1) { l[cur] = count; break; } cur = l[cur]; }
                        else { if (r[cur] == -1) { r[cur] = count; break; } cur = r[cur]; }
                    }
                }
                count++;
            }
            List<Integer> expected = new ArrayList<>();
            inorder(l, r, v, root, expected);
            PoolTreeIterator t = new PoolTreeIterator(l, r, v, root);
            int returned = 0;
            // Interleave hasNext, peekDepth and next in random order.
            for (int step = 0; step < 4 * n + 4; step++) {
                int op = rnd.nextInt(3);
                boolean more = returned < expected.size();
                if (op == 0) {
                    if (t.hasNext() != more) throw new AssertionError("hasNext oracle");
                } else if (op == 1) {
                    int want = more ? expectedDepth(l, r, v, root, expected.get(returned)) : 0;
                    if (t.peekDepth() != want) throw new AssertionError("depth oracle");
                } else if (more) {
                    if (t.next() != expected.get(returned)) throw new AssertionError("next oracle");
                    returned++;
                }
            }
        }
    }
}
```

#### Solution: [Vary] Peeking Over A Source That Cannot Restart (LeetCode 284)
<!-- id: ds-counting-peeker -->

**Approach.**
The wrapper keeps one cached element in `head` and a flag `hasHead`. The operation `peek()` pulls from the source only when the slot is empty, stores the result and returns it, so repeated peeks return the stored value with no source call. The operation `next()` hands over the stored element and clears the flag, or pulls directly when the slot is empty. The operation `hasNext()` returns `hasHead || source.hasNext()`, and `source.hasNext()` is a question that the source answers without producing an element, so it never touches the counter. The invariant is that the elements not yet returned are the cached element, if any, followed by the rest of the source. Every pull happens at the moment an element leaves the source for the first time, so `calls` equals the number of elements returned plus one when the slot is full.

**Complexity.**
- **Time** is O(1) for every operation, because each does a constant number of field reads and at most one source call.
- **Space** is O(1) extra, because the wrapper stores one `int` and one flag.

```java run
import java.util.NoSuchElementException;
import java.util.Random;

public final class CountingPeekerDemo {
    interface IntSource {
        boolean hasNext();
        int next();
    }

    /** Source that cannot restart and counts its own next() calls. */
    static final class CountingSource implements IntSource {
        private final int[] data;
        private int index = 0;
        int calls = 0;

        CountingSource(int[] data) { this.data = data; }

        public boolean hasNext() { return index < data.length; }

        public int next() {
            if (index >= data.length) throw new NoSuchElementException();
            calls++;
            return data[index++];
        }
    }

    static final class CountingPeeker {
        private final IntSource source;
        private int head;
        private boolean hasHead;

        CountingPeeker(IntSource source) { this.source = source; }

        /** Time: O(1). Space: O(1). Pulls at most once, only when the slot is empty. */
        int peek() {
            // An empty slot is the only moment a pull may happen; the exhausted source throws here.
            if (!hasHead) {
                head = source.next();
                hasHead = true;
            }
            return head;
        }

        /** Time: O(1). Space: O(1). Never calls source.next(). */
        boolean hasNext() {
            // Either the slot holds an element or the source still has one.
            return hasHead || source.hasNext();
        }

        /** Time: O(1). Space: O(1). Invariant: unreturned elements are the slot followed by the source rest. */
        int next() {
            // Hand over the cached element first so no element is skipped or repeated.
            if (hasHead) {
                hasHead = false;
                return head;
            }
            return source.next();
        }
    }

    public static void main(String[] args) {
        // Example 1: results and the counter after each stage are recomputed here.
        CountingSource s = new CountingSource(new int[] {4, 7, 9});
        CountingPeeker p = new CountingPeeker(s);
        if (p.peek() != 4 || p.peek() != 4) throw new AssertionError("peek twice");
        if (s.calls != 1) throw new AssertionError("two peeks must pull once");
        if (!p.hasNext() || s.calls != 1) throw new AssertionError("hasNext must not pull");
        if (p.next() != 4 || s.calls != 1) throw new AssertionError("next uses the cache");
        if (p.next() != 7 || s.calls != 2) throw new AssertionError("next pulls directly");
        if (p.peek() != 9 || s.calls != 3) throw new AssertionError("peek pulls once");
        if (p.next() != 9 || s.calls != 3) throw new AssertionError("last next");
        if (p.hasNext()) throw new AssertionError("exhausted");

        // Example 2: repeated hasNext never touches the source.
        CountingSource one = new CountingSource(new int[] {5});
        CountingPeeker q = new CountingPeeker(one);
        for (int i = 0; i < 3; i++) if (!q.hasNext()) throw new AssertionError("hasNext true");
        if (one.calls != 0) throw new AssertionError("no pull yet");
        if (q.next() != 5 || one.calls != 1) throw new AssertionError("single pull");

        // An empty source makes peek and next throw and records no call.
        CountingSource none = new CountingSource(new int[0]);
        CountingPeeker e = new CountingPeeker(none);
        boolean peekThrew = false;
        boolean nextThrew = false;
        try { e.peek(); } catch (NoSuchElementException ex) { peekThrew = true; }
        try { e.next(); } catch (NoSuchElementException ex) { nextThrew = true; }
        if (!peekThrew || !nextThrew || none.calls != 0) throw new AssertionError("empty source");

        // Random check: replay random operations against a list model and compare values and call counts.
        Random rnd = new Random(284);
        for (int trial = 0; trial < 500; trial++) {
            int m = rnd.nextInt(12);
            int[] data = new int[m];
            for (int i = 0; i < m; i++) data[i] = rnd.nextInt(100);
            CountingSource src = new CountingSource(data);
            CountingPeeker w = new CountingPeeker(src);
            int consumed = 0;
            boolean cached = false;
            for (int step = 0; step < 40; step++) {
                int before = src.calls;
                int op = rnd.nextInt(3);
                boolean more = consumed < m;
                if (op == 0) {
                    if (w.hasNext() != more) throw new AssertionError("hasNext model");
                    if (src.calls != before) throw new AssertionError("hasNext pulled");
                } else if (op == 1) {
                    if (!more) {
                        boolean threw = false;
                        try { w.peek(); } catch (NoSuchElementException ex) { threw = true; }
                        if (!threw) throw new AssertionError("peek must throw");
                    } else {
                        if (w.peek() != data[consumed]) throw new AssertionError("peek model");
                        // A peek pulls once when the slot was empty and never otherwise.
                        if (src.calls - before != (cached ? 0 : 1)) throw new AssertionError("peek pulls");
                        cached = true;
                    }
                } else if (more) {
                    if (w.next() != data[consumed]) throw new AssertionError("next model");
                    // A next pulls once only when the slot was empty.
                    if (src.calls - before != (cached ? 0 : 1)) throw new AssertionError("next pulls");
                    consumed++;
                    cached = false;
                }
                // The counter equals the returned elements plus the cached one.
                if (src.calls != consumed + (cached ? 1 : 0)) throw new AssertionError("call total");
            }
        }
    }
}
```

#### Solution: [Boundary] Flatten With Empty Lists And A Depth Limit (LeetCode 341)
<!-- id: ds-bounded-flatten -->

**Approach.**
The constructor only stores the top-level iterator, so it costs O(1) and reads nothing. The iteration keeps a stack of Java iterators, one for each list that still has unread entries, plus a cached integer `head`. The operation `hasNext()` loops while no integer is cached. It pops finished iterators, which are empty lists or finished lists, pushes the iterator of any nested list it meets, and stores the first integer it reaches. The stack size is the depth of the list on top, so before it pushes a nested list it compares the new depth with `maxDepth`. A list that is too deep sets a failed flag and throws `IllegalArgumentException`, and every later call throws again. Moving past empty lists removes no integer from the sequence, and repeating the call finds the cached integer at once, so `hasNext()` is idempotent. The invariant is that the integers not yet returned are the cached one, if any, followed by what the stacked iterators will produce. The operation `next()` calls `hasNext()`, clears the cache and returns it.

**Complexity.**
- **Time** is O(N) in total for N entries, including integers and lists, because each entry is read once. The depth comparison costs O(1) per list.
- **Space** is O(d) for the stack, where d is at most `maxDepth`, plus O(1) for the cache.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class BoundedFlattenDemo {
    /** Either one integer or a list of Nest values; a list may be empty. */
    static final class Nest {
        final Integer value;
        final List<Nest> items;

        private Nest(Integer value, List<Nest> items) { this.value = value; this.items = items; }

        static Nest of(int v) { return new Nest(v, null); }

        static Nest list(Nest... parts) { return new Nest(null, Arrays.asList(parts)); }

        boolean isInt() { return value != null; }
    }

    static final class FlatIterator {
        private final ArrayDeque<Iterator<Nest>> stack = new ArrayDeque<>();
        private int head;
        private boolean hasHead = false;
        private boolean failed = false;
        private final int maxDepth;

        FlatIterator(List<Nest> top, int maxDepth) {
            // The constructor reads nothing; the depth limit is checked during the scan.
            this.maxDepth = maxDepth;
            stack.push(top.iterator());
        }

        /** Time: O(1) amortized. Space: O(d). Skips empty lists and caches the next integer; removes nothing. */
        boolean hasNext() {
            // A list that was too deep keeps the iterator failed for every later call.
            if (failed) throw new IllegalArgumentException("depth exceeds " + maxDepth);
            // Keep going until an integer is cached or every iterator is finished.
            while (!hasHead && !stack.isEmpty()) {
                Iterator<Nest> top = stack.peek();
                if (!top.hasNext()) {
                    // A finished or empty list contributes nothing, so drop its cursor.
                    stack.pop();
                } else {
                    Nest n = top.next();
                    if (n.isInt()) {
                        // Cache the integer; it is pulled but not yet returned.
                        head = n.value;
                        hasHead = true;
                    } else {
                        // The stack size is the depth of the top list, so the nested list sits one deeper.
                        if (stack.size() + 1 > maxDepth) {
                            failed = true;
                            throw new IllegalArgumentException("depth " + (stack.size() + 1) + " exceeds " + maxDepth);
                        }
                        // A nested list becomes the new top cursor.
                        stack.push(n.items.iterator());
                    }
                }
            }
            return hasHead;
        }

        /** Time: O(1) amortized. Space: O(d). Invariant: unreturned integers are the cache then the stack. */
        int next() {
            if (!hasNext()) throw new NoSuchElementException();
            hasHead = false;
            return head;
        }
    }

    static int depthOf(List<Nest> list, int depth) {
        int best = depth;
        for (Nest n : list) if (!n.isInt()) best = Math.max(best, depthOf(n.items, depth + 1));
        return best;
    }

    static void flatten(List<Nest> list, List<Integer> out) {
        for (Nest n : list) {
            if (n.isInt()) out.add(n.value);
            else flatten(n.items, out);
        }
    }

    static Nest random(Random rnd, int depthLeft) {
        if (depthLeft == 0 || rnd.nextInt(3) == 0) return Nest.of(rnd.nextInt(50));
        int len = rnd.nextInt(4);
        Nest[] parts = new Nest[len];
        for (int i = 0; i < len; i++) parts[i] = random(rnd, depthLeft - 1);
        return Nest.list(parts);
    }

    public static void main(String[] args) {
        // Example 1: empty lists at the start, interior and end, depth exactly at the limit.
        List<Nest> top = Arrays.asList(
            Nest.list(), Nest.of(1), Nest.list(Nest.list(), Nest.of(2), Nest.list()), Nest.list(), Nest.of(3), Nest.list());
        if (depthOf(top, 1) != 3) throw new AssertionError("the example depth is 3");
        FlatIterator it = new FlatIterator(top, 3);
        // Repeated hasNext calls return the same answer and consume nothing.
        if (!it.hasNext() || !it.hasNext() || !it.hasNext()) throw new AssertionError("hasNext repeat");
        int[] want = {1, 2, 3};
        for (int w : want) if (it.next() != w) throw new AssertionError("value " + w);
        if (it.hasNext()) throw new AssertionError("exhausted");
        boolean threw = false;
        try { it.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("next must throw");

        // Example 2: with a limit of 2 the first next returns 1, and the following hasNext throws.
        FlatIterator shallow = new FlatIterator(top, 2);
        if (shallow.next() != 1) throw new AssertionError("value before the deep list");
        boolean rejected = false;
        try { shallow.hasNext(); } catch (IllegalArgumentException e) { rejected = true; }
        if (!rejected) throw new AssertionError("depth limit");
        // Every later call throws again.
        rejected = false;
        try { shallow.next(); } catch (IllegalArgumentException e) { rejected = true; }
        if (!rejected) throw new AssertionError("sticky failure");

        // Only empty lists: no values at all.
        FlatIterator hollow = new FlatIterator(Arrays.asList(Nest.list(Nest.list())), 3);
        if (hollow.hasNext()) throw new AssertionError("only empty lists");

        // Random check: compare with a recursive flatten, and the limit with a recursive depth.
        Random rnd = new Random(341);
        for (int trial = 0; trial < 500; trial++) {
            int parts = rnd.nextInt(6);
            Nest[] arr = new Nest[parts];
            for (int i = 0; i < parts; i++) arr[i] = random(rnd, 5);
            List<Nest> input = Arrays.asList(arr);
            int limit = 1 + rnd.nextInt(6);
            int depth = depthOf(input, 1);
            if (depth > limit) {
                boolean bad = false;
                FlatIterator deep = new FlatIterator(input, limit);
                // A full drain enters every list, so it must reach the deep one.
                try { while (deep.hasNext()) deep.next(); } catch (IllegalArgumentException e) { bad = true; }
                if (!bad) throw new AssertionError("limit should reject depth " + depth);
                continue;
            }
            List<Integer> expected = new ArrayList<>();
            flatten(input, expected);
            FlatIterator f = new FlatIterator(input, limit);
            int at = 0;
            // Randomly repeat hasNext before each next to check that it never consumes.
            while (true) {
                int repeats = rnd.nextInt(3);
                boolean more = false;
                for (int i = 0; i <= repeats; i++) more = f.hasNext();
                if (more != (at < expected.size())) throw new AssertionError("hasNext oracle");
                if (!more) break;
                if (f.next() != expected.get(at)) throw new AssertionError("value oracle");
                at++;
            }
        }
    }
}
```

#### Solution: [Recognize] Zigzag Over K Sources With Rotation Count (LeetCode 281)
<!-- id: ds-zigzag-rotations -->

**Approach.**
The class keeps one read position for each source, a cursor, a count of values left and a counter of rotations. The invariant is that whenever values remain, the cursor names a source whose position is before its end. The constructor runs `skipExhausted`, which advances the cursor one source at a time while the current source has no value, and each step adds one to the counter. The operation `next()` reads the value at the cursor, advances that position and lowers the remaining count. If values remain, it moves the cursor forward one step, counts it and calls `skipExhausted`, so the invariant holds again. When nothing remains, no step is taken, which keeps the cursor from looping on empty sources. The operation `hasNext()` tests the remaining count and changes nothing.

**Complexity.**
- **Time** is O(k) worst case for one call, because the cursor may pass every source once, and the total of all rotations is at most the number of values times k.
- **Space** is O(k) for the read positions, plus O(1) for the other fields, and the sources are not copied.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class ZigzagRotationsDemo {
    static final class Zigzag {
        private final int[][] sources;
        private final int[] pos;
        private int cursor = 0;
        private int remaining = 0;
        private int rotations = 0;

        Zigzag(int[][] sources) {
            this.sources = sources;
            this.pos = new int[sources.length];
            for (int[] s : sources) remaining += s.length;
            // Establish the invariant right after construction.
            if (remaining > 0) skipExhausted();
        }

        /** Moves the cursor forward, one counted step at a time, until it names a source with a value left. */
        private void skipExhausted() {
            // The loop ends because remaining > 0 guarantees some source still has a value.
            while (pos[cursor] == sources[cursor].length) {
                cursor = (cursor + 1) % sources.length;
                rotations++;
            }
        }

        /** Time: O(1). Space: O(1). Reads state only. */
        boolean hasNext() {
            return remaining > 0;
        }

        /** Time: O(k) worst case. Space: O(1). Invariant: the cursor names a source with a value, unless nothing remains. */
        int next() {
            if (remaining == 0) throw new NoSuchElementException();
            int value = sources[cursor][pos[cursor]++];
            remaining--;
            // Rotate only while values remain so the cursor never spins on empty sources.
            if (remaining > 0) {
                cursor = (cursor + 1) % sources.length;
                rotations++;
                skipExhausted();
            }
            return value;
        }

        /** Time: O(1). Space: O(1). */
        int rotations() {
            return rotations;
        }
    }

    /** Oracle: round-by-round order, and rotation count from cyclic distances between the used sources. */
    static int[] oracle(int[][] src, List<Integer> values) {
        List<Integer> used = new ArrayList<>();
        int longest = 0;
        for (int[] s : src) longest = Math.max(longest, s.length);
        for (int round = 0; round < longest; round++) {
            for (int j = 0; j < src.length; j++) {
                if (round < src[j].length) {
                    values.add(src[j][round]);
                    used.add(j);
                }
            }
        }
        int k = src.length;
        int total = 0;
        int previous = 0;
        // The first distance starts at source 0; later ones start at the previous source and wrap a full circle on a tie.
        for (int idx = 0; idx < used.size(); idx++) {
            int j = used.get(idx);
            if (idx == 0) total += j;
            else {
                int d = ((j - previous) % k + k) % k;
                total += d == 0 ? k : d;
            }
            previous = j;
        }
        return new int[] {total};
    }

    public static void main(String[] args) {
        // Example 1: values and rotation count are recomputed from the sources.
        int[][] a = {{1, 2, 3}, {}, {4}, {5, 6}};
        Zigzag z = new Zigzag(a);
        int[] want = {1, 4, 5, 2, 6, 3};
        for (int w : want) {
            if (!z.hasNext() || z.next() != w) throw new AssertionError("value " + w);
        }
        if (z.hasNext()) throw new AssertionError("exhausted");
        if (z.rotations() != 8) throw new AssertionError("rotations of example 1");
        boolean threw = false;
        try { z.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted next must throw");

        // Example 2: one source wraps once after the first value and stops after the last.
        Zigzag single = new Zigzag(new int[][] {{7, 8}});
        if (single.next() != 7 || single.next() != 8 || single.rotations() != 1) throw new AssertionError("single source");
        // No values: no steps at all.
        Zigzag hollow = new Zigzag(new int[][] {{}, {}});
        if (hollow.hasNext() || hollow.rotations() != 0) throw new AssertionError("all empty");

        // Random check: compare order and rotation count with the round-based oracle.
        Random rnd = new Random(281);
        for (int trial = 0; trial < 500; trial++) {
            int k = 1 + rnd.nextInt(6);
            int[][] src = new int[k][];
            for (int j = 0; j < k; j++) {
                src[j] = new int[rnd.nextInt(5)];
                for (int i = 0; i < src[j].length; i++) src[j][i] = rnd.nextInt(100);
            }
            List<Integer> expected = new ArrayList<>();
            int expectedRotations = oracle(src, expected)[0];
            Zigzag t = new Zigzag(src);
            for (int v : expected) {
                // hasNext twice proves it consumes nothing.
                if (!t.hasNext() || !t.hasNext()) throw new AssertionError("hasNext");
                if (t.next() != v) throw new AssertionError("order oracle");
            }
            if (t.hasNext()) throw new AssertionError("leftover");
            if (t.rotations() != expectedRotations) throw new AssertionError("rotation oracle");
        }
    }
}
```
