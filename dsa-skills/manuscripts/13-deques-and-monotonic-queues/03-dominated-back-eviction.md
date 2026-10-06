<!-- lesson-kind: standard -->
<!-- lesson-id: dominated-back-eviction -->
## Remove Weaker Values From The Back

<!-- stage: context -->
### Why Dropping A Reading Needs A Reason

A rolling-peak alert keeps a short list of readings and drops every stored reading that a new one beats. A reviewer reads the code and asks one question. How do you know a dropped reading can never matter again? The author answers that it is smaller, and the reviewer is not satisfied. A smaller reading can still matter if it lasts longer than the new one, or if the query later asks for the smallest value instead.

This lesson gives the reason in exact terms and shows why the stored list holds positions instead of bare values. It then shows how the reason makes the removal cheap. The question is: when is it safe to drop a stored position, and where in the deque do such positions sit?

<!-- stage: naive -->
### Filtering The Whole List On Every Arrival

The direct plan keeps a list of positions. When a new position arrives, the method scans the entire list and deletes every stored position whose value is smaller than the new value.

```java
static List<Integer> positionsAfter(int[] a) {
    List<Integer> kept = new ArrayList<>();
    for (int i = 0; i < a.length; i++) {
        final int x = a[i];
        kept.removeIf(j -> a[j] < x);   // scan every stored position
        kept.add(i);
    }
    return kept;
}
```

For `a = [5, 3, 4, 4, 2, 6]` the method ends with the list `[5]`, the position of the value 6. The result is correct, and the first position in the list always holds the largest value.

<!-- stage: bottleneck -->
### Scanning Positions That Cannot Be Smaller

```predict
The stored values run 9, 7, 4, 2 from the first stored position to the last. A new value 5 arrives. Which stored values are smaller than 5, and where are they in the list?

Only 4 and 2 are smaller, and they are the last two entries. Because the list is in decreasing order, every smaller value sits at the end, so the scan never needs to look at 9 or 7.
```

The method calls `removeIf` on the whole list for each arrival. A stream that decreases keeps every position, so the list grows to size n. The scans then cost 1 + 2 + ... + n, which is O(n^2) in total. The scan compares the new value with entries near the front that cannot be smaller, because the list stays in decreasing order. The repeated work is that comparison with entries the order already rules out.

<!-- stage: insight -->
### Removing Only The Dominated Suffix

#### Saying When A Position Is Dominated

A stored position `j` is **dominated** by a newer position `i` when `j < i` and `a[j] <= a[i]`. Take any window of consecutive positions that contains `j` and ends at `i` or later. That window must also contain `i`, because `i` lies between `j` and the end of the window. Its maximum is at least `a[i]`, which is at least `a[j]`, so `j` is never needed to report that maximum. A dominated position can leave for good.

#### Finding The Dominated Positions Fast

The stored values stay in decreasing order, so the values that are smaller than the new one form a **contiguous suffix** at the back. The method pops from the back while the back is dominated. It stops at the first stored position that is not dominated, and everything before that position is larger and stays. The pops are the only removals, and each position is popped at most once.

#### Choosing A Rule For Equal Values

The **tie rule** says what happens to an equal value at the back. The rule in this lesson removes strictly smaller values only, so equal values both stay. The invariant is that every stored position can still become the maximum of some future window, and every popped position cannot. Storing positions, not values, keeps the age of each entry, which a later lesson needs for expiry.

<!-- names: dominated, contiguous suffix, tie rule -->

<!-- stage: variables -->
### State Stored For Each Arrival

The method keeps four pieces of state.

- **Deque** holds stored positions in increasing position order, and the matching values are in non-increasing order.
- **i** is the position that arrives now, and it is the only position appended in this step.
- **a[i]** is the value that decides which back positions are removed.
- **Back position** is the last entry of the deque, and the loop reads its value as `a[back]`.

The deque stores positions, so every value read goes through the array `a`.

<!-- stage: trace -->
### Seeing Which Positions Leave

