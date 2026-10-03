<!-- lesson-kind: standard -->
<!-- lesson-id: membership-sets -->
## Membership Sets

<!-- stage: context -->
### The Steward And The Filing Cabinet

An event steward stands at a door with a rule: every ticket number may be used once, and a second arrival with the same number is turned away. The first few guests are easy, because she can glance down a short list of used numbers. By the fortieth guest she is reading the whole list for every ticket, and by the four-thousandth the queue is out of the door.

So she changes the system. She puts a small filing cabinet beside the door and files each used ticket in a drawer chosen from its number, say by the last two digits. When a ticket arrives she opens one drawer, glances at the few slips inside, and knows. She never reads the other drawers. The question she asks is only whether this number has been used, and she does not care when, how often or in which order.

<!-- stage: naive -->
### Reread The Whole List Each Time

The plain way to keep the rule is to hold a list of used numbers and search it for every arrival.

```java
static boolean hasRepeatWithList(int[] tickets) {
    List<Integer> used = new ArrayList<>();
    for (int t : tickets) {
        if (used.contains(t)) return true;     // reads the list from the front
        used.add(t);
    }
    return false;
}
```

On `[4, 9, 2, 9]` it returns true when the second 9 arrives, because `contains` finds the first one. It is correct and easy to read.

<!-- stage: bottleneck -->
### The List Gets Longer Every Time

`List.contains` compares the new value with the stored ones from the front, so the work grows with the list. When no number repeats, the `i`-th arrival costs about `i` comparisons, and the total is O(n * n). For `n = 100,000` that is about five billion comparisons, which takes many seconds and is the difference between passing and timing out.

The structure is the problem, not the loop. A list remembers the order of arrival, which this question never uses, and the price of that unused memory is a full search for every query. The steward's cabinet works because it gives up the order and keeps only what the question needs, so that each query touches one small drawer.

<!-- stage: insight -->
### Remember Only That A Value Appeared

A **hash set** stores values so that asking whether one is present takes expected constant time, however many values it holds. It turns each value into a number, uses the number to choose a bucket, and inspects only that bucket, which is exactly the cabinet drawer. You do not need the mechanics to use it. You need three facts: adding is expected O(1), asking is expected O(1), and the set forgets both order and multiplicity.

The **seen set** is how you put it to work in a scan. It holds exactly the relevant values processed so far, so the invariant is that before reading `nums[i]`, the set equals the distinct values of `nums[0..i-1]`. The **membership test** is the question asked about the current value before it is added. A yes means a repeat has been found and the scan can stop. A no means the value joins the set and the scan moves on. In Java, `add` returns `false` when the value was already present, so the test and the insert become a single call.

<!-- names: hash set, seen set, membership test -->

What the set does not keep matters just as much. It cannot tell how many times a value occurred or at which index, so a question that needs either belongs to the next lessons. It also gives no order. When the question only asks whether something has appeared, a plain set is the smallest structure that answers it, and a map would carry a value that nobody reads.

<!-- stage: variables -->
### One Set And One Question Per Step

The set `seen` starts empty, which is correct for a prefix of length zero. At each step the current value is tested, and then it is added if the scan continues. For a question about two collections, one collection is loaded into a set first and the other is scanned against it, with a second set collecting the answers so that each shared value is reported once. For a question about a changing state, such as a number being transformed repeatedly, the states themselves are the values stored, and a repeated state proves a loop.

<!-- stage: trace -->
### Two Scans With A Seen Set

```trace
{"cells":[4,9,2,9],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":4,"seen":"{4}","answer":"new"},"note":"Test 4: not in the set, so add it. The set is now {4}."},{"at":{"i":1},"vars":{"value":9,"seen":"{4, 9}","answer":"new"},"note":"Test 9: not in the set, so add it. The set is now {4, 9}."},{"at":{"i":2},"vars":{"value":2,"seen":"{2, 4, 9}","answer":"new"},"note":"Test 2: not in the set, so add it. The set is now {2, 4, 9}."},{"at":{"i":3},"vars":{"value":9,"seen":"{2, 4, 9}","answer":"repeat"},"note":"Test 9: it is already in the set {2, 4, 9}. A repeat is found, so stop."}]}
```

