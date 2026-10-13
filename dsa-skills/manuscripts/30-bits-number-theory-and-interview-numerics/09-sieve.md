<!-- lesson-kind: standard -->
<!-- lesson-id: sieve -->
## Sieve

<!-- stage: context -->
### Why Testing Each Number Alone Is Slow

A hash table library must pick a prime capacity. A test tool for it asks for every prime up to ten million, so that it can compare table sizes. A second tool must report how many primes lie below a bound, and a third must split many numbers into prime factors.

All three tools share one upper bound. They ask about a whole range of numbers, and not about one number. A routine that tests a single number from scratch throws away everything it learned about the neighbours. The question for this lesson is how a program answers prime questions for all numbers up to `n` with work that is close to linear in `n`.

A **prime** is an integer greater than 1 whose only positive divisors are 1 and itself. A **composite** is an integer greater than 1 that has another divisor. The numbers 0 and 1 are neither.

<!-- stage: naive -->
### Dividing Every Number By Small Values

The direct approach tests each number by trial division. A number `x` is prime when no integer from 2 up to the square root of `x` divides it. The method below collects the primes up to `n` this way.

```java
static boolean isPrime(int x) {
    if (x < 2) return false;                 // 0 and 1 are not prime
    for (int d = 2; (long) d * d <= x; d++) {
        if (x % d == 0) return false;        // a divisor at most sqrt(x) proves x composite
    }
    return true;                             // no divisor found, so x is prime
}

static int[] primesTrial(int n) {
    int[] buffer = new int[Math.max(n + 1, 0)];
    int size = 0;
    for (int x = 2; x <= n; x++) {
        if (isPrime(x)) buffer[size++] = x;  // each number is tested from scratch
    }
    return java.util.Arrays.copyOf(buffer, size);
}
```

The test for one number stops early when it finds a divisor. A prime has no divisor, so its test runs all the way to the square root. The tests for different numbers never share results.

<!-- stage: bottleneck -->
### Every Prime Costs A Full Square Root

```predict
The routine above lists the primes up to 10,000,000. There are 664,579 of them, and each one needs about 3,162 trial divisions. About how many divisions do the primes alone cost?

About two billion divisions. The count is 664,579 times 3,162, which is above 2 * 10^9, and the composites add more. The run takes several seconds, although the answer is only a list of numbers.
```

#### Count The Divisions

A prime `x` needs about the square root of `x` divisions, so the whole range costs up to O(n * sqrt(n)) time. For `n = 10,000,000` the primes alone need over two billion divisions. A division is slower than an addition, so the program exceeds a limit of one or two seconds.

#### Find The Repeated Work

The routine also repeats itself. The numbers 49, 77 and 91 are all multiples of 7 with no smaller prime divisor. Each test divides by 2, 3, 4, 5 and 6 without success and then finds 7. The divisions by 4 and 6 add nothing, because 2 had already shown that every multiple of 4 or 6 is even. The tests rediscover that 7 divides each of the three numbers. One divisor found once could settle all of its multiples at the same time. The target is a method whose total cost is close to O(n), and not O(n * sqrt(n)).

<!-- stage: insight -->
### Cross Out Multiples Once

#### Mark Multiples Instead Of Dividing

The **sieve of Eratosthenes** turns the question around. It keeps a boolean array `composite` of length `n + 1`, with every entry false at the start. It scans the numbers from 2 upward. When the scan reaches a number `p` whose flag is still false, no smaller prime divides `p`, so `p` is prime. The sieve then sets the **composite flag** to true for the multiples of `p`. A flag that is still false when the scan arrives is the proof that the number is prime, and no division is needed.

<!-- names: sieve of Eratosthenes, composite flag, square start, smallest prime factor -->

#### Start At The Square

Take a prime `p`. The multiple `p * k` with `k < p` has the factor `k`, and `k` has a prime factor smaller than `p`. An earlier prime already set the flag of `p * k`. The first multiple that no earlier prime reached is `p * p`. The marking loop therefore uses a **square start**, which means `m` begins at `p * p` and grows by `p`. This skips the `p - 1` smaller multiples of each prime, and it removes all writes once `p * p` is above `n`.

