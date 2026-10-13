<!-- lesson-kind: standard -->
<!-- lesson-id: structural-codecs -->
## Structural Codecs

<!-- stage: context -->
### Why Splitting At Commas Loses Data

A service stores the saved search tags of a user as one text line and sends the line to a second service. The sender joins the tags with commas, and the receiver splits the line at every comma. One user saved the two tags `c` and `c,c++`, and the second tag contains a comma on purpose. The receiver shows three tags, `c`, `c` and `c++`. The user never typed the third tag, and the original second tag is gone.

The same failure appears for trees. A cache keeps a binary tree as its values in the order a traversal visits them, and two different trees produce the same line. Each side works correctly on its own, and the data still changes on the way. The question of this lesson is how to write a structured value as a flat string. A decoder must rebuild exactly the value that went in, in one pass over the string.

<!-- stage: naive -->
### Join With A Delimiter And Split Back

The direct design picks a character that tags are unlikely to contain, joins the tags with it, and splits the line at that character. The class below does this with a comma.

```java
final class NaiveCodec {
    // Joins the tags with one comma between neighbours.
    static String encode(java.util.List<String> tags) {
        return String.join(",", tags);
    }

    // Cuts the line at every comma.
    static java.util.List<String> decode(String line) {
        return java.util.Arrays.asList(line.split(","));
    }
}
```

For the tags `go` and `java`, the encoder returns `go,java`, and the decoder returns the same two tags. A test with ordinary words passes, so the class looks finished.

```predict
What does decode(encode(list)) return for the three inputs ["c,c++"], ["x", ""] and the empty list?

For ["c,c++"], the line is c,c++ and the decoder returns two tags, c and c++. For ["x", ""], the line is x, and the Java method split removes trailing empty strings, so the decoder returns only x. For the empty list, the line is the empty string, and split on an empty string returns an array with one empty string, so the decoder returns [""] and not the empty list. All three results differ from the input.
```

<!-- stage: bottleneck -->
### Two Inputs With One Encoding

#### Why The Comma Design Fails

The defect is not slowness. A decoder is a function from the line back to the value. When two different values produce the same line, no decoder can return both of them. The encoder must therefore be injective, which means that different inputs always produce different lines. The comma design breaks injectivity at three places. A tag may contain the delimiter, a list may end with an empty tag, and the empty list collides with the list of one empty tag.

#### What An Escape Rule Costs

An escape rule is the usual repair. The encoder writes a backslash before every comma and every backslash, and the decoder undoes the rule. This works, and it costs more than it seems. The decoder has to read every character of every tag to find the escapes. Even a count of the tags takes O(n) time for a line of n characters. The encoder also rewrites each tag before it appends it.

#### What A Tree Line Needs

Trees have the same weakness in a different form. A preorder line of n values fits many different trees, and the number of binary trees with n nodes grows by a factor close to 4 for each added node. The line must carry the shape as well as the values. A good encoding has to meet three requirements. First, every input must have exactly one line. Second, the decoder must find each unit boundary without guessing. Third, one pass over the line must consume exactly the characters of one value, with no leftover and no overrun.

<!-- stage: insight -->
### Put Boundaries In The Text

#### State The Size Before The Content

<!-- names: length prefix, null marker, read cursor, value range -->

A **length prefix** is a number written in front of a piece of text that states how many characters the piece holds. For the tag list, each tag becomes a frame: its length in decimal digits, one `#`, and then the characters. The decoder reads digits up to the first `#`, converts them to a number `len`, and takes exactly `len` characters. It never looks at those characters, so a `#`, a digit or a comma inside a tag cannot move the boundary. The empty list encodes to the empty string, and the list of one empty tag encodes to `0#`, so the two stay apart.

#### Mark Every Missing Child

A **null marker** is a token written in the place of a child that does not exist. For a binary tree, the preorder line writes a node value, then the whole left subtree, then the whole right subtree. The line uses the token `N` for an absent subtree. Every node then has exactly two child places, and each place holds either a value or a marker. A tree with n nodes writes n values and n + 1 markers. The grammar `tree = N | value tree tree` has only one way to split a line into a root, a left part and a right part.

#### Turn Many Children Into Two Links

