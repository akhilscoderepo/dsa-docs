<!-- lesson-kind: combination -->
<!-- lesson-id: drop-with-stack -->
## Drop Earlier Items With A Stack

<!-- stage: context -->
### Why A Report Tool Keeps Large Digits

A report tool shortens a numeric invoice reference. The tool may delete at most `k` digits, and the remaining digits keep their order. The shorter reference should be as small as possible, because the report sorts by that number.

One idea is to delete the largest digits. On the reference `1432219` with `k = 3`, that idea deletes the 9, the 4 and the 3 and leaves `1221`. A better deletion leaves `1219`. This lesson asks which digits to delete when the program reads left to right and cannot see the rest at the moment it decides.

<!-- stage: contributions -->
### What The Proof And Stack Add

The greedy proof says when a deletion is safe. A digit is worth deleting when the digit after it is smaller. Deleting it moves a smaller digit into that position, and an earlier position outweighs every later position in the value of a number. The proof also says the deletion is allowed only while deletions remain.

The monotonic stack from Chapter 12 supplies the nearest earlier digit and keeps the survivors in order. It pops while the top is larger than the new item. Used alone, it has no limit on pops and no required length for the result. Here the proof adds a counter of deletions left and a final length, and the stack supplies the cheap access to the nearest worse digit. The pairing works because the proof decides when to pop and the stack decides which item.

<!-- stage: naive -->
### Deleting The Largest Digit Repeatedly

The direct plan scans the whole reference and deletes the largest digit, and it repeats this `k` times. When two digits are equal, it deletes the first of them. The plan treats a big digit as the worst digit to keep.

```java
static String deleteLargest(String num, int k) {
    StringBuilder sb = new StringBuilder(num);
    for (int round = 0; round < k && sb.length() > 0; round++) {
        int at = 0;
        for (int i = 1; i < sb.length(); i++) {
            if (sb.charAt(i) > sb.charAt(at)) at = i;     // first largest digit
        }
        sb.deleteCharAt(at);
    }
    return sb.length() == 0 ? "0" : sb.toString();
}
```

```predict
Run the method on `"1432219"` with `k = 3`. What does it return, and what is the smallest reference that three deletions can produce?

It returns `1221`. The deletions remove 9, then 4, then 3. The smallest result is `1219`, which deletes 4, 3 and 2. The digit 9 sits last, so removing it changes the least significant position, while removing 4 changes the second position.
```

<!-- stage: bottleneck -->
### Counting The Choices Of Digits

The method costs O(k * n) time, because each round scans the whole string. The cost is moderate. The answer is wrong, because the size of a digit is not what matters. Its place in the number matters.

Checking every choice of `k` digits to delete takes O(C(n, k) * n) time and is far too slow. The program needs a rule that looks at each digit once. The rule must compare a digit with its left neighbor, because the left neighbor decides which position the smaller digit takes.

<!-- stage: insight -->
### Deleting A Digit Before A Smaller One

#### The Left-To-Right Comparison

Read the digits from left to right and keep the survivors in a stack. When the new digit is smaller than the top, the top is worse than its right neighbor. Deleting the top moves the new digit into the position of the top, so the number gets smaller at that position, and no change at a later position can undo it.

#### Deleting While The Budget Lasts

The **removal budget** is the count `k` of deletions left. The rule is a **safe pop**. The program pops the top while the budget is positive and the top is larger than the new digit. Each pop spends one deletion. After the pops, the program pushes the new digit.

Safety follows from an exchange argument. Take a best answer that keeps the larger top `t` while deleting some digit later than the new digit `d`. Delete `t` instead, and keep that later digit. The result is no larger, because the digit `d` takes the position of `t` with a smaller value, and the earlier position wins. A best answer therefore pops every larger top while the budget lasts.

#### Finishing The Budget

If the digits end while the budget is positive, the stack is non-decreasing from bottom to top. The largest digits sit at the top, so the program deletes the last `k` digits of the stack. Leading zeros do not belong in the value, so the program strips them and returns `0` for an empty result. The structure that holds the survivors is the **kept stack**.

<!-- names: removal budget, safe pop, kept stack -->

<!-- stage: variables -->
### State For The Pop Loop

The loop keeps one stack and one counter. Four items describe the state.

