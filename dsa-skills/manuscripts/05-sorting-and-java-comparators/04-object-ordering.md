<!-- lesson-kind: standard -->
<!-- lesson-id: object-ordering -->
## Sort Objects By Several Fields

<!-- stage: context -->
### A Leaderboard With Mismatched Names

A quiz site stores each player's name in one array and each player's score in another. A report sorts the score array so that the best score comes first. The page then prints the sorted scores beside the original list of names. The top row shows the winner's score next to a player who finished last. Each array is sorted or ordered correctly on its own, but the pairing between them is gone.

Every field of one item must move together, and a tie on one field needs a rule from another field. This lesson answers two questions. How does a program sort whole records, and how does it state which field decides when the first field ties?

<!-- stage: naive -->
### Swapping Every Array In Step

The direct repair keeps the two arrays and swaps both of them whenever the sort swaps two scores. A bubble sort does this with one extra line per array.

```java
static void sortPlayers(String[] names, int[] scores) {
    for (int pass = 0; pass < scores.length - 1; pass++) {
        for (int i = 0; i + 1 < scores.length - pass; i++) {
            if (scores[i] < scores[i + 1]) {
                int s = scores[i]; scores[i] = scores[i + 1]; scores[i + 1] = s;
                String n = names[i]; names[i] = names[i + 1]; names[i + 1] = n;
            }
        }
    }
}
```

On names `["Ana", "Bo", "Cy"]` and scores `[70, 90, 80]` the method gives `["Bo", "Cy", "Ana"]` with scores `[90, 80, 70]`. The pairs stay together, and the highest score comes first.

<!-- stage: bottleneck -->
### Every Field Needs Its Own Swap

```predict
Two players have the score 90. The method above never swaps them. In which order do they appear, and what happens when the site adds a third array for the finish time?

They appear in their original order, because the comparison `scores[i] < scores[i + 1]` is false for a tie. The third array needs a third pair of swap lines in every place where a swap happens, and a missed line separates a field from its record again.
```

The method runs O(n^2) comparisons, and every new field adds a swap that the programmer must remember. The method also hides its tie rule. Equal scores keep the order that the input happened to have, so the output depends on an accident of the input. A better design moves all fields as one unit and states the tie rule in one place that a reader can find.

<!-- stage: insight -->
### Sort Records With A Priority Of Keys

The program should store each player as one object and sort the objects with one comparator that lists the keys in priority order.

#### Group The Fields Into One Record

A **record** is a Java class that holds named fields and generates its accessors. The declaration `record Player(String name, int score) {}` creates one object per player. Sorting an array of these objects moves each name together with its score, because the sort moves references to whole objects.

#### State The Tie Rule In The Comparator

A **tie rule** is the key that decides the order when all earlier keys are equal. The comparator for the leaderboard reads the score first, in descending order, and reads the name second, in ascending order. Writing the second key into the comparator turns an accident of the input into a stated contract. The chain `Comparator.comparingInt(Player::score).reversed().thenComparing(Player::name)` expresses both keys.

#### Reverse One Key Without Reversing The Others

A **descending key** reverses the order of one key. The method `reversed()` flips the comparator that it is called on, which here is the score comparator alone. The method `thenComparing` is called afterward, so the name key stays ascending. Calling `reversed()` at the end of the whole chain would reverse both keys.

<!-- names: record, tie rule, descending key -->

#### Sort Rows Stored As Arrays

A matrix such as `int[][] rows` is an array of objects, and each row is itself an `int[]` object. The call `Arrays.sort(rows, comparator)` is therefore legal. The comparator receives two row arrays, reads their cells, and returns an `int`. The sort swaps references to rows and never copies cells.

<!-- stage: variables -->
### The Record, Its Keys And Their Order

The comparator reads a few named pieces.

- **record** is one object that holds every field of one item, so a sort moves the fields together.
- **primary key** is the first field that the comparator reads.
- **tie key** is the field that the comparator reads only when the primary keys are equal.
- **direction** says whether a key sorts ascending or descending.

None of these pieces changes while the sort runs.

<!-- stage: trace -->
### Sorting Four Players By Score And Name

#### The Comparator Reads One Key Or Two

Take the players `Ana 90`, `Bo 85`, `Cy 90` and `Di 85`. The comparator reads the scores first. For `Bo` and `Ana` the scores differ, so the score alone decides, and `Ana` goes first. For `Ana` and `Cy` the scores tie at 90, so the comparator reads the names and `Ana` goes before `Cy`.

#### Sorting Rows As Arrays

Now take the rows `[2, 5]`, `[1, 3]` and `[2, 9]`. The comparator reads column 0 first, in ascending order. The rows `[2, 5]` and `[2, 9]` tie there, so it reads column 1 in descending order and puts `[2, 9]` first. The sorted rows are `[1, 3]`, `[2, 9]`, `[2, 5]`.

