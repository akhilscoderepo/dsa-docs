<!-- lesson-kind: standard -->
<!-- lesson-id: rolling-hash -->
## Rolling Hash

<!-- stage: context -->
### Why Equal Checksums Are Not Equal Data

A backup tool splits each file into fixed-size blocks and stores a block only once. To find duplicates quickly, it keeps a 32-bit checksum for every stored block and treats a new block with a known checksum as a copy. The design works for months. Then two different blocks produce the same checksum, the tool skips the second block, and a restore returns the wrong bytes without any error message. A 32-bit value has about 4.3 billion possibilities, yet random blocks start to repeat a value after roughly 77,000 of them, so the failure is certain at scale and not a rare accident.

The same tension appears wherever software compares many pieces of equal length. A genome tool looks for 10-letter sequences that occur twice in a DNA string. A plagiarism checker looks for the longest passage shared by two halves of a document. Comparing every piece letter by letter is slow, and a short fingerprint is fast but can be wrong. This lesson asks how to compute a fingerprint for every window of a string at almost no cost, and how to keep the answer correct when two fingerprints agree by accident.

<!-- stage: naive -->
### Copying Every Window Into A Set

The direct method cuts out each window of length `k`, puts the text into a `HashSet<String>`, and reports a repeat when the set already holds the text. Equality is exact here, because the set compares the actual characters.

```java
static int firstRepeatStartNaive(String s, int k) {
    java.util.HashSet<String> seen = new java.util.HashSet<>();
    for (int start = 0; start + k <= s.length(); start++) {
        String window = s.substring(start, start + k);
        if (!seen.add(window)) return start;
    }
    return -1;
}
```

On `"abcdabc"` with `k = 3` the method returns 4, the start of the second `"abc"`. The answer is correct. The cost is in what the loop does for each start: it copies `k` characters into a new `String`, and the set then reads those `k` characters again to compute a hash code and, on a match, once more to compare.

```predict
The loop above handles a string of length n with window length k. How many characters does it copy and read in total, and what changes when k grows to half of n?

Each of the n - k + 1 windows costs about k characters to copy and about k more to hash, so the copy costs (n - k + 1) * k characters and the hashing costs the same amount again. When k is n / 2, each of those two counts is about n^2 / 4, so the total is about n^2 / 2 character reads, and the set also holds the copied characters in memory at once.
```

<!-- stage: bottleneck -->
### Counting The Characters Read Twice

#### Cost Of The Direct Method

For `n` windows of length `k`, the direct method touches about `n * k` characters, which is O(n * k) time, and the set stores the same amount, which is O(n * k) memory. With `n = 1,000,000` and `k = 10` that is ten million character copies and the cost is acceptable. With `n = 30,000` and `k = 15,000` it is hundreds of millions of character copies, and the set holds all of them.

The longest duplicate substring problem makes the cost worse, because the window length is unknown. A search over lengths calls the window check about `log n` times with lengths up to `n`, so the direct method costs O(n^2 log n) in total. For `n = 30,000` that is roughly seven billion character reads.

#### The Repeated Work

Two neighbouring windows share all characters except one at each end. In `"abcdabc"` with `k = 3`, the window at start 0 is `"abc"` and the window at start 1 is `"bcd"`, so `k - 1 = 2` of the 3 characters are the same. The direct method reads those shared characters again for every new window. That repeated reading is the named waste. A better method must produce the summary of the next window from the summary of the current window and the two characters that differ, in constant time.

<!-- stage: insight -->
### Updating The Summary Letter By Letter

#### What A Polynomial Hash Stores

A **polynomial hash** turns a window of characters into one number. Give each character a numeric code, pick a base `B`, and treat the window as the digits of a number written in base `B`. The window `c0 c1 ... c(k-1)` gets the value `c0 * B^(k-1) + c1 * B^(k-2) + ... + c(k-1)`, reduced by a fixed modulus `M` so it stays small enough for a `long`. This lesson fixes a policy for lowercase text: the letters `a` to `z` map to the codes 1 to 26, never 0, and the base is 27, which is larger than every code. Two distinct windows of the same length would then have distinct values if no reduction took place. The reduction by `M = 1,000,000,007` is what allows a collision.

