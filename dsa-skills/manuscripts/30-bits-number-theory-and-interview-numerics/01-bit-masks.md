<!-- lesson-kind: standard -->
<!-- lesson-id: bit-masks -->
## Bit Masks

<!-- stage: context -->
### Why Many Yes-Or-No Values Get Clumsy

A file service checks three permissions for every user: read, write and delete. A first version passes three `boolean` values through every method call. A second version adds an execute permission, and every signature changes. Then a review tool must answer a harder question: which permissions do two users share?

A second problem has the same shape. Given two words, the program must decide whether they share any letter. Each word has at most 26 distinct letters, and each letter is either present or absent. The program asks this question for every pair of words in a list of 1,000 words.

Both problems store a small set of yes-or-no facts and then compare sets. One `int` has 32 positions, and one `long` has 64. Here the open question is how one integer can hold many yes-or-no facts and still allow a fast comparison of two such sets.

<!-- stage: naive -->
### Keeping One Boolean Per Fact

The direct approach keeps one `boolean` per fact. A permission set becomes a `boolean[]`, and a word becomes a set of its letters. The two methods below test a permission and test whether two words share a letter.

```java
static boolean hasPermission(boolean[] granted, int which) {
    return granted[which];                       // one array read answers one question
}

static boolean shareLetter(String a, String b) {
    for (int i = 0; i < a.length(); i++) {
        for (int j = 0; j < b.length(); j++) {
            if (a.charAt(i) == b.charAt(j)) {    // compare every letter of a with every letter of b
                return true;
            }
        }
    }
    return false;                                // no letter matched
}
```

The permission test is fast. The trouble is everything else. Combining two permission arrays needs a loop over all positions, and copying an array copies every position. The word test compares every letter of `a` with every letter of `b`, so it costs `a.length() * b.length()` comparisons for one pair.

<!-- stage: bottleneck -->
### Pair Tests Cost Too Many Comparisons

```predict
A list holds 1,000 words, and each word has 1,000 letters. The program tests every pair of words with the nested loops above. About how many letter comparisons does the worst case need?

About 5 * 10^11 comparisons. There are about 500,000 pairs, and each pair needs up to 1,000 * 1,000 = 10^6 letter comparisons. A computer runs roughly 10^9 simple steps per second, so this takes minutes.
```

#### Count The Comparisons

Let `n` be the number of words and `L` the length of the longest word. One pair costs O(L * L) comparisons. The program tests O(n * n) pairs, so the total is O(n * n * L * L). For `n = L = 1,000` the product is 10^12 when every ordered pair is tested. Testing each unordered pair once halves it to the 5 * 10^11 of the guess above.

#### Spot The Repeated Work

The loops compare the same 26 letters again and again. A word of length 1,000 still holds at most 26 distinct letters, so most comparisons repeat an answer the program already knows. The permission arrays waste work in the same way, because each combination loops over every position. The program needs a form of a set that stores all the facts together and compares two sets in one step.

<!-- stage: insight -->
### Store Each Fact As One Bit

#### Define The Bit Mask

A **bit mask** is an integer whose binary digits each record one yes-or-no fact. The value 1 in a digit means yes, and the value 0 means no. A **bit position** is the index of a digit, counted from 0 at the right. For the permissions read, write, delete and execute, assign positions 0, 1, 2 and 3. The mask `0101` in binary, which is the number 5, means read and delete are granted.

<!-- names: bit mask, bit position, complement -->

#### Build The Single-Bit Value

The expression `1 << p` is the integer with only bit position `p` set. It equals 2 raised to the power `p`. Every operation below combines the target mask with this single-bit value, so the other facts never change.

#### Apply The Four Operations

Let `m` be the mask and `b = 1 << p`. The test `(m & b) != 0` asks whether the fact at `p` holds, because AND keeps a digit only when both inputs have a 1 there. The update `m | b` sets the fact, because OR writes a 1 and never erases one. The update `m ^ b` toggles the fact, because XOR flips the one digit where `b` has a 1.

