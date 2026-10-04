<!-- lesson-kind: combination -->
<!-- lesson-id: tree-and-bfs -->
## Tree And BFS

<!-- stage: context -->
### The Snow Day Phone Tree

When snow closes a school, the principal calls two teachers, each teacher calls two parents, each parent calls two neighbours, and the news spreads down through the families in waves. The school board wants reports on how the news travelled. How many people were reached in each wave, and what did their numbers add up to? In what order should the waves be read out if the reader wants to alternate the direction of the roll call? Who was the first person and the last person of every wave? And in the following year the school switches to a plan where each caller phones as many people as they like.

The office clerk has the whole phone tree on paper, with every caller linked to the people they phone. She is asked to produce all these reports from the same paper, and she would like one method that serves every report.

<!-- stage: contributions -->
### What Each Structure Brings

The tree brings the shape. Every person has callers above and call-lists below, and nobody is reached twice, so a walk that leaves a person through each of the linked people reaches the whole school exactly once. What the tree does not bring by itself is an order of visiting that respects waves, because a walk down one branch reaches the deep families before the other branch's first one.

The first-in, first-out queue brings the order. People are added to the back as they are discovered and taken from the front, so everyone in one wave is handled before anyone in the next. What the queue lacks is a mark that says where one wave ends and the next begins, and it knows nothing about how many people a caller phones.

The recognition cue is a question about the whole tree that is answered one depth at a time, either as a summary, a selected position, or a reordered roll call, with the number of children per caller allowed to vary.

<!-- stage: naive -->
### Record Every Person And Sort By Wave

The direct method records, for every person, the wave number and the position in a left-to-right walk, then sorts all the records by wave and position, and finally cuts the sorted list into groups. A depth-first walk can supply both numbers, so no queue is needed.

```java
final class SortedWaves {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    record Seen(int wave, int order, int val) {}

    static List<List<Integer>> bySorting(Node root) {
        List<Seen> all = new ArrayList<>();
        collect(root, 0, all);
        all.sort(Comparator.comparingInt(Seen::wave).thenComparingInt(Seen::order));
        List<List<Integer>> groups = new ArrayList<>();
        for (Seen s : all) {
            if (groups.size() == s.wave()) groups.add(new ArrayList<>());
            groups.get(s.wave()).add(s.val());
        }
        return groups;
    }

    static void collect(Node n, int wave, List<Seen> all) {
        if (n == null) return;
        all.add(new Seen(wave, all.size(), n.val));
        collect(n.left, wave + 1, all);
        collect(n.right, wave + 1, all);
    }
}
```

The preorder position increases from left to right within one wave, so the sorted groups are exactly the waves in the right order.

<!-- stage: bottleneck -->
### Sorting Rebuilds Order That Was Free

The sort costs O(n log n) time and O(n) memory, and no wave can be reported until every person has been recorded and sorted. If the board only wants the first three waves of a school of a hundred thousand, the method still examines and sorts everyone. The depth-first collection also recurses as deep as the tree is tall, which is risky on a long chain of callers.

The waves are already in order at the moment of discovery. The people of one wave are discovered while the previous wave is being handled, so a queue produces them in sorted order with no comparisons at all, in O(n) total, and a report can stop after any wave. The sort is paying to rebuild a property that a queue gives for free. What remains is to find a clean boundary between waves, and to let a caller have any number of people to phone.

<!-- stage: insight -->
### One Queue Serves Every Report

A queue with a size snapshot, as in the first lesson of this chapter, handles one wave per outer iteration. The new point is that the work done while a wave is removed can be anything small. The method builds a **level summary**, a compact record of the wave such as its count and total, or its first and last person, or its list placed at the front or the back. Nothing about the queue changes between reports, only what is accumulated during the `size` removals.

A **child expansion** step does the discovery. For a binary tree it adds the left child and then the right child when they exist. For a tree with any number of children it loops over the caller's list of children and adds each one. The loop replaces two references by a collection, and nothing else in the method is different, which is why an N-ary tree needs no new idea.

