<!-- lesson-kind: standard -->
<!-- lesson-id: binary-tries -->
## Binary Tries

<!-- stage: context -->
### The Lamp Keeper Of Harbour Tower

The lamp keeper of Harbour Tower looks after a wall of identical lamps, each with a row of switches that are either up or down. A reading from one lamp is the pattern of its switches, written as a binary number with the leftmost switch as the biggest digit. Each night the keeper must pick two lamps whose patterns clash the most, where the clash score of two lamps is the number that has a one in every switch position at which the two patterns disagree, and a zero where they agree.

A clash on the leftmost switch is worth more than clashes on every other switch together, since one top digit outweighs all the digits below it. The keeper has hundreds of thousands of lamps and cannot afford to compare each lamp with every other, so she is looking for a way to find, for a given lamp, the lamp that clashes with it best.

<!-- stage: naive -->
### Score Every Pair Of Lamps

The direct method scores every pair of lamps by computing the clash number of the two patterns, and remembers the largest score seen.

```java
static int bestClash(int[] lamps) {
    int best = 0;
    for (int i = 0; i < lamps.length; i++) {
        for (int j = i + 1; j < lamps.length; j++) {
            best = Math.max(best, lamps[i] ^ lamps[j]);
        }
    }
    return best;
}
```

The method is easy to trust, since it looks at every pair and so cannot miss the best one. A single lamp gives the score 0 because there is no other lamp to clash with.

<!-- stage: bottleneck -->
### Pairs Grow Quadratically

With n lamps there are n * (n - 1) / 2 pairs, so the method costs O(n^2). Two hundred thousand lamps give twenty billion pair scores, which is far beyond what a second allows. Each score is a single instruction, so the trouble is only the number of pairs.

Yet most pairs are obviously poor. If a lamp has its top switch up, then any partner with that switch down already has a clash score above every score that a partner with the switch up can reach, whatever the lower switches say. The lamp does not need to look at those other partners at all. The question for a given lamp can be answered one switch at a time, from the top, by keeping only the lamps that are still candidates. A structure that groups lamps by their top switches could do this in a number of steps equal to the number of switches, instead of the number of lamps.

<!-- stage: insight -->
### Prefer The Other Side At Every Bit

Store each number as a path in a trie whose edges are bits, from the most significant bit to the least. Every number is written with the same **bit width**, which is a fixed count such as 31 for nonnegative ints, so all paths have the same length and every number ends at its own leaf. The edges are 0 and 1, and a node has at most two children.

To find the best partner for a number x, perform a **greedy descent** from the root. At each bit, look at the bit of x and ask whether the **opposite branch** exists, the child that holds the other bit value. If it does, take it, because a one in this position of the result is worth more than anything the lower bits can add. If it does not, take the only branch present and accept a zero here. The score is built bit by bit as the path is walked, and after the last bit it equals the best result achievable with any stored number.

The edges of this trie do not mean letters of a word. They are the digits of a number, and the search moves toward the side that is unlike the query, not toward the side that agrees with it.

The invariant is that after each bit, the node reached holds only numbers that give the best possible result in the bits seen so far, and a better prefix in a higher bit always beats every choice in the lower bits.

<!-- names: bit width, greedy descent, opposite branch -->

<!-- stage: variables -->
### Bit, Node And Partial Result

The variable `b` runs from the top bit down to 0, and the bit of x at that position is `(x >>> b) & 1`. A node `cur` holds up to two children in `kid[0]` and `kid[1]`. For a query, `want` is `1 - bit`, the opposite branch, and `score` is the partial result, which gains `1 << b` whenever the opposite branch is taken. The constant `TOP` is the highest bit position, one less than the bit width. For nonnegative ints below 2^31 it is 30, and a different contract needs a different value.

<!-- stage: trace -->
### Insertion And Greedy Descent

The first trace inserts 9, written in five bits as `01001`, into a trie that already holds 6 (`00110`) and 12 (`01100`). The pointer `b` moves over the bit positions of the number from the left. The first two bits follow edges that 12 created, so no nodes are added there, and the remaining three bits create new nodes. The count `nodes` includes the root.

