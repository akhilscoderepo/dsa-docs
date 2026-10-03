<!-- lesson-kind: standard -->
<!-- lesson-id: arrays-sort -->
## Arrays Sort

<!-- stage: context -->
### A Clerk And A Drawer Of Cards

A club clerk keeps membership cards in a drawer, each marked with a number. Twice a month she has to produce a tidy list from them: the numbers in increasing order, so she can spot a card that was filed twice. The drawer itself must stay as it is, because the treasurer's notes refer to cards by their position in the drawer.

So she never shuffles the drawer. She takes out a handful of cards, or all of them, lays them on the table, puts them in increasing order, and reads off the list. Sometimes the boss asks only about the cards between the third and seventh slot, and then she lifts out just that stretch. Once the cards are in order, a duplicate is easy to see: two cards with the same number must lie right next to each other.

<!-- stage: naive -->
### Compare Every Card With Every Other

Before the cards are in order, the only way to find a repeated number is to compare each card with every card after it. In Java that is a double loop over the array.

```java
static boolean hasRepeatByPairs(int[] cards) {
    for (int i = 0; i < cards.length; i++) {
        for (int j = i + 1; j < cards.length; j++) {
            if (cards[i] == cards[j]) return true;
        }
    }
    return false;
}
```

It is correct for every input, it does not modify the array, and it has no special cases for an empty drawer or a single card.

<!-- stage: bottleneck -->
### Every Pair Gets Looked At

Counting the pairs, a drawer of n cards needs n times n minus one over two comparisons when no card repeats, so the cost is O(n^2). Fifty thousand cards means more than a billion comparisons. Almost all of them are wasted, since two cards far apart in the drawer are compared even though a repeat is only ever interesting between cards that carry the same number.

There is a second cost that does not appear in the running time. A programmer who tries to speed this up by sorting the argument directly has changed the caller's data, and any code that still refers to positions in the original array now reads the wrong values. Such a bug does not crash. The result is a report that lists the right numbers in the wrong places. The sorting step needs a rule about who owns the array before it runs, and the range form of the call needs a rule about where the range stops.

<!-- stage: insight -->
### Sort A Copy, Then Look Next Door

Sorting turns a question about all pairs into a question about neighbors. Once the values are in nondecreasing order, any two equal values sit in one unbroken stretch, an **equal run**, so a repeat exists exactly when some adjacent pair is equal. The invariant after the call is stated for the whole array at once: every adjacent pair is in nondecreasing order, and each distinct value occupies one contiguous run.

Whether you may sort the argument itself is part of the problem's contract. If the caller needs the original order, make a **sorted copy** first, which costs O(n) extra memory and keeps the argument intact. If the contract allows modifying the input, sorting in place saves that memory. Both are legitimate; guessing is not.

For primitives, `Arrays.sort(int[])` uses the natural numeric order and needs no comparator. Nothing is lost by the missing tie rule here, since two equal ints cannot be told apart. The call also has a form for part of the array, and that form takes a **half-open range**: `Arrays.sort(a, from, to)` sorts the positions from `from` up to but not including `to`. A slice of length k is `to - from`, and the call with `from == to` is a legal no-op. The call throws an exception if `from > to` or if either bound is outside the array.

<!-- names: equal run, sorted copy, half-open range -->

Two edge cases deserve a name before they surprise you. An empty array and a one-element array are both already sorted, so a neighbor check over them has no pairs to examine and must answer "no repeat". And the neighbor check must compare with `==` or `<`, never by subtracting, for the same overflow reason as in the previous lesson.

<!-- stage: variables -->
### The Array, The Bounds And The Neighbor

The array `a` holds the working values, either the caller's own or a clone. In the range form, `from` is the first position included and `to` is the first position excluded, so the slice length is `to - from` and positions outside the slice never move. The scan uses an index `i` starting at 1 that compares `a[i - 1]` with `a[i]`. The only fact the scan needs from the earlier loop turns is that no equal pair has been seen yet, which is why a plain return inside the loop is enough.

