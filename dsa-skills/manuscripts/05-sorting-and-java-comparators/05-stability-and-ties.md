<!-- lesson-kind: standard -->
<!-- lesson-id: stability-and-ties -->
## Keep Equal Items In Order

<!-- stage: context -->
### Support Tickets Served Out Of Turn

A support desk serves tickets by priority, and tickets with the same priority wait in the order they arrived. A sort puts the urgent tickets first, as intended. Then a customer complains that a ticket from the morning was handled after a ticket from the evening, and both had the same priority. The sort did its job on the priority. It said nothing about the arrival order of equal tickets, and the arrival order changed.

Equal keys leave one decision open: which of two tied items goes first. This lesson answers two questions. Which Java sorts promise to keep tied items in arrival order, and how does a program enforce that order when no promise exists?

<!-- stage: naive -->
### Moving The Smallest Item To The Front

The direct method scans for the ticket with the smallest priority number and swaps it to the front. It then repeats on the rest of the array.

```java
final class Desk {
    record Ticket(String id, int priority) {}

    static void sortTickets(Ticket[] tickets) {
        for (int i = 0; i < tickets.length - 1; i++) {
            int smallest = i;
            for (int j = i + 1; j < tickets.length; j++) {
                if (tickets[j].priority() < tickets[smallest].priority()) {
                    smallest = j;
                }
            }
            Ticket tmp = tickets[i];
            tickets[i] = tickets[smallest];
            tickets[smallest] = tmp;
        }
    }
}
```

On tickets with priorities `[2, 2, 1]`, named `A`, `B` and `C` in arrival order, the method puts `C` first. The priorities are in order, so the sort looks correct.

<!-- stage: bottleneck -->
### The Swap Jumps Over Equal Tickets

```predict
In the array `[A2, B2, C1]`, what does the method return, and which of the two priority-2 tickets comes first in the result?

The swap moves C1 to index 0 and sends A2 to index 2. The result is `[C1, B2, A2]`, so B2 now comes before A2 although A2 arrived first. The swap carried A2 over B2, which is a ticket with the same priority.
```

A swap exchanges two items that can sit far apart, so it passes over every item between them. When an item between them ties with the item that moves, the tied items change order. The method also runs O(n^2) comparisons. A sort needs a property that forbids such jumps over equal keys. It must also run in O(n log n) time.

<!-- stage: insight -->
### Promise The Tie Order Or Store It

The program needs a sort that keeps tied items in input order, or a tie key that makes the order explicit.

#### Stable Sorts Keep Tied Items In Order

A sort is **stable** when two items with equal keys stay in their input order. The call `Arrays.sort(Object[])` and the call `List.sort` are stable, and the documentation promises it. The call `Arrays.sort(int[])` makes no such promise. For primitives this causes no harm, because two equal `int` values are indistinguishable. A tie order matters only for objects that carry more data than the key.

#### Store The Original Index As A Tie Key

When no stable sort is available, or when a problem wants the tie order written down, the program attaches the **original index** of each item and compares it as the last key. The comparator then reads the key first and the index second. No two items tie, because indexes are distinct. The sorted order is fully determined by the data, and any sort algorithm produces it.

#### Reverse The Comparator, Not The Array

Reversing a stable sorted array flips the order of tied items as well. Reversing the comparator flips the order of the keys and keeps tied items in input order. A requirement such as "highest priority first, ties in arrival order" therefore needs the reversed comparator.

<!-- names: stable, original index, tie order -->

#### Comparator Zero Means Interchangeable

The result zero says that the sort may place either item first. A stable sort fills in an order for such items, namely the input order. If the output must differ for two items that compare as zero, the comparator is missing a key.

<!-- stage: variables -->
### Key, Index And Tie Order

The sort and the comparator use these pieces.

- **key** is the field that the problem ranks, such as the priority.
- **index** is the position that an item had in the input, and it never changes.
- **tie order** is the order of items that have the same key, either the input order of a stable sort or the order of the index.

The key can repeat across items, and the index never repeats.

<!-- stage: trace -->
### Two Sorts Of The Same Tickets

#### The Swap Method Reorders A Tie

Take the tickets `A2`, `B2` and `C1`. The first scan finds `C1` as the smallest and swaps it with `A2`. The array becomes `C1, B2, A2`. The second scan compares `A2` with `B2`, finds no smaller priority, and stops. The pair of priority-2 tickets now has `B2` before `A2`.

