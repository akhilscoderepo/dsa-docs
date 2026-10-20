<!-- lesson-kind: combination -->
<!-- lesson-id: codec-structural-traversal -->
## Codec Structural Traversal

<!-- stage: context -->
### Why Two Trees Share One Cache Entry

A menu service caches a small binary tree of options as one line of text. The writer visits the tree in preorder and joins the values of the real nodes with commas. A tree with root 1 and only a left child 2 is stored as `1,2`. A second tree with root 1 and only a right child 2 is also stored as `1,2`. The reader attaches every value to the left side, so half of the menus come back with their options on the wrong side.

Both programs pass their own tests, and the reader never fails with an error. It returns a wrong tree without any warning. This lesson asks how to write the encoder and the decoder from one description of the text. Each tree must have one text, and a damaged text must raise an error and never produce a different tree.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Structural Codecs supplied the pieces of a single encoding. A length written before a string fixes the end of that string. A marker written for each missing child fixes the shape of a binary tree. One shared index into the tokens makes each decoding step consume one complete unit, and a leftover token proves a malformed text. The earlier chapters on trees and queues supplied the traversal orders: preorder with recursion, and level order with a queue of nodes.

This lesson joins the two skills. The new work is a rule for the pair of programs. The encoder and the decoder must be two walks over one traversal order, so that every place the encoder writes a token is a place the decoder reads one. The same rule covers a flat list of strings, a tree walked by levels, a forest, and a search tree whose order replaces the markers.

<!-- stage: naive -->
### Write The Values And Guess The Shape

The direct design writes the values of the real nodes in preorder and lets the reader attach the values greedily. The class below writes the line and reads it back with a deque of the remaining values.

```java
final class NaiveTreeText {
    record TreeNode(int val, TreeNode left, TreeNode right) {}

    // Writes the values of the real nodes in preorder, joined by commas.
    static void write(TreeNode n, StringBuilder sb) {
        if (n == null) return;
        if (sb.length() > 0) sb.append(',');
        sb.append(n.val());
        write(n.left(), sb);
        write(n.right(), sb);
    }

    // Reads one value, then builds the left side from whatever remains.
    static TreeNode read(java.util.ArrayDeque<Integer> rest) {
        if (rest.isEmpty()) return null;
        int v = rest.pollFirst();
        TreeNode left = read(rest);
        return new TreeNode(v, left, null);
    }
}
```

Take a path to the left, where 1 has left child 2 and 2 has left child 3. It writes `1,2,3`, and the reader returns the same path. A test on paths passes, so the pair looks correct.

```predict
A tree has root 4, left child 2 and right child 6. What line does write produce, and what tree does read return from that line?

The line is 4,2,6. The reader takes 4 as the root, and then its recursive call for the left side consumes both 2 and 6, so 6 becomes the left child of 2. The result is a path of three nodes, and the right child of the root is lost. The line contains no information about which side a value belongs to.
```

<!-- stage: bottleneck -->
### Same Values, Many Shapes

The text must tell the decoder where each subtree ends. A line of n values from a preorder walk fits every binary tree with those n nodes in that order. The count of such trees grows by a factor close to 4 for each added node, so the values alone cannot select one tree. The shape needs one marker for each missing child. A tree with n nodes has n + 1 missing children, so the line gains about one marker per node.

Two cost traps wait after the fix. A decoder that cuts the remaining text with `substring` at every node copies the rest of the line each time. A line of n tokens then costs O(n^2) character copies. A decoder that reads from one shared position costs O(n). The second trap is trust: a decoder that accepts any text and builds some tree hides damaged data. A good design needs three properties. First, every tree has exactly one text. Second, the decoder reads each token once and in the order the encoder wrote it. Third, the decoder accepts exactly the texts that the encoder can produce.

<!-- stage: insight -->
### One Grammar For Both Directions

#### Write The Rules Once

<!-- names: shared grammar, slot, canonical form -->

A **shared grammar** is one set of rules that describes every valid text, and both the encoder and the decoder follow it. For a binary tree in preorder the rules read `tree = N | value tree tree`. The encoder is a walk that produces a text matching the rules. The decoder is a walk of the same shape that consumes a text matching the rules. When the two walks use the same traversal order, an edit to the order changes both, and the pair cannot drift apart.

#### Give Every Child Place A Token

A **slot** is a place where a child may appear. Each node has two slots, a left one and a right one. The encoder writes exactly one token for each slot. The token is a value if a child fills the slot and a marker if the slot is empty. In level order, the queue decides the order of the slots. The oldest queued node owns the next two tokens. A forest of N-ary trees fits the same idea with a different slot pair. The left link of a binary node is the slot for the first child, and the right link is the slot for the next sibling. The roots of a forest form a chain of right links, exactly like the children of one node, so they need no special rule.

