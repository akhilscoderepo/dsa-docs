<!-- section: review -->
## Review

Return to this page after the lessons and again a few days later. Each question describes a situation and hides the lesson name. Commit to an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "so-rev-subtraction", "q": "A comparator returns `a - b` for `int` values and sorts ascending. For which pair does it put the wrong value first?", "options": ["a = 7, b = 9", "a = 2000000000, b = -2000000000", "a = -4, b = -9", "a = 0, b = 0"], "answer": 1, "explain": "The true difference 4000000000 does not fit in an `int`, so the result wraps to a negative number and the sort treats 2000000000 as the smaller value. The other pairs have small differences. The call `Integer.compare(a, b)` reads the sign without subtracting."}
```

```quiz
{"id": "so-rev-copy", "q": "A helper calls `Arrays.sort(nums)` on its parameter to read the median. Later, the caller draws the same array in arrival order. What is wrong?", "options": ["`Arrays.sort` returns a sorted copy and discards the original", "The sort works only on arrays shorter than 100000 values", "The helper reordered the caller's array, so it should sort a copy", "The median needs a comparator, and none was passed"], "answer": 2, "explain": "`Arrays.sort(int[])` sorts in place and returns nothing. The caller's array loses its arrival order. The call `Arrays.copyOf` gives the helper its own array to sort."}
```

```quiz
{"id": "so-rev-mirror", "q": "A comparator returns 1 whenever `a` is not smaller than `b`. What does it return for two equal values, in both argument orders?", "options": ["0 in both orders", "-1 and 1, one in each order", "It throws an exception for equal values", "1 in both orders, so each value claims to go second"], "answer": 3, "explain": "The rule never returns 0, so a pair of equal values gets 1 in both orders. The two answers contradict each other, and the comparator breaks the mirror property. The library may throw `IllegalArgumentException`, but it is not required to."}
```

```quiz
{"id": "so-rev-reversed", "q": "`Comparator.comparingInt(Player::score).reversed().thenComparing(Player::name)` sorts players. How does it order two players with equal scores?", "options": ["By name in descending order", "By name in ascending order", "By their order in the input only", "In an unspecified order"], "answer": 1, "explain": "The method `reversed()` applies to the score comparator, which comes before it. The method `thenComparing` adds the name key afterward, and that key stays ascending. Calling `reversed()` at the end of the chain would reverse both keys."}
```

```quiz
{"id": "so-rev-stable", "q": "Which choice keeps two tickets with equal priority in their input order?", "options": ["A selection sort that swaps the smallest ticket to the front", "A hand-written quicksort with a random pivot", "`Arrays.sort(Object[], comparator)` with a comparator on priority only", "`Arrays.sort(int[])` on the priorities"], "answer": 2, "explain": "The documentation promises that the object sort is stable. A selection sort swaps items across equal keys, and a primitive sort promises nothing about the order of equal values. Items that carry more data than the key need a stable sort or an index key."}
```

```quiz
{"id": "so-rev-frontier", "q": "Three requests ask for slot 3. After sorting, a sweep with a frontier gives each request the larger of its asked slot and the frontier. How many moves does the sweep count in total?", "options": ["0", "2", "3", "6"], "answer": 2, "explain": "The first request keeps slot 3 and the frontier becomes 4. The second takes slot 4 at cost 1, and the third takes slot 5 at cost 2. The total is 3."}
```

```quiz
{"id": "so-rev-last-run", "q": "A scan over a sorted array emits a pair of value and count only when the next value differs from the current one. What does it emit for `[4, 4, 4]`?", "options": ["The pair (4, 3)", "The pair (4, 1)", "Three pairs (4, 1)", "Nothing, because no next value ends the run"], "answer": 3, "explain": "The scan never sees a different next value, so it never emits the final run. The loop in the lesson ends a run at the array boundary as well, which removes this failure."}
```

```quiz
{"id": "so-rev-third", "q": "For `[5, 5, 4, 1]`, what does `sorted[sorted.length - 3]` return, and what is the third-highest distinct value?", "options": ["It returns 4, and the third-highest distinct value is 1", "It returns 5, and the third-highest distinct value is 4", "It returns 1, and the third-highest distinct value is 1", "It returns 4, and the third-highest distinct value is 4"], "answer": 0, "explain": "The sorted array is `[1, 4, 5, 5]`, and index 1 holds 4. The distinct values from the top are 5, 4 and 1. An index counts positions, so repeated values shift the answer."}
```

```quiz
{"id": "so-rev-close", "q": "Under the rules that swap any two characters and exchange two letters everywhere, which pair of strings is close?", "options": ["`aabb` and `ccdd`", "`abbccc` and `aaabbc`", "`abc` and `abcc`", "`aab` and `aaa`"], "answer": 1, "explain": "The two strings share the letters a, b and c, and their sorted counts are both 1, 2 and 3. The pair `aabb` and `ccdd` has different letters, the pair `abc` and `abcc` has different lengths, and the pair `aab` and `aaa` has different letter sets."}
```

### Questions To Ask Before Sorting

Before you call a sort, answer three questions in your own words. Which order does the next decision need, and which comparison produces it? What does the problem say about items that tie, and who owns that order? May the method change the caller's array, or must it sort a copy? Write the tie rule and the copy decision as one line of comment above the call. A reader who finds those lines can check the sort without running it.
