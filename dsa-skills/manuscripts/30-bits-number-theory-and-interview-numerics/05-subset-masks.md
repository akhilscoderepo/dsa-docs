<!-- lesson-kind: standard -->
<!-- lesson-id: subset-masks -->
## Subset Masks

<!-- stage: context -->
### Why Listing Every Combination Gets Heavy

A release has 12 optional features, and the test team must try every combination of switched-on features. Each combination needs a record of which features it contains. The team also wants to ask quick questions about a combination, such as whether it contains the payment feature or whether it fits inside another combination.

A combination of features is a **subset** of the 12 features. A set of `n` items has `2^n` subsets, so 12 features give 4,096 combinations. The program must visit each one exactly once and hold each one in a form that is cheap to store and cheap to test. The goal below is a way to represent one subset in a single value and walks through all of them without lists, duplicates or recursion.

<!-- stage: naive -->
### Building Each Combination As A List

The direct approach keeps every combination as its own list of feature numbers. It starts with one empty list. For each feature in turn, it copies every list built so far and appends the feature to each copy. After the last feature, the collection holds all combinations.

```java
static List<List<Integer>> allCombinations(int n) {
    List<List<Integer>> all = new ArrayList<>();
    all.add(new ArrayList<>());                  // start with the empty combination
    for (int feature = 0; feature < n; feature++) {
        int sizeBefore = all.size();
        for (int j = 0; j < sizeBefore; j++) {
            List<Integer> copy = new ArrayList<>(all.get(j));   // copy an existing combination
            copy.add(feature);                                   // the copy gains one feature
            all.add(copy);
        }
    }
    return all;
}

static boolean fitsInside(List<Integer> small, List<Integer> big) {
    return big.containsAll(small);               // scans both lists to answer one question
}
```

After feature `k` is processed, the collection holds `2^(k+1)` lists. The method is correct, and for 12 features it returns 4,096 lists.

<!-- stage: bottleneck -->
### Lists Cost Memory And Time Per Question

```predict
A program builds all combinations of 20 features as separate lists. About how many list objects and stored feature numbers does it hold at the end?

About one million list objects and about ten million stored numbers. There are 2^20 combinations, and a combination holds 10 features on average. Each stored number is a boxed Integer reference, so the memory use is far larger than the count suggests.
```

#### Count The Objects

The collection holds `2^n` lists, and the lists hold `n * 2^(n-1)` feature numbers in total. For `n = 20` that is more than a million objects and ten million references. The construction copies each list once per later feature, so the work is O(n * 2^n). The count of subsets cannot shrink, because the answer itself has `2^n` members. The extra cost comes from storing each member as a heavy object.

#### Count The Cost Of One Question

The method `fitsInside` calls `containsAll`, which scans both lists. For lists of length up to `n`, one question costs O(n^2) with a plain list, because each lookup scans a list. A program that asks such a question for every pair of combinations multiplies this cost by `4^n` pairs. The structure we need stores one combination in a single machine word and answers a membership question or a containment question in O(1).

<!-- stage: insight -->
### Store Each Subset In One Integer

#### Give Every Item One Bit

A **subset mask** is an integer whose bit `i` is 1 exactly when item `i` belongs to the subset. With four items numbered 0 to 3, the mask `1011` in binary, which is 11 in decimal, holds items 0, 1 and 3. The empty subset is the mask 0. The mask with every bit set for `n` items is the **full mask**, and its value is `(1 << n) - 1`. As a plain membership value, an `int` holds up to 31 items and a `long` holds up to 63. A loop that counts from 0 to `(1 << n) - 1` needs `n` of at most 30 for an `int` and at most 62 for a `long`, because `1 << 31` is already negative. The invariant of this lesson is that bit `i` of the mask states whether item `i` is in the subset.

<!-- names: subset mask, full mask, submask -->

#### Walk The Counter From Zero To The Full Mask

Every pattern of `n` bits is one subset, and each pattern appears exactly once as the counter counts from 0 to `(1 << n) - 1`. A loop over that range therefore visits every subset once, with no duplicates and no recursion. The test "is item `i` in the subset" is `(mask >> i) & 1`. The subset with item `i` added is `mask | (1 << i)`, and the subset with item `i` removed is `mask & ~(1 << i)`. The test "is subset `a` inside subset `b`" is `(a & b) == a`. Each of these operations costs O(1).

#### Walk Only The Subsets Of One Mask