#### Accept Exactly One Text Per Tree

The **canonical form** of a tree is the one text that the encoder produces for it. The encoder must produce the canonical form for every tree, and the decoder must accept only the canonical form. In the level-order format, the encoder trims the empty slots at the end of the text, and the decoder treats a missing token as empty. A text that ends with an explicit empty slot then breaks the rule and raises an error. A strict decoder gives a bijection between trees and texts, so a text that is accepted always rebuilds the tree whose canonical form it is.

#### Read A Postorder Text From The End

A search tree writes no markers because the value order fixes the shape. A postorder text lists the left subtree, then the right subtree, then the node. The node is therefore the last token of its subtree. The decoder reads from the end of the text. It takes the node first. It then builds the right subtree, because the right tokens sit just before the node. It builds the left subtree last.

#### Place Equal Values On The Left

The bounds follow one rule for equal values. If equal values go left, a subtree range is `(lo, hi]`, with the lower bound open and the upper bound closed. A node with value `v` gives its right subtree the range `(v, hi]` and its left subtree the range `(lo, v]`. A token outside the range is left for an ancestor. The postorder text `2,2,5` shows the rule. The decoder reads it from the end.

| Step | Token read | Range of the call | Result |
|---|---|---|---|
| 1 | 5 | `(-inf, inf]` | Accepted as the root. |
| 2 | 2 (second) | `(5, inf]` | Rejected, so the right subtree of 5 is empty. |
| 3 | 2 (second) | `(-inf, 5]` | Accepted as the left child of 5. |
| 4 | 2 (first) | `(2, 5]` | Rejected, so the right subtree of that node is empty. |
| 5 | 2 (first) | `(-inf, 2]` | Accepted as its left child. |

The result is a left path 5, 2, 2.

<!-- stage: variables -->
### State Shared By The Two Walks

The pair of walks needs a small amount of state, and each piece has one owner.

- **out** is the list that the encoder appends tokens to, and the second trace shows its length as the pointer `out`.
- **in** is the iterator over the tokens that the decoder reads, and only the decoder moves it. The first trace marks its next unread token with the pointer `in`.
- **queue** holds the nodes whose slots are still unwritten or unread, in level order, and it contains no `null`. The level-order decoder below uses it.
- **lo and hi** are the bounds of a subtree range, held as `long` so that the extreme `int` values stay inside.
- **owner** is the node taken from the front of the queue, and it receives the next two tokens. The trace shows it as `owner`.
- **chain** is the right-linked list of siblings that one call creates or walks in the forest exercise.

Every walk keeps this rule: the position moves only when a token is consumed, and every consumed token fills exactly one slot.

<!-- stage: trace -->
### Reading Levels And Writing Forests

#### Decoding Tokens With A Queue

The text `1,2,3,null,null,4,5` has seven tokens. The pointer `in` marks the next unread token of the iterator `in`. The root takes the first token, and the queue holds the root. The root takes the next two tokens as its left child 2 and its right child 3, and both enter the queue. Node 2 is the oldest queued node, so it takes the next two tokens, and both are `null`. Node 3 takes 4 and 5 as its children. The queue now holds 4 and 5. They find no tokens left, so every one of their slots counts as empty, and the decoder stops with `in` at the token count.

```trace
{"cells":["1","2","3","null","null","4","5"],"pointers":["in"],"steps":[{"at":{"in":1},"vars":{"queue":"[1]","built":"root 1"},"note":"The first token creates the root 1, and the queue holds the root. The index moves to the next unread token."},{"at":{"in":2},"vars":{"queue":"[2]","owner":"1","slot":"left"},"note":"The token 2 fills the left slot of node 1, and the new node joins the back of the queue."},{"at":{"in":3},"vars":{"queue":"[2,3]","owner":"1","slot":"right"},"note":"The token 3 fills the right slot of node 1, and the new node joins the back of the queue."},{"at":{"in":4},"vars":{"queue":"[3]","owner":"2","slot":"left"},"note":"The token null leaves the left slot of node 2 empty."},{"at":{"in":5},"vars":{"queue":"[3]","owner":"2","slot":"right"},"note":"The token null leaves the right slot of node 2 empty."},{"at":{"in":6},"vars":{"queue":"[4]","owner":"3","slot":"left"},"note":"The token 4 fills the left slot of node 3, and the new node joins the back of the queue."},{"at":{"in":7},"vars":{"queue":"[4,5]","owner":"3","slot":"right"},"note":"The token 5 fills the right slot of node 3, and the new node joins the back of the queue."},{"at":{"in":7},"vars":{"queue":"[5]","owner":"4","slot":"left"},"note":"No token is left, so the left slot of node 4 counts as empty."},{"at":{"in":7},"vars":{"queue":"[5]","owner":"4","slot":"right"},"note":"No token is left, so the right slot of node 4 counts as empty."},{"at":{"in":7},"vars":{"queue":"[]","owner":"5","slot":"left"},"note":"No token is left, so the left slot of node 5 counts as empty."},{"at":{"in":7},"vars":{"queue":"[]","owner":"5","slot":"right"},"note":"No token is left, so the right slot of node 5 counts as empty."}]}
```

