<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-xor -->
## Prefix XOR

<!-- stage: context -->
### Night Guards And Light Switches

A long corridor has twenty light switches in a row, and each night a guard walks it with a card that lists which switches to flip. A guard flips a switch on the card whether it is currently on or off, so the card only says "flip", never "turn on". Two guards who both flip the same switch leave it as it was, and the corridor's final state depends only on how many times each switch was flipped, odd or even.

The manager keeps the cards in the order the guards came. Now and then she asks: if only the guards from the third to the seventh had walked the corridor, which switches would end up flipped relative to the start? Each card is a number, with one bit per switch, and the manager is tired of combining the same cards again and again for questions that share most of their guards.

<!-- stage: naive -->
### Combine The Cards Of Each Question

The direct approach is to combine the cards from the first guard of the question to the last, flipping bits as it goes.

```java
static int combinedEffect(int[] cards, int first, int last) {
    int effect = 0;
    for (int g = first; g <= last; g++) {
        effect ^= cards[g];
    }
    return effect;
}
```

The XOR operator flips exactly the bits that are set in the card, so the result is the net effect of the guards from the first to the last, including both ends.

<!-- stage: bottleneck -->
### Questions Share Most Of Their Guards

A question covering m guards costs O(m), and a batch of q questions over n guards takes O(q n) when the questions are long, which is ten billion operations for a hundred thousand of each. Many questions begin at the first guard or overlap heavily, so the same flips are recomputed.

The structure that saves the work is that flipping is its own undo: a guard whose card is applied twice leaves nothing behind. If we know the combined effect of the first guards up to the end of a question, and the combined effect of the guards before its start, then applying the second effect on top of the first cancels the early guards and leaves exactly the guards of the question. Each question becomes one combination of two stored values, O(1), after one pass of O(n) that stores the combined effect after each guard.

<!-- stage: insight -->
### Flipping Twice Undoes The Flip

The operator is XOR, written `^`. For any value `x`, `x ^ x` is zero and `x ^ 0` is `x`, and the operator is order-independent. A **prefix XOR** is the XOR of everything before a position, stored with a leading zero slot as before, so `px[i + 1] = px[i] ^ a[i]` and `px[0] = 0`. The XOR of the cards from `left` to `right`, both included, is `px[right + 1] ^ px[left]`. The cards before `left` are in both slots, so they appear twice and cancel to zero, and what is left is the stretch.

This is the same plan as the range-sum table with a different cancellation. Sums cancel by subtraction; XOR cancels by XOR itself, because it is its own inverse. The invariant is that `px[i]` is the XOR of the first `i` values, so the answer for a range is always two lookups and one XOR.

<!-- names: prefix XOR, self-inverse, zero slot -->

Because XOR is **self-inverse**, the counting patterns of earlier lessons carry over. To count stretches whose XOR equals a target `k`, a stretch ending at the current position qualifies when an earlier prefix `e` satisfies `current ^ e == k`, which means `e == current ^ k`. The complement is computed by XOR, not by subtraction, and a frequency table of earlier prefix values supplies the count. The **zero slot** matters here too: a stretch that begins at the first element pairs with the empty prefix, so the table starts with the value zero seen once.

<!-- stage: variables -->
### Prefix Values And The Complement

`px` holds one slot per prefix with `px[0] = 0`, built by XOR-ing each value in turn. For range answers the two slots read are `px[left]` and `px[right + 1]`. For counting, `current` is the prefix through the present element, `need` is `current ^ k`, and `seen` is a map from a prefix value to how often it has occurred, seeded with zero occurring once. Values are `int`, since XOR never grows beyond the width of its operands, so no widening to `long` is needed.

<!-- stage: trace -->
### Building And Counting With XOR

The first trace builds the prefix XOR for the cards 6, 2, 7, 4 and then answers one question, cards from position 1 to position 3. The cells are the cards, the variables show the running XOR, and the final step reads two slots. Focus on that last step: the slots hold 7 and 6, and 7 XOR 6 is 1, which equals 2 XOR 7 XOR 4, the cards of the question.

