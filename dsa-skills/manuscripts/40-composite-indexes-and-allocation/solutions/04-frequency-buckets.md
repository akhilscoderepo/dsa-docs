<!-- solutions-for: 04-frequency-buckets -->
### Solutions For Frequency Buckets

#### Solution: [Build] Key Frequency Buckets (Author exercise)
<!-- id: ci40-key-buckets -->

**Approach.** A hash map from key to count is the source of truth. A second hash map from count to a sorted set of keys holds the buckets. An increment reads the old count and removes the key from that bucket, deleting the bucket when it empties. It then writes the new count and inserts the key into the next bucket. A single integer holds the largest count, because counts only grow.

The most common key is the first key of the top bucket, which is the smallest key of that bucket. A `keysAt` call copies the bucket for the count.

The invariant is that each key sits in the bucket numbered by its count, and no bucket is empty. The removal precedes the insertion, so a key never sits in two buckets.

**Complexity.**

- **Time** is O(log n) per call, because each call does a few hash lookups and one or two tree operations on a bucket.
- **Space** is O(n), because each key owns one count and one slot in a bucket.

```java run
import java.util.*;

public final class KeyBucketsSolution {
    static final class KeyBuckets {
        private final Map<String, Integer> countOf = new HashMap<>();          // key -> count, source of truth
        private final Map<Integer, TreeSet<String>> bucket = new HashMap<>();   // count -> sorted keys
        private int top = 0;                                                    // largest count with a bucket

        /**
         * Raises one count by 1 and moves the key to the next bucket.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the key leaves bucket c before it enters bucket c + 1.
         */
        void inc(String key) {
            int c = countOf.getOrDefault(key, 0);
            if (c > 0) {
                // Leave the old bucket and delete it when it empties.
                TreeSet<String> old = bucket.get(c);
                old.remove(key);
                if (old.isEmpty()) bucket.remove(c);
            }
            countOf.put(key, c + 1);
            bucket.computeIfAbsent(c + 1, k -> new TreeSet<>()).add(key);
            // Counts only grow, so the top never needs a search.
            top = Math.max(top, c + 1);
        }

        /** Returns the smallest key of the top bucket or an empty string; O(log n) time, O(1) space. */
        String mostCommon() { return top == 0 ? "" : bucket.get(top).first(); }

        /** Returns the keys with count c in order; O(k) time and space for k keys. */
        List<String> keysAt(int c) { return new ArrayList<>(bucket.getOrDefault(c, new TreeSet<>())); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        KeyBuckets a = new KeyBuckets();
        a.inc("a"); a.inc("b"); a.inc("b");
        if (!a.mostCommon().equals("b")) throw new AssertionError("e1");
        KeyBuckets b = new KeyBuckets();
        b.inc("y"); b.inc("x");
        if (!b.mostCommon().equals("x") || !b.keysAt(1).equals(List.of("x", "y"))) throw new AssertionError("e2");
        if (!new KeyBuckets().mostCommon().isEmpty()) throw new AssertionError("empty");
        // Random increments checked against a plain count map.
        Random rnd = new Random(4001);
        for (int round = 0; round < 300; round++) {
            KeyBuckets s = new KeyBuckets();
            Map<String, Integer> ref = new TreeMap<>();
            for (int op = 0; op < 60; op++) {
                String k = "k" + rnd.nextInt(6);
                ref.merge(k, 1, Integer::sum);
                s.inc(k);
                int best = 0; String bestKey = "";
                for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getValue() > best) { best = e.getValue(); bestKey = e.getKey(); }
                if (!s.mostCommon().equals(bestKey)) throw new AssertionError("mostCommon");
                int c = 1 + rnd.nextInt(best);
                List<String> want = new ArrayList<>();
                for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getValue() == c) want.add(e.getKey());
                if (!s.keysAt(c).equals(want)) throw new AssertionError("keysAt");
            }
        }
    }
}
```

#### Solution: [Vary] All O`one Data Structure (LeetCode 432)
<!-- id: ci40-all-oone -->

**Approach.** The buckets form a doubly linked list in increasing count order, between a head sentinel with count 0 and a tail sentinel. Each node holds its count and a hash set of keys. A hash map from key to node is the source of truth for the key's count.

