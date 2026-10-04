<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Sorting Records

#### Solution: [Build] Sort Scores (Author exercise)
<!-- id: so-sort-scores -->

**Approach.**
The method builds one `Player` record per name and score, sorts the records with a comparator that reads the score in descending order and then the name in ascending order, and returns the names. The record keeps each name with its score while the sort moves objects. The comparator chains the keys with `reversed()` on the score comparator only, so the name key stays ascending. The invariant after the sort is that every adjacent pair has a higher score on the left, or an equal score and a smaller name. The harness shows that `reversed()` at the end of the chain would flip both keys.

**Complexity.**
- **Time** is O(n log n * m), where m is the longest name, because each comparison reads at most m characters.
- **Space** is O(n) for the records and the answer.

```java run
import java.util.*;

public final class SortScores {
    record Player(String name, int score) {}

    /**
     * Returns the names ordered by score descending, then name ascending.
     * Time: O(n log n * m). Space: O(n).
     * Invariant: adjacent players have a higher score on the left, or an equal score and a smaller name.
     */
    static String[] rank(String[] names, int[] scores) {
        Player[] players = new Player[names.length];
        // One record per player keeps the name and the score together.
        for (int i = 0; i < names.length; i++) players[i] = new Player(names[i], scores[i]);
        // The reversal applies to the score comparator only, because thenComparing comes after it.
        Arrays.sort(players, Comparator.comparingInt(Player::score).reversed().thenComparing(Player::name));
        String[] out = new String[players.length];
        for (int i = 0; i < out.length; i++) out[i] = players[i].name();
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(rank(new String[] {"Ana", "Bo", "Cy"}, new int[] {70, 90, 80}), new String[] {"Bo", "Cy", "Ana"})) throw new AssertionError("example 1");
        if (!Arrays.equals(rank(new String[] {"Zed", "Amy", "Bob"}, new int[] {5, 5, 9}), new String[] {"Bob", "Amy", "Zed"})) throw new AssertionError("example 2");
        if (rank(new String[0], new int[0]).length != 0) throw new AssertionError("empty");
        // Java fact from the lesson: reversed() at the end of the chain reverses the name key as well.
        Player[] p = {new Player("A", 1), new Player("B", 1)};
        Arrays.sort(p, Comparator.comparingInt(Player::score).thenComparing(Player::name).reversed());
        if (!p[0].name().equals("B")) throw new AssertionError("reversed at the end");
        // Random inputs are checked against a selection-based oracle that follows the rule directly.
        Random rnd = new Random(81);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(8);
            String[] names = new String[n];
            int[] scores = new int[n];
            for (int k = 0; k < n; k++) { names[k] = "n" + (char) ('a' + k); scores[k] = rnd.nextInt(4) - 1; }
            List<Integer> left = new ArrayList<>();
            for (int k = 0; k < n; k++) left.add(k);
            String[] expect = new String[n];
            for (int pos = 0; pos < n; pos++) {
                int best = left.get(0);
                for (int k : left) {
                    if (scores[k] > scores[best] || (scores[k] == scores[best] && names[k].compareTo(names[best]) < 0)) best = k;
                }
                expect[pos] = names[best];
                left.remove(Integer.valueOf(best));
            }
            if (!Arrays.equals(rank(names, scores), expect)) throw new AssertionError(Arrays.toString(names));
        }
    }
}
```

#### Solution: [Vary] Reorder Data In Log Files (LeetCode 937)
<!-- id: so-reorder-logs -->

**Approach.**
The method splits the logs into letter-logs and digit-logs in one pass. It sorts only the letter-logs, with a comparator that compares the text after the first space and consults the identifier when the text ties. The digit-logs keep their order because the pass appended them in order and the comparator never sees them. The answer is the sorted letter-logs followed by the digit-logs. The invariant of the split pass is that each list holds its logs in input order.

**Complexity.**
- **Time** is O(n log n * m), where m is the longest log, because the sort compares strings of length up to m.
- **Space** is O(n * m) for the two lists and the answer.

