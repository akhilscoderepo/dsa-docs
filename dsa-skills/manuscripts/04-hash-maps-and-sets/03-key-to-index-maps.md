<!-- lesson-kind: standard -->
<!-- lesson-id: key-to-index-maps -->
## Key To Index Maps

<!-- stage: context -->
### Two Books For One Gift Card

A bookshop clerk is helping a customer spend a gift card of exactly 35 dollars on two books. The shelf holds the books in a fixed order, and the customer wants to be told the two shelf positions. The clerk walks along the shelf. At each book she asks what price would complete the gift card, then glances at a notepad where she has been writing every price she has passed together with the shelf position where she saw it.

If the completing price is on the notepad, she is done and can read off both positions. If not, she writes the current price and position on the notepad and steps to the next book. The notepad never needs the books themselves, only a price and a position, and the question she asks at each step is always about one specific price.

<!-- stage: naive -->
### Pair Every Book With Every Later Book

The direct reading of the task is to try every pair of positions and see whether the prices add up.

```java
static int[] pairBySearch(int[] prices, int target) {
    for (int i = 0; i < prices.length; i++) {
        for (int j = i + 1; j < prices.length; j++) {
            if (prices[i] + prices[j] == target) return new int[] {i, j};
        }
    }
    return new int[] {};
}
```

On `[8, 2, 11, 3]` with target 14 it returns `[2, 3]`, since 11 and 3 are the only pair that works. It returns positions in the original order, which is what the customer needs.

<!-- stage: bottleneck -->
### A Search For Every Book

The nested loops test about `n * n / 2` pairs, so the time is O(n * n). With 100,000 books that is five billion additions, and most of them are for pairs that could not possibly work. At book `i` the code does not know what it is looking for, so it tries every later partner, although only one price would complete the sum.

There is a tempting shortcut that goes wrong. Sorting the prices would let two ends walk toward each other, but sorting destroys the shelf positions that the customer asked for, and carrying the positions along requires extra bookkeeping. The cleaner observation is that for each book the partner price is determined exactly, as the target minus the current price. The task is therefore not a search for a pair but a single lookup per book, if the earlier prices can be found by value.

<!-- stage: insight -->
### Remember Where Each Value Was Seen

An **index map** is a hash map whose keys are values from the input and whose entries are positions at which those values were seen. In Java it is a `HashMap<Integer, Integer>` from value to index. The **complement** of a value `x` is the value that would finish the job, here `target - x`. Reading `nums[i]`, you ask the map for the complement. If it is present, the stored index and `i` are the answer. If not, you store `nums[i]` with index `i` and move on.

The map entry has a meaning that the problem must decide, and that decision is the **index rule**. A value may occur several times, so the map can keep the earliest position, the latest position, or something else, and each choice answers a different question. Two Sum can use either, since any earlier match is acceptable. A nearby-duplicate question needs the latest position, because only the closest earlier copy can be within range, so each new sighting overwrites the old entry. A widest-gap question needs the earliest, so a later sighting must not overwrite. State the rule in a sentence before writing the code.

<!-- names: index map, complement, index rule -->

The order of the steps also matters. Look up the complement before storing the current value, so an element can never pair with itself. With `[3, 7, 3]` and target 6, the first 3 is stored, and only the second 3 finds it. The invariant is that before reading position `i`, the map holds every distinct value in `nums[0..i-1]`, each with the position chosen by the index rule.

<!-- stage: variables -->
### A Map From Value To Position

The map `at` has values as keys and positions as entries. It starts empty. The current value is `nums[i]`, and its complement is computed with plain subtraction, which stays within `int` for the stated value ranges. Each step does one lookup, then one store unless the answer was found. When the index rule is the earliest position, the store is skipped for keys already present, and when it is the latest position, the store always overwrites. The answer is built from a stored position and the current index, so the pair is always ordered with the earlier position first.

<!-- stage: trace -->
### Finding A Partner And Tracking Copies

