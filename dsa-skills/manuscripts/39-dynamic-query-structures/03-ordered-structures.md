<!-- lesson-kind: standard -->
<!-- lesson-id: ordered-structures -->
## Ordered Structures

<!-- stage: context -->
### Find The Nearest Score Below A Limit

A game server keeps player scores and must answer one question many times per second. What is the highest stored score that does not exceed 1500? New scores arrive all the time, and old ones leave. Lesson 02 used a library sorted map. This exercise sets a standalone constraint instead: the runtime offers only arrays, linked nodes and integers, so the sorted structure must be built by hand.

A sorted array answers the question with binary search, but every insertion shifts half of the array. A linked chain inserts in constant time once the position is known. Finding that position means visiting nodes one by one. This lesson asks how to build search that stays fast while both insertions and removals keep happening.

<!-- stage: naive -->
### Walk A Sorted Chain Node By Node

The direct approach keeps the scores in a sorted singly linked chain. To answer the question, it starts at the first node and follows links until the next key would exceed the limit.

```java
final class SortedChain {
    static final class Node {
        int key;
        Node next;
        Node(int key, Node next) { this.key = key; this.next = next; }
    }

    Node first; // smallest key, or null for an empty chain

    // Returns the largest key at most limit, or -1 when every key is larger.
    int floor(long limit) {
        int best = -1;
        for (Node cur = first; cur != null && cur.key <= limit; cur = cur.next) {
            best = cur.key;
        }
        return best;
    }
}
```

Insertion and removal reuse the same walk to find the neighbor node, then relink in constant time. The code is short and correct, and it never shifts any element.

<!-- stage: bottleneck -->
### One Link Per Step Is Too Slow

```predict
A chain holds 1,000,000 sorted keys and the limit is larger than every key. How many links does floor follow, and does a longer chain change that count?

The loop follows all 1,000,000 links, because the cursor must pass every node before it reaches the end. A chain twice as long needs twice as many steps.
```

The walk costs O(n) per query, since the cursor moves exactly one node per step and the answer can sit at the far end. With 100,000 calls on 100,000 keys, the work reaches about 10^10 link follows. Insertion and removal inherit the same cost because they must locate the neighbor first.

The slow part is not relinking. The slow part is that the chain offers no way to jump over many nodes. A structure that keeps the sorted order but lets a search skip long stretches would cut the cost without shifting any element.

<!-- stage: insight -->
### Short Cuts Over A Sorted Chain

#### Stack Sparser Chains On Top

Keep the full sorted chain as level 0. Build level 1 as a second chain that holds only some of those nodes, again in sorted order. Build level 2 from some nodes of level 1, and continue upward. Every node on a higher level is the same node as on level 0, with one extra forward link per level.

This layered arrangement is a **skip list**. A search starts at the sparsest level and moves right while the next key still fits. When the next key is too large, the search drops one level and continues from the same node. At level 0 the search stops on the answer.

#### Choose Which Nodes Move Up

The rule that picks which nodes appear on higher levels is **promotion**. A fixed rule such as "every second node of a level moves up" gives about log n levels. Each level halves the remaining stretch. For a structure that changes, a fixed rule breaks on insertion. A new node instead flips a coin at insertion time and moves up one more level for each head. Each level then holds about half the nodes of the level below, in expectation.

<!-- names: skip list, promotion, predecessor -->

#### Return The Predecessor

A search never moves past the limit, so it ends on the **predecessor**. That node is the last one whose key is below the limit, or at or below it for a closed comparison. Insertion needs exactly this node on every level, because the new node attaches right after it. Erase needs it too, because it must relink the node before the removed one. One descent therefore serves search, insert and erase.

The invariant says that every level is sorted and forms a subsequence of the level below. Insertion and erase only splice links after the predecessors, so the invariant survives each call.

<!-- stage: variables -->
### Name The Pieces Before Coding

Four quantities describe the structure at any time.

- **Level count** is how many chains exist, about the base-2 logarithm of the number of nodes.
- **Node height** is the number of levels a node belongs to, and it equals its number of forward links.
- **Head** is a sentinel node that belongs to every level and holds no key.
- **Update array** stores, for each level, the last node whose key is below the target.

The comparison against the target is strict for insert, erase and exact search, and non-strict only for the floor query.

<!-- stage: trace -->
### Follow One Search And One Erase

#### Search For A Floor

