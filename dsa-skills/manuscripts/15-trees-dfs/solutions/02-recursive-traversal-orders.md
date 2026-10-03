<!-- solutions-for: 02-recursive-traversal-orders -->
### Recursive Traversal Orders

#### Solution: [Build] Binary Tree Preorder Traversal (LeetCode 144)
<!-- id: tr-preorder-walk -->

**Approach.** Turn the level-order array into two link arrays, `left[i]` and `right[i]`, holding the array position of each child or -1. Then walk from position 0 with a shared output list: if the position is -1 return, otherwise append the value, recurse left, and recurse right. Appending first is what makes every subtree contribute a block that starts with its own root. The assertions compare with a stack-based walk that pushes the right child before the left, and check that a list passed in by the caller collects the output of two separate runs only when the caller chooses to reuse it.

**Complexity.** O(n) time, and O(h) recursion stack besides the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PreorderWalk {
    static int[][] links(Integer[] v) {
        int n = v.length;
        int[] left = new int[n], right = new int[n];
        Arrays.fill(left, -1);
        Arrays.fill(right, -1);
        if (n == 0) return new int[][] {left, right};
        int[] queue = new int[n];
        int head = 0, tail = 0, next = 1;
        queue[tail++] = 0;
        while (head < tail) {
            int at = queue[head++];
            if (next < n) { if (v[next] != null) { left[at] = next; queue[tail++] = next; } next++; }
            if (next < n) { if (v[next] != null) { right[at] = next; queue[tail++] = next; } next++; }
        }
        return new int[][] {left, right};
    }

    static void walk(int at, Integer[] v, int[] left, int[] right, List<Integer> out) {
        if (at < 0) return;
        out.add(v[at]);
        walk(left[at], v, left, right, out);
        walk(right[at], v, left, right, out);
    }

    static List<Integer> preorder(Integer[] v) {
        int[][] lk = links(v);
        List<Integer> out = new ArrayList<>();
        if (v.length > 0) walk(0, v, lk[0], lk[1], out);
        return out;
    }

    static List<Integer> oracle(Integer[] v) {
        List<Integer> out = new ArrayList<>();
        if (v.length == 0) return out;
        int[][] lk = links(v);
        int[] stack = new int[v.length + 1];
        int top = 0;
        stack[top++] = 0;
        while (top > 0) {
            int at = stack[--top];
            out.add(v[at]);
            if (lk[1][at] >= 0) stack[top++] = lk[1][at];
            if (lk[0][at] >= 0) stack[top++] = lk[0][at];
        }
        return out;
    }

    static Integer[] randomTree(Random rnd) {
        int n = 1 + rnd.nextInt(12);
        int[] left = new int[n], right = new int[n];
        Arrays.fill(left, -1);
        Arrays.fill(right, -1);
        for (int i = 1; i < n; i++) {
            while (true) {
                int p = rnd.nextInt(i);
                if (rnd.nextBoolean()) { if (left[p] < 0) { left[p] = i; break; } }
                else if (right[p] < 0) { right[p] = i; break; }
            }
        }
        List<Integer> out = new ArrayList<>();
        List<Integer> queue = new ArrayList<>();
        queue.add(0);
        out.add(rnd.nextInt(201) - 100);
        int[] labels = new int[n];
        labels[0] = out.get(0);
        for (int q = 0; q < queue.size(); q++) {
            int id = queue.get(q);
            for (int kid : new int[] {left[id], right[id]}) {
                if (kid < 0) out.add(null);
                else { labels[kid] = rnd.nextInt(201) - 100; out.add(labels[kid]); queue.add(kid); }
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!preorder(new Integer[] {1, null, 2, 3}).equals(List.of(1, 2, 3))) throw new AssertionError("example 1");
        if (!preorder(new Integer[] {5, 3, 8, 1}).equals(List.of(5, 3, 1, 8))) throw new AssertionError("example 2");
        if (!preorder(new Integer[] {}).isEmpty()) throw new AssertionError("empty tree");
        Integer[] t = {5, 3, 8, 1};
        int[][] lk = links(t);
        List<Integer> shared = new ArrayList<>();
        walk(0, t, lk[0], lk[1], shared);
        walk(0, t, lk[0], lk[1], shared);
        if (shared.size() != 8) throw new AssertionError("a reused list keeps earlier output");
        Random rnd = new Random(15201);
        for (int k = 0; k < 5000; k++) {
            Integer[] v = randomTree(rnd);
            if (!preorder(v).equals(oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: tr-inorder-walk -->

**Approach.** The structure is the same as the previous walk with one line moved: recurse left, then append the value, then recurse right. The oracle works differently. It assigns each node a code of its position, writing the left turns and right turns from the root as a string, and orders the nodes by a rule that does not mention recursion: a node comes after everything in its left subtree and before everything in its right subtree, which for path strings means comparing paths with the left turn smaller than the stop marker and the stop marker smaller than the right turn. The assertions compare the walk with that sorted order, and also check that a binary search tree built from distinct values reads back in increasing order.

**Complexity.** O(n) time, and O(h) stack, where h can reach n on a chain.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InorderWalk {
    static final class Cell {
        final int val;
        Cell low, high;
        Cell(int val) { this.val = val; }
    }

    static Cell build(Integer[] v) {
        if (v.length == 0) return null;
        Cell[] made = new Cell[v.length];
        made[0] = new Cell(v[0]);
        int slot = 1;
        for (int i = 0; i < v.length && slot < v.length; i++) {
            if (made[i] == null) continue;
            if (v[slot] != null) { made[slot] = new Cell(v[slot]); made[i].low = made[slot]; }
            slot++;
            if (slot < v.length) {
                if (v[slot] != null) { made[slot] = new Cell(v[slot]); made[i].high = made[slot]; }
                slot++;
            }
        }
        return made[0];
    }

    static void visit(Cell c, List<Integer> out) {
        if (c == null) return;
        visit(c.low, out);
        out.add(c.val);
        visit(c.high, out);
    }

    static List<Integer> inorder(Integer[] v) {
        List<Integer> out = new ArrayList<>();
        visit(build(v), out);
        return out;
    }

    static void collect(Cell c, String path, List<String> paths, List<Integer> vals) {
        if (c == null) return;
        paths.add(path + "1");
        vals.add(c.val);
        collect(c.low, path + "0", paths, vals);
        collect(c.high, path + "2", paths, vals);
    }

    static List<Integer> oracle(Integer[] v) {
        List<String> paths = new ArrayList<>();
        List<Integer> vals = new ArrayList<>();
        collect(build(v), "", paths, vals);
        Integer[] order = new Integer[paths.size()];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> comparePaths(paths.get(a), paths.get(b)));
        List<Integer> out = new ArrayList<>();
        for (int i : order) out.add(vals.get(i));
        return out;
    }

    static int comparePaths(String a, String b) {
        int n = Math.min(a.length(), b.length());
        for (int i = 0; i < n; i++) {
            if (a.charAt(i) != b.charAt(i)) return Character.compare(a.charAt(i), b.charAt(i));
        }
        return Integer.compare(a.length(), b.length());
    }

    static Integer[] randomShape(Random rnd) {
        int n = 1 + rnd.nextInt(11);
        List<Integer> slots = new ArrayList<>();
        slots.add(rnd.nextInt(90));
        int open = 2, i = 0;
        while (slots.size() < 2 * n + 2 && i < slots.size() && open > 0) {
            i++;
            if (slots.get(i - 1) == null) continue;
            for (int c = 0; c < 2; c++) slots.add(rnd.nextInt(4) == 0 ? null : rnd.nextInt(90));
            if (slots.size() > 24) break;
        }
        while (!slots.isEmpty() && slots.get(slots.size() - 1) == null) slots.remove(slots.size() - 1);
        return slots.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!inorder(new Integer[] {1, null, 2, 3}).equals(List.of(1, 3, 2))) throw new AssertionError("example 1");
        if (!inorder(new Integer[] {5, 3, 8, 1}).equals(List.of(1, 3, 5, 8))) throw new AssertionError("example 2");
        if (!inorder(new Integer[] {}).isEmpty()) throw new AssertionError("empty tree");
        List<Integer> sorted = inorder(new Integer[] {8, 4, 12, 2, 6, 10, 14});
        for (int i = 1; i < sorted.size(); i++) if (sorted.get(i - 1) >= sorted.get(i)) throw new AssertionError("a search tree reads in increasing order");
        Random rnd = new Random(15202);
        for (int k = 0; k < 4000; k++) {
            Integer[] v = randomShape(rnd);
            if (v.length == 0 || v[0] == null) continue;
            if (!inorder(v).equals(oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tr-one-sided-orders -->

**Approach.** Make one recursive method that takes the node and three output lists and append to the first before the calls, the second between them, and the third after them. An empty subtree returns at the top, so a missing left side and a missing right side need no separate branches, and the empty array gives three empty lists. The oracle is a state machine on an explicit stack: each stack entry holds a node and a phase 0, 1 or 2, and the phase decides which list receives the value as the entry is advanced. The assertions compare the two for random trees, and check the left-only and right-only chains, where the preorder and postorder sheets are the reverse of each other.

**Complexity.** O(n) time for n nodes and O(h) stack in the recursive version.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneSidedOrders {
    static final class Vertex {
        final int val;
        Vertex a, b;
        Vertex(int val) { this.val = val; }
    }

    static Vertex build(Integer[] v) {
        if (v.length == 0) return null;
        List<Vertex> line = new ArrayList<>();
        Vertex root = new Vertex(v[0]);
        line.add(root);
        int next = 1;
        for (int k = 0; k < line.size() && next < v.length; k++) {
            Vertex cur = line.get(k);
            if (v[next] != null) { cur.a = new Vertex(v[next]); line.add(cur.a); }
            next++;
            if (next < v.length) {
                if (v[next] != null) { cur.b = new Vertex(v[next]); line.add(cur.b); }
                next++;
            }
        }
        return root;
    }

    static void all(Vertex x, List<Integer> pre, List<Integer> in, List<Integer> post) {
        if (x == null) return;
        pre.add(x.val);
        all(x.a, pre, in, post);
        in.add(x.val);
        all(x.b, pre, in, post);
        post.add(x.val);
    }

    static List<List<Integer>> sheets(Integer[] v) {
        List<Integer> pre = new ArrayList<>(), in = new ArrayList<>(), post = new ArrayList<>();
        all(build(v), pre, in, post);
        return List.of(pre, in, post);
    }

    static List<List<Integer>> oracle(Integer[] v) {
        List<List<Integer>> out = List.of(new ArrayList<>(), new ArrayList<>(), new ArrayList<>());
        Vertex root = build(v);
        if (root == null) return out;
        List<Vertex> nodes = new ArrayList<>();
        List<Integer> phases = new ArrayList<>();
        nodes.add(root);
        phases.add(0);
        while (!nodes.isEmpty()) {
            int top = nodes.size() - 1;
            Vertex x = nodes.get(top);
            int phase = phases.get(top);
            out.get(phase).add(x.val);
            if (phase == 0) {
                phases.set(top, 1);
                if (x.a != null) { nodes.add(x.a); phases.add(0); }
            } else if (phase == 1) {
                phases.set(top, 2);
                if (x.b != null) { nodes.add(x.b); phases.add(0); }
            } else {
                nodes.remove(top);
                phases.remove(top);
            }
        }
        return out;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(10);
        List<Integer> out = new ArrayList<>();
        List<Integer> queue = new ArrayList<>();
        int made = 1;
        out.add(rnd.nextInt(50));
        queue.add(0);
        for (int q = 0; q < queue.size(); q++) {
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(3) != 0) { out.add(rnd.nextInt(50)); queue.add(made); made++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        List<List<Integer>> none = sheets(new Integer[] {});
        if (none.size() != 3 || !none.get(0).isEmpty() || !none.get(1).isEmpty() || !none.get(2).isEmpty()) throw new AssertionError("example 1");
        List<List<Integer>> e2 = sheets(new Integer[] {1, 2, null, 3});
        if (!e2.equals(List.of(List.of(1, 2, 3), List.of(3, 2, 1), List.of(3, 2, 1)))) throw new AssertionError("example 2");
        List<List<Integer>> rightChain = sheets(new Integer[] {1, null, 2, null, 3});
        if (!rightChain.equals(List.of(List.of(1, 2, 3), List.of(1, 2, 3), List.of(3, 2, 1)))) throw new AssertionError("right chain");
        Random rnd = new Random(15203);
        for (int k = 0; k < 5000; k++) {
            Integer[] v = randomLevels(rnd);
            if (!sheets(v).equals(oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: tr-postorder-walk -->

**Approach.** Recurse into the left subtree, then the right subtree, and only then append the value. A node is therefore written after the complete blocks of both of its subtrees, which is exactly when everything it owns has been handled. The oracle uses the mirror fact that postorder is a reversed walk: writing node, then right subtree, then left subtree, and reversing the result, yields the postorder sheet. The assertions compare the recursive walk with that reversed walk on random trees and check that the root is always the last value.

**Complexity.** O(n) time, plus O(h) stack for the recursive version and O(n) for the oracle's reversed list.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class PostorderWalk {
    static int[] lo, hi;

    static void layout(Integer[] v) {
        lo = new int[v.length];
        hi = new int[v.length];
        Arrays.fill(lo, -1);
        Arrays.fill(hi, -1);
        int next = 1;
        for (int i = 0; i < v.length && next < v.length; i++) {
            if (v[i] == null && i > 0 && !reachable[i]) continue;
            if (next < v.length) { if (v[next] != null) { lo[i] = next; reachable[next] = true; } next++; }
            if (next < v.length) { if (v[next] != null) { hi[i] = next; reachable[next] = true; } next++; }
        }
    }
    static boolean[] reachable;

    static void setup(Integer[] v) {
        reachable = new boolean[v.length];
        if (v.length > 0) reachable[0] = true;
        layout(v);
    }

    static void finishLast(int at, Integer[] v, List<Integer> out) {
        if (at < 0) return;
        finishLast(lo[at], v, out);
        finishLast(hi[at], v, out);
        out.add(v[at]);
    }

    static List<Integer> postorder(Integer[] v) {
        setup(v);
        List<Integer> out = new ArrayList<>();
        if (v.length > 0) finishLast(0, v, out);
        return out;
    }

    static void mirrored(int at, Integer[] v, List<Integer> out) {
        if (at < 0) return;
        out.add(v[at]);
        mirrored(hi[at], v, out);
        mirrored(lo[at], v, out);
    }

    static List<Integer> oracle(Integer[] v) {
        setup(v);
        List<Integer> out = new ArrayList<>();
        if (v.length > 0) mirrored(0, v, out);
        Collections.reverse(out);
        return out;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(11);
        List<Integer> out = new ArrayList<>();
        int made = 1, queued = 1;
        out.add(rnd.nextInt(100));
        for (int q = 0; q < queued; q++) {
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(100)); made++; queued++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!postorder(new Integer[] {1, null, 2, 3}).equals(List.of(3, 2, 1))) throw new AssertionError("example 1");
        if (!postorder(new Integer[] {5, 3, 8, 1}).equals(List.of(1, 3, 8, 5))) throw new AssertionError("example 2");
        if (!postorder(new Integer[] {}).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(15204);
        for (int k = 0; k < 5000; k++) {
            Integer[] v = randomLevels(rnd);
            List<Integer> got = postorder(v);
            if (!got.equals(oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
            if (!got.get(got.size() - 1).equals(v[0])) throw new AssertionError("the root is written last");
        }
    }
}
```