A **submask** of a mask `m` is a mask whose set bits are all set in `m`. If `m` has `p` set bits, it has exactly `2^p` submasks. The expression `(sub - 1) & m` moves from one submask to the next smaller one. Subtracting 1 turns the lowest set bit of `sub` into 0 and turns every lower bit into 1. The AND with `m` then clears the lower bits that `m` does not allow. Starting from `sub = m` and repeating until `sub` reaches 0 visits every submask in descending order. The loop must process 0 before it stops, because 0 is also a submask and `(0 - 1) & m` would return `m` again.

<!-- stage: variables -->
### Quantities To Track In The Loop

Track these items while the loops run.

- **n** is the number of items, and item `i` uses bit `i`.
- **mask** is the current subset, an integer from 0 to `(1 << n) - 1`.
- **full** is the value `(1 << n) - 1`, which holds every item.
- **sub** is the current submask when the loop walks the subsets of one mask `m`.
- **bit** is the value `1 << i` that selects item `i`.

The loops use `int` when `n` is at most 30 and `long` when `n` can reach 62. The shift `1 << n` on an `int` uses only the low five bits of `n`, so `1 << 32` equals 1 and not 4,294,967,296. A `long` version must write `1L << n`. This lesson keeps `n` at 30 or below, so every enumeration loop works with an `int`.

<!-- stage: trace -->
### Follow Both Loops On Small Inputs

The first trace counts through all masks for three items named `a`, `b` and `c`. Item `a` uses bit 0, item `b` uses bit 1 and item `c` uses bit 2. The second trace walks the submasks of the mask 11, which is `1011` in binary.

#### Count Through All Masks

The cells hold the masks 0 to 7 in order. Each step reads the bits of the current mask from the lowest bit up and names the items whose bits are set. The step for mask 5 shows the idea. In binary 5 is `101`, so bits 0 and 2 are set, and the subset holds `a` and `c`.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["mask"],"steps":[{"at":{"mask":-1},"vars":{"size":0},"note":"The counter has not started. The loop will visit the 8 masks from 0 to 7."},{"at":{"mask":0},"vars":{"size":0},"note":"Mask 0 is 000 in binary. No bit is set, so this is the empty subset."},{"at":{"mask":1},"vars":{"size":1},"note":"Mask 1 is 001 in binary. Its set bits select a."},{"at":{"mask":2},"vars":{"size":1},"note":"Mask 2 is 010 in binary. Its set bits select b."},{"at":{"mask":3},"vars":{"size":2},"note":"Mask 3 is 011 in binary. Its set bits select a and b."},{"at":{"mask":4},"vars":{"size":1},"note":"Mask 4 is 100 in binary. Its set bits select c."},{"at":{"mask":5},"vars":{"size":2},"note":"Mask 5 is 101 in binary. Its set bits select a and c."},{"at":{"mask":6},"vars":{"size":2},"note":"Mask 6 is 110 in binary. Its set bits select b and c."},{"at":{"mask":7},"vars":{"size":3},"note":"Mask 7 is 111 in binary. Its set bits select a and b and c. This is the full mask, and the loop ends after it."}]}
```

#### Walk The Submasks Of 1011

The mask 11 has three set bits, so it has eight submasks. The loop starts at 11 and repeats the update `sub = (sub - 1) & 11`. The first update turns 11 into 10, because subtracting 1 clears bit 0 and bit 0 is allowed by 11. The update from 8 differs: subtracting 1 from `1000` gives `0111`, which is 7, and the AND with `1011` clears bit 2 and leaves 3. That jump skips 7, 6, 5 and 4, which are not submasks of 11. The loop ends after it processes 0.

```trace
{"cells":[11,10,9,8,3,2,1,0],"pointers":["k"],"steps":[{"at":{"k":-1},"vars":{"m":11},"note":"The mask is 11, which is 1011 in binary. The loop starts with sub equal to 11."},{"at":{"k":0},"vars":{"sub":11,"next":10},"note":"The submask is 11, which is 1011 in binary. The update (sub - 1) & 11 computes (11 - 1) & 11 and gives 10."},{"at":{"k":1},"vars":{"sub":10,"next":9},"note":"The submask is 10, which is 1010 in binary. The update (sub - 1) & 11 computes (10 - 1) & 11 and gives 9."},{"at":{"k":2},"vars":{"sub":9,"next":8},"note":"The submask is 9, which is 1001 in binary. The update (sub - 1) & 11 computes (9 - 1) & 11 and gives 8."},{"at":{"k":3},"vars":{"sub":8,"next":3},"note":"The submask is 8, which is 1000 in binary. The update (sub - 1) & 11 computes (8 - 1) & 11 and gives 3. The subtraction gives 7, and the AND clears the bits that 11 does not allow."},{"at":{"k":4},"vars":{"sub":3,"next":2},"note":"The submask is 3, which is 0011 in binary. The update (sub - 1) & 11 computes (3 - 1) & 11 and gives 2."},{"at":{"k":5},"vars":{"sub":2,"next":1},"note":"The submask is 2, which is 0010 in binary. The update (sub - 1) & 11 computes (2 - 1) & 11 and gives 1."},{"at":{"k":6},"vars":{"sub":1,"next":0},"note":"The submask is 1, which is 0001 in binary. The update (sub - 1) & 11 computes (1 - 1) & 11 and gives 0."},{"at":{"k":7},"vars":{"sub":0,"next":-1},"note":"The submask is 0, the empty subset. The loop processes it and then stops."}]}
```

<!-- stage: code -->
### Implement Both Loops

```java
final class SubsetLoops {
    static long countSubsetsWithSum(int[] w, int target) {
        int n = w.length;
        long count = 0;
        for (int mask = 0; mask < (1 << n); mask++) {          // each pattern of n bits is one subset
            long sum = 0;
            for (int i = 0; i < n; i++) {
                if (((mask >> i) & 1) == 1) {                    // bit i says item i is inside
                    sum += w[i];
                }
            }
            if (sum == target) count++;
        }
        return count;
    }

