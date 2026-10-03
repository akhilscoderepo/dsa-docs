<!-- lesson-kind: standard -->
<!-- lesson-id: lower-and-upper-bounds -->
## Lower And Upper Bounds

<!-- stage: context -->
### Shelving A New Book

A librarian keeps a row of books ordered by call number. A new book arrives and she must put it where it belongs, so that the row stays in order after she has pushed the later books one place along. She does not care whether a book with the same call number is already on the shelf. She needs the slot: the first place in the row whose book comes at or after the new one.

The slot might be the very first place, if the new book comes before everything, or the place just past the last book, if the new book comes after everything. She could be asked a second, slightly different question as well: where would the new book go if it had to sit after every book with the same call number, so that earlier copies stay in front of it. The two slots coincide when no copy is present, and they differ by the number of copies when some are.

<!-- stage: naive -->
### Walk Until The Row Passes

The simplest method walks from the left end until it meets a book that is not before the new one.

```java
static int slotByWalking(int[] row, int newBook) {
    int slot = 0;
    while (slot < row.length && row[slot] < newBook) slot++;
    return slot;
}
```

It returns zero for an empty row or when the new book belongs first, it returns the row length when the new book belongs last, and for repeated values it stops at the earliest copy.

<!-- stage: bottleneck -->
### Reading One Book At A Time

The walk may pass every book before it stops, which makes it O(n) readings, and a library that inserts many books pays that cost every time. The order of the row has not been used. Each book read says that one position is before the slot, but the order says much more: if a book at position `mid` is before the new one, then every earlier book is as well.

This situation is different from searching for an exact book, though, and the difference matters. The answer is not a position where a match must exist. It might be a position past the last book, where there is nothing to read, and it must be the first slot with a certain property even when many books share a call number. An exact search that stops when it reads a matching book would stop at an arbitrary copy and give an answer that is neither the first slot nor the last.

<!-- stage: insight -->
### Find Where The Answer Switches

For a fixed target, each position in a sorted array is either before the target or not. Reading the positions from left to right gives a run of "before" followed by a run of "not before", and the answer is the position where they switch. Two switch points are useful. The **lower bound** is the first position whose value is at least the target, which is the slot in front of every copy. The **upper bound** is the first position whose value is strictly greater than the target, which is the slot behind every copy. Their difference is the number of copies.

The search for a switch point uses a **half-open interval** `[lo, hi)`, where `lo` is a position that might be the answer and `hi` is a position that might also be the answer but has not been read, with `hi` starting at `n` because the switch may be past the last element. The loop runs while `lo < hi`. At each step it reads `mid`. If the value there is before the target, the switch must be after `mid`, so `lo = mid + 1`. Otherwise `mid` itself could be the switch, and everything after it cannot improve it, so `hi = mid`. When the loop ends, `lo` equals `hi` and is the answer.

<!-- names: lower bound, upper bound, half-open interval -->

The invariant has two halves. Every position before `lo` has been proved to be before the target, and the position `hi` is a possible switch point, either because it was read and found not to be before the target or because it is `n`. Equality never ends the loop, because the first copy might lie further left. For the lower bound, "before the target" means the value is less than the target. For the upper bound it means the value is less than or equal to the target. A thermometer that shows cold, cold, cold, warm, warm offers a picture: the search hunts for the tick where the reading flips, and once that tick is bracketed, readings elsewhere add nothing.

Wraparound problems use the upper bound with one extra rule. If the smallest letter strictly greater than the target does not exist, because the target is at least as large as every letter, the stated contract says the answer is the first letter, and that rule is applied after the search.

<!-- stage: variables -->
### Lo, Hi And The Switch Predicate

`lo` and `hi` are the edges of a half-open interval, with `hi` initially the array length. `mid` is the position read in each turn, and it is always at least `lo` and strictly less than `hi`, so it is a valid index. The predicate tells whether the value at `mid` is before the target, and it is the only place where the lower bound and the upper bound differ: strict less-than for the lower bound, less-than-or-equal for the upper bound. At the end, `lo` is the answer, and for a count of copies it is subtracted from the upper bound.

<!-- stage: trace -->
### Two Switch Points In One Row

The first trace finds the lower bound of 5 in the row 1, 3, 5, 5, 5, 8, 9, 11. The first reading is at position 4, which holds 5, a value that is not before the target, so the right edge moves to 4 without stopping. The step to study is the third: position 1 holds 3, which is before the target, so the left edge moves to 2, and then the two edges meet at 2.

```trace
{"cells":[1,3,5,5,5,8,9,11],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":4},"vars":{"value":5},"note":"Read position 4: 5 is not less than 5, so it may be the answer and hi becomes 4."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"value":5},"note":"Read position 2: 5 is not less than 5, so it may be the answer and hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"value":3},"note":"Read position 1: 3 is less than 5, so it is before the answer and lo becomes 2."},{"at":{"lo":2,"hi":2,"mid":-1},"vars":{"answer":2},"note":"The edges meet at 2, which is the answer."}]}
```

The second trace finds the upper bound of 5 in the same row. Now a value equal to 5 counts as before the target, so the first reading at position 4 sends the left edge to 5. The edges meet at 5, which is the first position holding something greater than 5. The difference from the lower bound, 5 minus 2, is 3, the number of copies of 5.