Take the eight keys 3, 7, 12, 18, 25, 31, 40 and 52 at indexes 0 to 7. Index i occupies one level plus the number of trailing zero bits of i + 1. This rule is a deterministic stand-in for the coin flips, so every run of the trace repeats exactly. The heights are therefore 1, 2, 1, 3, 1, 2, 1 and 4. Only key 52 reaches level 3.

The first trace answers the floor of 31. At level 3 the next key from the head is 52, which fails, so the search drops. At level 2 the cursor moves to key 18, then key 52 fails and the search drops. At level 1 the cursor moves to key 31, and key 52 fails again. At level 0 the next key is 40, which fails, so the cursor rests on index 5. That is six comparisons, against seven for the linear walk over the same chain, so the saving is small here and grows with n.

```trace
{"cells":["3","7","12","18","25","31","40","52"],"pointers":["cur","probe"],"steps":[{"at":{"cur":-1,"probe":7},"vars":{"level":3,"cmp":"52 <= 31 false"},"note":"Level 3: key 52 <= 31 fails, so the search drops one level."},{"at":{"cur":-1,"probe":3},"vars":{"level":2,"cmp":"18 <= 31"},"note":"Level 2: key 18 <= 31 holds, so the cursor moves to index 3."},{"at":{"cur":3,"probe":7},"vars":{"level":2,"cmp":"52 <= 31 false"},"note":"Level 2: key 52 <= 31 fails, so the search drops one level."},{"at":{"cur":3,"probe":5},"vars":{"level":1,"cmp":"31 <= 31"},"note":"Level 1: key 31 <= 31 holds, so the cursor moves to index 5."},{"at":{"cur":5,"probe":7},"vars":{"level":1,"cmp":"52 <= 31 false"},"note":"Level 1: key 52 <= 31 fails, so the search drops one level."},{"at":{"cur":5,"probe":6},"vars":{"level":0,"cmp":"40 <= 31 false"},"note":"Level 0: key 40 <= 31 fails, so the search stops here."},{"at":{"cur":5,"probe":5},"vars":{"level":0,"answer":31},"note":"The cursor rests on index 5, so floor(31) is key 31."}]}
```

#### Erase A Present Key

The second trace erases key 18 with a strict comparison, so it stops before any key equal to 18. Level 3 and level 2 leave the cursor at the head. Level 1 moves to key 7. Level 0 moves to key 12. The predecessor on each level is therefore head, head, index 1 and index 2. The level 0 successor of index 2 is key 18, so the node is present. Erase unlinks it on levels 0, 1 and 2, the three levels it occupies.

```trace
{"cells":["3","7","12","18","25","31","40","52"],"pointers":["cur","probe"],"steps":[{"at":{"cur":-1,"probe":7},"vars":{"level":3,"cmp":"52 < 18 false"},"note":"Level 3: key 52 < 18 fails, so the search drops one level."},{"at":{"cur":-1,"probe":3},"vars":{"level":2,"cmp":"18 < 18 false"},"note":"Level 2: key 18 < 18 fails, so the search drops one level."},{"at":{"cur":-1,"probe":1},"vars":{"level":1,"cmp":"7 < 18"},"note":"Level 1: key 7 < 18 holds, so the cursor moves to index 1."},{"at":{"cur":1,"probe":3},"vars":{"level":1,"cmp":"18 < 18 false"},"note":"Level 1: key 18 < 18 fails, so the search drops one level."},{"at":{"cur":1,"probe":2},"vars":{"level":0,"cmp":"12 < 18"},"note":"Level 0: key 12 < 18 holds, so the cursor moves to index 2."},{"at":{"cur":2,"probe":3},"vars":{"level":0,"cmp":"18 < 18 false"},"note":"Level 0: key 18 < 18 fails, so the search stops here."},{"at":{"cur":2,"probe":3},"vars":{"level":0,"unlink":"levels 0,1,2"},"note":"The level 0 successor of index 2 is index 3 with key 18, so erase unlinks index 3 on levels 0, 1 and 2."}]}
```

<!-- stage: code -->
### Search And Splice With An Update Array

The core method descends once and records the predecessor on every level. Insert and erase both reuse it, and the level source is a parameter so a test can fix every height.