The **complement** of `b` is `~b`, the integer that flips every digit of `b`. It has a 0 at position `p` and a 1 everywhere else. The update `m & ~b` clears the fact at `p`, because AND with the 0 erases that digit and AND with the 1s keeps all others.

#### Compare Two Sets In One Step

Two masks share a fact exactly when `(m1 & m2) != 0`. One AND compares up to 32 facts at once. For words, give letter `'a'` position 0 up to letter `'z'` at position 25. Two words are disjoint exactly when the AND of their masks is 0. The invariant is that bit `p` of a mask is 1 exactly when the fact at `p` holds, and every operation changes only the bit it names.

<!-- stage: variables -->
### Quantities To Track In The Masks

Track these items while reading or building a mask.

- **mask** is an `int` or `long` that holds all facts, with one bit per fact.
- **p** is the bit position of one fact, counted from 0 at the right.
- **bit** is `1 << p` for an `int`, or `1L << p` for a `long`, the value with only position `p` set.
- **wordMask** is the mask for one word, with bit `c - 'a'` set for each letter `c`.

An `int` holds positions 0 to 31, and the position 31 is the sign bit, so a mask that sets it is negative. A `long` holds positions 0 to 63. When a lesson names positions that can pass 31, the code must write `1L << p`. The plain `1 << p` is an `int` expression, and Java reduces its shift distance to the low 5 bits, so `1 << 32` equals 1.

<!-- stage: trace -->
### Follow Flag Changes And Word Masks

Take a flags value with bits 0 and 2 set, which is the number 5. Four operations follow in order. The first sets bit 3, the second clears bit 0, the third toggles bit 2, and the last tests bit 3.

#### Change Four Flags

The cells below list bits 0 to 7 of the starting value, and the pointer `b` marks the bit that each operation touches. Setting bit 3 ORs the value with 8, so 5 becomes 13. Clearing bit 0 ANDs with the complement of 1, so 13 becomes 12. Toggling bit 2 XORs with 4, which removes the 4 and gives 8. The test ANDs 8 with 8, and the nonzero result answers yes.

```trace
{"cells":[1,0,1,0,0,0,0,0],"pointers":["b"],"steps":[{"at":{"b":-1},"vars":{"flags":5},"note":"The starting value is 5, so bits 0 and 2 are set and no operation has run."},{"at":{"b":3},"vars":{"flags":13},"note":"Setting bit 3 ORs the value with 8. The value is now 13."},{"at":{"b":0},"vars":{"flags":12},"note":"Clearing bit 0 ANDs the value with the complement of 1. The value is now 12."},{"at":{"b":2},"vars":{"flags":8},"note":"Toggling bit 2 XORs the value with 4. The value is now 8."},{"at":{"b":3},"vars":{"flags":8,"test":8},"note":"Testing bit 3 ANDs the value with 8. The result is 8, which is not 0, so the answer is yes."}]}
```

#### Build The Mask Of One Word

The second trace reads the word `abca`, which the cells hold as letter positions 0, 1, 2 and 0. The pointer `i` walks the letters, and the variable `mask` shows the mask after each letter. The first letter sets bit 0, the second sets bit 1, and the third sets bit 2. The last letter repeats bit 0, and ORing a bit that is already set changes nothing, so the final mask is 7.

```trace
{"cells":[0,1,2,0],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"mask":0},"note":"The mask starts at 0, so no letter has been seen."},{"at":{"i":0},"vars":{"mask":1},"note":"The letter at position 0 sets bit 0. The mask is 1."},{"at":{"i":1},"vars":{"mask":3},"note":"The letter at position 1 sets bit 1. The mask is 3."},{"at":{"i":2},"vars":{"mask":7},"note":"The letter at position 2 sets bit 2. The mask is 7."},{"at":{"i":3},"vars":{"mask":7},"note":"The letter at position 0 is already set, so the OR leaves the mask unchanged. The mask is 7."}]}
```

The word `abca` and the word `dd` do not share a letter. The mask of `dd` is 8, and `7 & 8` is 0, so one AND proves that the words are disjoint.

