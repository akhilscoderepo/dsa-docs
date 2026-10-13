<!-- lesson-kind: standard -->
<!-- lesson-id: low-bit -->
## Low Bit

<!-- stage: context -->
### Why Scanning All 32 Positions Wastes Work

A permissions service stores the active flags of one account in a single `int`. Bit 0 means read access, bit 1 means write access, and so on up to bit 31. A billing job must visit every active flag and charge for it. Most accounts have two or three flags on, and a few have almost none.

The job has to find the next active flag again and again. A loop that tests all 32 positions does 32 tests even when one flag is on, and the job runs for millions of accounts every night. Lesson 3 asks how a program can jump straight from one set bit to the next, so that the work matches the number of active flags and not the width of the integer.

<!-- stage: naive -->
### Testing Every Position One By One

The direct approach shifts the value right by each position and checks the last bit. The method below counts the active flags, and the same loop shape visits them.

```java
static int countByScan(int x) {
    int count = 0;
    for (int i = 0; i < 32; i++) {
        if (((x >>> i) & 1) == 1) {     // the unsigned shift moves bit i down to position 0
            count++;                    // one active flag found
        }
    }
    return count;                       // the loop ran 32 times no matter how many flags are on
}
```

The loop uses the unsigned shift `>>>`, so a negative value does not fill the high bits with copies of the sign bit. Every call costs exactly 32 iterations. A value with one flag set costs as much as a value with all 32 flags set.

```predict
An account has only bit 30 set, and every other bit is 0. How many positions does the scan above test before it finds that flag, and how many does it test in total?

The scan tests positions 0 to 30, which is 31 positions, before it finds the flag. It then keeps going and tests position 31 as well, so the total is 32. The loop cannot tell that the remaining positions are all zero, so it never stops early.
```

<!-- stage: bottleneck -->
### The Scan Always Costs 32 Steps

#### Count The Wasted Tests

The scan takes O(w) steps for a word of `w` bits, and `w` is 32 for `int` and 64 for `long`. For one nightly job over 50 million accounts with three flags each, the scan performs 1.6 billion tests to find 150 million flags. About nine tests out of ten find a zero and do no useful work.

#### Why A Fixed Loop Cannot Skip

The loop variable `i` moves one position at a time because the code does not know where the next set bit is. A faster loop would need two things at once. It must find the position of the next set bit without looking at the zeros in between, and it must remove that bit so the next round finds a different one. The cost would then be O(k) for a value with `k` set bits, which is far below O(w) for sparse values. Integer arithmetic can do both steps, because subtracting 1 changes only the bits at and below the lowest set bit.

<!-- stage: insight -->
### Subtract One To Find The Lowest Bit

#### See What Subtraction Does To The Tail

The **lowest set bit** of a number is the 1 bit with the smallest position. Take `x = 180`, which is `10110100` in binary. Its lowest set bit is at position 2. Subtracting 1 borrows from that bit. The bit becomes 0, and the zeros below it become ones. The value `179` is `10110011`. Every bit above position 2 stays the same.

#### Clear The Lowest Set Bit

The expression `x & (x - 1)` keeps the high bits, because both operands agree on them. At position 2 and below, one operand holds a bit and the other holds its complement, so the AND gives 0. For 180 the result is `10110000`, which is 176. The lowest set bit has gone, and nothing else changed. The expression is the **clear step**, and each application removes exactly one set bit. A loop that repeats it until the value reaches 0 runs once per set bit.

<!-- names: lowest set bit, clear step, isolate -->

#### Isolate The Bit With Negation

Java stores negative numbers in two's complement, where `-x` equals `~x + 1`, and `~x + 1` is the complement of `x - 1`. So `-x` and `x - 1` flip the same bits relative to `x`. The expression `x & -x` therefore keeps only the lowest set bit and sets every other bit to 0. To **isolate** the bit means to produce a value with that single bit set. For 180, the result is `00000100`, which is 4. The invariant behind both expressions is that `x & (x - 1)` equals `x` minus its lowest set bit, and `x & -x` equals that removed bit.

#### Use The Smaller Value As A Table Entry

The clear step also gives a recurrence. The value `i & (i - 1)` is smaller than `i` and has exactly one set bit fewer. If the counts for all smaller values are known, then `count[i]` equals `count[i & (i - 1)] + 1`. A single left-to-right pass over `0..n` therefore fills the whole table with O(1) work per entry.

<!-- stage: variables -->
### Quantities To Track In The Loop

Track these items in a clear-step loop.

- **x** is the working `int` value, and the loop ends when it reaches 0.
- **x - 1** is the same value with the lowest set bit turned off and the tail turned on.
- **x & -x** is the isolated lowest set bit, a value that has a single bit set.
- **count** is the number of rounds finished, which equals the number of set bits removed.
- **ans[i]** is the table entry that holds the set bit count of the number `i`.

The loop tests `x != 0`, not `x > 0`. A negative `int` has the sign bit set, and a test with `>` would skip it. The value `Integer.MIN_VALUE` is the one case where `-x` equals `x`, so `x & -x` returns a negative number there. Code that needs the isolated bit as a positive number must widen it with `& 0xFFFFFFFFL`.