An increment starts at the key's node, or at the head for a new key. It looks at the next node. If that node has count one higher, the key joins it. Otherwise the call splices a new node right after the current one. A decrement looks at the previous node and does the mirror step, and a key whose count reaches 0 leaves the map. The call unlinks the old node when its set empties. The maximum key comes from the node before the tail, and the minimum key from the node after the head.

The invariant is that the list is sorted by count with no empty node, and each key's node has the key's count. Each call reads one neighbor, so the work is constant on average.

**Complexity.**

- **Time** is O(1) on average per call, because each call reads one neighbor, changes a constant number of links and makes hash operations.
- **Space** is O(n), because each key sits in one set and the list has at most n nodes.

```java run
import java.util.*;

public final class AllOneSolution {
    static final class AllOne {
        private static final class Node {
            final int count;
            final Set<String> keys = new HashSet<>();
            Node prev, next;
            Node(int count) { this.count = count; }
        }
        private final Node head = new Node(0), tail = new Node(0);              // sentinels
        private final Map<String, Node> nodeOf = new HashMap<>();                // key -> its node

        AllOne() { head.next = tail; tail.prev = head; }

        // Splices a new node after a in O(1).
        private Node insertAfter(Node a, int count) {
            Node n = new Node(count);
            n.prev = a; n.next = a.next;
            a.next.prev = n; a.next = n;
            return n;
        }

        // Removes a node from the list in O(1).
        private void unlink(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }

        /**
         * Raises a count by 1.
         * Time: O(1) on average.
         * Space: O(1) extra.
         * Invariant: the target node sits directly after the old node and holds count + 1.
         */
        void inc(String key) {
            Node cur = nodeOf.get(key);
            Node from = cur == null ? head : cur;                  // the head stands for count 0
            Node target = from.next;
            // The neighbor may skip the needed count, so create the bucket when it does.
            if (target == tail || target.count != from.count + 1) target = insertAfter(from, from.count + 1);
            target.keys.add(key);
            nodeOf.put(key, target);
            // The old bucket may be empty now, so remove it.
            if (cur != null) { cur.keys.remove(key); if (cur.keys.isEmpty()) unlink(cur); }
        }

        /**
         * Lowers a count by 1 and drops the key at 0.
         * Time: O(1) on average.
         * Space: O(1) extra.
         * Invariant: the target node sits directly before the old node and holds count - 1.
         */
        void dec(String key) {
            Node cur = nodeOf.get(key);
            if (cur.count == 1) nodeOf.remove(key);
            else {
                Node target = cur.prev;
                if (target == head || target.count != cur.count - 1) target = insertAfter(cur.prev, cur.count - 1);
                target.keys.add(key);
                nodeOf.put(key, target);
            }
            cur.keys.remove(key);
            if (cur.keys.isEmpty()) unlink(cur);
        }

        /** Returns any key with the largest count; O(1) time and space. */
        String getMaxKey() { return tail.prev == head ? "" : tail.prev.keys.iterator().next(); }

        /** Returns any key with the smallest count; O(1) time and space. */
        String getMinKey() { return head.next == tail ? "" : head.next.keys.iterator().next(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        AllOne a = new AllOne();
        a.inc("a"); a.inc("b"); a.inc("b");
        if (!a.getMaxKey().equals("b") || !a.getMinKey().equals("a")) throw new AssertionError("e1");
        AllOne b = new AllOne();
        b.inc("a"); b.dec("a");
        if (!b.getMaxKey().isEmpty() || !b.getMinKey().isEmpty()) throw new AssertionError("e2");
        // Random calls checked against a plain count map; any key with the right count is accepted.
        Random rnd = new Random(432);
        for (int round = 0; round < 300; round++) {
            AllOne s = new AllOne();
            Map<String, Integer> ref = new HashMap<>();
            for (int op = 0; op < 80; op++) {
                String k = "k" + rnd.nextInt(5);
                if (ref.containsKey(k) && rnd.nextInt(3) == 0) {
                    s.dec(k);
                    if (ref.get(k) == 1) ref.remove(k); else ref.merge(k, -1, Integer::sum);
                } else { s.inc(k); ref.merge(k, 1, Integer::sum); }
                int hi = 0, lo = Integer.MAX_VALUE;
                for (int v : ref.values()) { hi = Math.max(hi, v); lo = Math.min(lo, v); }
                String mx = s.getMaxKey(), mn = s.getMinKey();
                if (ref.isEmpty()) { if (!mx.isEmpty() || !mn.isEmpty()) throw new AssertionError("empty"); }
                else if (ref.get(mx) == null || ref.get(mx) != hi || ref.get(mn) == null || ref.get(mn) != lo) throw new AssertionError("min or max");
            }
        }
    }
}
```

