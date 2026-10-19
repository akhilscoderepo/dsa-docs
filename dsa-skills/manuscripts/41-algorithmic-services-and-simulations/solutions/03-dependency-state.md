<!-- solutions-for: 03-dependency-state -->
### Solutions For Dependency State

#### Solution: [Build] Expression Tree Evaluation (LeetCode 1628)
<!-- id: sv-dep-expression-tree -->

**Approach.** An abstract node class declares `evaluate()`. An operand node stores one integer and returns it. An operator node stores its symbol and two child nodes, evaluates the left child, then the right child, and applies the symbol. The builder reads the tokens left to right with a stack. An operand token pushes a new operand node. An operator token pops the right child first and the left child second, then pushes the new operator node.

The invariant is that after each token the stack holds the complete subtrees built so far, in token order. A valid postfix expression leaves exactly one node, which is the root. No node stores a result, so repeated calls give the same value.

**Complexity.**

- **Time** is O(n) to build and O(n) per `evaluate()` call, because every node is created once and visited once.
- **Space** is O(n) for the nodes, plus recursion depth up to the tree height.

```java run
import java.util.*;

public final class ExpressionTreeSolution {
    /** Common type for both node kinds; invariant: evaluate has no side effects. */
    static abstract class Node {
        abstract int evaluate();
    }

    static final class Operand extends Node {
        private final int number;
        Operand(int number) { this.number = number; }
        // O(1) time and space; returns the stored number.
        @Override int evaluate() { return number; }
    }

    static final class Operator extends Node {
        private final char symbol;
        private final Node left, right;
        Operator(char symbol, Node left, Node right) { this.symbol = symbol; this.left = left; this.right = right; }

        /**
         * Applies the symbol to the two child values.
         * Time: O(size of this subtree).
         * Space: O(height) for recursion.
         * Invariant: the left child is evaluated before the right child.
         */
        @Override int evaluate() {
            // Both children return before the symbol is applied.
            int a = left.evaluate(), b = right.evaluate();
            return switch (symbol) {
                case '+' -> a + b;
                case '-' -> a - b;
                case '*' -> a * b;
                default -> a / b;      // Java integer division truncates toward zero
            };
        }
    }

    /**
     * Builds the tree from a valid postfix token array.
     * Time: O(n).
     * Space: O(n).
     * Invariant: the stack holds complete subtrees in token order.
     */
    static Node build(String[] postfix) {
        Deque<Node> stack = new ArrayDeque<>();
        // One pass over the tokens, one push or two pops per token.
        for (String t : postfix) {
            if (t.length() == 1 && "+-*/".indexOf(t.charAt(0)) >= 0) {
                Node right = stack.pop();           // the right child was pushed last
                Node left = stack.pop();
                stack.push(new Operator(t.charAt(0), left, right));
            } else {
                stack.push(new Operand(Integer.parseInt(t)));
            }
        }
        // A valid expression leaves its root alone on the stack.
        return stack.pop();
    }

    // Oracle: evaluates the postfix tokens directly on a long stack.
    static long oracle(String[] postfix) {
        long[] st = new long[postfix.length];
        int top = 0;
        for (String t : postfix) {
            if (t.length() == 1 && "+-*/".indexOf(t.charAt(0)) >= 0) {
                long b = st[--top], a = st[--top];
                st[top++] = switch (t.charAt(0)) { case '+' -> a + b; case '-' -> a - b; case '*' -> a * b; default -> a / b; };
            } else st[top++] = Long.parseLong(t);
        }
        return st[0];
    }

    // Generates a random postfix expression, or returns null when a step leaves the int range or divides by zero.
    static String[] randomPostfix(Random rnd, int leaves) {
        List<String> out = new ArrayList<>();
        List<Long> vals = new ArrayList<>();
        int pushed = 0;
        while (pushed < leaves || vals.size() > 1) {
            boolean canOp = vals.size() >= 2;
            if (pushed < leaves && (!canOp || rnd.nextBoolean())) {
                int v = rnd.nextInt(101);
                out.add(Integer.toString(v)); vals.add((long) v); pushed++;
            } else {
                long b = vals.remove(vals.size() - 1), a = vals.remove(vals.size() - 1);
                char op = "+-*/".charAt(rnd.nextInt(4));
                if (op == '/' && b == 0) return null;
                long r = switch (op) { case '+' -> a + b; case '-' -> a - b; case '*' -> a * b; default -> a / b; };
                if (r > Integer.MAX_VALUE || r < Integer.MIN_VALUE) return null;
                out.add(String.valueOf(op)); vals.add(r);
            }
        }
        return out.toArray(new String[0]);
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text, including a repeated evaluate call.
        Node e1 = build(new String[] {"3", "4", "+", "2", "*"});
        if (e1.evaluate() != 14 || e1.evaluate() != 14) throw new AssertionError("e1");
        if (build(new String[] {"0", "7", "-", "2", "/"}).evaluate() != -3) throw new AssertionError("e2");
        // A single operand is already a complete expression.
        if (build(new String[] {"42"}).evaluate() != 42) throw new AssertionError("single");
        // Random valid expressions checked against the direct stack evaluation.
        Random rnd = new Random(1628);
        int checked = 0;
        for (int round = 0; round < 3000; round++) {
            String[] p = randomPostfix(rnd, 1 + rnd.nextInt(12));
            if (p == null) continue;
            Node root = build(p);
            if (root.evaluate() != oracle(p)) throw new AssertionError("value " + Arrays.toString(p));
            if (root.evaluate() != oracle(p)) throw new AssertionError("repeat");
            checked++;
        }
        if (checked < 500) throw new AssertionError("too few valid cases");
    }
}
```

