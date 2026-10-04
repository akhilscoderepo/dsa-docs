<!-- lesson-kind: standard -->
<!-- lesson-id: union-by-size -->
## Union By Size

<!-- stage: context -->
### Banners At The Fennick Hill Fair

Teodor is the secretary of the student council at Fennick Hill School, and he keeps the lunchtime clubs' membership list. Each club owns one banner, and exactly one member holds it. Nobody keeps a roster. Every other student just remembers one person they answer to, and that person answers to someone else, until the chain reaches the student who holds the banner. To learn which club a student belongs to, you ask who they answer to and keep asking until you meet a banner holder.

Clubs merge all term long. The kite club joins the chess club, then the chess club joins the choir, and a few weeks later two tiny groups fold into each other. Each merge ends with one banner and one club. Teodor has 600 students and hundreds of merges, and every day the headteacher asks whether two students belong to the same club. He wants each question answered after only a few "who do you answer to" hops, however the merges happened to be ordered.

<!-- stage: naive -->
### Hang The First Banner Under The Second

The plainest rule for a merge is to find the banner holders of both students and make the first holder answer to the second. Nothing about the clubs is consulted, and the first club simply loses its banner.

```java
static int holder(int[] answersTo, int student) {
    while (answersTo[student] != student) student = answersTo[student];
    return student;
}

static void mergeClubs(int[] answersTo, int a, int b) {
    answersTo[holder(answersTo, a)] = holder(answersTo, b);
}
```

This is correct. Two students share a club exactly when `holder` returns the same student for both, a merge of a club with itself rewrites a holder to point at itself and changes nothing, and every merge leaves a single holder per club. The only open question is how long the chains get. If student 0 is merged with student 1, then with 2, then with 3, and so on, the first holder keeps moving under a brand-new single student, and the chain from student 0 grows by one link per merge.

<!-- stage: bottleneck -->
### One Long Chain Of Hops

The rule never looks at how big the clubs are, so an adversarial order of merges can stack the clubs into a single line. After n - 1 such merges the chain from student 0 has n links, and each later `holder` call costs O(n). The merges themselves walk the growing chain too, so n of them cost 1 + 2 + ... + n steps, which is O(n^2) in total. For 600 students that is only about 180,000 hops. For a school district with 200,000 students it is twenty billion, and each daily question is still O(n) on its own.

The cause is easy to point at. A small club was hung above a large one, so every one of the large club's members moved one hop further from the banner. If the large club were attached below the small one's holder no member of it would pay, and only the few members of the small club would. A fix should therefore decide the direction of every merge from the clubs' sizes and bound the depth of anyone's chain by something much smaller than n.

<!-- stage: insight -->
### The Smaller Club Joins The Bigger

Choose the direction by counting. For every banner holder the structure stores the **root size**, the number of students in that holder's club, and it stores it only at the holder: the entry for anyone else is left behind and never read again. A merge first finds the two holders. If they are the same student the students already share a club and nothing is written. Otherwise the holder with the larger root size keeps the banner, the other holder starts answering to it, and the keeper's root size grows by the other's. That is **union by size**: the smaller tree is attached under the larger one.

The payoff is a **height bound**. A student's chain gets one link longer only when their holder is attached under another holder, and that happens only when their club is the smaller or the equal one. So the club that student belongs to at least doubles each time. A club cannot double more than log2 n times before it holds all n students, so nobody is ever more than log2 n hops from a banner. A merge and a lookup both cost O(log n), even with no path compression at all.

The invariant is that every student's chain ends at a holder, and the root size stored at that holder equals the real number of members. Both halves can be broken by comparing students instead of holders. The entry of an ordinary student is stale, and writing a total there leaves the true holder's count wrong.

<!-- names: union by size, root size, height bound -->

<!-- stage: variables -->
### Parents, Counts And Both Holders

The array `parent` holds, for each student, the one person they answer to, with `parent[i] == i` marking a banner holder. The array `size` is meaningful only at holders and starts at 1 everywhere, since each student begins as a one-member club. The integer `count` is the number of clubs left, which starts at n. In `union`, the students are `a` and `b`, their holders are `ra` and `rb`, and the holder that keeps the banner is `big` while `small` is the one that gives it up. Every write to `parent` and to `size` happens after both holders are known.

<!-- stage: trace -->
### Two Runs Of Merges

The first trace uses nine students and eight merge requests, listed as the cells in the order they arrive. The pointer `i` is the request being handled. The vars show the two holders found, the holder that ends up with the banner, its new root size and the number of clubs left. The fifth request joins a lone student 6 to a club of two, so the lone student gives up its banner, and the sixth joins a club of four to a club of three, so the smaller side moves. The seventh request names two students who already share a club, and it changes nothing.

