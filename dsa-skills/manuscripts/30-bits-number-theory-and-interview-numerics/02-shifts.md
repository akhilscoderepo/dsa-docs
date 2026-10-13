<!-- lesson-kind: standard -->
<!-- lesson-id: shifts -->
## Shifts

<!-- stage: context -->
### Why Reading One Bit Goes Wrong

A graphics routine stores a pixel color in one `int`: eight bits for red, eight for green and eight for blue. The routine must read the green part of millions of pixels. A network routine does the opposite and must pack a small user id and a small counter into one `int`, so a table stores one number per record.

Both routines ask for a bit or a group of bits at a known position in a binary number. A first attempt uses arithmetic on the decimal value. That attempt works for small positive values, and it fails on negative values. Here the open question is how to move binary bits to a known position and read them back, negative numbers included.

<!-- stage: naive -->
### Dividing And Taking Remainders

The direct approach uses division and remainder with powers of two. To read bit `i`, the method divides by 2 raised to the power `i` and takes the remainder by 2. The method below does that with a loop, and the second method counts bits the same way.

```java
static int digitAt(int x, int i) {
    int value = x;
    for (int step = 0; step < i; step++) {
        value = value / 2;               // each division drops the lowest bit
    }
    return value % 2;                    // the remainder by 2 is the bit now at the right
}

static int countOnes(int x) {
    int ones = 0;
    while (x != 0) {
        ones += x % 2;                   // add the lowest bit
        x = x / 2;                       // drop the lowest bit
    }
    return ones;
}
```

For `x = 180` and `i = 2`, the loop gives 45 after two divisions, and `45 % 2` is 1, which is correct. For small positive values, both methods work. They also spend one loop step per bit position, so a read at position 30 runs 30 divisions.

The next step needs the two's complement form, which Java uses for every `int`. Bit position `p` below 31 has weight 2 raised to the power `p`. The top bit, position 31, has weight negative 2 raised to the power 31. The value is the sum of the weights of the bits that are 1. To negate a number, flip every bit and add 1, so `-x` equals `~x + 1`. For 3, the pattern `0...011` flips to `1...100`, and adding 1 gives `1...101`, which is -3. The top bit contributes -2^31, and positions 2 to 30 add 2^31 - 4, so those bits sum to -4. Bit 0 adds 1 to reach -3. The same sum shows why -3 ends in a 1 bit, because -4 is even and only bit 0 can make the total odd.

<!-- stage: bottleneck -->
### Loops And Negative Remainders

```predict
What does the method digitAt return for x = -3 and i = 0? The two's complement form of -3 ends in a 1 bit.

It returns -1. In Java, the remainder of a negative number is zero or negative, so -3 % 2 is -1. The method never returns a bit for negative input, and the sign breaks every comparison with 1.
```

#### Count The Steps

Reading bit `i` costs `i` divisions, so one read costs O(i), up to O(w) for a number of `w` bits. A routine that reads every bit of a 32-bit number does 0 + 1 + ... + 31 divisions, which is O(w * w) work. A single operation on the hardware could do the same job.

#### Find The Sign Problem

Java stores an `int` in two's complement, and division rounds toward zero. For `x = -3`, the division `x / 2` gives -1, and `x % 2` gives -1. Neither value is a bit. A routine that tests `x % 2 == 1` misses every odd negative number. The program needs operators that treat the stored bits directly, with no decimal arithmetic in between, and that state clearly what they put into the vacated positions.

<!-- stage: insight -->
### Move Bits With Shift Operators

#### Define The Left Shift

The **left shift** `x << k` moves every bit of `x` up by `k` positions and fills the `k` lowest positions with 0. For nonnegative values below the overflow limit, it equals `x` times 2 raised to the power `k`. The value `3 << 2` is 12, because `11` becomes `1100`. The left shift builds the single-bit value `1 << p` that the previous lesson used.

<!-- names: left shift, signed right shift, zero-fill right shift -->

#### Define The Two Right Shifts

The **signed right shift** `x >> k` moves every bit down by `k` positions and copies the top bit, which is the sign, into the vacated high positions. A negative number stays negative, and `-8 >> 1` is -4. For a nonnegative `x`, it equals `x` divided by 2 raised to the power `k`, rounded down. For a negative `x`, it rounds toward negative infinity, so `-3 >> 1` is -2 and not -1.

