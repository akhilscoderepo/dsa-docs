<!-- lesson-kind: standard -->
<!-- lesson-id: partition-generation -->
## Cut A String Into Pieces

<!-- stage: context -->
### Why The Expected Output Drops Letters

A parser test needs every way to cut the record `abc` into consecutive fields. The developer reuses the subset search on the characters. The expected-output file then holds `ac`, a list that skips the letter `b`. No parser can read that list as fields of the record, because the fields must add up to the whole record.

A cut keeps every letter and keeps the order of the letters. The only freedom is where one field ends and the next begins. This lesson asks how a search lists exactly these cuts, and how it avoids testing cuts that already break a rule on their first field.

<!-- stage: naive -->
### Trying Every Set Of Cut Positions

The direct plan marks each gap between two neighbouring letters as cut or not cut. It loops over all masks of the gaps, builds the fields and tests every field against the rule at the end.

```java
static List<List<String>> cutAll(String s, java.util.function.Predicate<String> ok) {
    List<List<String>> out = new ArrayList<>();
    int gaps = Math.max(s.length() - 1, 0);
    for (int mask = 0; mask < (1 << gaps); mask++) {            // one bit for each gap
        List<String> fields = new ArrayList<>();
        int from = 0;
        for (int g = 0; g < gaps; g++)
            if ((mask >> g & 1) == 1) { fields.add(s.substring(from, g + 1)); from = g + 1; }   // a set bit cuts here
        if (!s.isEmpty()) fields.add(s.substring(from));                                          // the last field
        if (fields.stream().allMatch(ok)) out.add(fields);                                         // test every field at the end
    }
    return out;
}
```

The method lists every valid cut, because every cut corresponds to one mask. It builds and tests all masks, valid or not.

<!-- stage: bottleneck -->
### Counting Cuts With A Bad First Field

```predict
The record has 20 different letters, and a field is valid only when it reads the same forward and backward. How many masks does the plan test, and how many valid cuts exist?

The plan tests 2^19 = 524,288 masks, because 20 letters have 19 gaps. Only the cut into 20 single letters has valid fields, since no longer field reads the same in both directions. So one valid cut exists. A search that tests each field when it begins makes 21 calls and 210 field tests.
```

The plan costs O(n * 2^n) time because every mask pays for building and testing all of its fields. The first field of most masks already fails the rule, and the plan discovers that only after it has built the remaining fields.

A search can fix the first field first and test it at once. A failed first field removes every cut that begins with it. Only the suffix after a valid field still needs a cut, and that suffix is a smaller copy of the same task.

<!-- stage: insight -->
### Choosing The End Of The Next Field

#### Tracking The First Uncut Letter

The **start position** is the index of the first letter that no chosen field covers yet. The root call has start position 0. Letters before it belong to fields on the path, and letters from it onward form the suffix that the call must cut. The call owns that suffix and nothing else.

#### Choosing Where The Field Ends

The **piece end** is the index one past the last letter of the next field. A call loops over every piece end from `start + 1` to the string length. For each piece end, the field is the text from the start position up to the piece end. If the field passes the rule, the call adds it to the path and calls itself with the piece end as the new start position.

#### Finishing On An Empty Suffix

The **empty suffix** occurs when the start position equals the string length. No letter is left, so the fields on the path cover the whole string, and the call stores a copy. A call with a smaller start position may not store anything, because letters would be missing. The invariant is that fields on the path cover exactly the letters before the start position, with none skipped and none repeated.

<!-- names: start position, piece end, empty suffix -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Start position** is the number of letters that the path covers.
- **Piece end** is the loop variable, with `start < end <= n`.
- **Path** is the shared list of the fields chosen so far.
- **Rule** is the test that a field must pass before the call uses it.

A valid field moves the start position to the piece end. The search stores a copy of the path only when the start position equals the length `n`.

<!-- stage: trace -->
### Following The Start Position Through A Word

#### Cutting Three Letters Into Palindromes

The first trace cuts `aba` into fields that read the same in both directions. The pointer `start` marks the start position, and the pointer `end` marks the piece end that the loop tests. The variable `path` shows the path after the step, and `stored` counts the finished cuts.

