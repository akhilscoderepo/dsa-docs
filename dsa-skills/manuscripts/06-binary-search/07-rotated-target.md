<!-- lesson-kind: standard -->
<!-- lesson-id: rotated-target -->
## Rotated Target

<!-- stage: context -->
### A Magician Cuts The Deck

A magician lays out a deck of cards that was sorted by number, from 1 up to 52, and invites a guest to cut it. The guest lifts the top part and puts it underneath, so the deck now begins somewhere in the middle of the sequence, climbs to 52, jumps back to 1, and climbs again until it reaches the card just before the cut. The magician then asks the guest to name a number, and promises to say at which place in the cut deck that card lies.

Dealing the cards out one by one would find the card, but it would take as long as the deck is. The magician can look at any card instantly, and she knows the deck is two sorted runs glued together. Looking at the card in the middle, she can always tell which of the two ends of that card is a sorted stretch with no break in it. She also knows the range of numbers that stretch contains, so she can tell at once whether the named card could be in it.

<!-- stage: naive -->
### Deal Out The Cut Deck

The plain method looks at the cards one by one from the top.

```java
static int positionByDealing(int[] deck, int card) {
    for (int i = 0; i < deck.length; i++) {
        if (deck[i] == card) return i;
    }
    return -1;
}
```

It finds the card wherever it is, it reports minus one for a missing card, and it makes no use of the fact that the deck is two sorted runs.

<!-- stage: bottleneck -->
### The Cut Hides The Order

Dealing out is O(n) and for a missing card it examines every card. The earlier lesson found the position of the cut in O(log n), but knowing where the cut is does not by itself locate a card, because the deck is still not sorted from the top. A binary search that ignores the cut would compare the middle card with the target and go the wrong way for half of the possible targets.

What the magician needs is a rule that is correct at every step despite the cut. At each look she should be able to decide which half to keep without knowing where the cut is. That is possible because the break occurs in at most one of the two halves around the middle. The other half is an ordinary sorted run, and for an ordinary run one comparison with its first and last card says whether the target can be inside it. This gives O(log n) steps.

<!-- stage: insight -->
### One Half Is Always In Order

For a closed interval `[lo, hi]` in a rotated array with distinct values, at least one of the two halves on either side of `mid` contains no break. If `nums[lo] <= nums[mid]`, the left half `[lo, mid]` is the **sorted half**, because a break inside it would force `nums[mid]` to be smaller than `nums[lo]`. Otherwise the right half `[mid, hi]` is the sorted half. Identifying it takes one comparison.

The next step is the **range test**: a sorted half has a smallest element at one end and a largest at the other, so one more pair of comparisons tells whether the target lies in it. If it does, the search continues in that half, and if it does not, the target can only be in the other half, where the break is, and the search continues there. Either way the middle position is discarded after being compared with the target. The invariant is that the target, if present, is inside the interval, and each discarded part is proved not to contain it.

<!-- names: sorted half, range test, pivot index -->

An alternative is to find the **pivot index**, the position of the smallest element, using the search of the previous lesson. The pivot splits the array into two sorted pieces, and a plain exact search runs on whichever piece can contain the target: the target belongs to the right piece when it is at most the last element, and to the left piece otherwise. This uses two O(log n) searches in place of one, and each is a simple loop that can be checked separately.

Duplicates add the same ambiguity as before. When `nums[lo]`, `nums[mid]` and `nums[hi]` are all equal, neither half can be proved sorted, and the search cannot tell where the break is. If the middle is not the target, the two end elements cannot be the target either, since they are equal to it, so both ends can be dropped. That keeps the invariant, but removes only two positions per step, and a run of equal values makes the whole search O(n) in the worst case.

<!-- stage: variables -->
### Edges, Middle And The Sorted Half

`lo` and `hi` bound the closed interval that may contain the target, and `mid` is compared with the target first. The flag for the sorted half is derived from the comparison of `nums[lo]` with `nums[mid]`. The range test compares the target with the end values of the sorted half, where one end is included and the other, which is `mid`, is already excluded because it has just been compared. For the pivot approach the extra variable is the pivot index, and it fixes the two sorted pieces.

<!-- stage: trace -->
### Choosing The Half That Is In Order

The first trace looks for 0 in 4, 5, 6, 7, 0, 1, 2. At the first step the left half, from 4 to 7, is sorted, and 0 is not between them, so the search goes right. The step to study is the second, where the left half is now 0, 1 and the target 0 lies inside its range, so the right edge moves left and the third reading finds the target.

```trace
{"cells":[4,5,6,7,0,1,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":3},"vars":{"middle":7,"target":0},"note":"The left half 4 to 7 is sorted and the target 0 is outside its range, so lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"middle":1,"target":0},"note":"The left half 0 to 1 is sorted and the target 0 lies in its range, so hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":4},"vars":{"middle":0,"target":0},"note":"Position 4 holds 0, which equals the target 0. The search ends and reports position 4."}]}
```

The second trace allows repeats and looks for 0 in 1, 0, 1, 1, 1. At the first step the left, middle and right values are all 1, so no half can be proved sorted, and both ends are dropped. The step to study is the first one: it removes two positions without any information beyond the equality, and the search then proceeds as usual to find the 0.

```trace
{"cells":[1,0,1,1,1],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":4,"mid":2},"vars":{"middle":1,"target":0},"note":"The first, middle and last values are all 1, so neither half can be proved sorted. Drop both ends: lo becomes 1 and hi becomes 3."},{"at":{"lo":1,"hi":3,"mid":2},"vars":{"middle":1,"target":0},"note":"The left half 0 to 1 is sorted and the target 0 lies in its range, so hi becomes 1."},{"at":{"lo":1,"hi":1,"mid":1},"vars":{"middle":0,"target":0},"note":"Position 1 holds 0, which equals the target 0. The search ends and reports position 1."}]}
```

