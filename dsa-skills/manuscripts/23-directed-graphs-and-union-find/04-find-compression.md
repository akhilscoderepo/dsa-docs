<!-- lesson-kind: standard -->
<!-- lesson-id: find-compression -->
## Find Compression

<!-- stage: context -->
### Cards In The Saltmarsh Tin

The Saltmarsh Ramblers keep one membership card per walker in a biscuit tin, and the secretary, Odile, files them by number. Each card has a single line at the bottom, "I walk with:", followed by the number of another member. A group leader writes her own number there. Whenever two walking groups decide to combine, the leader of the smaller group crosses out her own number and writes the other leader's number instead, and nobody else's card is touched.

Odile gets a steady stream of questions on the phone. Is Wren in the same group as Tavish? Who leads Marit's group this month? To answer she picks up the card, reads the number, picks up that card, and carries on until she reaches a card showing its own number. After a busy autumn of mergers, some members sit at the end of a line of sixty cards, and she has begun to dread the phone. She wants a way to answer any such question for any tin, and she is willing to scribble on the cards while she does it.

<!-- stage: naive -->
### Read Cards Until A Leader Shows

The direct method answers every question from scratch. To find a member's leader, read the number on the card and move to that card, repeating until a card names itself. Two members are in the same group exactly when the two walks end at the same leader. A merge is a single write on one leader's card.

```java
static int leaderOf(int[] walksWith, int member) {
    while (walksWith[member] != member) {
        member = walksWith[member];
    }
    return member;
}

static boolean sameGroup(int[] walksWith, int a, int b) {
    return leaderOf(walksWith, a) == leaderOf(walksWith, b);
}

static void combine(int[] walksWith, int a, int b) {
    walksWith[leaderOf(walksWith, a)] = leaderOf(walksWith, b);
}
```

This is correct as long as the cards never form a loop, which the combine step guarantees because it only ever links one leader to a different leader. A card whose line shows its own number ends the walk at once, so a member who has never been merged costs nothing.

<!-- stage: bottleneck -->
### Long Lines Get Walked Again

A walk costs as many reads as there are cards on the line, and a line can grow to n cards for n members. Merge the groups one after another, each time pointing the old leader at a brand new one, and the first member ends up n cards from the top. Then q questions about that member cost O(q * n) reads in total. With a hundred thousand members and a hundred thousand questions, that is around ten billion card reads, which no phone call can wait for.

The painful part is that every question about the same member walks the very same line again. The first walk has already discovered who the leader is, yet it throws that knowledge away and the next caller starts at the bottom once more. Every card passed along the way would give the right answer if it simply named the leader. A better method should use each walk to shorten the line it just climbed, so that the price of a long line is paid once and not on every call.

<!-- stage: insight -->
### Leave Shortcuts Behind

Store the tin as an `int[]` where slot `i` holds the number on card `i`. This is the **parent array**: it records one link per member, and a member whose slot holds its own index is a root. Following links from any member must end at a root, and that root is the **representative** of the whole group. Two members belong together exactly when their representatives are the same, so the only question that ever needs answering is "which root is at the end of my line?". Call that operation `find`.

A line can be long, but it only matters how long it is the first time. Once a `find` has reached the root, it knows the representative for every card it passed, and it can rewrite each of those cards to name the root directly. This is **path compression**. Nothing about who belongs with whom has changed, since each rewritten card still leads to the same root in one step instead of many, and the next `find` from any of those members takes one read.

Compression only touches cards on the path that was just climbed. Cards hanging off to the side keep their old links, and they will be shortened when somebody asks about them.

The invariant is that every chain of links ends at exactly one root, before and after every rewrite.

<!-- names: parent array, representative, path compression -->

<!-- stage: variables -->
### Cards, Roots And Rewrites

The array `parent` holds one slot per member, and `parent[x] == x` marks a root. The variable `x` is the member currently being followed, `root` is the card the first climb ended on, and `next` remembers where to go after a slot has been overwritten. The counter `hops` is the number of links followed on the way up, and `rewrites` is the number of slots that were changed to point at the root. The array is changed in place by `find`, and that is deliberate and visible to callers: the stored groups stay the same, and only the shape of the lines changes.

<!-- stage: trace -->
### Two Finds On Two Shapes

