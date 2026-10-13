<!-- solutions-for: 92-codec-structural-traversal -->
### Solutions For Codec Structural Traversal

#### Solution: [Build] Length-Prefixed String Codec (Author exercise)
<!-- id: it37-fixed-width-frames -->

**Approach.**
Every string becomes one frame with a header of exactly four lowercase hexadecimal digits that give the string length, followed by the characters. The fixed header width means the decoder never searches for a delimiter. It checks that four header characters remain, converts them to a length, checks that the body fits in the remaining input, and takes the body in one step. The encoder rejects a string longer than 65535 characters, because four digits cannot hold a larger length.

The decoder is strict, so the code is a bijection between lists and valid encodings: an input is accepted exactly when `encode` can produce it. The header check tests each character against the ASCII digits and the letters `a` to `f` by hand. Library parsing is too lenient for this contract. `Integer.parseInt("-001", 16)` accepts a sign, and `Character.digit` accepts digits from other scripts. The invariant is that the read index stands on a frame boundary before each frame, and the decoder throws before it reads past the end.

**Complexity.**
- **Time** is O(total characters) for both directions, since each character is copied once and each header costs four steps.
- **Space** is O(total characters) for the output, with O(1) extra work for the header.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FixedWidthFrames {
    private static final String HEX = "0123456789abcdef";

    /**
     * Encodes each string as four hex digits of length followed by its characters.
     * Time: O(total characters). Space: O(total characters).
     * Invariant: every frame has a header of exactly four characters.
     */
    static String encode(List<String> items) {
        StringBuilder out = new StringBuilder();
        for (String s : items) {
            // Four hex digits hold lengths 0 to 65535; a longer string cannot be framed.
            if (s.length() > 0xFFFF) throw new IllegalArgumentException("string too long");
            int n = s.length();
            // The digits are written from the high nibble to the low nibble.
            for (int shift = 12; shift >= 0; shift -= 4) out.append(HEX.charAt((n >> shift) & 15));
            out.append(s);
        }
        return out.toString();
    }

    /**
     * Decodes the input or throws IllegalArgumentException when it is not a valid encoding.
     * Time: O(total characters). Space: O(total characters).
     * Invariant: i is a frame boundary at the top of every iteration.
     */
    static List<String> decode(String enc) {
        List<String> out = new ArrayList<>();
        int i = 0;
        while (i < enc.length()) {
            // A header needs four characters, and fewer than four remaining means a cut-off input.
            if (enc.length() - i < 4) throw new IllegalArgumentException("truncated header at " + i);
            int len = 0;
            for (int k = 0; k < 4; k++) {
                int d = HEX.indexOf(enc.charAt(i + k));
                // Only the sixteen lowercase digits are valid, so each valid input has one encoder output.
                if (d < 0) throw new IllegalArgumentException("bad header digit at " + (i + k));
                len = len * 16 + d;
            }
            i += 4;
            // The body must fit in what remains; the subtraction cannot overflow.
            if (enc.length() - i < len) throw new IllegalArgumentException("truncated body at " + i);
            out.add(enc.substring(i, i + len));
            i += len;
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: a body may contain the pipe character and digits.
        List<String> first = List.of("hi", "", "a|b");
        if (!encode(first).equals("0002hi00000003a|b")) throw new AssertionError("example 1 encode");
        if (!decode("0002hi00000003a|b").equals(first)) throw new AssertionError("example 1 decode");
        // Example 2: the empty list is the empty string, and cut-off inputs throw.
        if (!encode(List.of()).equals("") || !decode("").isEmpty()) throw new AssertionError("example 2 empty");
        for (String bad : new String[] {"0005ab", "00", "000g", "0001", "0001a0", "0A01a", "+001a", "-001a"}) {
            try {
                decode(bad);
                throw new AssertionError("accepted " + bad);
            } catch (IllegalArgumentException expected) {
                // The exception is the required behavior for each malformed boundary.
            }
        }
        // The library routines that the lesson avoids: parseInt takes a sign and Character.digit takes other scripts.
        if (Integer.parseInt("-001", 16) != -1 || Integer.parseInt("+0ab", 16) != 171) throw new AssertionError("parseInt sign");
        if (Character.digit('１', 16) != 1) throw new AssertionError("fullwidth digit");
        // The frame limit: 65535 characters fit, one more is rejected.
        String big = "x".repeat(0xFFFF);
        if (!decode(encode(List.of(big))).equals(List.of(big)) || !encode(List.of(big)).startsWith("ffff")) {
            throw new AssertionError("largest frame");
        }
        try { encode(List.of(big + "x")); throw new AssertionError("accepted 65536"); } catch (IllegalArgumentException ok) { }
        // Random lists round trip over an alphabet that contains header characters.
        Random rnd = new Random(3791L);
        String alphabet = "0123456789abcdefA|";
        for (int t = 0; t < 20000; t++) {
            List<String> items = new ArrayList<>();
            int k = rnd.nextInt(5);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(6);
                for (int c = 0; c < len; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                items.add(sb.toString());
            }
            if (!decode(encode(items)).equals(items)) throw new AssertionError("round trip " + items);
        }
        // Random strings: the decoder accepts exactly the strings that encode produces from its own output.
        for (int t = 0; t < 60000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(10);
            for (int c = 0; c < len; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            // Bias toward zero headers so that some random strings are valid.
            String s = rnd.nextBoolean() ? "0000".repeat(rnd.nextInt(3)) + sb : sb.toString();
            try {
                List<String> items = decode(s);
                if (!encode(items).equals(s)) throw new AssertionError("accepted a non-canonical input " + s);
            } catch (IllegalArgumentException rejected) {
                // A rejected input is allowed; the check above covers accepted inputs.
            }
        }
    }
}
```

#### Solution: [Vary] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: it37-level-order-codec -->

**Approach.**
The encoder walks the tree level by level with a queue of real nodes. For each dequeued node it writes the left child value or `null`, then the right child value or `null`, and it enqueues the children that exist. The queue never holds `null`, which matters because `ArrayDeque` throws `NullPointerException` on `add(null)`. After the walk the encoder removes the trailing `null` tokens, since the decoder can infer them. The empty tree encodes to the empty string, and a non-empty encoding never starts or ends with `null`.

The decoder repeats the same walk. It creates the root from the first token, and then each dequeued node consumes the next two tokens as its left and right child. A token that is missing because the string ended counts as `null`, which restores the trimmed tokens. The invariant is that the token index always points at the child slot of the oldest node in the queue. The decoder throws `IllegalArgumentException` for a leading or trailing `null` token. It also throws for tokens left over after the queue empties. Every accepted string is then the canonical output of `serialize`.

**Complexity.**
- **Time** is O(n), because each node enters and leaves the queue once and each token is read once.
- **Space** is O(n) for the token list, and the queue holds at most one level of the tree, which is O(w) for width w and at most O(n).

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Random;

public final class LevelOrderCodec {
    static final class TreeNode {
        final int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Writes the tree level by level and trims the trailing null tokens.
     * Time: O(n). Space: O(n) for tokens, O(w) for the queue.
     * Invariant: the queue holds only nodes whose two child slots are still unwritten.
     */
    static String serialize(TreeNode root) {
        if (root == null) return "";
        List<String> tokens = new ArrayList<>();
        Queue<TreeNode> queue = new ArrayDeque<>();
        tokens.add(Integer.toString(root.val));
        queue.add(root);
        // Each dequeued node writes exactly two child slots, in left-then-right order.
        while (!queue.isEmpty()) {
            TreeNode n = queue.poll();
            for (TreeNode c : new TreeNode[] {n.left, n.right}) {
                if (c == null) {
                    tokens.add("null");
                } else {
                    tokens.add(Integer.toString(c.val));
                    // Only real nodes enter the queue, because ArrayDeque rejects null elements.
                    queue.add(c);
                }
            }
        }
        // The decoder treats a missing token as null, so the trailing nulls carry no information.
        int end = tokens.size();
        while (tokens.get(end - 1).equals("null")) end--;
        return String.join(",", tokens.subList(0, end));
    }

    /**
     * Rebuilds the tree and rejects every string that serialize could not have produced.
     * Time: O(n). Space: O(n).
     * Invariant: idx is the next unread token and belongs to the oldest queued node.
     */
    static TreeNode deserialize(String s) {
        if (s.isEmpty()) return null;
        // The limit -1 keeps empty tokens, so a stray comma is rejected as a bad number below.
        String[] tok = s.split(",", -1);
        // A canonical string never begins or ends with null.
        if (tok[0].equals("null") || tok[tok.length - 1].equals("null")) throw new IllegalArgumentException("edge null");
        TreeNode root = new TreeNode(Integer.parseInt(tok[0]));
        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        int idx = 1;
        while (!queue.isEmpty()) {
            TreeNode n = queue.poll();
            // Two slots per node: left first, then right.
            for (int side = 0; side < 2; side++) {
                // A missing token stands for a trimmed null.
                if (idx >= tok.length) continue;
                String t = tok[idx++];
                if (t.equals("null")) continue;
                TreeNode c = new TreeNode(Integer.parseInt(t));
                if (side == 0) n.left = c; else n.right = c;
                queue.add(c);
            }
        }
        // Tokens that no node claimed mean the string was not a tree.
        if (idx < tok.length) throw new IllegalArgumentException("extra tokens");
        return root;
    }

    static TreeNode levelOrder(Integer... a) {
        if (a.length == 0 || a[0] == null) return null;
        TreeNode root = new TreeNode(a[0]);
        Queue<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < a.length) {
            TreeNode n = q.poll();
            if (i < a.length && a[i] != null) { n.left = new TreeNode(a[i]); q.add(n.left); }
            i++;
            if (i < a.length && a[i] != null) { n.right = new TreeNode(a[i]); q.add(n.right); }
            i++;
        }
        return root;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static String shape(TreeNode n) {
        return n == null ? "." : "(" + shape(n.left) + n.val + shape(n.right) + ")";
    }

    static TreeNode randomTree(Random rnd, int budget) {
        if (budget == 0 || rnd.nextInt(4) == 0) return null;
        TreeNode n = new TreeNode(rnd.nextInt(7) - 3);
        int leftBudget = rnd.nextInt(budget);
        n.left = randomTree(rnd, leftBudget);
        n.right = randomTree(rnd, budget - 1 - leftBudget);
        return n;
    }

    public static void main(String[] args) {
        // Example 1: serialize the tree [1,2,3,null,null,4,5].
        if (!serialize(levelOrder(1, 2, 3, null, null, 4, 5)).equals("1,2,3,null,null,4,5")) throw new AssertionError("example 1");
        // The tree [1,null,2,3] writes a trailing null for node 3's right slot and then trims it.
        if (!serialize(levelOrder(1, null, 2, 3)).equals("1,null,2,3")) throw new AssertionError("trimmed tail");
        // Example 2: decode "4,3,null,2", and reject "1,null".
        if (!same(deserialize("4,3,null,2"), levelOrder(4, 3, null, 2))) throw new AssertionError("example 2 decode");
        try { deserialize("1,null"); throw new AssertionError("accepted trailing null"); } catch (IllegalArgumentException ok) { }
        // The empty tree is the empty string, and a lone root is its value.
        if (!serialize(null).equals("") || deserialize("") != null || !serialize(levelOrder(7)).equals("7")) throw new AssertionError("empty and single");
        // The Java detail behind the queue design: ArrayDeque refuses null elements.
        try { new ArrayDeque<TreeNode>().add(null); throw new AssertionError("ArrayDeque took null"); } catch (NullPointerException ok) { }
        // Random trees: round trip, and no two shapes share a string.
        Random rnd = new Random(3792L);
        Map<String, String> seen = new HashMap<>();
        for (int i = 0; i < 20000; i++) {
            TreeNode t = randomTree(rnd, 1 + rnd.nextInt(8));
            String s = serialize(t);
            if (!same(deserialize(s), t)) throw new AssertionError("round trip " + shape(t));
            String prev = seen.put(s, shape(t));
            if (prev != null && !prev.equals(shape(t))) throw new AssertionError("collision " + s);
        }
        // Random strings: whatever the decoder accepts must be the canonical output for that tree.
        String[] pool = {"1", "2", "null", "null", "3"};
        for (int i = 0; i < 60000; i++) {
            int n = rnd.nextInt(8);
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < n; j++) sb.append(j > 0 ? "," : "").append(pool[rnd.nextInt(pool.length)]);
            try {
                TreeNode t = deserialize(sb.toString());
                if (!serialize(t).equals(sb.toString())) throw new AssertionError("non-canonical accepted " + sb);
            } catch (IllegalArgumentException rejected) {
                // Rejection is allowed; accepted strings were checked above.
            }
        }
    }
}
```

#### Solution: [Boundary] Encode N-ary Forest to Binary Tree (LeetCode 431)
<!-- id: it37-forest-to-binary -->

**Approach.**
A forest is a list of sibling roots, so the root list is handled by the same rule as any child list. One helper `encodeChain` takes an ordered list of nodes and returns the head of a right-linked chain. Each chain element gets the value of its node, its left link points to the chain of that node's children, and its right link points to the next element. The forest and every children list use the same helper, so there is no special case for the roots.

The decoder `decodeChain` walks one right chain and produces the list of nodes. It calls itself on the left link of each element for the children. The boundary cases follow from the grammar. An empty forest encodes to `null`, and `null` decodes to an empty list. A single childless root encodes to a node with two `null` links. A decoded node without children owns an empty list. The invariant is that a right chain is always one complete ordered list, and a left link always starts the chain of that node's own children.

**Complexity.**
- **Time** is O(n) for n nodes in the forest, because each node is converted once in each direction.
- **Space** is O(n) for the output, plus O(h) recursion depth for forest height h. A long list of siblings adds loop iterations and no depth.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class ForestToBinary {
    static final class Node {
        final int val;
        final List<Node> children = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static final class TreeNode {
        final int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Converts an ordered list of sibling nodes into a right-linked chain.
     * Time: O(nodes below the list). Space: O(same) output plus O(h) stack.
     * Invariant: the chain order equals the list order, and each left link starts that node's own chain.
     */
    static TreeNode encodeChain(List<Node> nodes) {
        TreeNode head = null, prev = null;
        // One iteration per sibling, in list order.
        for (Node n : nodes) {
            TreeNode t = new TreeNode(n.val);
            // The children of n form the chain on the left link.
            t.left = encodeChain(n.children);
            if (prev == null) head = t; else prev.right = t;
            prev = t;
        }
        return head;
    }

    /**
     * Converts one right chain back to a list of nodes.
     * Time: O(nodes in the chain and below). Space: O(same) output plus O(h) stack.
     * Invariant: every produced node owns an empty or filled children list, never null.
     */
    static List<Node> decodeChain(TreeNode head) {
        List<Node> out = new ArrayList<>();
        // The right links visit the siblings in their original order.
        for (TreeNode t = head; t != null; t = t.right) {
            Node n = new Node(t.val);
            n.children.addAll(decodeChain(t.left));
            out.add(n);
        }
        return out;
    }

    static String text(List<Node> forest) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < forest.size(); i++) {
            Node n = forest.get(i);
            sb.append(i > 0 ? "," : "").append(n.val);
            if (!n.children.isEmpty()) sb.append(text(n.children));
        }
        return sb.append(']').toString();
    }

    static String binary(TreeNode t) {
        return t == null ? "N" : t.val + " " + binary(t.left) + " " + binary(t.right);
    }

    static int size(List<Node> forest) {
        int s = 0;
        for (Node n : forest) s += 1 + size(n.children);
        return s;
    }

    static int size(TreeNode t) { return t == null ? 0 : 1 + size(t.left) + size(t.right); }

    static List<Node> randomForest(Random rnd, int budget) {
        List<Node> out = new ArrayList<>();
        // Each root takes a random share of the budget, so empty forests and long sibling lists both occur.
        while (budget > 0 && rnd.nextInt(5) != 0) {
            int share = 1 + rnd.nextInt(budget);
            Node n = new Node(rnd.nextInt(9) - 4);
            n.children.addAll(randomForest(rnd, share - 1));
            out.add(n);
            budget -= share;
        }
        return out;
    }

    static Node node(int v, Node... kids) {
        Node n = new Node(v);
        for (Node k : kids) n.children.add(k);
        return n;
    }

    public static void main(String[] args) {
        // Example 1: the forest [1[2,3], 4].
        List<Node> f = List.of(node(1, node(2), node(3)), node(4));
        TreeNode e = encodeChain(f);
        if (!binary(e).equals("1 2 N 3 N N 4 N N")) throw new AssertionError("example 1 " + binary(e));
        if (!text(decodeChain(e)).equals(text(f))) throw new AssertionError("example 1 decode");
        // Example 2: two childless roots chain on the right, and the empty forest is null.
        if (!binary(encodeChain(List.of(node(7), node(8)))).equals("7 N 8 N N")) throw new AssertionError("example 2");
        if (encodeChain(List.of()) != null || !decodeChain(null).isEmpty()) throw new AssertionError("empty forest");
        // A single childless root is a node with two null links, and decodes with an empty list.
        TreeNode lone = encodeChain(List.of(node(5)));
        if (lone.left != null || lone.right != null) throw new AssertionError("lone root links");
        List<Node> back = decodeChain(lone);
        if (back.size() != 1 || back.get(0).children == null || !back.get(0).children.isEmpty()) throw new AssertionError("lone root");
        // A one-child chain differs from two roots: 5[6] puts 6 on the left link, 5,6 puts it on the right.
        if (binary(encodeChain(List.of(node(5, node(6))))).equals(binary(encodeChain(List.of(node(5), node(6)))))) {
            throw new AssertionError("child and sibling collide");
        }
        // Random forests: round trip, equal node counts, and one forest per binary shape.
        Random rnd = new Random(3793L);
        Map<String, String> seen = new HashMap<>();
        for (int i = 0; i < 20000; i++) {
            List<Node> forest = randomForest(rnd, rnd.nextInt(10));
            TreeNode enc = encodeChain(forest);
            if (!text(decodeChain(enc)).equals(text(forest))) throw new AssertionError("round trip " + text(forest));
            if (size(enc) != size(forest)) throw new AssertionError("node count");
            String prev = seen.put(binary(enc), text(forest));
            if (prev != null && !prev.equals(text(forest))) throw new AssertionError("collision");
        }
    }
}
```

#### Solution: [Recognize] Serialize and Deserialize BST (LeetCode 449)
<!-- id: it37-bst-postorder-duplicates -->

**Approach.**
Review notes for this transfer prompt come first. The preorder method from the lesson reads the root first and bounds each subtree from above and below. With duplicates the bounds change, and a postorder string reverses the reading direction. Postorder lists the left subtree, then the right subtree, then the root, so the root is the last token. A decoder that reads from the end sees the root, then the right subtree, then the left subtree.

The rule of this exercise puts equal values in the left subtree: left values are at most the node value, and right values are greater. A value `v` belongs to a subtree with range `(lo, hi]` when `lo < v <= hi`. The decoder takes the last unread token as the root of the range. It builds the right subtree first with the range `(value, hi]`, and then the left subtree with the range `(lo, value]`. A token outside the range ends the subtree and stays unread. The split is unique, because left values are at most the root and right values are above it, so the right subtree always occupies the tokens just before the root. Leftover tokens after the root call mean the string is not a valid postorder, and the decoder throws.

The brute-force check inserts the reversed sequence into an ordinary tree that sends equal values left. Reversed postorder visits each parent before its descendants, so the insertion rebuilds the same tree. The sequence is valid exactly when the postorder of that tree equals the sequence.

**Complexity.**
- **Time** is O(n), because each token is parsed once and each call either consumes one token or returns at once.
- **Space** is O(n) for the parsed values and O(h) for the recursion, where h is the height of the tree.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class BstPostorderDuplicates {
    static final class TreeNode {
        final int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Writes the values in postorder, separated by commas; the empty tree gives "".
     * Time: O(n). Space: O(n) output plus O(h) stack.
     * Invariant: one token per node, and the root of each subtree is its last token.
     */
    static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        write(root, sb);
        return sb.toString();
    }

    private static void write(TreeNode n, StringBuilder sb) {
        // Children first, then the node itself, so the root ends the string.
        if (n == null) return;
        write(n.left, sb);
        write(n.right, sb);
        if (sb.length() > 0) sb.append(',');
        sb.append(n.val);
    }

    /** Holds the parsed values and the shared read position, which moves from the end toward the start. */
    private static final class Reader {
        final int[] vals;
        int pos;
        Reader(int[] vals) { this.vals = vals; this.pos = vals.length - 1; }
    }

    /**
     * Rebuilds the tree from the end of the string and rejects strings that are not a valid postorder.
     * Time: O(n). Space: O(n) values plus O(h) stack.
     * Invariant: build(lo, hi) consumes exactly the trailing tokens that lie in (lo, hi] and form one subtree.
     */
    static TreeNode deserialize(String s) {
        if (s.isEmpty()) return null;
        String[] parts = s.split(",", -1);
        int[] vals = new int[parts.length];
        // Each token is parsed once; a bad token throws NumberFormatException, an IllegalArgumentException.
        for (int i = 0; i < parts.length; i++) vals[i] = Integer.parseInt(parts[i]);
        Reader r = new Reader(vals);
        TreeNode root = build(r, Long.MIN_VALUE, Long.MAX_VALUE);
        // Unread tokens at the front belong to no subtree.
        if (r.pos != -1) throw new IllegalArgumentException("leftover tokens");
        return root;
    }

    private static TreeNode build(Reader r, long lo, long hi) {
        // A token outside (lo, hi] belongs to an ancestor's other side, so this subtree ends here.
        if (r.pos < 0 || r.vals[r.pos] <= lo || r.vals[r.pos] > hi) return null;
        TreeNode n = new TreeNode(r.vals[r.pos--]);
        // Reading backward sees the right subtree before the left one; equal values go left.
        n.right = build(r, n.val, hi);
        n.left = build(r, lo, n.val);
        return n;
    }

    // Insertion that sends equal values to the left.
    static TreeNode insert(TreeNode root, int v) {
        if (root == null) return new TreeNode(v);
        if (v <= root.val) root.left = insert(root.left, v); else root.right = insert(root.right, v);
        return root;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static String join(List<Integer> seq) {
        StringBuilder sb = new StringBuilder();
        for (int v : seq) sb.append(sb.length() > 0 ? "," : "").append(v);
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: root 5 with duplicates 3 and 3 on the left side.
        TreeNode t = null;
        for (int v : new int[] {5, 3, 8, 3, 4, 9}) t = insert(t, v);
        if (!serialize(t).equals("3,4,3,9,8,5")) throw new AssertionError("example 1 " + serialize(t));
        if (!same(deserialize("3,4,3,9,8,5"), t)) throw new AssertionError("example 1 decode");
        // Example 2: three equal values form a left chain, and "3,6,2,5" is rejected.
        TreeNode chain = deserialize("3,3,3");
        if (chain.left == null || chain.left.left == null || chain.right != null || chain.left.right != null) {
            throw new AssertionError("equal chain");
        }
        try { deserialize("3,6,2,5"); throw new AssertionError("accepted invalid"); } catch (IllegalArgumentException ok) { }
        // The empty tree and the extreme int values behave under the long bounds.
        if (!serialize(null).equals("") || deserialize("") != null) throw new AssertionError("empty");
        TreeNode ext = null;
        for (int v : new int[] {0, Integer.MIN_VALUE, Integer.MAX_VALUE, Integer.MIN_VALUE}) ext = insert(ext, v);
        if (!same(deserialize(serialize(ext)), ext)) throw new AssertionError("extremes");
        // Random trees with many duplicates: round trip.
        Random rnd = new Random(3794L);
        for (int i = 0; i < 20000; i++) {
            TreeNode tree = null;
            int n = rnd.nextInt(9);
            for (int j = 0; j < n; j++) tree = insert(tree, rnd.nextInt(5));
            if (!same(deserialize(serialize(tree)), tree)) throw new AssertionError("round trip " + serialize(tree));
        }
        // Brute force: reverse the sequence, insert it, and compare the postorder with the sequence.
        for (int i = 0; i < 60000; i++) {
            int n = 1 + rnd.nextInt(7);
            List<Integer> seq = new ArrayList<>();
            for (int j = 0; j < n; j++) seq.add(rnd.nextInt(5));
            TreeNode ref = null;
            for (int j = n - 1; j >= 0; j--) ref = insert(ref, seq.get(j));
            boolean valid = serialize(ref).equals(join(seq));
            boolean accepted;
            try { deserialize(join(seq)); accepted = true; } catch (IllegalArgumentException e) { accepted = false; }
            if (valid != accepted) throw new AssertionError("validity of " + join(seq));
        }
    }
}
```