A **direction rule** picks where a person lands in the wave's list. Alternating or every-third-wave reversal changes only this placement and never the order in which children are queued, because the next wave must still be discovered left to right.

The invariant is that at the start of each outer iteration the queue holds exactly one wave in left-to-right order, so each removal belongs to the summary being built, and the children it adds belong to the next one.

<!-- names: level summary, child expansion, direction rule -->

<!-- stage: variables -->
### Queue, Size And The Wave Record

The `queue` is an `ArrayDeque` of nodes or of node indexes, and the int `size` is read once per wave before any removal. The wave record is whatever the question needs: a pair `count` and `sum`, with `sum` held in a `long` when many values may be large, a list that is filled at one of its two ends, or the pair `first` and `last`. A `depth` counter is incremented after each outer iteration and drives the direction rule. For an N-ary tree the child collection is a `List<Integer>` of indexes, and the expansion loops over it in its given order, so the discovery order is the order of the lists.

<!-- stage: trace -->
### Wave Summaries On Two Phone Trees

The first trace summarises each wave of the tree 4, -2, 6, 1, null, 5, 9 by its count and total. The marker `node` rests on the person just removed from the queue. The variables `count` and `sum` grow during a wave and are written into the answer when the snapshot is used up. The second wave holds -2 and 6, which give a count of 2 and a sum of 4, and the third wave holds 1, 5 and 9.

```trace
{"cells":["4","-2","6","1","null","5","9"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"count":1,"sum":4,"queue":"-2 6"},"note":"The person 4 is removed from wave 1, so the count is 1 and the sum is 4; the queue behind holds -2 6. The snapshot of 1 is used up, so the pair [1, 4] is written for this wave."},{"at":{"node":1},"vars":{"count":1,"sum":-2,"queue":"6 1"},"note":"The person -2 is removed from wave 2, so the count is 1 and the sum is -2; the queue behind holds 6 1."},{"at":{"node":2},"vars":{"count":2,"sum":4,"queue":"1 5 9"},"note":"The person 6 is removed from wave 2, so the count is 2 and the sum is 4; the queue behind holds 1 5 9. The snapshot of 2 is used up, so the pair [2, 4] is written for this wave."},{"at":{"node":3},"vars":{"count":1,"sum":1,"queue":"5 9"},"note":"The person 1 is removed from wave 3, so the count is 1 and the sum is 1; the queue behind holds 5 9."},{"at":{"node":5},"vars":{"count":2,"sum":6,"queue":"9"},"note":"The person 5 is removed from wave 3, so the count is 2 and the sum is 6; the queue behind holds 9."},{"at":{"node":6},"vars":{"count":3,"sum":15,"queue":"empty"},"note":"The person 9 is removed from wave 3, so the count is 3 and the sum is 15; the queue behind holds empty. The snapshot of 3 is used up, so the pair [3, 15] is written for this wave."}]}
```

The second trace reads an N-ary tree given by the children lists [1, 2, 3], [4, 5], [], [6], [], [], [], where the labels are the positions. The root has three children, so the expansion loop adds three entries at once. The variable `queue` lists what waits behind the removed person, and the second wave holds 1, 2 and 3 and the third wave holds 4, 5 and 6 in the order the lists gave them.