This step lets the binary grammar above encode a tree whose nodes have any number of children. The standard step turns an N-ary tree into a binary tree. The left link of a binary node points to the first child, and the right link points to the next sibling. A parent then owns its children through a chain of right links that starts at its left link, and the order of the chain is the order of the children.

#### Read With One Shared Position

A **read cursor** is one index into the token array that every decoding step shares. A step reads the token at the cursor and moves the cursor forward by the number of tokens it consumed. For a tree, the step that decodes a node first reads the value, then calls itself for the left subtree, then calls itself for the right subtree. When a call returns, the cursor stands right after one complete subtree. Tokens may remain after the root call returns, or the tokens may end inside a subtree. In both cases the line is not a valid encoding, and the decoder reports an error.

#### Let The Order Replace The Markers

The last idea uses the ordering of a binary search tree to drop the markers. A **value range** is the pair of open bounds `(lo, hi)` that every value in a subtree of a binary search tree must satisfy. The root has no bounds. A left subtree of a node with value `v` takes the range `(lo, v)`, and a right subtree takes `(v, hi)`. A preorder line of values without markers is then enough. The decoder looks at the next token. If the token lies inside the current range, it becomes the next node. If the token lies outside, the subtree is finished, and the token stays unread for an ancestor whose range contains it.

<!-- stage: variables -->
### What The Decoder Tracks

The decoders in this lesson keep a small state. Each piece answers one question about the text that remains.

- **enc** is the encoded string, and it never changes during decoding.
- **i** is the index of the first character of the next frame, always on a frame boundary.
- **hash** is the index of the first `#` at or after `i`, which ends the header.
- **len** is the number of body characters that the current header promises.
- **items** is the list of decoded tags.
- **rest** is the deque of unread tokens of a tree line, and it acts as the read cursor.
- **next** is the front token of `rest`, read with `peekFirst`, or null when `rest` is empty.
- **lo and hi** are the open bounds of the value range for the subtree under construction, stored as `long`.

The bounds use `long` because a tree may store `Integer.MIN_VALUE` or `Integer.MAX_VALUE`, and a bound of type `int` could not stand strictly outside those two values.

<!-- stage: trace -->
### Reading Frames And Bounded Subtrees

#### Decoding A Framed String

The encoded string `2#ab0#3#c#d` holds three frames. The pointer `i` marks the first character of the current frame, and the pointer `hash` marks the `#` that ends its header. The decoder reads the digit 2 and the `#`, so the body starts right after `hash`. It takes `ab` and moves `i` past them. The next header is `0#`, so the body is empty, and the decoder takes nothing. The last header reads 3, and the body `c#d` contains a `#` that the decoder never examines, because the length already fixed where the frame ends. At the end `i` equals the number of cells, and the list holds three tags.

```trace
{"cells":["2","#","a","b","0","#","3","#","c","#","d"],"pointers":["i","hash"],"steps":[{"at":{"i":0,"hash":-1},"vars":{"items":"[]"},"note":"Start: the pointer i stands on the first character of the first frame, and no item is decoded."},{"at":{"i":4,"hash":1},"vars":{"len":2,"items":"[\"ab\"]"},"note":"The header says 2. The decoder takes the next 2 characters and moves i past them."},{"at":{"i":6,"hash":5},"vars":{"len":0,"items":"[\"ab\", \"\"]"},"note":"The header says 0, so the frame has an empty body. The decoder takes no characters and stores an empty item."},{"at":{"i":11,"hash":7},"vars":{"len":3,"items":"[\"ab\", \"\", \"c#d\"]"},"note":"The header says 3. The decoder takes the next 3 characters, including the # inside the body, because the length already fixed where the frame ends."}]}
```

#### Decoding A Preorder Line With Ranges

The line `5 3 1 4 8 9` is the preorder of a binary search tree with no markers. The pointer `rest` marks the front token of the deque `rest`, which is the token that the next decoding call looks at. The variable `range` shows the pair `lo` and `hi`, and `built` lists the nodes created so far. The root takes 5. The left call with range `(-inf, 5)` takes 3 and then 1. The call for the left child of 1 sees 4, which lies above the bound 1, so it returns without moving. The right call under 1 has range `(1, 3)` and also refuses 4. The right call under 3 has range `(3, 5)`, so it accepts 4. After that, 8 lies outside `(3, 4)` and `(4, 5)`, and both calls refuse it, so control returns to the root, whose right range `(5, inf)` accepts 8. The last token 9 becomes the right child of 8, and the final calls find no tokens.

