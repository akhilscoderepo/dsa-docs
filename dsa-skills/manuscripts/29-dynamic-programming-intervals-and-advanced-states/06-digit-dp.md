<!-- lesson-kind: standard -->
<!-- lesson-id: digit-dp -->
## Digit DP

<!-- stage: context -->
### Counting Codes Below A Limit

A registration system issues numeric codes. Staff dislike the digit 0 because it looks like the letter O on printed labels, so the system must never use a code that contains a 0. A manager asks how many valid codes exist among the integers from 1 to 3047. The answer must come back instantly, and the same question will soon arrive with limits near 10^18.

A first script checks every integer one at a time. It works for 3047 and stalls for 10^18, because the loop body would run a billion billion times.

Formally, the input is a non-negative integer `n`. The task is to count the integers `x` with `1 <= x <= n` whose decimal representation has no digit 0. The decimal representation of `x` has no leading zeros, so the integer 105 contains a 0 and the integer 15 does not. The input is read and never changed.

This lesson asks how to count such integers by looking at the digits of `n` once, and not at the integers themselves.

<!-- stage: naive -->
### Testing Every Integer In The Range

The direct method loops over every integer from 1 to `n`. It converts each integer to text and rejects it when the text contains the character `'0'`.

```java
static long countByLoop(long n) {
    long total = 0;
    for (long x = 1; x <= n; x++) {
        if (Long.toString(x).indexOf('0') < 0) {
            total++;
        }
    }
    return total;
}
```

For n = 3047 the loop makes 3047 checks and finds 2277 valid codes. Each check costs O(d) time, where d is the number of digits of `x`, so the whole method runs in O(n * d) time and uses O(d) memory for the text.

```predict
Suppose one check takes one nanosecond and n is 10^18. About how long does countByLoop run?

About 10^9 seconds, which is roughly 30 years. The cost grows with the value of n, and not with the number of digits of n. Doubling the number of digits squares the work.
```

<!-- stage: bottleneck -->
### Cost Grows With The Value Of n

The failure has one cause. The loop count equals the size of the range, and the size of the range is exponential in the number of digits. A number with 18 digits can reach 10^18, so the loop needs O(10^d) steps for d digits. The answer itself only depends on a short string of d digits.

A smarter method builds valid numbers digit by digit. It chooses a first digit, then a second, and so on, and it stops when a prefix already exceeds `n`. That method still visits one path for every valid number below the limit. Valid numbers with no digit 0 number about 9^d, so the visits still run in O(9^d) time. For d = 18 that is more than 10^17 paths.

The paths repeat their work. Take the prefixes 12 and 21. Each has two digits, each contains no 0, and each is already below the first two digits of a large `n`. The remaining digits can be chosen the same way after both prefixes, so the count of completions is identical. The next section defines the facts a prefix needs to remember, so equal prefixes share one answer and the work becomes O(d) steps.

<!-- stage: insight -->
### Remember Only Two Facts About A Prefix

A prefix of a number matters for the future in only two ways. It decides which next digits keep the number at or below `n`. It also decides whether the zero rule applies yet. Everything else about the prefix, such as which exact digits it holds, does not change the count of completions.

<!-- names: tight flag, started flag, ways table -->

#### The Tight Flag Limits The Next Digit

Write `n` as digits `n[0]`, `n[1]`, up to `n[d - 1]`, and process positions from left to right. A prefix is **tight** when it equals the first `p` digits of `n`. The **tight flag** is 1 for such a prefix and 0 otherwise. A tight prefix may place only digits from 0 up to `n[p]` at position `p`. A prefix that already sits below `n` may place any digit from 0 to 9.

After a digit is placed, the flag stays 1 only when the prefix was tight and the new digit equals `n[p]`. If the digit is smaller, the number is already below `n`, and the flag becomes 0 for good.

#### The Started Flag Handles Leading Zeros

