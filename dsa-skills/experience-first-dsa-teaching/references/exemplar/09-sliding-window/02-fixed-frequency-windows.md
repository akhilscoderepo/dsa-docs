<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-frequency-windows -->
## Fixed Frequency Windows

<!-- stage: context -->
### The Scrambled Probe

A genetics lab keeps a short probe, say the letters `abc`, and wants to know where in a long DNA-like string the probe appears in any order. The string `cba` counts, so does `bac`, and `abd` does not. Position matters for where the stretch starts, but inside the stretch the order is irrelevant. Only the letters present and how many of each count.

Every candidate is again a block of one fixed length, the length of the probe. What changed from the previous lesson is the summary. A single sum can no longer describe a block, because `cba` and `cca` have the same length and share letters yet differ in content. The summary now has to be a tally of how many times each letter occurs.

<!-- stage: naive -->
### Sort And Compare

The direct approach is to copy each block, sort its letters, and compare the sorted copy against the sorted probe. Two blocks hold the same letters in any order exactly when their sorted forms are equal.

```java
static List<Integer> findScrambledBruteForce(String s, String p) {
    char[] want = p.toCharArray();
    Arrays.sort(want);
    List<Integer> starts = new ArrayList<>();
    for (int start = 0; start + p.length() <= s.length(); start++) {
        char[] block = s.substring(start, start + p.length()).toCharArray();
        Arrays.sort(block);
        if (Arrays.equals(block, want)) starts.add(start);
    }
    return starts;
}
```

The logic is sound, and a short string runs instantly.

<!-- stage: bottleneck -->
### Paying To Sort Again

Each block costs a copy of `k` letters and a sort of `k` letters, which is `k log k`, and there are `n - k + 1` blocks. With `n = 30,000` and `k = 10,000` the sorting alone does about 20,000 blocks times 130,000 comparisons, a few billion steps. The cost compounds because neighboring blocks share almost every letter, and the method sorts them as if they were strangers. It also allocates a new string and a new array per block, so it creates tens of thousands of short-lived objects.

The method runs in O(n * k log k) time. The sorting is the wasteful part, because we never needed the letters in order. We only needed to know how many of each there are.

<!-- stage: insight -->
### A Tally That Updates Itself

Two blocks hold the same letters, in any order, exactly when they have the same tally: the same number of `a`s, the same number of `b`s, and so on. If the alphabet is lowercase English, a tally is 26 integers. Building a tally for one block costs `k`, but moving from one block to the next costs two. The letter that leaves gets its slot decreased by one, and the letter that arrives gets its slot increased by one.

We call this tally a **frequency signature**: the exact count of every symbol in the window. A fixed-size range whose state is a frequency signature is a **fixed frequency window**. The signature of the probe is computed once. A block matches when its signature equals the probe's, and comparing two signatures costs the size of the alphabet, not `k`.

<!-- names: frequency signature, fixed frequency window -->

The comparison step has a cost of its own, and it is worth seeing. Comparing 26 slots per block is constant work, so the total stays O(26 * n), which is linear. A larger alphabet makes the comparison heavier, and then it pays to track a single counter of how many slots currently disagree. That refinement appears in the combination lesson at the end of the chapter. For this lesson, comparing two small arrays is the simplest correct choice.

The signature is a multiset, not a set. A set would say `aab` and `abb` are the same because both contain `a` and `b`, but the probe `aab` needs two `a`s. Counting handles repeats naturally, and a set silently loses them.

<!-- stage: variables -->
### Three Pieces Of State

The array `need` holds the probe's signature and never changes. The array `have` holds the signature of the current window, and the invariant is that `have` describes exactly the `k` letters ending at `right`. The index `right` is the newest position. The start of the window is `right - k + 1`, so it is derived, not stored. A block is reported when `have` and `need` are equal, and the result list collects its start index.

<!-- stage: trace -->
### One Run Through

Take the string `cbaebabacd` and the probe `abc`, so `k = 3`. The first three letters, `c`, `b` and `a`, fill the window. Its signature has one of each letter, which equals the probe's signature, so index 0 is a match.

