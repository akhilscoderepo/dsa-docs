<!-- lesson-kind: standard -->
<!-- lesson-id: local-choice -->
## Local Choice

<!-- stage: context -->
### The Night Clerk At Harbor Hostel

The night clerk at Harbor Hostel has a row of rooms with different numbers of beds and a queue of travellers who arrive in parties. A party of two needs a room with at least two beds. A party of five needs one with at least five. Each room takes one party and each party takes one room, and the hostel wants as many parties as possible to sleep indoors tonight.

The clerk cannot see the whole queue in advance and there is no time to rearrange anyone at midnight. Each time she hands over a key, the key is gone. She has noticed that some of her choices feel wasteful, like giving the nine-bed dormitory to a couple, and that the wasteful ones tend to cost her a bed for a party later in the evening.

<!-- stage: naive -->
### Try Every Way Of Handing Out Keys

The plain method considers each party in turn and tries every unused room that is big enough, plus the option of turning the party away, and keeps the best total over all of those branches.

```java
static int bestHoused(int[] need, int[] beds, int g, boolean[] taken) {
    if (g == need.length) return 0;
    int best = bestHoused(need, beds, g + 1, taken);      // turn this party away
    for (int r = 0; r < beds.length; r++) {
        if (!taken[r] && beds[r] >= need[g]) {
            taken[r] = true;
            best = Math.max(best, 1 + bestHoused(need, beds, g + 1, taken));
            taken[r] = false;
        }
    }
    return best;
}
```

The method is correct for any input, because it looks at every legal way of pairing parties with rooms. For three parties and three rooms that is a few dozen branches, and nobody minds.

<!-- stage: bottleneck -->
### Most Branches Waste A Big Room

With n parties and m rooms, each party has up to m + 1 options, so the search makes on the order of O((m + 1)^n) calls. At twenty parties and twenty rooms that is far beyond what a computer can finish.

The waste is not random. Most branches hand a large room to a small party while a smaller room that would have done the job sits unused. Whatever follows that handout could have been done at least as well with the smaller room, because the large room is still available for a bigger party. The recursion cannot know that, so it explores each such branch in full and then discovers the same final score that the tidy branch already reached.

<!-- stage: insight -->
### Take The Cheapest Room That Works

Consider the smallest party that is still waiting. Among the rooms that fit it, the smallest room dominates every other choice. A choice has **dominance** when anything an optimal plan could do after another choice can also be done after this one, with a result that is no worse. Giving the smallest party the smallest room that fits leaves every larger room free, and a larger room fits every party that a smaller one fits.

That is a **commitment**: a decision taken once, never reopened, and never compared with its alternatives again. A commitment is only legitimate when it keeps an **optimal completion** alive, meaning that after the choice there is still a way to finish the unresolved part that matches the best total any plan could reach. The check is a short argument. Take any best plan. If it houses the smallest party in a different room, swap the two rooms. The party still fits, because the cheaper room fits it by choice, and whoever used the cheap room fits the larger room. The total does not drop.

<!-- names: dominance, commitment, optimal completion -->

Once the argument is accepted, the search collapses to a single pass. Order the parties from small to large and the rooms from small to large. For the smallest unhoused party, walk forward through the rooms. A room that is too small for it is too small for every party after it, so it can be dropped for good. The first room that fits is the cheapest one that works, so give it away and move on. Nothing is ever undone and nothing is compared twice.

<!-- stage: variables -->
### Two Cursors And A Count

The array `need` holds party sizes in ascending order and `beds` holds room capacities in ascending order. The cursor `g` is the first party that is still without a room, and every party before it has been housed. The cursor `r` is the next room to consider, and every room before it has either been given away or discarded. The count `housed` equals `g`, so it is the same quantity seen twice. Each loop step moves `r` forward by one, and moves `g` forward only when the room fits. Neither cursor ever goes back.

<!-- stage: trace -->
### Rooms Walked Against Waiting Parties

Take parties of sizes 1, 3 and 4, and rooms of capacities 1, 1, 2, 3 and 5. The first trace moves through the rooms, and the note on each step says which party the room was offered to. Room one has one bed, the smallest party needs one, so the key goes out. Room two has one bed, and the waiting party needs three, so the room is discarded without anyone being housed. Room three has two beds and is discarded for the same reason. Room four has three beds and fits the party of three, so it is given away. Room five has five beds and fits the last party, which needs four, so the scan ends with all three parties housed.