To compare numbers of different lengths, the method writes every number with exactly `d` digits and pads short numbers with zeros on the left. Those padding zeros are not part of the number, so the zero rule must ignore them. The **started flag** is 1 once a nonzero digit has been placed. While the flag is 0, a digit 0 is padding and stays allowed. Once the flag is 1, a digit 0 is a real digit and the zero rule forbids it.

#### One Cell For Each Combination

The two flags give four combinations. Let `ways[t][s]` count the prefixes of the current length with tight flag `t` and started flag `s`. This **ways table** is the whole state, and it has 4 entries. At each position, every entry spreads its count to the entries of the next position, one transition for each allowed digit.

The invariant is that after `p` positions, `ways[t][s]` equals the number of distinct digit prefixes of length `p` that satisfy the zero rule, are not above the first `p` digits of `n`, and have those exact flags. The final answer adds `ways[0][1]` and `ways[1][1]`, because the all-padding prefix stands for the integer 0, which the range excludes.

<!-- stage: variables -->
### The Digits And The Four Counts

The input is a number, and these working values describe the pass over its digits.

- **digits** is an `int[]` that holds the decimal digits of `n`, with `digits[0]` as the leading digit.
- **p** is the position being processed, from 0 to `d - 1`.
- **ways** is a `long[2][2]`; entry `ways[t][s]` counts the prefixes with tight flag `t` and started flag `s`.
- **next** is a fresh `long[2][2]` for position `p + 1`, filled from `ways`.
- **limit** is `digits[p]` when `t` is 1 and 9 when `t` is 0, the largest digit the prefix may place.

Java fills a new `long` array with zeros, so `next` starts empty without extra code. The counts are `long` because the answer for a number with 18 digits is near 9^18, which exceeds the `int` range. In the trace below, `t1s0` is the name used for `ways[1][0]`, and the other three names follow the same pattern.

<!-- stage: trace -->
### Two Runs Over The Digits

#### Counting Below 3047

The first run uses `n = 3047`. The cells list its four digits. The pointer `pos` shows the position just processed, and the value -1 marks the start before any digit. The variables `t1s0`, `t1s1`, `t0s0` and `t0s1` are the four counts after that position.

At the start, one empty prefix exists, and it is tight and not started. Position 0 may place 0 through 3. The digit 0 keeps the prefix unstarted, the digits 1 and 2 start a number below the limit, and the digit 3 starts a prefix that stays tight. At position 1 the limit digit is 0. The tight prefix `3` may place only 0, but a started prefix may not place 0, so that count drops to nothing. The unstarted count stays at 1, because only the all-padding prefix remains unstarted. The started counts then grow by about 9 per position, because each started prefix chooses any digit from 1 to 9, and the unstarted prefix adds nine new starts. The sum of the two started entries at the end is 2277, which equals the loop count from the naive stage.

```trace
{"cells":[3,0,4,7],"pointers":["pos"],"steps":[{"at":{"pos":-1},"vars":{"t1s0":1,"t1s1":0,"t0s0":0,"t0s1":0},"note":"One empty prefix exists. It is tight, because it equals the empty start of n, and it is not started."},{"at":{"pos":0},"vars":{"t1s0":0,"t1s1":1,"t0s0":1,"t0s1":2},"note":"Position 0 has limit digit 3. The started counts now sum to 3, of which 1 stay tight."},{"at":{"pos":1},"vars":{"t1s0":0,"t1s1":0,"t0s0":1,"t0s1":27},"note":"Position 1 has limit digit 0. The started counts now sum to 27, of which 0 stay tight."},{"at":{"pos":2},"vars":{"t1s0":0,"t1s1":0,"t0s0":1,"t0s1":252},"note":"Position 2 has limit digit 4. The started counts now sum to 252, of which 0 stay tight."},{"at":{"pos":3},"vars":{"t1s0":0,"t1s1":0,"t0s0":1,"t0s1":2277},"note":"Position 3 has limit digit 7. The started counts now sum to 2277, of which 0 stay tight."}]}
```