The **zero-fill right shift** `x >>> k` moves every bit down by `k` positions and fills the vacated high positions with 0. The result of `-8 >>> 1` is the large positive number 2147483644. Use `>>>` whenever the bits are a bit pattern and the sign carries no meaning.

#### Combine Shift And Mask To Read Bits

To read bit `i`, shift the number right by `i` positions and keep only the lowest bit. The expression is `(x >> i) & 1`. The shift brings bit `i` to position 0, and the AND with 1 erases every other bit. Because only position 0 survives, the choice between `>>` and `>>>` does not matter here, and both give the same result for `i` from 0 to 31.

To read a group of `w` bits starting at position `i`, use `(x >>> i) & ((1 << w) - 1)`. The value `(1 << w) - 1` is a run of `w` ones. To write a group, shift the field left by its starting position and combine with OR. The invariant is that a shift moves every bit by the same distance, and the two right shifts differ only in what fills the high positions.

<!-- stage: variables -->
### Quantities To Track In The Shifts

Track these items while moving bits.

- **x** is the `int` whose bits are read or written.
- **k** is the shift distance, and Java reads only its low 5 bits for an `int`.
- **position** is the index of a bit, counted from 0 at the right.
- **width** is the number of bits in a field, and `(1 << width) - 1` is its run of ones.

For an `int`, the shift distance `k` is reduced to `k & 31`. The expression `x << 32` therefore equals `x`, and `x >>> 32` equals `x`. For a `long`, Java reduces the distance to `k & 63`. The type of the left operand decides the result type, so `1 << 40` is an `int` and `1L << 40` is a `long`.

<!-- stage: trace -->
### Follow Bit Reads And Shifts

The first trace reads bits of the number 180. The second trace compares the two right shifts on -16.

#### Read Bits Of 180

The number 180 is `10110100` in binary. The cells below hold its eight bits from position 0 to position 7. The first cell is the lowest bit, so the cells read from right to left compared with the binary text. The pointer `i` marks the position that a read targets. For `i = 2`, the shift `180 >> 2` gives 45, and `45 & 1` is 1. For `i = 3`, the shift gives 22, and the result is 0. For `i = 7`, the shift gives 1, and the result is 1.

```trace
{"cells":[0,0,1,0,1,1,0,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"x":180},"note":"The cells show positions 0 to 7 of 180, and no read has run."},{"at":{"i":2},"vars":{"shifted":45,"bit":1},"note":"The shift 180 >> 2 gives 45. The AND with 1 keeps only the lowest bit, which is 1."},{"at":{"i":3},"vars":{"shifted":22,"bit":0},"note":"The shift 180 >> 3 gives 22. The AND with 1 keeps only the lowest bit, which is 0."},{"at":{"i":7},"vars":{"shifted":1,"bit":1},"note":"The shift 180 >> 7 gives 1. The AND with 1 keeps only the lowest bit, which is 1."}]}
```

#### Compare Right Shifts Of A Negative Number

The number -16 has a 1 in positions 4 to 31 and a 0 in positions 0 to 3. The cells below list, from smallest to largest, the shift distances 0, 4, 8, 12, 16, 20, 24, 28 and 31, and the pointer `s` marks the current distance. At distance 0 both shifts return -16, because a shift by 0 moves nothing. At distance 4 the signed shift gives -1, because the high positions copy the sign, and the zero-fill shift gives 268435455. The signed shift then stays at -1 for every larger distance. The zero-fill shift keeps halving its value and reaches 1 at distance 31.

