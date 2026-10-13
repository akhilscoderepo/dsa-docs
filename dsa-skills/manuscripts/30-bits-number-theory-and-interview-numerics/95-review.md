<!-- section: review -->
## Review

A service stores flags in twelve booleans, a checksum wraps to a negative total and a product loses its remainder. The questions below cover the ten lessons and the closing lesson. Return to this page after the lessons and again after a few days. Each question describes a situation, so decide the answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "rq30-rev-mask-clear", "q": "A flag word is `int f`. Which statement clears bit 3 and leaves the other bits unchanged?", "options": ["f &= ~(1 << 3)", "f |= (1 << 3)", "f ^= (1 << 3)", "f &= (1 << 3)"], "answer": 0, "explain": "AND with the complement of the bit zeroes only that bit. OR sets it, XOR flips it, and AND with the bare bit erases every other bit."}
```

```quiz
{"id": "rq30-rev-shift-negative", "q": "In Java, what does `-8 >> 1` evaluate to, and what does `-8 >>> 1` give for an int?", "options": ["-4 and 2147483644", "-4 and -4", "4 and 4", "-4 and 4"], "answer": 0, "explain": "The signed shift copies the sign bit, so -8 >> 1 is -4. The unsigned shift inserts a zero at the top, so the result is 2147483644."}
```

```quiz
{"id": "rq30-rev-low-bit", "q": "Which expression isolates the lowest set bit of a nonzero int x?", "options": ["x & (x - 1)", "x & -x", "x | (x - 1)", "x ^ (x >> 1)"], "answer": 1, "explain": "In two's complement, -x flips every bit above the lowest set bit, so x & -x keeps only that bit. x & (x - 1) removes it instead."}
```

```quiz
{"id": "rq30-rev-xor-pairs", "q": "An array holds every value twice except one value that appears once. What does the XOR of all elements equal?", "options": ["The sum of the distinct values", "Zero", "The single value", "The largest value"], "answer": 2, "explain": "Equal values cancel under XOR because a ^ a is 0 and 0 ^ b is b. Only the unpaired value remains."}
```

```quiz
{"id": "rq30-rev-subset-count", "q": "A set has 20 items. How many masks does the loop over all subsets visit?", "options": ["20", "400", "2^20, which is 1048576", "20!"], "answer": 2, "explain": "Each item is in or out, so there are 2^20 masks, including the empty one."}
```

```quiz
{"id": "rq30-rev-overflow", "q": "In Java, what does `Integer.MAX_VALUE + 1` evaluate to?", "options": ["Integer.MIN_VALUE", "An ArithmeticException", "2147483648", "Integer.MAX_VALUE"], "answer": 0, "explain": "int addition wraps around in two's complement without any exception, so the sum is Integer.MIN_VALUE."}
```

```quiz
{"id": "rq30-rev-mod-negative", "q": "Java evaluates `-7 % 3`. What is the result, and how do you get a non-negative remainder?", "options": ["2, with no fix needed", "-1, and ((a % m) + m) % m gives 2", "1, and a % m is already fine", "-2, and Math.abs gives 2"], "answer": 1, "explain": "Java keeps the sign of the dividend, so -7 % 3 is -1. Adding m before a second remainder gives 2."}
```

### Fixing A Wrong Answer

Open the lesson whose topic the question covers, such as Low Bit, Overflow or Modular Arithmetic, and reread its variables list and its applicability part. Then rerun its first trace by hand on a smaller input.
