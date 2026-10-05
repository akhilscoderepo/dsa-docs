<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-xor -->
## Use XOR As A Running Total

<!-- stage: context -->
### Checking Digests Of Record Ranges

A storage service writes records with numeric identifiers. For each range of records it keeps a digest, which is a single number built by combining the identifiers with the operator `^` in Java. A verifier receives a range of records and a digest, recomputes the digest, and compares the two numbers.

The service has 40,000 records and a stream of verification requests, each for a different range. Recomputing the digest from the first record of the range makes every request cost as much as the range is long. The remaining problem is to answer each request in constant time, although the operator `^` has no subtraction to remove the records before the range.

<!-- stage: naive -->
### Combining Every Identifier In The Range

The direct method combines the identifiers of the range one at a time with `^`, starting from 0.

```java
static int[] digestEach(int[] ids, int[][] queries) {
    int[] out = new int[queries.length];
    for (int q = 0; q < queries.length; q++) {
        int digest = 0;
        for (int i = queries[q][0]; i <= queries[q][1]; i++) digest ^= ids[i];
        out[q] = digest;
    }
    return out;
}
```

For `[5, 1, 7, 2, 6]` and the range from index 1 through index 3, the loop combines 1, 7 and 2 and returns 4.

```predict
The service holds 40,000 identifiers and receives 40,000 queries that each cover all of them. How many `^` operations does `digestEach` perform?

It performs 40,000 times 40,000 operations, which is 1,600,000,000. Each query costs the length of its range, so the cost is O(n) per query and O(n * q) in total.
```

<!-- stage: bottleneck -->
### Overlapping Ranges Repeat Their Work

Two queries over overlapping ranges combine the same identifiers twice. A query of length `w` performs `w` operations, so `q` queries cost O(n * q) in the worst case. The identifiers never change between queries, so the repeated work depends only on the data.

Sums solved this problem with a stored total and a subtraction. The operator `^` offers no subtraction. The question is whether a stored value can still remove the records before the range, and that depends on how `^` treats a value that it meets twice.

<!-- stage: insight -->
### Combine A Value Twice And It Vanishes

**Exclusive or**, written `^` in Java and called XOR, combines two integers bit by bit. Each result bit is 1 when the two input bits differ and 0 when they match. Three properties follow. The value `x ^ 0` equals `x`. The value `x ^ x` equals 0. The order and grouping of several `^` operations do not change the result.

#### Applying The Same Value Twice

The second property makes XOR **self-inverse**, which means that combining with a value a second time undoes the first combination. For any `y`, the expression `(y ^ x) ^ x` equals `y ^ (x ^ x)`, which equals `y ^ 0`, which equals `y`. The operation therefore acts as its own subtraction.

#### The Stored Array And The Query

The **prefix XOR** array `px` has length `n + 1`. It has `px[0] = 0` and `px[i + 1] = px[i] ^ ids[i]`, so `px[i]` is the XOR of the first `i` values. The value 0 is neutral for XOR, so it plays the role that 0 plays for a sum.

The XOR of the range from `left` through `right` equals `px[right + 1] ^ px[left]`. Both entries contain the identifiers before `left`. Those identifiers meet twice and cancel, so only the range remains. Preprocessing costs O(n) and each query costs O(1).

<!-- names: exclusive or, self-inverse, prefix XOR -->

#### Counting With A Target

The same idea works for the count of ranges with XOR equal to a target `k`. The range from boundary `a` to boundary `b` has XOR `px[b] ^ px[a]`. That value equals `k` exactly when `px[a] = px[b] ^ k`, because XOR with `k` undoes itself. A frequency map of earlier prefix values then counts the matches, as in the lesson on counting sums.

<!-- stage: variables -->
### Five Names And Their Roles

Five entries below name the values of the construction, the query and the counting loop.

- **px** is the array of length `n + 1` where entry `i` is the XOR of the first `i` values.
- **left** and **right** are the first and last index of a query range, and **end** is `right + 1`.
- **k** is the target XOR in the counting version.
- **seen** is the frequency map from a prefix XOR value to the number of earlier boundaries with that value.
- **cur** is the prefix XOR through the current value in the counting loop.

All values have type `int`, because `^` on two `int` values never leaves the `int` range. No widening is needed.

<!-- stage: trace -->
### One Query And One Count

#### A Query On Five Identifiers

