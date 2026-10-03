<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-frequency-windows -->
## Fixed Frequency Windows

<!-- stage: context -->
### A Jeweler Matching Bead Stretches

A jeweler has a long strand of colored glass beads, one letter per color, and a small sample card showing a handful of beads, say five. A customer asks her to point out every place along the strand where five consecutive beads use exactly the same colors as the sample card, in any order. Two reds, one blue and two greens on the card mean two reds, one blue and two greens in the stretch, however they are arranged.

She lays the card beside the strand and slides it along one bead at a time. At each position she has to decide quickly whether the five beads under the card agree with the card. The order of the beads does not matter, only how many of each color there are, and the strand has tens of thousands of beads.

<!-- stage: naive -->
### Sort Every Stretch And Compare

The plain method copies each stretch of the right length, puts its beads in order, and compares with the sample after it has been put in order once.

```java
static java.util.List<Integer> startsBySorting(String strand, String card) {
    java.util.List<Integer> starts = new java.util.ArrayList<>();
    int m = card.length();
    char[] wanted = card.toCharArray();
    java.util.Arrays.sort(wanted);
    for (int s = 0; s + m <= strand.length(); s++) {
        char[] piece = strand.substring(s, s + m).toCharArray();
        java.util.Arrays.sort(piece);
        if (java.util.Arrays.equals(piece, wanted)) starts.add(s);
    }
    return starts;
}
```

This returns every starting bead whose stretch has the same colors as the card, and an empty list when the card is longer than the strand.

<!-- stage: bottleneck -->
### Sorting Repeats Work On Shared Beads

Every stretch is copied and sorted from scratch, which costs about m log m steps, and there are n - m + 1 stretches. The total is O(n * m log m), and even a cheaper way of counting from scratch would still be O(n * m). Neighbouring stretches share m - 1 beads, so almost all of that work reproduces what the previous position already knew.

The sort also throws away the thing we need most. After sorting, the information that a stretch has two reds is buried inside a new arrangement, and moving to the next stretch means building another one. What we want is a small record of how many of each color the current stretch contains, which can be updated at its two ends in constant time. If the number of possible colors is fixed and small, comparing two such records costs a constant too, and the whole strand is handled in O(n) time.

<!-- stage: insight -->
### Keep A Tally Of The Current Stretch

Replace the sorted copy with a tally. For lowercase letters the tally is a **count array** of 26 integers, where `counts[c - 'a']` says how many beads of color `c` lie in the current stretch. When the frame moves one step, the entering bead adds one to its slot and the leaving bead removes one from its slot. Everything else in the tally is untouched, so each move costs two array updates no matter how long the stretch is.

The tally is what we compare, and the thing being compared is the **frequency signature** of a stretch: the full list of how many of each color it holds. Two stretches are anagrams of each other exactly when their signatures are equal, so the card's signature is computed once, and each position then needs a comparison of two arrays of fixed length 26, which is constant work. The invariant is that after the entering and leaving updates, the tally describes exactly the beads in positions `left` through `right`, and that range has length m.

Multiplicity is the reason a simple set of colors is not enough. A card with two reds and one blue is not matched by a stretch with one red, one blue and a green, even though both stretches contain only colors from the card, and a set cannot tell them apart. Only a signature that keeps the **multiplicity** of each color can. A related shortcut, checking that every card color appears in the stretch at least once, fails for the same reason.

The size of the array is a promise about the input. An array of 26 slots works because the strand uses lowercase letters only. If other characters could appear, the array would need a larger domain or a hash map from character to count.

<!-- names: count array, frequency signature, multiplicity -->

<!-- stage: variables -->
### Tally, Card And Frame Position

`need` is the signature of the card, built once before the pass and never changed. `have` is the tally of the current stretch, one slot per allowed character, and it is updated at both edges at every step. The single-array variant keeps `balance`, the card's counts minus the stretch's counts. `right` is the bead entering the frame, and the leaving bead sits at `right - m`, where m is the card length. `found` collects the answers, or a single boolean records whether any position matched. The two arrays are compared only once the frame holds exactly m beads, because before that moment the tally describes a shorter stretch and could never be a valid match.

<!-- stage: trace -->
### Two Strands Against Two Cards
 
The first trace searches the strand "abcbacab" for the card "abc", so m is 3, and its first step shows the frame right after the first three beads have filled the tally. The step to study is the third one, where the beads "cba" sit under the frame: the stretch has one of each color, the signature equals the card's, and the start is recorded.

