<!-- lesson-kind: standard -->
<!-- lesson-id: binary-tries -->
## Pick The Best XOR Partner

<!-- stage: context -->
### Why Comparing Every Pair Times Out

A tool receives 100,000 integer ids and must report the largest value of `a ^ b` over any two ids, where `^` is the bitwise exclusive or. The operation `a ^ b` writes a 1 in each bit position where `a` and `b` have different bits, and a 0 where they have the same bit. The first version tries every pair, and it needs about five billion operations, so the job times out.

The question looks like a numeric problem, and the answer follows from the binary digits of the ids. This lesson asks how a program picks the best partner for one id without testing the others.

<!-- stage: naive -->
### Trying Every Pair

The direct plan compares each element with every later element and keeps the largest XOR.

```java
static int maxXorByPairs(int[] a) {
    int best = 0;                                      // a single element gives a ^ a = 0
    for (int i = 0; i < a.length; i++) {
        for (int j = i + 1; j < a.length; j++) {       // every pair of positions once
            best = Math.max(best, a[i] ^ a[j]);        // XOR is symmetric, so one order suffices
        }
    }
    return best;
}
```

The method is correct for every array of nonnegative ints. It treats the numbers as opaque values, and it ignores that the leading binary digits decide which number is larger.

<!-- stage: bottleneck -->
### Counting The Pairs

```predict
The array has n = 100,000 ids. About how many pairs does the double loop test, and what does one test learn about the other pairs?

It tests about n * (n - 1) / 2, roughly 5 * 10^9 pairs. One test learns nothing about the other pairs, because the loop never uses the fact that a pair with a 1 in a high bit beats every pair with a 0 there.
```

The double loop costs O(n^2) time. The bottleneck is that the loop treats every pair as equally promising. Binary numbers do not behave that way. A result whose bit 30 is 1 is larger than every result whose bit 30 is 0, however large the lower bits are.

A search for the best partner of one value `x` can therefore decide the top bit first, then the next bit, and so on. Each decision needs to know only whether some stored number has a given bit pattern, and a prefix tree over bits answers that.

<!-- stage: insight -->
### Choosing The Bit That Differs

The **highest differing bit** decides the order of two XOR results. If result `A` has a 1 in a bit where result `B` has a 0, and all higher bits are equal, then `A` is larger than `B`. The program maximizes `x ^ y` by making the highest bit of the result 1 first, and then the next bit, and so on.

#### Storing Numbers As Bit Paths

The program stores each number as a **fixed-width path**. Every number uses the same number of bits, from the highest considered bit down to bit 0, and a number with fewer significant bits receives leading zeros. Each node has two children, one for bit 0 and one for bit 1. Two numbers share a node exactly when they share the leading bits.

#### Preferring The Opposite Edge

To find the best partner of `x`, the walk reads the bits of `x` from the highest. At each bit it prefers the **opposite branch**, the child whose bit differs from the bit of `x`, because that choice puts a 1 in the result. If the opposite child exists, the walk takes it and adds the bit value to the answer. If it does not exist, the walk takes the same child, and the result bit stays 0. The greedy choice is safe, because a higher bit always outweighs all lower bits together.

<!-- names: highest differing bit, fixed-width path, opposite branch -->

<!-- stage: variables -->
### The Pieces Of State

The structure and the walk need five pieces of state.

- **Width** is the number of bits that every stored number uses, and it is fixed before the first insert.
- **Child 0 and child 1** are the two links of a node, and either link may be null.
- **Current node** is the node reached after the bits above the current bit have been consumed.
- **Result** accumulates the XOR value, and bit `b` of it is set when the walk takes the opposite branch at bit `b`.
- **Partner prefix** is the bit pattern of the chosen stored number so far, which the walk follows implicitly.

The insert changes only the children. The walk changes the current node and the result at each bit.

<!-- stage: trace -->
### Following Bits Through The Tree

The traces use numbers of 5 bits, with bit 4 as the highest and bit 0 as the lowest.

#### Inserting A Number With A Shared Start

The first trace inserts 8, which is `01000`, into a tree that holds 10, which is `01010`. The pointer `i` marks the bit position in the cell list, so `i = 0` is bit 4. The variable `created` counts the nodes that the insert has created.