#### Stepping Through Both Sorts

```trace
{"cells":["Ana 90","Bo 85","Cy 90","Di 85"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"order":"['Ana 90', 'Bo 85', 'Cy 90', 'Di 85']"},"note":"Start: the first item forms a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"compare":"Bo 85 vs Ana 90","order":"['Ana 90', 'Bo 85', 'Cy 90', 'Di 85']"},"note":"The scores 85 and 90 differ, so the score decides. Bo 85 stays after Ana 90. Stop this insertion."},{"at":{"i":2,"j":1},"vars":{"compare":"Cy 90 vs Bo 85","order":"['Ana 90', 'Bo 85', 'Cy 90', 'Di 85']"},"note":"The scores 90 and 85 differ, so the score decides. Cy 90 goes before Bo 85. Swap them."},{"at":{"i":2,"j":0},"vars":{"compare":"Cy 90 vs Ana 90","order":"['Ana 90', 'Cy 90', 'Bo 85', 'Di 85']"},"note":"The scores tie at 90, so the name decides. Cy 90 stays after Ana 90. Stop this insertion."},{"at":{"i":3,"j":2},"vars":{"compare":"Di 85 vs Bo 85","order":"['Ana 90', 'Cy 90', 'Bo 85', 'Di 85']"},"note":"The scores tie at 85, so the name decides. Di 85 stays after Bo 85. Stop this insertion."},{"at":{"i":4,"j":-1},"vars":{"order":"['Ana 90', 'Cy 90', 'Bo 85', 'Di 85']"},"note":"The sort ends. Every adjacent pair follows the comparator."}]}
```

```trace
{"cells":["[2, 5]","[1, 3]","[2, 9]"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"order":"['[2, 5]', '[1, 3]', '[2, 9]']"},"note":"Start: the first item forms a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"compare":"[1, 3] vs [2, 5]","order":"['[2, 5]', '[1, 3]', '[2, 9]']"},"note":"The first columns 1 and 2 differ, so column 0 decides. [1, 3] goes before [2, 5]. Swap them."},{"at":{"i":2,"j":1},"vars":{"compare":"[2, 9] vs [2, 5]","order":"['[1, 3]', '[2, 5]', '[2, 9]']"},"note":"The first columns tie at 2, so column 1 decides in descending order. [2, 9] goes before [2, 5]. Swap them."},{"at":{"i":2,"j":0},"vars":{"compare":"[2, 9] vs [1, 3]","order":"['[1, 3]', '[2, 9]', '[2, 5]']"},"note":"The first columns 2 and 1 differ, so column 0 decides. [2, 9] stays after [1, 3]. Stop this insertion."},{"at":{"i":3,"j":-1},"vars":{"order":"['[1, 3]', '[2, 9]', '[2, 5]']"},"note":"The sort ends. Every adjacent pair follows the comparator."}]}
```

<!-- stage: code -->
### One Comparator With Two Keys

#### Players And Rows

```java
final class Roster {
    record Player(String name, int score) {}

    static void sortPlayers(Player[] players) {
        Arrays.sort(players, Comparator.comparingInt(Player::score).reversed()
                .thenComparing(Player::name));
    }

    static void sortRows(int[][] rows) {
        Arrays.sort(rows, (p, q) -> p[0] != q[0]
                ? Integer.compare(p[0], q[0])
                : Integer.compare(q[1], p[1]));
    }
}
```

#### What The Methods Cost

Each sort makes O(n log n) comparisons, and each comparison reads at most two fields. Sorting rows moves n references and no cells. The extra space is that of the library sort, plus the n record objects that the program already holds.

<!-- stage: applicability -->
### When Records Need A Comparator

#### Look For Several Fields And A Priority

Use a comparator over records whenever an item has several fields and the problem states which field decides first. The invariant is that all fields of an item move together and that every pair of items has one stated order, including pairs with equal primary keys. Write the full list of keys before writing code.

#### Where Separate Arrays Or Missing Tie Keys Fail

A false friend is the pair of parallel arrays, because any step that reorders one array and not the other breaks the pairing. Another false friend is a comparator with one key on data that has ties. Its output then depends on the input order. If the problem does not say which tied item goes first, state a tie key anyway, so that the output is deterministic and testable.

#### Java Details That Cause Failures

A comparator for `int[]` elements works only when the array holds the elements as an object, as `int[][]` does. A key stored as `int` that is negated for descending order fails for `Integer.MIN_VALUE`, so use `reversed()` or swap the arguments. Strings compare by `compareTo`, which orders by UTF-16 code unit and puts every uppercase letter before every lowercase letter.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Scores (Author exercise)
<!-- id: so-sort-scores -->

