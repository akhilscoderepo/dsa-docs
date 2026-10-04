<!-- lesson-kind: standard -->
<!-- lesson-id: key-equality -->
## Use Records As Keys

<!-- stage: context -->
### Orders Counted Per Delivery Cell

A delivery service splits a city into a grid and logs one pair `(row, col)` for each order. The dispatcher wants to know the largest number of orders that fall into a single grid cell. The first attempt stores each pair as an `int[]` of two entries in a map, and the dispatcher sees a count of 1 for every cell. Some cells have a hundred orders. The counts are wrong, although every pair holds the right numbers.

The values are right and the program still fails. The first question is what makes two keys the same key in a Java map. The second question is how to build a key from several numbers so that equal pairs find one entry.

<!-- stage: naive -->
### Searching A List Of Distinct Cells

The direct method avoids the map. It keeps a list of the distinct cells found so far with a count for each. For every order it scans the list for the same pair, adds one to the count when it finds the pair, and appends a new entry otherwise.

```java
static int busiestCell(int[][] orders) {
    List<int[]> cells = new ArrayList<>();
    List<Integer> counts = new ArrayList<>();
    int best = 0;
    for (int[] order : orders) {
        int at = -1;
        for (int k = 0; k < cells.size(); k++) {
            if (cells.get(k)[0] == order[0] && cells.get(k)[1] == order[1]) {
                at = k;
                break;
            }
        }
        if (at == -1) {
            cells.add(order);
            counts.add(1);
            at = counts.size() - 1;
        } else {
            counts.set(at, counts.get(at) + 1);
        }
        best = Math.max(best, counts.get(at));
    }
    return best;
}
```

On `[[1, 2], [0, 0], [1, 2], [2, 1], [1, 2]]` the method returns 3, because the cell `(1, 2)` occurs three times.

<!-- stage: bottleneck -->
### Each Order Scans Every Distinct Cell

```predict
The log holds 100000 orders and 50000 distinct cells. Roughly how many pair comparisons does the method make, and what does a map promise that this scan does not?

Each order scans the list of distinct cells found so far, which holds up to 50000 entries, so the method makes about n * d = 5 billion comparisons, which is O(n * d). A map finds the entry for a key in expected constant time and needs no scan.
```

The scan looks for one entry whose pair equals the current pair. A map performs that search in expected constant time, but only if the map considers two pairs equal exactly when their numbers are equal. The cost drops from O(n * d) to O(n), but only if the key type has the right idea of equality. The `int[]` attempt from the opening shows that this idea is not automatic.

<!-- stage: insight -->
### Make Equal Pairs Find One Entry

#### What A Map Does With A Key

A hash map first computes the `hashCode` of a key to choose where to look. It then compares keys with `equals` to confirm the match. Two keys that mean the same cell must have equal hash codes, and `equals` must report them as equal. This agreement is **logical equality**: two keys are equal when their contents are equal, whatever object holds them.

<!-- names: logical equality, hashCode contract, record -->

#### Arrays Compare By Identity

```predict
A program stores `new int[] {1, 2}` as a key and then looks up another array `new int[] {1, 2}`. What does the lookup return?

The lookup returns null. An array compares by identity, and the second array is a different object, so it is not equal to the first even though both hold 1 and 2. The map treats the two arrays as two keys.
```

The method `equals` of an array compares object identity. Two arrays with the same contents are two different keys, and each insert creates a new entry. This explains the count of 1 in the opening problem. A `List<Integer>` compares contents, but a record is simpler for a fixed pair.

#### A Record Supplies Both Methods

A **record** declares an immutable value type. The declaration `record Point(int row, int col) {}` generates `equals` and `hashCode` from its components. Two points with equal `row` and equal `col` are equal and have equal hash codes. This is the **hashCode contract**: keys that are equal must produce the same hash code. A record keeps the contract automatically, so a `Map<Point, Integer>` counts cells correctly.

#### Keys Must Not Change While Stored

The map stores the hash code at insertion time. If a field that takes part in `equals` and `hashCode` changes after insertion, the entry sits under its old hash code. A lookup with the new contents looks in another place. The entry becomes unreachable, although it still occupies space. The fields of a record are final, so records cannot break this rule. A mutable class used as a key can.

<!-- stage: variables -->
### Key, Record And Counts

The counting loop uses three values.

- **Point** is the record `Point(row, col)` that serves as the key.
- **counts** maps each distinct point to its number of orders and gains one increment per order.
- **best** holds the largest count seen so far and changes only when an increment exceeds it.

<!-- stage: trace -->
### Counting Cells And Merging Edges

#### Counting Orders Per Cell

