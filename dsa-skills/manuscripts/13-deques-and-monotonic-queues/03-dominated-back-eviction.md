<!-- lesson-kind: standard -->
<!-- lesson-id: dominated-back-eviction -->
## Dominated-Back Eviction

<!-- stage: context -->
### Parcels On A One-Way Belt

A depot has a conveyor belt that carries parcels past a packing table. Parcels are put on at one end in the order they arrive, and the belt moves them off at the other end in exactly the same order, so the first parcel to arrive is always the first to leave. The packer wants to know, at any moment, the weight of the heaviest parcel that is still somewhere on the belt.

She notices something while watching. Suppose a light parcel is on the belt and a heavier parcel is put on behind it. The light one will reach the end of the belt first, and when it leaves, the heavy one will still be there. For as long as the light parcel is on the belt, a heavier parcel is also on the belt. So the light parcel can never be the heaviest again, and she can stop keeping track of it. She wonders how much of the belt she really has to remember.

<!-- stage: naive -->
### Remember Every Parcel On The Belt

The direct method keeps every parcel in a list in order of arrival, and takes the maximum of the list whenever the packer asks for the heaviest.

```java
static int[] heaviestAfterEachArrival(int[] weights) {
    java.util.ArrayList<Integer> belt = new java.util.ArrayList<>();
    int[] answer = new int[weights.length];
    for (int i = 0; i < weights.length; i++) {
        belt.add(weights[i]);
        int heaviest = belt.get(0);
        for (int w : belt) heaviest = Math.max(heaviest, w);
        answer[i] = heaviest;
    }
    return answer;
}
```

It is correct. For the weights `[6, 1, 3]` it returns `[6, 6, 6]`.

<!-- stage: bottleneck -->
### Light Parcels Are Counted Needlessly

The list grows with every arrival, and each question scans all of it, so the total cost is about `n * n / 2`, which is O(n^2). For 100,000 parcels that is five billion weight comparisons. And most of those comparisons look at parcels that have no chance of ever being the answer: in the list `[6, 1, 3]` the weight 1 is checked three times although it is lighter than the 3 that arrived after it and will leave the belt before it.

The belt gives a reason to forget. A parcel that is lighter than a later arrival leaves first, so it is never the heaviest again. A list that discards such parcels at the moment the heavier one arrives would hold only parcels that still have a chance, and the heaviest of those would be easy to find if they were kept in a useful order.

<!-- stage: insight -->
### Discard What A Newcomer Outlives

A new entry at index `j` with value `v` makes an older entry at index `i < j` with value `u` a **dominated entry** when `u < v`, or `u <= v` if ties are given to the newer entry. The reason is the **outlast rule**: any window that contains `i` and ends at or after `j` also contains `j`, and `j` is at least as good as `i`, so `i` can never be the extreme value of any future window. The **safe discard** is therefore to remove such entries from the back of the deque before appending the new index, and to stop at the first entry that is not dominated.

This keeps one invariant: every stored index can still become the maximum of a future window, and every index that was popped could not. The values from front to back never increase, so the first entry is always the best one. The deque stores indices and not values, so that a later step can tell how old an entry is and tell equal values apart.

<!-- names: dominated entry, outlast rule, safe discard -->

The direction matters. For maximum queries a smaller older value is dominated. For minimum queries a smaller older value is the one that must be kept, because it is the better one, and it is the larger older values that are dominated. Discarding the wrong kind loses the answer, so the comparison is chosen from the query. The cost is O(n) over `n` arrivals, since every index is appended once and popped at most once.

<!-- stage: variables -->
### Indices, The Back And The Count Removed

The deque holds indices into the array, and the value of an entry is looked up as `a[index]`. The back is the newest surviving entry and the only place where domination is tested. The number of entries removed by an arrival can be anything from zero to the whole deque, and the sum of these numbers over the whole run is at most `n`, which is the amortized argument for the linear cost. When the problem allows equal values, decide whether an equal older entry is dominated before writing the comparison: using `<` keeps equal entries and `<=` replaces them. The front is read after the insertion, and in this lesson no entry expires, so the front is simply the best value seen so far.

<!-- stage: trace -->
### Heavy Parcels Clearing The Belt