```trace
{"cells":["6","2","7","4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"card":6,"prefixXor":6},"note":"XOR the card 6 into the running value, which becomes 6, and store it in slot 1."},{"at":{"i":1},"vars":{"card":2,"prefixXor":4},"note":"XOR the card 2 into the running value, which becomes 4, and store it in slot 2."},{"at":{"i":2},"vars":{"card":7,"prefixXor":3},"note":"XOR the card 7 into the running value, which becomes 3, and store it in slot 3."},{"at":{"i":3},"vars":{"card":4,"prefixXor":7},"note":"XOR the card 4 into the running value, which becomes 7, and store it in slot 4."},{"at":{"i":3},"vars":{"slotHigh":7,"slotLow":6,"answer":1},"note":"The query covers positions 1 to 3, so read slot 4, which holds 7, and slot 1, which holds 6. Their XOR is 1."}]}
```

The second trace counts the stretches of 4, 2, 2, 6, 4 whose XOR is 6. The variables show the prefix, the complement `current ^ 6`, and how many earlier prefixes match. Look at the fourth element: the prefix is 2, the complement is 4, and the value 4 has been a prefix twice before, so two stretches end there.

```trace
{"cells":["4","2","2","6","4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":4,"need":2,"found":0,"count":0},"note":"The prefix is 4 and the complement 4 XOR 6 is 2. It occurred 0 times before, so the count is 0."},{"at":{"i":1},"vars":{"prefix":6,"need":0,"found":1,"count":1},"note":"The prefix is 6 and the complement 6 XOR 6 is 0. It occurred 1 times before, so the count is 1."},{"at":{"i":2},"vars":{"prefix":4,"need":2,"found":0,"count":1},"note":"The prefix is 4 and the complement 4 XOR 6 is 2. It occurred 0 times before, so the count is 1."},{"at":{"i":3},"vars":{"prefix":2,"need":4,"found":2,"count":3},"note":"The prefix is 2 and the complement 2 XOR 6 is 4. It occurred 2 times before, so the count is 3."},{"at":{"i":4},"vars":{"prefix":6,"need":0,"found":1,"count":4},"note":"The prefix is 6 and the complement 6 XOR 6 is 0. It occurred 1 times before, so the count is 4."}]}
```

<!-- stage: code -->
### XOR Tables And XOR Counts

```java
static int[] buildXorTable(int[] a) {
    int[] px = new int[a.length + 1];
    for (int i = 0; i < a.length; i++) px[i + 1] = px[i] ^ a[i];
    return px;
}

static int rangeXor(int[] px, int left, int right) {
    return px[right + 1] ^ px[left];
}

static int countXorK(int[] a, int k) {
    Map<Integer, Integer> seen = new HashMap<>();
    seen.put(0, 1);
    int current = 0, count = 0;
    for (int x : a) {
        current ^= x;
        count += seen.getOrDefault(current ^ k, 0);
        seen.merge(current, 1, Integer::sum);
    }
    return count;
}

static long countEqualHalves(int[] a) {
    Map<Integer, long[]> seen = new HashMap<>();
    seen.put(0, new long[] {1, 0});
    int current = 0;
    long total = 0;
    for (int p = 1; p <= a.length; p++) {
        current ^= a[p - 1];
        long[] slot = seen.computeIfAbsent(current, v -> new long[2]);
        total += slot[0] * (p - 1) - slot[1];
        slot[0]++;
        slot[1] += p;
    }
    return total;
}
```

Each function scans the cards once, at constant expected cost per card. The table and range functions take O(n) space and the maps take space proportional to the number of distinct prefixes. The last function sums, for every pair of equal prefixes, the number of positions strictly between them, using a count and a running sum of earlier positions.

<!-- stage: applicability -->
### When Toggles Combine By Parity

Use prefix XOR when a question combines values by XOR, or by any operation that undoes itself, and asks about contiguous stretches. The invariant is that each prefix value is the XOR of all earlier values, so two equal prefix values enclose a stretch whose XOR is zero, and a stretch with XOR `k` encloses prefixes differing by `k`.

