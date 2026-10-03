<!-- lesson-kind: standard -->
<!-- lesson-id: read-and-write -->
## Read And Write

<!-- stage: context -->
### A Tray Of Rolls From The Oven

A baker pulls a long tray of rolls from the oven and lines them up in a row. A few of them are burnt, and she wants to fill a delivery box with the good ones, keeping them in the order they came out. She cannot lift rolls out and set them aside, because the counter is tiny and the tray is all she has. The box is the front of the same tray, so the good rolls have to slide forward to fill the places the burnt ones occupied.

She does this a few times a day with trays of thousands of rolls, and the number of burnt ones varies from none at all to nearly half. She wants a way to tidy the tray that touches each roll only a small number of times, however many are burnt.

<!-- stage: naive -->
### Close The Gap After Every Burnt Roll

The obvious approach is to walk along the tray, and whenever a burnt roll appears, slide every later roll one place forward to close the gap, then carry on from the same place.

```java
static int removeByShifting(int[] tray, int burnt) {
    int size = tray.length;
    int pos = 0;
    while (pos < size) {
        if (tray[pos] == burnt) {
            for (int j = pos + 1; j < size; j++) tray[j - 1] = tray[j];
            size--;                      // the tray is one roll shorter
        } else {
            pos++;
        }
    }
    return size;
}
```

The first `size` slots end up holding the good rolls in their original order, and the method returns that size. What lies beyond is left over from the sliding and carries no meaning.

<!-- stage: bottleneck -->
### Rolls Slide Once Per Burnt Neighbour

Each burnt roll triggers a slide of everything behind it, up to n - 1 assignments. If half of an n-roll tray is burnt, that is about n / 2 slides of about n / 2 rolls on average, so the method is O(n^2) in the worst case. A tray of fifty thousand rolls that is mostly burnt costs hundreds of millions of assignments.

The waste is that a good roll is moved again and again, one place per burnt roll in front of it, when it only ever needed to move once, straight to its final place. That final place can be known without any sliding. It is the number of good rolls already seen, because those rolls will occupy the front of the tray in order. A method that remembers that single count can copy each good roll directly to that place and never touch it again, which brings the whole job down to one pass, O(n), whatever the number of burnt rolls.

<!-- stage: insight -->
### One Finger Reads, One Finger Writes

Use two positions that both move forward. The **read index** visits every roll exactly once, from the first to the last, and never goes back. The **write index** marks the next free place at the front of the tray, where the next accepted roll will be put. For each roll the read index reaches, a decision is made: if the roll is good, copy it to the write index and advance the write index, and if it is burnt, do nothing and let the read index move on.

The region from position 0 up to, but not including, the write index is the **kept prefix**. It holds exactly the accepted rolls seen so far, in their original order, and it is already in the final form the caller wants. That is the invariant: at every moment the kept prefix satisfies the final contract for the part of the input that has been read. The invariant is preserved because a roll joins the prefix only after passing the test, and it always joins at the end.

Overwriting is safe because the write index never gets ahead of the read index. A slot at or after the write index but before the read index holds a roll that was already examined, so it is either burnt or already copied forward, and nothing unread is lost. This also explains why the test may look at the kept prefix itself. A rule such as "accept a roll only if it differs from the last accepted one" consults the slot just behind the write index, which is guaranteed to hold the latest accepted value and has not been disturbed by the scan.

<!-- names: read index, write index, kept prefix -->

<!-- stage: variables -->
### Two Indices And A Count

`read` runs from 0 to `n - 1` in a plain `for` loop. `write` starts at 0 and only grows, by one each time a roll is accepted, so after the loop it is both the next free slot and the number of accepted rolls, and that is what the method returns. `burnt` is the value to discard, or for other filters a parameter such as a limit on repeats. Because `write <= read` at all times, the assignment `tray[write] = tray[read]` can only overwrite a slot that is already finished with. When `write == read`, nothing has been discarded yet, and the assignment copies a value onto itself.

<!-- stage: trace -->
### Accepting Rolls In Order

The first trace removes the value 4 from a row of seven numbers. Look closely at the fourth step, where the read index is at 3 and the write index is still at 1, because two 4s were skipped on the way. The value 2 is copied across that gap of two slots in a single assignment, not slid one place at a time.