```trace
{"cells":[0,4,8,12,16,20,24,28,31],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"signed":-16,"zeroFill":-16},"note":"With distance 0 both shifts return -16."},{"at":{"s":1},"vars":{"signed":-1,"zeroFill":268435455},"note":"The signed shift copies the sign into the top positions and gives -1. The zero-fill shift puts zeros there and gives 268435455."},{"at":{"s":2},"vars":{"signed":-1,"zeroFill":16777215},"note":"The signed shift stays at -1. The zero-fill shift gives 16777215."},{"at":{"s":3},"vars":{"signed":-1,"zeroFill":1048575},"note":"The signed shift stays at -1. The zero-fill shift gives 1048575."},{"at":{"s":4},"vars":{"signed":-1,"zeroFill":65535},"note":"The signed shift stays at -1. The zero-fill shift gives 65535."},{"at":{"s":5},"vars":{"signed":-1,"zeroFill":4095},"note":"The signed shift stays at -1. The zero-fill shift gives 4095."},{"at":{"s":6},"vars":{"signed":-1,"zeroFill":255},"note":"The signed shift stays at -1. The zero-fill shift gives 255."},{"at":{"s":7},"vars":{"signed":-1,"zeroFill":15},"note":"The signed shift stays at -1. The zero-fill shift gives 15."},{"at":{"s":8},"vars":{"signed":-1,"zeroFill":1},"note":"The signed shift stays at -1. The zero-fill shift reaches 1, the sign bit alone."}]}
```

A loop that waits for `x >> 1` to reach 0 never ends for a negative `x`, because the value settles at -1. A loop on `x >>> 1` reaches 0 after at most 32 steps.

<!-- stage: code -->
### Implement Reads, Writes And Reversal

```java
final class Shifts {
    static int bitAt(int x, int position) {
        return (x >> position) & 1;                     // bring the bit to position 0, then erase the others
    }

    static int field(int x, int position, int width) {
        int run = (1 << width) - 1;                  // a run of width ones, for width up to 30
        return (x >>> position) & run;                  // zero fill keeps the high positions clean
    }

    static int withField(int x, int position, int width, int value) {
        int run = (1 << width) - 1;                  // the same run of ones
        int cleared = x & ~(run << position);           // erase the old field
        return cleared | ((value & run) << position);   // write the new field at its position
    }

    static int reverse(int n) {
        int result = 0;
        for (int i = 0; i < 32; i++) {               // exactly 32 positions, so the loop always ends
            result = (result << 1) | (n & 1);        // append the lowest bit of n at the right
            n >>>= 1;                                // drop that bit and keep zeros at the top
        }
        return result;
    }
}
```

Every method costs O(1), except `reverse`, which does 32 loop steps and therefore also costs O(1) for a fixed width. The method `reverse` uses `>>>=` and not `>>=`, so a negative input never copies the sign into the loop. The method `field` keeps `width` below 31 so that `1 << width` stays positive. The caller guarantees that `value` fits in `width` bits, and `value & run` protects the neighbor fields when it does not.

<!-- stage: applicability -->
### When Shifts Apply

#### Recognize The Pattern

Use shifts when bits must be read, moved or assembled by position. Typical cases are single flags at a known position, color channels, ids packed next to counters, and loops over all 32 positions of a number. The cue is a fixed layout in which every field has a known start and a known width.

The invariant to check before coding is that each field keeps its own range of positions and no two fields overlap. Reads must shift first and mask second, and writes must clear the old field before they insert the new one.

#### Watch For The Nearest False Friend

Division and multiplication by powers of two look like shifts, and they agree for small nonnegative values. Division rounds toward zero, and `>>` rounds toward negative infinity, so `-3 / 2` is -1 and `-3 >> 1` is -2. Use division when the quantity is a number that must round toward zero. Use a shift when the value is a bit pattern or a quantity that must round down.

#### Avoid The Java Shift Traps

Use `>>>` for any loop over bits that must end, because `>>` leaves a negative number at -1 forever. Remember that the shift distance wraps, so `1 << 32` is 1, and `1 << 31` is the negative number `Integer.MIN_VALUE`. Write parentheses around every shift, because `+` binds more tightly than `<<`, and `==` binds more tightly than `&`.

<!-- stage: exercises -->
### Exercises

#### [Build] Extract Bit I (Author exercise)
<!-- id: bt02-extract-bit -->

**Prerequisites.** The shift-then-mask read from this lesson.

**Problem.** Given a 32-bit `int` value `x` and a position `i`, return the binary bit of `x` at position `i`. Position 0 is the lowest bit and position 31 is the sign bit. The negative values use two's complement.

**Constraints.** The limits are:
- **`x`** is any `int`, including negative values.
- **`i`** is an `int` with `0 <= i <= 31`.
- **Return** is the `int` 0 or 1.
- **Mutation** is not applicable, because the input is a single value.

