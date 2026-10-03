<!-- lesson-kind: standard -->
<!-- lesson-id: key-equality -->
## Key Equality

<!-- stage: context -->
### Addresses Written On Paper Slips

A warehouse stores crates on shelves addressed by an aisle number and a bay number, such as aisle 4, bay 7. Pickers write the address on a paper slip and drop the slip into a tally box whenever they take a crate. At the end of the day the supervisor wants to know which shelf lost the most crates. Two pickers who both took a crate from aisle 4, bay 7 have written two different pieces of paper, but they mean the same shelf, and the supervisor must count them together.

A supervisor who sorted the slips by the identity of the paper would never see a match, since every slip is a different object. A sensible supervisor reads the two numbers on the slip and files by them. The same address written in different handwriting, or the reverse address of aisle 7, bay 4, is a matter of what is written, not of which paper it was written on.

<!-- stage: naive -->
### Keep Slips In A List

A direct version keeps every distinct address as a pair of ints and searches the list for a match each time a crate is taken.

```java
static int mostTakenByList(int[][] takes) {
    List<int[]> addresses = new ArrayList<>();
    List<Integer> counts = new ArrayList<>();
    int best = 0;
    for (int[] t : takes) {
        int at = -1;
        for (int i = 0; i < addresses.size(); i++) {
            if (Arrays.equals(addresses.get(i), t)) { at = i; break; }
        }
        if (at < 0) { addresses.add(t); counts.add(0); at = counts.size() - 1; }
        counts.set(at, counts.get(at) + 1);
        best = Math.max(best, counts.get(at));
    }
    return best;
}
```

On `[[4, 7], [1, 2], [4, 7]]` it returns 2, since the address 4, 7 was taken twice. It compares by content with `Arrays.equals`, which is the right idea.

<!-- stage: bottleneck -->
### A Search Through Every Address Seen

Each take may compare the new address with every distinct address so far, so with `k` distinct addresses the time is O(n * k), which approaches O(n * n) when most takes are from different shelves. The lookup by content is the same job that a hash map does in expected constant time, so the natural repair is a map from address to count.

The tempting repair fails silently. A `HashMap<int[], Integer>` accepts the arrays without complaint, but arrays in Java use identity for `equals` and `hashCode`, so two slips with the same two numbers are different keys. The map grows by one entry per take, every count is 1, and the program reports that no shelf was ever visited twice. The code compiles, runs and gives a wrong answer, which is worse than a crash. What is missing is a key type whose equality is defined by the values it holds.

<!-- stage: insight -->
### Make Equality Depend On The Fields

A **value key** is a key type whose equality and hash code are computed from the values it contains and not from where it lives in memory. In Java the shortest way to write one is a record, such as `record Point(int row, int col) {}`. The compiler generates `equals`, `hashCode` and `toString` from the components, so `new Point(4, 7)` equals any other `new Point(4, 7)` and the two land in the same bucket. With such a key, a `HashMap<Point, Integer>` is a frequency map of coordinates, exactly like the earlier ledgers.

A hash map relies on the **hash contract**. Whenever two keys are equal, they must have equal hash codes. The map computes a hash code to choose a bucket and then calls `equals` inside that bucket, so two equal keys with different hash codes are filed in different buckets and never meet. Records satisfy the contract automatically. A hand-written class must override `equals` and `hashCode` together, using the same fields in both.

<!-- names: value key, hash contract, immutable key -->

The third rule concerns time. An **immutable key** never changes the fields that participate in its hash code while it is stored. If a field changes after insertion, the entry stays in the bucket chosen by the old hash code, but lookups compute the new hash code and search a different bucket, so the entry becomes unreachable by lookup while still counting toward the size and appearing in iteration. Records are immutable by construction, which is the main reason to prefer them.

Keys can also be normalised before they are stored. If an edge between `a` and `b` is the same as an edge between `b` and `a`, store the pair in a fixed order, smallest first, so that both spellings become one key. If the direction matters, store the pair as written, so that `(a, b)` and `(b, a)` stay different. The choice is a decision about meaning, and it belongs in the sentence that describes the key.

<!-- stage: variables -->
### A Compound Key And What It Means

The key is built from one or more fields, and the lesson's rule is that those fields are the whole identity of the thing being counted or tested. The value is a count, a flag or a position, as in the earlier lessons. A normalising step may reorder the fields before the key is created. The key object is created fresh for each observation, which is cheap, and it is never modified after it has been put into a map or set. When a field must change, create a new key and remove the old one, never edit the stored one.

<!-- stage: trace -->
### Counting Coordinates And Merging Edges