<!-- stage: trace -->
### A Slice And A Neighbor Check

The first trace sorts only the slice from position 1 up to, but not including, position 5 of the array 9, 4, 7, 1, 8, 2. The two pointers mark where the slice begins and where it stops. Positions 0 and 5 hold 9 and 2 and never move, whatever happens inside. The last step shows the array after the call, with the slice in order and the ends unchanged.

```trace
{"cells":[9,4,7,1,8,2],"pointers":["from","to"],"steps":[{"at":{"from":1,"to":5},"vars":{"slice":"4,7,1,8","length":4},"note":"The call covers positions 1 up to but not including 5, so the slice is 4, 7, 1, 8 and its length is 4. Positions 0 and 5 are outside it."},{"at":{"from":1,"to":5},"vars":{"sortedSlice":"1,4,7,8"},"note":"Only the slice is put in order, giving 1, 4, 7, 8."},{"at":{"from":1,"to":5},"vars":{"array":"9,1,4,7,8,2","position0":9,"position5":2},"note":"The array after the call is 9, 1, 4, 7, 8, 2. The values 9 and 2 at the ends did not move."}]}
```

The second trace walks over a sorted copy of 8, 3, 6, 1, 6, 9, which is 1, 3, 6, 6, 8, 9, looking for equal neighbors. The scan starts at position 1 and compares each value with the one before it. The first two comparisons find different values, and the third finds two 6 values side by side. The step to study is that last one: the scan returns at once, because the run of equal values has been found and no later pair can change the answer.

```trace
{"cells":[1,3,6,6,8,9],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"previous":1,"current":3},"note":"Position 1 holds 3 and position 0 holds 1. They differ, so keep scanning."},{"at":{"i":2},"vars":{"previous":3,"current":6},"note":"Position 2 holds 6 and position 1 holds 3. They differ, so keep scanning."},{"at":{"i":3},"vars":{"previous":6,"current":6,"verdict":"repeat"},"note":"Position 3 holds 6 and position 2 holds 6. They are equal, so a repeat exists and the scan returns true here."}]}
```

<!-- stage: code -->
### Copy, Range And Neighbor Scan

```java
static boolean hasRepeat(int[] nums) {
    int[] work = Arrays.copyOf(nums, nums.length);
    Arrays.sort(work);
    for (int i = 1; i < work.length; i++) {
        if (work[i] == work[i - 1]) return true;
    }
    return false;
}

static int[] sortSlice(int[] nums, int from, int to) {
    int[] work = nums.clone();
    Arrays.sort(work, from, to);        // sorts [from, to), leaves the rest alone
    return work;
}

static boolean isNondecreasing(int[] a) {
    for (int i = 1; i < a.length; i++) {
        if (a[i - 1] > a[i]) return false;
    }
    return true;
}
```

Sorting dominates at O(n log n) time, the neighbor loop adds O(n), and the clone costs O(n) memory. `sortSlice` costs O(k log k) for a slice of length k, plus the clone. The sortedness check compares with `>` so it is safe at the extremes of the type, and it returns true for arrays of length 0 or 1 because the loop never runs.

<!-- stage: applicability -->
### When Sorting The Values Is Enough

Choose a plain sort of primitives when the question is about values and their order, not about where the values came from: repeats, the k-th smallest, the median, the closest pair. The invariant to rely on is that adjacent elements are in nondecreasing order and equal values are contiguous. Say in a comment whether the input may be modified, and sort a clone when it may not.

A false friend is a problem that sounds like sorting but asks about positions in the original array, such as "return the indexes of the two numbers that add to the target". After the sort the indexes are lost, so you need a different tool or you must carry the index along inside an object. Another is a custom order: `Arrays.sort(int[])` accepts no comparator, so any rule other than ascending numeric forces boxing or a different representation.