<!-- stage: trace -->
### Follow The Clear Step And The Table

#### Remove Every Set Bit From 180

The cells below are the eight low bits of 180, written from the highest position on the left to position 0 on the right. The pointer `bit` marks the set bit that the current round removes. Round one starts with 180, which is `10110100`. The value `x - 1` is `10110011`, and the AND gives `10110000`, so the bit at position 2 is gone. Round two starts with 176, and the lowest set bit is now at position 4. Round three removes position 5, and round four removes position 7. After four rounds the value is 0, which matches the four ones in 180.

```trace
{"cells":[1,0,1,1,0,1,0,0],"pointers":["bit"],"steps":[{"at":{"bit":-1},"vars":{"x":180,"rounds":0},"note":"The loop starts with x = 180, which is 10110100. No round has run yet."},{"at":{"bit":5},"vars":{"x":176,"rounds":1},"note":"Round 1 removes the set bit at position 2. The value x - 1 is 179, and the AND leaves 176."},{"at":{"bit":3},"vars":{"x":160,"rounds":2},"note":"Round 2 removes the set bit at position 4. The value x - 1 is 175, and the AND leaves 160."},{"at":{"bit":2},"vars":{"x":128,"rounds":3},"note":"Round 3 removes the set bit at position 5. The value x - 1 is 159, and the AND leaves 128."},{"at":{"bit":0},"vars":{"x":0,"rounds":4},"note":"Round 4 removes the set bit at position 7. The value x - 1 is 127, and the AND leaves 0. The value is 0, so the loop stops."}]}
```

#### Fill The Table For Eight

The cells below show the finished table for the numbers 0 to 8. Entries to the right of the pointer `i` are not read yet when the pointer arrives there. For `i = 5`, the number 5 is `101`, and `5 & 4` is 4, so the entry at index 4 plus one gives 2. For `i = 7`, the number 7 is `111`, and `7 & 6` is 6, whose count is 2, so the entry is 3. The number 8 clears down to 0, so its entry is one.

```trace
{"cells":[0,1,1,2,1,2,2,3,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prev":0,"ans":0},"note":"The entry for 0 is 0 and serves as the base case."},{"at":{"i":1},"vars":{"prev":0,"ans":1},"note":"The number 1 is 1 in binary. Clearing its lowest set bit gives 0, whose entry is 0, so the entry for 1 is 1."},{"at":{"i":2},"vars":{"prev":0,"ans":1},"note":"The number 2 is 10 in binary. Clearing its lowest set bit gives 0, whose entry is 0, so the entry for 2 is 1."},{"at":{"i":3},"vars":{"prev":2,"ans":2},"note":"The number 3 is 11 in binary. Clearing its lowest set bit gives 2, whose entry is 1, so the entry for 3 is 2."},{"at":{"i":4},"vars":{"prev":0,"ans":1},"note":"The number 4 is 100 in binary. Clearing its lowest set bit gives 0, whose entry is 0, so the entry for 4 is 1."},{"at":{"i":5},"vars":{"prev":4,"ans":2},"note":"The number 5 is 101 in binary. Clearing its lowest set bit gives 4, whose entry is 1, so the entry for 5 is 2."},{"at":{"i":6},"vars":{"prev":4,"ans":2},"note":"The number 6 is 110 in binary. Clearing its lowest set bit gives 4, whose entry is 1, so the entry for 6 is 2."},{"at":{"i":7},"vars":{"prev":6,"ans":3},"note":"The number 7 is 111 in binary. Clearing its lowest set bit gives 6, whose entry is 2, so the entry for 7 is 3."},{"at":{"i":8},"vars":{"prev":0,"ans":1},"note":"The number 8 is 1000 in binary. Clearing its lowest set bit gives 0, whose entry is 0, so the entry for 8 is 1."}]}
```

The hardest step is the one at `i = 8`. The previous entries grow in count, and then the count falls back to 1 because 8 is a power of two. The clear step removes its only set bit and lands on the entry for 0.

<!-- stage: code -->
### Implement Clear, Isolate And Count

```java
static int clearLowest(int x) {
    return x & (x - 1);                  // removes the lowest set bit; the value 0 stays 0
}

static int isolateLowest(int x) {
    return x & -x;                       // keeps only the lowest set bit; negative for MIN_VALUE
}

static int countSetBits(int x) {
    int count = 0;
    while (x != 0) {                     // the test is != 0 so negative values still run
        x &= (x - 1);                    // each round removes exactly one set bit
        count++;                         // the loop runs once per set bit, not once per position
    }
    return count;
}

static int[] countUpTo(int n) {
    int[] ans = new int[n + 1];          // ans[0] stays 0
    for (int i = 1; i <= n; i++) {
        ans[i] = ans[i & (i - 1)] + 1;   // i & (i - 1) is smaller, so its entry is already filled
    }
    return ans;
}
```

