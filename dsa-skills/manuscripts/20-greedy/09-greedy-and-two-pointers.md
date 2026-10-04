<!-- lesson-kind: combination -->
<!-- lesson-id: greedy-and-two-pointers -->
## Greedy And Two Pointers

<!-- stage: context -->
### The Dockmaster Of Marrow Bay

The dockmaster of Marrow Bay has three small jobs before the morning ferry leaves. She has a basket of souvenir tokens to hand to children, and each child will accept a token that is at least as valuable as the child's wish but not wildly more valuable, or the others will complain. She has a line of passengers waiting for the ferry, and each boat carries at most two people whose weights together stay under the limit painted on the hull. And she has a game with a row of brass discs, which she plays while waiting, where she can spend energy on a disc to earn a point or give up a point to win energy back.

Every job has a list that she can arrange in order of size before she starts. She notices that in each one the smallest and the biggest items matter far more than the ones in the middle.

<!-- stage: contributions -->
### What Sorted Piles And Pointers Each Bring

Sorting brings a monotone arrangement. Once the items are in order, every pair of positions has a clear relation, so a statement such as nobody to the right of here can use this item follows from one comparison. Two pointers bring the motion that exploits that arrangement. A pointer at each end, or one pointer in each of two sorted lists, can be moved inward in a single pass because each move discards an item for good.

The greedy argument brings the guarantee that the discarded item loses nothing. Without it, a pointer that moves is only a guess that happened to work on the examples. The cue for the combination is a pairing or selection question over sorted items, where the extreme items decide whether a partner exists and the exchange argument says which extreme to settle first.

<!-- stage: naive -->
### Search Every Pairing

The direct method for the ferry takes the first waiting passenger and tries every way to seat them, alone or with any other passenger who fits under the limit, and recurses on the rest.

```java
static int fewestBoats(long[] w, boolean[] used, long limit) {
    int i = 0;
    while (i < w.length && used[i]) i++;
    if (i == w.length) return 0;
    used[i] = true;
    int best = 1 + fewestBoats(w, used, limit);                       // passenger i rides alone
    for (int j = i + 1; j < w.length; j++) {
        if (!used[j] && w[i] + w[j] <= limit) {
            used[j] = true;
            best = Math.min(best, 1 + fewestBoats(w, used, limit));
            used[j] = false;
        }
    }
    used[i] = false;
    return best;
}
```

The method is exact for any passengers, since it looks at every legal seating. For ten passengers it answers at once.

<!-- stage: bottleneck -->
### Pairings Grow Factorially

The number of ways to seat n passengers in boats of two or fewer is on the order of O(n!), so the search breaks down near twenty. Almost all of the branches are pointless. They give the heaviest passenger a partner who is heavier than needed, or leave a light passenger to ride alone when someone heavy could share the boat with them.

Sorting exposes the structure. If the lightest passenger cannot fit with the heaviest, then nobody can, so the heaviest rides alone. If the lightest does fit with the heaviest, the pair is the most efficient use of the heaviest, because any other partner is at least as heavy. Each of these facts settles one passenger or two from the ends, and the recursion's branching, which only ever picked among the middle, disappears.

<!-- stage: insight -->
### Settle One End At A Time

Sorted order gives a **monotone candidate order**: moving right never makes an item lighter, so feasibility against a fixed partner changes at most once as the other pointer moves. That is what lets one pointer drop an item for good. For the ferry, look at the heaviest passenger H and the lightest L. If L + H exceeds the limit, no one fits with H, since every partner is at least as heavy as L, so H rides alone and the right pointer moves in.

If L + H fits, take the **endpoint commitment**: seat H with L. The exchange argument is short. In any best seating, H shares a boat with some p or rides alone. Swap p and L. The boat of H then carries L, which fits because L is lightest. The boat that held L now holds p, together with L's old partner q if there was one. That pair fits because q is no heavier than H, and H together with p already fits under the limit. The number of boats does not grow.

<!-- names: monotone candidate order, endpoint commitment, elimination step -->

Each move of a pointer is an **elimination step**: one item leaves the problem permanently, and the rest is the same problem on a shorter range. The token game works the same way. Spend the cheapest remaining token for a point, which never hurts, and when none is affordable and a point is in hand, sell the most expensive remaining token for energy, since it returns the most. For the souvenirs, a token that is too small for the current child is too small for every later child, and a token that is too big for the current child is too big for it whatever comes next, so each comparison removes one item.

<!-- stage: variables -->
### Two Cursors And What They Carry

