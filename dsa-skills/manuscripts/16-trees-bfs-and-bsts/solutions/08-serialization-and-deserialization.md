<!-- solutions-for: 08-serialization-and-deserialization -->
### Serialization And Deserialization

#### Solution: [Build] Preorder With Null Markers (Author exercise)
<!-- id: tb-preorder-null-markers -->

**Approach.** Write the weight, then the whole left hanging, then the whole right hanging, and write `#` for every empty hanging, which includes the two empty places under each leaf. The text has exactly 2n + 1 tokens for n weights. The oracle avoids recursion: it keeps an explicit stack, pops an entry, writes `#` for an empty one or the weight for a real one, and pushes the right child before the left so that the left is popped first. The assertions compare the strings on random trees, count the tokens, and check both examples.

**Complexity.** O(n) time and O(n) output, with O(h) recursion depth.

```java run
import java.util.*;

public final class PreorderMarkersRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static String serialize(Node root) {
        StringBuilder card = new StringBuilder();
        write(root, card);
        card.setLength(card.length() - 1);
        return card.toString();
    }

    static void write(Node node, StringBuilder card) {
        if (node == null) { card.append("#,"); return; }
        card.append(node.val).append(',');
        write(node.left, card);
        write(node.right, card);
    }

    static String viaStack(Node root) {
        List<String> tokens = new ArrayList<>();
        ArrayList<Node> stack = new ArrayList<>();
        stack.add(root);
        while (!stack.isEmpty()) {
            Node n = stack.remove(stack.size() - 1);
            if (n == null) { tokens.add("#"); continue; }
            tokens.add(String.valueOf(n.val));
            stack.add(n.right);
            stack.add(n.left);
        }
        return String.join(",", tokens);
    }

    public static void main(String[] args) {
        if (!serialize(build(new Integer[] {1, 2, 3, null, null, 4, 5})).equals("1,2,#,#,3,4,#,#,5,#,#")) throw new AssertionError("example 1");
        if (!serialize(build(new Integer[] {1, null, 2})).equals("1,#,2,#,#")) throw new AssertionError("example 2");
        Random rnd = new Random(16801);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 20, 0, 1000);
            String got = serialize(build(v));
            if (!got.equals(viaStack(build(v)))) throw new AssertionError("differs on " + Arrays.toString(v));
            int n = 0;
            for (Integer x : v) if (x != null) n++;
            if (got.split(",").length != 2 * n + 1) throw new AssertionError("token count should be 2n+1");
        }
    }
}
```

#### Solution: [Vary] Recursive Decoder (Author exercise)
<!-- id: tb-recursive-decoder -->

**Approach.** Read one token. A marker returns null, and a number creates a node whose left child is read by one recursive call and whose right child by the next, with a single shared cursor advanced once per token, so the right call begins exactly where the left call stopped. The oracle is an explicit-stack decoder that keeps a list of open slots and fills the most recent one with each token. Level-order arrays from random trees are compared by the assertions, check that re-encoding gives the original text back, and show with a short list demonstration that `ArrayList.remove(0)` shifts the remaining items, which is why a moving index is used.

**Complexity.** O(n) time and O(h) recursion depth.