The first trace follows `a = [5, 3, 4, 4, 2, 6]` with the maximum rule. The value 4 at position 2 removes position 1, whose value is 3, and the deque becomes positions 0 and 2. The second 4 at position 3 removes nothing, because the tie rule keeps equal values, so positions 0, 2 and 3 are stored. The value 6 at position 5 then removes four positions in a single arrival and leaves only position 5.

The second trace follows `a = [4, 6, 2, 5, 5, 1]` with the minimum rule. The value 2 at position 2 removes positions 1 and 0, because both hold larger values. The value 1 at position 5 removes three positions at once. The two traces show that a single arrival can remove many positions, but the total number of removals can never exceed the number of arrivals.

```trace
{"cells":[5,3,4,4,2,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","front_value":5,"removed":0},"note":"Index 0 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":1},"vars":{"deque":"[0,1]","front_value":5,"removed":0},"note":"Index 1 (value 3) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":2},"vars":{"deque":"[0,2]","front_value":5,"removed":1},"note":"Index 2 (value 4) removes index 1 from the back, since each has a value that 2 outlasts and beats. Then index 2 is appended."},{"at":{"i":3},"vars":{"deque":"[0,2,3]","front_value":5,"removed":0},"note":"Index 3 (value 4) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":4},"vars":{"deque":"[0,2,3,4]","front_value":5,"removed":0},"note":"Index 4 (value 2) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":5},"vars":{"deque":"[5]","front_value":6,"removed":4},"note":"Index 5 (value 6) removes index 4, 3, 2, 0 from the back, since each has a value that 5 outlasts and beats. Then index 5 is appended."}]}
```

```trace
{"cells":[4,6,2,5,5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","front_value":4,"removed":0},"note":"Index 0 (value 4) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":1},"vars":{"deque":"[0,1]","front_value":4,"removed":0},"note":"Index 1 (value 6) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":2},"vars":{"deque":"[2]","front_value":2,"removed":2},"note":"Index 2 (value 2) removes index 1, 0 from the back, since each has a value that 2 outlasts and beats. Then index 2 is appended."},{"at":{"i":3},"vars":{"deque":"[2,3]","front_value":2,"removed":0},"note":"Index 3 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":4},"vars":{"deque":"[2,3,4]","front_value":2,"removed":0},"note":"Index 4 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":5},"vars":{"deque":"[5]","front_value":1,"removed":3},"note":"Index 5 (value 1) removes index 4, 3, 2 from the back, since each has a value that 5 outlasts and beats. Then index 5 is appended."}]}
```

<!-- stage: code -->
### Popping Dominated Positions In Code

```java
static Deque<Integer> buildMax(int[] a) {
    Deque<Integer> d = new ArrayDeque<>();
    for (int i = 0; i < a.length; i++) {
        while (!d.isEmpty() && a[d.peekLast()] < a[i]) {   // back is dominated by position i
            d.pollLast();                                  // each position is popped once
        }
        d.addLast(i);                                      // position i is the newest entry
    }
    return d;
}
```

The array read `a[d.peekLast()]` unboxes the stored `Integer` into an `int` index. The method never compares two boxed positions with `==`. Boxed integers from -128 to 127 are cached, so `==` appears to work in small tests and then fails for larger positions.

The minimum version differs in one symbol. The comparison `a[d.peekLast()] > a[i]` removes larger values, so the front holds the smallest value.

- **Time** is O(n) in total, because each position is appended once and popped at most once.
- **Space** is O(n) in the worst case, which a strictly decreasing array reaches.

<!-- stage: applicability -->
### Checking The Domination Argument

#### Applying The Invariant

The invariant of this lesson is that every stored position can still become the answer for some future window, and every popped position cannot. The argument needs three facts. The positions are newer than the ones they dominate. The query is about a window of consecutive positions that ends at or after the new position. The comparison matches the query, larger values for a maximum.

#### Finding The False Friend

The false friend is a removal that matches the wrong query. Removing smaller values is safe for a maximum query and unsafe for a minimum query. A removed small value may be the minimum of a later window. A second false friend is a removal that ignores position. A newer value that is smaller does not dominate an older larger value. The older value can still win a window that holds both.