The call at start 0 tests the piece end 1, and the field `a` passes. The call at start 1 tests `b` and passes, and the call at start 2 tests `a`, passes and reaches start 3, which is the empty suffix. It stores `a, b, a`. Back at start 1, the field `ba` fails, and back at start 0, the field `ab` fails. The field `aba` passes and reaches start 3, so the search stores `aba` as the second cut.

#### Seeing A Subset Skip A Letter

The second trace runs the subset search on the letters of `abc`. It includes `a`, excludes `b` and includes `c`, so it stores `a, c`. The path covers two of three positions, and the letter at position 1 appears in no field. A cut has no such step.

#### Stepping Through Both Runs

```trace
{"cells":["a","b","a"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":1},"vars":{"path":"a","stored":0},"note":"The call at start 0 tests the piece end 1. The field a passes, so the path becomes [a]."},{"at":{"start":1,"end":2},"vars":{"path":"a,b","stored":0},"note":"The call at start 1 tests the piece end 2. The field b passes, so the path becomes [a,b]."},{"at":{"start":2,"end":3},"vars":{"path":"a,b,a","stored":1},"note":"The call at start 2 tests the piece end 3. The field a passes, so the path becomes [a,b,a]. The new start position equals the length, which is the empty suffix, so the search stores a copy."},{"at":{"start":1,"end":3},"vars":{"path":"a","stored":1},"note":"The field ba does not read the same in both directions, so the call skips this piece end."},{"at":{"start":0,"end":2},"vars":{"path":"empty","stored":1},"note":"The field ab does not read the same in both directions, so the call skips this piece end."},{"at":{"start":0,"end":3},"vars":{"path":"aba","stored":2},"note":"The call at start 0 tests the piece end 3. The field aba passes, so the path becomes [aba]. The new start position equals the length, which is the empty suffix, so the search stores a copy."}]}
```

```trace
{"cells":["a","b","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"kept":"a","covered":1},"note":"The subset search includes a, so the path holds the letter a."},{"at":{"i":1},"vars":{"kept":"a","covered":1},"note":"The search excludes b, so no field covers the letter at position 1."},{"at":{"i":2},"vars":{"kept":"ac","covered":2},"note":"The search includes c and stores the list a, c. Only 2 of 3 positions are covered, so it is not a cut."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Cuts With A Field Rule

The method tests a field with indices before it creates a string. It builds the field text only after the field passes.

```java
static void go(int start, String s, List<String> path, List<List<String>> out) {
    if (start == s.length()) {                          // the empty suffix: the path covers every letter
        out.add(new ArrayList<>(path));                 // store a copy of the fields
        return;
    }
    for (int end = start + 1; end <= s.length(); end++) {   // every possible end of the next field
        if (!isPalindrome(s, start, end - 1)) continue;     // the rule fails, so the whole branch is skipped
        path.add(s.substring(start, end));              // choose: the field covers start up to end - 1
        go(end, s, path, out);                          // the suffix starts at end
        path.remove(path.size() - 1);                   // undo the choice
    }
}

static boolean isPalindrome(String s, int lo, int hi) {
    while (lo < hi) if (s.charAt(lo++) != s.charAt(hi--)) return false;   // compare the two ends
    return true;                                        // a field of one letter always passes
}
```

#### Using The End Index Of Substring

The call `s.substring(start, end)` includes the index `start` and excludes the index `end`. For `end == start`, it returns the empty string, which the loop never requests because `end` begins at `start + 1`.

#### Cost Of The Search

A string of `n` letters has 2^(n-1) cuts in the worst case, so the output alone costs O(n * 2^n). Each field test costs up to O(n). A strict rule makes the search visit only a small part of the cuts. The stack uses O(n) memory.

<!-- stage: applicability -->
### Recognizing A Cut Problem

#### Spotting The Pattern

The cue is an output that splits a whole sequence into consecutive valid parts. The invariant is that the path covers exactly the letters before the start position, and each call owns the suffix from that position.

#### Finding The False Friend

The false friend is the subset search. It may skip letters, so it lists `ac` for `abc`. A second false friend is a store at any start position, which writes partial cuts into the output. The store belongs to the empty suffix only.

#### Recognizing The No-Go Cases

The search does not fit when the question asks for the number of cuts or for the best cut. A table over start positions answers those questions without listing cuts. It does not fit when fields may overlap or leave gaps. A string of 25 letters with a rule that almost always passes gives millions of cuts.

<!-- stage: exercises -->
### Exercises

#### [Build] All Splits Of A Short String (Author exercise)
<!-- id: bt-all-splits-short-string -->

**Prerequisites.** The start position, the piece end and the empty suffix of this lesson.

**Problem.** The string `s` has at most five lowercase letters. Return every way to cut `s` into non-empty consecutive fields, so that the fields joined in order give `s`. The search chooses the piece end from the smallest to the largest at each call, and the result keeps that order. The empty string has one cut, the cut with no fields.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 5`.
- **Characters** are lowercase English letters.
- **Count** of cuts is `2^(n-1)` for `n >= 1`, and 1 for `n = 0`.
- **Fields** are never empty.

