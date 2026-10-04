<!-- lesson-kind: standard -->
<!-- lesson-id: key-to-index-maps -->
## Remember Where A Value Appeared

<!-- stage: context -->
### Two Prices That Fill A Gift Card

A checkout page holds a gift card with a fixed balance, and the cart lists up to 100000 item prices. The page must find two cart items whose prices add up to exactly the balance, and it must report where the two items sit in the cart. The first version finds the pair on a small cart. On a full cart the page stalls for many seconds, and the second version finds the same pair at once.

A count or a yes-or-no answer does not help here, because the page must name positions. The question is what the program must remember about each earlier price so that one lookup finds its partner. A second question is which position to remember when a price occurs more than once.

<!-- stage: naive -->
### Trying Every Pair Of Items

The direct method tries each pair of positions, adds the two prices and compares the sum with the balance.

```java
static int[] twoSum(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) {
                return new int[] {i, j};
            }
        }
    }
    return new int[] {-1, -1};
}
```

On `[8, 2, 11, 3]` with balance 14 the method returns `[2, 3]`, because 11 and 3 add up to 14. When no pair works, the method returns `[-1, -1]`.

<!-- stage: bottleneck -->
### Every Price Searches All Later Prices

```predict
For each position i, which single number would let the program recognize the partner price, and why does the double loop still scan all later positions?

The partner of nums[i] must equal target - nums[i], which is one known number. The double loop does not use that number. It scans every later position and adds each price to nums[i], so a full cart costs O(n^2).
```

The inner loop answers the question "is there a later price equal to `target - nums[i]`" by trying every later price. That is a search for one known value. A scan is not needed for such a search when earlier values sit in a structure that finds a value directly. The method must also return a position, so the structure must keep the position next to each value. A scan of the cart once, with a stored position for each price already read, removes the inner loop.

<!-- stage: insight -->
### Store Each Value With Its Index

#### Look Up The Partner Before Storing

For a price `x`, the **complement** is `target - x`, the one price that completes the sum. The loop computes the complement of `nums[i]` and looks for it among the earlier positions. Looking up the complement before storing `nums[i]` has a purpose. A price must not pair with itself, and a cart `[3, 3]` with balance 6 holds two separate 3s. If the loop stored `3` first, the lookup would find the same position.

<!-- names: index map, complement, overwrite rule -->

#### Keep An Index Map

An **index map** is a map whose key is a value from the input and whose value is a position of that value. Java's `HashMap<Integer, Integer>` serves. After the iteration for index `i`, the map holds every value of `nums[0..i]` with one stored position for each. If the lookup of the complement succeeds, the stored position and `i` form the answer. If it fails, the loop stores `nums[i]` with position `i`.

#### Choose Which Position To Keep

A value can occur more than once, so the contract decides which position the map keeps. The **overwrite rule** states the choice. For Two Sum, either position of an equal pair gives a valid answer, because the first match ends the loop. For a question about the distance to the most recent equal value, the loop overwrites the entry with the newer position. For a question about the widest distance between equal values, the loop keeps the first position and does not overwrite. The contract names the meaning of the stored position, and the code follows that meaning.

#### What The Pass Costs

The loop makes one lookup and one store per position, each of expected constant time. The time is O(n) on average. The map holds up to n entries, so the space is O(n).

<!-- stage: variables -->
### Complement, Map And Position

Three values drive the pass.

- **complement** equals `target - nums[i]` and changes at every position.
- **map** holds each earlier value with its stored position and gains an entry when a lookup fails.
- **i** is the current position and increases by one at every iteration.

<!-- stage: trace -->
### Two Searches With One Map

#### Finding A Pair For The Balance

Take `nums = [8, 2, 11, 3]` and `target = 14`. At `i = 0` the price 8 has complement 6, which is not in the map, so the map stores 8 with position 0. At `i = 1` the price 2 has complement 12, which is missing, so the map stores 2. At `i = 2` the price 11 has complement 3, which is missing, so the map stores 11. At `i = 3` the price 3 has complement 11, which the map holds at position 2, so the answer is `[2, 3]`.

#### Keeping The Most Recent Position

The same map answers a different question. Take `nums = [5, 1, 5, 5]` and a limit `k = 1`. The question asks whether two equal values sit at most `k` positions apart. At `i = 2` the value 5 was last seen at position 0, a gap of 2, which is too wide. The loop overwrites the entry with position 2. At `i = 3` the value 5 was last seen at position 2, a gap of 1, so the answer is true.

#### Stepping Through Both Arrays

```trace
{"cells":[8,2,11,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":8,"complement":6,"map":"{}"},"note":"Value 8, complement 6, which is missing from the map. Store 8 at position 0."},{"at":{"i":1},"vars":{"value":2,"complement":12,"map":"{8@0}"},"note":"Value 2, complement 12, which is missing from the map. Store 2 at position 1."},{"at":{"i":2},"vars":{"value":11,"complement":3,"map":"{8@0, 2@1}"},"note":"Value 11, complement 3, which is missing from the map. Store 11 at position 2."},{"at":{"i":3},"vars":{"value":3,"complement":11,"map":"{8@0, 2@1, 11@2}"},"note":"Value 3, complement 11. The map holds 11 at position 2, so the answer is [2, 3]."}]}
```