```java run
import java.util.*;

public final class ReorderLogs {
    /**
     * Reorders logs so that letter-logs come first, sorted by content and identifier.
     * Time: O(n log n * m). Space: O(n * m).
     * Invariant: digits holds the digit-logs in input order.
     */
    static String[] reorder(String[] logs) {
        List<String> letters = new ArrayList<>();
        List<String> digits = new ArrayList<>();
        // One pass classifies each log by the first character of its content.
        for (String log : logs) {
            int space = log.indexOf(' ');
            if (Character.isDigit(log.charAt(space + 1))) digits.add(log);
            else letters.add(log);
        }
        // The identifier is read only when the content ties.
        letters.sort(Comparator.comparing((String s) -> s.substring(s.indexOf(' ') + 1)).thenComparing(s -> s.substring(0, s.indexOf(' '))));
        letters.addAll(digits);
        return letters.toArray(new String[0]);
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(reorder(new String[] {"d1 8 1", "l2 art can", "l1 art can", "d2 3"}), new String[] {"l1 art can", "l2 art can", "d1 8 1", "d2 3"})) throw new AssertionError("example 1");
        if (!Arrays.equals(reorder(new String[] {"a1 9", "b1 z", "a2 a"}), new String[] {"a2 a", "b1 z", "a1 9"})) throw new AssertionError("example 2");
        if (reorder(new String[0]).length != 0) throw new AssertionError("empty");
        // Random inputs are checked against an oracle that sorts by a combined key.
        Random rnd = new Random(82);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(7);
            String[] logs = new String[n];
            for (int k = 0; k < n; k++) {
                String id = "i" + (char) ('a' + rnd.nextInt(4));
                String rest = rnd.nextBoolean() ? "" + rnd.nextInt(3) : "" + (char) ('a' + rnd.nextInt(3)) + (rnd.nextBoolean() ? " b" : "");
                logs[k] = id + " " + rest;
            }
            List<String> expect = new ArrayList<>();
            for (String s : logs) if (!Character.isDigit(s.charAt(s.indexOf(' ') + 1))) expect.add(s);
            // The combined key puts the content first and the identifier second, with a separator below any letter.
            expect.sort(Comparator.comparing(s -> s.substring(s.indexOf(' ') + 1) + "\u0001" + s.substring(0, s.indexOf(' '))));
            for (String s : logs) if (Character.isDigit(s.charAt(s.indexOf(' ') + 1))) expect.add(s);
            if (!Arrays.equals(reorder(logs), expect.toArray(new String[0]))) throw new AssertionError(Arrays.toString(logs));
        }
    }
}
```

#### Solution: [Boundary] Equal Primary Keys (Author exercise)
<!-- id: so-sort-rows -->

**Approach.**
The method sorts the row array with a comparator that compares column 0 first. When column 0 is equal, it compares column 1 with the arguments swapped, which gives descending order without negation. Both comparisons use `Integer.compare`, so the extreme values cannot overflow. The array holds row objects, so the sort moves references to rows. The invariant after the sort is that adjacent rows have a smaller column 0 on the left, or an equal column 0 and a column 1 that is not smaller.

**Complexity.**
- **Time** is O(n log n), because each comparison reads at most two cells of each row.
- **Space** is O(n) for the working buffer of the object sort, and no cells are copied.

