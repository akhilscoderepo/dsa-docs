<!-- lesson-kind: standard -->
<!-- lesson-id: remainder-classes -->
## Remainder Classes

<!-- stage: context -->
### A Dial That Wraps Around

A round dial has k evenly spaced marks, numbered from 0 to k - 1, and a single pointer that starts at mark 0. A clerk feeds the dial a long tape of numbers. For each number the pointer moves forward by that many marks, wrapping around past the last mark back to zero, and a negative number moves the pointer backward. After every number the clerk writes down which mark the pointer is on.

A supervisor looks at the sheet of marks and asks: for how many stretches of consecutive numbers did the pointer travel an exact whole number of laps, ending on the mark where the stretch began? The tape is long, and a number can be larger than the dial or negative, so the clerk cannot do this by eye.

<!-- stage: naive -->
### Add Up Each Stretch And Test It

The direct approach is to add up every stretch of the tape and test whether its total is a multiple of the number of marks.

```java
static int countWholeLaps(int[] tape, int marks) {
    int count = 0;
    for (int first = 0; first < tape.length; first++) {
        int total = 0;
        for (int last = first; last < tape.length; last++) {
            total += tape[last];
            if (total % marks == 0) count++;
        }
    }
    return count;
}
```

It tests every stretch and is correct for numbers of either sign, since a remainder of zero is zero whether the total is positive or negative.

<!-- stage: bottleneck -->
### Every Stretch Is Totaled Separately

The two loops cover about n squared over two stretches, so the cost is O(n^2), which is five billion stretches for a tape of a hundred thousand numbers. The loop also throws away what the sheet of marks already knows: the pointer's mark after each number is enough to tell whether two moments are a whole number of laps apart.

Two moments at which the pointer sits on the same mark are separated by a whole number of laps, since the travel between them returns the pointer to where it was. So the supervisor's count is the number of pairs of moments, including the moment before the first number, that share a mark. If a mark was visited c times, it contributes c times (c - 1) over two pairs. Counting visits per mark takes one pass, so the whole count costs O(n).

<!-- stage: insight -->
### Same Dial Position, Same Class

Two totals are in the same **remainder class** when dividing each by `k` leaves the same remainder, and the difference of two numbers in the same class is a multiple of `k`. A stretch total is the difference of two running totals, so the stretch total is divisible by `k` exactly when its two running totals are in the same class. Instead of storing the running totals, store how often each class has occurred. For each position, the number of stretches ending there with a divisible total is the number of earlier running totals in the current class, and the table is updated after the lookup. This is the same count pattern as before, with the class replacing the exact total.

In Java the remainder operator can be negative: `-3 % 5` is `-3`, not `2`. A negative running total therefore lands on a class that does not match the same class reached from the other direction. The fix is the **normalized remainder**, a value always between zero and `k - 1`, produced by `Math.floorMod(total, k)`, which returns a non-negative result for a positive `k`. With normalized remainders, an array of `k` counters can be indexed directly, and the class of a negative total is correct.

<!-- names: remainder class, normalized remainder, pair count -->

The table plays one of two roles. To count stretches, it stores how often each class occurred, and the answer grows by the **pair count** of the current class before the class is updated. To decide whether a stretch of at least a given length exists, it stores the first index of each class, and an index difference is compared with the length rule. The seeded start, class zero before the first number, is present in both, because a stretch beginning at the first number pairs with it.

<!-- stage: variables -->
### Total, Class And Table

`total` is the running total, kept in a `long` unless the bounds make an `int` safe. `cls` is `Math.floorMod(total, k)`, a value from zero up to `k - 1`. For counting, `seen` is an array of `k` counters with `seen[0] = 1` at the start. For the length question, `firstAt` maps a class to the earliest index at which it occurred, with class zero at index minus one. Each step updates `total`, computes `cls`, reads the table, and only then records the current position.

<!-- stage: trace -->
### Classes Visited On The Dial

The first trace follows the tape 4, 5, 0, -2, -3, 1 on a dial with 5 marks. The running totals are 4, 9, 9, 7, 4, 5 and their classes are 4, 4, 4, 2, 4, 0. The step to study is the third: the class 4 has already occurred twice, so two stretches end here with a total divisible by 5, and the running count rises from 1 to 3.