The second trace is a different greedy choice, the lemonade queue. Each customer pays five, ten or twenty for a five-dollar drink, and the stand starts with no money. The state is two counters, fives and tens. For a ten the only change is a five. For a twenty there are two ways to make fifteen, a ten with a five, or three fives, and the trace takes the ten first because a five is useful for every later customer while a ten helps only with twenties. Follow the counters to see that the final twenty uses up the last ten and the last five together, and that the run succeeds.

```trace
{"cells":["1","1","2","3","5"],"pointers":["r"],"steps":[{"at":{"r":0},"vars":{"housed":1,"discarded":0,"waiting":3},"note":"The room with 1 bed fits the waiting party of 1, so the key goes out and the party cursor advances."},{"at":{"r":1},"vars":{"housed":1,"discarded":1,"waiting":3},"note":"The room with 1 bed is too small for the waiting party of 3, so it is discarded and nobody is housed."},{"at":{"r":2},"vars":{"housed":1,"discarded":2,"waiting":3},"note":"The room with 2 beds is too small for the waiting party of 3, so it is discarded and nobody is housed."},{"at":{"r":3},"vars":{"housed":2,"discarded":2,"waiting":4},"note":"The room with 3 beds fits the waiting party of 3, so the key goes out and the party cursor advances."},{"at":{"r":4},"vars":{"housed":3,"discarded":2,"waiting":"none"},"note":"The room with 5 beds fits the waiting party of 4, so the key goes out and the party cursor advances."}]}
```

```trace
{"cells":["5","5","10","5","20","10","5","20"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"fives":1,"tens":0},"note":"A five is paid for a five-dollar drink, so no change is owed and the fives counter grows."},{"at":{"i":1},"vars":{"fives":2,"tens":0},"note":"A five is paid for a five-dollar drink, so no change is owed and the fives counter grows."},{"at":{"i":2},"vars":{"fives":1,"tens":1},"note":"A ten is paid, so one five goes back as change and the tens counter grows."},{"at":{"i":3},"vars":{"fives":2,"tens":1},"note":"A five is paid for a five-dollar drink, so no change is owed and the fives counter grows."},{"at":{"i":4},"vars":{"fives":1,"tens":0},"note":"A twenty is paid. Fifteen is given as a ten plus a five, which keeps the remaining fives for later customers."},{"at":{"i":5},"vars":{"fives":0,"tens":1},"note":"A ten is paid, so one five goes back as change and the tens counter grows."},{"at":{"i":6},"vars":{"fives":1,"tens":1},"note":"A five is paid for a five-dollar drink, so no change is owed and the fives counter grows."},{"at":{"i":7},"vars":{"fives":0,"tens":0},"note":"A twenty is paid. Fifteen is given as a ten plus a five, which keeps the remaining fives for later customers."}]}
```

<!-- stage: code -->
### Two Cursors And Two Counters

```java
static int housed(int[] demand, int[] supply) {
    int[] need = demand.clone(), beds = supply.clone();   // sort copies, never the caller's arrays
    Arrays.sort(need);
    Arrays.sort(beds);
    int g = 0;
    for (int r = 0; r < beds.length && g < need.length; r++) {
        if (beds[r] >= need[g]) g++;                      // cheapest room that works
    }
    return g;
}

static boolean lemonade(int[] bills) {
    int fives = 0, tens = 0;
    for (int bill : bills) {
        if (bill == 5) fives++;
        else if (bill == 10) { if (fives == 0) return false; fives--; tens++; }
        else if (tens > 0 && fives > 0) { tens--; fives--; }   // spend the scarce-use ten first
        else if (fives >= 3) fives -= 3;
        else return false;
    }
    return true;
}
```

Sorting costs O(n log n) and the walk adds one step per room, so the walk is linear in n + m. The lemonade loop does a constant amount of work per customer. The clones leave the caller's arrays in their original order, which matters whenever the caller keeps indexes into them.

<!-- stage: applicability -->
### When The Cheap Choice Is Safe

Use a local choice when one option can be shown to dominate the others for everything that remains. The cue is a sequence of irrevocable decisions with a clear measure of how much each choice uses up, such as beds, change or time. The invariant to carry is that after every commitment an optimal completion still exists. State that sentence before writing any code, and check it with the swap argument on a small case.

