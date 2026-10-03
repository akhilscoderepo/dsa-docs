<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-skipping -->
## Duplicate Skipping

<!-- stage: context -->
### A Token Booth At The Fair

A fair runs a booth where visitors drop off tokens. Each token carries a whole number: a positive number is a prize credit and a negative number is a fee. At closing time the clerk lays all tokens out in one row, ordered by number, and her manager asks for a tidy list of every combination of three tokens whose numbers cancel out to zero. A combination counts once, however many tokens in the row carry the same numbers.

The row is full of twins. There are six tokens marked minus two, five marked zero, and many more. If the clerk is careless she writes "minus two, zero, two" on the list thirty times, once for every way of picking physical tokens, and the manager throws the sheet back. She wants each distinct trio written exactly once, and she does not want to burn the afternoon rediscovering trios she has already written.

<!-- stage: naive -->
### Try Every Trio, Then Tidy The List

The plain plan is to test every group of three positions, write down the ones that cancel, and remove repeats afterwards by putting each sorted trio into a set.

```java
static List<List<Integer>> tripletsByBruteForce(int[] tokens) {
    Set<List<Integer>> seen = new HashSet<>();
    for (int a = 0; a < tokens.length; a++)
        for (int b = a + 1; b < tokens.length; b++)
            for (int c = b + 1; c < tokens.length; c++)
                if ((long) tokens[a] + tokens[b] + tokens[c] == 0) {
                    List<Integer> trio = new ArrayList<>(List.of(tokens[a], tokens[b], tokens[c]));
                    Collections.sort(trio);
                    seen.add(trio);
                }
    return new ArrayList<>(seen);
}
```

It is correct for every row, including rows with no cancelling trio, where it returns an empty list. The order of the returned list is whatever the hash set happens to produce.

<!-- stage: bottleneck -->
### Thirty Copies Of One Discovery

Three nested loops visit about n cubed over six groups of positions, which is O(n^3), and for a row of three thousand tokens that is several billion checks. Worse, most of those checks rediscover something already known. When the row holds five tokens marked zero, the loops start from each of them in turn, and every start repeats exactly the same hunt for a partner pair among the tokens to its right. The set at the end hides the repetition from the manager, but it does not stop the clerk from paying for it, and it adds hashing work for every cancelling trio.

Two separate wastes are mixed together here. The first is the cubic search itself, which the order of the row can already shrink, because once one token is chosen the other two must add up to a known amount and a sorted row lets two pointers find such pairs in a single sweep. The second waste is the repeated discoveries, and that one is cured by never starting a hunt that an earlier equal token has already finished.

<!-- stage: insight -->
### Skip Only After The Branch Is Done

Sort the row first. Equal numbers then sit side by side, and every group of twins forms one run. Inside a run, the first token is the **representative**: it is the one allowed to start a hunt, because everything a later twin could find is also available to it. The twins that follow add no new combinations of numbers, only new ways to name the same ones.

The **skip rule** is therefore "ignore this choice if it equals the choice just before it, at the same level". The comparison looks backwards, at a token that has already been fully processed. That detail matters. The first token to the right of the chosen one may equal the chosen one, as in minus one, minus one, two, and it must still be used, because the two tokens belong to different levels. A forward comparison, which skips a token because the next one is equal, throws away the representative before its branch ran and loses the answer.

The same policy applies at every level of choice. The outer loop picks a **fixed value**, and it skips a position when the previous position holds the same number. The inner pair scan records a cancelling pair and only then steps both pointers past their runs of twins. Recording comes first and skipping comes second, so the representative is always evaluated before any twin is discarded.

<!-- names: representative, skip rule, fixed value -->

The invariant that makes this safe is about runs. Every combination of numbers that has been written to the list was written by the first token of its run at each level, and no run was entered a second time. A pointer never moves backwards, so the skipping loops only add steps that were going to be taken one by one anyway, and each sweep of the pair scan stays linear.