```trace
{"cells":["4","5","0","-2","-3","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":4,"class":4,"added":0,"count":0},"note":"The total is 4, in class 4. Class 4 occurred 0 times before, so 0 stretches end here and the count is 0."},{"at":{"i":1},"vars":{"total":9,"class":4,"added":1,"count":1},"note":"The total is 9, in class 4. Class 4 occurred 1 times before, so 1 stretches end here and the count is 1."},{"at":{"i":2},"vars":{"total":9,"class":4,"added":2,"count":3},"note":"The total is 9, in class 4. Class 4 occurred 2 times before, so 2 stretches end here and the count is 3."},{"at":{"i":3},"vars":{"total":7,"class":2,"added":0,"count":3},"note":"The total is 7, in class 2. Class 2 occurred 0 times before, so 0 stretches end here and the count is 3."},{"at":{"i":4},"vars":{"total":4,"class":4,"added":3,"count":6},"note":"The total is 4, in class 4. Class 4 occurred 3 times before, so 3 stretches end here and the count is 6."},{"at":{"i":5},"vars":{"total":5,"class":0,"added":1,"count":7},"note":"The total is 5, in class 0. Class 0 occurred 1 times before, so 1 stretches end here and the count is 7."}]}
```

The second trace uses the tape -3, 1, 2, -4 on a dial of 3 marks, to show the hazard of negative totals. Each step shows the class given by Java's `%`, which is negative, next to the normalized class. The step to study is the second: the running total is -2, `%` gives -2, which is not a valid dial mark, and the normalized class is 1.

```trace
{"cells":["-3","1","2","-4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":-3,"javaRemainder":0,"class":0,"count":1},"note":"The total is -3. Java's % gives 0 and the normalized class is 0, which occurred 1 times before, so the count is 1."},{"at":{"i":1},"vars":{"total":-2,"javaRemainder":-2,"class":1,"count":1},"note":"The total is -2. Java's % gives -2 and the normalized class is 1, which occurred 0 times before, so the count is 1."},{"at":{"i":2},"vars":{"total":0,"javaRemainder":0,"class":0,"count":3},"note":"The total is 0. Java's % gives 0 and the normalized class is 0, which occurred 2 times before, so the count is 3."},{"at":{"i":3},"vars":{"total":-4,"javaRemainder":-1,"class":2,"count":3},"note":"The total is -4. Java's % gives -1 and the normalized class is 2, which occurred 0 times before, so the count is 3."}]}
```

<!-- stage: code -->
### Normalize Then Count Or Measure

```java
static int subarraysDivByK(int[] nums, int k) {
    int[] seen = new int[k];
    seen[0] = 1;
    int total = 0, count = 0;
    for (int x : nums) {
        total += x;
        int cls = Math.floorMod(total, k);
        count += seen[cls];
        seen[cls]++;
    }
    return count;
}

static boolean checkSubarraySum(int[] nums, int k) {
    Map<Integer, Integer> firstAt = new HashMap<>();
    firstAt.put(0, -1);
    long total = 0;
    for (int i = 0; i < nums.length; i++) {
        total += nums[i];
        int cls = (int) Math.floorMod(total, (long) k);
        Integer earlier = firstAt.get(cls);
        if (earlier == null) firstAt.put(cls, i);
        else if (i - earlier >= 2) return true;
    }
    return false;
}

static int longestDivisibleSpan(int[] nums, int k) {
    Map<Integer, Integer> firstAt = new HashMap<>();
    firstAt.put(0, -1);
    long total = 0;
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        total += nums[i];
        int cls = (int) Math.floorMod(total, (long) k);
        Integer earlier = firstAt.get(cls);
        if (earlier == null) firstAt.put(cls, i);
        else best = Math.max(best, i - earlier);
    }
    return best;
}
```

Each function scans the tape once at constant expected cost per number. The counting version uses an array of k counters, and the length versions use a map with at most k entries. Total is a `long` where the sum of many values could pass an `int`.

<!-- stage: applicability -->
### When Divisibility Joins Two Totals