```trace
{"cells":["0","1","0","0","1"],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"nodes":10,"made":"no"},"note":"The bit 0 already has an edge, so the walk moves onto the existing node for 0."},{"at":{"b":1},"vars":{"nodes":10,"made":"no"},"note":"The bit 1 already has an edge, so the walk moves onto the existing node for 01."},{"at":{"b":2},"vars":{"nodes":11,"made":"yes"},"note":"The bit 0 has no edge below the node for 01, so a new node is created for 010."},{"at":{"b":3},"vars":{"nodes":12,"made":"yes"},"note":"The bit 0 has no edge below the node for 010, so a new node is created for 0100."},{"at":{"b":4},"vars":{"nodes":13,"made":"yes"},"note":"The bit 1 has no edge below the node for 0100, so a new node is created for 01001."},{"at":{"b":5},"vars":{"nodes":13,"made":"no"},"note":"All 5 bits are placed, so this value ends at its own leaf and the trie holds 13 nodes with the root."}]}
```

The second trace looks for the best partner of 9 among 6, 12, 30 and 17. At each bit, the note names the bit wanted, which is the opposite of the query bit, and whether that branch exists. The partial `score` grows only when the wanted branch is found. The final score is the best clash of 9 with any stored number, and the partner can be read off the path taken.

```trace
{"cells":["0","1","0","0","1"],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"want":1,"score":16},"note":"The query bit is 0, so the wanted bit is 1. That branch exists, so it is taken and the result gains 16."},{"at":{"b":1},"vars":{"want":0,"score":24},"note":"The query bit is 1, so the wanted bit is 0. That branch exists, so it is taken and the result gains 8."},{"at":{"b":2},"vars":{"want":1,"score":24},"note":"The query bit is 0, so the wanted bit is 1. That branch is missing, so the walk takes 0 and the result gains nothing here."},{"at":{"b":3},"vars":{"want":1,"score":24},"note":"The query bit is 0, so the wanted bit is 1. That branch is missing, so the walk takes 0 and the result gains nothing here."},{"at":{"b":4},"vars":{"want":0,"score":24},"note":"The query bit is 1, so the wanted bit is 0. That branch is missing, so the walk takes 1 and the result gains nothing here."}]}
```

<!-- stage: code -->
### Binary Trie For Maximum Xor

```java
final class BitTrie {
    private static final int TOP = 30;

    private static final class Node {
        final Node[] kid = new Node[2];
    }

    private final Node root = new Node();
    private int stored;

    void insert(int value) {
        Node cur = root;
        for (int b = TOP; b >= 0; b--) {
            int bit = (value >>> b) & 1;
            if (cur.kid[bit] == null) cur.kid[bit] = new Node();
            cur = cur.kid[bit];
        }
        stored++;
    }

    int bestWith(int x) {
        Node cur = root;
        int score = 0;
        for (int b = TOP; b >= 0; b--) {
            int want = 1 - ((x >>> b) & 1);
            if (cur.kid[want] != null) {
                score |= 1 << b;
                cur = cur.kid[want];
            } else {
                cur = cur.kid[1 - want];
            }
        }
        return score;
    }

    int stored() {
        return stored;
    }
}
```

Both operations take 31 steps, so insertion and a query cost O(B) for the bit width B, which is a constant for ints. The whole array is handled in O(n * B) time and O(n * B) space, and a query on a trie with no stored number must not be made, since there is no child to follow.

<!-- stage: applicability -->
### Maximising An Exclusive Or

Use this trie when the goal is to maximise the exclusive or of two numbers from a set, or of a query with a stored number: maximum xor pairs, maximum xor of a subarray through prefix values, and choosing a key to flip the most bits. The invariant is that a higher bit settled in favour of the result is never undone by lower bits, so the choice at each bit is final.

The false friend is the character trie. The two share their shape, yet the characters of a word are matched, and the search follows the branch that agrees with the query, while here the search follows the branch that disagrees. Treating the binary trie like a word dictionary leads to a search for the closest number, which is the opposite goal and gives the minimum xor, not the maximum. The same trie answers the minimum too, if the greedy choice is turned around.