```trace
{"cells":["a","b","c","b","a","c","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":2},"vars":{"a":1,"b":1,"c":1,"match":"yes"},"note":"The first 3 beads are in the tally, so the stretch is abc. The tally matches the card, so the start 0 joins the answers."},{"at":{"left":1,"right":3},"vars":{"a":0,"b":2,"c":1,"match":"no"},"note":"a leaves and b enters, so the stretch is bcb. The tally differs from the card, so nothing is recorded."},{"at":{"left":2,"right":4},"vars":{"a":1,"b":1,"c":1,"match":"yes"},"note":"b leaves and a enters, so the stretch is cba. The tally matches the card, so the start 2 joins the answers."},{"at":{"left":3,"right":5},"vars":{"a":1,"b":1,"c":1,"match":"yes"},"note":"c leaves and c enters, so the stretch is bac. The tally matches the card, so the start 3 joins the answers."},{"at":{"left":4,"right":6},"vars":{"a":2,"b":0,"c":1,"match":"no"},"note":"b leaves and a enters, so the stretch is aca. The tally differs from the card, so nothing is recorded."},{"at":{"left":5,"right":7},"vars":{"a":1,"b":1,"c":1,"match":"yes"},"note":"a leaves and b enters, so the stretch is cab. The tally matches the card, so the start 5 joins the answers."}]}
```

The second trace uses a different shape: the strand "zzabzaab" and the card "aab", which needs two a beads and one b. Look closely at start 2, where the stretch "abz" has one a, one b and one z, and so is not a match even though it includes both card colors. The only match comes at the very end, which shows that the frame can pass several near misses first.

```trace
{"cells":["z","z","a","b","z","a","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":2},"vars":{"a":1,"b":0,"z":2,"match":"no"},"note":"The first 3 beads are in the tally, so the stretch is zza. The tally differs from the card, so nothing is recorded."},{"at":{"left":1,"right":3},"vars":{"a":1,"b":1,"z":1,"match":"no"},"note":"z leaves and b enters, so the stretch is zab. The tally differs from the card, so nothing is recorded."},{"at":{"left":2,"right":4},"vars":{"a":1,"b":1,"z":1,"match":"no"},"note":"z leaves and z enters, so the stretch is abz. The tally differs from the card, so nothing is recorded."},{"at":{"left":3,"right":5},"vars":{"a":1,"b":1,"z":1,"match":"no"},"note":"a leaves and a enters, so the stretch is bza. The tally differs from the card, so nothing is recorded."},{"at":{"left":4,"right":6},"vars":{"a":2,"b":0,"z":1,"match":"no"},"note":"b leaves and a enters, so the stretch is zaa. The tally differs from the card, so nothing is recorded."},{"at":{"left":5,"right":7},"vars":{"a":2,"b":1,"z":0,"match":"yes"},"note":"z leaves and b enters, so the stretch is aab. The tally matches the card, so the start 5 joins the answers."}]}
```

<!-- stage: code -->
### Counting Ones, Anagram Starts, Permutation

```java
static int[] onesPerBlock(int[] bits, int k) {
    int[] ones = new int[bits.length - k + 1];
    int inside = 0;
    for (int right = 0; right < bits.length; right++) {
        inside += bits[right];
        if (right >= k) inside -= bits[right - k];
        if (right >= k - 1) ones[right - k + 1] = inside;
    }
    return ones;
}

static java.util.List<Integer> anagramStarts(String text, String pattern) {
    java.util.List<Integer> found = new java.util.ArrayList<>();
    int m = pattern.length();
    if (m > text.length()) return found;
    int[] need = new int[26], have = new int[26];
    for (int i = 0; i < m; i++) need[pattern.charAt(i) - 'a']++;
    for (int right = 0; right < text.length(); right++) {
        have[text.charAt(right) - 'a']++;
        if (right >= m) have[text.charAt(right - m) - 'a']--;
        if (right >= m - 1 && java.util.Arrays.equals(need, have)) found.add(right - m + 1);
    }
    return found;
}

static boolean hasPermutation(String pattern, String text) {
    int m = pattern.length();
    if (m > text.length()) return false;
    int[] balance = new int[26];
    for (int i = 0; i < m; i++) balance[pattern.charAt(i) - 'a']++;
    for (int i = 0; i < text.length(); i++) {
        balance[text.charAt(i) - 'a']--;
        if (i >= m) balance[text.charAt(i - m) - 'a']++;
        if (i >= m - 1) {
            boolean zero = true;
            for (int c = 0; c < 26 && zero; c++) zero = balance[c] == 0;
            if (zero) return true;
        }
    }
    return false;
}
```