<!-- stage: code -->
### Implement Flag Operations And Word Masks

```java
final class Masks {
    static int set(int mask, int p) {
        return mask | (1 << p);                  // OR writes a 1 at position p and keeps the rest
    }

    static int clear(int mask, int p) {
        return mask & ~(1 << p);                 // AND with the complement erases only position p
    }

    static int toggle(int mask, int p) {
        return mask ^ (1 << p);                  // XOR flips only position p
    }

    static boolean test(int mask, int p) {
        return (mask & (1 << p)) != 0;           // nonzero means the fact at p holds
    }

    static long setWide(long mask, int p) {
        return mask | (1L << p);                 // the L suffix keeps positions 32 to 63 valid
    }

    static int wordMask(String word) {
        int mask = 0;
        for (int i = 0; i < word.length(); i++) {
            mask |= 1 << (word.charAt(i) - 'a'); // one bit per distinct letter
        }
        return mask;
    }
}
```

The parentheses around each shift matter, because in Java the operator `&` binds more weakly than `!=`, and `+` binds more tightly than `<<`. The method `test` writes `!= 0` and never `== 1`, since the value of `mask & (1 << p)` is `1 << p`, which equals 1 only for position 0. Each operation costs O(1), and `wordMask` costs O(L) for a word of length `L`.

<!-- stage: applicability -->
### When A Bit Mask Applies

#### Recognize The Pattern

Reach for a mask when a set of yes-or-no facts has a small fixed number of members, up to 32 for an `int` and up to 64 for a `long`. Typical cases are permission flags, letters of the alphabet, chosen items out of a short list, and visited nodes in a small graph. The four operations above return in every later lesson of this chapter.

The invariant to check before coding is that bit `p` is 1 exactly when the fact at `p` holds. Each update must touch only its own bit, and each comparison must treat the mask as a whole set.

#### Watch For The Nearest False Friend

A `HashSet` or `boolean[]` is a false friend when the universe is small. It looks like the natural set type, and it works, but a hash set hashes and boxes each element and cannot compare two sets in one step. Use a hash set when the universe is large or unbounded, such as arbitrary strings. Use a mask when the universe has at most 64 members.

#### Avoid The Java Width Trap

The expression `1 << p` is an `int` even when it is stored into a `long`. A position of 32 or more silently wraps, because Java uses only the low 5 bits of the shift distance for an `int`. Write `1L << p` for any position that can exceed 30. Position 63 of a `long` is the sign bit, so a `long` mask that sets it is negative, and tests must compare with `!= 0` and never with `> 0`.

<!-- stage: exercises -->
### Exercises

#### [Build] Flag Operations (Author exercise)
<!-- id: bt01-flag-ops -->

**Prerequisites.** The four operations and the single-bit value from this lesson.

**Problem.** A flags value is a non-negative `int`. Each operation is a pair `(code, p)`. Code 0 tests whether bit `p` is set, code 1 sets bit `p`, code 2 clears bit `p`, and code 3 toggles bit `p`. Apply the operations in order. Return an `int` array of length 2. Slot 0 holds the final flags value. Slot 1 holds the number of test operations that found their bit set.

**Constraints.** The limits are:
- **`flags`** is an `int` with `0 <= flags < 2^31`.
- **`p`** is an `int` with `0 <= p <= 30`.
- **Operations** number at most `10^5`, and the list may be empty.
- **Return** is an `int[]` of length 2.
- **Mutation** of the operation list is not allowed.

**Example 1.** Input `flags = 5` and operations [[1,3],[2,0],[3,2],[0,3]], output [8,1], because the value goes 13, 12, 8 and the final test finds bit 3 set.

**Example 2.** Input `flags = 0` and operations [[2,5],[0,5],[3,30],[3,30],[0,30]], output [0,0], because clearing a clear bit changes nothing and toggling bit 30 twice restores it.

**Hint.** Which single-bit value does every operation share, and which operator turns it into set, clear or toggle?

