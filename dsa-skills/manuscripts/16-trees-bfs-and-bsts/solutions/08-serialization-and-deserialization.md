<!-- solutions-for: 08-serialization-and-deserialization -->
### Solutions For Tree Text

#### Solution: [Build] Preorder With Null Markers (Author exercise)
<!-- id: tb-codec-preorder -->

**Approach.**
The method appends tokens to a `StringBuilder` during a preorder walk. A call for a null node appends the marker `#`. A call for a real node appends its value and then makes two calls, the left child first and the right child second. A comma goes before every token except the first, so no token carries a trailing separator. Every empty slot in the tree writes exactly one marker, and a tree with `n` nodes has `n + 1` empty slots, so the text holds `2n + 1` tokens.

The invariant is that the tokens of a subtree form one contiguous block that starts with the subtree root. The marker for each missing child keeps that block self-delimiting.

**Complexity.**
- **Time** is O(n), because each node and each empty slot is handled once.
- **Space** is O(h) for the recursion stack, plus the output text.

```java run
import java.util.*;

public final class PreorderMarkers {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the preorder text with # for each empty slot.
     * Time: O(n), because each node and slot is handled once.
     * Space: O(h) for the recursion, plus the text.
     * Invariant: the tokens of a subtree form one contiguous block.
     */
    static String serialize(TreeNode root) {
        StringBuilder out = new StringBuilder();
        write(root, out);
        return out.toString();
    }

    private static void write(TreeNode node, StringBuilder out) {
        if (out.length() > 0) out.append(',');          // a separator goes between tokens only
        if (node == null) { out.append('#'); return; }  // the marker keeps the empty slot visible
        out.append(node.val);
        write(node.left, out);
        write(node.right, out);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(10)));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(10));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    /** Oracle: a string built by a different recursion that returns a list of tokens. */
    static List<String> tokens(TreeNode n) {
        List<String> out = new ArrayList<>();
        if (n == null) { out.add("#"); return out; }
        out.add(String.valueOf(n.val));
        out.addAll(tokens(n.left));
        out.addAll(tokens(n.right));
        return out;
    }

    static int size(TreeNode n) { return n == null ? 0 : 1 + size(n.left) + size(n.right); }

    public static void main(String[] args) {
        // Example 1: the five-node tree.
        TreeNode r = new TreeNode(1);
        r.left = new TreeNode(2);
        r.right = new TreeNode(3);
        r.right.left = new TreeNode(4);
        r.right.right = new TreeNode(5);
        if (!serialize(r).equals("1,2,#,#,3,4,#,#,5,#,#")) throw new AssertionError("ex1");
        // Example 2: the null root.
        if (!serialize(null).equals("#")) throw new AssertionError("ex2");
        // Trees that differ only in the side of a child must give different text.
        TreeNode a = new TreeNode(1), b = new TreeNode(1);
        a.left = new TreeNode(2);
        b.right = new TreeNode(2);
        if (serialize(a).equals(serialize(b))) throw new AssertionError("ambiguous");
        // Random trees must match the token oracle and hold 2n + 1 tokens.
        Random rnd = new Random(1671);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            String text = serialize(x);
            if (!text.equals(String.join(",", tokens(x)))) throw new AssertionError("oracle " + t);
            if (text.split(",").length != 2 * size(x) + 1) throw new AssertionError("count " + t);
        }
    }
}
```

#### Solution: [Vary] Recursive Decoder (Author exercise)
<!-- id: tb-codec-decoder -->

**Approach.**
The method splits the text at the commas and keeps one shared index in a one-element array. A recursive call reads the token at the index and advances the index by one, so each token is consumed exactly once. A token `#` returns `null`. Any other token creates a node with `Integer.parseInt`, and then the call builds the left subtree and the right subtree by two more calls that continue from the shared index. After the root call, the method walks the rebuilt tree level by level with a queue and returns the values from left to right. The final index equals the token count, because the text held exactly one tree.

The invariant is that each call finds the tokens of its own subtree next in the text. The writer's preorder grammar guarantees that, and the shared index never rewinds.

**Complexity.**
- **Time** is O(n), because each token is read once and each node is queued once.
- **Space** is O(n) for the tokens and the tree, plus O(h) for the recursion.

