<!-- solutions-for: 05-object-ordering -->
### Object Ordering

#### Solution: [Build] Sort Scores (Author exercise)
<!-- id: so-sort-scores -->

**Approach.** The order is a chain of two keys: score descending, then name ascending. `comparingInt(score).reversed()` flips only the score key, and `thenComparing(name)` is consulted only on a score tie. Because every field of the record takes part, two records compare as zero only when they are equal in both fields, and then they are interchangeable. The test compares with an insertion-based oracle that applies an explicit yes-or-no rule on random students with many ties.

**Complexity.** O(n log n) comparisons and O(n) extra space for the sorted copy.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class SortScores {
    record Student(String name, int score) {}

    static final Comparator<Student> RESULTS =
        Comparator.comparingInt(Student::score).reversed().thenComparing(Student::name);

    static List<Student> post(List<Student> in) {
        List<Student> out = new ArrayList<>(in);
        out.sort(RESULTS);
        return out;
    }
    static boolean first(Student a, Student b) {
        return a.score() != b.score() ? a.score() > b.score() : a.name().compareTo(b.name()) < 0;
    }
    static List<Student> oracle(List<Student> in) {
        List<Student> out = new ArrayList<>();
        for (Student s : in) {
            int at = 0;
            while (at < out.size() && !first(s, out.get(at))) at++;
            out.add(at, s);
        }
        return out;
    }

    public static void main(String[] args) {
        List<Student> ex1 = post(List.of(new Student("zoe", 90), new Student("ben", 85), new Student("amy", 90)));
        if (!ex1.equals(List.of(new Student("amy", 90), new Student("zoe", 90), new Student("ben", 85)))) throw new AssertionError("example 1");
        if (!post(List.of(new Student("kim", 70))).equals(List.of(new Student("kim", 70)))) throw new AssertionError("example 2");
        if (!post(List.of()).isEmpty()) throw new AssertionError("empty input");
        Random rnd = new Random(531);
        String[] names = {"amy", "ben", "cal", "dee", "eli"};
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            List<Student> in = new ArrayList<>();
            for (int i = 0; i < n; i++) in.add(new Student(names[rnd.nextInt(names.length)], 70 + 5 * rnd.nextInt(3)));
            if (!post(in).equals(oracle(in))) throw new AssertionError("differs from the insertion oracle on " + in);
        }
    }
}
```

#### Solution: [Vary] Reorder Data in Log Files (LeetCode 937)
<!-- id: so-reorder-logs -->

**Approach.** Split each line at its first space. The comparator puts any letter-log ahead of any digit-log, returns zero for two digit-logs, and for two letter-logs compares the content first and the identifier second. Returning zero for digit-logs is what keeps their original relative order, because `Arrays.sort` on objects is stable. The oracle partitions the lines, sorts the letter-logs by an explicit insertion with the same two keys, and appends the digit-logs in input order.

**Complexity.** O(n log n) comparisons, each costing time proportional to the line length, and O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ReorderLogs {
    static int compareLogs(String x, String y) {
        int sx = x.indexOf(' '), sy = y.indexOf(' ');
        boolean dx = Character.isDigit(x.charAt(sx + 1)), dy = Character.isDigit(y.charAt(sy + 1));
        if (dx && dy) return 0;
        if (dx) return 1;
        if (dy) return -1;
        int byContent = x.substring(sx + 1).compareTo(y.substring(sy + 1));
        return byContent != 0 ? byContent : x.substring(0, sx).compareTo(y.substring(0, sy));
    }
    static String[] reorder(String[] logs) {
        String[] out = logs.clone();
        Arrays.sort(out, ReorderLogs::compareLogs);
        return out;
    }
    static String[] oracle(String[] logs) {
        List<String> letters = new ArrayList<>(), digits = new ArrayList<>();
        for (String l : logs) (Character.isDigit(l.charAt(l.indexOf(' ') + 1)) ? digits : letters).add(l);
        List<String> sorted = new ArrayList<>();
        for (String l : letters) {
            int at = 0;
            while (at < sorted.size() && compareLogs(sorted.get(at), l) <= 0) at++;
            sorted.add(at, l);
        }
        sorted.addAll(digits);
        return sorted.toArray(new String[0]);
    }

    public static void main(String[] args) {
        String[] ex1 = reorder(new String[] {"id1 zed 4", "a2 3 9", "b0 art can", "x7 1 1", "c3 art can"});
        if (!Arrays.equals(ex1, new String[] {"b0 art can", "c3 art can", "id1 zed 4", "a2 3 9", "x7 1 1"})) throw new AssertionError("example 1");
        if (!Arrays.equals(reorder(new String[] {"m1 8 8", "k9 q"}), new String[] {"k9 q", "m1 8 8"})) throw new AssertionError("example 2");
        Random rnd = new Random(532);
        String[] contents = {"art", "art can", "zed", "can 1", "7", "3 4", "9 x"};
        String[] ids = {"a1", "b2", "c3", "d4", "e5", "f6"};
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            String[] logs = new String[n];
            for (int i = 0; i < n; i++) logs[i] = ids[i] + " " + contents[rnd.nextInt(contents.length)];
            if (!Arrays.equals(reorder(logs), oracle(logs))) throw new AssertionError("differs from the partition oracle on " + Arrays.toString(logs));
        }
    }
}
```

