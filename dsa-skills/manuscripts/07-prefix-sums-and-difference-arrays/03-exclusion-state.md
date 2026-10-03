<!-- lesson-kind: standard -->
<!-- lesson-id: exclusion-state -->
## Exclusion State

<!-- stage: context -->
### A Conveyor With A Bypass

A factory line has a row of stations, and each station multiplies the throughput of the line by its own factor: one doubles it, another triples it, another cuts it by a fifth. When a station breaks down, the foreman wants to know what the combined factor of the line would be with that station removed, which means the product of every other station's factor.

The foreman needs this number for each station in turn, so that the repair crew can be sent first to the station whose absence hurts the most. The line has thousands of stations, and the foreman wonders whether the answers can be produced without redoing the whole multiplication for every station.

<!-- stage: naive -->
### Multiply Everyone Else Each Time

The direct approach, for each station, is to multiply the factors of all the other stations.

```java
static long[] productsOfOthers(int[] factors) {
    int n = factors.length;
    long[] out = new long[n];
    for (int i = 0; i < n; i++) {
        long product = 1;
        for (int j = 0; j < n; j++) {
            if (j != i) product *= factors[j];
        }
        out[i] = product;
    }
    return out;
}
```

It is correct for any factors, including zeros and negative values, and it never divides by anything.

<!-- stage: bottleneck -->
### Every Station Redoes Almost The Same Product

For each of n stations the inner loop makes n - 1 multiplications, so the cost is O(n^2). With a hundred thousand stations that is ten billion multiplications, and each answer repeats nearly all the work of its neighbor: the product without station 5 and the product without station 6 share every other factor.

One shortcut is to multiply everything once and divide by the station's own factor. It is fast, and it is also fragile: a factor of zero makes the division impossible, and when two stations are zero, the shortcut has no way to tell that every answer is zero. A method that never divides is needed, and it comes from the shape of the answer: the product of the others is the product of everything to the left of the station times the product of everything to its right. Each of those two products can be built in one pass, so the whole answer costs O(n).

<!-- stage: insight -->
### Fold From Both Sides

Split the line at the station. The stations on its left form a group, and the stations on its right form another, and the answer for that station is the combination of the two groups. A **left pass** walks from the start and stores, at each position, the combination of everything before it. The value stored at position `i` is what the left pass knew before it read `a[i]`, so the station's own factor is never included. A **right pass** then walks from the end, carrying a **rolling suffix**, the combination of everything after the current position, and multiplies it into the stored value as it goes.

The state for this pattern is the pair of what lies strictly before and strictly after each position, which this chapter calls the **exclusion state**, and no division is needed because nothing was ever merged and then removed. The invariant after the left pass is that `out[i]` equals the product of `a[0]` through `a[i - 1]`, with the empty product equal to one. During the right pass, the invariant is that the rolling suffix equals the product of every element to the right of the current position, and the product is updated after the multiplication, not before it.

<!-- names: left pass, right pass, rolling suffix -->

For a sum, the answer is easier, because addition can be undone: total minus the value gives the sum of the others. The two-pass shape still works for sums, and it is the only shape that works for operations without an inverse, such as taking the largest value. For such an operation the left pass stores the best value strictly before each position, the right pass carries the best value strictly after it, and a single position can then ask about both sides without being included in either.

<!-- stage: variables -->
### Output Slots And A Single Carry

`out` holds one answer per position and is filled during the left pass with the combination of everything before the position. `carry` is a single variable used by the right pass: it starts as the identity of the operation, which is one for a product and zero for a sum, and after each position it absorbs that position's value. The identity matters because the first and the last positions have nothing on one side, and the empty side must contribute nothing. Products can grow quickly, so the type of `out` and `carry` is chosen from the stated bounds.

<!-- stage: trace -->
### One Walk Each Way

The first trace is the left pass for the factors 2, 3, 4, 5. The row of cells is the input, and the variables carry the product stored at each position. The step to study is the first: the stored value is one, the empty product, because nothing lies to the left of the first station.

```trace
{"cells":["2","3","4","5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stored":1,"factor":2},"note":"Store 1 at position 0, the product of everything before it, which is the empty product."},{"at":{"i":1},"vars":{"stored":2,"factor":3},"note":"Store 2 at position 1, the product of everything before it."},{"at":{"i":2},"vars":{"stored":6,"factor":4},"note":"Store 6 at position 2, the product of everything before it."},{"at":{"i":3},"vars":{"stored":24,"factor":5},"note":"Store 24 at position 3, the product of everything before it."}]}
```

The second trace is the right pass on the same factors, going from the last position to the first, with the rolling suffix starting at one. Pay attention to the third step: the suffix is 5 times 4, which is 20, and the stored value 2, the left part of the product, is multiplied by it to give 40, which is 2 times 4 times 5, with the 3 never merged in.

```trace
{"cells":["2","3","4","5"],"pointers":["i"],"steps":[{"at":{"i":3},"vars":{"suffix":1,"answer":24},"note":"The rolling suffix is 1, so position 3 becomes 24. Then the suffix absorbs 5."},{"at":{"i":2},"vars":{"suffix":5,"answer":30},"note":"The rolling suffix is 5, so position 2 becomes 30. Then the suffix absorbs 4."},{"at":{"i":1},"vars":{"suffix":20,"answer":40},"note":"The rolling suffix is 20, so position 1 becomes 40. Then the suffix absorbs 3."},{"at":{"i":0},"vars":{"suffix":60,"answer":60},"note":"The rolling suffix is 60, so position 0 becomes 60. Then the suffix absorbs 2."}]}
```