The input is `[5, 1, 7, 2, 6]`, and its prefix XOR array is `[0, 5, 4, 3, 1, 7]`. The query asks for index 1 through index 3. The pointer `left` marks `px[left]`, and the pointer `end` marks `px[right + 1]`. The two reads give 1 and 5, and `1 ^ 5` equals 4, which equals `1 ^ 7 ^ 2`.

```trace
{"cells":[0,5,4,3,1,7],"pointers":["left","end"],"steps":[{"at":{"left":-1,"end":-1},"vars":{"query":"[1, 3]"},"note":"The prefix XOR array is ready. The query asks for index 1 through index 3, so the reads are px[4] and px[1]."},{"at":{"left":-1,"end":4},"vars":{"px[end]":"1"},"note":"Read px[4] = 1, the XOR of the first 4 values."},{"at":{"left":1,"end":4},"vars":{"px[end]":"1","px[left]":"5"},"note":"Read px[1] = 5, the XOR of the first 1 values."},{"at":{"left":1,"end":4},"vars":{"answer":"1 ^ 5 = 4"},"note":"The first 1 values meet twice and cancel, so the answer is 4."}]}
```

#### Counting Ranges With XOR Six

The input is `[4, 2, 2, 6, 4]` and `k = 6`. The loop keeps the map of earlier prefix XOR values. At each step it looks up `cur ^ 6` and then records `cur`. The count rises to 4, and the matching ranges are `[4, 2]`, `[4, 2, 2, 6, 4]`, `[6]` and `[2, 2, 6]`.

```trace
{"cells":[4,2,2,6,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{0=1}","count":"0"},"note":"The map starts with prefix XOR 0 once, for boundary 0."},{"at":{"i":0},"vars":{"cur":"4","look up":"2","seen":"{0=1, 4=1}","count":"0"},"note":"Prefix XOR is 4. The key 4 ^ 6 = 2 occurs 0 times before, so the count becomes 0."},{"at":{"i":1},"vars":{"cur":"6","look up":"0","seen":"{0=1, 4=1, 6=1}","count":"1"},"note":"Prefix XOR is 6. The key 6 ^ 6 = 0 occurs 1 time before, so the count becomes 1."},{"at":{"i":2},"vars":{"cur":"4","look up":"2","seen":"{0=1, 4=2, 6=1}","count":"1"},"note":"Prefix XOR is 4. The key 4 ^ 6 = 2 occurs 0 times before, so the count becomes 1."},{"at":{"i":3},"vars":{"cur":"2","look up":"4","seen":"{0=1, 2=1, 4=2, 6=1}","count":"3"},"note":"Prefix XOR is 2. The key 2 ^ 6 = 4 occurs 2 times before, so the count becomes 3."},{"at":{"i":4},"vars":{"cur":"6","look up":"0","seen":"{0=1, 2=1, 4=2, 6=2}","count":"4"},"note":"Prefix XOR is 6. The key 6 ^ 6 = 0 occurs 1 time before, so the count becomes 4."}]}
```

<!-- stage: code -->
### The Array And The Count In Java

```java
static int[] buildPrefixXor(int[] ids) {
    int[] px = new int[ids.length + 1];
    for (int i = 0; i < ids.length; i++) px[i + 1] = px[i] ^ ids[i];
    return px;
}

static int rangeXor(int[] px, int left, int right) {
    return px[right + 1] ^ px[left];
}

static int countXor(int[] ids, int k) {
    java.util.HashMap<Integer, Integer> seen = new java.util.HashMap<>();
    seen.put(0, 1);
    int cur = 0, count = 0;
    for (int v : ids) {
        cur ^= v;
        count += seen.getOrDefault(cur ^ k, 0);
        seen.merge(cur, 1, Integer::sum);
    }
    return count;
}
```

Java gives `^` a lower precedence than `==`, so an expression such as `(a ^ b) == k` needs its parentheses. The array starts filled with zeros, so `px[0]` is already the neutral value. The counting loop reads the map before it records `cur`, which keeps the empty range out of the count.

<!-- stage: applicability -->
### When A Value Cancels Itself

#### The Invariant

The invariant is that `px[i]` is the XOR of the first `i` values for every `i` from 0 to `n`. The XOR of any range then equals the XOR of two entries, because the shared leading values cancel in pairs. The same argument shows that the counting loop sees each valid pair of boundaries once, at its later boundary.

#### The False Friend