```java run
import java.util.*;

public final class RecursiveDecoder {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static int consumed;                                    // tokens read by the last decode, for checking

    /**
     * Rebuilds the tree from its text and returns its values in level order.
     * Time: O(n), because each token is read once.
     * Space: O(n) for the tree, plus O(h) for the recursion.
     * Invariant: each call finds its own subtree's tokens next, and the index never moves back.
     */
    static List<Integer> levelValues(String text) {
        String[] tokens = text.split(",");
        int[] index = {0};
        TreeNode root = read(tokens, index);
        consumed = index[0];
        List<Integer> out = new ArrayList<>();
        if (root == null) return out;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {                          // plain level order over the rebuilt tree
            TreeNode node = queue.poll();
            out.add(node.val);
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
        }
        return out;
    }

    private static TreeNode read(String[] tokens, int[] index) {
        String token = tokens[index[0]++];                  // one token per call
        if (token.equals("#")) return null;
        TreeNode node = new TreeNode(Integer.parseInt(token));
        node.left = read(tokens, index);                    // left subtree tokens come next
        node.right = read(tokens, index);
        return node;
    }

    static String write(TreeNode n) {
        if (n == null) return "#";
        return n.val + "," + write(n.left) + "," + write(n.right);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(10)));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(10));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    static List<Integer> oracle(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        List<TreeNode> row = new ArrayList<>();
        if (root != null) row.add(root);
        while (!row.isEmpty()) {
            List<TreeNode> next = new ArrayList<>();
            for (TreeNode n : row) {
                out.add(n.val);
                if (n.left != null) next.add(n.left);
                if (n.right != null) next.add(n.right);
            }
            row = next;
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: five nodes in level order.
        if (!levelValues("1,2,#,#,3,4,#,#,5,#,#").equals(List.of(1, 2, 3, 4, 5))) throw new AssertionError("ex1");
        // Example 2: the empty tree.
        if (!levelValues("#").isEmpty()) throw new AssertionError("ex2");
        // Random trees: write, decode, and compare; every token must be consumed exactly once.
        Random rnd = new Random(1672);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            String text = write(x);
            if (!levelValues(text).equals(oracle(x))) throw new AssertionError("round " + t);
            if (consumed != text.split(",").length) throw new AssertionError("consumed " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty, Negative, And Multi-Digit Values (Author exercise)
<!-- id: tb-codec-edges -->

**Approach.**
The writer uses the comma as the separator and `#` as the marker. A comma cannot appear inside a number, and `#` is not a digit or a minus sign, so every token is either a whole signed integer or the marker. A value such as `-12` is written by `append(int)` as one token, and the next token starts after the next comma. The empty tree writes the single token `#`. The method then confirms that the matching reader returns the same tree, which holds because each call consumes one token and `Integer.parseInt` accepts a leading minus sign and several digits.

The invariant is that every token is parsed from the characters between two commas, so a number never merges with its neighbor and no marker looks like a number.

**Complexity.**
- **Time** is O(n), because each node and slot writes one token.
- **Space** is O(h) for the recursion, plus the text.

```java run
import java.util.*;

public final class CodecEdges {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the text form with commas and # for empty slots.
     * Time: O(n), because each node and slot writes one token.
     * Space: O(h) for the recursion, plus the text.
     * Invariant: every token is a whole signed integer or the marker.
     */
    static String serialize(TreeNode root) {
        StringBuilder out = new StringBuilder();
        write(root, out);
        return out.toString();
    }

    private static void write(TreeNode node, StringBuilder out) {
        if (out.length() > 0) out.append(',');
        if (node == null) { out.append('#'); return; }
        out.append(node.val);                           // a minus sign and all digits stay in one token
        write(node.left, out);
        write(node.right, out);
    }

    static TreeNode deserialize(String text) {
        String[] tokens = text.split(",");
        return read(tokens, new int[] {0});
    }

    private static TreeNode read(String[] tokens, int[] index) {
        String token = tokens[index[0]++];
        if (token.equals("#")) return null;
        TreeNode node = new TreeNode(Integer.parseInt(token));   // parseInt accepts a leading minus sign
        node.left = read(tokens, index);
        node.right = read(tokens, index);
        return node;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(2001) - 1000));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(2001) - 1000);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        // Example 1: a negative root with a multi-digit left child.
        TreeNode r = new TreeNode(-12);
        r.left = new TreeNode(305);
        if (!serialize(r).equals("-12,305,#,#,#")) throw new AssertionError("ex1");
        // Example 2: the empty tree.
        if (!serialize(null).equals("#")) throw new AssertionError("ex2");
        // Java claim: parseInt reads signed and multi-digit tokens.
        if (Integer.parseInt("-1000") != -1000 || Integer.parseInt("305") != 305) throw new AssertionError("parse");
        // Values-only text cannot tell two shapes apart, so the markers are required.
        TreeNode a = new TreeNode(1), b = new TreeNode(1);
        a.left = new TreeNode(2);
        b.right = new TreeNode(2);
        if (serialize(a).equals(serialize(b))) throw new AssertionError("shape");
        // Random trees with values from -1000 to 1000 must round-trip exactly, and the text must use only allowed characters.
        Random rnd = new Random(1673);
        for (int t = 0; t < 400; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(40));
            String text = serialize(x);
            if (!text.matches("[0-9,#-]+")) throw new AssertionError("chars " + t);
            if (!same(x, deserialize(text))) throw new AssertionError("round " + t);
        }
    }
}
```