Each position does two updates and one comparison of 26 slots, so time is O(26 n), which is O(n) for a fixed alphabet, and extra space is the 26-slot arrays. The first method is the plain sum from the previous lesson with bits as contributions. The last method keeps a single balance array instead of two, where the card adds and the stretch subtracts, so a match means every slot is zero.

<!-- stage: applicability -->
### Fixed Length With A Multiset Test

Suppose every candidate has the same length but validity depends on what the candidate contains, as with anagrams, permutations, or a block that must hold a given number of ones. Then a tally that is repaired at two ends is the natural tool. Name the invariant first: the tally describes exactly the current length-k stretch, and nothing is compared before the stretch reaches full length.

The first false friend is sorting every stretch, which restores correctness but destroys linear time, as the bottleneck showed. A second false friend is a set of seen characters, which forgets multiplicity and says yes to stretches that merely use the same colors.

In Java the hazard is the domain. `text.charAt(i) - 'a'` is a valid index only for lowercase letters, and a capital letter or a digit produces a negative or oversized index and an exception. State the alphabet in the contract, or choose a larger array or a `HashMap<Character, Integer>`. Compare arrays with `Arrays.equals`, never with `==`, which would compare references, and handle the case where the pattern is longer than the text before building anything.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-counts -->

**Prerequisites.** The fixed-size sums lesson, where a count is a sum of zero and one contributions.

**Problem.** Given an array that holds only 0 and 1 and a block length `k`, return an int array whose entry `i` is the number of ones among positions `i` to `i + k - 1`. Maintain one counter, and leave the input as it is.

**Constraints.** 1 <= k <= bits.length <= 100000, and every entry is 0 or 1. No element may be read more than twice.

**Example 1.** Input `bits = [1, 0, 1, 1, 0, 0, 1], k = 4`, output `[3, 2, 2, 2]`.

**Example 2.** Input `bits = [0, 0, 0], k = 3`, output `[0]`.

**Hint.** Which value leaves when `right` reaches k, and does the counter ever need to know about the zeros? What is the smallest right for which an entry can be written?

**Changed decision.** First rung: the tally is a single counter for one color, which is the smallest possible frequency state.

#### [Vary] Find All Anagrams in a String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Prerequisites.** The binary counts exercise above.

**Problem.** Given a text and a pattern of lowercase letters, return every start index at which the text has a substring that is an anagram of the pattern, in increasing order. Compare two count arrays of 26 slots after every move.

**Constraints.** 1 <= pattern.length(), 0 <= text.length() <= 100000, lowercase English letters only. A pattern longer than the text yields an empty list, and the code must say so.

**Example 1.** Input `text = "abcbacab", pattern = "abc"`, output `[0, 2, 3, 5]`.

**Example 2.** Input `text = "aaaa", pattern = "aa"`, output `[0, 1, 2]`.

**Hint.** What is the first right at which the stretch has m letters? What should happen when the pattern is longer than the text?

**Changed decision.** The state is a whole signature instead of one counter, and every matching start is recorded instead of one count.

#### [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Prerequisites.** The anagram exercise above.

**Problem.** Given a text, a pattern such as `aab`, and a block length `k` that is at least the pattern length, count the blocks of length `k` that contain at least as many of each letter as the pattern requires. A pattern with a repeated letter needs that letter repeated, so a plain set of letters is not a valid test.

**Constraints.** Lowercase letters only, 1 <= pattern.length() <= k <= text.length() <= 100000. Do work proportional to the text length, with no scan of 26 slots per step.

**Example 1.** Input `text = "abacaab", pattern = "aab", k = 4`, output 3.

**Example 2.** Input `text = "abxcb", pattern = "aab", k = 3`, output 0.

**Hint.** Keep a number that says how many required letters are still missing, and update it only when a changed slot crosses its required amount. Why would a set of letters accept the second example's first block?

**Changed decision.** Validity is a lower bound on each count rather than equality, and the repeated letter makes a set of colors invalid.

#### [Recognize] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Prerequisites.** The three exercises above.

**Problem.** Given a pattern and a text, return whether the text contains a substring that is a permutation of the pattern. Only existence matters, so stop at the first match, and keep a single array that holds the difference between the pattern's counts and the stretch's counts.

**Constraints.** Lowercase letters only, 1 <= pattern.length() and 0 <= text.length() <= 100000. A pattern longer than the text is allowed and answers false.

**Example 1.** Input `pattern = "abbc", text = "cbxabcb"`, output true.

**Example 2.** Input `pattern = "aab", text = "abxbaxa"`, output false.

**Hint.** What does it mean when every slot of the difference array is zero? What can the answer be before the stretch has reached length m?

**Changed decision.** The question is a yes or no, so the pass can stop early, and the state is one balance array instead of two tallies.