In the ferry loop, `lo` is the lightest passenger not yet seated, `hi` is the heaviest, and `boats` counts departures. When `lo == hi` one passenger is left and rides alone, and that must be counted exactly once. In the token game, `lo` is the cheapest unspent token, `hi` is the dearest unsold one, `power` is the current energy, `score` is the points in hand and `best` is the largest score reached. For the souvenirs, `i` is the next child and `j` the next token, with `matched` the pairs made. Sums such as `p[lo] + p[hi]` and a running `power` are held in `long`, since two valid ints can add to more than an int holds.

<!-- stage: trace -->
### Boats Filled And Tokens Played

The first trace seats the passengers of weights 2, 3, 4, 5 and 7 under a limit of nine. The lightest, two, and the heaviest, seven, add to exactly nine, which is allowed, so they share the first boat. Now three and five add to eight, so they share the second boat. Only the passenger of weight four is left with both pointers on the same place, and that one rides in a third boat.

The second trace plays tokens worth 10, 20, 30, 60 and 90 with forty-five energy. The ten is affordable and gives a point, and so does the twenty, leaving fifteen energy and two points. The thirty is too dear, so the ninety is sold, which costs a point and brings the energy to one hundred and five. Now thirty and sixty can both be bought. The score reaches three, the most at any time, and the pointers cross.

```trace
{"cells":["2","3","4","5","7"],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":4},"vars":{"boats":1},"note":"The lightest 2 and the heaviest 7 weigh 9 together, within the limit 9, so they share boat number 1."},{"at":{"lo":1,"hi":3},"vars":{"boats":2},"note":"The lightest 3 and the heaviest 5 weigh 8 together, within the limit 9, so they share boat number 2."},{"at":{"lo":2,"hi":2},"vars":{"boats":3},"note":"Both pointers stand on the weight 4, the last person, who rides alone in boat number 3."}]}
```

```trace
{"cells":["10","20","30","60","90"],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":4},"vars":{"power":35,"score":1},"note":"The cheapest token 10 is affordable with energy 45, so it is played face up for a point."},{"at":{"lo":1,"hi":4},"vars":{"power":15,"score":2},"note":"The cheapest token 20 is affordable with energy 35, so it is played face up for a point."},{"at":{"lo":2,"hi":4},"vars":{"power":105,"score":1},"note":"The cheapest token 30 costs more than the energy 15, so the dearest token 90 is sold face down for energy."},{"at":{"lo":2,"hi":3},"vars":{"power":75,"score":2},"note":"The cheapest token 30 is affordable with energy 105, so it is played face up for a point."},{"at":{"lo":3,"hi":3},"vars":{"power":15,"score":3},"note":"The cheapest token 60 is affordable with energy 75, so it is played face up for a point."}]}
```

<!-- stage: code -->
### Three Pointer Loops

```java
static int satisfiedWithTolerance(int[] greed, int[] sizes, int tol) {
    int[] g = greed.clone(), s = sizes.clone();
    Arrays.sort(g);
    Arrays.sort(s);
    int i = 0, j = 0, matched = 0;
    while (i < g.length && j < s.length) {
        if (s[j] < g[i]) j++;                                      // too small for this child and every later one
        else if ((long) s[j] > (long) g[i] + tol) i++;            // too big for this child, so skip the child
        else { matched++; i++; j++; }
    }
    return matched;
}

static int boats(int[] people, int limit) {
    int[] p = people.clone();
    Arrays.sort(p);
    int lo = 0, hi = p.length - 1, boats = 0;
    while (lo <= hi) {
        if (lo < hi && (long) p[lo] + p[hi] <= limit) lo++;        // the lightest shares the boat
        hi--;                                                       // the heaviest always departs
        boats++;
    }
    return boats;
}

static int bestScore(int[] tokens, long power) {
    int[] t = tokens.clone();
    Arrays.sort(t);
    int lo = 0, hi = t.length - 1, score = 0, best = 0;
    while (lo <= hi) {
        if (power >= t[lo]) { power -= t[lo++]; score++; best = Math.max(best, score); }
        else if (score > 0) { power += t[hi--]; score--; }
        else break;
    }
    return best;
}
```

Every loop moves at least one pointer on each pass, so each is linear after its sort, and the sort sets the cost at O(n log n). The boats loop counts the lone final passenger once, because the `lo < hi` test fails when the pointers meet. The widened sums prevent a wrapped total from passing the limit test.

<!-- stage: applicability -->
### When The Ends Decide

Use this combination when items can be sorted, the question is a pairing or a selection, and the smallest and largest items decide feasibility. The invariant is that all items outside the two pointers are already settled and everything inside is the same problem on a shorter range. State the elimination reason in a sentence for each pointer move, as a check that the move is more than a guess.

