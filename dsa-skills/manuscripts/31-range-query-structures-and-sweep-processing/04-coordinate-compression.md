<!-- lesson-kind: standard -->
<!-- lesson-id: coordinate-compression -->
## Coordinate Compression

<!-- stage: context -->
### Why Huge Values Break Array Indexing

A service logs the response time of each request in microseconds. Values reach one billion, yet a log batch holds only a few thousand requests. For every new request, the service must report how many earlier requests were faster. A counting array indexed by the value would need one billion slots, which is about 4 GB of `int` counters, to track a few thousand entries. Negative values or `long` values make the array impossible to build at all.

The question is how to keep a counting structure small when the values are huge or sparse. The answer depends on one observation. A count of "values below x" depends only on the order of the values and on which ones are equal. The actual magnitudes never enter the answer.

<!-- stage: naive -->
### Using The Value As The Index

The direct approach allocates an array large enough to be indexed by the value itself, then counts by scanning it.

```java
static int countBelow(int[] seenValues, int x) {
    int[] present = new int[1_000_000_001];   // one slot per possible value
    for (int v : seenValues) present[v]++;     // the value is used as the index
    int below = 0;
    for (int v = 0; v < x; v++) below += present[v];
    return below;
}
```

For values up to one billion, this method allocates about 4 GB on every call. It also scans up to a billion slots to answer one query. Values such as -5 throw `ArrayIndexOutOfBoundsException`.

<!-- stage: bottleneck -->
### Memory And Scan Follow The Value Range

```predict
A batch has 5,000 requests with response times up to 10^9. You want counts of earlier requests below each value. How many counting slots do you actually need?

Only 5,000 slots at most, one for each distinct value. The counts depend on the order of the values and not on their size, so the other billion slots never hold anything.
```

#### Measure The Wasted Space

The array in the naive method has `V + 1` slots, where `V` is the largest value. Space is O(V) and a single query scans O(V) slots. With `V = 10^9`, a batch of `n = 5,000` values uses a number of slots 200,000 times larger than `n`. Almost every slot stays at zero.

#### Spot What The Answer Needs

Take the values 7, 40 and 1,000,000. The count of values below 40 is 1. It stays 1 if the values become 2, 3 and 4. Only two facts about the data affect any count: which value is smaller than which, and which values are equal. Memory should therefore depend on the number of distinct values, which is at most `n`, and not on `V`.

<!-- stage: insight -->
### Replace Each Value By Its Position

#### Build The Table Of Distinct Values

**Coordinate compression** replaces each value by a small integer that keeps the order of the original values. Copy the values, sort the copy and remove duplicates. The result is a **rank table**, a sorted array with no repeated value. Position `p` in the table holds the `(p + 1)`-th smallest distinct value.

<!-- names: coordinate compression, rank table, dense rank -->

#### Look Up The Dense Rank

The **dense rank** of a value is its position in the rank table plus one, so ranks run from 1 to `m` with no gaps, where `m` is the number of distinct values. A binary search in the table finds the rank in O(log m) time. Equal values share one rank, and a smaller value always gets a smaller rank.

The mapping preserves exactly what counting needs. For two values `a` and `b`, `a < b` holds exactly when `rank(a) < rank(b)`, and `a == b` holds exactly when the ranks are equal. A structure indexed by rank therefore returns the same counts as one indexed by value, using only `m` slots.

The invariant of this method is that the table is sorted and free of duplicates. Binary search is only correct under that condition, and the dense ranks are only gap-free under it.

<!-- stage: variables -->
### Quantities Held During Compression

These items describe the state of one compression.

- **values** holds the original input, which stays unchanged.
- **table** holds the sorted distinct values, with `m` entries.
- **rank** is the 1-based position of a value in `table`, found by binary search.
- **m** is the number of distinct values, and the largest rank.

Once ranks feed a Fenwick tree, the tree has `m` positions. A value of rank `r` is stored at external position `r - 1`. A call to `prefix(r - 1)` then counts the values with rank below `r`, and `prefix(r)` counts values with rank up to `r`.

<!-- stage: trace -->
### Compress Seven Values Step By Step

The input is 900, -5, 1000000000, 900, 42, -5 and 7. Sorting removes the duplicates 900 and -5 and leaves five distinct values.

#### Rank Each Value With The Table

The table is -5, 7, 42, 900 and 1000000000, so `m = 5`. The first 900 searches the table and lands at position 3, so its rank is 4. The value -5 lands at position 0, which gives rank 1, and one billion lands at the last position, which gives rank 5.

The second 900 lands at position 3 again, so it receives rank 4 once more. The repeated -5 also receives its earlier rank 1. This repeat is the hardest step, because equal values must return equal ranks. The table holds each value once, so every search for that value ends at the same position.

