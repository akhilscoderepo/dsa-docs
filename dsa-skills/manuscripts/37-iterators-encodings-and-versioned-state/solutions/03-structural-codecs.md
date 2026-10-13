<!-- solutions-for: 03-structural-codecs -->
### Solutions For Structural Codecs

#### Solution: [Build] Encode and Decode Strings (LeetCode 271)
<!-- id: it37-string-framing -->

**Approach.**
Each string becomes one frame: its length in decimal digits, one `#`, and then its characters. The decoder reads digits up to the first `#`, converts them to a length `len`, and takes exactly `len` characters. The characters inside the frame are never inspected, so a `#`, a digit or a comma inside a string cannot change where the frame ends. After the frame the decoder stands at the first digit of the next frame, or at the end of the input.

The invariant is that the read index sits on a frame boundary before every step and on a frame boundary again after it. The empty list encodes to the empty string, and a list that holds one empty string encodes to `0#`, so the two inputs stay apart. The method `count` follows the same headers but jumps over the characters with an index addition, so it never copies them.

**Complexity.**
- **Time** of `encode` and `decode` is O(total characters), because every output or input character is appended or copied once. The time of `count` is O(k + total header digits) for k strings, since it skips each body in one addition.
- **Space** is O(total characters) for the encoded string or the decoded list. The method `count` uses O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class StringFraming {
    /**
     * Encodes the strings as length, '#', characters, one frame after another.
     * Time: O(total characters). Space: O(total characters).
     * Invariant: the output is a concatenation of complete frames.
     */
    static String encode(List<String> items) {
        StringBuilder out = new StringBuilder();
        // Each string appends its header and its body once, so the cost equals the output size.
        for (String s : items) out.append(s.length()).append('#').append(s);
        return out.toString();
    }

    /**
     * Reads the header that starts at index i and returns {length, index of the first body character}.
     * Time: O(digits). Space: O(1).
     * Invariant: i is the first digit of a frame.
     */
    private static int[] readHeader(String enc, int i) {
        int len = 0;
        // Digits accumulate until the first '#', which only a header can contain at this position.
        while (enc.charAt(i) != '#') {
            len = len * 10 + (enc.charAt(i) - '0');
            i++;
        }
        // The returned index skips the '#'.
        return new int[] {len, i + 1};
    }

    /**
     * Rebuilds the list by taking exactly len characters per frame.
     * Time: O(total characters). Space: O(total characters).
     * Invariant: i is a frame boundary before and after every iteration.
     */
    static List<String> decode(String enc) {
        List<String> out = new ArrayList<>();
        int i = 0;
        // One iteration consumes one complete frame.
        while (i < enc.length()) {
            int[] h = readHeader(enc, i);
            out.add(enc.substring(h[1], h[1] + h[0]));
            i = h[1] + h[0];
        }
        return out;
    }

    /**
     * Counts the frames without copying any body.
     * Time: O(k + header digits). Space: O(1) besides the small header array.
     * Invariant: i is a frame boundary before and after every iteration.
     */
    static int count(String enc) {
        int k = 0, i = 0;
        while (i < enc.length()) {
            int[] h = readHeader(enc, i);
            // The body is skipped with one addition, so its length does not matter.
            i = h[1] + h[0];
            k++;
        }
        return k;
    }

    public static void main(String[] args) {
        // Example 1: a body that contains '#' and a digit stays inside its frame.
        List<String> first = List.of("ab", "", "c#d");
        if (!encode(first).equals("2#ab0#3#c#d")) throw new AssertionError("example 1 encode");
        if (!decode("2#ab0#3#c#d").equals(first) || count("2#ab0#3#c#d") != 3) throw new AssertionError("example 1 decode");
        // Example 2: the empty list and the list of one empty string stay different.
        if (!encode(List.of()).equals("") || !encode(List.of("")).equals("0#")) throw new AssertionError("example 2 encode");
        if (count("") != 0 || count("0#") != 1 || !decode("0#").equals(List.of(""))) throw new AssertionError("example 2 decode");
        // A multi-digit length parses as one number.
        String twelve = "abcdefghijkl";
        if (!decode(encode(List.of(twelve, "z"))).equals(List.of(twelve, "z"))) throw new AssertionError("multi-digit length");
        // The fragile delimiter design from the lesson: split drops trailing empty strings.
        if ("x,".split(",").length != 1) throw new AssertionError("split drops trailing empties");
        // An empty input string splits into one empty string, so [] and [""] collide under join and split.
        if ("".split(",").length != 1 || !String.join(",", List.of()).equals(String.join(",", List.of("")))) {
            throw new AssertionError("join collision");
        }
        // Random lists over an alphabet that includes the frame characters themselves.
        Random rnd = new Random(3701L);
        String alphabet = "#0123456789a,";
        java.util.Map<String, List<String>> seen = new java.util.HashMap<>();
        for (int t = 0; t < 20000; t++) {
            List<String> items = new ArrayList<>();
            int k = rnd.nextInt(5);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(5);
                for (int c = 0; c < len; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                items.add(sb.toString());
            }
            String enc = encode(items);
            // Round trip and count must both recover the input.
            if (!decode(enc).equals(items)) throw new AssertionError("round trip " + items);
            if (count(enc) != items.size()) throw new AssertionError("count " + items);
            // Injectivity: one encoding never belongs to two different lists.
            List<String> prev = seen.put(enc, items);
            if (prev != null && !prev.equals(items)) throw new AssertionError("collision " + enc);
        }
    }
}
```

#### Solution: [Vary] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: it37-binary-tree-nulls -->

**Approach.**
The encoder writes the tree in preorder. A real node writes its value and then its left and right subtrees. A missing child writes the marker `N`. Tokens are separated by single spaces. The grammar is `tree = N | value tree tree`. Every encoding starts with a complete tree, and the number of `N` tokens is one more than the number of nodes.

The decoder follows the same grammar with a shared position in the token array. One call reads one token. A marker returns `null`. A value creates a node and then makes two calls for the two children. When the first call returns, the position stands after exactly one complete tree. The contract requires the whole string to be one tree. The decoder throws `IllegalArgumentException` when the tokens run out too early or when tokens remain after the root call returns.

**Complexity.**
- **Time** is O(n) for n nodes, because the encoder and the decoder visit each node and each marker once, and the string builder appends in amortized constant time.
- **Space** is O(n) for the string and the token array, plus O(h) call-stack depth for a tree of height h.

```java run
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import java.util.Random;