**Prerequisites.** Records, the tie rule and the descending key from this lesson.

**Problem.** Let `names` and `scores` be arrays of the same length, where `scores[i]` belongs to `names[i]`. Return the names ordered by score from highest to lowest. Order names with equal scores alphabetically by `compareTo`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= names.length == scores.length <= 10^4`.
- **Names** are distinct non-empty strings.
- **Scores** are 32-bit integers, and negative scores are legal.
- **Mutation** of the input arrays is not allowed.

**Example 1.** Input `names = ["Ana", "Bo", "Cy"]`, `scores = [70, 90, 80]`, output `["Bo", "Cy", "Ana"]`.

**Example 2.** Input `names = ["Zed", "Amy", "Bob"]`, `scores = [5, 5, 9]`, output `["Bob", "Amy", "Zed"]`.

**Hint.** Which structure keeps each name with its score while the sort runs, and which key reads the tie?

**Changed decision.** Basic case: two parallel arrays become one array of records, and a second key resolves ties.

#### [Vary] Reorder Data In Log Files (LeetCode 937)
<!-- id: so-reorder-logs -->

**Prerequisites.** Sort Scores above.

**Problem.** Let `logs` be an array of strings, each of the form `identifier rest`, where `rest` is a nonempty string. A log is a digit-log when the first character of `rest` is a digit, and a letter-log otherwise. Return the logs with all letter-logs first. Order letter-logs by `rest` and then by identifier, both by `compareTo`. Place the digit-logs after them in their original order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= logs.length <= 100`.
- **Identifier** is a nonempty string without spaces.
- **Rest** contains single spaces between words, and all words of one log are either all digits or all lowercase letters.
- **Mutation** of `logs` is not allowed.

**Example 1.** Input `logs = ["d1 8 1", "l2 art can", "l1 art can", "d2 3"]`, output `["l1 art can", "l2 art can", "d1 8 1", "d2 3"]`.

**Example 2.** Input `logs = ["a1 9", "b1 z", "a2 a"]`, output `["a2 a", "b1 z", "a1 9"]`.

**Hint.** Which logs does the comparator need to order, and which logs keep the position that they had?

**Changed decision.** The identifier is read only after the content ties, and one group of items bypasses the comparator.

#### [Boundary] Equal Primary Keys (Author exercise)
<!-- id: so-sort-rows -->

**Prerequisites.** The two exercises above.

**Problem.** Let `rows` be an array of `int[2]` arrays. Sort `rows` in place by column 0 ascending. Order rows with equal column 0 by column 1 descending.

**Constraints.** The limits are:
- **Length** satisfies `0 <= rows.length <= 10^4`.
- **Rows** each hold exactly two 32-bit integers, and values may be `Integer.MIN_VALUE` or `Integer.MAX_VALUE`.
- **Equal rows** may occur and are interchangeable.
- **Mutation** of `rows` in place is required.

**Example 1.** Input `rows = [[2, 5], [1, 3], [2, 9], [1, 3]]`, output `[[1, 3], [1, 3], [2, 9], [2, 5]]`.

**Example 2.** Input `rows = [[0, -2147483648], [0, 2147483647]]`, output `[[0, 2147483647], [0, -2147483648]]`.

**Hint.** Which method compares two columns without subtracting, and how does the comparator reverse only column 1?

**Changed decision.** Rows with equal primary keys need a stated secondary rule, and the elements are arrays, so the sort receives an object array.

#### [Recognize] Queue Reconstruction By Height (LeetCode 406)
<!-- id: so-queue-height -->

**Prerequisites.** All three exercises above.

**Problem.** Let `people` be an array of pairs `[h, k]`. A pair describes a person of height `h` who has exactly `k` people in front of them with height at least `h`. Return a queue, as an array of pairs, in which every person's `k` is correct. The input is guaranteed to have such a queue.

**Constraints.** The limits are:
- **Length** satisfies `1 <= people.length <= 2000`.
- **Heights** satisfy `0 <= h <= 10^6`.
- **Counts** satisfy `0 <= k < people.length`.
- **Answer** is unique, and `people` is not modified.

**Example 1.** Input `people = [[6, 1], [5, 0], [6, 0], [4, 2]]`, output `[[5, 0], [6, 0], [4, 2], [6, 1]]`.

**Example 2.** Input `people = [[3, 1], [3, 0], [3, 2]]`, output `[[3, 0], [3, 1], [3, 2]]`.

**Hint.** If the tallest people are placed first, which people can later insertions disturb, and at which index must a person go?

**Changed decision.** The first sort key makes a position meaningful, because shorter people never change the count of taller people.
