<!-- lesson-kind: combination -->
<!-- lesson-id: tree-dfs-returns -->
## Tree DFS Returns

<!-- stage: context -->
### Four Questions About One Phone Tree

A neighbourhood committee spreads news through a phone tree. One organiser calls up to two neighbours, each of whom calls up to two more, and so on, and every household sits below exactly one caller. The committee keeps asking questions about this one tree. How many rounds of calls does the news need to reach the last household? What is the longest chain of calls that links two households, counted by the households on it? Is the tree evenly spread, so that at every household the two branches below it take about the same number of rounds? And if each household has a goodwill score, some of them negative, which chain of connected households has the largest total?

The committee clerk has been answering each question with a fresh search through the tree, and the searches keep repeating each other's work. She suspects that one careful visit of every household should be enough to answer all four.

<!-- stage: contributions -->
### What Each Structure Brings

The tree brings ownership. Every household owns exactly one group below it, made of its own two branches, and no group belongs to two households. A question about the whole tree therefore splits into the same question about each branch, and the branches can be handled by the same method one after another, which is what a depth-first visit does.

The depth-first visit brings the moment of return. A household is handled after both branches have been finished, so it can use what they report and then report in turn to the household above. What it lacks is a rule about what to report, since a complete answer to some questions is not something a parent can build upon, such as a chain that already uses both branches of a household.

The recognition cue is a question about the whole tree whose answer at a household depends on the finished answers of its two branches, where the parent needs only part of what the household knows.

<!-- stage: naive -->
### Measure Heights At Every Household

The direct method answers the combined questions with one recursion that stops at each household and measures both of its branches from scratch, then uses the two heights to update the longest chain and the worst imbalance, and then moves on to the branches.

```java
static int height(Node house) {
    if (house == null) return 0;
    return 1 + Math.max(height(house.left), height(house.right));
}

static int[] byRemeasuring(Node house) {
    if (house == null) return new int[] {0, 0};
    int l = height(house.left), r = height(house.right);
    int[] a = byRemeasuring(house.left), b = byRemeasuring(house.right);
    return new int[] {
        Math.max(l + r, Math.max(a[0], b[0])),
        Math.max(Math.abs(l - r), Math.max(a[1], b[1]))
    };
}
```

The first entry is the longest chain in steps and the second the worst difference between two branches, and both are right because each household considers its own two branches.

<!-- stage: bottleneck -->
### The Same Branches Are Measured Again

Every household calls the height method on both of its branches, and each such call walks the whole branch below. On a phone tree that is one long line of n households, the top one measures n - 1 below it, the next n - 2, and so on, because no call stops early, and the total is O(n^2). A line of a hundred thousand households would need billions of steps, even though the recursion that visits each household already passes through every branch.

The measuring is also tied to the first two questions alone. The goodwill question needs a different number from each branch, the best total of a chain that starts at the top of the branch and goes down, and adding it means a third helper that walks the branches yet again. A scheme where each household receives the finished report of its two branches would take O(1) per household, O(n) in all, and one pass could carry the measurement for whichever question is asked.

<!-- stage: insight -->
### Report One Thing, Answer Another

Every question has two separate pieces of data at a household, and keeping them apart is the whole design. The **return state** is the small report handed to the parent: the height, the height or a failure mark, or the best chain total that goes down through one branch. The **local answer** is a complete result that is formed at this household from both reports and never handed up: the chain that uses both branches, the imbalance between them, the best total of a bent chain. The local answer is folded into a running result held outside the recursion, and the return state travels up.

The **combine step** takes the two child return states and the household's own value and produces both pieces. For depth the state is one plus the larger height and there is no local answer. For the longest chain, the state is the same height and the local answer is the sum of the two heights. For balance, the state is the height or the failure mark, and a failure at either child, or an imbalance beyond the limit, produces the mark at once. For the goodwill chain, the state is the household's score plus the better branch, cut off at zero, and the local answer is the score plus both cut-off branches.

The invariant is that the return state describes only a downward branch the parent can extend, while the running result holds the best complete answer over every household finished so far. Each household is combined once, so the work is O(n), and the extra memory is the stack of the tree height.