```trace
{"cells":["5","3","1","4","8","9"],"pointers":["rest"],"steps":[{"at":{"rest":0},"vars":{"range":"(-inf, inf)","built":"[]"},"note":"Start: the root call has no bounds, and every token is still unread."},{"at":{"rest":1},"vars":{"range":"(-inf, inf)","built":"[5]"},"note":"The token 5 lies inside (-inf, inf), so it becomes a node. Its left range is (-inf, 5) and its right range is (5, inf)."},{"at":{"rest":2},"vars":{"range":"(-inf, 5)","built":"[5, 3]"},"note":"The token 3 lies inside (-inf, 5), so it becomes a node. Its left range is (-inf, 3) and its right range is (3, 5)."},{"at":{"rest":3},"vars":{"range":"(-inf, 3)","built":"[5, 3, 1]"},"note":"The token 1 lies inside (-inf, 3), so it becomes a node. Its left range is (-inf, 1) and its right range is (1, 3)."},{"at":{"rest":3},"vars":{"range":"(-inf, 1)","built":"[5, 3, 1]"},"note":"The token 4 lies outside (-inf, 1), so the call returns null and leaves the token for an ancestor."},{"at":{"rest":3},"vars":{"range":"(1, 3)","built":"[5, 3, 1]"},"note":"The token 4 lies outside (1, 3), so the call returns null and leaves the token for an ancestor."},{"at":{"rest":4},"vars":{"range":"(3, 5)","built":"[5, 3, 1, 4]"},"note":"The token 4 lies inside (3, 5), so it becomes a node. Its left range is (3, 4) and its right range is (4, 5)."},{"at":{"rest":4},"vars":{"range":"(3, 4)","built":"[5, 3, 1, 4]"},"note":"The token 8 lies outside (3, 4), so the call returns null and leaves the token for an ancestor."},{"at":{"rest":4},"vars":{"range":"(4, 5)","built":"[5, 3, 1, 4]"},"note":"The token 8 lies outside (4, 5), so the call returns null and leaves the token for an ancestor."},{"at":{"rest":5},"vars":{"range":"(5, inf)","built":"[5, 3, 1, 4, 8]"},"note":"The token 8 lies inside (5, inf), so it becomes a node. Its left range is (5, 8) and its right range is (8, inf)."},{"at":{"rest":5},"vars":{"range":"(5, 8)","built":"[5, 3, 1, 4, 8]"},"note":"The token 9 lies outside (5, 8), so the call returns null and leaves the token for an ancestor."},{"at":{"rest":6},"vars":{"range":"(8, inf)","built":"[5, 3, 1, 4, 8, 9]"},"note":"The token 9 lies inside (8, inf), so it becomes a node. Its left range is (8, 9) and its right range is (9, inf)."},{"at":{"rest":6},"vars":{"range":"(8, 9)","built":"[5, 3, 1, 4, 8, 9]"},"note":"No token is left, so the call with range (8, 9) returns null."},{"at":{"rest":6},"vars":{"range":"(9, inf)","built":"[5, 3, 1, 4, 8, 9]"},"note":"No token is left, so the call with range (9, inf) returns null."}]}
```

<!-- stage: code -->
### Frames And Bounded Preorder In Java

#### The String Frames

The encoder appends the length, the `#` and the text. The decoder finds the next `#` with `indexOf`, parses the digits before it, and cuts the body by position.

```java
final class FrameCodec {
    static String encode(java.util.List<String> items) {
        StringBuilder out = new StringBuilder();
        for (String s : items) out.append(s.length()).append('#').append(s);
        return out.toString();
    }

    static java.util.List<String> decode(String enc) {
        java.util.List<String> items = new java.util.ArrayList<>();
        int i = 0;
        while (i < enc.length()) {
            int hash = enc.indexOf('#', i);                       // the first '#' after a frame start is always a header end
            int len = Integer.parseInt(enc.substring(i, hash));   // the digits before it are the body length
            items.add(enc.substring(hash + 1, hash + 1 + len));   // exactly len characters, whatever they are
            i = hash + 1 + len;                                   // the next frame starts right after the body
        }
        return items;
    }
}
```