Take the weights `5, 3, 4, 4, 2, 6` and look for the heaviest. Index 0 holds 5 and enters an empty deque. Index 1 holds 3, which does not beat the 5, so it is appended and nothing is removed. Index 2 holds 4, which beats the 3 at the back and not the 5, so index 1 is removed and index 2 is appended. Index 3 holds another 4, which does not beat the first 4, so both stay. Index 4 holds 2 and is appended. Index 5 holds 6, which beats every entry, so the whole deque of four indices is removed and index 5 stands alone. The step to study is the last one, where one heavy parcel clears everything behind it and makes the front change.

Now take the weights `4, 6, 2, 5, 5, 1` for the lightest, where an older larger value is dominated. The 6 is appended after the 4. The 2 beats the 6 and the 4 and clears the deque. The 5 is appended, the next 5 is kept next to it, and the 1 clears all three.

```trace
{"cells":[5,3,4,4,2,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","front_value":5,"removed":0},"note":"Index 0 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":1},"vars":{"deque":"[0,1]","front_value":5,"removed":0},"note":"Index 1 (value 3) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":2},"vars":{"deque":"[0,2]","front_value":5,"removed":1},"note":"Index 2 (value 4) removes index 1 from the back, since each has a value that 2 outlasts and beats. Then index 2 is appended."},{"at":{"i":3},"vars":{"deque":"[0,2,3]","front_value":5,"removed":0},"note":"Index 3 (value 4) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":4},"vars":{"deque":"[0,2,3,4]","front_value":5,"removed":0},"note":"Index 4 (value 2) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":5},"vars":{"deque":"[5]","front_value":6,"removed":4},"note":"Index 5 (value 6) removes index 4, 3, 2, 0 from the back, since each has a value that 5 outlasts and beats. Then index 5 is appended."}]}
```

```trace
{"cells":[4,6,2,5,5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","front_value":4,"removed":0},"note":"Index 0 (value 4) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":1},"vars":{"deque":"[0,1]","front_value":4,"removed":0},"note":"Index 1 (value 6) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":2},"vars":{"deque":"[2]","front_value":2,"removed":2},"note":"Index 2 (value 2) removes index 1, 0 from the back, since each has a value that 2 outlasts and beats. Then index 2 is appended."},{"at":{"i":3},"vars":{"deque":"[2,3]","front_value":2,"removed":0},"note":"Index 3 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":4},"vars":{"deque":"[2,3,4]","front_value":2,"removed":0},"note":"Index 4 (value 5) beats nothing at the back, so it is appended and nothing is removed."},{"at":{"i":5},"vars":{"deque":"[5]","front_value":1,"removed":3},"note":"Index 5 (value 1) removes index 4, 3, 2 from the back, since each has a value that 5 outlasts and beats. Then index 5 is appended."}]}
```

<!-- stage: code -->
### Insert With Domination

```java
static int insertMax(java.util.ArrayDeque<Integer> deque, int[] a, int i) {
    int removed = 0;
    while (!deque.isEmpty() && a[deque.peekLast()] < a[i]) {
        deque.removeLast();               // dominated: i outlasts it and is larger
        removed++;
    }
    deque.addLast(i);
    return removed;
}

static int insertMin(java.util.ArrayDeque<Integer> deque, int[] a, int i) {
    int removed = 0;
    while (!deque.isEmpty() && a[deque.peekLast()] > a[i]) {
        deque.removeLast();               // for minima, larger older entries are dominated
        removed++;
    }
    deque.addLast(i);
    return removed;
}
```

Each call is O(1) amortized, because every index is added once and removed at most once, and the deque occupies O(n) memory in the worst case of a strictly decreasing sequence for `insertMax`. The deque holds indices, so `a[deque.peekLast()]` unboxes the `Integer` to an `int` index before the array is read. The two methods differ only in the direction of one comparison, and exchanging them silently turns a maximum structure into a minimum one.

<!-- stage: applicability -->
### When Later Arrivals Replace Earlier Ones

Use domination from the back when a collection of entries leaves in arrival order, and the query is an extreme value over what remains. The invariant is that every stored index can still be the answer for some future state, and anything that was popped cannot, because a later and at-least-as-good entry outlasts it. Decide the direction of the comparison and the treatment of equal values from the question before coding.