#### Counting Below 130

The second run uses `n = 130`. Position 0 places the digit 0 or 1, because the limit digit is 1. The digit 1 keeps the prefix tight. At position 1 the limit digit is 3, so the tight prefix may place 0 to 3, and the digit 0 is forbidden because the prefix already started. It places 1, 2 or 3 and only the digit 3 stays tight. At position 2 the limit digit is 0, so the tight prefix `13` has no allowed digit and its count drops to 0. The final sum is 108.

```trace
{"cells":[1,3,0],"pointers":["pos"],"steps":[{"at":{"pos":-1},"vars":{"t1s0":1,"t1s1":0,"t0s0":0,"t0s1":0},"note":"One empty prefix exists. It is tight, because it equals the empty start of n, and it is not started."},{"at":{"pos":0},"vars":{"t1s0":0,"t1s1":1,"t0s0":1,"t0s1":0},"note":"Position 0 has limit digit 1. The started counts now sum to 1, of which 1 stay tight."},{"at":{"pos":1},"vars":{"t1s0":0,"t1s1":1,"t0s0":1,"t0s1":11},"note":"Position 1 has limit digit 3. The started counts now sum to 12, of which 1 stay tight."},{"at":{"pos":2},"vars":{"t1s0":0,"t1s1":0,"t0s0":1,"t0s1":108},"note":"Position 2 has limit digit 0. The started counts now sum to 108, of which 0 stay tight."}]}
```

<!-- stage: code -->
### Spreading Counts Across Four Entries

The method returns how many integers from 1 to `n` have no digit 0. It reads the digits of `n` once and keeps only the four counts.

```java
static long countZeroFree(long n) {
    int[] digits = Long.toString(n).chars().map(c -> c - '0').toArray();
    long[][] ways = new long[2][2];
    ways[1][0] = 1;
    for (int p = 0; p < digits.length; p++) {
        long[][] next = new long[2][2];
        for (int t = 0; t < 2; t++) {
            for (int s = 0; s < 2; s++) {
                if (ways[t][s] == 0) continue;
                int limit = t == 1 ? digits[p] : 9;
                for (int dig = 0; dig <= limit; dig++) {
                    if (s == 1 && dig == 0) continue;
                    int nt = (t == 1 && dig == limit) ? 1 : 0;
                    int ns = (s == 1 || dig != 0) ? 1 : 0;
                    next[nt][ns] += ways[t][s];
                }
            }
        }
        ways = next;
    }
    return ways[0][1] + ways[1][1];
}
```

The loops run d positions, four entries and at most ten digits, so the time is O(d * 4 * 10), which is O(d). The memory is O(d) for the digit array plus constant space for the two small tables. For n = 0 the digit array holds the single digit 0, the started count stays 0, and the method returns 0. The exercises below remove the flags one at a time and then add them back.

<!-- stage: applicability -->
### Recognizing Counts Under A Bound

#### Reading The Cue

Use this method when a question asks how many integers up to a bound satisfy a rule on their digits. Phrases such as "at most n", "no digit equal to", "digit sum" and "digits taken from a set" point here. The state is the position plus a tight flag plus a started flag, and a rule may add one more small fact, such as a running digit sum or the previous digit.

#### Checking The Invariant

The invariant says that each state summarizes every prefix with the same flags and the same extra fact, and that no prefix is counted twice or lost. Test a bound with one digit, such as 7. Test a bound that is a power of ten, such as 1000, where every tight prefix dies early. Test the bound 0, which must return 0. Compare the method against the loop on every bound up to a few thousand.

#### Avoiding The False Friend

The first false friend is a table that counts only numbers with exactly `d` digits, which misses every shorter number because the started flag is gone. The second is a table that never lets the tight flag expire, which counts numbers above the bound. The third is a rule that treats padding zeros as real digits, which rejects every number shorter than `n`. The method does not apply when the rule compares digits far apart with no small summary, because the extra fact then grows too large to store as a state.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Fixed-Length Digit Strings (Author exercise)
<!-- id: dp29-fixed-length-strings -->