<!-- names: return state, local answer, combine step -->

If a local answer were returned as the state, a parent would extend a chain that already forks, and the answer would describe no real chain.

<!-- stage: variables -->
### State, Local Result And Running Best

Each recursion has three parts that must be named separately in the code. The returned value is the state, an `int` or a small `int[]`. The local answer is a local variable computed from the two child states after both calls finish. The running best is a field or a one-element array that the combine step updates and that is reset before every query. A failure mark must lie outside the valid states: with heights that are never negative, -1 serves, and a null child returns the plain zero state.

<!-- stage: trace -->
### One Pass Answers Three Questions

The first trace walks the phone tree 1, 2, 3, 4, null, null, 5, given in level order, and follows three quantities at once. The pointer `node` marks the household that has just received both reports. Its columns are the height it reports, the longest chain found so far in steps, and the worst imbalance found so far. The household 2 is lopsided with one branch of height 1 and none on the other side, and the top household sees two equal branches and closes the longest chain at four steps.

```trace
{"cells":["1","2","3","4","null","null","5"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"height":1,"chain":0,"gap":0},"note":"The household 4 receives the branch heights 0 and 0, so its local chain is 0 steps and its imbalance is 0, and it reports the height 1."},{"at":{"node":1},"vars":{"height":2,"chain":1,"gap":1},"note":"The household 2 receives the branch heights 1 and 0, so its local chain is 1 steps and its imbalance is 1, and it reports the height 2."},{"at":{"node":6},"vars":{"height":1,"chain":1,"gap":1},"note":"The household 5 receives the branch heights 0 and 0, so its local chain is 0 steps and its imbalance is 0, and it reports the height 1."},{"at":{"node":2},"vars":{"height":2,"chain":1,"gap":1},"note":"The household 3 receives the branch heights 0 and 1, so its local chain is 1 steps and its imbalance is 1, and it reports the height 2."},{"at":{"node":0},"vars":{"height":3,"chain":4,"gap":1},"note":"The household 1 receives the branch heights 2 and 2, so its local chain is 4 steps and its imbalance is 0, and it reports the height 3."}]}
```

The second trace asks the goodwill question on the tree 2, -1, 3, null, 4. Each household reports the gain of the best branch that starts at it, cut off at zero, and separately forms the best bent chain through itself. The two numbers differ at the top household, which reports 5 upward but forms a chain worth 8 through itself, and only the report can be extended by a parent.

```trace
{"cells":["2","-1","3","null","4"],"pointers":["node"],"steps":[{"at":{"node":4},"vars":{"gain":4,"through":4,"best":4},"note":"The household 4 gets the usable branch gains 0 and 0, so the chain through it is worth 4, while the gain it reports upward is 4."},{"at":{"node":1},"vars":{"gain":3,"through":3,"best":4},"note":"The household -1 gets the usable branch gains 0 and 4, so the chain through it is worth 3, while the gain it reports upward is 3."},{"at":{"node":2},"vars":{"gain":3,"through":3,"best":4},"note":"The household 3 gets the usable branch gains 0 and 0, so the chain through it is worth 3, while the gain it reports upward is 3."},{"at":{"node":0},"vars":{"gain":5,"through":8,"best":8},"note":"The household 2 gets the usable branch gains 3 and 3, so the chain through it is worth 8, while the gain it reports upward is 5."}]}
```

<!-- stage: code -->
### Return A State And Fold An Answer

```java
final class DfsReturns {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int bestChain, worstGap, bestSum;

    static int heightState(Node node) {
        if (node == null) return 0;
        int l = heightState(node.left);
        int r = heightState(node.right);
        bestChain = Math.max(bestChain, l + r);
        worstGap = Math.max(worstGap, Math.abs(l - r));
        return 1 + Math.max(l, r);
    }

    static int gainState(Node node) {
        if (node == null) return 0;
        int l = Math.max(0, gainState(node.left));
        int r = Math.max(0, gainState(node.right));
        bestSum = Math.max(bestSum, node.val + l + r);
        return node.val + Math.max(l, r);
    }
}
```

Each node is combined once with constant work, so both walks take O(n) time and O(h) stack. The reset of the three fields before each query is part of the contract of the methods that call them.