```trace
{"cells":[4,1,4,2,3,4,5],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"value":4,"kept":0},"note":"Value 4 equals 4, so it is skipped and the read index moves on while the write index stays at 0."},{"at":{"read":1,"write":0},"vars":{"value":1,"kept":1},"note":"Value 1 is accepted and copied to slot 0, then the write index becomes 1."},{"at":{"read":2,"write":1},"vars":{"value":4,"kept":1},"note":"Value 4 equals 4, so it is skipped and the read index moves on while the write index stays at 1."},{"at":{"read":3,"write":1},"vars":{"value":2,"kept":2},"note":"Value 2 is accepted and copied to slot 1, then the write index becomes 2."},{"at":{"read":4,"write":2},"vars":{"value":3,"kept":3},"note":"Value 3 is accepted and copied to slot 2, then the write index becomes 3."},{"at":{"read":5,"write":3},"vars":{"value":4,"kept":3},"note":"Value 4 equals 4, so it is skipped and the read index moves on while the write index stays at 3."},{"at":{"read":6,"write":3},"vars":{"value":5,"kept":4},"note":"Value 5 is accepted and copied to slot 3, then the write index becomes 4."}]}
```

The second trace keeps only the first of each run of equal values in a sorted row of eight. The step to study is the fifth, where the read index is on a 3 that equals the value just behind the write index, so the test consults the kept prefix and refuses it. The row ends with four values accepted.

```trace
{"cells":[2,2,3,3,3,5,7,7],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"value":2,"kept":1},"note":"Value 2 differs from the newest accepted value, so it goes to slot 0 and the write index becomes 1."},{"at":{"read":1,"write":1},"vars":{"value":2,"kept":1},"note":"Value 2 equals the value just behind the write index, so the kept prefix refuses it and the write index stays at 1."},{"at":{"read":2,"write":1},"vars":{"value":3,"kept":2},"note":"Value 3 differs from the newest accepted value, so it goes to slot 1 and the write index becomes 2."},{"at":{"read":3,"write":2},"vars":{"value":3,"kept":2},"note":"Value 3 equals the value just behind the write index, so the kept prefix refuses it and the write index stays at 2."},{"at":{"read":4,"write":2},"vars":{"value":3,"kept":2},"note":"Value 3 equals the value just behind the write index, so the kept prefix refuses it and the write index stays at 2."},{"at":{"read":5,"write":2},"vars":{"value":5,"kept":3},"note":"Value 5 differs from the newest accepted value, so it goes to slot 2 and the write index becomes 3."},{"at":{"read":6,"write":3},"vars":{"value":7,"kept":4},"note":"Value 7 differs from the newest accepted value, so it goes to slot 3 and the write index becomes 4."},{"at":{"read":7,"write":4},"vars":{"value":7,"kept":4},"note":"Value 7 equals the value just behind the write index, so the kept prefix refuses it and the write index stays at 4."}]}
```

<!-- stage: code -->
### Filter Once, Then Keep Each Run Once

```java
static int removeValue(int[] tray, int burnt) {
    int write = 0;
    for (int read = 0; read < tray.length; read++) {
        if (tray[read] != burnt) {
            tray[write++] = tray[read];       // accepted rolls pack toward the front
        }
    }
    return write;
}

static int keepOnePerRun(int[] sorted) {
    int write = 0;
    for (int read = 0; read < sorted.length; read++) {
        if (write == 0 || sorted[read] != sorted[write - 1]) {
            sorted[write++] = sorted[read];   // differs from the newest accepted value
        }
    }
    return write;
}
```

Both loops read each slot once and write at most once, so the work is proportional to n with only two integers of extra storage. The array keeps its length, and only the first `write` slots are meaningful, so the caller must use the returned count and not `tray.length`. For `keepOnePerRun` the empty array needs no special case, since the loop body never runs and zero is returned.

<!-- stage: applicability -->
### Telling A Writer From A Window

Think of a write pointer whenever the output is a filtered or compacted version of the input, produced in place, with the first part of the array turning into the answer while the scan goes on. The test for each element may be about the element alone, as with a discarded value, or about the accepted prefix, as with a rule on repeats. State the invariant before coding, saying what the kept prefix promises, and write the single acceptance line that extends it.

The nearest false friend is the sliding window. A window also has two boundaries that move forward, but its left boundary removes state from a range that the answer is computed over, while the write pointer constructs output and the region behind it is never revisited. If the problem asks about a contiguous range with a running total, a window fits, and if it asks for a rearranged or filtered array, a writer fits. Another false friend is swapping the discarded element with the last element, which is shorter but destroys the order whenever the order matters.