The first three bits, 0, 1 and 0, match the path of 10, so the insert reuses three nodes. The bit 0 at `i = 3` has no child, because 10 has a 1 there, so the insert creates a node. The last bit creates a second node. The new number shares three nodes with 10 and adds two.

#### Querying For The Largest XOR

The second trace queries `x = 5`, which is `00101`, in a tree that holds 3, 10, 5, 25, 2 and 8. At bit 4 the bit of `x` is 0, so the walk prefers a child 1. The stored number 25, which is `11001`, provides it, and the result gets 16. At bit 3 and bit 2 the opposite child also exists, and the result gets 8 and 4. At bit 1 and bit 0 the opposite child is missing, so the walk takes the same child. The result is `11100`, which is 28.

#### Stepping Through Both Walks

```trace
{"cells":[0,1,0,0,0],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"created":0},"note":"The bit 0 at position 4 already has a child, so the insert reuses it."},{"at":{"i":1},"vars":{"created":0},"note":"The bit 1 at position 3 already has a child, so the insert reuses it."},{"at":{"i":2},"vars":{"created":0},"note":"The bit 0 at position 2 already has a child, so the insert reuses it."},{"at":{"i":3},"vars":{"created":1},"note":"The bit 0 at position 1 has no child, so the insert creates one."},{"at":{"i":4},"vars":{"created":2},"note":"The bit 0 at position 0 has no child, so the insert creates one."}]}
```

```trace
{"cells":[0,0,1,0,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"result":16,"partner":"1"},"note":"The bit of x at position 4 is 0, and a child 1 exists, so the walk takes it. The result gains 16."},{"at":{"i":1},"vars":{"result":24,"partner":"11"},"note":"The bit of x at position 3 is 0, and a child 1 exists, so the walk takes it. The result gains 8."},{"at":{"i":2},"vars":{"result":28,"partner":"110"},"note":"The bit of x at position 2 is 1, and a child 0 exists, so the walk takes it. The result gains 4."},{"at":{"i":3},"vars":{"result":28,"partner":"1100"},"note":"The bit of x at position 1 is 0, and no child 1 exists, so the walk takes the child 0. The result gains 0."},{"at":{"i":4},"vars":{"result":28,"partner":"11001"},"note":"The bit of x at position 0 is 1, and no child 0 exists, so the walk takes the child 1. The result gains 0."}]}
```

<!-- stage: code -->
### Writing The Bit Walk In Java

#### The Tree And The Query

The class stores nonnegative `int` values with 31 bits, so bit 30 is the highest. The insert and the query both loop from bit 30 down to bit 0.

```java
final class BinaryTrie {
    private static final class Node {
        final Node[] next = new Node[2];               // next[0] follows bit 0, next[1] follows bit 1
    }

    private static final int TOP = 30;                 // values are nonnegative ints, so 31 bits suffice
    private final Node root = new Node();

    void insert(int value) {
        Node cur = root;
        for (int b = TOP; b >= 0; b--) {               // highest bit first, always 31 steps
            int bit = (value >> b) & 1;
            if (cur.next[bit] == null) cur.next[bit] = new Node();   // create only a missing edge
            cur = cur.next[bit];
        }
    }

    int bestXor(int x) {                               // requires at least one stored value
        Node cur = root;
        int result = 0;
        for (int b = TOP; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (cur.next[1 - bit] != null) {           // the opposite edge puts a 1 in the result
                result |= 1 << b;
                cur = cur.next[1 - bit];
            } else {
                cur = cur.next[bit];                   // only the same edge exists, so this result bit is 0
            }
        }
        return result;
    }
}
```

#### Cost Of The Tree

Each insert and each query costs O(31) steps, which is O(1) for fixed-width ints, or O(B) for `B` bits. A maximum over `n` numbers costs O(n * B) time. The tree holds at most `n * B` nodes, so it needs O(n * B) memory.

<!-- stage: applicability -->
### Recognizing An XOR Maximization

#### Spotting The Pattern

The cue is an objective that maximizes an XOR, where the highest differing bit dominates all lower bits. The invariant is that at each bit the walk prefers the opposite branch when it exists, so the chosen path is the best one in order of bits from the highest.

#### Finding The False Friend