#### The Bounded Tree Decoder

The tree decoder uses immutable nodes, so it builds both children before it creates the parent. The deque holds the tokens that are still unread, and `peekFirst` looks without consuming.

```java
final class BoundedTree {
    record Node(int val, Node left, Node right) {}

    static Node build(java.util.ArrayDeque<Integer> rest, long lo, long hi) {
        Integer next = rest.peekFirst();                          // looking does not consume
        if (next == null || next <= lo || next >= hi) return null; // outside the range: leave the token for an ancestor
        int v = rest.pollFirst();                                 // inside the range: this token is a node
        Node left = build(rest, lo, v);                           // left values stay below v
        Node right = build(rest, v, hi);                          // right values stay above v
        return new Node(v, left, right);
    }
}
```

#### Cost And Java Details

- **Frames** cost O(n) time and space for n characters, because each character is appended once and copied once.
- **Bounded decode** costs O(k) time for k tokens, since each call either consumes one token or returns at once.
- **Recursion depth** equals the tree height, and a degenerate tree of 10^5 nodes can overflow the default thread stack, so an explicit stack is safer for such input.

The call `Integer.parseInt` throws `NumberFormatException` for a bad header, and this exception is a subclass of `IllegalArgumentException`. A decoder that must report malformed input can let it propagate or wrap it with a clearer message.

<!-- stage: applicability -->
### When A Codec Needs Boundaries

#### Recognizing The Pattern

Look for a structured value that must cross a flat string, a byte stream or a different tree shape, with the statement that the receiver rebuilds exactly the sender's value. Look also for tags such as "any characters", "may be empty", "preserve the order of children" and "no extra information". The invariant to state is that every encoded unit has an unambiguous boundary, and every decoder step consumes one complete unit. Then check injectivity by asking which two different inputs could produce the same text.

#### The Nearest False Friend

The false friend is a delimiter that never occurs in the test data. It makes every example pass and fails on the first input that contains the delimiter or ends with an empty piece. A second false friend is the preorder line of a binary search tree with duplicates or with an unknown ordering rule. The bounds trick needs a stated ordering and a stated rule for equal values. Without them, the markers are required.

#### When Not To Use It

Do not design a text format when a standard one fits and both sides can use a library. Java's own serialization, JSON or a length-delimited binary format already handle escapes, nesting and versions. Hand-written framing earns its place when the contract forbids libraries. It also fits when the decoder must skip items without copying them.

<!-- stage: exercises -->
### Exercises

#### [Build] Encode and Decode Strings (LeetCode 271)
<!-- id: it37-string-framing -->

**Prerequisites.** Strings and `StringBuilder`. This exercise changes the contract of LeetCode 271: the encoding format is fixed, and a third method counts the items without copying them.

**Problem.** Design a class `StringCodec`. The method `String encode(List<String> items)` returns the concatenation, over the items in order, of the decimal length of the item without leading zeros, the character `#`, and the characters of the item. The method `List<String> decode(String encoded)` returns a list equal to the list that `encode` received. The method `int count(String encoded)` returns the number of items and does not copy any item.

**Constraints.** These limits apply:
- **Items** number from 0 to 10^4, and the total number of characters is at most 10^5.
- **Characters** are any UTF-16 code units, including `#` and decimal digits.
- **Empty strings** are allowed as items, and the list itself may be empty.
- **Input** of `decode` and `count` is always the output of `encode`, so no error handling is required.

**Example 1.** Input the list `["ab", "", "c#d"]`, output the encoding `2#ab0#3#c#d`, the decoded list `["ab", "", "c#d"]` and the count 3.

**Example 2.** Input the list `[""]` and the empty list, output the encodings `0#` and the empty string, with counts 1 and 0.

**Hint.** After the decoder reads the digits and the `#`, how many characters does it know belong to the current item?

**Changed decision.** The format is fixed by length, so the body of an item is never examined. The method `count` follows the headers and jumps over each body with one addition.

#### [Vary] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: it37-binary-tree-nulls -->

**Prerequisites.** The first exercise above and preorder traversal. This exercise changes the contract of LeetCode 297: the text format is fixed, and the decoder must reject any string that is not exactly one tree.

