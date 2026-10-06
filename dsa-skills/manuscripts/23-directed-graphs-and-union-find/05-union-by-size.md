<!-- lesson-kind: standard -->
<!-- lesson-id: union-by-size -->
## Union By Size

<!-- stage: context -->
### Merging Networks Without Slow Lookups

A monitoring service receives cable reports such as "machine 12 is now linked to machine 40". After every report, an operator may ask whether two machines sit in the same network. The service stores each network as a tree of parent links. It answers a question by walking from each machine up to the tree's representative. If the reports arrive in an unlucky order, the trees grow into long chains. A single question then walks thousands of links, and a feed of two hundred thousand reports stalls.

The data is a parent array in which every element stores the index of its parent, and a representative stores its own index. The task is to merge two trees so that later walks stay short.

This lesson asks which of the two representatives should stay on top when two trees merge.

<!-- stage: naive -->
### Linking Under The Second Argument

The simplest merge finds the representative of each element and always hangs the first tree under the second. It never looks at how big either tree is.

```java
static int find(int[] parent, int x) {
    while (parent[x] != x) x = parent[x];
    return x;
}

static void unionFixed(int[] parent, int a, int b) {
    int ra = find(parent, a);
    int rb = find(parent, b);
    if (ra != rb) parent[ra] = rb;
}
```

Start with eight separate elements 0 to 7. Call `unionFixed` for the pairs (0,1), (1,2), (2,3), (3,4), (4,5), (5,6) and (6,7), in that order.

```predict
How many parent steps does find(parent, 0) take after these seven calls, and would the answer change if each pair were written in the other order?

It takes 7 steps. Each call hangs the old big tree under a new single element, so the tree becomes the chain 0, 1, 2, up to 7, and element 0 sits at the bottom. With the pairs written in the other order, as (1,0), (2,1) and so on, each call hangs a single element under the big tree. Every element then sits one step below the representative, and find takes at most 1 step. The same connections give a long chain or a flat tree, and only the argument order decides.
```

<!-- stage: bottleneck -->
### Chains Make Every Lookup Slow

The method itself is correct, because after each call the two elements share one representative. The cost depends on the shape of the tree. A walk from the deepest element takes as many steps as that element has ancestors, and the chain above gives n - 1 ancestors. One `find` is then O(n), and m operations cost O(m * n) in the worst case. With n = 100,000 and m = 200,000, that is about twenty billion parent reads.

Path compression, from the previous lesson, shortens a chain after a walk has climbed it. The first walk still pays the full price, and an adversary can build a new chain whenever it wants. The merge itself must control the shape, because the input decides the argument order and the program does not.

A better merge keeps every find at O(log n) steps in the worst case, with no help from compression. It needs one more number for each tree, and it needs a rule that uses that number when the two trees meet.

<!-- stage: insight -->
### Attach The Smaller Tree Under The Larger

A tree gets deep only when a merge puts a large tree under a small one. If the program always puts the small tree under the large one, depth cannot grow quickly.

<!-- names: height, smaller root, larger root -->

#### What To Store

A **root** is the representative of a tree, the one element whose parent is itself. The program keeps an array `size`, and `size[r]` is the number of elements in the tree of the root `r`. The **height** of a tree is the largest number of parent steps from any element up to its root. Only the entries of roots are meaningful. Once an element stops being a root, its entry is never read again.

#### The Rule

After finding the two roots, the program compares the sizes of the two roots. The root with the smaller count is the **smaller root**, and the other one is the **larger root**. On a tie, either root may stay on top. The smaller root gets the larger root as its new parent, and the larger root adds the smaller count to its own entry. The comparison uses the two roots and never the two original elements, because an element deep inside a tree has a stale count.

#### Why Height Stays Small

Take any element x. Its depth rises by one only when the tree that contains x is the smaller one in a merge. The merged tree then has at least twice as many elements as the old tree of x. The size of a tree never exceeds n, so the size can double at most log2(n) times. Therefore every depth, and so the height, is at most log2(n). For n = 100,000 that bound is 16 parent steps.

#### The Invariant

For every root r, `size[r]` equals the number of elements in the tree of r, and the sizes of all roots add up to n. A merge keeps this true, because the new count is the sum of the two old counts and the other root stops being a root.

<!-- stage: variables -->
### What The Structure Keeps

The structure keeps two arrays and one counter, and each merge uses four short-lived locals. All arrays have one entry for each element 0 to n - 1.

- **parent** is an int array; `parent[x] == x` marks x as a root.
- **size** is an int array; `size[r]` counts the elements of the tree rooted at r, and it starts at 1 everywhere.
- **components** is an int that starts at n and drops by one for each merge of two different trees.
- **big** and **small** hold the roots that `find` returns for `a` and `b`; a swap makes `big` the root of the larger tree, and `small` becomes a child of `big`.

<!-- stage: trace -->
### Two Merge Sequences Traced

#### Growing One Tree From Six Elements