```java
final class Layers {
    static final class Node {
        final int key;
        final Node[] next;
        Node(int key, int levels) { this.key = key; this.next = new Node[levels]; }
    }

    static final int MAX = 16;
    final Node head = new Node(0, MAX);
    int top = 1;

    // Fills update with the last node below target on each used level.
    Node descend(int target, Node[] update) {
        Node cur = head;
        for (int l = top - 1; l >= 0; l--) {
            while (cur.next[l] != null && cur.next[l].key < target) cur = cur.next[l];
            update[l] = cur;
        }
        return cur.next[0];
    }

    // Splices a node of the given height after its predecessors.
    void insert(int key, int height) {
        Node[] update = new Node[MAX];
        java.util.Arrays.fill(update, head);
        descend(key, update);
        Node node = new Node(key, height);
        for (int l = 0; l < height; l++) {
            node.next[l] = update[l].next[l];
            update[l].next[l] = node;
        }
        top = Math.max(top, height);
    }

    // Unlinks one node holding key, or returns false when the key is absent.
    boolean erase(int key) {
        Node[] update = new Node[MAX];
        java.util.Arrays.fill(update, head);
        Node hit = descend(key, update);              // hit is the first node with key >= target
        if (hit == null || hit.key != key) return false;
        for (int l = 0; l < hit.next.length; l++) update[l].next[l] = hit.next[l]; // bypass on each level
        return true;
    }

    // Largest stored key at most limit, or -1 when none; keys are non-negative here.
    int floor(int limit) {
        Node cur = head;
        for (int l = top - 1; l >= 0; l--)
            while (cur.next[l] != null && cur.next[l].key <= limit) cur = cur.next[l]; // closed comparison
        return cur == head ? -1 : cur.key;
    }
}
```

The array is pre-filled with the head, so levels above the current top need no special case. The height argument comes from a caller-supplied source, which is a seeded random generator in production and a constant in a test. The strict comparison places an equal key before its existing copies, which is a valid and consistent choice. Erase removes the first copy that the descent reaches.

The expected search cost is O(log n), because each level holds about half the nodes of the level below, so a search crosses about two nodes per level over about log n levels. A run of unlucky coin flips costs O(n) time but still returns a correct answer, because the answer comes from comparing keys.

<!-- stage: applicability -->
### Check Order And Reachability

#### Decide When To Use It

Reach for a layered search when the design needs nearest-key queries with frequent updates and no sorted-set class is available, which is the standalone constraint of this lesson. Typical cases are an interview setting without library collections, an embedded runtime, or a store that must expose its own range scan. Real systems use the same idea, for example the sorted sets of an in-memory database.

#### Guard The Invariant

The invariant to guard is that every level stays sorted and every node on a higher level also sits on level 0. A bug that links a node on level 2 without linking it on level 0 makes it reachable by some searches and invisible to others. Test with fixed heights, including all heights equal to one and all at the maximum.

#### Avoid Two False Friends

Binary search over a linked chain looks like the pattern, because jumping to the middle node halves the range. It breaks the precondition of random access. Reaching the middle node costs a walk of n / 2 links, so the search is O(n) again.

A skip list with a fixed promotion rule, such as every second node of a level, also looks like the pattern. The rule needs evenly spaced nodes, and insertions and removals destroy that spacing. After enough updates one level holds long stretches with no shortcut, and searches fall back toward O(n).

Choose a different tool when keys are small integers in a fixed range, since a Fenwick tree then answers count and rank queries without pointers. Also prefer an ordered map from the library when one exists.

<!-- stage: exercises -->
### Exercises

#### [Build] Layered Linked Search (Author exercise)
<!-- id: dq39-layered-linked-search -->

**Prerequisites.** The level, head and descent steps from this lesson.

**Problem.** Build a class `LayeredLinkedSearch` from a strictly ascending `int[] keys`. The key at index `i` joins `numberOfTrailingZeros(i + 1) + 1` linked levels. The method `floorIndex(long x)` returns the largest index whose key is at most `x`, or `-1` when every key exceeds `x`. The structure is built once and queried many times, with no updates. Calls arrive online, with no advance knowledge.

**Constraints.** The limits are:
- **Keys** number `0 <= n <= 10^5`, are distinct and ascend.
- **Queries** number at most `10^5`, with ratio 0 updates to 10^5 queries.
- **Comparison** is closed, so a key equal to `x` counts as a match.
- **Query value** `x` is any `long`.

**Example 1.** Input keys `[3, 7, 12, 18, 25, 31, 40, 52]` and `x = 31`, output `5`.

**Example 2.** Input the same keys and `x = 2`, output `-1`.

**Hint.** Which level should the search start on, and what condition makes it drop one level instead of stopping?

**Changed decision.** Basic case: search moves right on a sparse level and drops down, with heights fixed by a rule and no updates.