```trace
{"cells":["0","1","2","3","4","5","6"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"wave":1,"queue":"1 2 3"},"note":"The person 0 is removed from wave 1 and it adds its 3 children 1 2 3 to the queue. This was removal 1 of 1, so wave 1 is complete."},{"at":{"node":1},"vars":{"wave":2,"queue":"2 3 4 5"},"note":"The person 1 is removed from wave 2 and it adds its 2 children 4 5 to the queue."},{"at":{"node":2},"vars":{"wave":2,"queue":"3 4 5"},"note":"The person 2 is removed from wave 2 and it has no children to add."},{"at":{"node":3},"vars":{"wave":2,"queue":"4 5 6"},"note":"The person 3 is removed from wave 2 and it adds its 1 children 6 to the queue. This was removal 3 of 3, so wave 2 is complete."},{"at":{"node":4},"vars":{"wave":3,"queue":"5 6"},"note":"The person 4 is removed from wave 3 and it has no children to add."},{"at":{"node":5},"vars":{"wave":3,"queue":"6"},"note":"The person 5 is removed from wave 3 and it has no children to add."},{"at":{"node":6},"vars":{"wave":3,"queue":"empty"},"note":"The person 6 is removed from wave 3 and it has no children to add. This was removal 3 of 3, so wave 3 is complete."}]}
```

<!-- stage: code -->
### Summaries, Reversed Waves And Children Lists

```java
final class WaveReports {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static List<long[]> countAndSum(Node root) {
        List<long[]> waves = new ArrayList<>();
        if (root == null) return waves;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            long sum = 0;
            for (int k = 0; k < size; k++) {
                Node n = queue.poll();
                sum += n.val;
                if (n.left != null) queue.add(n.left);
                if (n.right != null) queue.add(n.right);
            }
            waves.add(new long[] {size, sum});
        }
        return waves;
    }

    static List<List<Integer>> reverseEveryKth(Node root, int k) {
        List<List<Integer>> waves = new ArrayList<>();
        if (root == null) return waves;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        for (int depth = 0; !queue.isEmpty(); depth++) {
            int size = queue.size();
            LinkedList<Integer> wave = new LinkedList<>();
            boolean reversed = depth % k == k - 1;
            for (int i = 0; i < size; i++) {
                Node n = queue.poll();
                if (reversed) wave.addFirst(n.val); else wave.addLast(n.val);
                if (n.left != null) queue.add(n.left);
                if (n.right != null) queue.add(n.right);
            }
            waves.add(wave);
        }
        return waves;
    }

    static List<List<Integer>> naryWaves(List<List<Integer>> children) {
        List<List<Integer>> waves = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(0);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> wave = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                int who = queue.poll();
                wave.add(who);
                for (int child : children.get(who)) queue.add(child);
            }
            waves.add(wave);
        }
        return waves;
    }
}
```

Every person enters and leaves the queue once, so each method takes O(n) time, plus O(n) for the lists produced. The queue holds at most two adjacent waves, so the extra space is O(w) for the widest wave w.

<!-- stage: applicability -->
### When Waves Answer The Question

Use the queue with a wave snapshot when a question about a hierarchy is read depth by depth: headcount per management level, the first and last seat of each row in a layout tree, or a spread time in a contact network where each step is one wave. The invariant is that the queue holds exactly one wave at the start of each outer pass, so a summary, a selection or a placement rule can be applied during the removals.

The first false friend is the sorted-record method of the naive section, which gives the right groups and pays O(n log n) for a result the queue gets free. A second false friend is reading `size` inside the loop, which mixes waves. A third is applying the direction rule to the order of enqueueing: reversing the children changes who is discovered first in the next wave, so the roll call would no longer be left to right at the next level. There is also a no-go condition: when the structure is a general graph with cycles, a plain queue would revisit people and needs a visited set, which belongs to the graph chapters.

In Java, keep the snapshot in a local `int`, use `ArrayDeque` for the queue, and use `LinkedList` or a precomputed index for a list that is filled from both ends, since `ArrayList.add(0, x)` shifts every element.

<!-- stage: exercises -->
### Exercises

#### [Build] Level Order As Count And Sum (LeetCode 102)
<!-- id: tc-level-count-sum -->

**Prerequisites.** The levels lesson and the size snapshot.

**Problem.** A school phone tree is stored by levels, with `null` marking each missing person. For every wave, from the top, report the pair `[count, sum]`, where `count` is the number of people in the wave and `sum` is the total of their numbers, which can be negative.