public final class BinaryTreeNulls {
    static final class TreeNode {
        final int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Writes the tree in preorder with N for each missing child.
     * Time: O(n). Space: O(n) output plus O(h) stack.
     * Invariant: each call appends the tokens of exactly one subtree.
     */
    static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        write(root, sb);
        return sb.toString();
    }

    private static void write(TreeNode node, StringBuilder sb) {
        // A separator goes before every token except the first.
        if (sb.length() > 0) sb.append(' ');
        // A missing child is a complete subtree of one token.
        if (node == null) { sb.append('N'); return; }
        sb.append(node.val);
        write(node.left, sb);
        write(node.right, sb);
    }

    /** Holds the token array and the one shared read position. */
    private static final class Reader {
        final String[] tokens;
        int pos;
        Reader(String[] tokens) { this.tokens = tokens; }
    }

    /**
     * Rebuilds the tree and rejects any string that is not exactly one tree.
     * Time: O(n). Space: O(n) tokens plus O(h) stack.
     * Invariant: after each read call the position stands after one complete subtree.
     */
    static TreeNode deserialize(String s) {
        // The limit -1 keeps trailing empty tokens, so a trailing space is detected as malformed.
        Reader r = new Reader(s.split(" ", -1));
        TreeNode root = read(r);
        // Leftover tokens mean the string held more than one tree.
        if (r.pos != r.tokens.length) throw new IllegalArgumentException("extra tokens");
        return root;
    }