#### Encoding A Forest As One Binary Tree

The forest has two roots. The first root 1 has the children 2 and 3, and the second root is 4. The encoder links the roots in a right chain, and each root links its children in a chain on its left link. The pointer `out` counts the tokens written so far. The preorder walk of the result visits 1, then its left chain with 2 and 3, then the right link of 1 to the root 4. A missing link writes `N`. The final text has nine tokens, which equals twice the number of nodes plus one.

```trace
{"cells":["1","2","N","3","N","N","4","N","N"],"pointers":["out"],"steps":[{"at":{"out":0},"vars":{"written":"[]"},"note":"Start: the encoder has linked the roots 1 and 4 in a right chain and put 2 and 3 in a chain on the left link of 1. Nothing is written yet."},{"at":{"out":1},"vars":{"written":"1"},"note":"The walk writes the value 1 for the root of the binary tree."},{"at":{"out":2},"vars":{"written":"1 2"},"note":"The walk writes the value 2 for the left link of 1."},{"at":{"out":3},"vars":{"written":"1 2 N"},"note":"The left link of 2 is missing, so the walk writes N."},{"at":{"out":4},"vars":{"written":"1 2 N 3"},"note":"The walk writes the value 3 for the right link of 2."},{"at":{"out":5},"vars":{"written":"1 2 N 3 N"},"note":"The left link of 3 is missing, so the walk writes N."},{"at":{"out":6},"vars":{"written":"1 2 N 3 N N"},"note":"The right link of 3 is missing, so the walk writes N."},{"at":{"out":7},"vars":{"written":"1 2 N 3 N N 4"},"note":"The walk writes the value 4 for the right link of 1."},{"at":{"out":8},"vars":{"written":"1 2 N 3 N N 4 N"},"note":"The left link of 4 is missing, so the walk writes N."},{"at":{"out":9},"vars":{"written":"1 2 N 3 N N 4 N N"},"note":"The right link of 4 is missing, so the walk writes N."}]}
```

<!-- stage: code -->
### One Grammar As Two Small Walks

#### The Encoder And The Decoder Side By Side

The encoder appends tokens to a list. The decoder pulls tokens from an iterator and checks that the iterator is drained at the end. Both methods follow the rule `tree = N | value tree tree`.

```java
final class PreorderPair {
    record TreeNode(int val, TreeNode left, TreeNode right) {}

    static void emit(TreeNode n, java.util.List<String> out) {
        if (n == null) { out.add("N"); return; }                  // an empty slot writes the marker
        out.add(Integer.toString(n.val()));                       // a filled slot writes the value
        emit(n.left(), out);                                      // the left subtree comes first
        emit(n.right(), out);                                     // the right subtree follows
    }

    static TreeNode take(java.util.Iterator<String> in) {
        if (!in.hasNext()) throw new IllegalArgumentException("text ended early");
        String t = in.next();                                     // one call consumes exactly one token
        if (t.equals("N")) return null;
        TreeNode left = take(in);                                 // same order as emit: left, then right
        TreeNode right = take(in);
        return new TreeNode(Integer.parseInt(t), left, right);
    }

    static TreeNode parse(String text) {
        java.util.Iterator<String> in = java.util.Arrays.asList(text.split(",", -1)).iterator();
        TreeNode root = take(in);
        if (in.hasNext()) throw new IllegalArgumentException("leftover tokens"); // exactly one tree per text
        return root;
    }
}
```

#### A Level-Order Decoder

The level-order text needs a queue, because the oldest queued node owns the next two tokens. This sketch uses the iterator `in` and the node `owner` from the trace above. It accepts any text, and the level-order exercise adds the canonical-form checks.