#### Solution: [Boundary] Empty Bucket Removal (Author exercise)
<!-- id: ci40-empty-bucket -->

**Approach.** This solution stores the buckets in a tree map from count to a sorted set of keys, so the order of buckets comes from the tree and not from links. A hash map from key to count is the source of truth. One helper moves a key from a count to a new count. It removes the key from the old bucket, deletes that tree map entry when the set is empty, and inserts the key into the new bucket. A move to count 0 only removes.

The number of buckets is the size of the tree map. The largest count is the last key of the tree map, and its smallest key is the first element of that bucket.

The invariant is that every tree map entry holds at least one key, so `bucketCount()` equals the number of distinct counts held by live keys. The helper is the only code that changes a bucket, so the check for an empty bucket cannot be skipped.

**Complexity.**

- **Time** is O(log n) per call, because the tree map and the tree sets cost logarithmic time per operation.
- **Space** is O(n), since every key holds one count and sits in exactly one bucket set.

```java run
import java.util.*;

public final class EmptyBucketSolution {
    static final class CountLedger {
        private final Map<String, Integer> countOf = new HashMap<>();
        private final TreeMap<Integer, TreeSet<String>> buckets = new TreeMap<>();

        /**
         * Moves a key between buckets and deletes any bucket that empties.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: no entry of buckets is empty when the helper returns.
         */
        private void move(String key, int from, int to) {
            if (from > 0) {
                TreeSet<String> old = buckets.get(from);
                old.remove(key);
                // Delete the bucket in the same step that empties it.
                if (old.isEmpty()) buckets.remove(from);
            }
            if (to > 0) {
                countOf.put(key, to);
                buckets.computeIfAbsent(to, k -> new TreeSet<>()).add(key);
            } else {
                countOf.remove(key);
            }
        }

        /** Raises a count by 1; O(log n) time, O(1) space; invariant: delegated to move. */
        void inc(String key) {
            int c = countOf.getOrDefault(key, 0);
            move(key, c, c + 1);
        }

        /** Lowers a count by 1 and drops the key at 0; O(log n) time, O(1) space; invariant: delegated to move. */
        void dec(String key) {
            int c = countOf.get(key);
            move(key, c, c - 1);
        }

        /** Returns the smallest key with the largest count; O(log n) time, O(1) space. */
        String getMaxKey() { return buckets.isEmpty() ? "" : buckets.lastEntry().getValue().first(); }

        /** Returns the number of distinct positive counts; O(1) time and space. */
        int bucketCount() { return buckets.size(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        CountLedger a = new CountLedger();
        a.inc("a"); a.inc("b"); a.inc("b");
        if (a.bucketCount() != 2) throw new AssertionError("e1 before");
        a.dec("a");
        if (a.bucketCount() != 1) throw new AssertionError("e1 after");
        CountLedger b = new CountLedger();
        b.inc("x"); b.inc("y"); b.inc("x"); b.inc("y");
        if (b.bucketCount() != 1) throw new AssertionError("e2 before");
        b.dec("y");
        if (b.bucketCount() != 2) throw new AssertionError("e2 after");
        if (new CountLedger().bucketCount() != 0 || !new CountLedger().getMaxKey().isEmpty()) throw new AssertionError("empty");
        // Random calls checked against a recount of distinct values.
        Random rnd = new Random(4003);
        for (int round = 0; round < 300; round++) {
            CountLedger s = new CountLedger();
            Map<String, Integer> ref = new TreeMap<>();
            for (int op = 0; op < 80; op++) {
                String k = "k" + rnd.nextInt(5);
                if (ref.containsKey(k) && rnd.nextInt(3) == 0) {
                    s.dec(k);
                    if (ref.get(k) == 1) ref.remove(k); else ref.merge(k, -1, Integer::sum);
                } else { s.inc(k); ref.merge(k, 1, Integer::sum); }
                if (s.bucketCount() != new HashSet<>(ref.values()).size()) throw new AssertionError("bucketCount");
                int hi = 0; String hiKey = "";
                for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getValue() > hi) { hi = e.getValue(); hiKey = e.getKey(); }
                if (!s.getMaxKey().equals(hiKey)) throw new AssertionError("getMaxKey");
            }
        }
    }
}
```