```trace
{"cells":[1,3,5,5,5,8,9,11],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":4},"vars":{"value":5},"note":"Read position 4: 5 is at most 5, so it is before the answer and lo becomes 5."},{"at":{"lo":5,"hi":8,"mid":6},"vars":{"value":9},"note":"Read position 6: 9 is greater than 5, so it may be the answer and hi becomes 6."},{"at":{"lo":5,"hi":6,"mid":5},"vars":{"value":8},"note":"Read position 5: 8 is greater than 5, so it may be the answer and hi becomes 5."},{"at":{"lo":5,"hi":5,"mid":-1},"vars":{"answer":5},"note":"The edges meet at 5, which is the answer."}]}
```

<!-- stage: code -->
### Both Bounds And A Wraparound Letter

```java
static int lowerBound(int[] a, int target) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int upperBound(int[] a, int target) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static char nextGreatestLetter(char[] letters, char target) {
    int lo = 0, hi = letters.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (letters[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo == letters.length ? letters[0] : letters[lo];
}
```

Each loop halves the interval, so the cost is O(log n) time and O(1) space. The number of copies of a value is `upperBound - lowerBound`, found in O(log n) without any walking. In the letter version the position `letters.length` stands for "no letter is greater", and the final line turns that into the first letter, as the contract requires.

<!-- stage: applicability -->
### When The Answer Is An Insertion Point

Use a bound search when the output is a position between elements, such as where to insert, how many values are below a threshold, or how many copies exist. The invariant to state is the pair of facts about `lo` and `hi`: everything before `lo` fails the predicate, and `hi` is a possible answer. Name the predicate in a comment, since the entire difference between the two bounds sits in it.

A false friend is exact search. It may stop on equality, but a bound may not, because the first or last copy might lie to one side. Another false friend is the habit of searching for the target and then adjusting by one, which gives the wrong answer when the target is absent or repeated. A third is a half-open loop written with a closed-interval update, such as `hi = mid - 1`, which can skip the answer.

In Java, start `hi` at `a.length` and not at `a.length - 1`, so that the answer past the end is representable. Compare with `<` and `<=` for the predicates and never subtract. If the contract has a wraparound, apply it after the loop and not inside it.

<!-- stage: exercises -->
### Exercises

#### [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-search-insert -->

**Prerequisites.** The first-and-last lesson, and the half-open convention above.

**Problem.** Given a sorted array of distinct integers and a target, return the index of the target if present, and otherwise the index where it would be inserted to keep the array sorted. Find the first position whose value is at least the target.

**Constraints.** 0 <= nums.length <= 100000, strictly increasing values, and any `int` target. Run in O(log n).

**Example 1.** Input `nums = [2, 4, 7, 9], target = 7`, output 2.

**Example 2.** Input `nums = [2, 4, 7, 9], target = 5`, output 2.

**Hint.** What is the predicate that is false on a prefix and true afterwards? What value should `hi` start with, and why?

**Changed decision.** First rung: the answer may be a position with nothing to read, so the interval is half-open and the loop never stops on equality.

#### [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Prerequisites.** The search-insert exercise above.

**Problem.** Given a sorted array that may hold repeated values and a target, return the first position whose value is strictly greater than the target, or the array length if there is none. Use it to count copies of the target as the upper bound minus the lower bound.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values, nondecreasing. Run in O(log n).

**Example 1.** Input `nums = [1, 2, 2, 2, 5], target = 2`, output 4, and the number of copies is 3.

**Example 2.** Input `nums = [1, 2, 2, 2, 5], target = 0`, output 0.

**Hint.** Which comparison in the loop decides that a value is before the answer? How does it differ from the lower bound?

**Changed decision.** The predicate changes from strictly less to less-or-equal, which moves the switch point behind the copies of the target.

#### [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Prerequisites.** The two exercises above.

**Problem.** Test both bounds on a target smaller than every element, a target larger than every element, and an empty array. Show that the insertion positions are 0 and the array length, and that the two bounds agree when the target is absent.

**Constraints.** 0 <= nums.length <= 1000. Include `Integer.MIN_VALUE` and `Integer.MAX_VALUE` as targets, and make no out-of-range array reads.

**Example 1.** Input `nums = [5, 6, 7], target = 1`, output both bounds equal to 0.

**Example 2.** Input `nums = [5, 6, 7], target = 9`, output both bounds equal to 3, the array length.

**Hint.** What is the answer when every value fails the predicate? What does an empty array do to the loop condition?

**Changed decision.** The targets sit outside the data, so the answer is at one of the two ends and the position `n` must be a legal result.

#### [Recognize] Find Smallest Letter Greater Than Target (LeetCode 744)
<!-- id: bs-next-greatest-letter -->

**Prerequisites.** All three exercises above.

**Problem.** Given a sorted array of lowercase letters, which may contain repeats, and a target letter, return the smallest letter that is strictly greater than the target. If no such letter exists, return the first letter of the array.

**Constraints.** 2 <= letters.length <= 10000, lowercase English letters in nondecreasing order, and the array contains at least two different letters.

**Example 1.** Input `letters = ['d', 'h', 'h', 'm', 't'], target = 'h'`, output `'m'`.

**Example 2.** Input `letters = ['d', 'h', 'h', 'm', 't'], target = 'z'`, output `'d'`.

**Hint.** Which bound gives the first letter strictly greater than the target? What does the position equal to the array length mean here?

**Changed decision.** The upper bound is used, followed by a wraparound rule that turns the position past the end into the first letter.