```trace
{"cells":[900,-5,1000000000,900,42,-5,7],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"m":5},"note":"Sorting and removing duplicates gives the table [-5, 7, 42, 900, 1000000000] with 5 distinct values."},{"at":{"i":0},"vars":{"value":900,"position":3,"rank":4},"note":"The value 900 sits at table position 3, so its rank is 4."},{"at":{"i":1},"vars":{"value":-5,"position":0,"rank":1},"note":"The value -5 sits at table position 0, so its rank is 1."},{"at":{"i":2},"vars":{"value":1000000000,"position":4,"rank":5},"note":"The value 1000000000 sits at table position 4, so its rank is 5."},{"at":{"i":3},"vars":{"value":900,"position":3,"rank":4},"note":"The value 900 sits at table position 3, so its rank is 4."},{"at":{"i":4},"vars":{"value":42,"position":2,"rank":3},"note":"The value 42 sits at table position 2, so its rank is 3."},{"at":{"i":5},"vars":{"value":-5,"position":0,"rank":1},"note":"The value -5 sits at table position 0, so its rank is 1."},{"at":{"i":6},"vars":{"value":7,"position":1,"rank":2},"note":"The value 7 sits at table position 1, so its rank is 2."}]}
```

#### Count Smaller Values With A Fenwick Tree

The next input is the instruction order 8, 2, 5, 5, 9, 1, 5. Each value is first compressed, then counted against the values inserted before it. The cost of an insertion is the smaller of two counts: the inserted values strictly below it and the inserted values strictly above it.

The table is 1, 2, 5, 8 and 9. The third value, 5, arrives after 8 and 2, so one value lies below it and one lies above it. The fourth value, 5, finds the earlier 5 in neither count, because the counts are strict. That strict comparison is the step to watch, since `prefix(r)` would include the equal value and `prefix(r - 1)` does not.

```trace
{"cells":[8,2,5,5,9,1,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"m":5,"total":0},"note":"The table is [1, 2, 5, 8, 9], so the tree has 5 positions and starts empty."},{"at":{"i":0},"vars":{"rank":4,"less":0,"greater":0,"cost":0,"total":0},"note":"The value 8 has rank 4. 0 earlier values are below it and 0 are above it, so the cost is 0 and the total is 0."},{"at":{"i":1},"vars":{"rank":2,"less":0,"greater":1,"cost":0,"total":0},"note":"The value 2 has rank 2. 0 earlier values are below it and 1 are above it, so the cost is 0 and the total is 0."},{"at":{"i":2},"vars":{"rank":3,"less":1,"greater":1,"cost":1,"total":1},"note":"The value 5 has rank 3. 1 earlier values are below it and 1 are above it, so the cost is 1 and the total is 1."},{"at":{"i":3},"vars":{"rank":3,"less":1,"greater":1,"cost":1,"total":2},"note":"The value 5 has rank 3. 1 earlier values are below it and 1 are above it, so the cost is 1 and the total is 2."},{"at":{"i":4},"vars":{"rank":5,"less":4,"greater":0,"cost":0,"total":2},"note":"The value 9 has rank 5. 4 earlier values are below it and 0 are above it, so the cost is 0 and the total is 2."},{"at":{"i":5},"vars":{"rank":1,"less":0,"greater":5,"cost":0,"total":2},"note":"The value 1 has rank 1. 0 earlier values are below it and 5 are above it, so the cost is 0 and the total is 2."},{"at":{"i":6},"vars":{"rank":3,"less":2,"greater":2,"cost":2,"total":4},"note":"The value 5 has rank 3. 2 earlier values are below it and 2 are above it, so the cost is 2 and the total is 4."}]}
```

<!-- stage: code -->
### Build The Table And Look Up Ranks

```java
static long[] buildTable(long[] values) {
    long[] copy = values.clone();              // keep the input unchanged
    Arrays.sort(copy);                         // sorting costs O(n log n)
    int m = 0;
    for (int i = 0; i < copy.length; i++) {
        if (i == 0 || copy[i] != copy[i - 1]) copy[m++] = copy[i];   // keep first of each run
    }
    return Arrays.copyOf(copy, m);             // the table holds m distinct values
}

static int rank(long[] table, long value) {
    int pos = Arrays.binarySearch(table, value);   // O(log m) lookup
    return pos < 0 ? 0 : pos + 1;                  // 0 means the value is absent
}
```

The first method sorts a copy and writes each first-of-run value forward, which removes duplicates in one pass. The comparison uses `!=` on `long` values, so no subtraction occurs and no overflow can happen. The second method turns a table position into a 1-based rank and reports 0 for an absent value. Together they cost O(n log n) to build and O(log m) per lookup.

<!-- stage: applicability -->
### When To Compress Coordinates

#### Recognize The Pattern

Compress when the values are sparse, huge or negative, and the question depends only on order and equality. Typical cases are counting smaller earlier values with a Fenwick tree, counting inversions, and sweeping over interval endpoints. The invariant to protect is that the table is sorted without duplicates, and that every query value either appears in the table or is handled as absent.