A false friend is applying the sum rules by habit: subtracting two XOR prefixes gives garbage, since the cancellation is by XOR. Another is the operation that cannot be undone, such as OR or AND, for which no prefix table recovers a range. A third is forgetting the leading zero slot, which loses every stretch that starts at the first element.

In Java, `^` has lower precedence than `==` in a comparison chain, so write parentheses around an XOR inside a condition. XOR on `int` stays within `int`, so no widening is needed, but a count of pairs can grow past `int`, and the last function above uses `long` for that reason. Use `getOrDefault` for a missing prefix.

<!-- stage: exercises -->
### Exercises

#### [Build] XOR Log (LeetCode 1310)
<!-- id: ps-xor-log -->

**Prerequisites.** The range queries lesson, and the XOR operator from Chapter 00.

**Problem.** The earlier version of this task gave the array up front. Now values arrive one at a time. Design a log with `append(value)` and `query(left, right)`, which returns the XOR of the values at positions `left` through `right`, both included, among the values appended so far. Each call must take constant time.

**Constraints.** Up to 100000 calls, 0 <= value <= 1000000000, and every query satisfies 0 <= left <= right < number of values appended.

**Example 1.** Input appends of 6, 2, 7, 4 and then `query(1, 3)`, output 1.

**Example 2.** Input appends of 9, 9 and then `query(0, 1)`, output 0.

**Hint.** What must be stored when a value is appended? Which two stored values answer a query?

**Changed decision.** First rung: the table grows online, one slot per append, and the cancellation is by XOR instead of subtraction.

#### [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Prerequisites.** The XOR Log exercise above, and the prefix counts lesson.

**Problem.** Given an array of non-negative integers and a target `k`, return the number of non-empty contiguous stretches whose XOR equals `k`. Keep a table of how many times each prefix XOR has occurred, and look up the complement `current ^ k` before recording the current prefix.

**Constraints.** 1 <= arr.length <= 100000 and 0 <= arr[i], k <= 1000000000.

**Example 1.** Input `arr = [4, 2, 2, 6, 4], k = 6`, output 4.

**Example 2.** Input `arr = [0, 0], k = 0`, output 3.

**Hint.** If `current ^ earlier == k`, what is `earlier`? Which prefix value is present before any element is read?

**Changed decision.** The complement is found by XOR, not subtraction, and the table counts occurrences as in the count lesson.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Prerequisites.** The two exercises above.

**Problem.** Decide whether any non-empty contiguous stretch has XOR exactly `k`, using a set of seen prefix values. Show that a set that starts empty misses the stretch that begins at the first element, and that starting it with the value zero fixes the answer.

**Constraints.** 1 <= arr.length <= 100000 and 0 <= arr[i], k <= 1000000000.

**Example 1.** Input `arr = [5], k = 5`, output true.

**Example 2.** Input `arr = [1, 2, 4], k = 8`, output false.

**Hint.** What is the prefix before the first element? For `arr = [5]`, which earlier prefix does the first element need?

**Changed decision.** The empty prefix is a real earlier value, so the set begins with zero before any element is read.

#### [Recognize] Count Triplets That Can Form Two Arrays of Equal XOR (LeetCode 1442)
<!-- id: ps-equal-xor-triplets -->

**Prerequisites.** All three exercises above.

**Problem.** Count the triples of indices `(i, j, k)` with `i < j <= k` such that the XOR of the values from `i` to `j - 1` equals the XOR of the values from `j` to `k`. Two equal halves mean the whole stretch from `i` to `k` has XOR zero, so each pair of equal prefix values encloses as many triples as there are choices for the split point.

**Constraints.** 1 <= arr.length <= 300 and 1 <= arr[i] <= 100000000. A solution that is linear in the length is welcome, but not required.

**Example 1.** Input `arr = [2, 3, 1, 6, 7]`, output 4.

**Example 2.** Input `arr = [1, 1, 1, 1, 1]`, output 10.

**Hint.** What does it say about the whole stretch if its two halves have the same XOR? How many split points does a stretch of a given length have?

**Changed decision.** The question is rewritten as zero-XOR stretches, and every stretch contributes a number of triples that depends on its length.