Take the tickets `[4, 9, 2, 9]`. The first three values are new, so each one is added and the set grows to `{2, 4, 9}`. The fourth value, 9, is already in the set, so the test answers yes at index 3 and the method returns true without reading anything further.

```trace
{"cells":[2,4,16,37,58,89,145,42,20,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":2,"seen":"{2}","answer":"new"},"note":"Test 2: not in the set, so add it. The set is now {2}."},{"at":{"i":1},"vars":{"value":4,"seen":"{2, 4}","answer":"new"},"note":"Test 4: not in the set, so add it. The set is now {2, 4}."},{"at":{"i":2},"vars":{"value":16,"seen":"{2, 4, 16}","answer":"new"},"note":"Test 16: not in the set, so add it. The set is now {2, 4, 16}."},{"at":{"i":3},"vars":{"value":37,"seen":"{2, 4, 16, 37}","answer":"new"},"note":"Test 37: not in the set, so add it. The set is now {2, 4, 16, 37}."},{"at":{"i":4},"vars":{"value":58,"seen":"{2, 4, 16, 37, 58}","answer":"new"},"note":"Test 58: not in the set, so add it. The set is now {2, 4, 16, 37, 58}."},{"at":{"i":5},"vars":{"value":89,"seen":"{2, 4, 16, 37, 58, 89}","answer":"new"},"note":"Test 89: not in the set, so add it. The set is now {2, 4, 16, 37, 58, 89}."},{"at":{"i":6},"vars":{"value":145,"seen":"{2, 4, 16, 37, 58, 89, 145}","answer":"new"},"note":"Test 145: not in the set, so add it. The set is now {2, 4, 16, 37, 58, 89, 145}."},{"at":{"i":7},"vars":{"value":42,"seen":"{2, 4, 16, 37, 42, 58, 89, 145}","answer":"new"},"note":"Test 42: not in the set, so add it. The set is now {2, 4, 16, 37, 42, 58, 89, 145}."},{"at":{"i":8},"vars":{"value":20,"seen":"{2, 4, 16, 20, 37, 42, 58, 89, 145}","answer":"new"},"note":"Test 20: not in the set, so add it. The set is now {2, 4, 16, 20, 37, 42, 58, 89, 145}."},{"at":{"i":9},"vars":{"value":4,"seen":"{2, 4, 16, 20, 37, 42, 58, 89, 145}","answer":"repeat"},"note":"Test 4: it is already in the set {2, 4, 16, 20, 37, 42, 58, 89, 145}. A repeat is found, so stop."}]}
```

The second scan stores states instead of array values. Starting from 2 and repeatedly replacing the number with the sum of the squares of its digits gives 2, 4, 16, 37, 58, 89, 145, 42 and 20, all new. The next state is 4, which is already stored. The sequence has entered a loop, so it can never reach 1, and the scan stops after ten states instead of running forever.

<!-- stage: code -->
### Duplicates, Intersections And Loops

```java
static boolean hasDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int x : nums) {
        if (!seen.add(x)) return true;         // add returns false when x was already stored
    }
    return false;
}

static int[] intersection(int[] a, int[] b) {
    Set<Integer> inA = new HashSet<>();
    for (int x : a) inA.add(x);
    Set<Integer> shared = new TreeSet<>();
    for (int y : b) if (inA.contains(y)) shared.add(y);
    int[] out = new int[shared.size()];
    int k = 0;
    for (int v : shared) out[k++] = v;
    return out;
}

static boolean isHappy(int n) {
    Set<Integer> states = new HashSet<>();
    while (n != 1) {
        if (!states.add(n)) return false;      // a repeated state is a loop
        n = digitSquareSum(n);
    }
    return true;
}

static int digitSquareSum(int n) {
    int sum = 0;
    for (; n > 0; n /= 10) sum += (n % 10) * (n % 10);
    return sum;
}
```

Every input value is touched a fixed handful of times, which gives expected O(n) time and O(n) extra space. `hasDuplicate` can stop early, and `isHappy` is bounded because digit-square sums of numbers up to a few billion stay small, so only a few hundred distinct states can occur. The intersection uses a `TreeSet` for the answer only to give a deterministic order, which costs an extra logarithmic factor on the answer and is a choice, not a requirement.

