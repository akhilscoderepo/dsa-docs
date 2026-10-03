<!-- lesson-kind: standard -->
<!-- lesson-id: object-ordering -->
## Object Ordering

<!-- stage: context -->
### A Teacher Posts The Exam Results

A teacher has marked an exam and must pin the results on the classroom door. Each sheet in her pile carries a student's name and a score. The rule she announces is simple: the highest score goes at the top, and students with the same score are listed alphabetically. Parents will read the list, and two students with equal scores will compare their positions, so the rule has to give one answer.

She cannot sort by score and hope. Her pile happens to be in the order the papers were handed in, and a student who handed in late would land above a student who handed in early with the same mark, for no reason anyone could defend. The sheet is a record with several fields, and the ordering is a statement about which field decides first, which field decides next, and what happens when everything the rule looks at is equal.

<!-- stage: naive -->
### Insert Each Sheet Into A Sorted Stack

A first plan is to build the posted list one sheet at a time. Keep a list that is already in the right order, and for each new sheet walk down the list until you find the right place, then insert it there.

```java
final class ResultsBoard {
    record Student(String name, int score) {}

    static List<Student> postByInsertion(List<Student> sheets) {
        List<Student> posted = new ArrayList<>();
        for (Student s : sheets) {
            int at = 0;
            while (at < posted.size() && goesFirst(posted.get(at), s)) at++;
            posted.add(at, s);
        }
        return posted;
    }

    static boolean goesFirst(Student a, Student b) {
        if (a.score() != b.score()) return a.score() > b.score();
        return a.name().compareTo(b.name()) < 0;
    }
}
```

It gives the right list for every input where no two sheets are identical in both fields, and the rule for ties is visible in `goesFirst`.

<!-- stage: bottleneck -->
### Slow Walks And Scattered Rules

Each insertion walks past up to n sheets and shifts the list tail, so the whole procedure costs O(n^2). The second issue is where the rule lives. It sits inside a helper written for this one program, and every other piece of code that needs the same order, a printout, a ranking, a search, writes its own copy. When two copies disagree on a tie, two pages of the same report list a pair of students differently.

The library sorts objects in O(n log n) and takes the rule as a comparator. The remaining risk is what the rule says about ties. A comparator that looks only at the score leaves tied students in whatever order the sort happens to leave them, and the problem statement gets to decide whether that is acceptable. Writing the full rule down, to the last field, removes the question.

<!-- stage: insight -->
### The Comparator Owns The Tie Rule

For a record with several fields, the order is a statement of priorities, and the comparator is the place that statement lives. It names the **sort key** that decides first, then the key that decides when the first ties, and so on until every field that matters has been considered. The part people forget is the **tie rule**, the answer to "what if everything checked so far is equal?". Either the remaining records are interchangeable and a zero is honest, or the comparator must continue to another field until the order is fully determined.

Objects in Java can be sorted by a comparator, and that includes arrays of arrays. An `int[][]` is an **object array**, because each row `int[]` is itself an object, so `Arrays.sort(rows, comparator)` is legal with a `Comparator<int[]>` that reads `a[0]` and `a[1]`. The elements of a plain `int[]` are primitives, which is why that array has no such overload. This distinction matters whenever a problem hands you pairs as two-element arrays.

<!-- names: sort key, tie rule, object array -->

A sorted order can also be a preparation for building something. When people in a queue are described by their height and by how many taller or equal people stand in front of them, sorting them with the tallest first, and with smaller counts first among equals, makes a one-by-one insertion at the stated position safe: everyone already placed is at least as tall, so a person's count is exactly the index where they belong, and later, shorter people can never disturb it.

<!-- stage: variables -->
### Record, Key List And Output

The record holds the fields the comparator may read, and the comparator reads them without changing them. The key list is ordered, and the first key that differs decides, so later keys never override earlier ones. The output list is built by the library or, in the reconstruction, by inserting at an index: the state is the partial list built so far, and the invariant is that every person already in it is at least as tall as everyone still to come.

<!-- stage: trace -->
### Sheets Settling And A Queue Rebuilt

The first trace inserts four exam sheets into a sorted list, with the rule "higher score first, then name". The step to study is the fourth insertion, where a new sheet with the same score as an earlier one slots in by name, ahead of a student whose name comes later in the alphabet.

