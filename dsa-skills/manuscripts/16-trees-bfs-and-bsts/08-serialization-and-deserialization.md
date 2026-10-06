<!-- lesson-kind: standard -->
<!-- lesson-id: serialization-and-deserialization -->
## Turn A Tree Into Text And Back

<!-- stage: context -->
### Why The Saved Tree Reloads Wrong

A game saves a decision tree to disk so that a player can quit and return. The first version writes the values of the nodes in one line, in the order a walk visits them. A player saves a tree where the node 1 has a left child 2. After reloading, the game shows a tree where the node 2 is the right child of the node 1. The saved text for those two trees is the same line, `1 2`, so the loader cannot tell which tree the player had.

Memory holds a tree as linked nodes, and a file holds only a sequence of characters. This lesson asks what the sequence must contain so that exactly one tree can be rebuilt from it, and how the writer and the reader stay in step.

<!-- stage: naive -->
### Writing Only The Values

The direct plan writes the value of each node in a walk order and separates the values with commas. The loader reads the values back and inserts them one at a time into a search tree.

```java
final class SaveValuesOnly {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void write(TreeNode node, StringBuilder out) {
        if (node == null) return;                       // a missing child writes nothing
        out.append(node.val).append(',');               // the value of this node
        write(node.left, out);
        write(node.right, out);
    }

    static String save(TreeNode root) {
        StringBuilder out = new StringBuilder();
        write(root, out);
        return out.toString();                          // for example "7,3,5,9,"
    }
}
```

For the tree with the root 7, the children 3 and 9, and a right child 5 of the node 3, the text is `7,3,5,9,`. A loader that inserts the values into a search tree rebuilds the same tree for this input.

<!-- stage: bottleneck -->
### Finding Two Trees With One Text

```predict
Take the tree where the node 1 has only a left child 2, and the tree where the node 1 has only a right child 2. What text does the values-only method write for each, and how many different trees can one text stand for?

Both trees produce the text `1,2,`. A text of n values can stand for many different trees, because the same sequence fits several shapes, and the loader has no way to choose.
```

The text loses the positions of the missing children, and a missing child is part of the shape. A repair that records the missing positions fixes the problem. In a tree with n nodes, the nodes have 2n child slots, and n - 1 of them hold a node, so n + 1 slots are empty. Writing one extra symbol for each empty slot makes the text 2n + 1 symbols long, which is O(n). The extra symbols cost little, and they remove the ambiguity.

<!-- stage: insight -->
### Write Every Empty Slot Too

A **null marker** is a fixed symbol, written in place of a missing child. The method writes the tree in preorder, which visits the node, then its left subtree, then its right subtree. A node writes its value. A missing child writes the null marker. The text `1,2,#,#,#` stands for the node 1 with a left child 2, because after the value 2 the next two symbols close the left and right slots of the node 2, and the last symbol closes the right slot of the node 1.

#### Reading With The Same Grammar

A **token** is one piece of text between two commas, such as `12`, `-7` or `#`. The reader follows the same rule as the writer. It reads the next token. A null marker ends the subtree and returns an empty slot. A number creates a node, and then the reader builds the left subtree and then the right subtree by reading further tokens in the same way. Because the writer emitted tokens in exactly this order, every call finds the tokens of its own subtree next in line.

#### Sharing One Position

All calls read from the same list of tokens, and each call must start where the previous one stopped. The reader keeps one **shared index** that moves forward by exactly one for every token it consumes. A call never rewinds the index. After the root call returns, the index equals the number of tokens, which confirms that the text held exactly one tree.

The rule for the symbols also decides the format. The comma separates tokens, so a value with several digits or a minus sign stays one token. The null marker `#` can never be mistaken for a number.

<!-- names: null marker, token, shared index -->

<!-- stage: variables -->
### The State Of Writer And Reader

- **out** is the text the writer builds, with one token for each node and each empty slot.
- **tokens** is the array that the reader gets by splitting the text at the commas.
- **index** is the shared position of the next unread token, and it starts at 0.
- **node** is the node a number token creates, and its two child calls read the tokens that follow.

<!-- stage: trace -->
### Writing Nine Tokens And Reading Them Back

Each cell is one token of the text. The pointer `at` marks the token being written or read.

#### Writing The Tree In Preorder

The tree has the root 7 and the children 3 and 9, and the node 3 has a right child 5. The text has nine tokens: `7,3,#,5,#,#,9,#,#`.