#### Solution: [Vary] Excel Sum Formula (LeetCode 631)
<!-- id: sv-dep-excel-sum -->

**Approach.** Each cell has a literal number or a formula, which is a map from cell index to the number of times the formula names it. The cached value of each cell is derived from that definition. Each cell also owns a set of dependents, the cells whose formulas name it. A `sum` call expands every reference string into cell indexes and counts them, so a cell named by two rectangles gets the count 2.

An edit follows the same steps for `set` and `sum`. First the cell leaves the dependents of every cell in its old formula. Then it stores the new definition and joins the dependents of every cell in the new formula. Then a depth-first search over dependents starts at the edited cell and records each cell after its dependents. Reversing that list puts every cell after the cells it reads, and the sheet recomputes the formula cells in that order.

The invariant is that every cached value equals the sum of count times value over its formula, and a cell appears in the dependents of exactly the cells its formula names. The acyclic guarantee of the contract makes the search finish.

**Complexity.**

- **Time** is O(R + A + E) per edit, where R is the number of cells in the named rectangles, A is the number of affected cells and E is their formula entries. `get` is O(1).
- **Space** is O(H * W + F), where F is the total number of formula entries.

```java run
import java.util.*;

public final class ExcelSumSolution {
    static final class Excel {
        private final int width;
        private final int[] value;
        private final Map<Integer, Integer>[] formula;     // null for a literal cell; cell -> times named
        private final Set<Integer>[] dependents;           // cells whose formulas name this cell

        @SuppressWarnings("unchecked")
        Excel(int height, char lastColumn) {
            width = lastColumn - 'A' + 1;
            int n = height * width;
            value = new int[n];
            formula = new Map[n];
            dependents = new Set[n];
            for (int i = 0; i < n; i++) dependents[i] = new HashSet<>();
        }

        private int id(int row, char col) { return (row - 1) * width + (col - 'A'); }

        /** Stores a literal and refreshes dependents; time O(A + E), space O(A). */
        void set(int row, char col, int v) {
            int c = id(row, col);
            detach(c);                 // the cell stops reading its old formula cells
            value[c] = v;
            refresh(c);                // dependents see the new literal
        }

        int get(int row, char col) { return value[id(row, col)]; }

        /**
         * Gives the cell a formula and returns its value.
         * Time: O(R + A + E).
         * Space: O(R + A).
         * Invariant: the cell joins dependents only after it left the old ones.
         */
        int sum(int row, char col, String[] refs) {
            int c = id(row, col);
            Map<Integer, Integer> counts = new HashMap<>();
            // Each named cell, inside or outside a rectangle, adds one to its count.
            for (String ref : refs) {
                String[] part = ref.split(":");
                int r1 = Integer.parseInt(part[0].substring(1)), c1 = part[0].charAt(0) - 'A';
                int r2 = r1, c2 = c1;
                if (part.length == 2) { r2 = Integer.parseInt(part[1].substring(1)); c2 = part[1].charAt(0) - 'A'; }
                for (int r = r1; r <= r2; r++) for (int k = c1; k <= c2; k++) counts.merge((r - 1) * width + k, 1, Integer::sum);
            }
            detach(c);
            formula[c] = counts;
            for (int d : counts.keySet()) dependents[d].add(c);
            refresh(c);
            return value[c];
        }

        // Removes the cell from the dependents of everything its old formula named; time O(entries).
        private void detach(int c) {
            if (formula[c] == null) return;
            for (int d : formula[c].keySet()) dependents[d].remove(c);
            formula[c] = null;
        }

        // Recomputes the edited cell and everything that reads it, in an order where readers come last.
        private void refresh(int start) {
            List<Integer> post = new ArrayList<>();
            collect(start, new boolean[value.length], post);
            Collections.reverse(post);
            for (int c : post) {
                if (formula[c] == null) continue;      // a literal keeps its number
                long s = 0;
                for (Map.Entry<Integer, Integer> e : formula[c].entrySet()) s += (long) e.getValue() * value[e.getKey()];
                value[c] = (int) s;
            }
        }

        // Depth-first search over dependents; a cell is recorded after all of its dependents.
        private void collect(int c, boolean[] seen, List<Integer> post) {
            if (seen[c]) return;
            seen[c] = true;
            for (int d : dependents[c]) collect(d, seen, post);
            post.add(c);
        }
    }

    // Oracle state: a literal or a count map per cell, evaluated from scratch on every read.
    static final class Brute {
        final int w, n;
        final long[] lit;
        final Map<Integer, Integer>[] def;
        @SuppressWarnings("unchecked")
        Brute(int h, int w) { this.w = w; n = h * w; lit = new long[n]; def = new Map[n]; }

        long eval(int c, long[] memo, boolean[] done) {
            if (def[c] == null) return lit[c];
            if (done[c]) return memo[c];
            long s = 0;
            for (Map.Entry<Integer, Integer> e : def[c].entrySet()) s += e.getValue() * eval(e.getKey(), memo, done);
            done[c] = true; memo[c] = s;
            return s;
        }

        long read(int c) { return eval(c, new long[n], new boolean[n]); }

        boolean reaches(int from, int target, boolean[] seen) {
            if (from == target) return true;
            if (seen[from] || def[from] == null) return false;
            seen[from] = true;
            for (int d : def[from].keySet()) if (reaches(d, target, seen)) return true;
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Excel x = new Excel(3, 'C');
        x.set(1, 'A', 2);
        if (x.sum(3, 'C', new String[] {"A1", "A1:B2"}) != 4) throw new AssertionError("e1");
        x.set(2, 'B', 5);
        if (x.get(3, 'C') != 9) throw new AssertionError("e2 first");
        if (x.sum(1, 'A', new String[] {"B2"}) != 5) throw new AssertionError("e2 sum");
        if (x.get(3, 'C') != 15) throw new AssertionError("e2 last");
        // Replacing a formula by a literal must stop later edits of the old inputs from reaching it.
        Excel y = new Excel(2, 'B');
        y.set(1, 'A', 1);
        y.sum(2, 'B', new String[] {"A1"});
        y.set(2, 'B', 7);
        y.set(1, 'A', 9);
        if (y.get(2, 'B') != 7) throw new AssertionError("stale dependents");
        // Random edits on a 4 by 4 grid checked against evaluation from the definitions.
        Random rnd = new Random(631);
        int accepted = 0;
        for (int round = 0; round < 200; round++) {
            Excel s = new Excel(4, 'D');
            Brute b = new Brute(4, 4);
            for (int op = 0; op < 60; op++) {
                int r = 1 + rnd.nextInt(4), col = rnd.nextInt(4), c = (r - 1) * 4 + col;
                if (rnd.nextInt(3) == 0) {
                    int v = rnd.nextInt(10);
                    s.set(r, (char) ('A' + col), v);
                    b.def[c] = null; b.lit[c] = v;
                } else {
                    int k = 1 + rnd.nextInt(3);
                    String[] refs = new String[k];
                    Map<Integer, Integer> counts = new HashMap<>();
                    for (int i = 0; i < k; i++) {
                        int r1 = 1 + rnd.nextInt(4), c1 = rnd.nextInt(4);
                        boolean rect = rnd.nextBoolean();
                        int r2 = rect ? r1 + rnd.nextInt(5 - r1) : r1, c2 = rect ? c1 + rnd.nextInt(4 - c1) : c1;
                        refs[i] = "" + (char) ('A' + c1) + r1 + (rect ? ":" + (char) ('A' + c2) + r2 : "");
                        for (int rr = r1; rr <= r2; rr++) for (int cc = c1; cc <= c2; cc++) counts.merge((rr - 1) * 4 + cc, 1, Integer::sum);
                    }
                    // Skip a formula that would read its own cell, because the contract excludes it.
                    boolean cyc = false;
                    for (int d : counts.keySet()) if (b.reaches(d, c, new boolean[16])) cyc = true;
                    if (cyc) continue;
                    Map<Integer, Integer> oldDef = b.def[c];
                    b.def[c] = counts;
                    // Skip a formula whose values would leave the int range anywhere in the grid.
                    boolean big = false;
                    for (int i = 0; i < 16; i++) if (Math.abs(b.read(i)) > 1_000_000_000L) big = true;
                    if (big) { b.def[c] = oldDef; continue; }
                    int got = s.sum(r, (char) ('A' + col), refs);
                    if (got != b.read(c)) throw new AssertionError("sum result");
                    accepted++;
                }
                // Every cell must match a fresh evaluation after each call.
                for (int i = 0; i < 16; i++) if (s.get(1 + i / 4, (char) ('A' + i % 4)) != b.read(i)) throw new AssertionError("cell " + i);
            }
        }
        if (accepted < 500) throw new AssertionError("too few formulas");
    }
}
```