<!-- stage: applicability -->
### When Only Presence Matters

Use a seen set when the decision depends on whether a value, a state or a coordinate has already appeared, and counts and positions are irrelevant. The invariant to say aloud is that the set equals the distinct values of the processed prefix. If you cannot say that sentence, the structure is probably holding the wrong thing.

The false friend is a map used for membership. A `HashMap<Integer, Boolean>` or a map whose values are never read does the same work with extra memory and extra noise, and it invites questions about values that do not exist. The opposite mistake is just as real: a set cannot answer "how many times", so a count question that reaches for a set loses the answer.

Java adds several hazards. `List.contains` and `String.contains` on a list are linear, so a list is not a set. A `HashSet<int[]>` compares arrays by identity, so two arrays with equal contents count as different values, and a record or a string key is the repair that Chapter 04 returns to. Boxed `Integer` values are compared with `equals` inside a set, and an `int` input needs boxing, which costs memory. Iteration order of a `HashSet` is unspecified, so sort or use a `TreeSet` when the output order matters.

<!-- stage: exercises -->
### Exercises

#### [Build] Contains Duplicate (LeetCode 217)
<!-- id: hm-contains-duplicate -->

**Prerequisites.** Chapter 01 loop invariants; the seen set in this lesson.

**Problem.** Given an integer array `nums`, return true if some value appears at least twice and false if every value is distinct. Do not modify the array, and stop as soon as the answer is known.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Expected linear time is the target.

**Example 1.** Input `nums = [3, 8, 5, 3]`, output true.

**Example 2.** Input `nums = []`, output false, because an empty array has no pair.

**Hint.** What single fact must be remembered after reading each value, and what is the cheapest structure that answers it?

**Changed decision.** First rung: the question needs presence only, so a set replaces the repeated search of a list.

#### [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: hm-intersection-arrays -->

**Prerequisites.** The build exercise above.

**Problem.** Given two integer arrays, return the distinct values that occur in both, in increasing order. A value that appears several times in either array is reported once.

**Constraints.** 0 <= nums1.length, nums2.length <= 10^4 and values lie in -10^6..10^6. Each input may contain repeats.

**Example 1.** Input `nums1 = [4, 9, 5, 9]`, `nums2 = [9, 4, 9, 8, 4]`, output `[4, 9]`.

**Example 2.** Input `nums1 = []`, `nums2 = [1]`, output `[]`.

**Hint.** Which array should be loaded into a set, and how do you avoid reporting a shared value twice?

**Changed decision.** The membership question now crosses two collections, and the answer itself must be a set of distinct values.

#### [Boundary] Happy Number (LeetCode 202)
<!-- id: hm-happy-number -->

**Prerequisites.** The two exercises above.

**Problem.** Repeatedly replace a positive integer with the sum of the squares of its digits. Return true if the process reaches 1, and false if it enters a loop that never reaches 1. The method must terminate on every input.

**Constraints.** 1 <= n <= 2^31 - 1. The state to remember is the current number. No recursion limit may be relied on.

**Example 1.** Input `n = 7`, output true, through 49, 97, 130, 10 and 1.

**Example 2.** Input `n = 4`, output false, since 4 leads to 16, 37, 58, 89, 145, 42, 20 and back to 4.

**Hint.** What would an unbounded loop do on input 4, and what repeated thing proves it is a loop?

**Changed decision.** The stored values are states of a process, and a repeat is evidence of an infinite loop.

#### [Recognize] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-consecutive -->

**Prerequisites.** All three exercises above.

**Problem.** Given an unsorted integer array, return the length of the longest run of values that are consecutive integers, such as 8, 9, 10, 11, in any order in the array. Values may repeat, and the target time is linear without sorting. Start counting only from a value whose predecessor is absent.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Sorting would cost O(n log n) and is not the intended route.

**Example 1.** Input `nums = [31, 8, 9, 30, 10, 32, 11]`, output 4, from 8, 9, 10, 11.

**Example 2.** Input `nums = [9, 9, 9]`, output 1, since repeats do not extend a run.

**Hint.** If you started counting from every value, how many times would the same run be counted? Which values can safely be skipped?

**Changed decision.** Membership tests of a neighbour value replace sorting, and the start-of-run test prevents repeated work.