**Prerequisites.** The ways table from this lesson, without the two flags.

**Problem.** A string `allowed` holds distinct decimal digit characters, and an integer `len` is given. Count the strings of exactly `len` characters in which every character appears in `allowed`. Characters may repeat, and a leading `'0'` is an ordinary character.

**Constraints.** The limits are:
- **Length** satisfies `0 <= len <= 15`.
- **Allowed set** has between 1 and 10 distinct characters, each from `'0'` to `'9'`.
- **Result** is a `long`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `len = 4`, `allowed = "024"`, output `81`.

**Example 2.** Input `len = 3`, `allowed = "1357"`, output `64`.

**Hint.** If `ways[p]` counts the valid strings of length `p`, how many choices does position `p` have?

**Changed decision.** The table has no tight or started state, so every position offers the same choices.

#### [Vary] Add Tight State (Author exercise)
<!-- id: dp29-add-tight-state -->

**Prerequisites.** The exercise above.

**Problem.** A non-negative integer `n` and a string `allowed` of distinct digit characters are given. Write `n` with `d` digits, where `d` is the length of its decimal representation. Count the digit strings of exactly `d` characters, with leading zeros allowed, that read as a value at most `n` and use only characters from `allowed`.

**Constraints.** The limits are:
- **Bound** satisfies `0 <= n <= 10^15`.
- **Allowed set** has between 1 and 10 distinct characters, each from `'0'` to `'9'`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the inputs are values.

**Example 1.** Input `n = 3047`, `allowed = "0123"`, output `208`.

**Example 2.** Input `n = 58`, `allowed = "2468"`, output `8`.

**Hint.** Which digits may a prefix place when it still equals the leading digits of `n`, and which when it is already smaller?

**Changed decision.** The prefix now carries a tight flag, so the digit limit depends on the history and not only on the position.

#### [Boundary] Leading Zero And Number Zero (Author exercise)
<!-- id: dp29-leading-zero-and-zero -->

**Prerequisites.** The two exercises above.

**Problem.** A non-negative integer `n` and an integer `k` are given. Count the integers `x` with `0 <= x <= n` whose decimal representation contains exactly `k` digits equal to 0. The representation has no leading zeros, and the integer 0 is written as the single digit `0`.

**Constraints.** The limits are:
- **Bound** satisfies `0 <= n <= 10^15`.
- **Zero count** satisfies `0 <= k <= 16`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the inputs are values.

**Example 1.** Input `n = 100`, `k = 2`, output `1`.

**Example 2.** Input `n = 0`, `k = 1`, output `1`.

**Hint.** Which padding zeros must stay out of the count, and which digit of the integer 0 must stay in?

**Changed decision.** The started flag decides which zeros count, and the integer 0 is the one case where the number never starts but still owns one zero digit.

#### [Recognize] Numbers At Most N Given Digit Set (LeetCode 902)
<!-- id: dp29-digit-set-at-most-n -->

**Prerequisites.** All three exercises above.

**Problem.** A set `digits` of distinct characters from `'1'` to `'9'` and an integer `n` are given. Count the positive integers `x` with `x <= n` whose decimal representation uses only characters from `digits`. A character may appear many times in one integer.

**Constraints.** The limits are:
- **Set size** satisfies `1 <= digits.length() <= 9`, with distinct characters from `'1'` to `'9'`.
- **Bound** satisfies `1 <= n <= 10^9`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the inputs are values.

**Example 1.** Input `digits = "249"`, `n = 500`, output `30`.

**Example 2.** Input `digits = "1357"`, `n = 1000`, output `84`.

**Hint.** Which numbers are shorter than `n`, and which flag lets the table count them without a separate case?

**Changed decision.** The rule now forbids digits outside a set and not one digit, and the set has no 0, so a started number can never place a padding zero by mistake.
