<!-- lesson-kind: standard -->
<!-- lesson-id: find-compression -->
## Find Compression

<!-- stage: context -->
### Answering Same-Group Queries While Groups Merge

A monitoring service receives events of the form "machine `a` is now linked to machine `b`". Between events, operators ask whether two machines can reach each other through the links seen so far. A search through the link graph answers one question in O(V + E), and a busy service receives hundreds of thousands of questions. A slow answer delays an alert while an outage spreads.

Model the machines as the numbers `0` to `n - 1`. A group is the set of machines that can reach one another. Two operations arrive in any order. The first merges the groups of two machines. The second asks whether two machines are in the same group. Groups only merge and never split.

This lesson asks how to keep both operations cheap when the same groups merge and receive thousands of questions.

<!-- stage: naive -->
### Storing A Group Number Per Machine

The first attempt keeps one group number for every machine. Two machines are in the same group when their numbers are equal, so a question costs one comparison. A merge overwrites every number of the second group with the number of the first group.

```java
static int[] label;

static void init(int n) {
    label = new int[n];
    for (int i = 0; i < n; i++) label[i] = i;
}

static void merge(int a, int b) {
    int keep = label[a];
    int drop = label[b];
    if (keep == drop) return;
    for (int i = 0; i < label.length; i++) {
        if (label[i] == drop) label[i] = keep;
    }
}

static boolean sameGroup(int a, int b) {
    return label[a] == label[b];
}
```

Suppose 1000 machines start alone, and the events link machine 0 to 1, then 1 to 2, and so on up to 998 to 999.

```predict
About how many array reads do these 999 merges perform in total?

About one million. Each merge scans all 1000 entries of the array, even though only one entry changes in the first merge and few change in the next ones. The cost per merge depends on n, and not on the size of the groups involved.
```

<!-- stage: bottleneck -->
### A Merge That Scans Every Machine

A question costs O(1), but a merge costs O(n) because the loop checks every machine to find the members of one group. A sequence of m operations with n machines costs O(n * m), which is about 10^10 steps for n and m near 10^5. The scan is wasteful, because a merge changes the group of only a few machines in many sequences.

A cheaper merge changes one entry. Give each machine one link to another machine in its group, and let exactly one machine per group link to itself. Merging two groups then redirects the self-linked machine of one group to a machine of the other, which is one write. The price moves to the question. To compare two machines, the method follows links until it reaches a self-linked machine, and the link path can be as long as the group.

Merging 0 into 1, then 1 into 2, and so on creates one long chain, so a single question costs O(n) and m questions cost O(n * m) again. The slowness has moved and has not disappeared. A repair must keep each chain short after one walk. The next stage names that step.

<!-- stage: insight -->
### Shortening The Path While Walking It

A question that walks a long path has already paid for the walk. It can rewrite the links it passed, so the next question over the same machines is cheap.

<!-- names: root, chain, path compression -->

#### Links And The Root

Each machine `x` stores `parent[x]`, the machine it links to. A machine with `parent[x] == x` is the **root** of its group, and each group has exactly one root. Following the links from any machine of the group ends at that root. Two machines are in the same group exactly when their roots are equal. At the start every machine is its own root, so `n` groups of size one exist.

#### Walking And Rewriting The Path

The method `find(x)` works in two passes. The first pass follows the links from `x` until it reaches the root. The second pass walks the same links again and sets `parent` of each visited machine to the root. This rewrite is **path compression**. A long **chain** of links becomes a star in which every visited machine points straight at the root.

The rewrite is safe because it changes no root. A machine still leads to the same root after its link changes, so the groups stay the same sets. Only the number of steps changes.

#### Merging And The Cost

A merge calls `find` on both machines and, when the roots differ, sets `parent` of one root to the other. The invariant is that following `parent` from any machine reaches exactly one root, and that compression never changes which root that is. A first `find` on a chain of length k costs k steps. Afterwards each machine on that chain is one step from the root. Over a sequence of m operations, compression alone gives O(log n) amortized cost per operation, a known result that this lesson uses without proof. The next lesson adds a rule for merging that brings the cost close to constant.

<!-- stage: variables -->
### What The Structure Keeps