```trace
{"cells":["mia 90","ben 85","zoe 90","ann 85"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"insert":"mia 90","list":"mia 90"},"note":"Insert mia with 90. It is the first sheet. The list reads mia 90."},{"at":{"i":1},"vars":{"insert":"ben 85","list":"mia 90, ben 85"},"note":"Insert ben with 85. ben loses to mia on a lower score, so it stays behind. The list reads mia 90, ben 85."},{"at":{"i":2},"vars":{"insert":"zoe 90","list":"mia 90, zoe 90, ben 85"},"note":"Insert zoe with 90. zoe beats ben on a higher score, so it moves ahead; zoe loses to mia on the same score and a later name, so it stays behind. The list reads mia 90, zoe 90, ben 85."},{"at":{"i":3},"vars":{"insert":"ann 85","list":"mia 90, zoe 90, ann 85, ben 85"},"note":"Insert ann with 85. ann beats ben on the same score and an earlier name, so it moves ahead; ann loses to zoe on a lower score, so it stays behind. The list reads mia 90, zoe 90, ann 85, ben 85."}]}
```

The second trace rebuilds a queue from people written as height over count. They have already been sorted tallest first, and shorter counts first among equal heights. Each person is inserted at the index equal to their count. The step to study is the insertion of 5 over 0: it lands at the very front, ahead of everyone taller, and the people behind it shift one place right without any of their own counts being disturbed, since only people who are at least as tall count toward theirs.

```trace
{"cells":["7/0","7/1","6/1","5/0","5/2","4/4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"person":"7/0","insertAt":0,"line":"7/0"},"note":"Place 7/0 at index 0. Everyone already in line is at least as tall, so exactly 0 of them stand in front. The line is now 7/0."},{"at":{"i":1},"vars":{"person":"7/1","insertAt":1,"line":"7/0, 7/1"},"note":"Place 7/1 at index 1. Everyone already in line is at least as tall, so exactly 1 of them stand in front. The line is now 7/0, 7/1."},{"at":{"i":2},"vars":{"person":"6/1","insertAt":1,"line":"7/0, 6/1, 7/1"},"note":"Place 6/1 at index 1. Everyone already in line is at least as tall, so exactly 1 of them stand in front. The line is now 7/0, 6/1, 7/1."},{"at":{"i":3},"vars":{"person":"5/0","insertAt":0,"line":"5/0, 7/0, 6/1, 7/1"},"note":"Place 5/0 at index 0. Everyone already in line is at least as tall, so exactly 0 of them stand in front. The line is now 5/0, 7/0, 6/1, 7/1."},{"at":{"i":4},"vars":{"person":"5/2","insertAt":2,"line":"5/0, 7/0, 5/2, 6/1, 7/1"},"note":"Place 5/2 at index 2. Everyone already in line is at least as tall, so exactly 2 of them stand in front. The line is now 5/0, 7/0, 5/2, 6/1, 7/1."},{"at":{"i":5},"vars":{"person":"4/4","insertAt":4,"line":"5/0, 7/0, 5/2, 6/1, 4/4, 7/1"},"note":"Place 4/4 at index 4. Everyone already in line is at least as tall, so exactly 4 of them stand in front. The line is now 5/0, 7/0, 5/2, 6/1, 4/4, 7/1."}]}
```

<!-- stage: code -->
### Records, Rows And Insert-At-Count

```java
final class ObjectOrders {
    record Student(String name, int score) {}

    static final Comparator<Student> RESULTS =
        Comparator.comparingInt(Student::score).reversed().thenComparing(Student::name);

    static int[][] rebuildQueue(int[][] people) {
        int[][] order = people.clone();
        Arrays.sort(order, (a, b) -> a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(a[1], b[1]));
        List<int[]> line = new ArrayList<>();
        for (int[] p : order) line.add(p[1], p);
        return line.toArray(new int[0][]);
    }

    static int compareLogs(String x, String y) {
        int sx = x.indexOf(' '), sy = y.indexOf(' ');
        boolean dx = Character.isDigit(x.charAt(sx + 1)), dy = Character.isDigit(y.charAt(sy + 1));
        if (dx && dy) return 0;
        if (dx) return 1;
        if (dy) return -1;
        int byContent = x.substring(sx + 1).compareTo(y.substring(sy + 1));
        return byContent != 0 ? byContent : x.substring(0, sx).compareTo(y.substring(0, sy));
    }
}
```

The sort costs O(n log n) comparisons. Inserting into an `ArrayList` at an index shifts the tail, so the queue rebuild is O(n^2) in the worst case from the shifting, even though each shift is a cheap block copy. Log comparison scans each line once per comparison, which is proportional to the line length.

<!-- stage: applicability -->
### When The Items Have Several Fields