#### Stop At The Square Root

When `p * p` is greater than `n`, the marking loop for `p` has no work, and every later prime has none either. The outer loop can stop at the largest `p` with `p * p <= n`. Every composite number up to `n` has a prime factor of at most its square root, so each composite is marked by then. The scan still reads every flag to collect the primes.

#### Count The Total Work

Prime `p` writes about `n / p` flags. The sum of `n / p` over the primes up to `n` grows as n log log n, and the log log factor is below 4 for any `n` that fits in memory. The total is close to linear. The invariant is that after the sieve finishes the loop for prime `p`, every composite whose smallest prime factor is at most `p` carries a true flag.

#### Store A Factor Instead Of A Flag

Some questions need the factors and not only the primality. Replace the boolean array by an `int[]` named `spf`, where `spf[x]` is the **smallest prime factor** of `x`. A marking loop writes `p` into `spf[m]` only if `spf[m]` is still 0. The outer loop assigns `spf[x] = x` when it reaches a prime `x`, because that entry is still 0. A number then splits into primes by repeating `x = x / spf[x]`, one step per prime factor, so a factorization costs O(log x).

<!-- stage: variables -->
### Quantities The Sieve Tracks

Track these items while the sieve runs.

- **composite** is a `boolean[]` of length `n + 1`, and true means the index is composite.
- **p** is the current candidate in the outer scan, and a false flag makes it prime.
- **m** is the multiple being marked, stored as a `long` so `p * p` cannot wrap.
- **spf** is an `int[]` where `spf[x]` holds the smallest prime factor of `x`.
- **count** is the number of primes found by the final pass.

In a trace, the pointer `p` and the pointer `m` are positions in the list of numbers shown, and the value of that number equals the position plus 2. The flags for 0 and 1 stay unused, because neither number is prime.

<!-- stage: trace -->
### Follow One Sieve And One Factorization

#### Sieve Every Number Up To Thirty

Take `n = 30`. The numbers 2 to 30 are listed below. The scan reaches 2, whose flag is false, so 2 is prime and its multiples 4, 6, up to 30 get marked. That is 14 writes. The scan reaches 3, still unmarked, and starts at 9, because 6 already carries a flag. It marks 9, 15, 21 and 27. The number 5 starts at 25 and marks only 25, because 10, 15 and 20 are already marked. The number 7 has `7 * 7 = 49`, which is above 30, so the loop ends. The unmarked numbers are the 10 primes up to 30.

```trace
{"cells":[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],"pointers":["p","m"],"steps":[{"at":{"p":-1,"m":-1},"vars":{"marks":0},"note":"No number is marked yet. The scan has not reached any candidate."},{"at":{"p":0,"m":2},"vars":{"p":2,"firstMultiple":4,"newMarks":14,"marks":14},"note":"The flag of 2 is false, so 2 is prime. The loop starts at 4 and writes 14 new marks: 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30."},{"at":{"p":1,"m":7},"vars":{"p":3,"firstMultiple":9,"newMarks":4,"marks":18},"note":"The flag of 3 is false, so 3 is prime. The loop starts at 9 and writes 4 new marks: 9, 15, 21, 27."},{"at":{"p":3,"m":23},"vars":{"p":5,"firstMultiple":25,"newMarks":1,"marks":19},"note":"The flag of 5 is false, so 5 is prime. The loop starts at 25 and writes 1 new marks: 25."},{"at":{"p":5,"m":-1},"vars":{"p":7,"square":49,"marks":19},"note":"For p = 7 the square is 49, which is above 30. The loop ends, and every composite up to 30 is marked."},{"at":{"p":-1,"m":-1},"vars":{"primes":10,"marks":19},"note":"The unmarked numbers are the 10 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29."}]}
```

#### Split Eighty-Four Into Primes

Take `spf` built for `n = 100` and the number 84. The trace lists the value of `x` after each division. The smallest prime factor of 84 is 2, so `x` becomes 42. The factor of 42 is 2, so `x` becomes 21. The factor of 21 is 3, so `x` becomes 7. The number 7 is prime, so its factor is 7 and `x` becomes 1. The loop stops at 1. The factors collected in order are 2, 2, 3 and 7, whose product is 84.