The false friend is pointer motion without the argument. A pair-sum problem on a sorted array can be solved by a pointer on each end because the sum is monotone in each pointer, but a pairing that maximises the number of boats is a different claim, and it needs the exchange argument. The pattern stops applying when more than two items share a boat, since the lightest-with-heaviest swap no longer covers the extra item, and a plain sorted pair-sum search from Chapter 08 does not choose a best pairing at all.

In Java, clone arrays before sorting if the caller owns the order, widen sums before comparing with the limit, and make the equality case explicit. Count the last unpaired item once, and stop loops when the pointers cross rather than when they meet.

<!-- stage: exercises -->
### Exercises

#### [Build] Assign Cookies (LeetCode 455)
<!-- id: gc-cookies-with-tolerance -->

**Prerequisites.** The two-pointer chapter (Chapter 08); the local-choice lesson of this chapter.

**Problem.** Child `i` accepts a cookie of any size from `greed[i]` up to `greed[i] + tol`, both ends included, and no cookie may be shared between two children. Return the largest number of children who can be given an acceptable cookie.

**Constraints.** 0 <= greed.length, sizes.length <= 100000 and 1 <= greed[i], sizes[j] <= 2147483647 and 0 <= tol <= 2147483647. The sum `greed[i] + tol` can exceed the `int` range.

**Example 1.** Input `greed = [1, 4, 9]`, `sizes = [2, 3, 10, 7]`, `tol = 2`, output 2.

**Example 2.** Input `greed = [3, 3, 5]`, `sizes = [3, 5, 5, 6]`, `tol = 0`, output 2.

**Hint.** What should happen to a cookie that is too small for the smallest remaining child? What should happen to a child for whom the smallest remaining cookie is too big?

**Changed decision.** A cookie can now be too big as well as too small, so each comparison discards either a cookie or a child.

#### [Vary] Boats to Save People (LeetCode 881)
<!-- id: gc-boats-limit -->

**Prerequisites.** The cookie exercise above.

**Problem.** Each boat carries at most two people, and the total weight in a boat may not exceed `limit`. Every person weighs at most `limit`. Return the fewest boats needed to carry everyone.

**Constraints.** 0 <= people.length <= 100000 and 1 <= people[i] <= limit <= 2147483647.

**Example 1.** Input `people = [7, 2, 5, 3, 4]`, `limit = 9`, output 3.

**Example 2.** Input `people = [2147483647, 2147483647]`, `limit = 2147483647`, output 2.

**Hint.** When the lightest passenger cannot fit with the heaviest, what does that say about the heaviest? When the two fit, why is pairing them safe?

**Changed decision.** The pair is chosen from the two ends, so feasibility is tested only between the lightest and heaviest remaining.

#### [Boundary] Exact Capacity And One Remaining Person (Author exercise)
<!-- id: gc-exact-capacity-last-person -->

**Prerequisites.** The two exercises above.

**Problem.** Run the boat rule on `people` with the given `limit`, where a pair whose total equals `limit` is allowed. Return two numbers: the total number of boats, and how many of those boats carry exactly two people.

**Constraints.** 0 <= people.length <= 100000 and 1 <= people[i] <= limit <= 2147483647.

**Example 1.** Input `people = [3, 3, 3]`, `limit = 6`, output `[2, 1]`, since the middle person is left alone once the pointers meet.

**Example 2.** Input `people = [5]`, `limit = 5`, output `[1, 0]`.

**Hint.** Which condition makes a pair legal when the pointers are on the same person? Where does the last unpaired person get counted?

**Changed decision.** Equality is feasible, and the final singleton is counted exactly once.

#### [Recognize] Bag of Tokens (LeetCode 948)
<!-- id: gc-bag-of-tokens -->

**Prerequisites.** All three exercises above.

**Problem.** You start with `power` energy and no score. Each token can be used once. Playing a token face up costs `tokens[i]` energy and gives one point, and needs at least that much energy. Playing it face down gives `tokens[i]` energy and costs one point, and needs at least one point. Return the largest score you can hold at any moment.

**Constraints.** 0 <= tokens.length <= 100000, 1 <= tokens[i] <= 2147483647 and 0 <= power <= 4000000000. Energy can pass the `int` range while the game runs.

**Example 1.** Input `tokens = [60, 20, 90, 30, 10]`, `power = 45`, output 3.

**Example 2.** Input `tokens = [2147483647, 1, 2147483647]`, `power = 2147483647`, output 1.

**Hint.** Which token should be spent for a point, and which should be sold for energy? When is it not worth selling a token at all?

**Changed decision.** The pointers now carry a resource and a score: the low end is spent for points and the high end is sold for energy only when stuck.