```java run
import java.util.*;

public final class DecoderRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Node decode(String text) {
        String[] tokens = text.split(",");
        int[] cursor = {0};
        return read(tokens, cursor);
    }

    static Node read(String[] tokens, int[] cursor) {
        String token = tokens[cursor[0]++];
        if (token.equals("#")) return null;
        Node node = new Node(Integer.parseInt(token));
        node.left = read(tokens, cursor);
        node.right = read(tokens, cursor);
        return node;
    }

    static Node viaOpenSlots(String text) {
        String[] tokens = text.split(",");
        if (tokens[0].equals("#")) return null;
        Node root = new Node(Integer.parseInt(tokens[0]));
        ArrayList<Node> parents = new ArrayList<>();
        ArrayList<Boolean> wantsLeft = new ArrayList<>();
        parents.add(root);
        wantsLeft.add(true);
        for (int i = 1; i < tokens.length; i++) {
            int top = parents.size() - 1;
            Node parent = parents.get(top);
            boolean left = wantsLeft.get(top);
            Node made = tokens[i].equals("#") ? null : new Node(Integer.parseInt(tokens[i]));
            if (left) { parent.left = made; wantsLeft.set(top, false); }
            else { parent.right = made; parents.remove(top); wantsLeft.remove(top); }
            if (made != null) { parents.add(made); wantsLeft.add(true); }
        }
        return root;
    }

    static String encode(Node n) {
        if (n == null) return "#";
        return n.val + "," + encode(n.left) + "," + encode(n.right);
    }

    public static void main(String[] args) {
        if (!Arrays.toString(levels(decode("1,2,#,#,3,4,#,#,5,#,#"))).equals("[1, 2, 3, null, null, 4, 5]")) throw new AssertionError("example 1");
        if (!Arrays.toString(levels(decode("1,#,2,#,#"))).equals("[1, null, 2]")) throw new AssertionError("example 2");
        if (decode("#") != null) throw new AssertionError("a lone marker is the empty tree");
        ArrayList<String> demo = new ArrayList<>(List.of("a", "b", "c"));
        demo.remove(0);
        if (!demo.toString().equals("[b, c]")) throw new AssertionError("remove(0) shifts the rest forward");
        Random rnd = new Random(16802);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 20, 0, 1000);
            String text = encode(build(v));
            if (!Arrays.equals(levels(decode(text)), levels(viaOpenSlots(text)))) throw new AssertionError("decoders differ on " + text);
            if (!Arrays.equals(levels(decode(text)), v)) throw new AssertionError("array changed on " + text);
            if (!encode(decode(text)).equals(text)) throw new AssertionError("re-encoding differs");
        }
    }
}
```

#### Solution: [Boundary] Empty, Negative, And Multi-Digit Values (Author exercise)
<!-- id: tb-codec-edge-values -->

**Approach.** A comma separates tokens and the lone character `#` marks emptiness, so neither can be mistaken for part of a number, and an empty tree is written as the single token `#`. Tokens are parsed with `Integer.parseInt`, which accepts a leading minus sign and the full 32-bit range. The assertions show why the delimiter matters: without it, two different trees give the same string, and with it they differ. Trees whose weights are drawn from the extremes, negative values and long numbers are encoded and decoded again and must be unchanged, and the empty tree is checked separately.

**Complexity.** O(n) time and O(n) output.

```java run
import java.util.*;

public final class CodecEdgesRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static final int[] TABLE = {Integer.MIN_VALUE, -1000000, -10, -1, 0, 7, 12345, Integer.MAX_VALUE};

    static String encode(Node n) {
        if (n == null) return "#";
        return n.val + "," + encode(n.left) + "," + encode(n.right);
    }

    static Node decode(String text) {
        String[] tokens = text.split(",");
        int[] cursor = {0};
        return read(tokens, cursor);
    }

    static Node read(String[] tokens, int[] cursor) {
        String token = tokens[cursor[0]++];
        if (token.equals("#")) return null;
        Node node = new Node(Integer.parseInt(token));
        node.left = read(tokens, cursor);
        node.right = read(tokens, cursor);
        return node;
    }

    static String withoutDelimiter(Node n) {
        if (n == null) return "#";
        return n.val + withoutDelimiter(n.left) + withoutDelimiter(n.right);
    }

    public static void main(String[] args) {
        if (!encode(build(new Integer[] {})).equals("#")) throw new AssertionError("example 1");
        if (!encode(build(new Integer[] {-10, null, 2000000000})).equals("-10,#,2000000000,#,#")) throw new AssertionError("example 2");
        Node a = build(new Integer[] {1, 12});
        Node b = build(new Integer[] {11, 2});
        if (!withoutDelimiter(a).equals(withoutDelimiter(b))) throw new AssertionError("without a delimiter these trees should collide");
        if (encode(a).equals(encode(b))) throw new AssertionError("with a delimiter they must differ");
        if (decode("#") != null) throw new AssertionError("empty round trip");
        if (Integer.parseInt("-2147483648") != Integer.MIN_VALUE) throw new AssertionError("parseInt handles the minimum");
        Random rnd = new Random(16803);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 14, 0, 7);
            for (int i = 0; i < v.length; i++) if (v[i] != null) v[i] = TABLE[v[i]];
            String text = encode(build(v));
            if (!Arrays.equals(levels(decode(text)), v)) throw new AssertionError("round trip failed on " + text);
        }
    }
}
```

