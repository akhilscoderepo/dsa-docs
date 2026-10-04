<!-- lesson-kind: standard -->
<!-- lesson-id: amortized-cost -->
## Amortized Analysis Of Operation Sequences

<!-- stage: context -->
### Why Occasional Resizing Distorts Worst-Case Cost

A growable array backs a request log. It starts with capacity 1. When the array is full, an append allocates an array of twice the capacity and copies every stored element. Most appends write one value and take constant time. Occasionally an append copies every stored element.

Ask how long one append takes, and two accurate answers exist. The worst single append copies all stored elements, so it costs O(n). A typical append writes one value, so it costs O(1). A time limit built on the worst single append is far too pessimistic. A time limit that ignores the resizing appends is wrong. Software shows the same pattern whenever a structure repairs or resizes itself now and then, as hash table rehashing does. We need a way to state the cost of a whole sequence of operations without ignoring either kind of append.

<!-- stage: naive -->
### Multiplying The Worst-Case Cost By n

The cautious approach to cost takes the most expensive single operation and multiplies it by the number of operations. Here is that approach applied to a growing array that copies everything when it fills.

```java
static long worstCasePerAppend(long appends) {
    long perAppend = appends;          // an append may copy up to every stored element
    return perAppend * appends;
}
```

For one million appends, the method reports a total of about one trillion steps. That number rests on a real fact and a wrong multiplication. The real fact is that a single append can copy a lot. The wrong multiplication assumes that every append does.

<!-- stage: bottleneck -->
### Worst-Case Bound Overstates Total Cost

#### Compare The Bound With The Count

The worst-case product is O(n^2), and for `n = 1,000,000` it gives 10^12. A doubling array that performs that many appends actually makes roughly one million copies, which is O(n). The claim is wrong by a factor of about a million. A team that believed it would reject a sound design.

#### Find The Flawed Assumption

The mistake is treating the expensive operation as if it happened every time. After a doubling copy of `c` elements, the array has `c` empty slots. The next `c` appends cost almost nothing before another copy is needed. The expensive resizes are rare, and each one creates capacity for many later cheap appends. The opposite danger is just as real. An array that grows by one slot each time really does cost O(n^2) in total, because every append copies everything. The worst-case bound is accurate for that policy and wrong for doubling.

<!-- stage: insight -->
### Defining Amortized Cost Over A Sequence

#### Define Amortized Cost

The right question is not what the most expensive call costs. Ask instead what a long sequence of calls costs in total, divided evenly by the number of calls. That average over a worst-case sequence is the **amortized cost** per operation. It is a guarantee about whole sequences, with no randomness and no assumption about typical inputs.

#### Apply The Accounting Method

One way to compute it is to let cheap operations store **credit** that a later expensive operation uses. Charge every append three units. One unit pays for writing the new value, and you save the other two. A doubling from capacity `c` to `2c` copies `c` elements. It happens only after `c / 2` appends since the previous doubling, because the array held `c / 2` elements right after that doubling. Those `c / 2` appends each saved two units, so `c` units are waiting. That is exactly the price of the copy.

<!-- names: amortized cost, credit, potential -->

#### Apply The Potential Method

Another view uses a **potential**, a function of the structure's state that measures the work stored for later operations. For the doubling array, take the potential as `2 * size - capacity`. It is near 0 right after a resize and rises by 2 with each cheap append. A resize copies `size` elements and returns the potential to a small constant. Both views say the same thing: the total charged cost always covers the total actual cost, so the average is constant.

The invariant behind every amortized argument is that, over any sequence of operations, the total amount charged is at least the total actual work done. The invariant does not say that any single call is cheap.

<!-- stage: variables -->
### Size, Capacity And Copy Count

Track these quantities for the growing array.

- **size** counts the values the array holds.
- **capacity** counts the slots the array allocates.
- **resize** happens exactly when `size` equals `capacity` and one more value arrives.
- **copy count** totals the elements that resizes have moved so far.
- **copy count divided by `n`** is the ratio the amortized claim bounds after `n` appends.

The ratio stays bounded under doubling and grows without limit under grow-by-one.

<!-- stage: trace -->
### Copy Counts For Eight Appends

#### Appends One To Four

Start with capacity 1.

- **Append 1** finds one free slot and writes, so no copy happens.
- **Append 2** finds the array full, grows the capacity to 2, copies the single stored element and writes.
- **Append 3** finds capacity 2 full, grows to 4 and copies two elements.
- **Append 4** fits without any work.

#### Append Five Triggers The Largest Resize