- **stack** holds the surviving digits in order, and its top is the last survivor.
- **k** is the number of deletions left, and it never drops below zero.
- **d** is the digit under test.
- **result** is the stack read from bottom to top, after the last `k` digits and the leading zeros are removed.

A digit equal to the top does not pop it, because deleting an equal digit does not make the number smaller at that position.

<!-- stage: trace -->
### Two Reads With Pops

#### Deleting Three Digits

The first trace reads `1432219` with `k = 3`. The pointer `i` marks the digit under test.

The digit 1 goes on the stack. The digit 4 goes on top of 1. The digit 3 is smaller than 4, so the loop pops 4 and spends one deletion. The digit 2 pops 3, and the next digit 2 does not pop an equal 2. The digit 1 pops 2, which spends the last deletion. The digit 9 goes on the stack, and the result is `1219`.

```trace
{"cells":["1","4","3","2","2","1","9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"1","k":3},"note":"The digit 1 is read. No larger top is available or the budget is spent, so nothing is popped."},{"at":{"i":1},"vars":{"stack":"14","k":3},"note":"The digit 4 is read. No larger top is available or the budget is spent, so nothing is popped."},{"at":{"i":2},"vars":{"stack":"13","k":2},"note":"The digit 3 is read. The top 4 is larger, so the loop pops it and spends a deletion."},{"at":{"i":3},"vars":{"stack":"12","k":1},"note":"The digit 2 is read. The top 3 is larger, so the loop pops it and spends a deletion."},{"at":{"i":4},"vars":{"stack":"122","k":1},"note":"The digit 2 is read. No larger top is available or the budget is spent, so nothing is popped."},{"at":{"i":5},"vars":{"stack":"121","k":0},"note":"The digit 1 is read. The top 2 is larger, so the loop pops it and spends a deletion."},{"at":{"i":6},"vars":{"stack":"1219","k":0},"note":"The digit 9 is read. No larger top is available or the budget is spent, so nothing is popped."}]}
```

#### Keeping One Copy Of Each Letter

A second problem keeps each distinct letter once and wants the smallest string. The rule changes in one way. A letter may pop a larger top only when that top appears again later, because the string must still contain it. The trace reads `cbacdcbc`.

```trace
{"cells":["c","b","a","c","d","c","b","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"c"},"note":"The letter c is new."},{"at":{"i":1},"vars":{"stack":"b"},"note":"The letter b is new. The top c is larger and appears later, so the loop pops it."},{"at":{"i":2},"vars":{"stack":"a"},"note":"The letter a is new. The top b is larger and appears later, so the loop pops it."},{"at":{"i":3},"vars":{"stack":"ac"},"note":"The letter c is new."},{"at":{"i":4},"vars":{"stack":"acd"},"note":"The letter d is new."},{"at":{"i":5},"vars":{"stack":"acd"},"note":"The letter c is already on the stack, so the loop skips it."},{"at":{"i":6},"vars":{"stack":"acdb"},"note":"The letter b is new."},{"at":{"i":7},"vars":{"stack":"acdb"},"note":"The letter c is already on the stack, so the loop skips it."}]}
```

<!-- stage: code -->
### Popping Larger Digits Within The Budget

```java
static String smallestAfterRemoving(String num, int k) {
    StringBuilder stack = new StringBuilder();
    for (int i = 0; i < num.length(); i++) {
        char d = num.charAt(i);
        while (k > 0 && stack.length() > 0 && stack.charAt(stack.length() - 1) > d) {
            stack.deleteCharAt(stack.length() - 1);      // safe pop: spend one deletion
            k--;
        }
        stack.append(d);
    }
    stack.setLength(stack.length() - Math.min(k, stack.length()));   // leftover budget removes the tail
    int start = 0;
    while (start < stack.length() - 1 && stack.charAt(start) == '0') start++;   // strip leading zeros
    return stack.length() == 0 ? "0" : stack.substring(start);
}
```

The string builder serves as the stack, and the pop condition compares characters, which order the same way as digits. The condition `k > 0` is the budget check. The final `setLength` handles the digits that were never popped.

- **Time** is O(n), because each digit is pushed once and popped at most once.
- **Space** is O(n) for the stack.

<!-- stage: applicability -->
### When A Stack Carries The Deletion

#### Applying The Invariant