**Problem.** A binary tree node has an `int val` and two links, `left` and `right`. In the examples, a tree is written in level order, where `null` marks a missing child. The method `String serialize(TreeNode root)` writes the tree in preorder as tokens separated by single spaces. A node writes its decimal value, then its left subtree, then its right subtree, and a missing child writes `N`. The method `TreeNode deserialize(String s)` returns the tree that `s` describes. It throws `IllegalArgumentException` when `s` is not exactly one tree in this format.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 1000.
- **Values** are any `int`, including negative values.
- **Empty tree** is `null` and serializes to `N`.
- **Malformed input** includes a missing token, a leftover token, an empty token and a token that is neither `N` nor an integer.

**Example 1.** Input the tree `[1, 2, 3, null, null, 4, 5]`, output the string `1 2 N N 3 4 N N 5 N N`.

**Example 2.** Input the empty tree, output `N`. Input the string `1 N N N`, output an `IllegalArgumentException`, because the tree ends after three tokens and one token remains.

**Hint.** After the call for the root returns, what must be true about the position in the token array if the string is exactly one tree?

**Changed decision.** The markers make the shape explicit, and the shared position makes the end of the tree explicit. The decoder checks both, so the string must match the grammar exactly.

#### [Boundary] Encode N-ary Tree to Binary Tree (LeetCode 431)
<!-- id: it37-nary-to-binary -->

**Prerequisites.** The second exercise above. This exercise changes the contract of LeetCode 431: the link roles are fixed, and the decoder must return empty children lists.

**Problem.** An N-ary node has an `int val` and an ordered `List<Node> children`. The method `TreeNode encode(Node root)` returns a binary tree in which the left link of each binary node points to the binary node of the first child, and the right link points to the binary node of the next sibling. The method `Node decode(TreeNode root)` returns an N-ary tree equal to the tree that `encode` received. A node without children decodes to a node with an empty list. In the examples, an N-ary tree is written as `value[child,child]`, and a binary tree is written as its preorder with `N` for a missing link.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 10^4, and the height is at most 1000.
- **Children** per node are unrestricted, and the order of the list is the order of the children.
- **Values** are any `int`.
- **Root** of an encoded tree has a `null` right link, and an absent tree encodes to `null`.

**Example 1.** Input the tree `1[3[5,6],2,4]`, output the binary tree `1 3 5 N 6 N N 2 N 4 N N N`.

**Example 2.** Input the tree `7`, output `7 N N`. Input the absent tree, output `N`.

**Hint.** Which link of a binary node reaches its first child, and which link reaches the next child of the same parent?

**Changed decision.** Ownership of children moves into the links. A sibling hangs on the right link of the previous sibling, so a long list of children makes a long right chain and adds no depth.

#### [Recognize] Serialize and Deserialize BST (LeetCode 449)
<!-- id: it37-bst-preorder-bounds -->

**Prerequisites.** The second exercise above and binary search tree ordering. This exercise is a transfer prompt: the interview question is how to use the ordering to drop the markers. It changes the contract of LeetCode 449 with a strict decoder.

**Problem.** A binary search tree has distinct `int` values, with every value in the left subtree below the node value and every value in the right subtree above it. The method `String serialize(TreeNode root)` returns the values in preorder, separated by single spaces, with no other token. The empty tree gives the empty string. The method `TreeNode deserialize(String s)` returns the tree that `s` describes and throws `IllegalArgumentException` when no binary search tree has `s` as its preorder.

**Constraints.** These limits apply:
- **Nodes** number from 0 to 1000.
- **Values** are distinct and cover the whole `int` range.
- **Tokens** in a valid string equal the number of nodes.
- **Strings** passed to `deserialize` may be malformed.

**Example 1.** Input the tree with root 5, left subtree `3(1, 4)` and right subtree `8(null, 9)`, output `5 3 1 4 8 9`.

**Example 2.** Input the string `5 3 7 4`, output an `IllegalArgumentException`. The token 7 becomes the right child of 5, and the token 4 lies outside every open range that remains.

**Hint.** If a token falls outside the bounds of the subtree under construction, which part of the tree must own it?

**Changed decision.** The shape comes from the value ranges and no marker is written. A leftover token after the root call proves that the string is not a valid preorder.