```trace
{"cells":[8,2,11,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":8,"complement":6,"map":"{}"},"note":"Value 8, complement 6, which is not in the map. Store 8 at position 0."},{"at":{"i":1},"vars":{"value":2,"complement":12,"map":"{8@0}"},"note":"Value 2, complement 12, which is not in the map. Store 2 at position 1."},{"at":{"i":2},"vars":{"value":11,"complement":3,"map":"{8@0, 2@1}"},"note":"Value 11, complement 3, which is not in the map. Store 11 at position 2."},{"at":{"i":3},"vars":{"value":3,"complement":11,"map":"{8@0, 2@1, 11@2}"},"note":"Value 3, complement 11. The map holds 11 at position 2, so the answer is [2, 3]."}]}
```

Take prices `[8, 2, 11, 3]` and target 14. At index 0 the complement is 6, which is not stored, so 8 is stored with position 0. At index 1 the complement is 12, still absent, so 2 is stored. At index 2 the complement is 3, which has not appeared yet, so 11 is stored. At index 3 the value is 3 and its complement is 11, which is stored with position 2, so the answer is `[2, 3]`.

```trace
{"cells":[5,1,5,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":5,"gap":"none","map":"{}"},"note":"Value 5 is new. Store it at position 0."},{"at":{"i":1},"vars":{"value":1,"gap":"none","map":"{5@0}"},"note":"Value 1 is new. Store it at position 1."},{"at":{"i":2},"vars":{"value":5,"gap":2,"map":"{5@0, 1@1}"},"note":"Value 5 was last seen at 0, a gap of 2, which is too wide. Overwrite its entry with 2."},{"at":{"i":3},"vars":{"value":5,"gap":1,"map":"{5@2, 1@1}"},"note":"Value 5 was last seen at 2, a gap of 1, which is within 1. Return true."}]}
```

The second scan keeps only the latest position of each value, for a question about two equal values at most one step apart. The first 5 is stored at 0. The 1 is stored at 1. The next 5 is at index 2, and its stored partner is at 0, a gap of 2, which is too wide, so the entry is overwritten with 2. The final 5 at index 3 finds its partner at 2, a gap of 1, which is within range, and the answer is true. If the entry had not been overwritten, the check would have compared against position 0 and missed it.

<!-- stage: code -->
### Pairs, Windows And First Positions

```java
static int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> at = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        Integer j = at.get(target - nums[i]);          // look up the complement first
        if (j != null) return new int[] {j, i};
        at.put(nums[i], i);                            // then store the current value
    }
    return new int[] {};
}

static boolean nearbyDuplicate(int[] nums, int k) {
    Map<Integer, Integer> last = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        Integer j = last.get(nums[i]);
        if (j != null && i - j <= k) return true;
        last.put(nums[i], i);                          // overwrite: the latest copy is the closest one
    }
    return false;
}

static int[] firstOccurrence(int[] nums) {
    Map<Integer, Integer> first = new HashMap<>();
    int[] out = new int[nums.length];
    for (int i = 0; i < nums.length; i++) {
        first.putIfAbsent(nums[i], i);                 // keep the earliest position
        out[i] = first.get(nums[i]);
    }
    return out;
}
```

Each method makes one pass with expected constant work per element, giving expected O(n) time with O(n) space. The lookup uses `Integer` and compares with `null` instead of calling `containsKey` and `get` separately, which saves a second hash computation. `put` overwrites and `putIfAbsent` keeps the old entry, and the choice between them is exactly the index rule in code.

<!-- stage: applicability -->
### When A Past Position Answers The Question

Use an index map when the current element needs one earlier location, or one earlier value computed from the current one, and the answer is expressed in positions. Say the invariant plainly: the map holds each distinct processed value with the position chosen by the index rule. Name the rule, and name the check-before-store order.