<!-- stage: code -->
### One Pass And Pivot Then Search

```java
static int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {                           // left half is sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {                                         // right half is sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}

static boolean searchWithRepeats(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return true;
        if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }       // ambiguous: drop both ends
        else if (a[lo] <= a[mid]) {
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}

static int pivotThenSearch(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;
        else hi = mid;
    }
    int pivot = lo;
    if (pivot == 0) { lo = 0; hi = a.length - 1; }
    else if (target >= a[0]) { lo = 0; hi = pivot - 1; }
    else { lo = pivot; hi = a.length - 1; }
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

The one-pass search and the pivot method are both logarithmic in time, with constant extra memory, for distinct values. The repeat-tolerant version drops to O(n) in the worst case because the ambiguous step removes only two elements. The pivot method does about twice as many halvings, since it finds the cut and then searches.

<!-- stage: applicability -->
### When The Cut Is Unknown

Use a rotated search when the array is a sorted array that was cut and swapped, and the question is about a target value, not only the cut. The invariant is the same as for exact search: the target, if present, lies in the interval. The new fact is the choice of half, which rests on the claim that at least one half around the middle is sorted, and that claim is only true for rotations of a sorted array.

A false friend is finding the minimum and stopping. The pivot index locates the cut, but the target still needs a search over one of the two pieces. Another false friend is the comparison of the target with the middle alone, as in exact search, which sends the search the wrong way when the middle lies in the other piece. A third is duplicates handled by the distinct-value code, which can discard the half that holds the target when the three sampled values are equal.

In Java, write the sorted-half test with `<=` against `nums[mid]`, so that a one-element left half counts as sorted, and write the range test with the target strictly less than `nums[mid]` on one side, since the middle has already been compared. When duplicates are allowed, compare the middle with the target before anything else, and say plainly in a comment that the ambiguous case costs linear time.

<!-- stage: exercises -->
### Exercises

#### [Build] Search in Rotated Sorted Array (LeetCode 33)
<!-- id: bs-rotated-search -->

**Prerequisites.** The rotated-minimum lesson and exact search.

**Problem.** A strictly increasing array was rotated at an unknown place. Return the index of the target, or minus one if it is absent. At each step decide which half is sorted, test whether the target can be in it, and discard only a half that cannot hold the target.

**Constraints.** 1 <= nums.length <= 5000, distinct values within the `int` range, and a target anywhere in the `int` range. Run in O(log n).

**Example 1.** Input `nums = [9, 11, 15, 2, 4, 6], target = 4`, output 4.

**Example 2.** Input `nums = [9, 11, 15, 2, 4, 6], target = 7`, output -1.

**Hint.** What does `nums[lo] <= nums[mid]` tell you about the left half? When the target is outside the range of the sorted half, where must it be?

**Changed decision.** First rung: the comparison with the middle value alone is not enough, so the search first identifies the half that is in order.

#### [Vary] Pivot Then Search (Author exercise)
<!-- id: bs-pivot-then-search -->

**Prerequisites.** The rotated-search exercise above, and the right-end test of the previous lesson.

**Problem.** Solve the same task in two phases. First find the rotation index with the right-end comparison. Then run an ordinary binary search on the sorted piece that can contain the target, and return its index in the original array.

**Constraints.** 1 <= nums.length <= 5000 and distinct values. The second phase must be a plain exact search over one piece, not over a rotated range.

**Example 1.** Input `nums = [9, 11, 15, 2, 4, 6], target = 11`, output 1.

**Example 2.** Input `nums = [5, 6, 1, 2, 3], target = 1`, output 2.

**Hint.** Which piece does the target belong to if it is at least the first element? What changes when the rotation index is zero?

**Changed decision.** The problem is split into finding the cut and searching a plain sorted piece, trading one clever loop for two simple ones.

#### [Boundary] Search in Rotated Sorted Array II (LeetCode 81)
<!-- id: bs-rotated-search-repeats -->

**Prerequisites.** The two exercises above.

**Problem.** The rotated array may contain repeated values. Return whether the target occurs. Handle the case in which the first, middle and last values are equal, where neither half can be proved sorted.

**Constraints.** 1 <= nums.length <= 5000 and values within the `int` range, nondecreasing before the rotation. State the worst-case cost in a comment.

**Example 1.** Input `nums = [1, 0, 1, 1, 1], target = 0`, output true.

**Example 2.** Input `nums = [3, 3, 3, 1, 3], target = 2`, output false.

**Hint.** If the middle is not the target and the three sampled values are equal, which positions can you drop? What does that do to the worst case?

**Changed decision.** Equal samples make the sorted half ambiguous, so the loop gives up both ends one step at a time.

#### [Recognize] Explain Both Strategies (Author exercise)
<!-- id: bs-explain-both-strategies -->

**Prerequisites.** All three exercises above.

**Problem.** Implement the one-pass sorted-half search and the pivot-then-search method for distinct values, check that they always agree, and count array reads for each. Then state in a comment the complexity of each strategy and the fact that each must prove before discarding a part.

**Constraints.** 1 <= nums.length <= 5000, distinct values, and any targets. Count reads of `nums` with a counter in the test harness.

**Example 1.** Input `nums = [9, 11, 15, 2, 4, 6], target = 15`, output 2 from both strategies.

**Example 2.** Input `nums = [9, 11, 15, 2, 4, 6], target = 1`, output -1 from both strategies.

**Hint.** What must be true about the interval for the one-pass search to discard half? What two facts does the pivot method rely on?

**Changed decision.** The task is to compare approaches, so correctness is shown by agreement and cost is shown by counting reads.