```java run
import java.util.*;

public final class SortRows {
    /**
     * Sorts rows by column 0 ascending and then column 1 descending, in place.
     * Time: O(n log n). Space: O(n) worst case for the library buffer.
     * Invariant: adjacent rows satisfy the two-key order.
     */
    static void sortRows(int[][] rows) {
        // The ternary reads column 1 only when column 0 ties.
        Arrays.sort(rows, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(q[1], p[1]));
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        int[][] e1 = {{2, 5}, {1, 3}, {2, 9}, {1, 3}};
        sortRows(e1);
        if (!Arrays.deepEquals(e1, new int[][] {{1, 3}, {1, 3}, {2, 9}, {2, 5}})) throw new AssertionError("example 1");
        int[][] e2 = {{0, Integer.MIN_VALUE}, {0, Integer.MAX_VALUE}};
        sortRows(e2);
        if (!Arrays.deepEquals(e2, new int[][] {{0, Integer.MAX_VALUE}, {0, Integer.MIN_VALUE}})) throw new AssertionError("example 2");
        sortRows(new int[0][]);
        // Java fact from the lesson: a row is an object, so the sort swaps references and keeps each row intact.
        int[] first = {9, 1}, second = {1, 1};
        int[][] pair = {first, second};
        sortRows(pair);
        if (pair[0] != second || pair[1] != first) throw new AssertionError("references");
        // Random inputs are checked against the oracle that sorts a list with a long-based key.
        Random rnd = new Random(83);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 1, -1};
        for (int t = 0; t < 500; t++) {
            int[][] a = new int[rnd.nextInt(8)][];
            for (int k = 0; k < a.length; k++) a[k] = new int[] {pool[rnd.nextInt(3)], pool[rnd.nextInt(pool.length)]};
            List<int[]> expect = new ArrayList<>(Arrays.asList(a));
            expect.sort((p, q) -> {
                if (p[0] != q[0]) return p[0] < q[0] ? -1 : 1;
                return Long.compare((long) q[1], (long) p[1]);
            });
            sortRows(a);
            if (!Arrays.deepEquals(a, expect.toArray(new int[0][]))) throw new AssertionError(Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Recognize] Queue Reconstruction By Height (LeetCode 406)
<!-- id: so-queue-height -->

**Approach.**
The method sorts the people by height in descending order and by `k` in ascending order. It then inserts each person into a list at index `k`. A person who is inserted later is never taller than anyone placed earlier, so later insertions never change the count of taller people in front of an earlier person. For a person of height `h`, the list holds only people with height at least `h` at the moment of insertion, so index `k` places exactly `k` such people in front. The invariant after each insertion is that every person already in the list has the correct count in the list. The harness checks the answer against a brute-force search over all permutations.

**Complexity.**
- **Time** is O(n^2), because each of n insertions into an `ArrayList` can shift up to n elements, and the sort adds O(n log n).
- **Space** is O(n) for the list.

```java run
import java.util.*;

public final class QueueHeight {
    /**
     * Rebuilds the queue from pairs [h, k].
     * Time: O(n^2). Space: O(n).
     * Invariant: after each insertion, every person in the list has the correct count within the list.
     */
    static int[][] reconstruct(int[][] people) {
        int[][] sorted = people.clone();
        // Taller people come first; among equal heights, the smaller k comes first.
        Arrays.sort(sorted, (p, q) -> p[0] != q[0] ? Integer.compare(q[0], p[0]) : Integer.compare(p[1], q[1]));
        List<int[]> queue = new ArrayList<>();
        // Each insertion at index k places exactly k taller-or-equal people in front.
        for (int[] person : sorted) queue.add(person[1], person);
        return queue.toArray(new int[0][]);
    }

    static boolean valid(int[][] q) {
        for (int i = 0; i < q.length; i++) {
            int c = 0;
            for (int j = 0; j < i; j++) if (q[j][0] >= q[i][0]) c++;
            if (c != q[i][1]) return false;
        }
        return true;
    }

    static boolean search(int[][] a, int k, int[][] expected) {
        if (k == a.length) return valid(a) && Arrays.deepEquals(a, expected);
        for (int i = k; i < a.length; i++) {
            int[] t = a[k]; a[k] = a[i]; a[i] = t;
            boolean ok = search(a, k + 1, expected);
            t = a[k]; a[k] = a[i]; a[i] = t;
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(reconstruct(new int[][] {{6, 1}, {5, 0}, {6, 0}, {4, 2}}), new int[][] {{5, 0}, {6, 0}, {4, 2}, {6, 1}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(reconstruct(new int[][] {{3, 1}, {3, 0}, {3, 2}}), new int[][] {{3, 0}, {3, 1}, {3, 2}})) throw new AssertionError("example 2");
        // Random valid inputs come from random queues; the answer must be the queue itself, and it must be valid.
        Random rnd = new Random(84);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] queue = new int[n][];
            for (int i = 0; i < n; i++) queue[i] = new int[] {rnd.nextInt(4), 0};
            for (int i = 0; i < n; i++) {
                int c = 0;
                for (int j = 0; j < i; j++) if (queue[j][0] >= queue[i][0]) c++;
                queue[i][1] = c;
            }
            int[][] shuffled = queue.clone();
            List<int[]> l = new ArrayList<>(Arrays.asList(shuffled));
            Collections.shuffle(l, rnd);
            int[][] in = l.toArray(new int[0][]);
            int[][] out = reconstruct(in);
            if (!valid(out)) throw new AssertionError("invalid answer");
            if (!search(out.clone(), 0, out)) throw new AssertionError("oracle disagrees");
            if (!Arrays.deepEquals(out, queue)) throw new AssertionError("not the original queue");
        }
    }
}
```
