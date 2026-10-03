<!-- lesson-kind: standard -->
<!-- lesson-id: range-queries -->
## Range Queries

<!-- stage: context -->
### A Bakery's Sales Ledger

A bakery keeps a ledger with one line per day, showing how many loaves were sold that day. The ledger is never edited once a day is closed. The owner is preparing a loan application, and the bank keeps asking for totals over stretches of days: the second week of March, the ten days around a holiday, the single Saturday of a street fair, the whole year so far. There are hundreds of such questions, each with a different first day and last day.

Adding the lines for every stretch by hand is slow, and the same days are added again and again by different questions. The bookkeeper notices that the totals for different stretches overlap heavily, and wonders whether a single extra column in the ledger could make every one of these questions quick.

<!-- stage: naive -->
### Add The Days Of Each Stretch

The direct approach is to answer each question by adding the daily lines from the first day of the stretch to the last.

```java
static long totalBetween(int[] daily, int firstDay, int lastDay) {
    long total = 0;
    for (int d = firstDay; d <= lastDay; d++) {
        total += daily[d];
    }
    return total;
}
```

Both ends are included, and the loop is correct for any stretch inside the ledger, including a single day.

<!-- stage: bottleneck -->
### Overlapping Stretches Add The Same Days

A stretch of length m costs O(m), so q questions over a ledger of n days cost O(q n) in the worst case, since many questions cover most of the year. With a hundred thousand days and a hundred thousand questions, that is again about ten billion additions, most of them repeating days that an earlier question already counted.

Look at what any stretch really is. The total from the first day through the last day is the total of everything up to the last day with everything before the first day taken away. The totals up to each day were built once in the previous lesson, so each question is the difference between two numbers that are already stored. After one pass of O(n) to build the totals, a question costs O(1).

<!-- stage: insight -->
### Subtract Two Stored Totals

Every contiguous stretch of the data is a prefix with a smaller prefix removed. With the sentinel layout from the last lesson, where `prefix[i]` holds the sum of the first `i` values, a **range sum** of the values at positions `left` to `right`, both included, is `prefix[right + 1] - prefix[left]`. The first term counts every value from the start through `right`. The second counts every value before `left`. The values before `left` appear in both terms, so they vanish: this is **cancellation**, and it is the entire idea.

The invariant is the formula itself. For any `left` and `right` with `0 <= left <= right < n`, the two slots read are inside the array, and their difference equals the sum of exactly the positions in the stretch. The sentinel is what makes `left = 0` safe, since `prefix[0]` is zero, and the extra slot at the end is what makes `right = n - 1` safe.

<!-- names: range sum, cancellation, half-open range -->

Some code describes a stretch as a **half-open range**, from `left` up to but not including `right`. The same idea gives `prefix[right] - prefix[left]`, with no `+ 1`. Both conventions are correct, and mixing them is the usual source of off-by-one errors, so a solution should say which one the contract uses and compute the slot indices from that. Only the input needs to stay unchanged. The prefix array is built once, and every later question reads two slots.

<!-- stage: variables -->
### The Table And Two Slots

`prefix` is the table of totals with `n + 1` entries, built once and never changed. `left` and `right` are the positions that bound the question, and under the inclusive convention both belong to the stretch. The two slots read are `right + 1` and `left`, and the answer is their difference as a `long`. A query is valid only when `0 <= left`, `left <= right`, and `right < n`, and an invalid query is a contract question, not something the formula fixes.

<!-- stage: trace -->
### Two Reads Answer A Question

The first trace answers one question on the daily sales 3, 1, 4, 1, 5, 9, 2, 6, whose table of totals is 0, 3, 4, 8, 9, 14, 23, 25, 31. The cells are the table, and the question asks for days 2 to 5, both included. Pay attention to the third step, where the two stored totals are 23 and 4, and their difference 19 is the sum of days 2, 3, 4 and 5, which are 4, 1, 5 and 9.

```trace
{"cells":["0","3","4","8","9","14","23","25","31"],"pointers":["lo","hi"],"steps":[{"at":{"lo":2,"hi":6},"vars":{"left":2,"right":5},"note":"The question covers days 2 to 5. The slot after the last day is 6 and the slot before the first day is 2."},{"at":{"lo":2,"hi":6},"vars":{"slotHigh":23,"slotLow":4},"note":"Read slot 6, which holds 23, and slot 2, which holds 4."},{"at":{"lo":2,"hi":6},"vars":{"answer":19},"note":"Subtract: 23 - 4 = 19, the sum of 4, 1, 5 and 9."}]}
```

The second trace answers three questions on the same table in turn: a single day, the whole ledger, and one more single day. The cells are again the table. The step to study is the second question, where the left slot is the sentinel at position zero, so the whole ledger needs no special case.

```trace
{"cells":["0","3","4","8","9","14","23","25","31"],"pointers":["lo","hi"],"steps":[{"at":{"lo":4,"hi":5},"vars":{"left":4,"right":4,"answer":5},"note":"The question is a single day, days 4 to 4: slot 5 minus slot 4 is 14 - 9 = 5."},{"at":{"lo":0,"hi":8},"vars":{"left":0,"right":7,"answer":31},"note":"The question is the whole ledger, days 0 to 7: slot 8 minus slot 0 is 31 - 0 = 31. The left slot is the sentinel at position 0, which holds 0, so no special case is needed."},{"at":{"lo":3,"hi":4},"vars":{"left":3,"right":3,"answer":1},"note":"The question is a single day, days 3 to 3: slot 4 minus slot 3 is 9 - 8 = 1."}]}
```