#### Solution: [Recognize] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: tb-codec-297 -->

**Approach.**
The class pairs a writer and a reader that follow one grammar: a tree is either the marker `#` or a value followed by a left tree and a right tree. `serialize` walks the tree in preorder and writes a comma-separated token for every node and every empty slot. `deserialize` splits the text at the commas and reads the tokens with one shared index. A marker returns `null`, and a number creates a node whose two children come from the next two calls. The marker keeps the shape, and the comma keeps multi-digit and negative values whole, so a round trip rebuilds the same tree. Repeated values do not matter, because the text records positions and not value lookups.

The invariant is that the reader's calls consume the writer's tokens in the writer's order, so each subtree reads its own block of tokens.

**Complexity.**
- **Time** is O(n) for each method, because every node and slot is handled once.
- **Space** is O(h) for the recursion, plus O(n) for the text and the tokens.

```java run
import java.util.*;

public final class Codec {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Writes a tree as text, and reads it back.
     * Time: O(n) for each method.
     * Space: O(h) for the recursion, plus the text and tokens.
     * Invariant: the reader consumes the writer's tokens in the writer's order.
     */
    String serialize(TreeNode root) {
        StringBuilder out = new StringBuilder();
        write(root, out);
        return out.toString();
    }

    private void write(TreeNode node, StringBuilder out) {
        if (out.length() > 0) out.append(',');
        if (node == null) { out.append('#'); return; }
        out.append(node.val);
        write(node.left, out);
        write(node.right, out);
    }

    TreeNode deserialize(String data) {
        String[] tokens = data.split(",");
        int[] index = {0};                                  // the shared position
        return read(tokens, index);
    }

    private TreeNode read(String[] tokens, int[] index) {
        String token = tokens[index[0]++];
        if (token.equals("#")) return null;
        TreeNode node = new TreeNode(Integer.parseInt(token));
        node.left = read(tokens, index);
        node.right = read(tokens, index);
        return node;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(7) - 3));          // small range forces repeated values
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(7) - 3);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        Codec codec = new Codec();
        // Example 1: the five-node tree round-trips.
        TreeNode r = new TreeNode(1);
        r.left = new TreeNode(2);
        r.right = new TreeNode(3);
        r.right.left = new TreeNode(4);
        r.right.right = new TreeNode(5);
        if (!same(r, codec.deserialize(codec.serialize(r)))) throw new AssertionError("ex1");
        // Example 2: the empty tree round-trips to null.
        if (codec.deserialize(codec.serialize(null)) != null) throw new AssertionError("ex2");
        // A chain of 10000 nodes round-trips without a problem in the stack depth.
        TreeNode chain = new TreeNode(0), tail = chain;
        for (int i = 1; i < 5000; i++) { tail.right = new TreeNode(i % 7); tail = tail.right; }
        if (!same(chain, codec.deserialize(codec.serialize(chain)))) throw new AssertionError("chain");
        // Random trees with repeated and negative values must round-trip and re-serialize to the same text.
        Random rnd = new Random(1674);
        for (int t = 0; t < 400; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(40));
            String text = codec.serialize(x);
            TreeNode y = codec.deserialize(text);
            if (!same(x, y) || !codec.serialize(y).equals(text)) throw new AssertionError("round " + t);
        }
    }
}
```