#### Solution: [Boundary] Dependency Cycle Policy (Author exercise)
<!-- id: sv-dep-cycle-policy -->

**Approach.** The sheet stores each formula as a list of names, a value for every cell and a dependents set for every name that some formula reads. A `setFormula` call runs a depth-first search that starts at the proposed references and follows the existing formulas. If the search reaches the target cell, including by a direct self-reference, the call returns `false` before it writes anything. The search needs no knowledge of the target's old formula, because a path ends the moment it reaches the target.

When the check passes, the call detaches the cell from its old inputs, stores the new list, registers the cell as a dependent of each new input and refreshes the cell and its dependents in reverse post-order. A name that no call has defined still holds a dependents set, so a later `setLiteral` on it reaches its readers.

The invariant is that the formula graph is acyclic after every call, and every cached value equals its formula applied to current values. A rejected call changes neither.

**Complexity.**

- **Time** is O(k + V + E) per `setFormula` call for k refs and for the V cells and E entries the search and refresh visit. `get` is O(1).
- **Space** is O(n + e) for n named cells and e formula entries.

```java run
import java.util.*;

public final class CyclePolicySolution {
    static final class Sheet {
        private final Map<String, List<String>> formula = new HashMap<>();
        private final Map<String, Set<String>> dependents = new HashMap<>();
        private final Map<String, Long> value = new HashMap<>();

        /** Reads a value in O(1); an unset cell is 0. */
        long get(String cell) { return value.getOrDefault(cell, 0L); }

        /** Stores a literal; a literal cannot create a cycle because it reads nothing. Time O(A + E). */
        void setLiteral(String cell, long v) {
            detach(cell);
            value.put(cell, v);
            refresh(cell);
        }

        /**
         * Replaces the formula unless it would create a cycle.
         * Time: O(k + V + E).
         * Space: O(V).
         * Invariant: the search runs before the first write.
         */
        boolean setFormula(String cell, List<String> refs) {
            // Reaching the target from any reference means the target would read itself.
            if (reaches(refs, cell)) return false;
            detach(cell);
            formula.put(cell, new ArrayList<>(refs));
            // Each reference learns that the cell reads it.
            for (String r : refs) dependents.computeIfAbsent(r, k -> new HashSet<>()).add(cell);
            refresh(cell);
            return true;
        }

        // Drops the old formula edges so no stale dependents remain; time O(entries).
        private void detach(String cell) {
            List<String> old = formula.remove(cell);
            if (old == null) return;
            for (String r : old) dependents.get(r).remove(cell);
        }

        // Iterative search along formula edges; each cell expands once, so time is O(V + E).
        private boolean reaches(List<String> from, String target) {
            Deque<String> stack = new ArrayDeque<>(from);
            Set<String> seen = new HashSet<>();
            while (!stack.isEmpty()) {
                String c = stack.pop();
                if (c.equals(target)) return true;
                if (seen.add(c)) stack.addAll(formula.getOrDefault(c, List.of()));
            }
            return false;
        }

        // Recomputes the start cell and its readers in reverse post-order of the dependents graph.
        private void refresh(String start) {
            List<String> post = new ArrayList<>();
            collect(start, new HashSet<>(), post);
            Collections.reverse(post);
            for (String c : post) {
                List<String> f = formula.get(c);
                if (f == null) continue;
                long sum = 0;
                for (String r : f) sum += get(r);
                value.put(c, sum);
            }
        }

        private void collect(String c, Set<String> seen, List<String> post) {
            if (!seen.add(c)) return;
            for (String d : dependents.getOrDefault(c, Set.of())) collect(d, seen, post);
            post.add(c);
        }
    }

    // Oracle: keeps definitions only, detects cycles with Kahn's algorithm and evaluates with memoization.
    static final class Brute {
        final Map<String, Long> lit = new HashMap<>();
        final Map<String, List<String>> def = new HashMap<>();

        boolean acyclic(Map<String, List<String>> d) {
            Map<String, Integer> indeg = new HashMap<>();
            Map<String, List<String>> out = new HashMap<>();
            for (Map.Entry<String, List<String>> e : d.entrySet()) {
                indeg.putIfAbsent(e.getKey(), 0);
                for (String r : e.getValue()) {
                    indeg.putIfAbsent(r, 0);
                    indeg.merge(e.getKey(), 1, Integer::sum);
                    out.computeIfAbsent(r, k -> new ArrayList<>()).add(e.getKey());
                }
            }
            Deque<String> q = new ArrayDeque<>();
            for (Map.Entry<String, Integer> e : indeg.entrySet()) if (e.getValue() == 0) q.add(e.getKey());
            int removed = 0;
            while (!q.isEmpty()) {
                String c = q.poll();
                removed++;
                for (String u : out.getOrDefault(c, List.of())) if (indeg.merge(u, -1, Integer::sum) == 0) q.add(u);
            }
            return removed == indeg.size();
        }

        long read(String c, Map<String, Long> memo) {
            if (!def.containsKey(c)) return lit.getOrDefault(c, 0L);
            Long m = memo.get(c);
            if (m != null) return m;
            long s = 0;
            for (String r : def.get(c)) s += read(r, memo);
            memo.put(c, s);
            return s;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Sheet s = new Sheet();
        s.setLiteral("a", 3);
        s.setLiteral("b", 4);
        if (!s.setFormula("c", List.of("a", "b")) || s.get("c") != 7) throw new AssertionError("e1 formula");
        if (s.setFormula("a", List.of("c")) || s.get("a") != 3) throw new AssertionError("e1 reject");
        // Example 2 from the problem text.
        Sheet t = new Sheet();
        if (t.setFormula("x", List.of("x"))) throw new AssertionError("self reference");
        if (!t.setFormula("x", List.of("y", "y"))) throw new AssertionError("e2 formula");
        t.setLiteral("y", 5);
        if (t.get("x") != 10) throw new AssertionError("e2 value");
        if (t.setFormula("y", List.of("x"))) throw new AssertionError("e2 reject");
        // Random calls over six names checked against a cycle test on the whole graph.
        Random rnd = new Random(3003);
        String[] names = {"a", "b", "c", "d", "e", "f"};
        int rejected = 0, accepted = 0;
        for (int round = 0; round < 400; round++) {
            Sheet sh = new Sheet();
            Brute b = new Brute();
            for (int op = 0; op < 40; op++) {
                String cell = names[rnd.nextInt(6)];
                if (rnd.nextInt(3) == 0) {
                    long v = rnd.nextInt(11) - 5;
                    sh.setLiteral(cell, v);
                    b.def.remove(cell); b.lit.put(cell, v);
                } else {
                    int k = 1 + rnd.nextInt(3);
                    List<String> refs = new ArrayList<>();
                    for (int i = 0; i < k; i++) refs.add(names[rnd.nextInt(6)]);
                    Map<String, List<String>> cand = new HashMap<>(b.def);
                    cand.put(cell, refs);
                    boolean want = b.acyclic(cand);
                    if (sh.setFormula(cell, refs) != want) throw new AssertionError("verdict " + cell + refs);
                    if (want) { b.def.put(cell, refs); accepted++; } else rejected++;
                }
                // Every name, accepted call or not, must match a fresh evaluation.
                Map<String, Long> memo = new HashMap<>();
                for (String n : names) if (sh.get(n) != b.read(n, memo)) throw new AssertionError("value " + n);
            }
        }
        if (rejected < 100 || accepted < 100) throw new AssertionError("weak coverage");
    }
}
```