```trace
{"cells":["0-1","2-3","1-3","4-5","6-4","3-5","2-0","7-8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ra":0,"rb":1,"keeper":0,"rootSize":2,"clubs":8},"note":"Holders 0 and 1 are found first. Holder 1 gives up its banner and answers to 0, whose size becomes 2."},{"at":{"i":1},"vars":{"ra":2,"rb":3,"keeper":2,"rootSize":2,"clubs":7},"note":"Holders 2 and 3 are found first. Holder 3 gives up its banner and answers to 2, whose size becomes 2."},{"at":{"i":2},"vars":{"ra":0,"rb":2,"keeper":0,"rootSize":4,"clubs":6},"note":"Holders 0 and 2 are found first. Holder 2 gives up its banner and answers to 0, whose size becomes 4."},{"at":{"i":3},"vars":{"ra":4,"rb":5,"keeper":4,"rootSize":2,"clubs":5},"note":"Holders 4 and 5 are found first. Holder 5 gives up its banner and answers to 4, whose size becomes 2."},{"at":{"i":4},"vars":{"ra":6,"rb":4,"keeper":4,"rootSize":3,"clubs":4},"note":"Holders 6 and 4 are found first. Holder 6 gives up its banner and answers to 4, whose size becomes 3."},{"at":{"i":5},"vars":{"ra":0,"rb":4,"keeper":0,"rootSize":7,"clubs":3},"note":"Holders 0 and 4 are found first. Holder 4 gives up its banner and answers to 0, whose size becomes 7."},{"at":{"i":6},"vars":{"ra":0,"rb":0,"keeper":0,"rootSize":7,"clubs":3},"note":"Students 2 and 0 both lead to holder 0, so they already share a club and nothing is written."},{"at":{"i":7},"vars":{"ra":7,"rb":8,"keeper":7,"rootSize":2,"clubs":2},"note":"Holders 7 and 8 are found first. Holder 8 gives up its banner and answers to 7, whose size becomes 2."}]}
```

The second trace makes the same seven students merge student 0 with each of 1 to 6 in turn, the order that built a chain in the naive rule. The vars compare the two rules side by side. The value `naiveDepth` is how many hops student 0 needs under the hang-the-first-banner rule, and `sizeDepth` is the longest chain anywhere under the smaller-joins-bigger rule. The first grows with every merge while the second stays at one.

```trace
{"cells":["0-1","0-2","0-3","0-4","0-5","0-6"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"naiveDepth":1,"sizeDepth":1},"note":"After merging 0 with 1, student 0 needs 1 hop under the naive rule, while the longest chain under the size rule is 1."},{"at":{"i":1},"vars":{"naiveDepth":2,"sizeDepth":1},"note":"After merging 0 with 2, student 0 needs 2 hops under the naive rule, while the longest chain under the size rule is 1."},{"at":{"i":2},"vars":{"naiveDepth":3,"sizeDepth":1},"note":"After merging 0 with 3, student 0 needs 3 hops under the naive rule, while the longest chain under the size rule is 1."},{"at":{"i":3},"vars":{"naiveDepth":4,"sizeDepth":1},"note":"After merging 0 with 4, student 0 needs 4 hops under the naive rule, while the longest chain under the size rule is 1."},{"at":{"i":4},"vars":{"naiveDepth":5,"sizeDepth":1},"note":"After merging 0 with 5, student 0 needs 5 hops under the naive rule, while the longest chain under the size rule is 1."},{"at":{"i":5},"vars":{"naiveDepth":6,"sizeDepth":1},"note":"After merging 0 with 6, student 0 needs 6 hops under the naive rule, while the longest chain under the size rule is 1."}]}
```

<!-- stage: code -->
### A Club Registry With Sizes

```java
final class ClubRegistry {
    private final int[] parent;
    private final int[] size;
    private int count;

    ClubRegistry(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        count = n;
    }

    int find(int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        int big = size[ra] >= size[rb] ? ra : rb;
        int small = big == ra ? rb : ra;
        parent[small] = big;
        size[big] += size[small];
        count--;
        return true;
    }

    int clubSize(int x) { return size[find(x)]; }
    int clubs() { return count; }
}
```

The `find` here has no path compression, so the log2 n bound comes from the attach rule alone. Adding compression later only shortens chains further. The method `union` returns true when two clubs really merged and false when they were already one, and a caller such as an edge scanner can use that result directly. Time per call is O(log n), memory is O(n), and `clubSize` reads `size` at the holder, never at the student asked about.

<!-- stage: applicability -->
### When Merges Must Stay Shallow

Reach for this when two groups are repeatedly fused and the next question is only "same group?" or "how big is this group?". The recognition cue is a stream of merges with no deletions, such as friend requests, cables joining machines, or edges that arrive one at a time. The invariant to defend is that `size` is correct at every holder and that a holder is always found before anything is written, so the chain from any element stays within log2 n links.

The false friend is the size of the elements you were handed. Reading `size[a]` and `size[b]` looks right while the clubs are single students, and it quietly breaks once one of them has been absorbed, because that entry is stale and the total ends up written at the wrong place. Do not use this structure when groups must be split again, when members have to be listed in order, or when you need the actual route between two elements. It records membership only. In Java the trap is `new int[n]`, which is zero-filled: a `size` array that is never set to 1 makes every comparison a tie, and the structure falls back to the naive chains without any exception to warn you.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Two Roots (Author exercise)
<!-- id: ug-merge-two-roots -->