<!-- stage: applicability -->
### A Parent Needs Only Part

Reach for this pattern when a question about a whole tree is answered by a best, a count or a check over all households, and a household can form its result from the finished reports of its branches. Examples are longest paths, heaviest paths, validity checks that also need a size, and most-frequent-subtree questions. The invariant is that the return state is only what the parent can extend, and the local answer goes to the running result.

A false friend is returning the complete answer upward, which is correct when the answer is a single height and wrong for a chain that can fork. A second false friend is remeasuring with a separate helper at each household, which restores the O(n^2) cost. A third is a failure mark that lies inside the valid range, which turns a good report into a failure.

In Java, reset the running result at the start of each query, because a static field keeps the last tree's answer, and start it at the smallest valid value for the question, not at zero by habit, since sums can be negative.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Depth of Binary Tree (LeetCode 104)
<!-- id: td-height-and-deepest -->

**Prerequisites.** The depth lesson and the diameter lesson of this chapter.

**Problem.** For a level-order tree, return `[height, deepest]`, where height counts nodes on the longest root-to-leaf path and `deepest` is the number of leaves that lie at that depth. The empty tree gives `[0, 0]`.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -100 and 100.

**Example 1.** Input `values = [1, 2, 3, 4]`, output `[3, 1]`.

**Example 2.** Input `values = [1, 2, 3, 4, null, null, 5]`, output `[3, 2]`.

**Hint.** What must each household report so that its parent can tell which branch is deeper, and what happens at a tie?

**Changed decision.** The state is a pair, and the counts of the two branches are added only when their heights are equal.

#### [Vary] Diameter of Binary Tree (LeetCode 543)
<!-- id: td-diameter-turns -->

**Prerequisites.** The Build rung above and the running result.

**Problem.** For a level-order tree, return `[diameter, turns]`, the largest number of edges on a path between two nodes, and the number of nodes at which some path of that length turns, meaning the highest node of such a path. The empty tree gives `[0, 0]`, and a single node gives `[0, 1]`.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -100 and 100.

**Example 1.** Input `values = [1, 2, 3]`, output `[2, 1]`.

**Example 2.** Input `values = [1, 2, null, 3, 4]`, output `[2, 2]`.

**Hint.** What does a household compare its local sum with, and why can the final count not be decided until the whole tree is done?

**Changed decision.** The running result must hold a best and a count of how often it was reached, and it restarts the count whenever a larger value is found.

#### [Boundary] Balanced Binary Tree (LeetCode 110)
<!-- id: td-weighted-balance -->

**Prerequisites.** The Vary rung and the failure mark from the balance lesson.

**Problem.** Each node has a non-negative weight, its value, and the height of a node is its weight plus the larger height of its two branches, with 0 for a missing branch. For a level-order tree and an integer `k` with `k >= 0`, return whether at every node the two branch heights differ by at most `k`.

**Constraints.** 0 <= values.length <= 5000, weights are integers between 0 and 100, and 0 <= k <= 1000.

**Example 1.** Input `values = [3, 1, 2]`, `k = 1`, output `true`.

**Example 2.** Input `values = [3, 1, 2]`, `k = 0`, output `false`.

**Hint.** Which value can never be a height when weights are not negative, and where is it checked?

**Changed decision.** Heights are sums of weights and the tolerance is a parameter, while the sentinel stays outside the valid heights and a failed branch ends the call before any comparison.

#### [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: td-path-sum-turn -->

**Prerequisites.** The Boundary rung and the cut-off at zero.

**Problem.** For a non-empty level-order tree, return `[bestSum, turn]`, the largest sum over any path that follows parent-child links, and the smallest value among the highest nodes of paths that reach that sum. Values may be negative.

**Constraints.** 1 <= values.length <= 3000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [2, -1, 3, null, 4]`, output `[8, 2]`.

**Example 2.** Input `values = [-4]`, output `[-4, -4]`.

**Hint.** Which of the two numbers computed at a node can a parent use, and which feeds the running result?

**Changed decision.** The running result keeps the best sum together with the smallest top value that achieved it, so ties are resolved while the walk is still running.