The false friend is greed without a proof. Choosing the largest reward or the biggest item first sounds the same, but it only works when a swap argument backs it. Coin change with denominations 1, 3 and 4 shows the failure: to make six, the largest coin first takes four and then needs two ones, three coins, while two threes are enough. Weighted jobs behave the same way. Also expect trouble when a choice changes what later choices cost, since the swap may then not preserve feasibility.

In Java, sort clones when the contract does not allow reordering the input, and compare sizes with `>=` when equality is feasible. Use `long` if capacities are added together.

<!-- stage: exercises -->
### Exercises

#### [Build] Smallest Sufficient Match (Author exercise)
<!-- id: gr-smallest-sufficient-match -->

**Prerequisites.** Sorting a copy of an array from Chapter 05; the nested loop over two arrays.

**Problem.** Each party in `need` must receive at most one room from `beds`, and each room serves at most one party. Process the parties from the smallest need to the largest, breaking ties by the lower input index. Each party takes the smallest unused room whose capacity is at least its need, again breaking ties by the lower index. Return an array with one entry per party, holding the index of its room or -1 if no room remains that fits.

**Constraints.** 0 <= need.length, beds.length <= 12, and every size is between 1 and 1000. The input arrays must not be modified.

**Example 1.** Input `need = [2, 5, 1]`, `beds = [4, 1, 6]`, output `[0, 2, 1]`.

**Example 2.** Input `need = [3, 3]`, `beds = [2, 9]`, output `[1, -1]`, because the room with two beds cannot take either party.

**Hint.** If the party of five were served first, what would happen to the small parties? Which rooms can be skipped for every later party once the smallest is served?

**Changed decision.** First rung: serve the smallest unmet demand with the smallest sufficient resource, and never reopen the choice.

#### [Vary] Assign Cookies (LeetCode 455)
<!-- id: gr-assign-cookies -->

**Prerequisites.** The smallest sufficient match above.

**Problem.** Child `i` is content with a cookie of size at least `greed[i]`. Each child gets at most one cookie and each cookie goes to at most one child. Return the largest number of content children.

**Constraints.** 0 <= greed.length, sizes.length <= 30000 and all values are between 1 and 2^31 - 1. The caller's arrays are left in their original order.

**Example 1.** Input `greed = [2, 5, 1, 9]`, `sizes = [3, 1, 6]`, output 3.

**Example 2.** Input `greed = [3, 3, 3]`, `sizes = [3, 9]`, output 2, since a cookie exactly as large as the greed is enough.

**Hint.** After sorting both sides, when can a cookie be discarded for good? What should the other cursor do when a cookie is accepted?

**Changed decision.** Both sides are sorted, so the room search becomes a single forward pass with two cursors.

#### [Boundary] Unusable Resources (Author exercise)
<!-- id: gr-unusable-resources -->

**Prerequisites.** The two exercises above.

**Problem.** Run the sorted two-cursor pass on `need` and `beds`, and return two numbers: how many parties are housed, and how many rooms the pass discards. A room is discarded when it is examined while a party is still waiting and it is too small for that party. Rooms never examined, because every party was already housed, are not counted.

**Constraints.** 0 <= need.length, beds.length <= 12 and sizes are between 1 and 2147483647. Equal sizes fit.

**Example 1.** Input `need = [4, 4]`, `beds = [1, 2, 3]`, output `[0, 3]`, since every room is discarded and nobody is housed.

**Example 2.** Input `need = [2, 6]`, `beds = [2147483647, 2, 1]`, output `[2, 1]`.

**Hint.** Which cursor moves when a room does not fit? What stops the pass when all parties are housed before the rooms run out?

**Changed decision.** The unusable room is skipped without consuming a party, and the loop must stop as soon as the parties are gone.

#### [Recognize] Lemonade Change (LeetCode 860)
<!-- id: gr-lemonade-change -->

**Prerequisites.** All three exercises above.

**Problem.** Customers queue in order, each paying 5, 10 or 20 for a drink that costs 5. The stand starts with no money and must give exact change to each customer. Return whether every customer can be served.

**Constraints.** 0 <= bills.length <= 100000 and each bill is 5, 10 or 20.

**Example 1.** Input `bills = [5, 5, 10, 5, 20, 10, 5, 20]`, output true.

**Example 2.** Input `bills = [5, 10, 10, 20]`, output false, since the second ten has no five left to match it.

**Hint.** A twenty can be changed in two ways. Which bills are useful for every later customer, and which are useful only for one kind?

**Changed decision.** The scarce resource is a five-dollar bill, so the choice among two ways to make change is settled by which one keeps more fives.