<!-- names: polynomial hash, rolling update, collision check -->

#### How The Rolling Update Works

The **rolling update** moves the window one position to the right. Subtract the outgoing character times `B^(k-1)`, multiply the remainder by `B`, and add the incoming character. Each of the three operations touches one character, so the new value costs O(1) instead of O(k). The value `B^(k-1) mod M` is computed once before the scan. In Java the subtraction can leave a negative number, because the `%` operator keeps the sign of the left operand, so the code adds `M` after the subtraction to return to the range 0 to `M - 1`.

#### Why A Collision Check Is Needed

Reducing by a modulus means that different windows can share a value. With `n` windows there are about `n^2 / 2` pairs, and a single modulus near one billion gives each pair a chance of about one in a billion. For `n = 30,000` the expected number of accidental matches in one pass is about 0.45, so a real run meets collisions regularly. The **collision check** is the rule that a hash match is only a candidate. The code compares the two windows character by character, using start indexes into the original string and no substring copy, and accepts the match only when every character agrees. The check costs O(k) but runs only on a match, so a pass over distinct windows pays almost nothing for it.

For DNA the policy is different and stronger. The four letters get the 2-bit codes A as 0, C as 1, G as 2 and T as 3, and the window is the 2-bit digits written in base 4. A window of 10 letters needs 20 bits, which fits in an `int` without any modulus, so the value is exact and a match needs no check.

<!-- stage: variables -->
### Values The Scan Keeps

The scan keeps a small set of named values, and each one belongs to the policy stated above.

- **code** is the number for one letter, 1 to 26 for `a` to `z`.
- **BASE** is the constant 27, one larger than the biggest code.
- **MOD** is the constant 1,000,000,007, a prime that keeps every product inside a `long`.
- **power** is `BASE^(k-1) mod MOD`, the weight of the outgoing letter.
- **hash** is the value of the current window, always in the range 0 to `MOD - 1`.
- **seen** maps a hash value to the start indexes of the windows that produced it.
- **DNA code** is the 2-bit number for one letter in the DNA policy: A is 0, C is 1, G is 2 and T is 3.

<!-- stage: trace -->
### Sliding Across Two Strings

#### First String Finds A Real Repeat

Take `s = "abcdabc"` with `k = 3`, base 27 and modulus 1,000,000,007. The weight `power` is 729. The pointer `end` marks the last index of the current window. At `end = 2` the window `"abc"` has the value 1 * 729 + 2 * 27 + 3 = 786. Sliding to `end = 3` subtracts `a` times 729, leaving 57, multiplies by 27 and adds 4 for `d`, which gives 1543 for `"bcd"`. The next two slides give 2296 for `"cda"` and 2945 for `"dab"`. At `end = 6` the window `"abc"` has the value 786 again. The table lookup finds the earlier start 0, the collision check compares the three letters, and all of them agree, so the repeat is real.

#### Second String Meets A False Match

To make a collision visible by hand, the second trace uses the small modulus 101, so `power` is 22. The string is `"abbcde"` and `k = 3`. The first window `"abb"` has the value 78. The slide to `"bbc"` subtracts 22 and gives 0 after the multiplication. The slide to `"bcd"` subtracts 44 from 0, which gives -44. The code adds 101 and continues with -44 + 101 = 57, which is the reason for the normalization. Then 57 * 27 + 4 = 1543, which is 28 modulo 101, so the new hash is 28. The slide to `"cde"` also normalizes and ends at 78, the same value as `"abb"`. The table reports start 0, the collision check compares `c` with `a` and rejects the match, and the scan correctly finds no repeat.