The structure keeps one array, and each call keeps three integers. The root represents a group, so no list of members exists.

- **parent** is an int array of length `n`; `parent[x] == x` marks `x` as a root, and any other value is the next machine toward the root.
- **x** is the machine passed to `find`; the method never changes it.
- **root** is the int that the first pass finds, the machine with `parent[root] == root`.
- **cur** is the machine the second pass is rewriting; it moves from `x` toward the root.

<!-- stage: trace -->
### Compressing Paths On Two Trees

#### A Chain Of Five Machines

The first structure is a chain. Machine 0 is the root, and each other machine links to its left neighbor: machine 1 to 0, machine 2 to 1, and so on up to machine 4. The cells are the machine ids and the pointer `cur` shows the machine under work. The variable `parents` lists `parent[0]` to `parent[4]`. The call `find(4)` walks four links in its first pass. Its second pass then rewrites the links of machines 4, 3 and 2, and the link of machine 1 already points at the root.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":4},"vars":{"parents":"0-0-1-2-3","phase":"walk","root":"unknown"},"note":"The call find(4) starts its first pass at machine 4."},{"at":{"cur":3},"vars":{"parents":"0-0-1-2-3","phase":"walk","root":"unknown"},"note":"Machine 4 links to machine 3, so the walk moves there. Links followed so far: 1."},{"at":{"cur":2},"vars":{"parents":"0-0-1-2-3","phase":"walk","root":"unknown"},"note":"Machine 3 links to machine 2, so the walk moves there. Links followed so far: 2."},{"at":{"cur":1},"vars":{"parents":"0-0-1-2-3","phase":"walk","root":"unknown"},"note":"Machine 2 links to machine 1, so the walk moves there. Links followed so far: 3."},{"at":{"cur":0},"vars":{"parents":"0-0-1-2-3","phase":"walk","root":0},"note":"Machine 1 links to machine 0, so the walk moves there. Links followed so far: 4. Machine 0 links to itself, so it is the root."},{"at":{"cur":4},"vars":{"parents":"0-0-1-2-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 4 to root 0 and then moves to machine 3."},{"at":{"cur":3},"vars":{"parents":"0-0-1-0-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 3 to root 0 and then moves to machine 2."},{"at":{"cur":2},"vars":{"parents":"0-0-0-0-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 2 to root 0 and then moves to machine 1."},{"at":{"cur":1},"vars":{"parents":"0-0-0-0-0","phase":"rewrite","root":0},"note":"Machine 1 already links to root 0, so the second pass stops. The call returns 0 after 4 links."}]}
```

#### A Branching Tree With Two Calls

The second structure has seven machines, and the links for machines 0 to 6 are 0, 0, 1, 2, 3, 3 and 4. Machine 6 sits five links from the root. The call `find(6)` rewrites machines 6, 4, 3 and 2, so each of them points straight at the root. The later call `find(5)` benefits from the first call. Machine 3 now points at the root, so the walk from machine 5 takes two links, where it took four before.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["cur"],"steps":[{"at":{"cur":6},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":"unknown"},"note":"The call find(6) starts its first pass at machine 6."},{"at":{"cur":4},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":"unknown"},"note":"Machine 6 links to machine 4, so the walk moves there. Links followed so far: 1."},{"at":{"cur":3},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":"unknown"},"note":"Machine 4 links to machine 3, so the walk moves there. Links followed so far: 2."},{"at":{"cur":2},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":"unknown"},"note":"Machine 3 links to machine 2, so the walk moves there. Links followed so far: 3."},{"at":{"cur":1},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":"unknown"},"note":"Machine 2 links to machine 1, so the walk moves there. Links followed so far: 4."},{"at":{"cur":0},"vars":{"parents":"0-0-1-2-3-3-4","phase":"walk","root":0},"note":"Machine 1 links to machine 0, so the walk moves there. Links followed so far: 5. Machine 0 links to itself, so it is the root."},{"at":{"cur":6},"vars":{"parents":"0-0-1-2-3-3-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 6 to root 0 and then moves to machine 4."},{"at":{"cur":4},"vars":{"parents":"0-0-1-2-0-3-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 4 to root 0 and then moves to machine 3."},{"at":{"cur":3},"vars":{"parents":"0-0-1-0-0-3-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 3 to root 0 and then moves to machine 2."},{"at":{"cur":2},"vars":{"parents":"0-0-0-0-0-3-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 2 to root 0 and then moves to machine 1."},{"at":{"cur":1},"vars":{"parents":"0-0-0-0-0-3-0","phase":"rewrite","root":0},"note":"Machine 1 already links to root 0, so the second pass stops. The call returns 0 after 5 links."},{"at":{"cur":5},"vars":{"parents":"0-0-0-0-0-3-0","phase":"walk","root":"unknown"},"note":"The call find(5) starts its first pass at machine 5."},{"at":{"cur":3},"vars":{"parents":"0-0-0-0-0-3-0","phase":"walk","root":"unknown"},"note":"Machine 5 links to machine 3, so the walk moves there. Links followed so far: 1."},{"at":{"cur":0},"vars":{"parents":"0-0-0-0-0-3-0","phase":"walk","root":0},"note":"Machine 3 links to machine 0, so the walk moves there. Links followed so far: 2. Machine 0 links to itself, so it is the root."},{"at":{"cur":5},"vars":{"parents":"0-0-0-0-0-0-0","phase":"rewrite","root":0},"note":"The second pass sets the link of machine 5 to root 0 and then moves to machine 3."},{"at":{"cur":3},"vars":{"parents":"0-0-0-0-0-0-0","phase":"rewrite","root":0},"note":"Machine 3 already links to root 0, so the second pass stops. The call returns 0 after 2 links."}]}
```