<!-- stage: variables -->
### Index, Edges, Sum And Answer List

`i` is the position of the chosen token, and it is skipped when `i > 0` and the previous token holds the same number. `lo` starts just right of `i` and `hi` starts at the end of the row, and both are written to the list only after a hit. `sum` is computed as a `long`, because three large `int` values can add past the largest `int` and wrap to a wrong sign. `result` is the list of distinct trios, and each trio is built in increasing order because the row is sorted. The row itself is sorted in place, which is allowed here, so the caller's array is permuted afterwards.

<!-- stage: trace -->
### Records Come Before Skips

The first trace runs on the row minus one, minus one, 0, 1, 2, 2. At the first step the chosen token is minus one, and the pair scan reads minus one and 2, which cancel it. Study the second step: the trio is recorded, and only then does `hi` hop over the twin 2, and the next read is 0 and 1. The later steps show the second minus one being skipped without any scan, because the token before it is its twin.

```trace
{"cells":[-1,-1,0,1,2,2],"pointers":["i","lo","hi"],"steps":[{"at":{"i":0,"lo":1,"hi":5},"vars":{"sum":0,"found":1},"note":"-1 + -1 + 2 = 0. Record the trio first, then move past the twins: lo becomes 2 and hi becomes 3."},{"at":{"i":0,"lo":2,"hi":3},"vars":{"sum":0,"found":2},"note":"-1 + 0 + 1 = 0. Record the trio first, then move past the twins: lo becomes 3 and hi becomes 3."},{"at":{"i":1,"lo":-1,"hi":-1},"vars":{"found":2},"note":"Position 1 holds -1, the same as position 0, whose hunt already finished. Skip it without scanning."},{"at":{"i":2,"lo":3,"hi":5},"vars":{"sum":3,"found":2},"note":"0 + 1 + 2 = 3, too large, so hi becomes 4."},{"at":{"i":2,"lo":3,"hi":4},"vars":{"sum":3,"found":2},"note":"0 + 1 + 2 = 3, too large, so hi becomes 3."},{"at":{"i":3,"lo":4,"hi":5},"vars":{"sum":5,"found":2},"note":"1 + 2 + 2 = 5, too large, so hi becomes 4."}]}
```

The second trace uses a longer row, minus 2, minus 2, 0, 0, 0, 2, 2, 2, where runs of three twins collide with the pointers. Watch the step after the zero trio is recorded: `lo` and `hi` have met on the same position, so the scan for that chosen token ends at once, and the twins that remain are passed over by the outer check one at a time instead of by new scans. This row also gives a different ending than the first one, with one trio of three different numbers and one made of three twins.

```trace
{"cells":[-2,-2,0,0,0,2,2,2],"pointers":["i","lo","hi"],"steps":[{"at":{"i":0,"lo":1,"hi":7},"vars":{"sum":-2,"found":0},"note":"-2 + -2 + 2 = -2, too small, so lo becomes 2."},{"at":{"i":0,"lo":2,"hi":7},"vars":{"sum":0,"found":1},"note":"-2 + 0 + 2 = 0. Record the trio first, then move past the twins: lo becomes 5 and hi becomes 5."},{"at":{"i":1,"lo":-1,"hi":-1},"vars":{"found":1},"note":"Position 1 holds -2, the same as position 0, whose hunt already finished. Skip it without scanning."},{"at":{"i":2,"lo":3,"hi":7},"vars":{"sum":2,"found":1},"note":"0 + 0 + 2 = 2, too large, so hi becomes 6."},{"at":{"i":2,"lo":3,"hi":6},"vars":{"sum":2,"found":1},"note":"0 + 0 + 2 = 2, too large, so hi becomes 5."},{"at":{"i":2,"lo":3,"hi":5},"vars":{"sum":2,"found":1},"note":"0 + 0 + 2 = 2, too large, so hi becomes 4."},{"at":{"i":2,"lo":3,"hi":4},"vars":{"sum":0,"found":2},"note":"0 + 0 + 0 = 0. Record the trio first, then move past the twins: lo becomes 4 and hi becomes 4."},{"at":{"i":3,"lo":-1,"hi":-1},"vars":{"found":2},"note":"Position 3 holds 0, the same as position 2, whose hunt already finished. Skip it without scanning."},{"at":{"i":4,"lo":-1,"hi":-1},"vars":{"found":2},"note":"Position 4 holds 0, the same as position 3, whose hunt already finished. Skip it without scanning."},{"at":{"i":5,"lo":6,"hi":7},"vars":{"sum":6,"found":2},"note":"2 + 2 + 2 = 6, too large, so hi becomes 6."}]}
```