In Java, remember that the range bounds are inclusive at the start and exclusive at the end, and that an out-of-range or reversed pair raises an exception. The one-argument sort changes the array you pass, and the cost of cloning is worth paying whenever other code holds a reference to it.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort A Primitive Copy (Author exercise)
<!-- id: so-primitive-copy -->

**Prerequisites.** The ordering-contracts lesson; array cloning from Chapter 01.

**Problem.** Write a method that takes an `int[]` and returns a new array holding the same values in nondecreasing order, while the argument keeps its original contents and order. Show with a check that the argument was not changed.

**Constraints.** 0 <= nums.length <= 100000 and every `int` value is allowed. The result is a different array object from the argument.

**Example 1.** Input `nums = [6, 2, 9, 2]`, output `[2, 2, 6, 9]`, and `nums` is still `[6, 2, 9, 2]`.

**Example 2.** Input `nums = []`, output `[]`, a new empty array.

**Hint.** Which call duplicates an array, and which call sorts it? What happens to the caller's view if you skip the first step?

**Changed decision.** First rung: you decide who owns the array before sorting, and copy to keep the argument intact.

#### [Vary] Sort A Subrange (Author exercise)
<!-- id: so-subrange -->

**Prerequisites.** The primitive-copy exercise above.

**Problem.** Given an `int[]` and two bounds `from` and `to`, return a copy in which only positions from `from` up to but not including `to` are sorted ascending, and every other position keeps its value. Document the bounds in the method comment.

**Constraints.** 0 <= from <= to <= nums.length. When `from == to` the result equals the input. Reject bounds outside the array by letting the library raise its exception.

**Example 1.** Input `nums = [9, 4, 7, 1, 8, 2], from = 1, to = 5`, output `[9, 1, 4, 7, 8, 2]`.

**Example 2.** Input `nums = [3, 2, 1], from = 2, to = 2`, output `[3, 2, 1]`, since the slice is empty.

**Hint.** Is the position `to` part of the slice? What does a slice with `from` equal to `to` contain?

**Changed decision.** The sort now covers a slice, so the exclusive upper bound becomes part of the contract.

#### [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: so-empty-single-extreme -->

**Prerequisites.** The two exercises above.

**Problem.** Sort arrays that are empty, have one element, or contain `Integer.MIN_VALUE` and `Integer.MAX_VALUE`, and verify the result with a sortedness check that compares neighbors. Show that a check written as a subtraction wrongly rejects a correctly sorted array.

**Constraints.** 0 <= length <= 12. Any `int` value is allowed. The sortedness check must not subtract.

**Example 1.** Input `[Integer.MAX_VALUE, 0, Integer.MIN_VALUE]`, output `[Integer.MIN_VALUE, 0, Integer.MAX_VALUE]`.

**Example 2.** Input `[]`, output `[]`, and the check reports that it is sorted.

**Hint.** How many adjacent pairs does an array of length zero or one have? What does `Integer.MAX_VALUE - Integer.MIN_VALUE` evaluate to in 32-bit arithmetic?

**Changed decision.** The test data sits at the limits of both length and value, where a careless check or a subtraction fails.

#### [Recognize] Contains Duplicate (LeetCode 217)
<!-- id: so-contains-duplicate-sorted -->

**Prerequisites.** All three exercises above.

**Problem.** Return true if any value appears at least twice in the array, and false if all values are distinct. For this exercise the contract allows the method to reorder the argument, so sort it directly and look at adjacent pairs.

**Constraints.** 1 <= nums.length <= 100000 and -1000000000 <= nums[i] <= 1000000000. In-place sorting is allowed.

**Example 1.** Input `nums = [7, 3, 8, 3]`, output true.

**Example 2.** Input `nums = [4, 9, 1, 6]`, output false.

**Hint.** After sorting, where must two equal values be? How many pairs does the final scan need to examine?

**Changed decision.** The array is sorted in place, so the neighbor check replaces the pair loop and the argument pays the price.
