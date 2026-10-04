<!-- lesson-kind: standard -->
<!-- lesson-id: amortized-cost -->
## Amortized Cost

<!-- stage: context -->
### Why Occasional Resizing Distorts Cost

You rent a storage unit for boxes and start with one that holds a single box. When the unit fills, you rent a unit twice the size and carry every box across. Most days you simply add a box, which takes seconds. Occasionally the unit is full, and the whole afternoon goes to moving.

Ask how long adding a box takes, and two honest answers exist. The worst single day takes as long as the whole move. The typical day takes seconds. A budget that plans every day around the worst afternoon is absurdly pessimistic. A budget that ignores the move days is wrong. Software shows the same pattern whenever a structure repairs or resizes itself now and then. We need a way to price a whole sequence of operations without lying about either kind of day.

<!-- stage: naive -->
### Price Every Operation At Its Worst

The cautious approach to cost takes the most expensive single operation and multiplies it by the number of operations. Here is that approach applied to a growing array that copies everything when it fills.

```java
static long worstCasePerAppend(long appends) {
    long perAppend = appends;          // an append may copy up to every stored element
    return perAppend * appends;
}
```

For one million appends, the method reports a total of about one trillion steps. That number rests on a real fact and a wrong multiplication. The real fact is that a single append can copy a lot. The wrong multiplication assumes that every append does.

<!-- stage: bottleneck -->
### The Estimate Is Off By A Million

#### Compare The Estimate With The Count

The worst-case product is O(n^2), and for `n = 1,000,000` it gives 10^12. A doubling array that performs that many appends actually makes roughly one million copies, which is O(n). The claim is wrong by a factor of about a million. A team that believed it would reject a perfectly good design.

#### Find The Flawed Assumption

The mistake is treating the expensive operation as if it happened every time. After a doubling copy of `c` elements, the array has `c` empty slots. The next `c` appends cost almost nothing before another copy is needed. The expensive events are rare, and they pay for themselves by creating room. The opposite danger is just as real. An array that grows by one slot each time really does cost O(n^2) in total, because every append copies everything. The pessimistic estimate is accurate for that policy and wrong for doubling.

<!-- stage: insight -->
### Spread The Repair Over The Calls

#### Define Amortized Cost

The right question is not what the most expensive call costs. Ask instead what a long sequence of calls costs in total, divided evenly by the number of calls. That average over a worst-case sequence is the **amortized cost** per operation. It is a guarantee about whole sequences, with no randomness and no assumption about typical inputs.

#### Save Credit For The Resize

One way to compute it is to let cheap operations deposit **credit** that the expensive one later spends. Charge every append three units. One unit pays for writing the new value, and you save the other two. A doubling from capacity `c` to `2c` copies `c` elements. It happens only after `c / 2` appends since the previous doubling, because the array held `c / 2` elements right after that doubling. Those `c / 2` appends each saved two units, so `c` units are waiting. That is exactly the price of the copy.

<!-- names: amortized cost, credit, potential -->

#### Measure Potential

Another view uses a **potential**, a stored quantity that measures how much prepaid work sits in the structure. For the doubling array, the unused slots after a resize are prepaid room. A cheap append lowers that potential by one slot. The resize converts the used-up potential into a new batch of empty slots. Both views say the same thing: the total charged cost always covers the total actual cost, so the average is constant.

The invariant behind every amortized argument is that, over any sequence of operations, the total amount charged is at least the total actual work done. The invariant does not say that any single call is cheap.

<!-- stage: variables -->
### Size, Capacity And Copies

Track three numbers for the growing array. The size counts the values the array holds. The capacity counts the slots the array allocates. A resize happens exactly when the size equals the capacity and one more value arrives. The copy count is the total number of elements that resizes have moved so far. The amortized claim compares the copy count after `n` appends with `n` itself. You can watch that ratio stay bounded under doubling and grow without limit under grow-by-one.

<!-- stage: trace -->
### Eight Appends Into A Doubling Array

#### Early Appends

Start with capacity 1. The first append finds one free slot and writes, so no copy happens. The second append finds the array full, grows the capacity to 2, copies the single stored element and then writes. The third append finds capacity 2 full, grows to 4 and copies two elements. The fourth append fits without any work.

#### The Fifth Append

The fifth append triggers the largest repair so far. Capacity 4 is full, so the array grows to 8 and copies four elements. Appends six, seven and eight then fit for free. The capacities are 1, 2, 4 and 8, and the copies total 1 + 2 + 4, which is 7 for eight appends. That is fewer than one copy per append. The hardest step is the fifth, where one append copies four elements and the total still stays linear. Every doubling gives the array as many free slots as it copied elements, so as many cheap appends follow. That pattern is the mechanism behind the bound.

```trace
{"cells":[1,2,3,4,5,6,7,8],"pointers":["size","cap"],"steps":[{"at":{"size":1,"cap":1},"vars":{"capacity":1,"copiedNow":0,"totalCopies":0},"note":"Append 1: a free slot exists, so it just writes. No copy. Total copies 0."},{"at":{"size":2,"cap":2},"vars":{"capacity":2,"copiedNow":1,"totalCopies":1},"note":"Append 2: the array was full, so it grows to capacity 2 and copies 1 element, then writes. Total copies 1."},{"at":{"size":3,"cap":4},"vars":{"capacity":4,"copiedNow":2,"totalCopies":3},"note":"Append 3: the array was full, so it grows to capacity 4 and copies 2 elements, then writes. Total copies 3."},{"at":{"size":4,"cap":4},"vars":{"capacity":4,"copiedNow":0,"totalCopies":3},"note":"Append 4: a free slot exists, so it just writes. No copy. Total copies 3."},{"at":{"size":5,"cap":8},"vars":{"capacity":8,"copiedNow":4,"totalCopies":7},"note":"Append 5: the array was full, so it grows to capacity 8 and copies 4 elements, then writes. Total copies 7."},{"at":{"size":6,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 6: a free slot exists, so it just writes. No copy. Total copies 7."},{"at":{"size":7,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 7: a free slot exists, so it just writes. No copy. Total copies 7."},{"at":{"size":8,"cap":8},"vars":{"capacity":8,"copiedNow":0,"totalCopies":7},"note":"Append 8: a free slot exists, so it just writes. No copy. Total copies 7."}]}
```