<!-- stage: code -->
### Triplets And Pairs Without Repeats

```java
static List<List<Integer>> distinctTriplets(int[] row) {
    Arrays.sort(row);                                   // sorted in place, allowed by the contract
    List<List<Integer>> result = new ArrayList<>();
    for (int fixed = 0; fixed + 2 < row.length; fixed++) {
        if (fixed > 0 && row[fixed] == row[fixed - 1]) continue;   // earlier twin already ran
        int left = fixed + 1, right = row.length - 1;
        while (left < right) {
            long sum = (long) row[fixed] + row[left] + row[right];
            if (sum < 0) left++;
            else if (sum > 0) right--;
            else {
                result.add(List.of(row[fixed], row[left], row[right]));   // record first
                int goneLeft = row[left], goneRight = row[right];
                while (left < right && row[left] == goneLeft) left++;      // then skip twins
                while (left < right && row[right] == goneRight) right--;
            }
        }
    }
    return result;
}

static List<int[]> distinctPairs(int[] sorted, long target) {
    List<int[]> pairs = new ArrayList<>();
    int lo = 0, hi = sorted.length - 1;
    while (lo < hi) {
        long sum = (long) sorted[lo] + sorted[hi];
        if (sum < target) lo++;
        else if (sum > target) hi--;
        else {
            pairs.add(new int[] {sorted[lo], sorted[hi]});
            int a = sorted[lo], b = sorted[hi];
            while (lo < hi && sorted[lo] == a) lo++;
            while (lo < hi && sorted[hi] == b) hi--;
        }
    }
    return pairs;
}
```

Sorting costs O(n log n), and each chosen token starts one sweep that moves two pointers at most n steps in total, so the search is O(n^2) time, with the output list as the only extra memory beyond sorting. The pair version is a single sweep, linear after the input is sorted. When both pointers sit on the same number and the run is skipped from both sides, the `left < right` guards stop the loops from walking across each other.

<!-- stage: applicability -->
### When Equal Choices Name One Answer

Reach for this shape when the answer is a collection of value combinations, the candidates can be ordered, and the same numbers can be reached through many different positions. The question to ask is whether two different branches can produce the same output, and the way to answer it is to sort and look for runs. State the invariant before coding: each run is entered once at every level of choice, and a run is entered only after the run before it has finished.

The nearest false friend is skipping with a forward look, the version that compares a token with the next one before doing any work. It passes most tests, and then fails on rows like minus one, minus one, two, where the legal answer uses two equal numbers. A second false friend is cleaning the output with a set, which gives correct lists but keeps the cubic or quartic cost of the repeated work. A third is a problem that asks for index tuples, where twins at different positions are different answers and nothing may be skipped.

In Java, compare numbers with `==` on `int`, never on `Integer` objects, because boxed values outside a small cache are not equal by identity. Say out loud whether the input may be reordered, because sorting in place permutes the caller's array. Keep the sum in `long`, and put the recording line before both skipping loops.

<!-- stage: exercises -->
### Exercises

#### [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Prerequisites.** The opposite-ends pair scan, and the idea of a run of equal values.