#### The Stable Sort Keeps The Tie

A stable insertion sort moves a ticket left only while its priority is strictly smaller than the priority on its left. For `B2` the left neighbor `A2` has an equal priority, so `B2` stays. For `C1` the left neighbor `B2` has a larger priority, so `C1` moves left twice. The result is `C1, A2, B2`.

#### Stepping Through Both Sorts

```trace
{"cells":["A2","B2","C1"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"order":"['A2', 'B2', 'C1']"},"note":"Start: the scan looks for the smallest priority from index 0."},{"at":{"i":0,"j":1},"vars":{"smallest":"A2","order":"['A2', 'B2', 'C1']"},"note":"B2 is not smaller than A2, so the smallest stays A2."},{"at":{"i":0,"j":2},"vars":{"smallest":"A2","order":"['A2', 'B2', 'C1']"},"note":"C1 has a smaller priority than A2, so it becomes the smallest."},{"at":{"i":0,"j":2},"vars":{"order":"['C1', 'B2', 'A2']"},"note":"Swap index 0 with index 2. The array is now ['C1', 'B2', 'A2']."},{"at":{"i":1,"j":2},"vars":{"smallest":"B2","order":"['C1', 'B2', 'A2']"},"note":"A2 is not smaller than B2, so the smallest stays B2."},{"at":{"i":3,"j":-1},"vars":{"order":"['C1', 'B2', 'A2']"},"note":"The sort ends. B2 now comes before A2, so the tie order changed."}]}
```

```trace
{"cells":["A2","B2","C1"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"order":"['A2', 'B2', 'C1']"},"note":"Start: the first ticket forms a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"order":"['A2', 'B2', 'C1']"},"note":"B2 is not strictly smaller than A2. It stays, so a tie keeps its order."},{"at":{"i":2,"j":1},"vars":{"order":"['A2', 'B2', 'C1']"},"note":"C1 has a strictly smaller priority than B2. Move it left."},{"at":{"i":2,"j":0},"vars":{"order":"['A2', 'C1', 'B2']"},"note":"C1 has a strictly smaller priority than A2. Move it left."},{"at":{"i":3,"j":-1},"vars":{"order":"['C1', 'A2', 'B2']"},"note":"The sort ends. A2 still comes before B2."}]}
```

<!-- stage: code -->
### A Stable Sort And An Index Key

#### Stable Sort And Explicit Index

```java
final class Desk {
    record Ticket(String id, int priority) {}

    static void sortStable(Ticket[] tickets) {
        Arrays.sort(tickets, Comparator.comparingInt(Ticket::priority));
    }

    static int[] orderByValue(int[] keys) {
        Integer[] positions = new Integer[keys.length];
        for (int i = 0; i < keys.length; i++) {
            positions[i] = i;
        }
        Arrays.sort(positions, (a, b) -> keys[a] != keys[b]
                ? Integer.compare(keys[a], keys[b])
                : Integer.compare(a, b));
        int[] out = new int[keys.length];
        for (int i = 0; i < out.length; i++) {
            out[i] = positions[i];
        }
        return out;
    }
}
```

#### What The Methods Cost

Both sorts make O(n log n) comparisons. The stable object sort needs a buffer of up to n references. The method `orderByValue` boxes n indexes, so its space is O(n).

<!-- stage: applicability -->
### When Tie Order Changes The Answer

#### Ask Who Owns The Tie Order

Ask for each sort what the problem says about equal keys. If tied items are indistinguishable, ignore the question. If the problem names an order, put it in the comparator as a key. If the problem says that the arrival order must stay, use a stable sort and say so in a comment. The invariant is that every pair of items has exactly one defined order.

#### Where Stability Does Not Help

A false friend is the idea that a stable sort fixes every tie problem. A stable sort preserves the order that the input had, and the input order may be arbitrary. If the problem asks for ties in alphabetical order, the comparator needs an alphabetical key. A stable sort does help across two passes: sorting by the second key first and then by the first key, with a stable sort, gives the first key priority and the second key as the tie rule. A sort that is not stable breaks that pairing.

#### Java Details That Cause Failures

The documentation of `Arrays.sort(int[])` makes no promise about the order of equal values, and none is needed for primitives. Never rely on the behavior of a particular implementation. A comparator that returns the difference of two `int` fields can overflow, so use `Integer.compare`. Sorting `Integer[]` with `Collections.reverseOrder()` keeps tied items in input order, because the comparator is reversed and not the array.