    static List<Integer> submasks(int m) {
        List<Integer> out = new ArrayList<>();
        for (int sub = m; ; sub = (sub - 1) & m) {              // next smaller submask of m
            out.add(sub);
            if (sub == 0) break;                                 // stop after 0, or the loop never ends
        }
        return out;
    }
}
```

The first method does O(n * 2^n) work, because each of the `2^n` masks scans `n` bits. The second method does O(2^p) steps for a mask with `p` set bits and one O(1) update per step. The explicit `break` replaces a loop condition such as `sub > 0`, which would stop before the submask 0 is processed. The `int` masks stay non-negative because `n` is at most 30.

<!-- stage: applicability -->
### When Subset Masks Apply

#### Recognize The Pattern

Reach for a mask when the universe holds at most about 20 items and the answer depends on which items are chosen together. Typical signals are a statement that asks for every subset, a count of selections that satisfy a rule, or a small limit such as `n <= 20`. The invariant to state before coding is that bit `i` of the mask means item `i` is chosen. Every update must keep that meaning, and every test must read it.

The cost sets the limit. A loop over all masks does `2^n` iterations, so `n = 20` gives about one million and `n = 30` gives over a billion. Per-mask work of `n` steps multiplies that by `n`. Beyond roughly 25 items, a plain enumeration does not finish in a normal time limit.

#### Watch For The Nearest False Friend

Recursive backtracking is a false friend. It also visits every subset and often suits the same limits. Choose backtracking when the program must prune early, such as stopping a branch whose sum is already too large. Choose the mask loop when the program needs the whole subset as a value, for example as a key for a table or a state in a search, or when it asks containment questions between subsets.

#### Avoid The Java Shift Traps

The expression `1 << n` is an `int` shift, and for `n = 31` it produces the negative number `Integer.MIN_VALUE`. For `n = 32` it equals 1. Use `1L << n` whenever `n` can exceed 30, and keep the mask in a `long`. Write `(mask >> i) & 1` with parentheses, because `==` binds tighter than `&` in Java. The shift `>>` keeps the sign bit, so use `>>>` when a mask can be negative and the program must read the top bit as data.

<!-- stage: exercises -->
### Exercises

#### [Build] Enumerate All Masks (Author exercise)
<!-- id: bt05-subset-sum-count -->

**Prerequisites.** The subset mask and the bit test from this lesson.

**Problem.** Given an integer array `w` and an integer `target`, count the subsets of the positions of `w` whose elements add up to `target`. The empty subset has sum 0. Two subsets that pick different positions count separately, even when their values are equal.

**Constraints.** The limits are:
- **`n`** is the length of `w`, an `int` with `0 <= n <= 20`.
- **Values** are `int` values with absolute value at most 1,000.
- **`target`** is an `int` with absolute value at most 20,000.
- **Return** is a `long`.
- **Mutation** of `w` is not allowed.

**Example 1.** Input `w = [3,1,4,2]` and `target = 5`, output 2, from the subsets at positions 0 and 3 (3 + 2) and at positions 1 and 2 (1 + 4).

**Example 2.** Input `w = [0,2,-2]` and `target = 0`, output 4, because the empty subset, the zero, the pair 2 and -2, and all three positions each sum to 0.

**Hint.** Which bit of the mask says that item `i` is inside, and what does the empty mask contribute?

**Changed decision.** Baseline case: one loop over all masks replaces the lists of the direct approach.

#### [Vary] Subsets (LeetCode 78)
<!-- id: bt05-subset-list -->

**Prerequisites.** The previous exercise and the submask update from this lesson.

**Problem.** LeetCode 78 asks for all subsets of an array in any order. This version changes the contract. Given an array `nums` of distinct integers and a mask `m`, where bit `i` of `m` allows position `i`, return only the subsets that use allowed positions. Produce one list per submask of `m`, in descending order of the submask value. Each list holds the chosen elements in increasing position order.

**Constraints.** The limits are:
- **`n`** is the length of `nums`, an `int` with `1 <= n <= 10`.
- **Values** are distinct `int` values with absolute value at most 100.
- **`m`** is an `int` with `0 <= m < 2^n`.
- **Return** is a `List<List<Integer>>` with `2^p` lists for `p` set bits of `m`.

**Example 1.** Input `nums = [7,-2,5]` and `m = 5`, which is 101 in binary, output [[7,5],[5],[7],[]], from the submasks 5, 4, 1 and 0.

**Example 2.** Input `nums = [4]` and `m = 0`, output `[[]]`, because the only submask is 0 and it selects no element.

**Hint.** Which update moves from one submask to the next smaller one, and when does the loop stop?

**Changed decision.** The walk covers only the set bits of a given mask, and the output order is fixed.

#### [Boundary] Exponential Budget (Author exercise)
<!-- id: bt05-exponential-budget -->

**Prerequisites.** The cost discussion in the applicability stage.

**Problem.** A program enumerates every subset of `n` items and spends `n` basic steps on each subset, so the total is `n * 2^n` steps. Given a step budget `budget`, return the largest integer `n >= 0` such that `n * 2^n <= budget`. The product for `n = 0` is 0.

**Constraints.** The limits are:
- **`budget`** is a `long` with `1 <= budget <= 10^12`.
- **Return** is an `int` with `0 <= n <= 40`.
- **Arithmetic** uses `long` values, and `1L << n` gives `2^n`.

**Example 1.** Input `budget = 1000`, output 7, since 7 * 128 = 896 fits and 8 * 256 = 2,048 does not.

**Example 2.** Input `budget = 1000000000000`, output 34, since 34 * 2^34 = 584,115,552,256 fits and 35 * 2^35 = 1,202,590,842,880 does not.

**Hint.** The product grows with every step of `n`. Start at `n = 0`, compute the next product `(n + 1) * (1L << (n + 1))`, and stop before the first product that exceeds `budget`. For a budget up to 10^12 the largest product the loop forms is near 10^13, so a `long` holds it.

**Changed decision.** The question moves from enumerating subsets to deciding whether enumeration is affordable, so the program compares a step count with a budget.

#### [Recognize] Shortest Path Visiting All Nodes (LeetCode 847)
<!-- id: bt05-walk-all-nodes -->

**Prerequisites.** The first three exercises above.

**Problem.** LeetCode 847 asks for the shortest walk that visits every node of a graph. That task needs a search over visited sets, which a later lesson teaches. This version changes the contract to a mask-only check. An undirected graph has nodes `0` to `n - 1`. The array `adj` holds one mask per node, and bit `j` of `adj[i]` is 1 exactly when nodes `i` and `j` share an edge. Given a candidate route, a list of nodes, return `true` exactly when every two consecutive nodes of the route share an edge and the route visits every node at least once.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 30`.
- **`adj`** is symmetric, and bit `i` of `adj[i]` is 0.
- **Route** holds between 1 and 1,000 nodes, each in `0` to `n - 1`.
- **Repeats** of nodes and edges inside the route are allowed.
- **Return** is a `boolean`.

**Example 1.** Input `adj = [14,1,1,1]`, a star whose center is node 0, and `route = [1,0,2,0,3]`, output `true`. The route `[1,0,2]` gives `false`, because node 3 is never visited.

**Example 2.** Input `adj = [2,1,0]`, where nodes 0 and 1 share an edge and node 2 is alone, and `route = [0,1,0]`, output `false`. The steps are valid, but node 2 is missing from the visited set.

**Hint.** Keep one visited mask and one test per step. Which AND tells whether the next node is a neighbor of the current node, and which comparison tells that the visited mask is full?

**Changed decision.** The task checks one given route and does not search for the best one, so the state is a single visited mask and no queue is needed.