Use this pairing when you must delete at most `k` items, or must keep exactly `k` items, from a sequence while the order of the survivors stays. The invariant is that after each item, the stack holds the best survivors of the prefix that the budget allows. State the pop condition, the budget, and the required final length before you code.

#### Finding Cases That Break The Precondition

A false friend is the plain monotonic stack, which pops without a budget and ignores the final length. A second false friend is deleting the largest items first. The largest item can sit in the least significant place, and the order of positions decides the value.

#### Avoiding Java Pitfalls

Compare `char` digits directly, because `'0'` to `'9'` order as their values. Strip leading zeros after the loop, and return `"0"` for an empty result. Use `StringBuilder` and never `String +=` inside the loop, because each concatenation copies the whole string.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove K Digits (LeetCode 402)
<!-- id: gr-remove-k-digits -->

**Prerequisites.** The safe pop and the removal budget of this lesson.

**Problem.** String `num` holds decimal digits and has no leading zero unless it is the single digit `0`. Delete exactly `min(k, num.length())` digits so that the remaining digits keep their order and form the smallest possible number. Return the number as a string without leading zeros. Return `"0"` when no digits remain.

**Constraints.** The limits are:
- **Length** is `0 <= num.length() <= 10^5`.
- **Digits** are characters `'0'` to `'9'`.
- **Budget** is `0 <= k <= 10^5`, and it may exceed the length.
- **Return** is `"0"` for an empty result.

**Example 1.** Input `num = "1432219"` and `k = 3`, output `"1219"`.

**Example 2.** Input `num = "10200"` and `k = 1`, output `"200"`.

**Hint.** What happens to the budget when no digit is followed by a smaller one?

**Changed decision.** The deletion count is exact, and the answer is a number.

#### [Vary] Remove Duplicate Letters (LeetCode 316)
<!-- id: gr-remove-duplicate-letters -->

**Prerequisites.** The previous exercise.

**Problem.** String `s` holds lowercase letters. Return the lexicographically smallest subsequence of `s` that contains every distinct letter of `s` exactly once. A subsequence keeps the order of the letters that it takes.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^4`.
- **Characters** are lowercase English letters.
- **Result** has one copy of each distinct letter.
- **Empty** input returns the empty string.

**Example 1.** Input `s = "cbacdcbc"`, output `"acdb"`.

**Example 2.** Input `s = "bcabc"`, output `"abc"`.

**Hint.** When may the loop pop a larger letter without losing it?

**Changed decision.** A pop needs the top letter to appear again later, and no counter is used.

#### [Boundary] Smallest Subsequence of Distinct Characters (LeetCode 1081)
<!-- id: gr-distinct-subsequence-positions -->

**Prerequisites.** The previous exercise.

**Problem.** String `s` holds lowercase letters. Among the subsequences that contain every distinct letter exactly once, choose the lexicographically smallest string. If several position sets give that string, choose the set whose positions are lexicographically smallest. Return the positions of the chosen letters in increasing order.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^4`.
- **Characters** are lowercase English letters.
- **Positions** start at 0.
- **Empty** input returns an empty array.

**Example 1.** Input `s = "baab"`, output `[1,3]`.

**Example 2.** Input `s = "abab"`, output `[0,1]`.

**Hint.** Which copy of a repeated letter should the loop keep when it has a choice?

**Changed decision.** The method returns positions, and a tie rule picks among equal strings.

#### [Recognize] Find the Most Competitive Subsequence (LeetCode 1673)
<!-- id: gr-most-competitive-subsequence -->

**Prerequisites.** The removal budget of this lesson.

**Problem.** Array `nums` holds integers, and `k` is at most its length. Return the subsequence of length exactly `k` that is smallest when compared position by position from the left. A subsequence keeps the order of the elements that it takes.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are integers in `0 <= nums[i] <= 10^9`.
- **Size** is `1 <= k <= nums.length`.
- **Mutation** does not occur.

**Example 1.** Input `nums = [3,5,2,6]` and `k = 2`, output `[2,6]`.

**Example 2.** Input `nums = [4,7,5,9,6,8]` and `k = 3`, output `[4,5,6]`.

**Hint.** How many elements may still be dropped before the stack cannot reach length `k`?

**Changed decision.** The final length is fixed, so the budget comes from the length.
