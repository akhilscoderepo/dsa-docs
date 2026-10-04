<!-- lesson-kind: combination -->
<!-- lesson-id: greedy-and-monotonic-stack -->
## Greedy And Monotonic Stack

<!-- stage: context -->
### The Engraver Of Lintel Hall

An engraver at Lintel Hall has been given a long stone strip carved with a row of characters, and the order of the characters may never change. She may chisel away some of them, and what remains must read as small as possible, as a number if the strip holds digits and as a word in dictionary order if it holds letters. A strip of digits must lose exactly the number of digits that the client names. A strip of letters must end up with each letter appearing once. Sometimes the client wants a fixed number of characters left standing, nothing more and nothing less.

She cannot put a chiselled character back, so every cut must be right. She also knows the reading convention: two strips are compared at the first position where they differ, and the smaller character at that position wins no matter what follows.

<!-- stage: contributions -->
### What Argument And Stack Each Bring

The greedy argument brings the licence to remove. Because strips are compared at the first difference, an earlier position matters more than every later one. If a larger character stands in front of a smaller one that has just arrived, removing the larger one improves the earliest position where the candidates could differ, and so it is never worse than keeping it, provided the removal is allowed.

The stack brings the place to look. The characters kept so far sit in reading order, and the one nearest to the newcomer is on top, so the single candidate for removal is found at once. Popping also keeps the survivors in their original order. What the plain stack of the monotonic-stack chapter lacks is any limit, so the combination adds a budget of removals, or a promise that the character will return later. The cue is a request for the smallest or largest subsequence under a length or uniqueness rule.

<!-- stage: naive -->
### Try Every Way To Chisel

The direct method generates every strip that can result from removing exactly k characters and keeps the smallest, comparing strips as numbers after dropping leading zeros.

```java
static String smallestByTrial(String s, int i, int drop, String kept) {
    if (i == s.length()) return drop == 0 ? kept : null;
    String dropped = drop > 0 ? smallestByTrial(s, i + 1, drop - 1, kept) : null;
    String retained = smallestByTrial(s, i + 1, drop, kept + s.charAt(i));
    if (dropped == null) return retained;
    if (retained == null) return dropped;
    return numericLess(dropped, retained) ? dropped : retained;
}

static boolean numericLess(String a, String b) {
    String x = a.replaceFirst("^0+", ""), y = b.replaceFirst("^0+", "");
    return x.length() != y.length() ? x.length() < y.length() : x.compareTo(y) < 0;
}
```

The answer is exact for any strip, because each of the C(n, k) outcomes is built and compared. On a strip of a dozen digits it is instant.

<!-- stage: bottleneck -->
### Almost Every Outcome Is Hopeless

There are C(n, k) outcomes, which grows faster than any polynomial, and building each takes O(n) more. Fifty digits with twenty removed is already beyond any machine. Yet most outcomes lose at the very first position where they differ from a better one, so the later characters never decide anything.

That observation suggests a different order of work. Decide the first character of the answer, then the second, and so on, and at each step keep only the best prefix. When a new character arrives that is smaller than the last character kept, the last one is the obvious culprit: removing it improves the prefix at its own position. The question is only when that removal is permitted, and the permission is where the greedy argument has to be careful.

<!-- stage: insight -->
### Pop Only When Popping Is Allowed

A **safe pop** removes the character on top of the stack because the newcomer is smaller and the removal cannot hurt. It cannot hurt because of the first-difference rule. Any answer that keeps the top and removes something later can be rewritten to remove the top instead. The rewritten answer agrees up to the top's position, and there it holds the same character as before or a smaller one. So the safe pop is an exchange, and the stack always holds the best prefix that the characters seen so far allow.

For a digit strip with k removals, the **pop budget** is k itself. Each safe pop spends one, and when the strip ends with budget left over, the extra removals come off the tail, since the stack is by then non-decreasing and the last digits are the largest. For a competitive subsequence of length k, the budget is not a count but a promise: the pop is allowed only while enough characters remain after the newcomer to fill the answer back to length k. Leading zeros need one more rule, since they are removed from the printed answer after all pops are done.

<!-- names: safe pop, pop budget, future availability -->

For distinct letters the permission is **future availability**. The top may be popped only if the same letter appears again later, because otherwise popping would lose it for good. A letter that is already in the stack is skipped when it arrives again, since the earlier copy is in a better position, and the stack keeps its order. The proof is the same exchange, with the extra condition that the removed letter has a later occurrence to take its place. A pure monotonic stack pops whenever a smaller element comes, with no budget and no promise, which is why those problems do not need this argument.

<!-- stage: variables -->
### The Stack, The Budget And The Promise