The false friend is removing the wrong values. Popping smaller entries is safe for a maximum, and it is unsafe for a minimum, where the smaller entry is the better one and the newcomer cannot replace it. A second false friend is sorting the entries, which also exposes the best one but costs more and loses the arrival order that expiry will need in the next lessons. A third is a priority queue, which keeps every entry and needs stale entries to be removed lazily.

Do not use it when entries can leave in an order other than arrival order, because the outlast rule depends on the older entry leaving first. If a parcel could be taken from the middle of the belt, a light parcel could be the heaviest again. Do not use it either when the query needs more than the extreme value, such as the second largest. In Java, remember that the deque stores indices, so comparisons go through `a[...]`, and an equal-value policy has to be stated.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Maximum Candidate (Author exercise)
<!-- id: dq-insert-maximum-candidate -->

**Prerequisites.** The two previous lessons of this chapter.

**Problem.** Process the array `a` from left to right. For each index `i`, remove from the back of a deque of indices every index whose value is strictly smaller than `a[i]`, then append `i`. Return an array whose entry `i` is the number of indices removed at step `i`.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [6, 1, 3, 3, 8, 2, 5]`, output `[0, 0, 1, 0, 3, 0, 1]`.

**Example 2.** Input `a = [4, 4, 4]`, output `[0, 0, 0]`, since equal values are not strictly smaller.

**Hint.** What does the deque store, and which entry does the comparison read? When does the loop stop?

**Changed decision.** First rung: the deque stores indices, and every arrival removes the entries it strictly beats before it is appended.

#### [Vary] Insert Minimum Candidate (Author exercise)
<!-- id: dq-insert-minimum-candidate -->

**Prerequisites.** The Insert Maximum Candidate exercise above.

**Problem.** Process `a` from left to right. For each index `i`, remove from the back of a deque of indices every index whose value is strictly larger than `a[i]`, then append `i`. Return the indices in the deque, from front to back, after the last step.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [6, 1, 3, 3, 8, 2, 5]`, output `[1, 5, 6]`.

**Example 2.** Input `a = [9, 8, 7]`, output `[2]`, because every new value is smaller than the one before it.

**Hint.** Which comparison has to be reversed? Why is the value at the front the smallest of the stored ones?

**Changed decision.** The comparison is reversed, so that larger older values are dominated and the deque supports minima.

#### [Boundary] Repeated Equal Values (Author exercise)
<!-- id: dq-repeated-equal-values -->

**Prerequisites.** The two exercises above.

**Problem.** Run the maximum deque over `a` under two policies: keep equals, where a newcomer removes strictly smaller entries, and keep only the newest, where it removes smaller or equal entries. Return the largest size the deque reaches during the run under each policy, as `[keepEquals, keepNewest]`.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [7, 7, 7, 7, 7]`, output `[5, 1]`.

**Example 2.** Input `a = [1, 2, 3]`, output `[1, 1]`, since every value is strictly larger than the one before it and clears the deque under both policies.

**Hint.** What is the front value at every step under each policy? Which policy is safe if entries will later expire in arrival order?

**Changed decision.** Equality is the only thing that changes between the two runs, and the effect is on memory use, not on the answer.

#### [Recognize] Online Suffix Maximum Candidates (Author exercise)
<!-- id: dq-online-suffix-maximum -->

**Prerequisites.** All three exercises above.

**Problem.** Values arrive one at a time and nothing ever expires. After each arrival, report two numbers: the largest value seen so far, and the number of candidates the maximum deque holds, where a newcomer removes strictly smaller entries. Return the pairs in order.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Constant amortized time per arrival.

**Example 1.** Input `a = [2, 8, 3, 3, 1, 9, 4]`, output `[[2, 1], [8, 1], [8, 2], [8, 3], [8, 4], [9, 1], [9, 2]]`.

**Example 2.** Input `a = [7, 5, 5]`, output `[[7, 1], [7, 2], [7, 3]]`.

**Hint.** The candidates are exactly the values that no later value strictly exceeds. Which end of the deque holds the largest value so far?

**Changed decision.** The deque is read after every insertion with nothing expiring, so the front is the running maximum and the size is the number of surviving candidates.