The call `clearLowest(0)` returns 0, because `0 - 1` is `-1` with every bit set and `0 & -1` is 0. The loop in `countSetBits` terminates because each round lowers the number of set bits by one. The table method reads only entries below `i`, which makes the single pass correct.

<!-- stage: applicability -->
### When The Low Bit Helps

#### Recognize The Cue

Reach for this trick when a program repeatedly needs the next set bit of a flag word, a mask of chosen items or a visited set. The loop cost then depends on the number of set bits and not on the width of the integer. The same tools also test whether a number is a power of two, because `x > 0 && (x & (x - 1)) == 0` holds exactly for those numbers. The invariant to check is that each round removes one bit and leaves the rest unchanged.

#### Name The False Friend

A shift loop looks like a close alternative, because it also reads the bits one by one. It is a false friend for sparse values, since it always pays for every position. The shift loop remains the right tool when the code needs the position of each bit and not only the count of bits.

#### Watch The Signed Edge

The value `-x` wraps around for `Integer.MIN_VALUE`, so `x & -x` yields `Integer.MIN_VALUE`, a negative number. A loop that tests `x > 0` silently ignores every value with bit 31 set. Treat the argument as a 32-bit pattern, test against 0 with `!=`, and widen to `long` before comparing the isolated bit with other positive values.

<!-- stage: exercises -->
### Exercises

#### [Build] Clear One Set Bit (Author exercise)
<!-- id: bt03-clear-low-bits -->

**Prerequisites.** The clear step `x & (x - 1)` from this lesson.

**Problem.** Given a non-negative integer `x` and a non-negative integer `k`, apply the clear step to `x` up to `k` times, stopping early when the value reaches 0. Return the final value. The clear step replaces `x` by `x & (x - 1)`.

**Constraints.** The limits are:
- **`x`** is an `int` with `0 <= x <= 2^31 - 1`.
- **`k`** is an `int` with `0 <= k <= 100`.
- **Return** is an `int`.
- **Zero** input returns 0 for every `k`.

**Example 1.** Input `x = 180` and `k = 2`, output 160. The value 10110100 loses its two lowest ones and becomes 10100000.

**Example 2.** Input `x = 7` and `k = 5`, output 0. The value has three set bits, so the loop stops at 0 after three rounds.

**Hint.** Write `x` in binary and cross out the lowest 1 once per round.

**Changed decision.** Baseline case: one round removes one bit, and the loop stops at 0.

#### [Vary] Number of 1 Bits (LeetCode 191)
<!-- id: bt03-count-set-bits -->

**Prerequisites.** The first exercise above.

**Problem.** Given a non-negative integer `n`, return the number of bits equal to 1 in its binary representation. The intended method performs one round per set bit.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 2^31 - 1`.
- **Return** is an `int` between 0 and 31.
- **Zero** input returns 0.

**Example 1.** Input `n = 180`, output 4, because 10110100 contains four ones.

**Example 2.** Input `n = 2147483647`, output 31, because every value bit is set and the loop runs 31 rounds.

**Hint.** What does the loop count if each round clears exactly one set bit?

**Changed decision.** The result is the number of rounds, so the output is a count and not a value.

#### [Boundary] Zero And Negative Int (Author exercise)
<!-- id: bt03-lowest-bit-signed -->

**Prerequisites.** The first two exercises above.

**Problem.** Treat an `int` `x` as a fixed 32-bit two's complement pattern. Return the lowest set bit of that pattern as a non-negative `long`, so that bit 31 gives 2147483648. Return 0 when the pattern has no set bit.

**Constraints.** The limits are:
- **`x`** is any `int`, including negative values and `Integer.MIN_VALUE`.
- **Return** is a `long` between 0 and 2^31.
- **Zero** input returns 0.
- **Mutation** of the input is not applicable, since it is a value.

**Example 1.** Input `x = -8`, output 8, because the pattern ends in three zeros and the lowest one is at position 3.

**Example 2.** Input `x = -2147483648`, output 2147483648, because only bit 31 is set and the `int` result of `x & -x` is negative.

**Hint.** What does `-x` produce for the most negative `int`, and how do you widen a negative `int` to a non-negative `long`?

**Changed decision.** The input may be negative, so the result must not depend on the sign.

#### [Recognize] Counting Bits (LeetCode 338)
<!-- id: bt03-count-bits-table -->

**Prerequisites.** The first three exercises above.

**Problem.** Given an integer `n`, return an array `ans` of length `n + 1` such that `ans[i]` is the number of 1 bits in the binary representation of `i`, for every `i` from 0 to `n`. The intended method fills the array in one pass, and each entry reads one earlier entry.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 10^5`.
- **Return** is a new `int[]` of length `n + 1`.
- **Entry 0** is 0.

**Example 1.** Input `n = 8`, output `[0,1,1,2,1,2,2,3,1]`, where the last entry restarts at 1 because 8 is a single set bit.

**Example 2.** Input `n = 0`, output `[0]`, a single entry for the number 0.

**Hint.** Which smaller number do you get by clearing the lowest set bit of `i`?

**Changed decision.** The program fills a table, so each answer reuses an earlier answer.