#### Solution: [Recognize] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: tb-serialize-binary-tree -->

**Approach.** The encoder walks the tree with a queue, writes the weight of each dequeued node and then the weight or `null` of each of its two children, enqueueing only the present children. The decoder reads the first token as the root, then for each dequeued node reads two tokens with a moving index, attaching the present ones and enqueueing them. Neither side recurses, so a very deep tree is safe. The oracle derives the expected text straight from the input array: its entries in order, followed by enough `null` tokens to give every present node two child tokens, which is 2m + 1 tokens for m present nodes. The assertions check the text, the round trip on random trees, and a chain of one hundred thousand nodes.

**Complexity.** O(n) time and O(w) queue space, with no recursion.

```java run
import java.util.*;

public final class LevelCodecRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static String encode(Node root) {
        if (root == null) return "null";
        StringBuilder text = new StringBuilder();
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        text.append(root.val);
        while (!queue.isEmpty()) {
            Node n = queue.poll();
            for (Node child : new Node[] {n.left, n.right}) {
                if (child == null) { text.append(",null"); continue; }
                text.append(',').append(child.val);
                queue.add(child);
            }
        }
        return text.toString();
    }

    static Node decode(String text) {
        String[] tokens = text.split(",");
        if (tokens[0].equals("null")) return null;
        Node root = new Node(Integer.parseInt(tokens[0]));
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        int at = 1;
        while (!queue.isEmpty()) {
            Node n = queue.poll();
            if (!tokens[at].equals("null")) { n.left = new Node(Integer.parseInt(tokens[at])); queue.add(n.left); }
            at++;
            if (!tokens[at].equals("null")) { n.right = new Node(Integer.parseInt(tokens[at])); queue.add(n.right); }
            at++;
        }
        return root;
    }

    static String expected(Integer[] v) {
        List<String> tokens = new ArrayList<>();
        int present = 0;
        for (Integer x : v) { tokens.add(x == null ? "null" : String.valueOf(x)); if (x != null) present++; }
        while (tokens.size() < 2 * present + 1) tokens.add("null");
        return String.join(",", tokens);
    }

    static String report(Integer[] v) {
        String text = encode(build(v));
        boolean same = Arrays.equals(levels(decode(text)), v);
        return "[\"" + text + "\", " + same + "]";
    }

    public static void main(String[] args) {
        if (!report(new Integer[] {1, 2, 3, null, null, 4, 5}).equals("[\"1,2,3,null,null,4,5,null,null,null,null\", true]")) throw new AssertionError("example 1");
        if (!report(new Integer[] {1, null, 2}).equals("[\"1,null,2,null,null\", true]")) throw new AssertionError("example 2");
        if (!encode(null).equals("null") || decode("null") != null) throw new AssertionError("empty tree");
        Random rnd = new Random(16804);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 20, -1000, 1000);
            if (!encode(build(v)).equals(expected(v))) throw new AssertionError("text differs on " + Arrays.toString(v));
            if (!Arrays.equals(levels(decode(encode(build(v)))), v)) throw new AssertionError("round trip failed on " + Arrays.toString(v));
        }
        Node root = new Node(0), tail = root;
        for (int i = 1; i < 100000; i++) { tail.left = new Node(i % 1000); tail = tail.left; }
        Node back = decode(encode(root));
        int depth = 0;
        for (Node at = back; at != null; at = at.left) depth++;
        if (depth != 100000) throw new AssertionError("deep chain should survive the round trip");
    }
}
```