The false friend is the character prefix tree from the earlier lessons. It has the same shape, and its edges have a different meaning. A character tree follows the edge that equals the next letter. A bit tree follows the opposite edge when it can, so equal paths are the worst case and not the best case.

Binary search on a sorted copy of the numbers is another false friend. Sorting orders numbers by value, and it does not order them by the XOR with a given `x`, so the nearest value is not the best partner.

#### Recognizing The No-Go Cases

The tree does not fit when the objective is a sum, a difference or a minimum XOR, because other rules decide those. It does not fit when inputs may be negative unless the program states how it treats the sign bit, since a width of 31 bits drops it. A short list of numbers also does not justify the tree, because the pair loop is simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Fixed-Width Bits (Author exercise)
<!-- id: tr-insert-fixed-width-bits -->

**Prerequisites.** The prefix tree of the previous lessons and the XOR definition above.

**Problem.** Given an array `values` of nonnegative integers and an integer `width`, insert each value into an empty binary tree as a path of exactly `width` bits, from bit `width - 1` down to bit 0. Return the number of nodes below the root.

**Constraints.** The limits are:
- **Count** is `0 <= values.length <= 10^4`.
- **Width** is `1 <= width <= 31`.
- **Values** satisfy `0 <= value < 2^width`.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [1,2,3]` and `width = 3`, output 6.

**Example 2.** Input `values = [5,5]` and `width = 3`, output 3.

**Hint.** How many bits does every value consume, even when the value is small? Which nodes does a repeated value reuse?

**Changed decision.** Every value is a path of the same length, and each level has two children, not many.

#### [Vary] Best XOR Partner (Author exercise)
<!-- id: tr-best-xor-partner -->

**Prerequisites.** The previous exercise.

**Problem.** Given a nonempty array `stored` and an array `queries` of nonnegative integers, produce an array whose entry at position `j` is the largest value of `queries[j] ^ s` over all entries `s` of `stored`.

**Constraints.** The limits are:
- **Count** is `1 <= stored.length <= 10^4` and `0 <= queries.length <= 10^4`.
- **Values** satisfy `0 <= value <= 2^31 - 1`.
- **Width** of the paths is 31 bits.
- **Mutation** does not occur; both arrays keep their contents.

**Example 1.** Input `stored = [3,10,5,25,2,8]` and `queries = [5,2]`, output `[28,27]`.

**Example 2.** Input `stored = [7]` and `queries = [0,7]`, output `[7,0]`.

**Hint.** Which child does the walk prefer at each bit? What does the walk do when the preferred child is missing?

**Changed decision.** The walk prefers the opposite child and builds the answer bit by bit.

#### [Boundary] Equal Values And Sign Policy (Author exercise)
<!-- id: tr-equal-values-sign-policy -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `values` of nonnegative integers, return the largest value of `values[i] ^ values[j]` over positions `i < j`. Return -1 when the array has fewer than two elements. Equal values at different positions form a valid pair.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** satisfy `0 <= value <= 2^31 - 1`, so no value is negative.
- **Width** of the paths is 31 bits.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [6,6,6]`, output 0.

**Example 2.** Input `values = [2147483647,0]`, output 2147483647.

**Hint.** When is it safe to query a value against the tree? Which bit of an `int` must stay unused?

**Changed decision.** The method queries each value before it inserts the value, so a position never pairs with itself.

#### [Recognize] Maximum XOR of Two Numbers in an Array (LeetCode 421)
<!-- id: tr-maximum-xor-pair -->

**Prerequisites.** The previous three exercises.

**Problem.** Given an array `nums` of nonnegative integers, return the maximum value of `nums[i] ^ nums[j]` over all positions `i` and `j` with `0 <= i <= j < nums.length`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 2 * 10^5`.
- **Values** satisfy `0 <= nums[i] <= 2^31 - 1`.
- **Pairs** may use the same position twice.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [3,10,5,25,2,8]`, output 28.

**Example 2.** Input `nums = [14,70,53,83,49,91,36,80,92,51,66,70]`, output 127.

**Hint.** Which value does each number look for among all the others? What decides the answer between two candidate partners?

**Changed decision.** The tree is built from every value first, and each value then queries the whole tree.