**Example 1.** Input `s = "abc"`, output `[["a","b","c"],["a","bc"],["ab","c"],["abc"]]`.

**Example 2.** Input `s = ""`, output `[[]]`.

**Hint.** What does the first call do for a piece end equal to the string length? How many letters does the path cover when the call stores a cut?

**Changed decision.** Every piece end is a choice, and the call stores a cut only at the empty suffix.

#### [Vary] Valid-Piece Predicate (Author exercise)
<!-- id: bt-valid-piece-predicate -->

**Prerequisites.** The previous exercise.

**Problem.** The string `s` holds decimal digits, and `limit` is a positive integer. Return every cut of `s` into non-empty fields where each field is a number without a leading zero and with a value of at most `limit`. The field `0` is allowed, and the field `05` is not. The search tries the smallest piece end first, and the result keeps that order.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 12`.
- **Characters** are the digits `0` to `9`.
- **Limit** is `1 <= limit <= 10^6`.
- **Values** of fields fit in a `long`.

**Example 1.** Input `s = "100"`, `limit = 255`, output `[["1","0","0"],["10","0"],["100"]]`.

**Example 2.** Input `s = "909"`, `limit = 90`, output `[["9","0","9"],["90","9"]]`.

**Hint.** Which fields may a call try after the digit `0` begins a field? Once a field exceeds `limit`, do longer fields from the same start stay valid?

**Changed decision.** The call tests a field before it recurses, and a field above `limit` ends the loop for that start.

#### [Boundary] Empty Suffix Completion (Author exercise)
<!-- id: bt-empty-suffix-completion -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s` and an integer `parts`, return every cut of `s` into exactly `parts` non-empty consecutive fields. The search stores a cut only when the path holds `parts` fields and no letter remains. A path with `parts` fields and a remaining suffix is not a result. The result follows the same order of piece ends.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10`.
- **Characters** are lowercase English letters.
- **Parts** is `0 <= parts <= 12`, and `parts` may exceed the length.
- **Empty result** is an empty list when no cut matches.

**Example 1.** Input `s = "abcd"`, `parts = 2`, output `[["a","bcd"],["ab","cd"],["abc","d"]]`.

**Example 2.** Input `s = ""`, `parts = 0`, output `[[]]`.

**Hint.** What is the start position when the path holds `parts` fields but letters remain? When must the loop stop adding fields?

**Changed decision.** Two conditions guard the store: the start position equals the length and the field count equals `parts`.

#### [Recognize] Palindrome Partitioning (LeetCode 131)
<!-- id: bt-palindrome-partitioning -->

**Prerequisites.** The previous three exercises.

**Problem.** Given a lowercase string `s`, return every cut of `s` into non-empty fields where each field reads the same forward and backward. A field of one letter qualifies. Fields are tried from shortest to longest, and the result keeps that order.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 14`.
- **Characters** are lowercase English letters.
- **Fields** are never empty.
- **Mutation** does not occur; the result holds new lists.

**Example 1.** Input `s = "abba"`, output `[["a","b","b","a"],["a","bb","a"],["abba"]]`.

**Example 2.** Input `s = "ab"`, output `[["a","b"]]`.

**Hint.** What does the rule test for the field from `start` to `end - 1`? Which cut always exists, whatever the letters are?

**Changed decision.** The rule is a palindrome test on two indices. The test runs before the call copies the field.