The window slides. Letter `e` arrives and `c` leaves, so the window `bae` now has an `e` that the probe does not have, and the signature no longer matches. Next `b` arrives and `b` leaves, giving `aeb`, still containing `e`. Then `a` arrives and `a` leaves, giving `eba`. The `e` stays in the window for exactly three slides and then leaves.

When `b` arrives and `e` leaves, the window is `bab`: two `b`s and no `c`, which fails. Then `a` arrives and `b` leaves, giving `aba`, which also fails because there is no `c`. Next comes the `c` that completes things. Letter `c` arrives and the first `a` leaves, so the window is `bac`, one of each, and index 6 is a match. The final letter `d` arrives while `b` leaves, so the window becomes `acd`, which fails because the `b` is gone.

The answer is `[0, 6]`. Two of the eight windows matched, and every window was examined by two small updates, never by a rebuild.

```trace
{"cells":["c","b","a","e","b","a","b","a","c","d"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"c","found":0},"note":"Take in index 0 (letter c). The window is not full yet."},{"at":{"left":0,"right":1},"vars":{"window":"cb","found":0},"note":"Take in index 1 (letter b). The window is not full yet."},{"at":{"left":0,"right":2},"vars":{"window":"cba","found":0},"note":"Take in index 2 (letter a). The window is not full yet."},{"at":{"left":0,"right":2},"vars":{"window":"cba","found":1},"note":"The window is full. Its signature equals the probe's, so index 0 is a match."},{"at":{"left":1,"right":3},"vars":{"window":"bae","found":1},"note":"Add e, remove c. The window is bae; it does not match."},{"at":{"left":2,"right":4},"vars":{"window":"aeb","found":1},"note":"Add b, remove b. The window is aeb; it does not match."},{"at":{"left":3,"right":5},"vars":{"window":"eba","found":1},"note":"Add a, remove a. The window is eba; it does not match."},{"at":{"left":4,"right":6},"vars":{"window":"bab","found":1},"note":"Add b, remove e. The window is bab; it does not match."},{"at":{"left":5,"right":7},"vars":{"window":"aba","found":1},"note":"Add a, remove b. The window is aba; it does not match."},{"at":{"left":6,"right":8},"vars":{"window":"bac","found":2},"note":"Add c, remove a. The window is bac; it matches, so start 6 is recorded."},{"at":{"left":7,"right":9},"vars":{"window":"acd","found":2},"note":"Add d, remove b. The window is acd; it does not match."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static List<Integer> findScrambled(String s, String p) {
    List<Integer> starts = new ArrayList<>();
    int k = p.length();
    if (k == 0 || k > s.length()) return starts;
    int[] need = new int[26], have = new int[26];
    for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
    for (int right = 0; right < s.length(); right++) {
        have[s.charAt(right) - 'a']++;                          // arrival
        if (right >= k) have[s.charAt(right - k) - 'a']--;      // departure
        if (right >= k - 1 && Arrays.equals(have, need)) starts.add(right - k + 1);
    }
    return starts;
}
```

The array index `c - 'a'` is valid only for lowercase letters, which is a statement about the input domain and not a language guarantee. A capital letter or a digit would index outside the array or share a slot with another letter. When the problem allows more symbols, either widen the table to the stated range, such as 128 for ASCII, or switch to a `HashMap<Character, Integer>` and delete a key when its count reaches zero so that map equality still means signature equality.

The loop does `n` iterations, each with two array updates and one comparison of 26 slots, so the time is O(26 * n), which is O(n) for a fixed alphabet. The extra space is two arrays of 26, which is O(1), plus the output list. No substring is created anywhere.

<!-- stage: applicability -->
### When It Applies

Use a fixed frequency window when every candidate has the same length and validity depends on which symbols it contains and how many of each, not on their order. The invariant to state is that `have` equals the signature of the `k` symbols ending at `right`, updated by one arrival and one departure per step.

The false friend is the aggregate window from the previous lesson. A sum or a count of one kind of item is a single number, and it cannot tell `cba` from `cca`. When two different multisets can produce the same aggregate, the aggregate is too weak, and you need a signature. In the other direction, do not reach for a signature when a single count is enough, since it adds a comparison cost for no gain.