The argument needs an objective that depends on the highest bit first. For a sum or a product of two numbers a higher bit does not dominate in the same way, and the trie gives no shortcut. In Java, an `int` has 32 bits and the top one is the sign. With nonnegative inputs below 2^31, start at bit 30. If negative numbers are allowed, decide whether the result is read as signed or unsigned, and start at bit 31 for the unsigned reading. Shift with `>>>` so that the sign does not smear into the lower bits.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Fixed-Width Bits (Author exercise)
<!-- id: tn-insert-fixed-bits -->

**Prerequisites.** The prefix node lesson, with edges now being bits.

**Problem.** Given a bit width `w` and a list of integers that are each at least 0 and below 2^w, write every integer with exactly `w` bits, most significant first, and insert it into an empty binary trie. Return `[nodes, leaves]`, where `nodes` counts all nodes other than the root and `leaves` counts the nodes at depth `w`.

**Constraints.** 1 <= w <= 20, 0 <= values.length <= 1000, and each value is below 2^w.

**Example 1.** Input `w = 3`, `values = [1, 2, 3, 5]`, output `[9, 4]`.

**Example 2.** Input `w = 4`, `values = [8, 8, 0]`, output `[8, 2]`.

**Hint.** Which bits of a new value follow edges that already exist, and what does a repeated value add?

**Changed decision.** The depth of every path is the fixed width, so leading zeros are real edges and no value stops early.

#### [Vary] Best XOR Partner (Author exercise)
<!-- id: tn-best-xor-partner -->

**Prerequisites.** The Insert Fixed-Width Bits rung.

**Problem.** A nonempty list of stored nonnegative integers is given, followed by a list of queries. For each query `x`, return the largest value of `x ^ y` over all stored `y`. Use 31 bits, from bit 30 down to bit 0.

**Constraints.** 1 <= stored.length <= 5000, 0 <= queries.length <= 5000, and every number is between 0 and 2^31 - 1.

**Example 1.** Input `stored = [6, 12, 9, 30, 17]`, `queries = [9, 17, 0]`, output `[24, 29, 30]`.

**Example 2.** Input `stored = [1]`, `queries = [1, 0]`, output `[0, 1]`.

**Hint.** At each bit, which child would make the result bit a one, and what do you do when it is missing?

**Changed decision.** Instead of following the query's own bit, the descent prefers the opposite bit and builds the result as it goes.

#### [Boundary] Equal Values And Sign Policy (Author exercise)
<!-- id: tn-equal-and-sign -->

**Prerequisites.** The Best XOR Partner rung and the choice of a bit width.

**Problem.** For a list of 32-bit signed integers, return the largest value of `(a ^ b)` read as an unsigned 32-bit number, over pairs of different positions in the list, as a `long`. Return -1 if the list has fewer than two entries. Equal values at different positions form a valid pair. Traverse bits 31 down to 0.

**Constraints.** 0 <= values.length <= 3000 and every value is a signed 32-bit integer.

**Example 1.** Input `values = [5, -5]`, output `4294967294`.

**Example 2.** Input `values = [7, 7, 7]`, output `0`.

**Hint.** Should a number be inserted before or after it is queried, and which bit holds the sign?

**Changed decision.** The width is 32 and the sign bit is an ordinary top bit, and a value is queried against earlier values only, so a number never pairs with itself.

#### [Recognize] Maximum XOR of Two Numbers in an Array (LeetCode 421)
<!-- id: tn-max-xor-pair -->

**Prerequisites.** The Equal Values And Sign Policy rung.

**Problem.** For an array of nonnegative integers, return the largest value of `nums[i] ^ nums[j]` over all pairs of indices, where `i` and `j` may be equal, so the answer is never negative.

**Constraints.** 1 <= nums.length <= 200000 and 0 <= nums[i] <= 2^31 - 1.

**Example 1.** Input `nums = [14, 11, 7, 2]`, output `12`.

**Example 2.** Input `nums = [4096, 4095]`, output `8191`.

**Hint.** What does the best partner of each number look like bit by bit, and which structure stores all numbers at once?

**Changed decision.** All numbers are stored first and each is then queried, which is safe because a pair with itself gives 0 and never beats a real pair.