**Prerequisites.** The `find` walk from the previous lesson and the size-based attach rule from this one.

**Problem.** There are `n` elements numbered 0 to n-1, each in its own group, and `pairs` is a list of merge requests applied in order. For a request `[a, b]`, first find the root of each element. If the roots are equal, skip the request. Otherwise the root with the larger group size becomes the parent of the other, and when the sizes are equal the root of `a` stays on top. Only the receiving root's size changes. Return the final `parent` array as a new `int[]`, with `find` used without path compression so the links are exactly those written by the merges. The input is not modified.

**Constraints.** 1 <= n <= 1000, 0 <= pairs.length <= 2000, and every element is between 0 and n-1. A pair may repeat or name the same element twice.

**Example 1.** Input `n = 5, pairs = [[0,1],[2,3],[1,3]]`, output `[0,0,0,2,4]`.

**Example 2.** Input `n = 6, pairs = [[3,2],[1,0],[2,1],[4,3],[5,4]]`, output `[1,3,3,3,3,3]`.

**Hint.** Which two numbers decide the direction of a link, and are they read before or after the elements are walked up to their roots?

**Changed decision.** Links are written between the two roots that were found first, instead of between the two elements that were given.

#### [Vary] Repeated Unequal Merges (Author exercise)
<!-- id: ug-repeated-unequal -->

**Prerequisites.** The Merge Two Roots rung.

**Problem.** The same merging process runs on `n` elements and the list `pairs`, but now the output is a record of growth. Return an `int[]` with one entry per request, where entry `k` is the size of the largest group after the first `k+1` requests have been processed. Before any request the largest group has size 1. A request between two elements of one group changes nothing, and its entry repeats the previous value. The `pairs` array is not modified.

**Constraints.** 1 <= n <= 1000 and 0 <= pairs.length <= 2000. Every element is between 0 and n-1.

**Example 1.** Input `n = 6, pairs = [[0,1],[2,3],[1,3],[4,5],[0,2]]`, output `[2,2,4,4,4]`.

**Example 2.** Input `n = 7, pairs = [[5,6],[4,5],[3,4],[0,1],[2,3],[1,6]]`, output `[2,3,4,4,5,7]`.

**Hint.** After a real merge, which of the two roots holds the new total, and which entry should the running maximum read?

**Changed decision.** The answer is read from the size of the receiving root after each merge, instead of only the parent links being rebuilt.

#### [Boundary] Already Connected (Author exercise)
<!-- id: ug-already-connected -->

**Prerequisites.** The Repeated Unequal Merges rung.

**Problem.** Process `pairs` over `n` elements as before and return an `int[]` of three values: the number of groups left, the number of requests that were ignored because the two elements already shared a root, and the size of the largest group at the end. A request that names one element twice, or repeats an earlier request in either direction, counts as ignored. An ignored request must not change any size or reduce the group count. The `pairs` array is not modified.

**Constraints.** 1 <= n <= 1000 and 0 <= pairs.length <= 2000, with every element between 0 and n-1.

**Example 1.** Input `n = 4, pairs = [[0,1],[1,0],[2,2]]`, output `[3,2,2]`.

**Example 2.** Input `n = 5, pairs = [[0,1],[1,2],[2,0],[0,2],[3,4]]`, output `[2,2,3]`.

**Hint.** Where in the loop must the equal-roots check sit so that neither a size nor the count has been touched yet?

**Changed decision.** A request whose roots match exits before any write, instead of merging a root into itself.

#### [Recognize] Redundant Connection (LeetCode 684)
<!-- id: ug-redundant-connection -->

**Prerequisites.** The Already Connected rung, and the idea that an undirected cycle is closed by an edge inside one component.

**Problem.** A tree with `n` vertices numbered 0 to n-1 had one extra edge added, so `edges` holds exactly `n` pairs, none repeated and none joining a vertex to itself. Return the edge, as a new two-element `int[]` in the same order its endpoints appear in the input, that completes the cycle when edges are added one by one in input order. Equivalently, it is the last edge in the input whose removal leaves a tree. The `edges` array is not modified.

**Constraints.** 3 <= n <= 1000, `edges.length == n`, and the graph is connected before the extra edge is considered. Vertices are numbered from 0, unlike the original LeetCode statement.

**Example 1.** Input `n = 3, edges = [[0,1],[1,2],[0,2]]`, output `[0,2]`.

**Example 2.** Input `n = 5, edges = [[0,1],[1,2],[2,0],[2,3],[3,4]]`, output `[2,0]`.

**Hint.** When an edge arrives, what must be true of the two roots for the edge to be the one that closes a loop?

**Changed decision.** The edge scanner stops at the first request that merges nothing, instead of continuing to build the full structure.
