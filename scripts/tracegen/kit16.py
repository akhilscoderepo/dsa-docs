"""Expands @@NODE@@ style tokens inside chapter 16 solution files with shared Java helper snippets."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / '16-trees-bfs-and-bsts'
KIT = {
"NODE": """    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
""",
"BUILD": """    static Node build(Integer[] v) {
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
""",
"LEVELS": """    static Integer[] levels(Node root) {
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
""",
"RANDTREE": """    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
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
""",
"RELABEL": """    static Integer[] relabel(Integer[] shape) {
        Integer[] out = shape.clone();
        int next = 0;
        for (int i = 0; i < out.length; i++) if (out[i] != null) out[i] = next++;
        return out;
    }

    static int countNodes(Integer[] v) {
        int c = 0;
        for (Integer x : v) if (x != null) c++;
        return c;
    }
""",
"ORACLELCA": """    static Node find(Node n, int val) {
        if (n == null) return null;
        if (n.val == val) return n;
        Node inLeft = find(n.left, val);
        return inLeft != null ? inLeft : find(n.right, val);
    }

    static Node viaParents(Node root, int p, int q) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        Set<Node> above = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node a = find(root, p); a != null; a = parent.get(a)) above.add(a);
        Node a = find(root, q);
        while (!above.contains(a)) a = parent.get(a);
        return a;
    }
""",
"PLAININSERT": """    static Node plainInsert(Node root, int key) {
        if (root == null) return new Node(key);
        Node at = root;
        while (true) {
            if (key == at.val) return root;
            if (key < at.val) { if (at.left == null) { at.left = new Node(key); return root; } at = at.left; }
            else { if (at.right == null) { at.right = new Node(key); return root; } at = at.right; }
        }
    }

    static Node randomBst(Random rnd, int maxNodes, int range) {
        Node root = null;
        int n = rnd.nextInt(maxNodes + 1);
        for (int i = 0; i < n; i++) root = plainInsert(root, rnd.nextInt(range));
        return root;
    }

    static void inorderInto(Node n, List<Integer> out) {
        if (n == null) return;
        inorderInto(n.left, out);
        out.add(n.val);
        inorderInto(n.right, out);
    }
""",
}
def expand(text):
    import re
    text = re.sub(r"```trace\n(@@TRACE\d@@)\n```", r"\1", text)
    for k, v in KIT.items():
        text = text.replace("@@%s@@\n" % k, v)
    import re
    assert "@@" not in re.sub(r"@@TRACE\d*@@", "", text), "unknown token"
    return text
if __name__ == "__main__":
    for p in sorted(ROOT.rglob("*.md")):
        t = p.read_text(); n = expand(t)
        if n != t: p.write_text(n); print("expanded", p.name)