The first run has six elements and the calls (0,1), (2,1), (3,4) and (4,2). The cells are the element indices. The pointers `big` and `small` mark the roots chosen by the comparison, and the variables show both arrays after the call. The last call is the important one. The elements 4 and 2 both still hold a stale size of 1, yet their roots 3 and 0 hold sizes 2 and 3. The comparison of roots puts the tree of 3 under 0.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["big","small"],"steps":[{"at":{"big":0,"small":1},"vars":{"call":"0,1","parent":"0 0 2 3 4 5","size":"2 1 1 1 1 1","components":5},"note":"The call (0,1) joins the roots 0 and 1. The root 1 becomes a child of 0, and size[0] becomes 2."},{"at":{"big":0,"small":2},"vars":{"call":"2,1","parent":"0 0 0 3 4 5","size":"3 1 1 1 1 1","components":4},"note":"The call (2,1) joins the roots 0 and 2. The root 2 becomes a child of 0, and size[0] becomes 3."},{"at":{"big":3,"small":4},"vars":{"call":"3,4","parent":"0 0 0 3 3 5","size":"3 1 1 2 1 1","components":3},"note":"The call (3,4) joins the roots 3 and 4. The root 4 becomes a child of 3, and size[3] becomes 2."},{"at":{"big":0,"small":3},"vars":{"call":"4,2","parent":"0 0 0 0 3 5","size":"5 1 1 2 1 1","components":2},"note":"The call (4,2) joins the roots 0 and 3. The root 3 becomes a child of 0, and size[0] becomes 5."}]}
```

#### Merges That Change Nothing

The second run has five elements and the calls (0,1), (1,0), (2,2), (2,3) and (3,1). The second call finds one root for both arguments, and the third call has the same element twice. Both calls leave `size` and `components` untouched. The last call joins two trees of equal size, and the tie keeps the root of the first argument on top.

```trace
{"cells":[0,1,2,3,4],"pointers":["big","small"],"steps":[{"at":{"big":0,"small":1},"vars":{"call":"0,1","parent":"0 0 2 3 4","size":"2 1 1 1 1","components":4},"note":"The call (0,1) joins the roots 0 and 1. The root 1 becomes a child of 0, and size[0] becomes 2."},{"at":{"big":0,"small":0},"vars":{"call":"1,0","parent":"0 0 2 3 4","size":"2 1 1 1 1","components":4},"note":"The call (1,0) finds the single root 0 for both arguments, so it changes nothing."},{"at":{"big":2,"small":2},"vars":{"call":"2,2","parent":"0 0 2 3 4","size":"2 1 1 1 1","components":4},"note":"The call (2,2) finds the single root 2 for both arguments, so it changes nothing."},{"at":{"big":2,"small":3},"vars":{"call":"2,3","parent":"0 0 2 2 4","size":"2 1 2 1 1","components":3},"note":"The call (2,3) joins the roots 2 and 3. The root 3 becomes a child of 2, and size[2] becomes 2."},{"at":{"big":2,"small":0},"vars":{"call":"3,1","parent":"2 0 2 2 4","size":"2 1 4 1 1","components":2},"note":"The call (3,1) joins the roots 2 and 0. The root 0 becomes a child of 2, and size[2] becomes 4."}]}
```

<!-- stage: code -->
### Union By Size In Java

The class below stores the two arrays and the counter. The method `union` returns true only when it joins two different trees.

```java
final class SizedSets {
    private final int[] parent;
    private final int[] size;
    private int components;

    SizedSets(int n) {
        parent = new int[n];
        size = new int[n];
        components = n;
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }

    int find(int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    boolean union(int a, int b) {
        int big = find(a);
        int small = find(b);
        if (big == small) return false;
        if (size[big] < size[small]) { int t = big; big = small; small = t; }
        parent[small] = big;
        size[big] += size[small];
        components--;
        return true;
    }

    int components() { return components; }
}
```

The two writes `parent[small] = big` and `size[big] += size[small]` must happen together. If the program skips the second write, the next comparison reads a wrong count and the height bound breaks. Each `find` takes at most log2(n) steps because the height bound holds, so a call to `union` costs O(log n) in the worst case. Adding path compression lowers the average further, as lesson 7 explains. The two arrays take O(n) space.

<!-- stage: applicability -->
### Recognizing Merges That Need Balance

#### Reading The Cue

Use union by size when many merge calls arrive in an order that the program does not control. Typical statements describe links, friendships or shared identifiers that arrive one at a time. The structure also fits tasks that report the size of the largest group, because `size[big]` already holds it.

#### Checking The Invariant

The invariant is that `size[r]` is correct for every root r. It holds only if the comparison happens between roots and the update happens at the surviving root. A merge that returns early for equal roots must change neither array. If it added the size again, the counts would exceed the number of elements, and the component count would drift.

#### Avoiding The False Friend

The false friend is a comparison of `size[a]` with `size[b]` for the original elements. It compiles, it often gives the right answer on small inputs, and it fails when an element is not a root. In the first trace, the elements 4 and 2 both read 1 while their trees hold 2 and 3 elements. Ask each time whether the two values compared are the sizes of roots.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Two Roots (Author exercise)
<!-- id: dg-merge-two-roots -->

**Prerequisites.** The `find` walk and the size rule of this lesson.

**Problem.** Elements are numbered `0` to `n - 1`, and each element starts as its own tree with `parent[i] = i`. Process the operations `ops` in order. For `ops[k] = [a, b]`, let `ra` and `rb` be the roots of `a` and `b`. If `ra == rb`, do nothing. Otherwise the root with the strictly smaller tree size becomes a child of the other root. When the sizes are equal, `rb` becomes a child of `ra`. Do not shorten any path. Return the final `parent` array.

**Constraints.** The limits are:
- **Elements** satisfy `1 <= n <= 1000`.
- **Operations** satisfy `0 <= ops.length <= 2000`, and every value is in `0..n-1`.
- **Size** of a tree is its number of elements.
- **Result** is an `int[]` of length `n`.

**Example 1.** Input `n = 6`, `ops = [[0,1],[2,1],[3,4],[4,2]]`, output `[0,0,0,0,3,5]`.

**Example 2.** Input `n = 4`, `ops = [[0,1],[2,3],[1,3]]`, output `[0,0,0,2]`.

**Hint.** Which two elements must the comparison read before any entry of `parent` changes?

**Changed decision.** The method finds both roots first and compares the sizes of the roots, and it writes one parent link and one size update.

#### [Vary] Repeated Unequal Merges (Author exercise)
<!-- id: dg-repeated-unequal -->

**Prerequisites.** The first exercise above.

**Problem.** Elements are numbered `0` to `n - 1`, and each pair in `ops` declares that its two elements are in the same group. Two elements are in one group when a chain of declared pairs joins them. Process all pairs with union by size. Return an `int[]` named `groupSize` of length `n`, where `groupSize[i]` is the number of elements in the group of element `i` after all pairs.

**Constraints.** The limits are:
- **Elements** satisfy `1 <= n <= 1000`.
- **Pairs** satisfy `0 <= ops.length <= 2000`, and every value is in `0..n-1`.
- **Order** of the pairs may produce merges of very unequal groups.
- **Result** reads the count of the root of each element.

**Example 1.** Input `n = 7`, `ops = [[0,1],[0,2],[0,3],[4,5],[6,0]]`, output `[5,5,5,5,2,2,5]`.

**Example 2.** Input `n = 6`, `ops = [[5,4],[4,3],[3,2],[2,1]]`, output `[1,5,5,5,5,5]`.

**Hint.** Which entry of `size` receives the added count when a single element joins a large group?

**Changed decision.** The method adds the count of the smaller root to the larger root only, and it answers each element by reading `size[find(i)]`.

#### [Boundary] Already Connected (Author exercise)
<!-- id: dg-already-connected -->

**Prerequisites.** The two exercises above.

**Problem.** Elements have the numbers `0` to `n - 1`. The list `ops` holds pairs `[a, b]`. A pair may repeat, may appear in reverse order, may close a cycle, and may have `a == b`. Merge the groups of `a` and `b` for each pair. Return an `int[]` of length 2 that holds the number of groups and the size of the largest group after all pairs.

**Constraints.** The limits are:
- **Elements** satisfy `1 <= n <= 1000`.
- **Pairs** satisfy `0 <= ops.length <= 2000`, and every value is in `0..n-1`.
- **Equal values** `a == b` are allowed and change nothing.
- **Result** is `[groups, largest]`, and `largest >= 1`.

**Example 1.** Input `n = 4`, `ops = [[0,1],[1,0],[2,2],[1,2],[0,2]]`, output `[2,3]`.

**Example 2.** Input `n = 3`, `ops = [[0,1],[1,2],[2,0],[0,2]]`, output `[1,3]`.

**Hint.** What must a call change when both arguments already have the same root?

**Changed decision.** The method returns before touching `size` or the group count when the two roots are equal, so no element is counted twice.

#### [Recognize] Redundant Connection (LeetCode 684)
<!-- id: dg-redundant-connection -->

**Prerequisites.** All three exercises above.

**Problem.** A graph has vertices `1` to `n`. It started as a tree, and one extra edge was added, so `edges` holds `n` edges `[a, b]` with `a < b`. Return the edge that can be removed so that the rest is a tree. When several edges qualify, return the one that appears last in `edges`.

**Constraints.** The limits are:
- **Vertices** satisfy `3 <= n <= 1000`.
- **Edges** number exactly `n`, and no edge repeats.
- **Graph** is connected before any removal.
- **Result** is one edge of the input, as an `int[]` of length 2.

**Example 1.** Input `edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]`, output `[1,4]`.

**Example 2.** Input `edges = [[2,3],[1,2],[1,3],[3,4]]`, output `[1,3]`.

**Hint.** When the edges are read in order, which edge is the first whose endpoints already share a root?

**Changed decision.** The method scans the edges once, merges the roots of each edge, and returns the first edge whose two roots are already equal.