The false friend is the plain sum. Sums and XOR feel alike, since both combine a prefix with a single value. The sum of two equal values is not 0, and so the difference formula for sums cannot replace the XOR formula. Using the wrong operator in the query gives numbers that look plausible and are wrong.

#### Conditions That Break The Fit

The operation must have an inverse for the stored-prefix method. A bitwise AND and a bitwise OR have no inverse, so a range AND needs a different structure. The values must also stay unchanged between queries. One update changes every later entry of the prefix array.

<!-- stage: exercises -->
### Exercises

#### [Build] XOR Of Half-Open Windows (LeetCode 1310)
<!-- id: ps-xor-half-open -->

**Prerequisites.** The prefix XOR array and the self-inverse property of this lesson.

**Problem.** Given an integer array `arr` and a list of queries `[start, end]`, return for each query the XOR of `arr[start]` through `arr[end - 1]`. The end index is not part of the window, which differs from LeetCode 1310, and a window with `start == end` has XOR 0.

**Constraints.** The limits are:
- **Length** is `0 <= arr.length <= 3 * 10^4`.
- **Values** are `int` values with `0 <= arr[i] <= 10^9`.
- **Queries** satisfy `0 <= start <= end <= arr.length`.
- **Return type** is `int[]`.

**Example 1.** Input `arr = [5,1,7,2,6]` and queries `[[1,4],[0,5],[2,2]]`, output `[4,7,0]`.

**Example 2.** Input `arr = [9]` and queries `[[0,1],[1,1]]`, output `[9,0]`.

**Hint.** With the excluded end index, which two entries of `px` bound the window?

**Changed decision.** Basic case: the operation is XOR, and the half-open window removes the `+ 1` from the formula.

#### [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Prerequisites.** The first exercise above and the frequency map of the lesson on counting sums.

**Problem.** Given an integer array `arr` and an integer `k`, count the non-empty contiguous subarrays whose XOR equals `k`.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 10^5`.
- **Values** are `int` values with `0 <= arr[i] <= 10^9`.
- **Target** satisfies `0 <= k <= 10^9`.
- **Return type** is `long`, because the count can exceed the `int` range.

**Example 1.** Input `arr = [4,2,2,6,4]` and `k = 6`, output 4.

**Example 2.** Input `arr = [3,3,3]` and `k = 3`, output 4.

**Hint.** The key to look up is `cur ^ k` and not `cur - k`. Why does XOR with `k` undo the XOR with `k`?

**Changed decision.** The lookup key changes from a difference to an XOR, while the structure of the counting loop stays.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Prerequisites.** The first exercise and the earliest-index map of the lesson on balanced spans.

**Problem.** Given an integer array `arr`, return the length of the longest non-empty contiguous subarray whose XOR is 0. Return 0 when no such subarray exists.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 10^5`.
- **Values** are `int` values with `0 <= arr[i] <= 10^9`.
- **Seed** is the prefix XOR 0 at index -1.
- **Return value** is the length.

**Example 1.** Input `arr = [1,2,3]`, output 3.

**Example 2.** Input `arr = [4,5]`, output 0.

**Hint.** A subarray that starts at index 0 has XOR 0 only when its prefix XOR is 0. Which entry of the map lets that case match?

**Changed decision.** The span can start at index 0, so the map needs the entry for the empty prefix and the earliest index must not be overwritten.

#### [Recognize] Count Triplets With Equal XOR (LeetCode 1442)
<!-- id: ps-triplets-1442 -->

**Prerequisites.** All exercises above.

**Problem.** Given an integer array `arr`, count the triplets `(i, j, k)` with `0 <= i < j <= k < arr.length` such that the XOR of `arr[i]` through `arr[j - 1]` equals the XOR of `arr[j]` through `arr[k]`.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 300`.
- **Values** are `int` values with `1 <= arr[i] <= 10^8`.
- **Order** of the indexes is `i < j <= k`.
- **Return type** is `int`.

**Example 1.** Input `arr = [5,1,4,0,4,1]`, output 11.

**Example 2.** Input `arr = [9,9,9]`, output 2.

**Hint.** The two XOR values are equal exactly when the XOR of `arr[i]` through `arr[k]` is 0. For such a pair `(i, k)`, how many choices of `j` exist?

**Changed decision.** Equal prefix XOR values at two boundaries mark a zero-XOR range, and the count of triplets is the sum of `k - i` over those ranges.