#### Solution: [Boundary] Equal Primary Keys (Author exercise)
<!-- id: so-equal-primary-keys -->

**Approach.** With an age-only comparator, people of equal age compare as zero, and the stable object sort leaves them in the order of the input. Two permutations of the same people therefore give different outputs. Adding the name as a secondary key makes every pair of distinct people comparable, so every permutation gives the same output. The program tries all permutations of up to four people and collects the distinct outputs of each order: more than one for age-only, exactly one for age-then-name.

**Complexity.** The order itself is O(n log n); the exhaustive check is O(n! n log n) and only suits tiny test inputs.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public final class EqualPrimaryKeys {
    record Person(String name, int age) {}

    static void permutations(List<Person> pool, int k, List<List<Person>> out) {
        if (k == pool.size()) { out.add(new ArrayList<>(pool)); return; }
        for (int i = k; i < pool.size(); i++) {
            java.util.Collections.swap(pool, k, i);
            permutations(pool, k + 1, out);
            java.util.Collections.swap(pool, k, i);
        }
    }
    static Set<List<Person>> distinctOutputs(List<Person> people, Comparator<Person> order) {
        List<List<Person>> perms = new ArrayList<>();
        permutations(new ArrayList<>(people), 0, perms);
        Set<List<Person>> outputs = new HashSet<>();
        for (List<Person> p : perms) {
            List<Person> sorted = new ArrayList<>(p);
            sorted.sort(order);
            outputs.add(sorted);
        }
        return outputs;
    }

    public static void main(String[] args) {
        List<Person> people = List.of(new Person("zed", 30), new Person("amy", 30), new Person("bo", 25), new Person("cy", 30));
        Comparator<Person> ageOnly = Comparator.comparingInt(Person::age);
        Comparator<Person> ageThenName = ageOnly.thenComparing(Person::name);
        if (distinctOutputs(people, ageOnly).size() <= 1) throw new AssertionError("example 1: age-only output depends on the input order");
        if (distinctOutputs(people, ageThenName).size() != 1) throw new AssertionError("example 2: the full order gives one output");
        List<Person> only = distinctOutputs(people, ageThenName).iterator().next();
        if (!only.get(0).name().equals("bo") || !only.get(1).name().equals("amy")) throw new AssertionError("expected order bo, amy, cy, zed");
        List<Person> distinct = List.of(new Person("a", 1), new Person("b", 2), new Person("c", 3));
        if (distinctOutputs(distinct, ageOnly).size() != 1) throw new AssertionError("with no ties, age alone is enough");
    }
}
```

#### Solution: [Recognize] Queue Reconstruction by Height (LeetCode 406)
<!-- id: so-queue-reconstruction -->

**Approach.** Sort the rows with a `Comparator<int[]>` so that taller people come first and, among equal heights, the smaller count comes first. Then insert each person at the index equal to their count. When a person is inserted, everyone already in the list is at least as tall, so the count equals the number of people in front, which is the index. Later people are shorter or equal with a count that is at least as large, so they never change an earlier person's count. The test builds random valid queues, derives each person's pair, shuffles, reconstructs, and requires both the original queue and satisfaction of every count.

**Complexity.** O(n log n) comparisons plus O(n^2) element shifts in the worst case for the inserts; O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class QueueReconstruction {
    static int[][] reconstruct(int[][] people) {
        int[][] order = people.clone();
        Arrays.sort(order, (a, b) -> a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(a[1], b[1]));
        List<int[]> line = new ArrayList<>();
        for (int[] p : order) line.add(p[1], p);
        return line.toArray(new int[0][]);
    }
    static boolean satisfies(int[][] queue) {
        for (int i = 0; i < queue.length; i++) {
            int taller = 0;
            for (int j = 0; j < i; j++) if (queue[j][0] >= queue[i][0]) taller++;
            if (taller != queue[i][1]) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        int[][] ex1 = reconstruct(new int[][] {{6, 1}, {4, 4}, {6, 0}, {5, 0}, {5, 2}, {4, 0}});
        if (!Arrays.deepEquals(ex1, new int[][] {{4, 0}, {5, 0}, {6, 0}, {5, 2}, {4, 4}, {6, 1}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(reconstruct(new int[][] {{3, 0}}), new int[][] {{3, 0}})) throw new AssertionError("example 2");
        Random rnd = new Random(533);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] queue = new int[n][];
            for (int i = 0; i < n; i++) queue[i] = new int[] {1 + rnd.nextInt(5), 0};
            for (int i = 0; i < n; i++) {
                int taller = 0;
                for (int j = 0; j < i; j++) if (queue[j][0] >= queue[i][0]) taller++;
                queue[i][1] = taller;
            }
            List<int[]> shuffled = new ArrayList<>(Arrays.asList(queue));
            Collections.shuffle(shuffled, rnd);
            int[][] got = reconstruct(shuffled.toArray(new int[0][]));
            if (!satisfies(got)) throw new AssertionError("a count is violated: " + Arrays.deepToString(got));
            if (!Arrays.deepEquals(got, queue)) throw new AssertionError("not the original queue: " + Arrays.deepToString(got) + " vs " + Arrays.deepToString(queue));
        }
    }
}
```