```trace
{"cells":[5,1,5,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":5,"gap":"none","map":"{}"},"note":"Value 5 is new. Store it at position 0."},{"at":{"i":1},"vars":{"value":1,"gap":"none","map":"{5@0}"},"note":"Value 1 is new. Store it at position 1."},{"at":{"i":2},"vars":{"value":5,"gap":2,"map":"{5@0, 1@1}"},"note":"Value 5 was last seen at 0, a gap of 2, which is too wide. Overwrite its entry with 2."},{"at":{"i":3},"vars":{"value":5,"gap":1,"map":"{5@2, 1@1}"},"note":"Value 5 was last seen at 2, a gap of 1, which is within 1. Return true."}]}
```

<!-- stage: code -->
### An Index Map And One Pass

#### Finding The Pair

```java
static int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> at = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        Integer j = at.get(complement);
        if (j != null) {
            return new int[] {j, i};
        }
        at.put(nums[i], i);
    }
    return new int[] {-1, -1};
}
```

#### What The Method Costs

The loop runs n times, and each iteration does one `get` and at most one `put`, so the time is O(n) on average. The map holds at most n entries, so the space is O(n). The variable `j` has type `Integer` and not `int`, because `get` returns `null` for a missing key, and unboxing `null` into an `int` throws an exception.

<!-- stage: applicability -->
### When A Map Of Positions Fits

#### Look For One Earlier Partner

Use an index map when the current value needs one earlier location or one earlier complement immediately. Typical cases are a pair that adds to a target, the nearest earlier equal value, and the first occurrence of a value. The invariant is that the map holds, for each value read so far, the position that the contract names, either the first or the most recent. The contract must say which position the answer needs, and an unstated choice is the usual source of wrong answers.

#### Sorting Is A False Friend

A false friend here is sorting the array and then searching for the partner. Sorting moves values to new positions, so the answer no longer names the original positions. Sorting also costs O(n log n) in time. A task that asks only whether a pair exists can use sorting, but a task that returns original indexes needs the remembered positions.

#### Java Details That Cause Failures

The call `put` returns the previous value of the key, or `null` when the key was absent, so one call can both read and replace. The subtraction `target - nums[i]` can wrap around when the values span the whole 32-bit range, so the constraints below keep every value and the target within one billion.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum (LeetCode 1)
<!-- id: hm-two-sum -->

**Prerequisites.** The index map and the lookup before the store from this lesson.

**Problem.** Let `nums` be an array of integers and `target` an integer. Return the two indexes `i` and `j` with `i < j` and `nums[i] + nums[j] == target`. Exactly one such pair exists.

**Constraints.** The limits are:
- **Length** satisfies `2 <= nums.length <= 10^5`.
- **Values** and `target` satisfy `|value| <= 10^9`, and duplicates may occur.
- **Answer** holds two different indexes in increasing order.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [6, 2, 9, 4]`, `target = 10`, output `[0, 3]`.

**Example 2.** Input `nums = [5, 5]`, `target = 10`, output `[0, 1]`.

**Hint.** Which fact about an earlier value does the loop need, and what must it store alongside the value?

**Changed decision.** Basic case: a map from value to position replaces the inner loop.

#### [Vary] Contains Duplicate II (LeetCode 219)
<!-- id: hm-nearby-duplicate -->

**Prerequisites.** Two Sum above.

**Problem.** Let `nums` be an integer array and `k` a non-negative integer. Return true when two different indexes `i` and `j` satisfy `nums[i] == nums[j]` and `|i - j| <= k`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers.
- **Limit** satisfies `0 <= k <= 10^5`; a limit of 0 always gives false.
- **Answer** is a boolean.

**Example 1.** Input `nums = [7, 2, 7]`, `k = 1`, output false.

**Example 2.** Input `nums = [7, 2, 7]`, `k = 2`, output true.

**Hint.** Among all earlier positions of a value, which one gives the smallest gap to the current position?

**Changed decision.** The stored position is the most recent one, and the entry is overwritten.

#### [Boundary] First Index Wins (Author exercise)
<!-- id: hm-first-index-wins -->

**Prerequisites.** The two exercises above.

**Problem.** Let `nums` be an integer array and `queries` an integer array. For each query value, return its smallest index in `nums`, or -1 when the value does not occur.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length, queries.length <= 10^5`.
- **Values** are 32-bit integers, and `nums` may hold repeated values.
- **Answer** has the same length as `queries`.
- **Method** builds the map once and answers every query by one lookup.

**Example 1.** Input `nums = [4, 6, 4, 6, 6]`, `queries = [6, 4, 9]`, output `[1, 0, -1]`.

**Example 2.** Input `nums = []`, `queries = [3]`, output `[-1]`.

**Hint.** If the loop stored every position, which one would the map hold at the end, and which one does the answer need?

**Changed decision.** The map must keep the first position, so the loop stores a value only when it is absent.

#### [Recognize] Widest Equal-Value Pair (Author exercise)
<!-- id: hm-widest-pair -->

**Prerequisites.** All three exercises above.

**Problem.** Let `nums` be an integer array. Among all pairs of indexes `i < j` with `nums[i] == nums[j]`, return the largest value of `j - i`. Return 0 when no value occurs twice.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers.
- **Answer** is an `int` from 0 to `nums.length - 1`.
- **Method** makes one pass with one map.

**Example 1.** Input `nums = [3, 1, 4, 1, 5, 3]`, output 5, for the two 3s at indexes 0 and 5.

**Example 2.** Input `nums = [1, 2, 3]`, output 0.

**Hint.** For a fixed right index, which earlier index gives the widest gap?

**Changed decision.** The pass keeps the first position of each value and measures the distance at every later repeat.