```java
static final class Node {
    int val; Node left, right;
    Node(int val) { this.val = val; }
}

static Node parseLevels(String text) {
    if (text.isEmpty()) return null;                                      // the empty tree has the empty text
    java.util.Iterator<String> in = java.util.Arrays.asList(text.split(",", -1)).iterator();
    Node root = new Node(Integer.parseInt(in.next()));                    // the first token is the root
    java.util.ArrayDeque<Node> queue = new java.util.ArrayDeque<>();
    queue.add(root);
    while (!queue.isEmpty()) {
        Node owner = queue.poll();                                        // the oldest queued node owns two slots
        if (in.hasNext()) {                                               // a missing token means an empty slot
            String t = in.next();
            if (!t.equals("null")) { owner.left = new Node(Integer.parseInt(t)); queue.add(owner.left); }
        }
        if (in.hasNext()) {
            String t = in.next();
            if (!t.equals("null")) { owner.right = new Node(Integer.parseInt(t)); queue.add(owner.right); }
        }
    }
    return root;
}
```

#### Cost And Java Details

- **Encoder** takes O(n) time and O(n) space for n nodes, because every node adds one value token and every missing child adds one marker.
- **Decoder** costs O(n) time, since the iterator hands out each token once and no step copies the remaining text.
- **Recursion depth** equals the tree height, so a degenerate tree of 10^5 nodes needs an explicit stack in place of recursion.

The call `text.split(",", -1)` keeps trailing empty strings, so a damaged text that ends with a comma reaches the decoder as an empty token and fails there. The default `split(",")` would drop that token and accept the damaged text. The class `ArrayDeque` throws `NullPointerException` when asked to store `null`, so a level-order queue holds only real nodes.

<!-- stage: applicability -->
### When The Pair Must Match

#### Recognizing The Pattern

Look for a requirement that a structure be written to text, bytes or another tree and rebuilt equal. Look also for words such as "exactly", "preserve order", "empty child lists" and "reject malformed input". The invariant to state is that the encoder and the decoder follow one traversal order, every slot has one token, and the decoder accepts only the canonical form. A test of that invariant feeds every damaged variant of a valid text to the decoder and expects an error.

#### The Nearest False Friend

The false friend is a pair of programs that pass the round trip `decode(encode(x)) == x`. The round trip covers only the texts that the encoder writes. A decoder that is too lenient passes it and still accepts damaged texts, and an encoder that sometimes writes two texts for one tree passes it too. A second false friend is the trick of dropping markers from a search tree, which fails once the ordering rule changes, for example when duplicates are allowed.

#### When Not To Use It

Do not write a codec by hand when a library format fits the contract and both sides can use it. A text format that must survive many software versions also needs an explicit version token, which a bare grammar lacks. The hand-written pair earns its place when the contract names the format. It also fits when the decoder must reject damaged input.

<!-- stage: exercises -->
### Exercises

#### [Build] Length-Prefixed String Codec (Author exercise)
<!-- id: it37-fixed-width-frames -->

**Prerequisites.** The lesson Structural Codecs and exceptions in Java. This exercise fixes the header width and adds errors for damaged input.

**Problem.** Design a class `FrameCodec`. The method `String encode(List<String> items)` writes one frame per item, in order. A frame is four lowercase hexadecimal digits that give the length of the item, followed by the characters of the item. It throws `IllegalArgumentException` when an item has more than 65535 characters. The method `List<String> decode(String encoded)` returns the list that `encode` would have received. It throws `IllegalArgumentException` for every string that `encode` cannot produce. Such a string has a header with fewer than four characters, a header character outside `0-9a-f`, or a body shorter than its header states.

**Constraints.** These limits apply:
- **Items** number from 0 to 1000, and each item has at most 65535 characters.
- **Characters** are any UTF-16 code units, and the pipe, digits and letters from `a` to `f` are allowed inside bodies.
- **Empty list** encodes to the empty string.
- **Input** of `decode` may be any string.

**Example 1.** Input the list `["hi", "", "a|b"]`, output the encoding `0002hi00000003a|b`, and the decoder returns the same list.

**Example 2.** Input the strings `0005ab`, `00` and `000g`, output an `IllegalArgumentException` for each, because the body is short, the header is short, and `g` is not a hexadecimal digit.

**Hint.** The header has a fixed width, so where does the decoder look for the end of the header, and what must it check before it reads the body?

**Changed decision.** A fixed-width header replaces the search for a delimiter, and the decoder rejects every input that the encoder cannot produce. Library parsing is not strict enough for the header.

#### [Vary] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: it37-level-order-codec -->

**Prerequisites.** The first exercise above and breadth-first search with a queue. This exercise changes the contract of LeetCode 297: the order is level by level, trailing empty slots are trimmed, and the decoder accepts only that canonical form.