Take the orders `(1, 2), (0, 0), (1, 2), (2, 1), (1, 2)`. The first order creates the entry for `(1, 2)` with count 1. The second creates `(0, 0)`. The third finds `(1, 2)`, because a new `Point(1, 2)` equals the stored point, and raises it to 2. The fifth order raises it to 3. The answer is 3.

#### Making The Key Order Independent

A second task counts connections between two nodes where the connection `(a, b)` and the connection `(b, a)` are the same. The loop first builds the key with the smaller number first, so `(3, 1)` becomes `(1, 3)`. Take `(3, 1), (1, 3), (2, 5), (5, 2), (3, 1)`. The normalized keys are `(1, 3)`, `(1, 3)`, `(2, 5)`, `(2, 5)` and `(1, 3)`, so the map holds `(1, 3)` with 3 and `(2, 5)` with 2.

#### Stepping Through Both Lists

```trace
{"cells":["(1,2)","(0,0)","(1,2)","(2,1)","(1,2)"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"counts":"{}"},"note":"Start: the map is empty."},{"at":{"i":0},"vars":{"key":"(1,2)","counts":"{(1,2): 1}"},"note":"Order (1, 2). The key is new, so create its entry."},{"at":{"i":1},"vars":{"key":"(0,0)","counts":"{(1,2): 1, (0,0): 1}"},"note":"Order (0, 0). The key is new, so create its entry."},{"at":{"i":2},"vars":{"key":"(1,2)","counts":"{(1,2): 2, (0,0): 1}"},"note":"Order (1, 2). A new Point equals the stored key, so its count rises to 2."},{"at":{"i":3},"vars":{"key":"(2,1)","counts":"{(1,2): 2, (0,0): 1, (2,1): 1}"},"note":"Order (2, 1). The key is new, so create its entry."},{"at":{"i":4},"vars":{"key":"(1,2)","counts":"{(1,2): 3, (0,0): 1, (2,1): 1}"},"note":"Order (1, 2). A new Point equals the stored key, so its count rises to 3."}]}
```

```trace
{"cells":["(3,1)","(1,3)","(2,5)","(5,2)","(3,1)"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"counts":"{}"},"note":"Start: the map is empty."},{"at":{"i":0},"vars":{"key":"(1,3)","counts":"{(1,3): 1}"},"note":"Pair (3, 1) becomes the key (1, 3). The key is new, so create its entry."},{"at":{"i":1},"vars":{"key":"(1,3)","counts":"{(1,3): 2}"},"note":"Pair (1, 3) becomes the key (1, 3). The entry exists, so its count rises to 2."},{"at":{"i":2},"vars":{"key":"(2,5)","counts":"{(1,3): 2, (2,5): 1}"},"note":"Pair (2, 5) becomes the key (2, 5). The key is new, so create its entry."},{"at":{"i":3},"vars":{"key":"(2,5)","counts":"{(1,3): 2, (2,5): 2}"},"note":"Pair (5, 2) becomes the key (2, 5). The entry exists, so its count rises to 2."},{"at":{"i":4},"vars":{"key":"(1,3)","counts":"{(1,3): 3, (2,5): 2}"},"note":"Pair (3, 1) becomes the key (1, 3). The entry exists, so its count rises to 3."}]}
```

<!-- stage: code -->
### A Record As The Map Key

#### Counting Orders With A Record

```java
final class Cells {
    record Point(int row, int col) {}

    static int busiestCell(int[][] orders) {
        Map<Point, Integer> counts = new HashMap<>();
        int best = 0;
        for (int[] order : orders) {
            Point p = new Point(order[0], order[1]);
            int now = counts.merge(p, 1, Integer::sum);
            best = Math.max(best, now);
        }
        return best;
    }
}
```

#### What The Method Costs

The loop creates one record and makes one map operation for each order, so the expected time is O(n). The map holds one entry per distinct cell, so the space is O(d). The call `merge(p, 1, Integer::sum)` stores 1 for a new key and otherwise adds 1 to the stored count. It returns the new count, which the loop compares with `best`. The record `Point` sits inside the same class as the method.

<!-- stage: applicability -->
### When The Key Has Several Parts

#### Look For Coordinates And Pairs

Use a record key when the thing to look up consists of several values, such as a grid coordinate, a pair of node numbers, or a state with two fields. The invariant has two parts. Equal logical keys have equal hash codes. No field that takes part in equality changes while the key is stored. Normalize the key before insertion when the meaning ignores some difference, such as the order of the two ends of an edge.

#### A Delimited String Is A False Friend

A false friend here is a string such as `row + "," + col` used as the key. It works, but each lookup builds a new string and the code must trust the delimiter. A mistake such as `"1" + "11"` against `"11" + "1"` merges different pairs when the delimiter is missing. A record states the fields and needs no parsing.