The stack is a character or integer array with a size counter `top`, and it holds the best prefix so far. For digits, `k` is the remaining pop budget and it only decreases. For letters, `last[c]` is the final position of each letter, `inStack[c]` says whether a letter is on the stack, and `i` is the position being read, so a letter is poppable when `last[c] > i`. For subsequences of a required size, `n - i` counts the characters still unread including the newcomer, so a pop is allowed when `top - 1 + (n - i) >= k`. Nothing outside the stack is ever stored, and the input is only read.

<!-- stage: trace -->
### Digits Removed And Letters Kept

The first trace removes two digits from 52913. The digit five goes on the stack. The two arrives and is smaller, so the five is popped and one removal is left. The nine goes on top of the two. The one arrives and the nine is larger, so the nine is popped and the budget is spent. The three goes on top of the one. The stack reads 2, 1, 3, so the answer is 213.

The second trace keeps each letter of dcbadbcd once, in the smallest order. The d, c, b and a arrive in descending order, and each pop is permitted because each popped letter appears again later. The stack becomes just a. The next d goes on top of the a. The b then arrives and pops that d, because another d still lies ahead, and the c and the final d are pushed, so the answer is abcd.

```trace
{"cells":["5","2","9","1","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"5","budget":2},"note":"The digit 5 starts the stack."},{"at":{"i":1},"vars":{"stack":"2","budget":1},"note":"The digit 2 is smaller than 5, so that digit is popped, spending removals, and 2 is pushed."},{"at":{"i":2},"vars":{"stack":"29","budget":1},"note":"The digit 9 is larger than the top, so nothing is popped and it is pushed."},{"at":{"i":3},"vars":{"stack":"21","budget":0},"note":"The digit 1 is smaller than 9, so that digit is popped, spending removals, and 1 is pushed."},{"at":{"i":4},"vars":{"stack":"213","budget":0},"note":"The digit 3 is larger than the top, so nothing is popped and it is pushed."}]}
```

```trace
{"cells":["d","c","b","a","d","b","c","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"d"},"note":"The letter d starts the stack."},{"at":{"i":1},"vars":{"stack":"c"},"note":"The letter c is smaller than the top, and the popped letter d appear again later, so the pop is permitted and c is pushed."},{"at":{"i":2},"vars":{"stack":"b"},"note":"The letter b is smaller than the top, and the popped letter c appear again later, so the pop is permitted and b is pushed."},{"at":{"i":3},"vars":{"stack":"a"},"note":"The letter a is smaller than the top, and the popped letter b appear again later, so the pop is permitted and a is pushed."},{"at":{"i":4},"vars":{"stack":"ad"},"note":"The letter d is larger than the top, so it is pushed without popping."},{"at":{"i":5},"vars":{"stack":"ab"},"note":"The letter b is smaller than the top, and the popped letter d appear again later, so the pop is permitted and b is pushed."},{"at":{"i":6},"vars":{"stack":"abc"},"note":"The letter c is larger than the top, so it is pushed without popping."},{"at":{"i":7},"vars":{"stack":"abcd"},"note":"The letter d is larger than the top, so it is pushed without popping."}]}
```

<!-- stage: code -->
### Three Stacks With Three Permissions

```java
static String removeKDigits(String num, int k) {
    StringBuilder stack = new StringBuilder();
    for (char c : num.toCharArray()) {
        while (k > 0 && stack.length() > 0 && stack.charAt(stack.length() - 1) > c) {
            stack.setLength(stack.length() - 1);                   // safe pop, one removal spent
            k--;
        }
        stack.append(c);
    }
    stack.setLength(stack.length() - k);                          // leftover budget comes off the tail
    int start = 0;
    while (start < stack.length() - 1 && stack.charAt(start) == '0') start++;
    return stack.length() == 0 ? "0" : stack.substring(start);
}

static String removeDuplicateLetters(String s) {
    int[] last = new int[26];
    for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
    boolean[] inStack = new boolean[26];
    StringBuilder stack = new StringBuilder();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (inStack[c - 'a']) continue;                           // the earlier copy is better placed
        while (stack.length() > 0 && stack.charAt(stack.length() - 1) > c && last[stack.charAt(stack.length() - 1) - 'a'] > i) {
            inStack[stack.charAt(stack.length() - 1) - 'a'] = false;
            stack.setLength(stack.length() - 1);
        }
        stack.append(c);
        inStack[c - 'a'] = true;
    }
    return stack.toString();
}

static int[] competitive(int[] nums, int k) {
    int n = nums.length, top = 0;
    int[] stack = new int[k];
    for (int i = 0; i < n; i++) {
        while (top > 0 && stack[top - 1] > nums[i] && top - 1 + (n - i) >= k) top--;
        if (top < k) stack[top++] = nums[i];
    }
    return stack;
}
```