The fifth append triggers the largest resize so far.

- **Append 5** finds capacity 4 full, grows to 8 and copies four elements.
- **Appends 6 to 8** fit without copying.
- **Capacities** are 1, 2, 4 and 8.
- **Total copies** are 1 + 2 + 4, which is 7 for eight appends and fewer than one per append.

The hardest step is the fifth, where one append copies four elements and the total still stays linear. Every doubling gives the array as many free slots as it copied elements, so as many cheap appends follow. That pattern is the mechanism behind the bound.

```trace
{"cells":[1,2,3,4,5,6,7,8],"pointers":["size","cap"],"steps":[{"at":{"size":1,"cap":1},"vars":{"capacity":1,"copiedNow":0,"totalCopies":0},"note":"Append 1: a free slot exists, so it just writes. No copy. Total copies 0."},{"at":{"size":2,"cap":2},"vars":{"capacity":2,"copiedNow":1,"totalCopies":1},"note":"Append 2: the array was full, so it grows to capacity 2 and copies 1 element, then writes. Total copies 1."},{"at":{"size":3,"cap":4},"vars":{"capacity":4,"copiedNow":2,"totalCopies":3},"note":"Append 3: the array was full, so it grows to capacity 4 and copies 2 elements, then writes. Total copies 3."},{"at":{"size":4,"cap":4},"vars":{"capacity":4,"copiedNow":0,"totalCopies":3},"note":"Append 4: a free slot exists, so it just writes. No copy. Total copies 3."},{"at":{"size":5,"cap":8},"vars":{"capacity":8,"copiedNow":4,"totalCopies":7},"note":"Append 5: the array was full, so it grows to capacity 8 and copies 4 elements, then writes. Total copies 7."},{"at":{"size":6,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 6: a free slot exists, so it just writes. No copy. Total copies 7."},{"at":{"size":7,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 7: a free slot exists, so it just writes. No copy. Total copies 7."},{"at":{"size":8,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 8: a free slot exists, so it just writes. No copy. Total copies 7."}]}
```

<!-- stage: code -->
### Simulating Doubling And Grow-By-One Policies

```java
static long copiesForAppends(int appends, boolean doubling) {
    int capacity = 1, size = 0;
    long copies = 0;
    for (int k = 0; k < appends; k++) {
        if (size == capacity) {
            capacity = doubling ? capacity * 2 : capacity + 1;
            copies += size;                    // every stored element is moved to the new array
        }
        size++;
    }
    return copies;
}
```

The loop mirrors what a growable array does when a value arrives. The condition `size == capacity` is the only place a resize happens. The cost of that resize is the number of elements already stored. Switching the policy flag changes the capacity update and leaves the accounting identical. Both runs take O(appends) time to simulate. The counts they return differ enormously: linear for doubling and quadratic for growing by one.

<!-- stage: applicability -->
### When Amortized Analysis Applies

#### Recognize The Pattern

Reach for amortized reasoning when all three conditions hold.

- **Usual cost** of the operation is small.
- **Occasional resize or repair** does a large amount of work.
- **Repair** creates room for many cheap calls afterward.

Typical cases are growable arrays, hash table resizing, and a queue built from two stacks, which a later chapter uses. The invariant is that the total charged cost over any sequence of operations pays for the total actual cost.

#### Check The Amortized Guarantee

A false friend in amortized analysis is a bound that looks like a per-call guarantee but only holds for the whole sequence. Here it is an amortized O(1) bound read as worst-case O(1) for every call.

- **Amortized O(1)** is not worst-case O(1), and one call can still take O(n).
- **Latency-sensitive loops** cannot accept that single slow call.
- **Total-cost problems** are unaffected, because only the sum over many calls counts.
- **Random-input average** is a different notion, since amortized analysis is a worst-case statement about a sequence.

#### Check Java's ArrayList

Java's `ArrayList` documents that `add` runs in amortized constant time, so an interview answer should say amortized and not constant. The growth policy matters. Growth by a fixed number of slots loses the guarantee, while growth by any constant factor above one keeps it.

<!-- stage: exercises -->
### Exercises

#### [Build] Doubling Array (Author exercise)
<!-- id: pc-doubling-array -->

**Prerequisites.** The size, capacity and copy-count bookkeeping in this lesson.

**Problem.** A dynamic array stores `size` values in a block of `capacity` slots. It starts empty with capacity 1. An append writes one value at position `size`. If `size == capacity` before the write, the array first allocates a block of twice the capacity and copies every stored value into it. Given a number of appends `n`, return the list of capacities that occur, in order, and the total number of element copies. Then state how the total compares with `n`. The expected result is that the total stays proportional to `n`.