#### Stepping Through Both Strings

```trace
{"cells":["a","b","c","d","a","b","c"],"pointers":["end"],"steps":[{"at":{"end":2},"vars":{"window":"abc","hash":786,"check":"-"},"note":"end = 2: window abc has hash 786."},{"at":{"end":3},"vars":{"out":1,"raw":57,"window":"bcd","hash":1543,"check":"-"},"note":"end = 3: removing a leaves 57. The window bcd then has hash 1543."},{"at":{"end":4},"vars":{"out":2,"raw":85,"window":"cda","hash":2296,"check":"-"},"note":"end = 4: removing b leaves 85. The window cda then has hash 2296."},{"at":{"end":5},"vars":{"out":3,"raw":109,"window":"dab","hash":2945,"check":"-"},"note":"end = 5: removing c leaves 109. The window dab then has hash 2945."},{"at":{"end":6},"vars":{"out":4,"raw":29,"window":"abc","hash":786,"check":"equal"},"note":"end = 6: removing d leaves 29. The window abc then has hash 786. The table holds start 0 for this hash, and all 3 letters agree, so the repeat is real."}]}
```

```trace
{"cells":["a","b","b","c","d","e"],"pointers":["end"],"steps":[{"at":{"end":2},"vars":{"window":"abb","hash":78,"check":"-"},"note":"end = 2: window abb has hash 78."},{"at":{"end":3},"vars":{"out":1,"raw":56,"window":"bbc","hash":0,"check":"-"},"note":"end = 3: removing a leaves 56. The window bbc then has hash 0."},{"at":{"end":4},"vars":{"out":2,"raw":-44,"window":"bcd","hash":28,"check":"-"},"note":"end = 4: removing b leaves -44, which is negative, so adding 101 gives 57. The window bcd then has hash 28."},{"at":{"end":5},"vars":{"out":2,"raw":-16,"window":"cde","hash":78,"check":"differ"},"note":"end = 5: removing b leaves -16, which is negative, so adding 101 gives 85. The window cde then has hash 78. The table holds start 0 for this hash, but abb differs from cde, so the check rejects the match."}]}
```

<!-- stage: code -->
### Scanning With Hashes And Index Checks

#### The Scan With Verification

The class below applies the policy from the insight. The method `firstRepeatStart` takes the modulus as a parameter so the same code can be tried with a tiny modulus, and the method `sameWindow` compares two windows by index.

```java
final class RollingScan {
    static final long BASE = 27;

    // Compares two windows of length k in place; no substring is created.
    static boolean sameWindow(String s, int a, int b, int k) {
        for (int j = 0; j < k; j++) {
            if (s.charAt(a + j) != s.charAt(b + j)) return false;
        }
        return true;
    }

    // Returns the start of the first window equal to an earlier one, or -1.
    static int firstRepeatStart(String s, int k, long mod) {
        int n = s.length();
        if (k <= 0 || k > n) return -1;
        long power = 1;
        for (int j = 1; j < k; j++) power = power * BASE % mod;
        java.util.HashMap<Long, java.util.ArrayList<Integer>> seen = new java.util.HashMap<>();
        long hash = 0;
        for (int end = 0; end < n; end++) {
            int in = s.charAt(end) - 'a' + 1;
            if (end >= k) {
                int out = s.charAt(end - k) - 'a' + 1;
                hash = (hash - out * power % mod + mod) % mod;
            }
            hash = (hash * BASE + in) % mod;
            if (end < k - 1) continue;
            int start = end - k + 1;
            java.util.ArrayList<Integer> earlier = seen.computeIfAbsent(hash, h -> new java.util.ArrayList<>());
            for (int other : earlier) if (sameWindow(s, other, start, k)) return start;
            earlier.add(start);
        }
        return -1;
    }
}
```

#### Cost Of The Scan