Use remainder classes when a question asks whether the total of a stretch is a multiple of some number, or counts such stretches, and the total can be written as a difference of two running totals. The invariant is that two running totals are in the same class exactly when the stretch between them is divisible, and that every class is computed with `floorMod` so it is never negative.

A false friend is the plain `%` operator on a running total that can be negative, which sends equal classes to different keys and can even produce a negative array index. Another is storing the exact running totals, which treats totals that differ by a multiple of `k` as different, and so misses stretches. A third is mixing the two table roles: a count table cannot check a length rule, and a first-index table cannot count pairs.

In Java, call `Math.floorMod` with the same types on both sides, using `long` when the total is `long`. Make sure `k` is positive before dividing, since a zero divisor throws an `ArithmeticException`. Allocate the counter array to size `k`, and seed class zero before the loop, with a count of one for counting or index minus one for lengths.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-sums-divisible-k -->

**Prerequisites.** The prefix counts lesson, and integer remainders.

**Problem.** Given an integer array and a positive integer `k`, return the number of non-empty contiguous stretches whose sum is divisible by `k`. Use an array of `k` counters indexed by the normalized class of the running total, and add the counter of the current class before incrementing it.

**Constraints.** 1 <= nums.length <= 30000, -10000 <= nums[i] <= 10000, and 2 <= k <= 10000.

**Example 1.** Input `nums = [4, 5, 0, -2, -3, 1], k = 5`, output 7.

**Example 2.** Input `nums = [5], k = 9`, output 0.

**Hint.** When are two running totals the same class? What must be the count of class zero before any value is read?

**Changed decision.** First rung: the table is keyed by a remainder class instead of an exact total, so equal classes pair up.

#### [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-subarray-sum -->

**Prerequisites.** The Subarray Sums Divisible by K exercise above, and the earliest balance lesson.

**Problem.** Return true if some contiguous stretch of at least two numbers has a sum that is a multiple of `k`, and false otherwise. Store the first index of each class, and accept a repeated class only when the two indices are at least two apart.

**Constraints.** 1 <= nums.length <= 100000, 0 <= nums[i] <= 1000000000, and 1 <= k <= 2147483647. The running total may pass the range of `int`.

**Example 1.** Input `nums = [23, 2, 4, 6, 7], k = 6`, output true.

**Example 2.** Input `nums = [23, 2, 6, 4, 7], k = 13`, output false.

**Hint.** Why must the first index of a class be kept, and not the latest? What does a gap of exactly one mean?

**Changed decision.** The question is existence with a length rule, so the table stores the first index per class instead of a count.

#### [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-values -->

**Prerequisites.** The two exercises above.

**Problem.** Count the stretches whose sum is divisible by `k` on inputs with negative numbers, using `Math.floorMod`. Show that normalizing with a plain `%` operator breaks the count, either by throwing on a negative array index or by returning a wrong number.

**Constraints.** 1 <= nums.length <= 30000, -1000000000 <= nums[i] <= 1000000000, and 2 <= k <= 10000. Use `long` for the running total.

**Example 1.** Input `nums = [-3, 1, 2, -4], k = 3`, output 3.

**Example 2.** Input `nums = [-1, -1, 2], k = 3`, output 1.

**Hint.** What does `-2 % 3` return in Java? Which function always returns a value from zero to `k - 1`?

**Changed decision.** The running total may be negative, so every class is passed through `floorMod` before it is used as an index.

#### [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-longest-divisible-span -->

**Prerequisites.** All three exercises above.

**Problem.** Return the length of the longest contiguous stretch, of any positive length, whose sum is divisible by `k`, or zero if there is none. The question asks for a length, so the table holds the first index of each class, and a repeated class gives a candidate length.

**Constraints.** 1 <= nums.length <= 100000, -1000000000 <= nums[i] <= 1000000000, and 2 <= k <= 1000000000.

**Example 1.** Input `nums = [3, 1, 4, 1, 5], k = 5`, output 3.

**Example 2.** Input `nums = [1, 2], k = 5`, output 0.

**Hint.** Which earlier index of a class gives the longest stretch? Can `k` be too large for an array of counters?

**Changed decision.** The meaning of the table changes from a count of visits to the earliest index, and a map replaces the array when `k` is large.