```trace
{"cells":["7","3","#","5","#","#","9","#","#"],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"slot":"root"},"note":"The writer emits the value 7 for the root."},{"at":{"at":1},"vars":{"slot":"left slot of 7"},"note":"The writer emits the value 3 for the left slot of 7."},{"at":{"at":2},"vars":{"slot":"left slot of 3"},"note":"The left slot of 3 is empty, so the writer emits the null marker."},{"at":{"at":3},"vars":{"slot":"right slot of 3"},"note":"The writer emits the value 5 for the right slot of 3."},{"at":{"at":4},"vars":{"slot":"left slot of 5"},"note":"The left slot of 5 is empty, so the writer emits the null marker."},{"at":{"at":5},"vars":{"slot":"right slot of 5"},"note":"The right slot of 5 is empty, so the writer emits the null marker."},{"at":{"at":6},"vars":{"slot":"right slot of 7"},"note":"The writer emits the value 9 for the right slot of 7."},{"at":{"at":7},"vars":{"slot":"left slot of 9"},"note":"The left slot of 9 is empty, so the writer emits the null marker."},{"at":{"at":8},"vars":{"slot":"right slot of 9"},"note":"The right slot of 9 is empty, so the writer emits the null marker."}]}
```

The writer produced four value tokens and five null markers. That is 2n + 1 = 9 tokens for n = 4 nodes.

#### Reading The Tokens Back

The reader gets the same nine tokens. The variable `depth` is the number of calls that are waiting for a child to finish.

```trace
{"cells":["7","3","#","5","#","#","9","#","#"],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"depth":1},"note":"Token 0 is 7, so the reader creates a node for the root and reads its left subtree next."},{"at":{"at":1},"vars":{"depth":2},"note":"Token 1 is 3, so the reader creates a node for the left slot of 7 and reads its left subtree next."},{"at":{"at":2},"vars":{"depth":3},"note":"Token 2 is the null marker, so the left slot of 3 stays empty."},{"at":{"at":3},"vars":{"depth":3},"note":"Token 3 is 5, so the reader creates a node for the right slot of 3 and reads its left subtree next."},{"at":{"at":4},"vars":{"depth":4},"note":"Token 4 is the null marker, so the left slot of 5 stays empty."},{"at":{"at":5},"vars":{"depth":4},"note":"Token 5 is the null marker, so the right slot of 5 stays empty."},{"at":{"at":6},"vars":{"depth":2},"note":"Token 6 is 9, so the reader creates a node for the right slot of 7 and reads its left subtree next."},{"at":{"at":7},"vars":{"depth":3},"note":"Token 7 is the null marker, so the left slot of 9 stays empty."},{"at":{"at":8},"vars":{"depth":3},"note":"Token 8 is the null marker, so the right slot of 9 stays empty."}]}
```

The index reaches 9 at the end, which equals the token count. The reader built four nodes and filled five empty slots.

<!-- stage: code -->
### The Codec In Code

```java
final class TreeCodec {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static String serialize(TreeNode root) {
        StringBuilder out = new StringBuilder();
        write(root, out);
        return out.toString();
    }

    private static void write(TreeNode node, StringBuilder out) {
        if (out.length() > 0) out.append(',');          // a comma goes between tokens only
        if (node == null) { out.append('#'); return; }  // the null marker keeps the shape
        out.append(node.val);
        write(node.left, out);                          // left subtree first, as the reader expects
        write(node.right, out);
    }

    static TreeNode deserialize(String text) {
        String[] tokens = text.split(",");
        int[] index = {0};                              // one shared position for every call
        return read(tokens, index);
    }

    private static TreeNode read(String[] tokens, int[] index) {
        String token = tokens[index[0]++];              // consume exactly one token per call
        if (token.equals("#")) return null;             // an empty slot ends this subtree
        TreeNode node = new TreeNode(Integer.parseInt(token));
        node.left = read(tokens, index);                // the left subtree's tokens come next
        node.right = read(tokens, index);               // the right subtree's tokens follow
        return node;
    }
}
```

The reader uses a moving index. Removing the first element of a list for each token would shift every remaining element each time.

- **Time** is O(n) for both directions, because each node and each empty slot is handled once.
- **Space** is O(h) for the recursion stack, plus O(n) for the text and the tokens.

<!-- stage: applicability -->
### Using A Matched Pair Of Methods

#### Recognizing The Cue