    private static TreeNode read(Reader r) {
        // Running out of tokens in the middle of a subtree is malformed input.
        if (r.pos >= r.tokens.length) throw new IllegalArgumentException("truncated");
        String t = r.tokens[r.pos++];
        if (t.equals("N")) return null;
        // parseInt throws NumberFormatException, a subclass of IllegalArgumentException, for a bad token.
        TreeNode node = new TreeNode(Integer.parseInt(t));
        node.left = read(r);
        node.right = read(r);
        return node;
    }

    // Builds a tree from a level-order array in which null marks a missing child.
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

    // Oracle shape string: nested parentheses, independent of the token format.
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
        // Example 1: the level-order tree [1,2,3,null,null,4,5].
        TreeNode t = levelOrder(1, 2, 3, null, null, 4, 5);
        if (!serialize(t).equals("1 2 N N 3 4 N N 5 N N")) throw new AssertionError("example 1");
        if (!same(deserialize("1 2 N N 3 4 N N 5 N N"), t)) throw new AssertionError("example 1 decode");
        // Example 2: the empty tree is the single token N, and extra tokens are rejected.
        if (!serialize(null).equals("N") || deserialize("N") != null) throw new AssertionError("example 2 empty");
        for (String bad : new String[] {"1 N N N", "1 N", "", "1 N N ", "x N N", "1  N N"}) {
            try {
                deserialize(bad);
                throw new AssertionError("accepted " + bad);
            } catch (IllegalArgumentException expected) {
                // The exception is the required behavior for a string that is not exactly one tree.
            }
        }
        // The Java detail behind the limit -1: the default split drops trailing empty tokens.
        if ("1 N N ".split(" ").length != 3 || "1 N N ".split(" ", -1).length != 4) throw new AssertionError("split limit");
        // A negative value and a large value survive the round trip.
        TreeNode wide = levelOrder(-2147483648, 2147483647);
        if (!same(deserialize(serialize(wide)), wide)) throw new AssertionError("int extremes");
        // Random trees: the round trip recovers the shape, and distinct shapes never share a string.
        Random rnd = new Random(3702L);
        Map<String, String> seen = new HashMap<>();
        for (int i = 0; i < 20000; i++) {
            TreeNode tree = randomTree(rnd, 1 + rnd.nextInt(8));
            String s = serialize(tree);
            TreeNode back = deserialize(s);
            if (!same(back, tree)) throw new AssertionError("round trip " + shape(tree));
            // The token count is 2n + 1 for n nodes, which is the grammar's counting rule.
            int n = countNodes(tree);
            if (s.split(" ").length != 2 * n + 1) throw new AssertionError("token count");
            String prev = seen.put(s, shape(tree));
            if (prev != null && !prev.equals(shape(tree))) throw new AssertionError("collision " + s);
        }
        // Malformed mutations: dropping or adding a token always throws.
        for (int i = 0; i < 5000; i++) {
            String s = serialize(randomTree(rnd, 1 + rnd.nextInt(8)));
            String dropped = s.contains(" ") ? s.substring(0, s.lastIndexOf(' ')) : "";
            try { deserialize(dropped); throw new AssertionError("accepted truncation " + s); } catch (IllegalArgumentException ok) { }
            try { deserialize(s + " N"); throw new AssertionError("accepted extension " + s); } catch (IllegalArgumentException ok) { }
        }
    }

    static int countNodes(TreeNode n) { return n == null ? 0 : 1 + countNodes(n.left) + countNodes(n.right); }
}
```

#### Solution: [Boundary] Encode N-ary Tree to Binary Tree (LeetCode 431)
<!-- id: it37-nary-to-binary -->

**Approach.**
The mapping gives each binary node two roles. The left link points to the first child of the original node, and the right link points to the next sibling of the original node. The encoder creates the binary node of each child and links the children in order. The first child hangs on the left of the parent, and every later child hangs on the right of its previous sibling. A node without children keeps a `null` left link, and the root has a `null` right link because the root has no sibling.

The decoder reverses the roles. For a binary node it starts at the left link and follows right links, so it visits the children in their original order and decodes each one. A binary node with no left link decodes to a node with an empty children list, never a `null` list. The invariant is that the right chain below a left link holds exactly the ordered children of one parent, and no other node.

**Complexity.**
- **Time** is O(n) for n nodes, because both directions create or visit each node once.
- **Space** is O(n) for the new tree, plus O(h) recursion depth where h is the height of the N-ary tree. A parent with many children adds loop iterations and no recursion depth, since siblings are linked in a loop.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class NaryToBinary {
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
     * Encodes with left = first child and right = next sibling.
     * Time: O(n). Space: O(n) output plus O(h) stack.
     * Invariant: the returned node has a null right link until its caller attaches it as a sibling.
     */
    static TreeNode encode(Node root) {
        // An absent tree encodes to an absent tree.
        if (root == null) return null;
        TreeNode t = new TreeNode(root.val);
        TreeNode prev = null;
        // The loop visits the children in list order, so sibling order is the order of the right links.
        for (Node c : root.children) {
            TreeNode e = encode(c);
            // The first child hangs on the left of the parent; each later child hangs on its previous sibling.
            if (prev == null) t.left = e; else prev.right = e;
            prev = e;
        }
        return t;
    }

    /**
     * Decodes by walking the right chain below each left link.
     * Time: O(n). Space: O(n) output plus O(h) stack.
     * Invariant: every produced node owns a non-null, possibly empty, children list.
     */
    static Node decode(TreeNode t) {
        if (t == null) return null;
        Node n = new Node(t.val);
        // The first child is the left link; the others follow along right links.
        for (TreeNode c = t.left; c != null; c = c.right) n.children.add(decode(c));
        return n;
    }

    // Canonical text of an N-ary tree: value, then children in brackets.
    static String text(Node n) {
        if (n == null) return "null";
        StringBuilder sb = new StringBuilder().append(n.val);
        if (!n.children.isEmpty()) {
            sb.append('[');
            for (int i = 0; i < n.children.size(); i++) sb.append(i > 0 ? "," : "").append(text(n.children.get(i)));
            sb.append(']');
        }
        return sb.toString();
    }

    // Preorder text of the binary tree, with N for a missing link.
    static String binary(TreeNode t) {
        if (t == null) return "N";
        return t.val + " " + binary(t.left) + " " + binary(t.right);
    }

    static int size(Node n) {
        int s = 1;
        for (Node c : n.children) s += size(c);
        return s;
    }

    static int size(TreeNode t) { return t == null ? 0 : 1 + size(t.left) + size(t.right); }

    static Node randomTree(Random rnd, int budget) {
        Node n = new Node(rnd.nextInt(9) - 4);
        int left = budget - 1;
        // Each child takes a random share of the remaining budget, so empty and wide lists both occur.
        while (left > 0 && rnd.nextInt(5) != 0) {
            int share = 1 + rnd.nextInt(left);
            n.children.add(randomTree(rnd, share));
            left -= share;
        }
        return n;
    }

    static Node parent(int v, Node... kids) {
        Node n = new Node(v);
        for (Node k : kids) n.children.add(k);
        return n;
    }

    public static void main(String[] args) {
        // Example 1: 1[3[5,6],2,4].
        Node tree = parent(1, parent(3, new Node(5), new Node(6)), new Node(2), new Node(4));
        TreeNode enc = encode(tree);
        if (!binary(enc).equals("1 3 5 N 6 N N 2 N 4 N N N")) throw new AssertionError("example 1 " + binary(enc));
        if (!text(decode(enc)).equals("1[3[5,6],2,4]")) throw new AssertionError("example 1 decode");
        // Example 2: a lone root, and the absent tree.
        if (!binary(encode(new Node(7))).equals("7 N N") || encode(null) != null || decode(null) != null) {
            throw new AssertionError("example 2");
        }
        // A childless node decodes to an empty list and not to null.
        Node leaf = decode(encode(new Node(7)));
        if (leaf.children == null || !leaf.children.isEmpty()) throw new AssertionError("empty list");
        // Random trees: round trip, no right link on the root, same node count, injective binary form.
        Random rnd = new Random(3703L);
        java.util.Map<String, String> seen = new java.util.HashMap<>();
        for (int i = 0; i < 20000; i++) {
            Node t = randomTree(rnd, 1 + rnd.nextInt(9));
            TreeNode e = encode(t);
            if (!text(decode(e)).equals(text(t))) throw new AssertionError("round trip " + text(t));
            if (e.right != null) throw new AssertionError("root has a right link");
            if (size(e) != size(t)) throw new AssertionError("node count");
            String prev = seen.put(binary(e), text(t));
            if (prev != null && !prev.equals(text(t))) throw new AssertionError("collision");
        }
    }
}
```