**Problem.** Given an array sorted in nondecreasing order and a `long` target, return every distinct pair of values `[x, y]` with `x <= y` and `x + y == target`, using two different positions. List the pairs by increasing `x`. The input is promised sorted and must not be modified.

**Constraints.** 0 <= nums.length <= 100000, any `int` values, and any `long` target. Each pair must appear once even when its values occur many times, and the scan must make at most 2n pointer moves.

**Example 1.** Input `nums = [1, 1, 2, 3, 3, 4, 5, 5], target = 6`, output `[[1, 5], [2, 4], [3, 3]]`.

**Example 2.** Input `nums = [2, 2, 2, 2], target = 4`, output `[[2, 2]]`.

**Hint.** After a pair is recorded, how many positions on each side hold a number that could only rebuild the same pair? Which pointer moves first, and what must be true before it does?

**Changed decision.** First rung: a hit is no longer the end of the sweep, so both pointers must leave their runs after the pair has been recorded.

#### [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-all -->

**Prerequisites.** The unique-pairs exercise above.

**Problem.** Given an unsorted array of integers, return every distinct triplet of values that adds up to zero, each triplet in nondecreasing order and the list in lexicographic order. The method may sort the input array in place.

**Constraints.** 0 <= nums.length <= 3000 and any `int` values within plus or minus one billion, so a triple sum can leave the `int` range. Do not use a set to remove repeats, and aim at O(n^2) time.

**Example 1.** Input `nums = [-4, 2, -2, 0, 2, 0, -2, 4]`, output `[[-4, 0, 4], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]`.

**Example 2.** Input `nums = [3, -1, -1, -1, 2]`, output `[[-1, -1, 2]]`.

**Hint.** What must be compared to decide that a chosen position repeats an earlier one, the previous position or the next? Where does the pair scan begin for a chosen position `i`?

**Changed decision.** The pair sweep now runs once per chosen position, so the skip policy appears twice: in the outer loop before a hunt starts, and in the inner loop after a trio is recorded.

#### [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal -->

**Prerequisites.** The 3Sum exercise above.

**Problem.** Return the distinct zero-sum triplets of an unsorted array that may consist of a single repeated value from end to end. Count the number of times a pointer or the chosen index advances, and show that an all-equal array costs only a linear amount of them.

**Constraints.** 0 <= nums.length <= 3000 and any `int` values. For an array of n equal elements the count of advances must be at most 4n.

**Example 1.** Input `nums = [0, 0, 0, 0]`, output `[[0, 0, 0]]`.

**Example 2.** Input `nums = [7, 7, 7, 7, 7]`, output `[]`.

**Hint.** When the first trio of zeros is recorded in a long run of zeros, how far can the pair scan travel before it ends? What does the outer loop do with every later zero?

**Changed decision.** The whole array is one run at every level, so any skip written in the wrong order shows up either as a missing trio or as a quadratic scan.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-all -->

**Prerequisites.** The 3Sum and all-equal exercises above.

**Problem.** Given an array of small integers and a target, return every distinct quadruplet of values that adds up to the target, each quadruplet in nondecreasing order and the list in lexicographic order. Apply the duplicate policy to both fixed positions and to the final pair scan. The array may be sorted in place.

**Constraints.** 0 <= nums.length <= 200 and each value between minus 1000 and 1000, and a target between minus 4000 and 4000. Aim at O(n^3) time without a set.

**Example 1.** Input `nums = [3, 1, 1, 1, 0, 2, 2, -1], target = 5`, output `[[-1, 1, 2, 3], [0, 1, 1, 3], [0, 1, 2, 2], [1, 1, 1, 2]]`.

**Example 2.** Input `nums = [2, 2, 2, 2, 2], target = 8`, output `[[2, 2, 2, 2]]`.

**Hint.** Which loop levels need their own backward comparison? What are the start positions of the second fixed index and of the pair scan?

**Changed decision.** A second fixed position joins the first, so the backward-looking skip is applied at three places and each one starts its comparison just after the position that opened its level.