<!-- stage: code -->
### Find With Two Passes And Merge

The class below stores the links, returns the root of a machine with compression and merges two groups.

```java
static final class Groups {
    private final int[] parent;

    Groups(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        int cur = x;
        while (parent[cur] != root) {
            int next = parent[cur];
            parent[cur] = root;
            cur = next;
        }
        return root;
    }

    boolean merge(int a, int b) {
        int ra = find(a);
        int rb = find(b);
        if (ra == rb) return false;
        parent[ra] = rb;
        return true;
    }

    boolean sameGroup(int a, int b) {
        return find(a) == find(b);
    }
}
```

The second loop must save `next` before it overwrites `parent[cur]`, or the walk loses its place. The loop is iterative on purpose, because a recursive `find` on a chain of 100000 machines overflows the default Java stack. The loop stops at `parent[cur] == root`, so it never rewrites a link that is already correct. Memory is O(n) for `parent`, and the amortized time per operation is O(log n) with this merge rule.

<!-- stage: applicability -->
### Recognizing Merge And Same-Group Queries

#### Reading The Cue

Use this structure when many operations ask which merged group contains an element, and groups only grow. Statements describe friends who become connected, edges that arrive one at a time, or equivalence relations such as "these two accounts are the same person". The answer needs only the group identity or the number of groups, and never the path between two elements.

#### Checking The Invariant

The invariant is that following `parent` from any element reaches one root, and compression keeps that root unchanged. It breaks if code writes `parent[x]` for a machine that is not a root during a merge, because that cuts the machines below `x` away from their group. Merge only the roots that `find` returned.

#### Avoiding The False Friend

The false friend is a shortest-path or enumeration task that sounds similar. The structure stores only group membership, so it cannot list the machines on a route or report the length of one. It also cannot remove a link, because compression has already discarded the original paths. When a task needs deletions, routes or distances, use a graph search instead.

<!-- stage: exercises -->
### Exercises

#### [Build] Follow Parents To Root (Author exercise)
<!-- id: dg-follow-to-root -->

**Prerequisites.** The parent array of this lesson.

**Problem.** An int array `parent` of length `n` describes a forest. A vertex `v` with `parent[v] == v` is a root, and every other vertex leads to a root by repeated replacement `v = parent[v]`. For each query vertex `q`, return the root reached from `q` and the number of replacements performed. Return an `int[][]` in which row `i` is `{root, steps}` for `queries[i]`. The method must not modify `parent`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Forest** guarantee: no cycle other than a self link, so every walk ends.
- **Queries** satisfy `0 <= queries.length <= 10^5`, and each value is in `0..n-1`.
- **Result** has one row per query, in query order.