```trace
{"cells":["1,2","3,4","1,2","1,2","3,4","0,0"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"point":"(1,2)","count":1,"repeated":0},"note":"Observation (1,2) becomes a Point key. Its count is now 1. Counts: (1,2) 1."},{"at":{"i":1},"vars":{"point":"(3,4)","count":1,"repeated":0},"note":"Observation (3,4) becomes a Point key. Its count is now 1. Counts: (1,2) 1, (3,4) 1."},{"at":{"i":2},"vars":{"point":"(1,2)","count":2,"repeated":1},"note":"Observation (1,2) becomes a Point key. Its count is now 2. Counts: (1,2) 2, (3,4) 1."},{"at":{"i":3},"vars":{"point":"(1,2)","count":3,"repeated":1},"note":"Observation (1,2) becomes a Point key. Its count is now 3. Counts: (1,2) 3, (3,4) 1."},{"at":{"i":4},"vars":{"point":"(3,4)","count":2,"repeated":2},"note":"Observation (3,4) becomes a Point key. Its count is now 2. Counts: (1,2) 3, (3,4) 2."},{"at":{"i":5},"vars":{"point":"(0,0)","count":1,"repeated":2},"note":"Observation (0,0) becomes a Point key. Its count is now 1. Counts: (1,2) 3, (3,4) 2, (0,0) 1."}]}
```

Take the observations (1,2), (3,4), (1,2), (1,2), (3,4) and (0,0). Each one becomes a `Point` record, and the map treats equal points as one key. The count for (1,2) rises to 1, 2 and then 3 as its three observations arrive, while (3,4) reaches 2 and (0,0) stays at 1. The most frequent coordinate has count 3, and two coordinates were observed at least twice.

```trace
{"cells":["5-4","4-5","3-3","4-5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"edge":"(5,4)","key":"(4,5)","size":1},"note":"Edge (5,4) is normalised to the key (4,5). It is new, so the set grows. Size: 1."},{"at":{"i":1},"vars":{"edge":"(4,5)","key":"(4,5)","size":1},"note":"Edge (4,5) is normalised to the key (4,5). It is already stored, so the set does not change. Size: 1."},{"at":{"i":2},"vars":{"edge":"(3,3)","key":"(3,3)","size":2},"note":"Edge (3,3) is normalised to the key (3,3). It is new, so the set grows. Size: 2."},{"at":{"i":3},"vars":{"edge":"(4,5)","key":"(4,5)","size":2},"note":"Edge (4,5) is normalised to the key (4,5). It is already stored, so the set does not change. Size: 2."}]}
```

The second trace merges undirected edges. The edges (5,4), (4,5), (3,3) and (4,5) are written with the smaller endpoint first, so the first, second and fourth all become the key (4,5), and (3,3) is its own key. The set grows to size 1 after the first edge, stays at 1 after the second, grows to 2 for the loop, and stays at 2 after the last edge. Without the normalising step the first two edges would count as two different keys.

<!-- stage: code -->
### Records As Keys

```java
final class KeyExamples {
    record Point(int row, int col) {}

    record Pair(int from, int to) {}

    static int repeatedCoordinates(int[][] observations) {
        Map<Point, Integer> count = new HashMap<>();
        for (int[] o : observations) count.merge(new Point(o[0], o[1]), 1, Integer::sum);
        int repeated = 0;
        for (int c : count.values()) if (c >= 2) repeated++;
        return repeated;
    }

    static int distinctUndirectedEdges(int[][] edges) {
        Set<Pair> seen = new HashSet<>();
        for (int[] e : edges) {
            seen.add(new Pair(Math.min(e[0], e[1]), Math.max(e[0], e[1])));   // normalise: smaller endpoint first
        }
        return seen.size();
    }

    static int mostRepeatedTransition(int[] states) {
        Map<Pair, Integer> count = new HashMap<>();
        int best = 0;
        for (int i = 0; i + 1 < states.length; i++) {
            best = Math.max(best, count.merge(new Pair(states[i], states[i + 1]), 1, Integer::sum));
        }
        return best;
    }
}
```

Each method makes one pass with one small allocation per observation, which gives expected O(n) time and O(k) space for `k` distinct keys. `merge` returns the new count, which `mostRepeatedTransition` uses to track the maximum without a second pass. The records need no extra code for equality, and the normalisation in `distinctUndirectedEdges` turns two spellings of the same edge into one key.

<!-- stage: applicability -->
### When The Key Has Several Parts