Each character is pushed once and popped at most once, so every method runs in O(n) time and the stack takes at most O(n) space, or O(k) for the last one. The comparison between a stack character and the newcomer is strict, so equal characters are never popped, which keeps the earlier one and costs nothing.

<!-- stage: applicability -->
### When Removal Needs Permission

Use this combination when the answer is a subsequence that must be the smallest or largest in reading order, and it has a length, a count of removals, or a uniqueness rule. The invariant is that the stack holds the best prefix that the characters read so far permit, and every pop is justified by the first-difference exchange together with its permission. Write the permission down first, as a budget or a later occurrence or a length promise.

The false friend is the plain monotonic stack. Those problems pop on every smaller newcomer to find a nearest smaller neighbour, and nothing is promised about what remains, so using the plain pop here would remove characters that the contract forces you to keep. Another false friend is picking the smallest digits by sorting, which breaks the reading order and so produces an invalid subsequence.

In Java, compare characters with the strict `>` so equal ones stay, strip leading zeros only after all pops, return "0" for an empty result, and use a `StringBuilder` or an array as the stack to avoid quadratic string copying.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove K Digits (LeetCode 402)
<!-- id: gc-remove-k-digits -->

**Prerequisites.** The monotonic-stack chapter (Chapter 12); the exchange lesson of this chapter.

**Problem.** Given a string of digits `num` and an integer `k`, remove exactly `k` digits so that the number that remains is as small as possible, keeping the order of the other digits. Return the result without leading zeros, and return "0" if nothing remains.

**Constraints.** 0 <= k <= num.length() <= 100000 and `num` has only the characters `0` to `9`.

**Example 1.** Input `num = "52913"`, `k = 2`, output `"213"`.

**Example 2.** Input `num = "1002003"`, `k = 2`, output `"3"`, since the leading zeros vanish after the removals.

**Hint.** What is true of a digit that stands before a smaller digit? What should be removed if the budget outlasts the digits?

**Changed decision.** First rung: a larger digit is popped only while the removal budget lasts.

#### [Vary] Remove Duplicate Letters (LeetCode 316)
<!-- id: gc-remove-duplicate-letters -->

**Prerequisites.** The digit-removal exercise above.

**Problem.** Given a string of lowercase letters, remove duplicates so that each letter appears exactly once and the result is the smallest in dictionary order among all such subsequences.

**Constraints.** 0 <= s.length() <= 100000 and `s` has only the letters `a` to `z`.

**Example 1.** Input `s = "dcbadbcd"`, output `"abcd"`.

**Example 2.** Input `s = "baab"`, output `"ab"`.

**Hint.** When is it safe to pop the top letter? What do you do when the incoming letter is already on the stack?

**Changed decision.** The budget is replaced by a promise that the popped letter returns later.

#### [Boundary] Smallest Subsequence of Distinct Characters (LeetCode 1081)
<!-- id: gc-distinct-by-rank -->

**Prerequisites.** The two exercises above.

**Problem.** The string `s` has printable ASCII characters, and the string `order` lists every character that appears in `s` from smallest to largest. Among the subsequences of `s` that contain each distinct character exactly once, return the one that is smallest when compared position by position using the order in `order`, where a character earlier in `order` is smaller.

**Constraints.** 0 <= s.length() <= 100000, every character of `s` has code from 33 to 126, and `order` has no repeated character and contains every character of `s`, and may contain others.

**Example 1.** Input `s = "bacab"`, `order = "cba"`, output `"cab"`.

**Example 2.** Input `s = "bacab"`, `order = "abc"`, output `"acb"`.

**Hint.** What changes in the pop test when characters are compared by rank rather than by code? Which of uniqueness, later availability and the leading position are checked at each step?

**Changed decision.** Comparison goes through a rank table, so uniqueness, future availability and the first-position rule must all hold together on a 128-entry alphabet.

#### [Recognize] Find the Most Competitive Subsequence (LeetCode 1673)
<!-- id: gc-competitive-subsequence -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums` and a number `k`, return the subsequence of length `k` that is the most competitive: at the first position where two subsequences of length `k` differ, the one with the smaller number is more competitive.

**Constraints.** 1 <= k <= nums.length <= 100000 and 0 <= nums[i] <= 1000000000.

**Example 1.** Input `nums = [6, 4, 9, 5, 3, 8, 7]`, `k = 3`, output `[3, 8, 7]`.

**Example 2.** Input `nums = [2, 2, 2]`, `k = 2`, output `[2, 2]`, since equal values are never popped.

**Hint.** How many elements must still be read for the stack to be able to reach length `k`? Which test uses that number?

**Changed decision.** The budget is the remaining-length requirement, so a pop is allowed only while enough numbers remain to refill the stack.