The first trace is a line of eight members where each one follows the member just below, so member 7 is seven links from the root 0. The cells are the member numbers and the pointer `x` is the card being read. The first eight steps climb, with `hops` counting links followed. The next six rewrite the cards on the way back down the same line, and `rewrites` counts the slots that changed. Member 1 already follows the root, so it needs no write, and that is why the rewriting starts at 7 and stops at 2.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["x"],"steps":[{"at":{"x":7},"vars":{"hops":0,"rewrites":0},"note":"Query 7: card 7 is read; it names 6, one more hop."},{"at":{"x":6},"vars":{"hops":1,"rewrites":0},"note":"Query 7: card 6 is read; it names 5, one more hop."},{"at":{"x":5},"vars":{"hops":2,"rewrites":0},"note":"Query 7: card 5 is read; it names 4, one more hop."},{"at":{"x":4},"vars":{"hops":3,"rewrites":0},"note":"Query 7: card 4 is read; it names 3, one more hop."},{"at":{"x":3},"vars":{"hops":4,"rewrites":0},"note":"Query 7: card 3 is read; it names 2, one more hop."},{"at":{"x":2},"vars":{"hops":5,"rewrites":0},"note":"Query 7: card 2 is read; it names 1, one more hop."},{"at":{"x":1},"vars":{"hops":6,"rewrites":0},"note":"Query 7: card 1 is read; it names 0, one more hop."},{"at":{"x":0},"vars":{"hops":7,"rewrites":0},"note":"Query 7: card 0 is read; it names itself, so it is the root."},{"at":{"x":7},"vars":{"hops":7,"rewrites":1},"note":"Query 7: card 7 now names the root 0 instead of 6."},{"at":{"x":6},"vars":{"hops":7,"rewrites":2},"note":"Query 7: card 6 now names the root 0 instead of 5."},{"at":{"x":5},"vars":{"hops":7,"rewrites":3},"note":"Query 7: card 5 now names the root 0 instead of 4."},{"at":{"x":4},"vars":{"hops":7,"rewrites":4},"note":"Query 7: card 4 now names the root 0 instead of 3."},{"at":{"x":3},"vars":{"hops":7,"rewrites":5},"note":"Query 7: card 3 now names the root 0 instead of 2."},{"at":{"x":2},"vars":{"hops":7,"rewrites":6},"note":"Query 7: card 2 now names the root 0 instead of 1."}]}
```

The second trace uses a bushier tree of nine members and asks three questions in a row: member 8, then member 6, then member 8 again. Cards off the climbed path, such as 3 and 5, keep their links, while every card that was on a path ends up one hop from the root. The third question shows the payoff: its single hop costs one read where the first question needed three.

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["x"],"steps":[{"at":{"x":8},"vars":{"hops":0,"rewrites":0},"note":"Query 8: card 8 is read; it names 7, one more hop."},{"at":{"x":7},"vars":{"hops":1,"rewrites":0},"note":"Query 8: card 7 is read; it names 2, one more hop."},{"at":{"x":2},"vars":{"hops":2,"rewrites":0},"note":"Query 8: card 2 is read; it names 0, one more hop."},{"at":{"x":0},"vars":{"hops":3,"rewrites":0},"note":"Query 8: card 0 is read; it names itself, so it is the root."},{"at":{"x":8},"vars":{"hops":3,"rewrites":1},"note":"Query 8: card 8 now names the root 0 instead of 7."},{"at":{"x":7},"vars":{"hops":3,"rewrites":2},"note":"Query 8: card 7 now names the root 0 instead of 2."},{"at":{"x":6},"vars":{"hops":0,"rewrites":0},"note":"Query 6: card 6 is read; it names 4, one more hop."},{"at":{"x":4},"vars":{"hops":1,"rewrites":0},"note":"Query 6: card 4 is read; it names 1, one more hop."},{"at":{"x":1},"vars":{"hops":2,"rewrites":0},"note":"Query 6: card 1 is read; it names 0, one more hop."},{"at":{"x":0},"vars":{"hops":3,"rewrites":0},"note":"Query 6: card 0 is read; it names itself, so it is the root."},{"at":{"x":6},"vars":{"hops":3,"rewrites":1},"note":"Query 6: card 6 now names the root 0 instead of 4."},{"at":{"x":4},"vars":{"hops":3,"rewrites":2},"note":"Query 6: card 4 now names the root 0 instead of 1."},{"at":{"x":8},"vars":{"hops":0,"rewrites":0},"note":"Query 8: card 8 is read; it names 0, one more hop."},{"at":{"x":0},"vars":{"hops":1,"rewrites":0},"note":"Query 8: card 0 is read; it names itself, so it is the root. Member 8 already follows the root, so nothing is rewritten."}]}
```

<!-- stage: code -->
### Find With A Second Pass

```java
static int find(int[] parent, int x) {
    int root = x;
    while (parent[root] != root) {
        root = parent[root];
    }
    while (parent[x] != root) {
        int next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

static void link(int[] parent, int a, int b) {
    int ra = find(parent, a), rb = find(parent, b);
    if (ra != rb) parent[ra] = rb;
}
```

The first loop climbs to the root and the second loop walks the same line again, saving the next card before overwriting the current slot. It stops when a card already names the root, so the root itself and its direct followers are never written. The version is iterative on purpose: no call stack grows with the length of the line. A single `find` costs time proportional to the line it climbs, and across many operations the total stays far below the naive O(q * n), with the sharper bounds arriving once merges also keep lines short. Space is the one `int[]`.

<!-- stage: applicability -->
### When Groups Merge And Get Asked

Reach for this when a problem keeps merging groups and keeps asking which group something belongs to: friends who become connected, cities joined by roads one at a time, accounts sharing an email. The recognition cue is that each question names an element and expects a group identity, or asks whether two elements share one, while merges keep arriving between the questions. The invariant is that following links from any element always ends at exactly one root, and rewriting a card to point at that root never changes who belongs together.