<!-- stage: code -->
### Build Once, Subtract Per Question

```java
static long[] buildTable(int[] a) {
    long[] prefix = new long[a.length + 1];
    for (int i = 0; i < a.length; i++) {
        prefix[i + 1] = prefix[i] + a[i];
    }
    return prefix;
}

static long sumInclusive(long[] prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}

static long sumHalfOpen(long[] prefix, int left, int right) {
    return prefix[right] - prefix[left];
}
```

Building costs one pass and n + 1 slots, and each question reads two slots, so q questions cost O(n + q) in total. The two query forms differ only by the shift of the right slot, which is the entire difference between the conventions.

<!-- stage: applicability -->
### When Questions Outnumber Changes

Use this when the data does not change, many questions ask for the total of a contiguous stretch, and each question names its own ends. The invariant is the subtraction rule: slot `right + 1` minus slot `left` equals the total of the stretch, as long as the table is built from the unchanged input.

A false friend is the sliding window, which keeps a total for one moving stretch and is a good tool when the stretches are related, with each one a small shift of the previous one. It does not give an answer for an arbitrary pair of ends on demand. Another false friend is the table kept after the data changes: if values are updated, the table is stale and every later answer is wrong, and a structure for changing data is needed instead. A third is subtraction on a quantity that cannot be undone, such as the maximum, where removing the earlier part does not recover the stretch.

In Java, read the bound convention from the contract and write it as a comment above the formula. Use a `long` table, and cast nothing late: the subtraction of two `long` slots is exact, and an `int` table can wrap before the subtraction happens. Reject or document queries that fall outside the array, since the formula reads outside it silently only when the slot count is wrong.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query - Immutable (LeetCode 303)
<!-- id: ps-range-immutable -->

**Prerequisites.** The prefix construction lesson, with its sentinel slot.

**Problem.** Design a class that is given an integer array once, and then answers many requests for the sum of the values from index `left` through index `right`, both included. Each request must take constant time after the setup.

**Constraints.** 1 <= nums.length <= 10000, -100000 <= nums[i] <= 100000, and up to 10000 requests with 0 <= left <= right < nums.length.

**Example 1.** Input `nums = [4, -3, 6, 2, 8]` and the request `(1, 3)`, output 5.

**Example 2.** Input the same array and the request `(0, 4)`, output 17.

**Hint.** What do you store at construction time? Which two stored values does a request read?

**Changed decision.** First rung: the work moves from each request to the constructor, and a request becomes one subtraction.

#### [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Prerequisites.** The Range Sum Query exercise above.

**Problem.** Change the contract so that a request `(left, right)` asks for the values at positions `left` up to but not including `right`. Derive the formula, and show that a request with `left == right` is a valid request for an empty stretch whose answer is zero.

**Constraints.** 1 <= nums.length <= 100000 and 0 <= left <= right <= nums.length, so `right` may equal the length.

**Example 1.** Input `nums = [4, -3, 6, 2, 8]` and the request `(1, 4)`, output 5.

**Example 2.** Input the same array and the request `(3, 3)`, output 0.

**Hint.** Which slot stands for everything before `right` when `right` is excluded? Can `right` equal the length?

**Changed decision.** The right end is excluded, so the second slot read is `right` itself, and an empty stretch becomes legal.

#### [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array -->

**Prerequisites.** The two exercises above.

**Problem.** Answer the request `(0, n - 1)` for the whole array and a request for a single value at either end, without reading before position zero or past the end of the table. Explain which sentinel makes each case safe.

**Constraints.** 1 <= nums.length <= 100000 and values between -1000000000 and 1000000000, so the total needs a `long`.

**Example 1.** Input `nums = [1000000000, 1000000000, 1000000000]` and the request `(0, 2)`, output 3000000000.

**Example 2.** Input `nums = [5]` and the request `(0, 0)`, output 5.

**Hint.** What is read for a left end of zero? What is read for a right end of `n - 1`?

**Changed decision.** The extreme ends of the array touch both edges of the table, so the sentinel slot and the final slot are used on purpose.

#### [Recognize] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-queries-intro -->

**Prerequisites.** All three exercises above. The dedicated XOR lesson comes later in the chapter.

**Problem.** Given an array of non-negative integers and a list of requests `(left, right)`, return for each request the bitwise XOR of the values from `left` through `right`, both included. Reuse the table idea with XOR in place of addition, since XOR of a value with itself is zero.

**Constraints.** 1 <= arr.length <= 30000, 0 <= arr[i] <= 1000000000, and up to 30000 requests with 0 <= left <= right < arr.length.

**Example 1.** Input `arr = [6, 2, 7, 4]` and the request `(1, 3)`, output 1.

**Example 2.** Input the same array and the request `(0, 0)`, output 6.

**Hint.** Which operation plays the role of subtraction when you want to remove the part before `left`?

**Changed decision.** The operation changes from addition to XOR, so the removal of the early part is done by XOR instead of subtraction.