**Constraints.** 0 <= values.length <= 3000 and every number is an integer between -1000 and 1000.

**Example 1.** Input `values = [3, 9, 20, null, null, 15, 7]`, output `[[1, 3], [2, 29], [2, 22]]`.

**Example 2.** Input `values = [1, -5, null, 2, null, -3]`, output `[[1, 1], [1, -5], [1, 2], [1, -3]]`.

**Hint.** What is the only thing kept during a wave instead of a list of people?

**Changed decision.** A wave leaves behind two numbers rather than a list, and they are filled in during the same `size` removals that discover the next wave.

#### [Vary] Zigzag In Blocks Of K (LeetCode 103)
<!-- id: tc-zigzag-every-kth -->

**Prerequisites.** The Count And Sum rung and the direction rule.

**Problem.** Read the waves from the top, but reverse the roll call of every k-th wave, namely the waves at depths k-1, 2k-1 and so on, and leave all other waves left to right. With k = 2 this is the familiar zigzag, and with k = 1 every wave is reversed. The order in which children are queued is never changed.

**Constraints.** 0 <= values.length <= 2000, 1 <= k <= 50, and numbers are integers between -1000 and 1000.

**Example 1.** Input `values = [1, 2, 3, 4, 5, 6, 7, 8, 9]`, `k = 3`, output `[[1], [2, 3], [7, 6, 5, 4], [8, 9]]`.

**Example 2.** Input `values = [1, 2, 3, 4, 5, 6, 7, 8, 9]`, `k = 1`, output `[[1], [3, 2], [7, 6, 5, 4], [9, 8]]`.

**Hint.** Which depths are reversed, and does reversing a wave change which people are queued for the next one?

**Changed decision.** The reversal is decided by `depth % k == k - 1` for each wave, and it affects only where a person lands in its own list.

#### [Boundary] Both Side Views And Hidden Count (LeetCode 199)
<!-- id: tc-both-views-hidden -->

**Prerequisites.** The Zigzag In Blocks Of K rung and the last-removal idea.

**Problem.** For a tree stored by levels, return `[leftView, rightView, hidden]`. The left view lists the first person of each wave and the right view lists the last person of each wave, both from the top down. The count `hidden` is the number of people who are neither first nor last in their wave, so a wave of one or two people hides nobody.

**Constraints.** 0 <= values.length <= 2000 and numbers are integers between -1000 and 1000.

**Example 1.** Input `values = [1, 2, 3, 4, 5, 6, 7]`, output `[[1, 2, 4], [1, 3, 7], 2]`.

**Example 2.** Input `values = [1, 2, 3, null, 5, null, 4]`, output `[[1, 2, 5], [1, 3, 4], 0]`.

**Hint.** For a wave of size s, which removal counters are the first and last, and how many people are left between them?

**Changed decision.** Both ends of each wave are recorded, and the hidden count is `size - 2` for waves larger than two, which uses only the snapshot and the removal counter.

#### [Recognize] N-ary Tree Level Order Traversal (LeetCode 429)
<!-- id: tc-nary-level-order -->

**Prerequisites.** The Both Side Views rung and the child collection.

**Problem.** A tree has nodes 0 to n-1 with node 0 as the root, and `children[i]` lists the children of node i in left-to-right order. Return the node numbers grouped by wave from the root down, each wave in the order given by the children lists, and an empty list is never returned because the root always exists.

**Constraints.** 1 <= children.length <= 10000 and the lists describe one tree rooted at node 0.

**Example 1.** Input `children = [[1, 2, 3], [4, 5], [], [6], [], [], []]`, output `[[0], [1, 2, 3], [4, 5, 6]]`.

**Example 2.** Input `children = [[1], [2], [3], []]`, output `[[0], [1], [2], [3]]`.

**Hint.** What replaces the two `if` lines that add a left and a right child?

**Changed decision.** The two child checks become a loop over the node's list of children, and every other line of the wave method stays as it was.