**Example 1.** Input `x = 180` and `i = 2`, output 1, because `180 >> 2` is 45 and the lowest bit of 45 is 1.

**Example 2.** Input `x = -2147483643` and `i = 31`, output 1, because position 31 is the sign bit of a negative `int`.

**Hint.** Which bit must reach position 0, and which single AND keeps only that bit?

**Changed decision.** Baseline case: one shift and one AND read exactly one position.

#### [Vary] Reverse Bits (LeetCode 190)
<!-- id: bt02-reverse-bits -->

**Prerequisites.** The extract bit exercise above.

**Problem.** Given a 32-bit value `n`, return the value whose bit at position `31 - i` equals the bit of `n` at position `i`, for every `i` from 0 to 31. Treat `n` as a pattern of 32 bits. The result may be negative as an `int`.

**Constraints.** The limits are:
- **`n`** is any `int`, including negative values.
- **Width** is exactly 32 positions, and leading zeros count.
- **Return** is an `int` that holds the reversed pattern.
- **Library** methods such as `Integer.reverse` are not allowed.

**Example 1.** Input `n = 43261596`, output 964176192, because the 32-bit pattern `00000010100101000001111010011100` reverses to `00111001011110000010100101000000`.

**Example 2.** Input `n = -3`, output -1073741825, because the pattern `11111111111111111111111111111101` reverses to `10111111111111111111111111111111` and has a 0 only at position 30.

**Hint.** Which bit of `n` is appended first, and which operator moves the finished result up by one position?

**Changed decision.** The operation changes from reading one position to reading all 32 positions and appending each one in reverse order.

#### [Boundary] Negative Values (Author exercise)
<!-- id: bt02-negative-values -->

**Prerequisites.** The two exercises above and the comparison of both right shifts from this lesson.

**Problem.** Given an `int` value `x`, return the number of bits equal to 1 in its 32-bit two's complement pattern. Your loop must end for negative values.

**Constraints.** The limits are:
- **`x`** is any `int` from `Integer.MIN_VALUE` to `Integer.MAX_VALUE`.
- **Return** is an `int` from 0 to 32.
- **Loop** must perform at most 32 steps.
- **Library** methods such as `Integer.bitCount` are not allowed.

**Example 1.** Input `x = -8`, output 29, because the pattern `11111111111111111111111111111000` has 29 ones.

**Example 2.** Input `x = Integer.MIN_VALUE`, output 1, because only the sign bit is 1, and a loop with `>>` would stay at -1 forever.

**Hint.** What does the signed right shift leave in the top positions of a negative number, and what does the zero-fill shift leave?

**Changed decision.** The input now includes negative numbers, so the loop must use the zero-fill shift to reach 0.

#### [Recognize] Pack Two Fields (Author exercise)
<!-- id: bt02-pack-fields -->

**Prerequisites.** All three exercises above.

**Problem.** A table stores each record as one `int`. A record holds a field `x` in the top 12 positions (positions 20 to 31) and a field `y` in the low 20 positions (positions 0 to 19). The memory budget allows one `int` per record, so separate arrays for `x` and `y` are not allowed. Given records `(x, y)` and queries `(r, f)`, store every record in a single `int`. Then, for each query, return field `f` of record `r`, read back from the stored `int`. Field 0 is `x` and field 1 is `y`.

**Constraints.** The limits are:
- **`x`** is an `int` with `0 <= x <= 4,095`.
- **`y`** is an `int` with `0 <= y <= 1,048,575`.
- **Records** number at most `10^5`, and queries number at most `10^5`.
- **Query** uses `0 <= r < records` and `f` equal to 0 or 1.
- **Return** is an `int[]` with one value per query.

**Example 1.** Input records [[4095,7],[1,1048575],[0,0]] and queries [[0,0],[0,1],[1,1]], output [4095,7,1048575]. The first record stores as -1048569, which is negative, and the zero-fill shift still recovers 4095.

**Example 2.** Input records [[2,5]] and queries [[0,0],[0,1]], output [2,5], because the record stores as 2097157 and the two reads split it again.

**Hint.** Each record must fit in one 32-bit `int`. How many bits does each field need, and what does the top bit do to a read of the upper field?

**Changed decision.** The state is now two fields in one number, so every read needs the right shift and the right mask for its own field.