In Java, the array cannot shrink, so the return value carries the new length, and slots past it hold stale data. Compare primitive values with `!=`, but compare objects with `equals` and be aware that moving an object copies a reference, not the object. Guard any look-behind such as `write - 2` so that it cannot go below zero.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Prerequisites.** The read and write indices of this lesson, and the stable compaction idea from Chapter 01.

**Problem.** Given an `int` array and a value `val`, remove every entry equal to `val` in place, keeping the survivors in order at the front. Return a pair `[k, moves]`, where `k` is the number of survivors and `moves` is the number of survivors that now sit in a slot different from the one they started in. Do not assign a slot to itself.

**Constraints.** 0 <= nums.length <= 50000 and any `int` values. Use constant extra memory, one pass, and count every real assignment.

**Example 1.** Input `nums = [4, 9, 4, 6, 7], val = 4`, output `[3, 3]`, with the first three slots holding `[9, 6, 7]`.

**Example 2.** Input `nums = [8, 8, 2, 3], val = 9`, output `[4, 0]`, and the array is unchanged.

**Hint.** When do the read index and the write index point at the same slot? What does an assignment between them do in that case?

**Changed decision.** First rung: the count of real assignments is returned along with the length, so a self-copy has to be recognized and skipped.

#### [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Prerequisites.** The remove-element exercise above.

**Problem.** An array holds `Token` objects, each with an `int key`. Rearrange the array in place so that all tokens with a nonzero key come first in their original order, followed by the zero-key tokens. Every original token object must remain in the array exactly once, so no token may be replaced by a new object.

**Constraints.** 0 <= tokens.length <= 20000 and any `int` keys. Tokens are compared by identity of the object when checking the result. The zero-key tokens may end in any order, and extra memory must be constant.

**Example 1.** Input keys `[3, 0, 0, 5, 0, 8]`, output keys `[3, 5, 8, 0, 0, 0]`.

**Example 2.** Input keys `[6, 7]`, output keys `[6, 7]`, with both tokens untouched.

**Hint.** Copying nonzero tokens forward and then filling the tail would lose objects. What can the write slot receive instead, so that the discarded token is kept?

**Changed decision.** The suffix cannot be filled with fresh zeroes, because identity matters, so the accepted token and the token at the write slot trade places.

#### [Boundary] Remove Duplicates from Sorted Array (LeetCode 26)
<!-- id: tp-keep-last-of-run -->

**Prerequisites.** The two exercises above.

**Problem.** An array of `Item` objects, each with an `int key` and a `char tag`, is sorted by key. Keep exactly one item per key, and keep the last item of each run of equal keys, so that the tag shows which item survived. Compact the survivors to the front in order and return the count.

**Constraints.** 0 <= items.length <= 30000, any `int` keys, sorted by key with equal keys adjacent. Constant extra memory, and the empty array must work with no special branch.

**Example 1.** Input `[1:a, 1:b, 2:c, 3:d, 3:e, 3:f]`, output `k = 3` with prefix `[1:b, 2:c, 3:f]`.

**Example 2.** Input `[]`, output `k = 0`.

**Hint.** The acceptance test cannot ask whether the item differs from the last accepted one, since that would keep the first of a run. What fact about the next item tells you the current one ends its run?

**Changed decision.** The kept representative is the last of its run, so the test looks ahead from the read index, and one-element runs are accepted automatically.

#### [Recognize] Remove Duplicates from Sorted Array II (LeetCode 80)
<!-- id: tp-at-most-limit -->

**Prerequisites.** All three exercises above.

**Problem.** Given a sorted `int` array and a limit `L`, keep at most `L` copies of each value, compacting the survivors to the front in order, and return the count. The array may be modified, and the limit can be any value from 0 up to the array length.

**Constraints.** 0 <= nums.length <= 50000, any `int` values sorted nondecreasing, and 0 <= L <= nums.length. The scan reads each slot once, and `L = 0` must return 0.

**Example 1.** Input `nums = [2, 2, 2, 2, 5, 5, 9], L = 3`, output `k = 6` with prefix `[2, 2, 2, 5, 5, 9]`.

**Example 2.** Input `nums = [4, 4], L = 0`, output `k = 0`.

**Hint.** The read index advances every time, and only the acceptance test changes. Which slot of the kept prefix tells you how many copies of the current value are already there, and what happens when `write < L`?

**Changed decision.** The limit is a parameter, so the acceptance test looks back `L` places in the kept prefix, and the zero limit needs a guard in place of the fixed two copies.