#### [Vary] Design Skiplist (LeetCode 1206)
<!-- id: dq39-design-skiplist -->

**Prerequisites.** The layered search exercise above and the splice code from this lesson.

**Problem.** Design a class `Skiplist` that stores integers and allows duplicates. The method `add(num)` inserts one more copy. The method `search(num)` returns whether at least one copy exists. The method `erase(num)` removes exactly one copy and returns whether a copy existed. The constructor receives an `IntSupplier` that returns the height of each new node, so tests can fix every height. Updates and queries are mixed in roughly equal numbers, and calls arrive online.

**Constraints.** The limits are:
- **Values** are `int` values in `0` to `20000`.
- **Calls** number at most `5 * 10^4` in total, split about evenly between updates and queries.
- **Height** returned by the supplier is clamped to `1` to `16`.
- **Duplicates** are stored as separate nodes.

**Example 1.** Input add(1), add(2), add(3), search(0), add(4), search(1), erase(0), erase(1), search(1), output the five query and erase results `false, true, false, true, false` in order.

**Example 2.** Input add(5), add(5), erase(5), search(5), erase(5), search(5), erase(5), output `true, true, true, false, false`.

**Hint.** When duplicates have different heights, which copy does erase remove, and does it remove that same node on every level?

**Changed decision.** Heights now come from random promotion, and insertion and erase must splice links on every level a node occupies.

#### [Boundary] Duplicate Key Policy (Author exercise)
<!-- id: dq39-duplicate-key-policy -->

**Prerequisites.** The skiplist exercise above.

**Problem.** Design `CountedSkiplist`, a multiset that stores one node per distinct key together with a count. The method `add(key, times)` adds `times` copies. The method `eraseOne(key)` removes one copy and returns whether the key was present. The method `eraseAll(key)` removes every copy and returns the number removed. The method `count(key)` returns the multiplicity and `size()` returns the total over all keys. A node must disappear when its count reaches zero. Updates and queries are mixed evenly, and calls arrive online.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Keys** are `int` values in `0` to `10^9`.
- **Times** is a `long` in `1` to `3 * 10^9`.
- **Counts and size** are `long` values.
- **Absent key** gives `false` for eraseOne and `0` for eraseAll and count.

**Example 1.** Input add(7,3), add(7,2), count(7), eraseOne(7), count(7), eraseAll(7), count(7), output `5, true, 4, 4, 0`.

**Example 2.** Input add(4,2), add(9,1), eraseOne(9), size(), eraseAll(9), eraseOne(4), size(), output `true, 2, 0, true, 1`.

**Hint.** What should happen to the node structure when the count reaches zero, and which type holds a total that exceeds the `int` range?

**Changed decision.** Duplicates become a count on one node, so removal must tell apart lowering a count from unlinking a node.

#### [Recognize] Nearest Keys In A Multiset (Author exercise)
<!-- id: dq39-ordered-multiset-api -->

**Prerequisites.** The duplicate key policy exercise above.

**Problem.** Recognize that `lower(x)` and `floor(x)` are the same descent with limits `x` and `x + 1`, then build `OrderedMultiset` on that single descent. The structure has a fixed capacity of distinct keys and a caller-supplied height source. The method `add(x)` adds one copy. The method `removeOne(x)` removes one copy and returns whether it existed. The method `count(x)` returns the multiplicity. The method `lower(x)` returns the largest stored key strictly below `x`, and `floor(x)` returns the largest stored key at most `x`. Both return `-1` when no such key exists. Store the nodes in parallel arrays addressed by slot index, so the capacity bound is exact. Queries outnumber updates about three to one, calls arrive online, and no library sorted set is available.

**Constraints.** The limits are:
- **Capacity** is at most `10^5` distinct keys at any time.
- **Keys** are `int` values in `0` to `2^31 - 1`.
- **Calls** number at most `4 * 10^5`.
- **Comparison** for `lower` is strict and for `floor` is closed.
- **Removed slots** are reused by later keys.

**Example 1.** Input add(10), add(10), add(30), floor(10), lower(10), lower(31), count(10), output `10, -1, 30, 2`.

**Example 2.** Input add(5), add(8), removeOne(8), floor(100), lower(5), floor(4), output `true, 5, -1, -1`.

**Hint.** Can floor use a strict search with a larger limit, and what happens to that limit for the largest `int` key?

**Changed decision.** The API now needs nearest-key queries on both sides of a key, so one strict descent serves both by shifting the limit.