The false friend is treating the structure as a graph you can look inside. The links are shortcuts toward a root and not the original edges, so after compression the line from a member to the root no longer shows how the member was connected, and no route can be read back from it. Cutting a link is no better: deleting one edge from a merged group cannot be undone by erasing a card, because the other cards may already point past it.

Do not use it when you need the actual path between two elements, the shortest route, or a connection that can be removed again, because a plain traversal or an offline method is needed there. In Java, a recursive `find` that writes `parent[x] = find(parent[x])` is neat but uses one stack frame per link, so a line of a million cards raises `StackOverflowError` on a thread with an ordinary stack. The iterative version above is safe, and an `int[]` is a reference, so `int[] saved = parent` does not take a snapshot: use `clone()` when the original must stay as it was.

<!-- stage: exercises -->
### Exercises

#### [Build] Follow Parents To Root (Author exercise)
<!-- id: ug-follow-root -->

**Prerequisites.** The naive walk from this lesson and the idea that a slot holding its own index is a root.

**Problem.** The `parent` array describes a forest: `parent[i]` is the member that `i` follows, and `parent[i] == i` marks a root. Given `parent` and a start member `x`, return an `int[]` of two values: the root at the end of the line from `x`, and the number of links followed to get there. Do not rewrite any slot, and do not modify the array.

**Constraints.** 1 <= parent.length <= 100000, every entry is a valid index, and following links from any member always reaches a root, so the array has no loops other than a root pointing at itself.

**Example 1.** Input `parent = [0,0,1,2,2,5], x = 3`, output `[0, 3]`.

**Example 2.** Input `parent = [0,0,2,2,3,3], x = 5`, output `[2, 2]`.

**Hint.** What condition on `parent[x]` tells you that the loop should stop, and what do you count each time it does not?

**Changed decision.** The walk only reads the array and counts links, with no rewriting, so a repeated question costs the same each time.

#### [Vary] Compress A Chain (Author exercise)
<!-- id: ug-compress-chain -->

**Prerequisites.** The Follow Parents To Root rung and the second loop of the code stage.

**Problem.** Run one `find` from `x` with compression and return the resulting array. Every member on the line from `x` up to, but not including, the root ends up pointing straight at the root. Members not on that line keep their original slot. The argument array must stay as it was, so build and return a new `int[]`.

**Constraints.** 1 <= parent.length <= 100000, and the input is a valid forest as in the Build rung.

**Example 1.** Input `parent = [0,0,1,2,3], x = 4`, output `[0,0,0,0,0]`.

**Example 2.** Input `parent = [0,0,0,1,1,3,4], x = 6`, output `[0,0,0,1,0,3,0]`.

**Hint.** Which slot must be read before it is overwritten, and which members must be left exactly as they were?

**Changed decision.** The walk now writes: each visited slot is redirected to the root, instead of only being read.

#### [Boundary] Singleton Components (Author exercise)
<!-- id: ug-singletons -->

**Prerequisites.** The Compress A Chain rung.

**Problem.** There are `n` members numbered 0 to n-1, and at the start each one is alone and is its own root. The array `edges` lists pairs `{a, b}` that join the groups of `a` and `b`. A pair may name the same member twice, may repeat an earlier pair, or may appear in either order. Return the number of members who are still alone after every pair has been applied, meaning their group contains no other member. A pair `{v, v}` joins nothing.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 3000, and every endpoint is between 0 and n-1. The `edges` array is not modified.

**Example 1.** Input `n = 5, edges = [[0,1],[2,2]]`, output `3`.

**Example 2.** Input `n = 4, edges = [[1,2],[2,1],[3,3]]`, output `2`.

**Hint.** Before any pair is applied, what is the size of every group, and does a pair naming one member twice change anything?

**Changed decision.** Each member starts as a root pointing at itself, and the answer is counted by group size after all merges, not by the number of roots.

#### [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: ug-provinces -->

**Prerequisites.** The Singleton Components rung.

**Problem.** The matrix `isConnected` is n by n, with `isConnected[i][j] == 1` when cities `i` and `j` are directly linked and 0 otherwise. Linking is symmetric and `isConnected[i][i]` is always 1. A province is a maximal set of cities that can reach each other through direct links. Return an `int[]` of two values: the number of provinces, and the number of cities in the largest province. The matrix is not modified.

**Constraints.** 1 <= n <= 200, every entry is 0 or 1, the matrix is symmetric, and the diagonal is all 1.

**Example 1.** Input `isConnected = [[1,1,0],[1,1,0],[0,0,1]]`, output `[2, 2]`.

**Example 2.** Input `isConnected = [[1,0,0,1,0],[0,1,1,0,0],[0,1,1,1,0],[1,0,1,1,0],[0,0,0,0,1]]`, output `[2, 4]`.

**Hint.** After all links are applied, how do you tell which members belong together, and why must you ask `find` instead of reading a slot directly?

**Changed decision.** Cities are merged by `find` as links are read, and the answers come from the final roots instead of from a traversal of the matrix.