The scan reads each character once for the update, which is O(n) time, plus O(k) for each collision check. With a large modulus the checks run almost only on true repeats, and the scan returns at the first one, so the expected cost is O(n + k). The table holds up to `n - k + 1` start indexes, which is O(n) memory, and it holds no characters, in contrast to the O(n * k) memory of the direct method. If many windows share one hash value, the lists grow and the scan degrades, which is why the modulus must be large and the check must stay.

<!-- stage: applicability -->
### Deciding When A Hash Fits

#### The Invariant To Keep

After each slide, `hash` must equal the polynomial value of exactly the current window under the fixed base, modulus and letter codes. That statement is the invariant of the method. It breaks if the base or the codes change midway, if the subtraction is left negative, or if the multiplication runs in `int` and overflows. In Java the product `1,000,000,006 * 27` already exceeds the `int` range, so every intermediate value lives in a `long`.

#### The False Friend Of Equal Hashes

Equal hash values are a false friend of equal windows. They prove a difference when they disagree, since equal windows always give equal values, but they prove nothing when they agree. A solution that returns the answer on a hash match alone passes small tests and fails on the one input where two windows collide. The collision check from the insight is the fix, and the check compares indexes without creating a `substring`.

#### When Another Method Fits Better

A hash needs equal-length windows, so a single comparison of two unrelated strings is better done with `String.equals` or `regionMatches`. When the alphabet is tiny and the window short, as with 10 DNA letters, an exact 2-bit code replaces the modulus and the check disappears. When a guarantee against adversarial input matters more than speed, because the cost of a long run of collisions is quadratic, the suffix structures covered later in this chapter give a worst-case bound that does not depend on a lucky choice of base and modulus. Treat the hash as a fast filter whose output is verified, and do not use it where an unverified answer would corrupt data.

<!-- stage: exercises -->
### Exercises

#### [Build] Fixed-Window Hash (Author exercise)
<!-- id: as-fixed-window-hash -->

**Prerequisites.** The rolling update and the letter policy from this lesson.

**Problem.** A string `s` of lowercase letters `a` to `z` and a window length `k` are given. Map each letter to its code, `a` to 1 up to `z` to 26. The hash of a window `w` of length `k` is the sum over positions `j` from 0 to `k - 1` of `code(w[j]) * 27^(k-1-j)`, reduced modulo 1,000,000,007. Return the hash of the last window, the one that starts at index `s.length() - k`. Compute it by sliding from the first window, which means removing the outgoing letter and appending the incoming letter at each step.

**Constraints.** The limits are:
- **Length** of `s` is between 1 and 100,000.
- **Window** `k` satisfies `1 <= k <= s.length()`.
- **Alphabet** is lowercase `a` to `z` only.
- **Answer** is a `long` in the range 0 to 1,000,000,006.

**Example 1.** Input `s = "abcab"`, `k = 3`, output 2216, the hash of `"cab"`.

**Example 2.** Input `s = "zzzzzzzzzz"`, `k = 10`, output 130653411. The window is the whole string, so no slide happens and the value is reduced several times.

**Hint.** Build the first window with the same multiply-and-add step that the slide uses. What value must you precompute for the outgoing letter?

**Changed decision.** Basic case: one window summary replaces a rescan of `k` letters at each step.

#### [Vary] Repeated DNA Sequences (LeetCode 187)
<!-- id: as-repeated-dna -->

**Prerequisites.** The fixed-window hash exercise and the 2-bit DNA codes from the insight.

**Problem.** Let `s` be a string over the letters `A`, `C`, `G` and `T`. A sequence is a substring of length exactly 10. Return every sequence that occurs at least twice in `s`, where occurrences may overlap, each sequence listed once, in ascending alphabetical order. This lesson uses the exact 2-bit code of each window as its key, so the contract here asks for sorted output and never relies on a modulus.