<!-- stage: code -->
### Two Passes And A Carry

```java
static long[] sumExceptSelf(int[] a) {
    long total = 0;
    for (int x : a) total += x;
    long[] out = new long[a.length];
    for (int i = 0; i < a.length; i++) out[i] = total - a[i];
    return out;
}

static int[] productExceptSelf(int[] a) {
    int n = a.length;
    int[] out = new int[n];
    int left = 1;
    for (int i = 0; i < n; i++) {
        out[i] = left;
        left *= a[i];
    }
    int right = 1;
    for (int i = n - 1; i >= 0; i--) {
        out[i] *= right;
        right *= a[i];
    }
    return out;
}

static int[][] bestOnEachSide(int[] a) {
    int n = a.length;
    int[] leftBest = new int[n], rightBest = new int[n];
    int best = -1;
    for (int i = 0; i < n; i++) {
        leftBest[i] = best;
        best = Math.max(best, a[i]);
    }
    best = -1;
    for (int i = n - 1; i >= 0; i--) {
        rightBest[i] = best;
        best = Math.max(best, a[i]);
    }
    return new int[][] {leftBest, rightBest};
}
```

Each function makes a constant number of passes over the input and uses O(1) extra space beyond the output. The product version assumes that every partial product fits in an `int`, as its exercise promises, and a larger range would need `long`.

<!-- stage: applicability -->
### When Every Position Needs The Rest

Use this when each output position needs the combination of every other element, or of everything strictly on each side. The invariant is that a position's stored value never includes the position's own element, because the stored value is recorded before the element is folded in. That ordering, record then fold, is the one thing to get right.

A false friend is division: the product of everything divided by the element is fast for a product with no zeros, and it breaks or returns nonsense when zeros are present, and it does not exist for operations like the maximum. Another false friend is a left pass alone, which gives the answer for a one-sided question and misses the other side. A third is a prefix table of the whole product, which includes the element itself and needs undoing.

In Java, choose the type from the bounds: an `int` product overflows silently, so say why it cannot, or use `long`. Start the carry at the identity of the operation, one for products and zero for sums, and a sentinel such as minus one for a maximum only when the contract keeps the values non-negative. Update the carry after using it, never before.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Prerequisites.** The prefix construction lesson, and `long` totals.

**Problem.** For each position, return the sum of all the other values. Addition can be undone, so the grand total minus the value gives the answer. Use `long`, because the grand total can pass the range of `int`.

**Constraints.** 1 <= nums.length <= 100000 and -1000000000 <= nums[i] <= 1000000000.

**Example 1.** Input `nums = [3, -1, 4]`, output `[3, 7, 2]`.

**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000]`, output `[2000000000, 2000000000, 2000000000]`.

**Hint.** What single number summarizes everything? What do you remove to exclude one position?

**Changed decision.** First rung: because addition has an inverse, the exclusion is one subtraction and no second pass is needed.

#### [Vary] Product of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Prerequisites.** The Sum Except Self exercise above.

**Problem.** Return an array in which position `i` holds the product of all the elements except the one at `i`, without using division. Build the products of everything on the left in one pass, then fold in a rolling product of everything on the right in a second pass.

**Constraints.** 2 <= nums.length <= 100000, -30 <= nums[i] <= 30, and every prefix or suffix product fits in a 32-bit integer.

**Example 1.** Input `nums = [2, 3, 4, 5]`, output `[60, 40, 30, 24]`.

**Example 2.** Input `nums = [-1, 2, -3]`, output `[-6, 3, -2]`.

**Hint.** What does the left pass leave in each slot? What must the right-pass variable contain before it is multiplied in?

**Changed decision.** Division is not allowed, so each answer is the product of a left part and a right part built in separate passes.

#### [Boundary] Product of Array Except Self With Zeros (LeetCode 238)
<!-- id: ps-product-with-zeros -->

**Prerequisites.** The two exercises above.

**Problem.** Take inputs that contain zeros: one zero, several zeros, or only zeros. Solve the product problem a second way, by counting the zeros and multiplying the non-zero values, then dividing only where it is safe, and check that the answers match the division-free passes. Show which input makes a plain divide fail.

**Constraints.** 2 <= nums.length <= 100000, -30 <= nums[i] <= 30, at least one zero in the tested inputs, and every product fits in a 32-bit integer.

**Example 1.** Input `nums = [0, 4, 5]`, output `[20, 0, 0]`.

**Example 2.** Input `nums = [0, 0, 3]`, output `[0, 0, 0]`.

**Hint.** If exactly one value is zero, which position is the only one with a non-zero answer? What if two are zero?

**Changed decision.** Zeros remove the inverse that division relies on, so a count of zeros decides the answer before any division happens.

#### [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-prefix-suffix-maximums -->

**Prerequisites.** All three exercises above.

**Problem.** For each position, return the largest value strictly to its left and the largest value strictly to its right, as two arrays, using minus one where a side is empty. The maximum has no inverse, so the answer cannot be recovered from a grand maximum, and each side needs its own pass.

**Constraints.** 1 <= nums.length <= 100000 and 0 <= nums[i] <= 1000000000, so minus one is safe as the marker for an empty side.

**Example 1.** Input `nums = [3, 9, 2, 7]`, output left `[-1, 3, 9, 9]` and right `[9, 7, 7, -1]`.

**Example 2.** Input `nums = [5]`, output left `[-1]` and right `[-1]`.

**Hint.** What is the maximum of nothing? Why can you not remove an element from a stored maximum?

**Changed decision.** The operation is a maximum with no inverse, so the exclusion state is built from two one-sided passes.