<!-- stage: exercises -->
### Exercises

#### [Build] Stable Score Sort (Author exercise)
<!-- id: so-stable-tickets -->

**Prerequisites.** The stable sort from this lesson.

**Problem.** Let `ids` and `priorities` be arrays of the same length, where `priorities[i]` belongs to `ids[i]`. Return the ids ordered by priority from the smallest number to the largest. Ids with equal priority keep their order in `ids`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= ids.length == priorities.length <= 10^4`.
- **Ids** are non-empty strings and may repeat.
- **Priorities** are 32-bit integers.
- **Mutation** of the input arrays is not allowed.

**Example 1.** Input `ids = ["A", "B", "C"]`, `priorities = [2, 2, 1]`, output `["C", "A", "B"]`.

**Example 2.** Input `ids = ["x", "y", "z", "w"]`, `priorities = [5, 1, 5, 1]`, output `["y", "w", "x", "z"]`.

**Hint.** Which sort keeps tied items in input order, and what does the comparator read?

**Changed decision.** Basic case: the comparator reads only the key, and the stable sort supplies the tie order.

#### [Vary] Explicit Index Tie (Author exercise)
<!-- id: so-index-tie -->

**Prerequisites.** Stable Score Sort above.

**Problem.** Let `keys` be an array of integers. Return an array `order` of the indexes `0` to `keys.length - 1`, arranged so that `keys[order[0]] <= keys[order[1]] <= ...`. When two keys are equal, the smaller index comes first. The comparator must state this tie rule and must not rely on stability.

**Constraints.** The limits are:
- **Length** satisfies `0 <= keys.length <= 10^4`.
- **Keys** are 32-bit integers, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Answer** holds each index exactly once.
- **Mutation** of `keys` is not allowed.

**Example 1.** Input `keys = [30, 10, 30, 20]`, output `[1, 3, 0, 2]`.

**Example 2.** Input `keys = [4, 4, 4]`, output `[0, 1, 2]`.

**Hint.** Which array can be sorted so that a comparator looks up each key, and which second field breaks a tie?

**Changed decision.** The sort runs on indexes and not on values, and the tie rule moves into the comparator.

#### [Boundary] Comparator Equality (Author exercise)
<!-- id: so-case-ties -->

**Prerequisites.** The two exercises above.

**Problem.** Let `words` be an array of strings. Return the words sorted by `String.CASE_INSENSITIVE_ORDER`. Break ties between words that differ only in letter case by placing the word that is greater under `compareTo` first, so a lowercase letter comes before its uppercase form. The comparator returns zero only for identical strings.

**Constraints.** The limits are:
- **Length** satisfies `0 <= words.length <= 10^4`.
- **Words** are strings of ASCII letters with length from 0 to 50.
- **Identical words** may repeat and are interchangeable.
- **Mutation** of `words` is not allowed.

**Example 1.** Input `words = ["bee", "Ant", "ant", "Bee"]`, output `["ant", "Ant", "bee", "Bee"]`.

**Example 2.** Input `words = ["a", "A", "a"]`, output `["a", "a", "A"]`.

**Hint.** When the case-insensitive comparison returns zero, which second comparison separates the words, and in which direction?

**Changed decision.** A zero from the first key still leaves different outputs, so the comparator needs a second key.

#### [Recognize] Sort Integers By The Number Of 1 Bits (LeetCode 1356)
<!-- id: so-bit-count -->

**Prerequisites.** All three exercises above.

**Problem.** Let `arr` be an array of non-negative integers. Return the integers sorted by the number of 1 bits in their binary form, from fewest to most. Integers with the same number of 1 bits are ordered by value from smallest to largest.

**Constraints.** The limits are:
- **Length** satisfies `0 <= arr.length <= 10^4`.
- **Values** satisfy `0 <= arr[i] <= 2^31 - 1`.
- **Ties** follow the numeric rule and not the input order.
- **Mutation** of `arr` is not allowed.

**Example 1.** Input `arr = [1024, 3, 2147483647, 6]`, output `[1024, 3, 6, 2147483647]`.

**Example 2.** Input `arr = [5, 5, 0]`, output `[0, 5, 5]`.

**Hint.** Which method counts the 1 bits of an `int`, and which key must follow it so that the order does not depend on the input?

**Changed decision.** The tie rule is numeric and explicit, so the output has one correct order for every input order.