```trace
{"cells":[84,42,21,7,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"x":84,"spf":2,"factors":"[2]"},"note":"The value x is 84 and spf[84] is 2. The factor 2 joins the list, and x becomes 42."},{"at":{"i":1},"vars":{"x":42,"spf":2,"factors":"[2, 2]"},"note":"The value x is 42 and spf[42] is 2. The factor 2 joins the list, and x becomes 21."},{"at":{"i":2},"vars":{"x":21,"spf":3,"factors":"[2, 2, 3]"},"note":"The value x is 21 and spf[21] is 3. The factor 3 joins the list, and x becomes 7."},{"at":{"i":3},"vars":{"x":7,"spf":7,"factors":"[2, 2, 3, 7]"},"note":"The value x is 7 and spf[7] is 7. The factor 7 joins the list, and x becomes 1."},{"at":{"i":4},"vars":{"x":1,"factors":"[2, 2, 3, 7]"},"note":"The value x is 1, so the loop stops. The product of the factors is 84."}]}
```

The hardest step is the start of the loop for 3. A reader may expect it to begin at 6, which is the first multiple of 3. The flag of 6 is already true because of 2, so the write would repeat earlier work. The square start 9 is the first multiple that no earlier prime reached.

<!-- stage: code -->
### Implement Flags And Factor Table

```java
static boolean[] sieveFlags(int n) {
    boolean[] composite = new boolean[Math.max(n + 1, 2)];   // slots 0 and 1 always exist
    for (int p = 2; (long) p * p <= n; p++) {
        if (composite[p]) continue;                          // a marked number is not prime
        for (long m = (long) p * p; m <= n; m += p) {
            composite[(int) m] = true;                       // multiples below p*p were marked earlier
        }
    }
    return composite;                                        // false at index x >= 2 means x is prime
}

static int[] smallestFactor(int n) {
    int[] spf = new int[Math.max(n + 1, 2)];
    for (int p = 2; p <= n; p++) {
        if (spf[p] != 0) continue;                           // a value was written, so p is composite
        spf[p] = p;                                          // a prime is its own smallest factor
        for (long m = (long) p * p; m <= n; m += p) {
            if (spf[(int) m] == 0) spf[(int) m] = p;         // keep the first, which is the smallest
        }
    }
    return spf;
}
```

The first method stops its outer loop at the square root, because larger primes mark nothing. The second method runs the outer loop over every `p`, since a prime above the square root must still receive `spf[p] = p`. Both methods compute `p * p` in `long`, so no product wraps. Memory is one byte per flag, or four bytes per `spf` entry.

<!-- stage: applicability -->
### When To Use A Sieve

#### Recognize The Pattern

Use a sieve when many primality questions, prime counts or factorizations share one upper bound `n` that fits in an array. The cue is a range of numbers and not one huge number. The invariant to state before coding is that the loop for prime `p` marks only multiples from `p * p`, because smaller multiples have a smaller prime factor and are already marked.

#### Watch For The Nearest False Friend

Trial division is a false friend. It is the right tool for a single query number, or for a few queries on numbers far larger than any array could index. For one number near 10^12, a sieve cannot be allocated, and a loop to the square root takes 10^6 steps. For a range of queries below 10^7, the sieve wins by a large factor.

#### Avoid The Java Hazards

Computing `p * p` in `int` wraps for `p` above 46,340 and makes the loop condition true again, so the loop never ends. Cast to `long` first, or compare `p <= n / p`. The flags for 0 and 1 are false in the array, so the final pass must start from 2, and an input `n` below 2 must return an empty result. A `boolean[]` of `n + 1` entries costs `n + 1` bytes, so `n` near 2^31 cannot be allocated at all.

<!-- stage: exercises -->
### Exercises

#### [Build] Primes Through N (Author exercise)
<!-- id: bt09-primes-through-n -->

**Prerequisites.** The sieve and the square start from this lesson.