**Constraints.** The limits are:
- **Length** of `s` is between 0 and 100,000.
- **Alphabet** is `A`, `C`, `G` and `T` only.
- **Answer** is a list of 10-letter strings, empty when no sequence repeats.
- **Order** is ascending by the order A, C, G, T.

**Example 1.** Input `s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"`, output `["AAAAACCCCC", "CCCCCAAAAA"]`.

**Example 2.** Input `s = "AAAAAAAAAAAAA"` with 13 letters, output `["AAAAAAAAAA"]`. Four overlapping windows are equal, yet the sequence appears once in the answer. An input shorter than 10 letters gives an empty list.

**Hint.** Twenty bits hold ten letters. Which operation drops the oldest two bits when a new letter enters?

**Changed decision.** The stored key changes from a modulus-reduced hash to an exact 2-bit code, so the collision check is removed.

#### [Boundary] Negative Modular Difference (Author exercise)
<!-- id: as-negative-modular-difference -->

**Prerequisites.** The rolling update and the Java behavior of `%` for negative values.

**Problem.** A string `s` of lowercase letters has the codes `a` to 1 up to `z` to 26. A window length `k` is given, and the hash uses base 27 and modulus 101. Return the array of hashes of all windows of length `k`, from the leftmost to the rightmost, where the hash of a window `w` is the sum of `code(w[j]) * 27^(k-1-j)` for `j` from 0 to `k - 1`, reduced modulo 101. Compute each hash from the previous one by sliding. After the outgoing letter is removed, the intermediate value must be brought back into the range 0 to 100 before the multiplication.

**Constraints.** The limits are:
- **Length** of `s` is between 0 and 1,000.
- **Window** `k` is at least 1, and the answer is empty when `k > s.length()`.
- **Alphabet** is lowercase `a` to `z` only.
- **Answer** has `s.length() - k + 1` values, each between 0 and 100.

**Example 1.** Input `s = "abcab"`, `k = 3`, output `[79, 25, 95]`. The second slide subtracts 44 from 25 and gets -19 before the fix.

**Example 2.** Input `s = "zyxzy"`, `k = 3`, output `[59, 12, 43]`. The first slide subtracts 572 from 59, so the unreduced difference is -513 and a single addition of 101 would still leave it negative.

**Hint.** What range does `%` give for a negative left operand in Java? How many multiples of 101 can the subtracted term span?

**Changed decision.** The subtracted term is reduced before the difference is taken, so one addition of the modulus afterwards is enough and the order of those operations matters.

#### [Recognize] Longest Duplicate Substring (LeetCode 1044)
<!-- id: as-longest-duplicate-substring -->

**Prerequisites.** The collision check and the fixed-window scan from this lesson.

**Problem.** A string `s` of lowercase letters is given. A duplicate substring is a substring that occurs at least twice in `s`, where the occurrences may overlap. Return a duplicate substring of maximum length. When several duplicate substrings share the maximum length, return any one of them. When no duplicate exists, return the empty string. The lesson on suffix structures later in this chapter solves this problem with a suffix array. Here the contract requires a binary search on the length with a rolling hash, and a verified comparison for every hash match.

**Constraints.** The limits are:
- **Length** of `s` is between 0 and 30,000.
- **Alphabet** is lowercase `a` to `z` only.
- **Answer** is a substring of `s`, or the empty string.
- **Ties** allow any longest duplicate.
- **Verification** is by index comparison, with no substring created inside the search loop.

**Example 1.** Input `s = "banana"`, output `"ana"`. The two occurrences start at indexes 1 and 3 and overlap on the letter `a`. This is the only duplicate of length 3.

**Example 2.** Input `s = "aaaaa"`, output `"aaaa"`, with occurrences at indexes 0 and 1. The input `s = "abcd"` gives the empty string.

**Hint.** If a duplicate of length L exists, does one of length L - 1 exist? What does that answer let you do with the lengths?

**Changed decision.** The window length is no longer given, so a binary search chooses it and the rolling hash answers one yes-or-no question per length.