#### Solution: [Recognize] Design Spreadsheet (LeetCode 3484)
<!-- id: sv-dep-spreadsheet-query -->

**Approach.** The only stored state is a grid of integers, one per cell, so the grid is authoritative and nothing is derived. A formula passed to `getValue` is a question about the grid at the moment of the call. The method removes the leading `=`, splits the text at the `+`, and turns each side into a number. A side that starts with a letter is a cell name, so the method reads its column from the letter and its row from the digits and returns the stored number. Any other side is an integer literal.

No cached value exists, so a later `setCell` cannot leave a stale one, and the sheet needs no dependents map and no cycle check. The invariant is that the grid holds the latest number for each cell and `getValue` reads it at call time.

**Complexity.**

- **Time** is O(1) per call, because a formula has two terms and each term parses in constant time.
- **Space** is O(rows) for the grid of 26 columns.

```java run
import java.util.*;

public final class SpreadsheetQuerySolution {
    static final class Spreadsheet {
        private final int[][] grid;

        Spreadsheet(int rows) { grid = new int[rows + 1][26]; }

        /** Stores a number in O(1) time and space; the grid is the only state. */
        void setCell(String cell, int v) { grid[row(cell)][cell.charAt(0) - 'A'] = v; }

        /** Clears a cell and returns the number it held; O(1) time and space. */
        int resetCell(String cell) {
            int old = grid[row(cell)][cell.charAt(0) - 'A'];
            grid[row(cell)][cell.charAt(0) - 'A'] = 0;
            return old;
        }

        /**
         * Evaluates "=X+Y" against the current grid without storing anything.
         * Time: O(1).
         * Space: O(1).
         * Invariant: the result uses the numbers present at call time.
         */
        int getValue(String formula) {
            // Drop the equals sign, then split the two terms at the plus sign.
            String[] terms = formula.substring(1).split("\\+");
            return term(terms[0]) + term(terms[1]);
        }

        private int row(String cell) { return Integer.parseInt(cell.substring(1)); }

        // A term starting with a letter is a cell name; any other term is a number.
        private int term(String t) {
            if (Character.isLetter(t.charAt(0))) return grid[row(t)][t.charAt(0) - 'A'];
            return Integer.parseInt(t);
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Spreadsheet s = new Spreadsheet(3);
        s.setCell("A1", 2);
        s.setCell("B2", 5);
        if (s.getValue("=A1+B2") != 7 || s.getValue("=A1+10") != 12) throw new AssertionError("e1");
        if (s.getValue("=C3+C3") != 0) throw new AssertionError("e2 unset");
        if (s.resetCell("A1") != 2) throw new AssertionError("e2 reset");
        if (s.getValue("=A1+B2") != 5 || s.getValue("=7+8") != 15) throw new AssertionError("e2 last");
        // A query must not leave anything behind: a later edit changes the next answer.
        s.setCell("A1", 100);
        if (s.getValue("=A1+B2") != 105) throw new AssertionError("fresh read");
        // Random calls checked against a map keyed by cell name and parsed with a pattern.
        Random rnd = new Random(3484);
        java.util.regex.Pattern p = java.util.regex.Pattern.compile("=([A-Z0-9]+)\\+([A-Z0-9]+)");
        for (int round = 0; round < 300; round++) {
            Spreadsheet sp = new Spreadsheet(20);
            Map<String, Integer> ref = new HashMap<>();
            for (int op = 0; op < 80; op++) {
                String cell = "" + (char) ('A' + rnd.nextInt(26)) + (1 + rnd.nextInt(20));
                int t = rnd.nextInt(3);
                if (t == 0) {
                    int v = rnd.nextInt(100001);
                    sp.setCell(cell, v); ref.put(cell, v);
                } else if (t == 1) {
                    if (sp.resetCell(cell) != ref.getOrDefault(cell, 0)) throw new AssertionError("reset");
                    ref.remove(cell);
                } else {
                    String a = rnd.nextBoolean() ? cell : String.valueOf(rnd.nextInt(100001));
                    String b = "" + (char) ('A' + rnd.nextInt(26)) + (1 + rnd.nextInt(20));
                    String f = "=" + a + "+" + b;
                    java.util.regex.Matcher m = p.matcher(f);
                    if (!m.matches()) throw new AssertionError("pattern");
                    int want = 0;
                    for (int g = 1; g <= 2; g++) {
                        String x = m.group(g);
                        want += Character.isLetter(x.charAt(0)) ? ref.getOrDefault(x, 0) : Integer.parseInt(x);
                    }
                    if (sp.getValue(f) != want) throw new AssertionError("value " + f);
                }
            }
        }
    }
}
```