A second false friend is sorting. Sorting every block works and is the first idea most people have, but it throws away the overlap between neighbors, which is the entire reason windows exist.

Check three things before coding. State the symbol domain, because it decides the table size. Check that the probe is not longer than the text, because no block can exist then. Remember that the probe may repeat symbols, so test with something like `aab` and not only with distinct letters.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-window-counts -->

**Prerequisites.** The previous lesson on fixed-size windows; Chapter 03 string indexing.

**Problem.** Given a string `bits` made only of the characters `0` and `1`, and an integer `k`, return an array whose entry `i` is the number of `1` characters in the block of length `k` starting at index `i`. Maintain a two-slot count table for the window, one slot per character, and read the answer from it.

**Constraints.** 1 <= k <= bits.length <= 10^5 and every character is `0` or `1`. Target O(n) time and O(1) extra space beyond the output.

**Example 1.** Input `bits = "1101"`, `k = 2`, output `[2, 1, 1]`.

**Example 2.** Input `bits = "000"`, `k = 3`, output `[0]`, because the single block contains no ones.

**Hint.** Which slot of the table does an entering character change, and which slot does the leaving character change, and when does the first departure happen?

**Changed decision.** The state moves from one sum to a table with a slot per symbol, which is the smallest possible frequency signature.

#### [Vary] Find All Anagrams in a String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Prerequisites.** The binary counts exercise above; this lesson.

**Problem.** Given strings `s` and `p`, return every index `i` such that the block of `s` starting at `i`, of length `p.length()`, is a rearrangement of `p`. The indices may come back in any order.

**Constraints.** 1 <= s.length, p.length <= 3 * 10^4, and both strings consist of lowercase English letters. Target O(n) time.

**Example 1.** Input `s = "abacbabc"`, `p = "abc"`, output `[1, 2, 3, 5]`.

**Example 2.** Input `s = "aaaa"`, `p = "aa"`, output `[0, 1, 2]`. Matching blocks overlap, so the answer includes starts that are one apart.

**Hint.** If the window and the probe must contain exactly the same letters with exactly the same counts, what does it take to compare two tallies, and what must you check before you start sliding?

**Changed decision.** The summary becomes a 26-slot signature, and the answer collects every start that matches instead of a single number.

#### [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Prerequisites.** The two exercises above.

**Problem.** Given strings `s` and `p`, return the smallest index at which a block of `s` is a rearrangement of `p`, or -1 if there is none. The probe `p` may contain repeated letters, and a block must contain every letter of `p` exactly as many times as `p` does. If `p` is longer than `s`, return -1.

**Constraints.** 1 <= p.length <= 10^5, 0 <= s.length <= 10^5, and both strings contain lowercase English letters only. Target O(n) time.

**Example 1.** Input `s = "abbabb"`, `p = "aab"`, output `-1`. Every block contains both letters, but none contains two `a`s, so a set-based check would wrongly report 0.

**Example 2.** Input `s = "bbaab"`, `p = "aab"`, output `1`, from the block `"baa"`.

**Hint.** Why can a set of letters not tell `abb` from `aab`, and what does a counting table do differently when the same letter arrives twice?

**Changed decision.** The probe now repeats a letter, which exposes multiplicity, and the output is the first start or a sentinel instead of every match.

#### [Recognize] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Prerequisites.** The three exercises above.

**Problem.** Given strings `s1` and `s2`, decide whether some substring of `s2` uses exactly the letters of `s1`, with exactly the same counts. Return `true` or `false`.

**Constraints.** 1 <= s1.length, s2.length <= 10^4, and both strings consist of lowercase English letters. Target O(n) time.

**Example 1.** Input `s1 = "abc"`, `s2 = "xxcabyy"`, output `true`, because `s2` contains `"cab"`.

**Example 2.** Input `s1 = "abc"`, `s2 = "acxbcxa"`, output `false`. All three letters appear, but never within one block of three.

**Hint.** The question changes from collecting every match to asking whether one exists. What should the loop do the first time the two tallies agree?

**Changed decision.** The output shrinks to a Boolean, so the scan can stop at the first match and the code must return early.