#### Java Details That Cause Failures

An array used as a key compares by identity, so use a record or a `List`. A class with its own `equals` must also define `hashCode` with the same fields. A record gives both. A mutable key must not change while it sits in a map, so build the key at the moment of insertion and do not reuse and edit one key object.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Coordinates (Author exercise)
<!-- id: hm-count-coordinates -->

**Prerequisites.** The record key and the counting loop from this lesson.

**Problem.** Let `orders` be an array of pairs `{row, col}`. Return the largest number of entries of `orders` that are equal to each other. Return 0 for an empty array. Use the record `Point(int row, int col)` as the key.

**Constraints.** The limits are:
- **Length** satisfies `0 <= orders.length <= 10^5`.
- **Coordinates** satisfy `-10^9 <= row, col <= 10^9`.
- **Pairs** are arrays with exactly two entries, and the method does not change them.
- **Answer** is an `int` from 0 to `orders.length`.

**Example 1.** Input `orders = [[4, 4], [4, 5], [5, 4], [4, 4]]`, output 2.

**Example 2.** Input `orders = [[0, 1], [1, 0]]`, output 1, because the pairs `(0, 1)` and `(1, 0)` differ.

**Hint.** What must the key hold so that two orders at the same cell find one entry?

**Changed decision.** Basic case: the key has two fields, and the record supplies equality.

#### [Vary] Undirected Edge Key (Author exercise)
<!-- id: hm-undirected-edge -->

**Prerequisites.** Count Coordinates above.

**Problem.** Let `edges` be an array of pairs `{a, b}` that name connections between two nodes. The connections `(a, b)` and `(b, a)` are the same. Return the number of distinct connections.

**Constraints.** The limits are:
- **Length** satisfies `0 <= edges.length <= 10^5`.
- **Nodes** are integers with `|a|, |b| <= 10^9`, and `a == b` is legal.
- **Normalization** puts the smaller node first, ahead of the key construction.
- **Answer** is an `int` from 0 to `edges.length`.

**Example 1.** Input `edges = [[1, 2], [2, 1], [2, 3], [3, 2], [1, 2]]`, output 2.

**Example 2.** Input `edges = [[7, 7], [7, 7]]`, output 1.

**Hint.** If two inputs mean the same edge, what should the program do to them before it builds the key?

**Changed decision.** The key is normalized before insertion, so two orders of one pair give one key.

#### [Boundary] Mutable-Key Failure (Author exercise)
<!-- id: hm-mutable-key -->

**Prerequisites.** The two exercises above and the rule about stored keys from this lesson.

**Problem.** A walker starts at `(0, 0)` and reads a string of moves. The move `'U'` adds 1 to `row`, `'D'` subtracts 1, `'R'` adds 1 to `col` and `'L'` subtracts 1. Return the number of distinct positions the walker occupies, including the start. The walker keeps its position in one mutable `int[2]`.

**Constraints.** The limits are:
- **Moves** has length `0 <= moves.length() <= 10^5` and holds only `'U'`, `'D'`, `'L'` and `'R'`.
- **Position** array is one object that the loop edits in place.
- **Key** built from the position must not change after insertion.
- **Answer** is an `int` from 1 to `moves.length() + 1`.

**Example 1.** Input `moves = "RULD"`, output 4, because the walker returns to the start.

**Example 2.** Input `moves = ""`, output 1.

**Hint.** What would the set hold if the program inserted the position array itself after each move?

**Changed decision.** The program builds a fresh immutable key from the current position at each insertion.

#### [Recognize] Count Directed Transitions (Author exercise)
<!-- id: hm-directed-transitions -->

**Prerequisites.** All three exercises above.

**Problem.** Let `states` be an integer array that records the states of a system over time. A transition is a pair of neighbors `(states[i], states[i + 1])`. Return the largest number of times one transition occurs. The transition `(a, b)` differs from `(b, a)`. Return 0 when `states` has fewer than two entries.

**Constraints.** The limits are:
- **Length** satisfies `0 <= states.length <= 10^5`.
- **Values** are 32-bit integers.
- **Key** is an immutable `Pair(from, to)` record.
- **Answer** is an `int` from 0 to `states.length - 1`.

**Example 1.** Input `states = [1, 2, 1, 2, 2, 1]`, output 2, for the transitions `(1, 2)` and `(2, 1)`.

**Example 2.** Input `states = [5]`, output 0.

**Hint.** Which exercise above normalized the key, and why must this exercise leave the order as it is?

**Changed decision.** The key keeps its order, so the two directions stay different entries.