<!-- stage: code -->
### A Growth Policy With A Counter

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

The loop mirrors what a growable array does when a value arrives. The condition `size == capacity` is the only place a resize happens. The cost of that resize is the number of elements already stored. Switching the policy flag changes the capacity update and leaves the accounting identical, which is the point of the exercise. Both runs take O(appends) time to simulate. The counts they return differ enormously: linear for doubling and quadratic for growing by one.

<!-- stage: applicability -->
### When An Average Is A Guarantee

#### Recognize The Pattern

Reach for amortized reasoning when an operation is usually cheap but sometimes does a large repair, and the repair creates room for many cheap calls afterward. Typical cases are growable arrays, hash table resizing, and a queue built from two stacks, which a later chapter uses. The invariant is that the total charged cost over any sequence of operations pays for the total actual cost.

#### Avoid The False Friend

The false friend is the word amortized itself. Amortized O(1) is not worst-case O(1) for every call, and one unlucky call can still take O(n). That matters when a single slow call is unacceptable, as in a latency-sensitive loop. It does not matter when only the total over many calls counts. Amortized analysis is also not an average over random inputs. It is a worst-case statement about a sequence.

#### Check Java's ArrayList

Java's `ArrayList` documents that `add` runs in amortized constant time, so an interview answer should say amortized and not constant. The growth policy matters. Growth by a fixed number of slots loses the guarantee, while growth by any constant factor above one keeps it.

<!-- stage: exercises -->
### Exercises

#### [Build] Doubling Array (Author exercise)
<!-- id: pc-doubling-array -->

**Prerequisites.** The size, capacity and copy-count bookkeeping in this lesson.

**Problem.** Start with capacity 1 and append eight values, doubling the capacity whenever the array is full. List the capacities that occur, count every element copy, and observe that the total stays proportional to the number of appends.

**Constraints.** Capacity starts at 1 and doubles on demand. A copy moves each stored element once and the new value's write is not counted as a copy.

**Example 1.** Input 8 appends, output capacities 1, 2, 4, 8 and a total of 7 copies.

**Example 2.** Input 1 append, output capacity 1 and 0 copies, since the first value fits without any resize.

**Hint.** Which appends find the array full? How many elements are stored at the moment of each resize?

**Changed decision.** First rung: turns the idea of occasional repair into a concrete tally of copies.

#### [Vary] Grow By One (Author exercise)
<!-- id: pc-grow-by-one -->

**Prerequisites.** The doubling-array exercise above.

**Problem.** Repeat the experiment when the capacity increases by exactly one each time the array is full. Sum `1 + 2 + ... + (n-1)` and explain why append becomes O(n) amortized instead of O(1).

**Constraints.** Capacity starts at 1 and grows by 1 on demand. Copies follow the same counting rule as the doubling exercise.

**Example 1.** Input 8 appends, output 28 copies, compared with 7 for doubling.

**Example 2.** Input 1 append, output 0 copies, so the two policies agree on the smallest sequence.

**Hint.** With growth by one, how often is the array full, and how many elements are stored each time? What does the sum of the first `n - 1` integers equal?

**Changed decision.** Only the growth rule changes, and it converts a linear total into a quadratic one.

#### [Boundary] One Expensive Append (Author exercise)
<!-- id: pc-one-expensive-append -->

**Prerequisites.** The two exercises above.

**Problem.** In a doubling array that reaches 1,025 stored values, identify the single append that triggers an O(n) copy. Reconcile that spike with the claim that appends are amortized O(1) over the whole sequence.

**Constraints.** Capacity starts at 1 and doubles on demand. Count 1,025 appends in total, so the final append is the one to examine.

**Example 1.** Input 1,025 appends, output that append number 1,025 copies 1,024 elements while the 1,024 appends before it copied 1,023 elements in total.

**Example 2.** Input 1,024 appends, output no spike at the end, since capacity 1,024 is exactly full and no further append has arrived.

**Hint.** When is the array full after exactly a power of two values? How many copies came from all the earlier resizes combined?

**Changed decision.** The question moves from the total to a single spike, and the exercise asks you to explain why one costly call does not break the average.

#### [Recognize] Potential Intuition (Author exercise)
<!-- id: pc-potential-intuition -->

**Prerequisites.** All three exercises above.

**Problem.** Treat the unused slots after a doubling as prepaid capacity. Explain, without formal algebra, how that stored potential funds the future cheap appends and the next resize, and show with numbers why a charge of three units per append is enough.

**Constraints.** Charge three units per append: one to write and two saved. A resize from capacity `c` to `2c` costs `c` units.

**Example 1.** Input a resize from capacity 4 to 8 after four stored values, output that the two appends since the previous resize saved 4 units and the copy costs 4.

**Example 2.** Input the very first resize from capacity 1 to 2 after one stored value, output that the one earlier append saved 2 units and the copy costs 1, so a unit is even left over.

**Hint.** After a resize to capacity `2c`, how many appends can happen before the next resize? How many units does each of those appends save?

**Changed decision.** The argument shifts from counting copies to explaining why the counted total is bounded, using stored credit.