Reach for an object comparator whenever the thing being ordered carries more than one field and the problem states a priority among them. Write the priority list before the code, and for every field ask whether a tie in it is acceptable. The invariant is that the comparator, and nothing else, decides the order, and that it decides every pair the problem cares about.

A false friend is sorting by one field and trusting that the rest will fall into the order of the input. Sometimes that works because the library sort of objects is stable, and sometimes the next person to edit the code changes the input order and the output changes with it. Another false friend is a problem that sounds like ordering but is really grouping, where equal keys must be adjacent and their relative order does not matter at all.

In Java, `int[][]` sorts with a comparator because rows are objects, and `int[]` does not. Use `Integer.compare` for fields, `String.compareTo` for text, and never subtract. When a comparator reads fields of a mutable object, do not change those fields during the sort.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Scores (Author exercise)
<!-- id: so-sort-scores -->

**Prerequisites.** The comparator-contracts lesson; records from Chapter 01 or 03.

**Problem.** Given students with a name and an integer score, return them ordered by score from highest to lowest, with equal scores ordered by name alphabetically. Build the order as a comparator over the whole record.

**Constraints.** 0 <= students.length <= 1000, scores between 0 and 100, names are non-empty lowercase words. Two students with the same name and score are interchangeable.

**Example 1.** Input `(zoe,90), (ben,85), (amy,90)`, output `(amy,90), (zoe,90), (ben,85)`.

**Example 2.** Input `(kim,70)`, output `(kim,70)`.

**Hint.** Which of the two keys has to be reversed? What decides between students whose scores tie?

**Changed decision.** First rung: the order moves from a single number to a record with a priority list.

#### [Vary] Reorder Data in Log Files (LeetCode 937)
<!-- id: so-reorder-logs -->

**Prerequisites.** The sort-scores exercise above.

**Problem.** Each log line is an identifier, a space, and then content. A letter-log has a lowercase letter as the first character of its content, and a digit-log has a digit there. Return the lines with all letter-logs first, ordered by content and then by identifier, followed by the digit-logs in their original relative order.

**Constraints.** 1 <= logs.length <= 100. Each line has an identifier of one or more characters without spaces, one space, and content of at least one character.

**Example 1.** Input `["id1 zed 4", "a2 3 9", "b0 art can", "x7 1 1", "c3 art can"]`, output `["b0 art can", "c3 art can", "id1 zed 4", "a2 3 9", "x7 1 1"]`.

**Example 2.** Input `["m1 8 8", "k9 q"]`, output `["k9 q", "m1 8 8"]`.

**Hint.** What should the comparator return for two digit-logs? Which comparison decides between two letter-logs whose content is the same?

**Changed decision.** The identifier now matters only after the content ties, and one kind of record has no order among its members.

#### [Boundary] Equal Primary Keys (Author exercise)
<!-- id: so-equal-primary-keys -->

**Prerequisites.** The two exercises above.

**Problem.** Sort people by age only and show that the output depends on the input order when ages tie. Then add a secondary key, the name, and show that the output no longer depends on the input order at all.

**Constraints.** Use at most 6 people, with at least two sharing an age. Check every permutation of the input.

**Example 1.** Input `(zed,30), (amy,30), (bo,25)` in two different orders, output with the age-only order: two different results.

**Example 2.** Input the same people with the age-then-name order, output: one result for every input order.

**Hint.** What does the library do with elements the comparator calls equal? How many distinct outputs can the full order produce for a fixed set of people?

**Changed decision.** The data is chosen so the primary key ties, forcing a decision about what the secondary rule is.

#### [Recognize] Queue Reconstruction by Height (LeetCode 406)
<!-- id: so-queue-reconstruction -->

**Prerequisites.** All three exercises above.

**Problem.** Each person is a pair, a height and the number of people standing in front of them who are at least as tall. Rebuild a queue that satisfies every pair. Sort so that insertion at the stated index is safe, then insert each person at index equal to their count.

**Constraints.** 1 <= people.length <= 2000, heights between 1 and 1000000, and the input is guaranteed to describe at least one valid queue. Sort rows with a `Comparator<int[]>`.

**Example 1.** Input `[[6,1],[4,4],[6,0],[5,0],[5,2],[4,0]]`, output `[[4,0],[5,0],[6,0],[5,2],[4,4],[6,1]]`.

**Example 2.** Input `[[3,0]]`, output `[[3,0]]`.

**Hint.** Whom must you place first so that later insertions cannot change an earlier count? Among people of equal height, who goes first?

**Changed decision.** The sort order is chosen so that a later construction step is correct, in place of being the answer itself.