Use a value key when the thing being counted, grouped or tested is described by several fields, such as a coordinate, a pair of states or a small application object. The invariant to remember is that equal logical keys have equal hash codes, and that the fields that decide equality never change while the key is stored.

The false friend is the array. An `int[]` or other array looks like a natural coordinate pair, but it uses identity equality, so a map keyed by arrays never finds an existing entry. A related false friend is a hand-built string such as `"4,7"`, which works but costs allocation, parsing and the risk of ambiguous separators, and a record states the intent better. Packing two small ints into one `long` is a legitimate optimisation when the bounds are known, but it needs an explicit contract for the range of each field.

Java-specific hazards are the reason this lesson exists. Overriding only `equals` without `hashCode` breaks the contract. Overriding both on a mutable class and then changing a field inside a map breaks reachability. Using `==` on keys compares identity. Prefer records, keep keys immutable, and if you write `equals` by hand, derive `hashCode` from exactly the same fields, for example with `Objects.hash`.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Coordinates (Author exercise)
<!-- id: hm-count-coordinates -->

**Prerequisites.** Frequency maps lesson; the value key in this lesson.

**Problem.** Each observation is a row and a column. Return the number of distinct coordinates that were observed at least twice. Use a record as the key.

**Constraints.** 0 <= observations.length <= 10^5, and rows and columns lie in -10^6..10^6. Each observation is an array of two ints.

**Example 1.** Input `observations = [[1, 2], [3, 4], [1, 2], [1, 2], [3, 4], [0, 0]]`, output 2.

**Example 2.** Input `observations = [[1, 2], [2, 1]]`, output 0, since swapping the fields gives a different coordinate.

**Hint.** What goes wrong if each observation array is used directly as a map key? Which field values decide whether two observations are the same?

**Changed decision.** First rung: the key is a compound value, so equality has to be defined by its fields.

#### [Vary] Undirected Edge Key (Author exercise)
<!-- id: hm-undirected-edge-key -->

**Prerequisites.** The build exercise above.

**Problem.** Each edge is a pair of endpoints, and an edge from `a` to `b` is the same edge as one from `b` to `a`. Return the number of distinct edges. A loop from a vertex to itself is a valid edge.

**Constraints.** 0 <= edges.length <= 10^5 and endpoints lie in 0..10^9. Normalise every pair to a fixed order before inserting it.

**Example 1.** Input `edges = [[1, 2], [2, 1], [3, 3], [2, 3]]`, output 3.

**Example 2.** Input `edges = [[5, 4], [4, 5], [5, 4]]`, output 1.

**Hint.** What fixed order makes both spellings of an edge identical? What happens to a loop under that order?

**Changed decision.** The meaning of equality is widened, so the key is normalised before it is stored.

#### [Boundary] Mutable-Key Failure (Author exercise)
<!-- id: hm-mutable-key-failure -->

**Prerequisites.** The two exercises above.

**Problem.** A key class has one mutable field `x`, and its `equals` and `hashCode` both use `x`. Insert a key with `x = start` into a `HashMap`, then change the field to `changed`. Return two booleans: whether `containsKey` finds the key afterwards, and whether the entry can still be found by scanning the entries. Explain why they can differ.

**Constraints.** 0 <= start, changed <= 1000. The map is a plain `HashMap` that has not been resized. Do not remove or re-insert the key.

**Example 1.** Input `start = 3`, `changed = 8`, output `[false, true]`.

**Example 2.** Input `start = 3`, `changed = 3`, output `[true, true]`, because an unchanged field leaves the hash code alone.

**Hint.** Which bucket was the entry filed in, and which bucket does a lookup of the changed key search?

**Changed decision.** The question is not how to store a key but what happens to a stored key whose identity changes.

#### [Recognize] Count Directed Transitions (Author exercise)
<!-- id: hm-directed-transitions -->

**Prerequisites.** All three exercises above.

**Problem.** Given a sequence of states, consider each consecutive pair `(from, to)` as a transition. Return the largest number of times any one directed transition occurs. A transition from `a` to `b` is different from one from `b` to `a`. Sequences shorter than two states have no transitions.

**Constraints.** 0 <= states.length <= 10^5 and states lie in -10^9..10^9. Use an immutable pair as the key and do not normalise.

**Example 1.** Input `states = [1, 2, 1, 3, 1, 2]`, output 2, from the transition 1 to 2.

**Example 2.** Input `states = [4, 9, 4]`, output 1, because 4 to 9 and 9 to 4 are different keys.

**Hint.** Which of the previous exercises needs the order of the fields to matter, and which needs it ignored?

**Changed decision.** Direction is part of the identity, so the key keeps its fields in the order they were read.