**Problem.** Each `TreeNode` stores an `int val` and the links `left` and `right`. Examples list a tree in level order and use `null` for an absent child. The method `String serialize(TreeNode root)` visits the nodes level by level, left to right. Each visited node writes its left slot and then its right slot as the child value or the token `null`, and the tokens are joined by commas. The root value comes first. Trailing `null` tokens are removed, and the empty tree gives the empty string. The method `TreeNode deserialize(String s)` returns the tree and throws `IllegalArgumentException` for every string that `serialize` cannot produce.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 1000.
- **Values** are any `int`.
- **Accepted strings** do not begin or end with `null`, and every token is `null` or a decimal integer.
- **Leftover tokens** that no queued node can claim make the string invalid.

**Example 1.** Input the tree `[1, 2, 3, null, null, 4, 5]`, output `1,2,3,null,null,4,5`.

**Example 2.** Input the string `4,3,null,2`, output the tree `[4, 3, null, 2]`. Input the string `1,null`, output an `IllegalArgumentException`, because the text ends with `null`.

**Hint.** When the tokens end while nodes are still waiting in the queue, what must the remaining slots of those nodes be?

**Changed decision.** The queue decides which node owns the next two tokens, so the decoder is iterative and has no recursion. Trimming makes the text shorter and requires the decoder to restore the missing slots.

#### [Boundary] Encode N-ary Forest to Binary Tree (LeetCode 431)
<!-- id: it37-forest-to-binary -->

**Prerequisites.** The second exercise above and the exercise on N-ary trees in the lesson Structural Codecs. This exercise changes the contract of LeetCode 431: the input is an ordered forest, not one tree.

**Problem.** Each N-ary `Node` stores an `int val` and an ordered `List<Node> children`. A forest is an ordered list of N-ary roots. The method `TreeNode encode(List<Node> roots)` returns one binary tree in which the roots form a chain of right links, and the left link of each binary node starts the chain of the children of that node. The method `List<Node> decode(TreeNode root)` returns a forest equal to the forest that `encode` received. An empty forest encodes to `null`, and a node without children decodes to a node with an empty list. In the examples, a forest is written as `[value[child,child],value]`, and a binary tree is written as its preorder with `N` for a missing link.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 10^4, and the height is at most 1000.
- **Roots and children** per list are unrestricted, and list order is the order in the chain.
- **Values** are any `int`.
- **Empty forest** and the forest with one childless root must encode to different trees.

**Example 1.** Input the forest `[1[2,3],4]`, output the binary tree `1 2 N 3 N N 4 N N`.

**Example 2.** Input the forest `[7,8]`, output `7 N 8 N N`. Input the empty forest, output `N`.

**Hint.** A root and a child both belong to a list of siblings. Which single helper can build the chain for both?

**Changed decision.** The roots are treated like any other sibling list, so one helper serves the forest and every children list. The empty forest becomes a boundary case of the same rule.

#### [Recognize] Serialize and Deserialize BST (LeetCode 449)
<!-- id: it37-bst-postorder-duplicates -->

**Prerequisites.** The bounds idea from the lesson Structural Codecs, where each subtree accepts only values inside a range, and the bounded preorder decoder from that lesson. This exercise is a transfer prompt: the interview question is how the bounds change when equal values are allowed and the text is postorder. It changes the contract of LeetCode 449.

**Problem.** A binary search tree stores `int` values. Every value in the left subtree is at most the node value, and every value in the right subtree is greater. The method `String serialize(TreeNode root)` returns the values in postorder, separated by commas, with no other token. The empty tree gives the empty string. The method `TreeNode deserialize(String s)` returns the tree that `s` describes and throws `IllegalArgumentException` when no tree that follows the rule has `s` as its postorder.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 1000.
- **Values** may repeat and cover the whole `int` range.
- **Tokens** in a valid string equal the number of nodes.
- **Strings** passed to `deserialize` may be malformed.

**Example 1.** Input the tree with root 5, left subtree `3(3, 4)` and right subtree `8(null, 9)`, output `3,4,3,9,8,5`.

**Example 2.** Input the string `3,3,3`, output a tree in which each node has only a left child. Input `3,6,2,5`, output an `IllegalArgumentException`, because the value 6 is greater than the root 5 and still belongs to no right subtree.

**Hint.** Reading from the end, which subtree comes right after the root, and which side owns a token that equals the root?

**Changed decision.** The text is read backward, so the right subtree is built first. Equal values go left, so the upper bound of a range is closed and the lower bound is open.