#### Solution: [Recognize] Maximum Frequency Stack (LeetCode 895)
<!-- id: ci40-freq-stack -->

**Approach.** A hash map from value to count is the source of truth. A second hash map from frequency to a stack of values holds the buckets. A push raises the count of the value to `f` and pushes the value onto the stack for `f`. The value therefore appears once in every stack from 1 up to its count, in push order. An integer tracks the highest frequency that has a non-empty stack.

A pop takes the top of the stack for the highest frequency, lowers that value's count by 1 and lowers the highest frequency when the stack becomes empty. The top of the highest stack is the value whose latest push reached that frequency, which is the value closest to the top among the tied values.

The invariant is that the stack for frequency `f` holds one entry for each value with a count of at least `f`, in the order in which those values reached `f`.

**Complexity.**

- **Time** is O(1) per call, because each call does a constant number of hash and deque operations.
- **Space** is O(n), because a value with count `f` owns `f` entries, and the entries add up to the number of pushes.

```java run
import java.util.*;

public final class FreqStackSolution {
    static final class FreqStack {
        private final Map<Integer, Integer> countOf = new HashMap<>();            // value -> occurrences
        private final Map<Integer, Deque<Integer>> stackAt = new HashMap<>();      // frequency -> values in push order
        private int top = 0;                                                       // highest non-empty frequency

        /**
         * Pushes a value into the stack for its new frequency.
         * Time: O(1).
         * Space: O(1) extra.
         * Invariant: the value appears in stacks 1 through its count.
         */
        void push(int val) {
            int f = countOf.merge(val, 1, Integer::sum);
            stackAt.computeIfAbsent(f, k -> new ArrayDeque<>()).push(val);
            top = Math.max(top, f);
        }

        /**
         * Removes the most frequent value, preferring the latest push on ties.
         * Time: O(1).
         * Space: O(1) extra.
         * Invariant: top names the highest non-empty stack after the call.
         */
        int pop() {
            Deque<Integer> st = stackAt.get(top);
            int val = st.pop();
            // The highest stack may empty, so move top down by one.
            if (st.isEmpty()) top--;
            // Lower the count or drop the value at zero.
            if (countOf.get(val) == 1) countOf.remove(val); else countOf.merge(val, -1, Integer::sum);
            return val;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        FreqStack a = new FreqStack();
        for (int v : new int[] {5, 7, 5, 7, 4, 5}) a.push(v);
        int[] want = {5, 7, 5, 4};
        for (int w : want) if (a.pop() != w) throw new AssertionError("e1");
        FreqStack b = new FreqStack();
        b.push(1); b.push(1); b.push(2);
        if (b.pop() != 1 || b.pop() != 2) throw new AssertionError("e2");
        // Random calls checked against a list scan: highest count, then latest last occurrence.
        Random rnd = new Random(895);
        for (int round = 0; round < 300; round++) {
            FreqStack s = new FreqStack();
            List<Integer> ref = new ArrayList<>();
            for (int op = 0; op < 80; op++) {
                if (ref.isEmpty() || rnd.nextInt(5) < 3) { int v = rnd.nextInt(4); ref.add(v); s.push(v); }
                else {
                    int bestVal = -1, bestCount = 0, bestLast = -1;
                    for (int v = 0; v < 4; v++) {
                        int cnt = Collections.frequency(ref, v), last = ref.lastIndexOf(v);
                        if (cnt > bestCount || (cnt == bestCount && cnt > 0 && last > bestLast)) { bestVal = v; bestCount = cnt; bestLast = last; }
                    }
                    ref.remove(bestLast);
                    if (s.pop() != bestVal) throw new AssertionError("pop");
                }
            }
        }
    }
}
```