#### Avoid The False Friend

Compression is not a way to shrink values that take part in arithmetic. If the answer sums, subtracts or multiplies the values themselves, ranks lose the information. A false friend of compression is the sorted position of each element, where equal values receive different positions. That variant breaks every equality test, so counts that treat ties as equal go wrong.

#### Watch The Java Hazards

Comparing with subtraction such as `(int) (a - b)` overflows for values near the ends of the `long` range. Use `Long.compare` or `Arrays.sort` on a primitive array. Do not use a value as an array index unless its range is small and non-negative. Compression is also an offline technique, since the table needs all values before the first query.

<!-- stage: exercises -->
### Exercises

#### [Build] Compress Distinct Values (Author exercise)
<!-- id: rq31-compress-distinct -->

**Prerequisites.** The rank table and dense rank from this lesson.

**Problem.** Given an array `values` of integers and an array `queries` of integers, build the sorted array of distinct values in `values`. Return, for each query, the 1-based position of that query in the sorted distinct array, or 0 when the query does not occur in `values`.

**Constraints.** The limits are:
- **`values`** has `0 <= length <= 10^5` entries, each an `int`.
- **`queries`** has `0 <= length <= 10^5` entries, each an `int`.
- **Result** is an `int[]` with one entry per query, and `values` stays unmodified.

**Example 1.** Input values 40, 7, 40, 1000000, 7 and queries 7, 1000000, 5. Output 1, 3, 0.

**Example 2.** Input values 3, 3, 3, 3 and queries 3, 4. Output 1, 0, since only one distinct value exists.

**Hint.** After sorting and removing duplicates, which search finds the position of a query?

**Changed decision.** Baseline case: builds the table and the lookup that later exercises reuse.

#### [Vary] Preserve Equal Ranks (Author exercise)
<!-- id: rq31-equal-ranks -->

**Prerequisites.** The exercise above.

**Problem.** Given an array `values`, return an array `ranks` of the same length where `ranks[i]` is the dense rank of `values[i]`. The dense rank of a value is 1 plus the number of distinct values in `values` that are strictly smaller. Equal values must receive equal ranks.

**Constraints.** The limits are:
- **`values`** has `0 <= length <= 10^5` entries, each an `int`.
- **Ranks** start at 1 and have no gaps up to the number of distinct values.
- **Result** keeps the input order, and `values` stays unmodified.

**Example 1.** Input 100, 5, 100, 70, 5. Output 3, 1, 3, 2, 1.

**Example 2.** Input 8, 8, 8. Output 1, 1, 1, since all values are equal.

**Hint.** Which value does a rank count: every earlier element, or every distinct smaller value?

**Changed decision.** Query values are replaced by the input itself, and equal values must share one rank.

#### [Boundary] Negative And Extreme Values (Author exercise)
<!-- id: rq31-extreme-values -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `values` of `long` integers that may be negative, zero, `Long.MIN_VALUE` or `Long.MAX_VALUE`, return the dense rank of each element as defined in the previous exercise. The comparison of two values must be correct for the full `long` range.

**Constraints.** The limits are:
- **`values`** has `0 <= length <= 10^5` entries, each a `long`.
- **Comparison** may not use subtraction, and no value may serve as an array index.
- **Result** is an `int[]` in input order.

**Example 1.** Input Long.MAX_VALUE, -1, Long.MIN_VALUE, 0, -1. Output 4, 2, 1, 3, 2.

**Example 2.** Input an empty array. Output an empty array.

**Hint.** What does `Long.MAX_VALUE - Long.MIN_VALUE` evaluate to in Java?

**Changed decision.** The value range widens to the full `long` range, so the comparison itself must be safe.

#### [Recognize] Create Sorted Array Cost (LeetCode 1649)
<!-- id: rq31-sorted-array-cost -->

**Prerequisites.** The three exercises above and the Fenwick tree lesson.

**Problem.** An initially empty container receives the elements of `instructions` in order. Inserting an element costs the smaller of two counts: the elements already in the container that are strictly less than it, and those that are strictly greater. Return the total cost of all insertions modulo 1,000,000,007.

**Constraints.** The limits are:
- **`instructions`** has `1 <= length <= 10^5` entries.
- **Each element** is an `int` with `1 <= element <= 10^9`.
- **Equal elements** count in neither the less count nor the greater count.
- **Result** is returned modulo 1,000,000,007 as a `long`.

**Example 1.** Input 4, 9, 4, 1, 7, 7. Output 2. The costs are 0, 0, 0, 0, 1, 1.

**Example 2.** Input 3, 3, 3, 3. Output 0, since no element is strictly less or greater than another.

**Hint.** Which two prefix queries on the Fenwick tree give the less count and the greater count?

**Changed decision.** Ranks now index a Fenwick tree that changes as elements arrive, and the counts must be strict.