**Problem.** Given an integer `n`, return every prime `p` with `2 <= p <= n`. The primes appear in increasing order in an `int[]`.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 2,000,000`.
- **Order** of the result is increasing.
- **Empty** result is an array of length 0, and it occurs for `n < 2`.
- **Mutation** does not apply, because the input is one integer.

**Example 1.** Input `n = 30`, output `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`, the 10 primes up to 30.

**Example 2.** Input `n = 2`, output `[2]`, because the bound itself is prime. Input `n = 1` returns an empty array.

**Hint.** Which index does the first marking loop for prime `p` start from, and why can no smaller multiple of `p` still be unmarked?

**Changed decision.** Baseline case: marks multiples in a Boolean array instead of testing each number.

#### [Vary] Count Primes (LeetCode 204)
<!-- id: bt09-count-primes-below -->

**Prerequisites.** The exercise above.

**Problem.** Given an integer `n`, count the primes strictly smaller than `n`. This version differs from the original statement, because it also reports the largest of those primes. Return an `int[]` of length 2 with the count first and the largest prime second, and use -1 as the largest prime when the count is 0.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 5,000,000`.
- **Bound** is exclusive, so a prime equal to `n` does not count.
- **Return** is `{count, largest}`.

**Example 1.** Input `n = 10`, output `{4, 7}`, from the primes 2, 3, 5 and 7.

**Example 2.** Input `n = 2`, output `{0, -1}`, because the prime 2 is not strictly smaller than 2.

**Hint.** The bound excludes `n` itself. Which array size and which final scan range keep `n` out of the count?

**Changed decision.** The range ends before `n`, and the answer needs a second value taken from the same scan.

#### [Boundary] Zero One And p-Squared Overflow (Author exercise)
<!-- id: bt09-square-overflow -->

**Prerequisites.** The two exercises above and the Java hazards from this lesson.

**Problem.** A sieve of size `n` has flags for the numbers 0 to `n`. For a prime `p`, its marking loop writes the flags at `p * p`, `p * p + p`, and so on, up to `n`. Given `n` and a list of primes, return for each prime the number of writes its marking loop makes. A write counts even when the flag is already true. The loop makes no write when `p * p` is above `n`. The array of flags is not built.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 2,147,483,647`.
- **Primes** are `int` values with `2 <= p <= 2,147,483,647`, and at most 100,000 queries.
- **Small `n`** with `n < 4` gives 0 for every prime.
- **Return** is an `int[]` with one count per query.

**Example 1.** Input `n = 2147483647` and primes `[46340, 46341, 2147483647]`, output `[2, 0, 0]`. The square of 46,341 is above `n`, but in `int` arithmetic it wraps to a negative number.

**Example 2.** Input `n = 30` and primes `[2, 3, 5, 7]`, output `[14, 8, 2, 0]`, because the loop for 3 writes 9, 12, 15, 18, 21, 24, 27 and 30.

**Hint.** What does `p * p` become in `int` when `p` is 46,341, and which type keeps the square exact? The loop writes `p * p` first, so the count is `(n - p * p) / p + 1` when `p * p <= n`.

**Changed decision.** The largest legal bound makes the square overflow, so the start index needs wider arithmetic.

#### [Recognize] Smallest Prime Factor Sieve (Author exercise)
<!-- id: bt09-prime-factor-queries -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer `n` and a list of queries, each a number `x` with `2 <= x <= n`, return the prime factorization of every query. A factorization is the list of primes whose product is `x`, in nondecreasing order, with each prime repeated once per occurrence.

**Constraints.** The limits are:
- **`n`** is an `int` with `2 <= n <= 1,000,000`.
- **Queries** number at most 100,000.
- **Return** is an `int[][]` with one row per query.

**Example 1.** Input `n = 100` and queries `[12, 97, 84]`, output `[[2, 2, 3], [97], [2, 2, 3, 7]]`.

**Example 2.** Input `n = 100` and queries `[64, 2]`, output `[[2, 2, 2, 2, 2, 2], [2]]`, a power of two and a prime.

**Hint.** One table built once serves every query. What does a single table entry have to store so that a number splits into primes by repeated division?

**Changed decision.** The array stores a factor, and not a flag, so repeated factorizations cost O(log x) each.