The false friend is sorting. Sorting is a good tool when only values matter, but it rearranges positions, so a request for original indices needs bookkeeping that the map avoids. Another false friend is a frequency map, which knows how many but not where. If the problem asks where, store positions.

Java detail matters. `HashMap.get` returns an `Integer` that is `null` when the key is missing, and unboxing it into an `int` throws. Check for `null` first, as the code does. `put` and `putIfAbsent` differ in whether they keep the first position, so pick deliberately. When the complement `target - x` can overflow `int`, compute it as a `long`, and look it up in a `Map<Long, Integer>`. The stated constraints in the exercises keep it within range.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum (LeetCode 1)
<!-- id: hm-two-sum -->

**Prerequisites.** Chapter 01 index meaning; the index map in this lesson.

**Problem.** Given an integer array `nums` and an integer `target`, return the indices of two different positions whose values add up to `target`, smaller index first. Exactly one valid pair exists.

**Constraints.** 2 <= nums.length <= 10^5, -10^9 <= nums[i], target <= 10^9. The same position may not be used twice.

**Example 1.** Input `nums = [8, 2, 11, 3]`, `target = 14`, output `[2, 3]`.

**Example 2.** Input `nums = [4, 4]`, `target = 8`, output `[0, 1]`, since equal values at different positions are allowed.

**Hint.** What value completes the sum at each position, and where would the earlier copy of that value have been recorded?

**Changed decision.** First rung: the question at each step is a single lookup of a computed value, and the answer is a stored position.

#### [Vary] Contains Duplicate II (LeetCode 219)
<!-- id: hm-contains-duplicate-two -->

**Prerequisites.** The build exercise above.

**Problem.** Given an integer array `nums` and an integer `k`, return true if there are two different indices `i` and `j` with `nums[i] == nums[j]` and `|i - j| <= k`, and false otherwise.

**Constraints.** 0 <= nums.length <= 10^5 and 0 <= k <= 10^5. Values fit in `int`.

**Example 1.** Input `nums = [6, 2, 6]`, `k = 2`, output true.

**Example 2.** Input `nums = [6, 2, 3, 6]`, `k = 2`, output false, since the equal values are three apart.

**Hint.** Which earlier copy of the current value is the closest, and what should happen to the stored entry after each check?

**Changed decision.** The index rule changes to the latest position, so every sighting overwrites the previous entry.

#### [Boundary] First Index Wins (Author exercise)
<!-- id: hm-first-index-wins -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array, return an array of the same length in which entry `j` is the index of the first occurrence of `nums[j]`. Explain why storing the latest position instead would give a different answer.

**Constraints.** 0 <= nums.length <= 10^5. Values may repeat many times, and each value's earliest position must be kept.

**Example 1.** Input `nums = [7, 3, 7, 7]`, output `[0, 1, 0, 0]`.

**Example 2.** Input `nums = [5, 5, 5]`, output `[0, 0, 0]`, where an overwriting map would report the previous copy instead.

**Hint.** Which map call keeps an entry that is already there? What does `put` do on a repeated key?

**Changed decision.** The index rule is the earliest position, so a later sighting must be ignored instead of stored.

#### [Recognize] Widest Equal-Value Pair (Author exercise)
<!-- id: hm-widest-equal-pair -->

**Prerequisites.** All three exercises above.

**Problem.** Return the largest value of `j - i` over all pairs of positions `i < j` with `nums[i] == nums[j]`, or 0 if no value repeats. Store the first index of each value and compare it with the current position.

**Constraints.** 0 <= nums.length <= 10^5. Values fit in `int` and repeat arbitrarily.

**Example 1.** Input `nums = [4, 1, 9, 4, 2, 4]`, output 5, from the first and last 4.

**Example 2.** Input `nums = [1, 2, 3]`, output 0, because no value repeats.

**Hint.** For a fixed current position, which earlier copy gives the widest pair? What must the map therefore remember?

**Changed decision.** The earliest position answers a maximum-distance question, which the latest position of the previous lesson could not.