#### No-Go Conditions

Do not use this removal when a window can skip positions, because the argument needs the new position inside every window that holds the old one. Do not use it when the query asks for the number of values above a bound, because dominated positions still count there.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Maximum Candidate (Author exercise)
<!-- id: dq-insert-max -->

**Prerequisites.** The non-increasing rule from the previous lesson; this lesson.

**Problem.** Start with an empty deque of positions into an integer array `a`. Process the positions `0, 1, ..., n - 1` in order. For position `i`, remove from the back every stored position `j` with `a[j] < a[i]`, then append `i`. Return the stored positions after the last arrival, from the front to the back.

**Constraints.** The limits are:
- **Length** `n` is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** stay stored, because only strictly smaller values are removed.
- **Output** is an `int[]` of positions, empty for empty input.

**Example 1.** Input `[5, 3, 4, 4, 2, 6]`, output `[5]`.

**Example 2.** Input `[3, 3, 1]`, output `[0, 1, 2]`.

**Hint.** The deque stores positions, so each comparison reads the array at a stored position. Which stored positions does the last value in Example 1 remove?

**Changed decision.** First exercise of the lesson: the deque stores positions, and the value comes from the array.

#### [Vary] Insert Minimum Candidate (Author exercise)
<!-- id: dq-insert-min -->

**Prerequisites.** The build exercise above.

**Problem.** Repeat the process of the previous exercise with the opposite comparison. At position `i`, pop every stored position `j` that has `a[j] > a[i]` from the back, and then append `i`. Report what the deque holds after the last arrival, front first.

**Constraints.** The limits are:
- **Length** `n` is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** stay stored, because only strictly larger values are removed.
- **Output** is an `int[]` of positions, empty for empty input.

**Example 1.** Input `[4, 6, 2, 5, 5, 1]`, output `[5]`.

**Example 2.** Input `[1, 2, 3]`, output `[0, 1, 2]`.

**Hint.** Only the comparison changes. Which end of the stored values now holds the smallest value?

**Changed decision.** The comparison flips, and the removed values are the larger ones.

#### [Boundary] Repeated Equal Values (Author exercise)
<!-- id: dq-repeated-equal -->

**Prerequisites.** Both exercises above.

**Problem.** Two tie policies handle a stored position whose value equals the new value. Under the keep policy the stored position stays. Under the replace policy the stored position is removed. Given an integer array `a` and a boolean `keepEqual`, process the positions in order with the maximum rule. After each arrival, record the front position. Return the array of recorded front positions.

**Constraints.** The limits are:
- **Length** `n` is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Flag** `keepEqual` picks the policy for the whole run.
- **Output** has length `n`, and each entry is a position.

**Example 1.** Input `a = [4, 4, 2]` with `keepEqual = true`, output `[0, 0, 0]`.

**Example 2.** Input `a = [4, 4, 2]` with `keepEqual = false`, output `[0, 1, 1]`.

**Hint.** Both policies report a front with the same value. Which of two equal positions stays in range longer when old positions later expire?

**Changed decision.** The tie rule changes which position stays at the front, not which value.

#### [Recognize] Online Suffix Maximum Candidates (Author exercise)
<!-- id: dq-suffix-maxima -->

**Prerequisites.** The maximum rule with positions.

**Problem.** A suffix maximum of an array `a` is a position `i` such that `a[i] >= a[j]` for every `j > i`. The last position always qualifies. Return all suffix maxima in increasing order of position.

**Constraints.** The limits are:
- **Length** `n` is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** qualify, because the test is greater than or equal.
- **Output** is an `int[]` of positions, empty for empty input.

**Example 1.** Input `[4, 2, 7, 3]`, output `[2, 3]`.

**Example 2.** Input `[5, 5, 1]`, output `[0, 1, 2]`.

**Hint.** Compare the answer with the stored positions after the last arrival of the maximum rule. Which positions never lose to a later value?

**Changed decision.** The deque is the answer, because no position ever expires.