#### Solution: [Recognize] Serialize and Deserialize BST (LeetCode 449)
<!-- id: it37-bst-preorder-bounds -->

**Approach.**
This is a transfer prompt, so the review notes come first. A general tree needs a marker for every missing child because values alone do not say where a subtree ends. A binary search tree has a second source of boundaries: every value in a subtree lies in an open range that the ancestors set. The encoder can therefore write plain preorder values with no markers, and the string holds exactly one token per node.

The decoder keeps a read position and two bounds. The call `build(lo, hi)` looks at the next token. If the token is missing or lies outside `(lo, hi)`, the token belongs to some ancestor's other subtree, so the call returns `null` and leaves the position alone. Otherwise the token becomes a node. The left subtree uses the range `(lo, value)` and the right subtree uses `(value, hi)`. The bounds are `long`, so the stored values `Integer.MIN_VALUE` and `Integer.MAX_VALUE` still fit strictly inside them.

A valid string is consumed completely by the root call. The decoder throws `IllegalArgumentException` when tokens remain, because such a string is not the preorder of any tree with distinct values. The brute-force check inserts the numbers of a candidate sequence into an ordinary BST and accepts the sequence exactly when the resulting preorder equals the candidate.

**Complexity.**
- **Time** is O(n), because each token is parsed once and each call either consumes one token or returns at once.
- **Space** is O(n) for the token array and O(h) for the recursion, where h is the height of the tree.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class BstPreorderBounds {
    static final class TreeNode {
        final int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Writes the values in preorder, separated by single spaces; an empty tree gives "".
     * Time: O(n). Space: O(n) output plus O(h) stack.
     * Invariant: one token per node and no marker.
     */
    static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        write(root, sb);
        return sb.toString();
    }

    private static void write(TreeNode n, StringBuilder sb) {
        // A missing child writes nothing; the value ranges mark its place.
        if (n == null) return;
        if (sb.length() > 0) sb.append(' ');
        sb.append(n.val);
        write(n.left, sb);
        write(n.right, sb);
    }

    /** Holds the parsed values and the shared read position. */
    private static final class Reader {
        final int[] vals;
        int pos;
        Reader(int[] vals) { this.vals = vals; }
    }

    /**
     * Rebuilds the tree from preorder values and rejects strings that are not a BST preorder.
     * Time: O(n). Space: O(n) for the values plus O(h) stack.
     * Invariant: build(lo, hi) consumes exactly the tokens that lie in (lo, hi) and form one subtree.
     */
    static TreeNode deserialize(String s) {
        if (s.isEmpty()) return null;
        String[] parts = s.split(" ", -1);
        int[] vals = new int[parts.length];
        // Each token parses once; a bad token throws NumberFormatException, an IllegalArgumentException.
        for (int i = 0; i < parts.length; i++) vals[i] = Integer.parseInt(parts[i]);
        Reader r = new Reader(vals);
        TreeNode root = build(r, Long.MIN_VALUE, Long.MAX_VALUE);
        // A leftover token has no place in the tree that the earlier tokens built.
        if (r.pos != vals.length) throw new IllegalArgumentException("leftover tokens");
        return root;
    }

    private static TreeNode build(Reader r, long lo, long hi) {
        // A token outside the open range belongs to an ancestor's other side, so this subtree ends here.
        if (r.pos == r.vals.length || r.vals[r.pos] <= lo || r.vals[r.pos] >= hi) return null;
        TreeNode n = new TreeNode(r.vals[r.pos++]);
        n.left = build(r, lo, n.val);
        n.right = build(r, n.val, hi);
        return n;
    }

    // Plain BST insertion, used to build test trees and as the brute-force oracle.
    static TreeNode insert(TreeNode root, int v) {
        if (root == null) return new TreeNode(v);
        if (v < root.val) root.left = insert(root.left, v); else root.right = insert(root.right, v);
        return root;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static int count(TreeNode n) { return n == null ? 0 : 1 + count(n.left) + count(n.right); }

    public static void main(String[] args) {
        // Example 1: the BST with root 5, left subtree 3(1,4) and right subtree 8(null,9).
        TreeNode t = null;
        for (int v : new int[] {5, 3, 8, 1, 4, 9}) t = insert(t, v);
        if (!serialize(t).equals("5 3 1 4 8 9")) throw new AssertionError("example 1");
        if (!same(deserialize("5 3 1 4 8 9"), t)) throw new AssertionError("example 1 decode");
        // Example 2: a sequence that no BST produces as a preorder.
        try {
            deserialize("5 3 7 4");
            throw new AssertionError("accepted a bad preorder");
        } catch (IllegalArgumentException expected) {
            // The leftover token 4 is the required failure.
        }
        // The empty tree is the empty string, and the extreme int values survive the long bounds.
        if (!serialize(null).equals("") || deserialize("") != null) throw new AssertionError("empty");
        TreeNode ext = null;
        for (int v : new int[] {0, Integer.MIN_VALUE, Integer.MAX_VALUE}) ext = insert(ext, v);
        if (!same(deserialize(serialize(ext)), ext)) throw new AssertionError("extremes");
        // Random BSTs: round trip, and exactly one token per node.
        Random rnd = new Random(3704L);
        for (int i = 0; i < 20000; i++) {
            Set<Integer> used = new HashSet<>();
            TreeNode tree = null;
            int n = rnd.nextInt(9);
            while (used.size() < n) {
                int v = rnd.nextInt(30) - 10;
                if (used.add(v)) tree = insert(tree, v);
            }
            String s = serialize(tree);
            if (!same(deserialize(s), tree)) throw new AssertionError("round trip " + s);
            int tokens = s.isEmpty() ? 0 : s.split(" ").length;
            if (tokens != count(tree)) throw new AssertionError("token count");
        }
        // Brute force: a sequence is valid exactly when inserting it into a BST reproduces it as a preorder.
        for (int i = 0; i < 30000; i++) {
            int n = 1 + rnd.nextInt(6);
            Set<Integer> used = new HashSet<>();
            List<Integer> seq = new ArrayList<>();
            while (seq.size() < n) {
                int v = rnd.nextInt(8);
                if (used.add(v)) seq.add(v);
            }
            TreeNode ref = null;
            for (int v : seq) ref = insert(ref, v);
            StringBuilder sb = new StringBuilder();
            for (int v : seq) sb.append(sb.length() > 0 ? " " : "").append(v);
            boolean valid = serialize(ref).equals(sb.toString());
            boolean accepted;
            try { deserialize(sb.toString()); accepted = true; } catch (IllegalArgumentException e) { accepted = false; }
            if (valid != accepted) throw new AssertionError("validity of " + sb);
        }
    }
}
```