Use a matched writer and reader when a tree must be stored, sent over a network, or compared as text. The words "serialize", "encode", "save the structure" and "rebuild exactly" point here. The format is fixed by the pair of methods, and the problem usually allows any format that round-trips.

#### Stating The Invariant

The invariant is that the writer and the reader follow the same traversal grammar, so a reader call finds its own subtree's tokens next. Each null marker keeps one empty slot visible. After the root call, the reader has consumed every token.

#### Avoiding The False Friend

The false friend is a text of values alone, as the ambiguity above shows. A search tree can be rebuilt from its preorder values by insertion, but a general binary tree cannot. A second trap is the delimiter. Values may be negative or have several digits, and a text without a separator turns `1`, `2` and `12` into the same characters. Pick a separator and a null marker that cannot appear inside a number.

<!-- stage: exercises -->
### Exercises

#### [Build] Preorder With Null Markers (Author exercise)
<!-- id: tb-codec-preorder -->

**Prerequisites.** The null marker and the preorder rule from this lesson.

**Problem.** Return the text form of a binary tree. The text lists the tokens of a preorder walk separated by commas. A node writes its value, and a missing child writes `#`. A null root gives the text `#`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 1000.
- **Values** satisfy `0 <= val <= 9`, so each value is one digit.
- **Answer** is a string with `2n + 1` tokens for `n` nodes.
- **Mutation** does not occur.

**Example 1.** Input root 1 with children 2 and 3, where 3 has children 4 and 5, output `1,2,#,#,3,4,#,#,5,#,#`.

**Example 2.** Input a null root, output `#`.

**Hint.** What does a call write for a null node? In which order do the left and right calls run?

**Changed decision.** Missing children write a marker, and the order is preorder.

#### [Vary] Recursive Decoder (Author exercise)
<!-- id: tb-codec-decoder -->

**Prerequisites.** The exercise above.

**Problem.** Given the text form of a binary tree as in the exercise above, rebuild the tree with a recursive reader that consumes one token per call, and return the values of the rebuilt tree in level order from left to right, with no markers. The shared index must move forward exactly once per token.

**Constraints.** The limits are:
- **Text** is a valid form of a tree with 0 to 1000 nodes, and each value is one digit.
- **Index** advances by one for each token and never moves back.
- **Answer** is a list of the values, and the empty tree gives an empty list.
- **Mutation** does not occur.

**Example 1.** Input `1,2,#,#,3,4,#,#,5,#,#`, output `[1, 2, 3, 4, 5]`.

**Example 2.** Input the text `#`, output the empty list `[]`.

**Hint.** What does the reader return for the token `#`? Which call reads the tokens of the right subtree?

**Changed decision.** A reader replaces the writer, and a shared index replaces the recursion over nodes.

#### [Boundary] Empty, Negative, And Multi-Digit Values (Author exercise)
<!-- id: tb-codec-edges -->

**Prerequisites.** The two exercises above.

**Problem.** Given the root of a binary tree whose values may be negative or have several digits, return its text form with comma separators and the marker `#`. The text must give back exactly the same tree when it is read by the decoder. The empty tree gives `#`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `-1000 <= val <= 1000`.
- **Answer** is a string that contains no space and no character other than digits, minus signs, commas and `#`.
- **Mutation** does not occur.

**Example 1.** Input root -12 with a left child 305 and no right child, output `-12,305,#,#,#`.

**Example 2.** Input a null root, output `#`.

**Hint.** What separates `-12` from the next token? Why can `#` never be confused with a number?

**Changed decision.** The format must keep multi-character numbers whole, and the empty tree must stay valid.

#### [Recognize] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: tb-codec-297 -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class `Codec` with a method `serialize` that turns a binary tree into a string, and a method `deserialize` that turns that string back into a tree with the same shape and values. Any format is accepted if the two methods match. The input of `deserialize` is always an output of `serialize`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `-1000 <= val <= 1000`, and values may repeat.
- **Answer** of a round trip is a tree equal to the input in shape and values.
- **Mutation** does not occur to the input tree.

**Example 1.** Input root 1 with children 2 and 3, where 3 has children 4 and 5, output a rebuilt tree with the same nodes in the same positions.

**Example 2.** Input a null root, output a null root.

**Hint.** Which symbols mark an empty slot and a boundary between values? How does the reader know where one subtree stops?

**Changed decision.** The writer and the reader are separate methods that must agree on one grammar.