**Constraints.** `n` is an `int` with `1 <= n <= 10^6`. Capacity starts at 1, and the initial capacity counts as the first capacity in the list. A resize multiplies the capacity by 2. A resize copies each stored value once, so it costs `size` copies at that moment. The write of the new value is not a copy. The total is a `long`. Only appends occur, with no removals.

**Example 1.** Input 8 appends, output capacities 1, 2, 4, 8 and a total of 7 copies.

**Example 2.** Input 1 append, output capacity 1 and 0 copies, since the first value fits without any resize.

**Hint.** Which appends find the array full? How many elements are stored at the moment of each resize?

**Changed decision.** Baseline case: turns the idea of occasional repair into a concrete tally of copies.

#### [Vary] Grow By One (Author exercise)
<!-- id: pc-grow-by-one -->

**Prerequisites.** The doubling-array exercise above.

**Problem.** Use the dynamic array from the previous exercise, but change the resize rule. When the array is full, the new capacity is the old capacity plus one. Given a number of appends `n`, return the total number of element copies. Show that the total equals `1 + 2 + ... + (n-1)`, and explain why the cost per append becomes O(n) amortized and not O(1).

**Constraints.** `n` is an `int` with `1 <= n <= 10^5`. Capacity starts at 1 and grows by exactly 1 when the array is full. Copies follow the same rule as in the doubling exercise: a resize copies each stored value once, and the write of the new value is not a copy. The total is a `long`, because it reaches about `5 * 10^9`. Only appends occur.

**Example 1.** Input 8 appends, output 28 copies, compared with 7 for doubling.

**Example 2.** Input 1 append, output 0 copies, so the two policies agree on the smallest sequence.

**Hint.** With growth by one, how often is the array full, and how many elements are stored each time? What does the sum of the first `n - 1` integers equal?

**Changed decision.** Only the growth rule changes, and it converts a linear total into a quadratic one.

#### [Boundary] One Expensive Append (Author exercise)
<!-- id: pc-one-expensive-append -->

**Prerequisites.** The two exercises above.

**Problem.** Use the doubling array from the first exercise. Perform 1,025 appends. Identify the one append in this sequence that copies the most elements, and report how many elements it copies and how many elements all earlier appends copied together. Then explain why this single O(n) append does not contradict the claim that appends cost O(1) amortized over the whole sequence.

**Constraints.** Capacity starts at 1 and doubles when `size == capacity`. A resize copies each stored value once, and the write of the new value is not a copy. The sequence has exactly 1,025 appends, so the final append is the one to examine. The counts are `long` values. Only appends occur.

**Example 1.** Input 1,025 appends, output that append number 1,025 copies 1,024 elements while the 1,024 appends before it copied 1,023 elements in total.

**Example 2.** Input 1,024 appends, output no spike at the end, since capacity 1,024 is exactly full and no further append has arrived.

**Hint.** When is the array full after exactly a power of two values? How many copies came from all the earlier resizes combined?

**Changed decision.** The question moves from the total to a single spike, and the exercise asks you to explain why one costly call does not break the average.

#### [Recognize] Potential Intuition (Author exercise)
<!-- id: pc-potential-intuition -->

**Prerequisites.** All three exercises above.

**Problem.** Start from the same doubling array that the first exercise defines. Give each append a charge of 3 units. One unit pays for the write, and the other 2 units go into a credit balance. A resize from capacity `c` to `2c` costs `c` units, taken from the balance. The appends after a resize save credit for the next resize. Show with numbers that the balance never becomes negative, so a charge of 3 units per append is enough. Use plain arithmetic and no formal algebra.

**Constraints.** The charge is exactly 3 units per append: 1 unit to write and 2 units saved. A resize from capacity `c` to `2c` happens when `size == c` and costs `c` units. The balance starts at 0, and all quantities are whole units. Capacity starts at 1 and only appends occur.

**Example 1.** Input a resize from capacity 4 to 8 after four stored values, output that the two appends since the previous resize saved 4 units and the copy costs 4.

**Example 2.** Input the very first resize from capacity 1 to 2 after one stored value, output that the one earlier append saved 2 units and the copy costs 1, so a unit is even left over.

**Hint.** After a resize to capacity `2c`, how many appends can happen before the next resize? How many units does each of those appends save?

**Changed decision.** The argument shifts from counting copies to explaining why the counted total is bounded, using stored credit.