**Example 1.** Input `parent = [0,0,1,2,3]`, `queries = [4,0,2]`, output `[[0,4],[0,0],[0,2]]`.

**Example 2.** Input `parent = [0,1,1,2,4,4]`, `queries = [3,5,1]`, output `[[1,2],[4,1],[1,0]]`.

**Hint.** Which value of `parent[v]` tells the walk to stop, and what does the step count equal for a root?

**Changed decision.** The method follows the links with a loop and leaves the array unchanged, so every query pays for the full path again.

#### [Vary] Compress A Chain (Author exercise)
<!-- id: dg-compress-chain -->

**Prerequisites.** The exercise above.

**Problem.** An int array `parent` of length `n` describes a forest as in the previous exercise. Process the query vertices in order. For each query `q`, find its root and set `parent[v]` to that root for every vertex `v` on the path from `q` to the root. Vertices that are not on a queried path keep their links. Return the array `parent` after all queries.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Forest** guarantee: no cycle other than a self link.
- **Queries** satisfy `0 <= queries.length <= 10^5`, and each value is in `0..n-1`.
- **Result** is a new `int[]` of length `n`, and the input array is not modified.

**Example 1.** Input `parent = [0,0,1,2,3]`, `queries = [4]`, output `[0,0,0,0,0]`.

**Example 2.** Input `parent = [0,0,1,2,3]`, `queries = [2,3]`, output `[0,0,0,0,3]`.

**Hint.** The second example leaves machine 4 untouched. Which vertices does a query rewrite, and when must the method save the next link?

**Changed decision.** After the walk reaches the root, the method walks the path again and points each visited vertex directly at the root, saving the old link before overwriting it.

#### [Boundary] Singleton Components (Author exercise)
<!-- id: dg-singleton-components -->

**Prerequisites.** The two exercises above.

**Problem.** A structure starts with `n` elements `0` to `n - 1`, and each element is alone in its own group. An operation is `{0, a, b}` to merge the groups of `a` and `b`, or `{1, a, b}` to ask whether `a` and `b` are in the same group. Process the operations in order and return a `boolean[]` with one answer for every operation of type 1. A merge of two elements that already share a group changes nothing.

**Constraints.** The limits are:
- **Elements** satisfy `1 <= n <= 10^5`.
- **Operations** satisfy `0 <= ops.length <= 10^5`, and `a` and `b` are in `0..n-1`.
- **Equal arguments** occur, so `a == b` is possible.
- **Result** has one entry per type 1 operation, in order.

**Example 1.** Input `n = 3`, `ops = [[1,0,0],[1,0,1],[0,0,1],[1,0,1]]`, output `[true,false,true]`.

**Example 2.** Input `n = 4`, `ops = [[0,2,2],[1,2,3],[0,2,3],[0,3,2],[1,3,2],[1,1,1]]`, output `[false,true,true]`.

**Hint.** What is the root of an element that no merge has touched, and what does a merge of an element with itself do?

**Changed decision.** Every element starts as its own root. A merge links two different roots only, so equal arguments and repeated merges leave the array unchanged.

#### [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: dg-provinces -->

**Prerequisites.** All three exercises above.

**Problem.** There are `n` cities. The matrix `isConnected` has `isConnected[i][j] = 1` when cities `i` and `j` are directly connected, and 0 otherwise. A province is a maximal set of cities where any two cities have a direct or indirect connection. Return the number of provinces.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 200`.
- **Matrix** entries are 0 or 1, with `isConnected[i][i] = 1` and `isConnected[i][j] == isConnected[j][i]`.
- **Result** is one `int` from 1 to `n`.
- **Input** is not modified.

**Example 1.** Input `isConnected = [[1,1,0],[1,1,0],[0,0,1]]`, output `2`.

**Example 2.** Input `isConnected = [[1,0,0,1,0],[0,1,0,1,0],[0,0,1,0,0],[1,1,0,1,0],[0,0,0,0,1]]`, output `3`.

**Hint.** Start with `n` groups. How does the number of groups change when a merge succeeds, and when it finds equal roots?

**Changed decision.** The method merges the two cities of every matrix entry equal to 1. It lowers a counter only when the roots differ, so the counter ends at the number of remaining roots.