**Changed decision.** Baseline case: each operation changes or reads exactly one bit.

#### [Vary] Permission Set (Author exercise)
<!-- id: bt01-permission-set -->

**Prerequisites.** The flag operations exercise above.

**Problem.** Five named permissions have fixed bit positions: `READ` is 0, `WRITE` is 1, `DELETE` is 2, `EXECUTE` is 3 and `ADMIN` is 4. A user receives every permission in a list `grants` and then loses every permission in a list `revokes`. A name can repeat inside a list. Given a list `required`, return `true` exactly when the user ends with every required permission.

**Constraints.** The limits are:
- **Names** are always one of the five permission names above.
- **Lists** `grants`, `revokes` and `required` each hold at most `1,000` names.
- **Empty** `required` returns `true`.
- **Revoking** a permission that was never granted changes nothing.
- **Return** is a `boolean`, and no list is modified.

**Example 1.** Input `grants = ["READ","WRITE","DELETE"]`, `revokes = ["DELETE"]` and `required = ["READ","WRITE"]`, output `true`. With `required = ["READ","DELETE"]` the output is `false`, because `DELETE` was revoked.

**Example 2.** Input `grants = ["READ"]`, `revokes = []` and `required = ["READ","WRITE"]`, output `false`, because the user owns `READ` but not `WRITE`, so a test for any shared bit would wrongly say yes.

**Hint.** Build one mask per list. Does "has every required permission" mean one shared bit or all required bits?

**Changed decision.** The operation changes from one bit to a whole set, so the test `(effective & need) != 0` must become an equality with `need`.

#### [Boundary] Position Width (Author exercise)
<!-- id: bt01-position-width -->

**Prerequisites.** The two exercises above and the Java width trap from this lesson.

**Problem.** Given a list of bit positions, return the `long` whose binary digits are 1 exactly at those positions and 0 elsewhere. A position can repeat. Position `p` means the digit worth 2 raised to the power `p`, counted modulo 2^64 in two's complement, so position 63 gives a negative `long`.

**Constraints.** The limits are:
- **Positions** are `int` values with `0 <= p <= 63`.
- **Length** of the list is at most `10^5`, and an empty list returns 0.
- **Duplicates** set the same digit once.
- **Return** is a `long`, which may be negative.
- **Mutation** of the list is not allowed.

**Example 1.** Input `[0,40,63]`, output `-9223370937343148031`, because position 63 is the sign digit of a `long`, so the result is negative.

**Example 2.** Input `[32,32]`, output `4294967296`, because the duplicate sets position 32 once, and the form `1 << 32` would give 1 instead.

**Hint.** What type does `1 << p` have, and what happens to its shift distance when `p` is 32 or more?

**Changed decision.** Positions now pass 31, so the single-bit value must be a `long` and the `int` form fails.

#### [Recognize] Disjoint Word Pairs (LeetCode 318)
<!-- id: bt01-disjoint-word-pairs -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `words` of lowercase words, count the index pairs `(i, j)` with `i < j` whose two words share no letter. This lesson changes the contract of LeetCode 318, which asks for the largest product of two word lengths. The later combination lesson of this chapter keeps the original product form, so this version returns a count.

**Constraints.** The limits are:
- **`words.length`** is an `int` with `0 <= n <= 1,000`.
- **Each word** is nonempty, has at most 1,000 letters and uses only `'a'` to `'z'`.
- **Pairs** use two different indexes, and equal words at different indexes count as two words.
- **Return** is an `int`, and fewer than two words return 0.

**Example 1.** Input `["abc","de","cf","ghi"]`, output 5, because only the pair `abc` and `cf` shares a letter among the six pairs.

**Example 2.** Input `["aa","aa","b"]`, output 2, because each `aa` is disjoint from `b`, and the two equal words share the letter `a`.

**Hint.** One mask per word is enough. Which single operation on two masks tells you that two words are disjoint?

**Changed decision.** The answer changes from a maximum product to a count, so every pair is visited and nothing is skipped.
