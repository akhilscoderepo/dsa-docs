# Chapter 03: Strings

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| indexing/scans | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| immutable-result construction and `StringBuilder` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| parsing/validation state machines | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| normalization | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| fixed-alphabet counting | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| run-length construction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| center-expansion palindromes | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Push prior partial state | Need nested parsing | Nested context is LIFO | https://leetcode.com/problems/decode-string/ | Core |
| Two pointers from center | Need palindrome substring | Every palindrome has a center (or gap) | https://leetcode.com/problems/longest-palindromic-substring/ | Core |
| Shared prefix path | Need many prefix operations | Shared prefixes are represented once | https://leetcode.com/problems/implement-trie-prefix-tree/ | Core |
| Reuse matched prefix after mismatch | Need substring search efficiently | A matched prefix is also a suffix, so previous work can be reused | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ | Advanced |
| Reuse previous match interval | Need longest prefix/suffix information for repeated patterns | Previously matched interval provides reusable information | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ | Advanced |


### Released Combination Ladders

No combination is released by this chapter's current prerequisite boundary. The visible deferred entries below remain ownership notes, not premature exercises.


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

Strings are indexed sequences with immutable values in Java. This chapter stays with string-local state: it does not borrow maps, two pointers, or windows before those chapters release them.

### Indexed Scans

**Recognition cue.** Each character can be inspected independently or folded into a small running answer. **State.** `i` is the next unexamined index. **False friend.** A reversed or paired comparison needs two pointers, not one scan.

- **Build - Author exercise: Count Digits.** Given `s`, return how many characters are decimal digits. `"a1b2" -> 2`; `"" -> 0`.
- **Vary - LC 58 Length of Last Word.** Scan characters while defining exactly when a word begins and ends.
- **Boundary - Author exercise: First Delimiter.** Return the first index of `':'`, or `-1`; test `":x"` and `"abc"`.
- **Recognize - LC 709 To Lower Case.** Each output character depends only on its input character.

### Safe Construction

**Recognition cue.** The output is built incrementally. **State.** A `StringBuilder` contains exactly the completed output prefix. **Java hazard.** Repeated `+` in a loop creates repeated immutable strings. **False friend.** Do not use `StringBuilder.insert(0, ...)` for reversal; it turns linear work quadratic.

- **Build - Author exercise: Remove Spaces.** Return `s` without spaces using a `StringBuilder`.
- **Vary - LC 151 Reverse Words in a String.** Build the final words with explicit separator ownership.
- **Boundary - Author exercise: Empty Result.** `"   " -> ""`; never leave a trailing separator.
- **Recognize - LC 6 Zigzag Conversion.** Builders own the independently constructed rows.

### Parsing State

**Recognition cue.** Characters change a small parser state: digit, sign, decimal point, token boundary, or error. **State.** State variables record what has already been legally consumed. **False friend.** Nested scopes require a stack and arrive in Chapter 11.

- **Build - Author exercise: Parse a Signed Integer Token.** Consume an optional sign followed by one or more digits, and reject the token if any other character appears.
- **Vary - LC 8 String to Integer (atoi).** Consume optional sign and digits under explicit overflow rules.
- **Boundary - LC 65 Valid Number.** A decimal point and exponent each have placement rules; test `"."` and `"2e10"`.
- **Recognize - LC 165 Compare Version Numbers.** Parse components without converting an unbounded version to one integer.

### Normalization

**Recognition cue.** Equivalent inputs differ only by case, separators, or a stated canonical representation. **State.** The normalized representation preserves the equality contract. **False friend.** Sorting as a canonical signature is released only after Chapter 05.

- **Build - Author exercise: Lowercase Letters Only.** Return lowercase alphabetic characters from `s`.
- **Vary - LC 520 Detect Capital.** Normalize the allowed capitalization forms before deciding validity.
- **Boundary - Author exercise: Punctuation Only.** `"?!" -> ""`; make the empty normalized result legal.
- **Recognize - LC 482 License Key Formatting.** Normalize case and regroup from a clear output contract.

### Fixed Alphabet Counts

**Recognition cue.** The character set is explicitly small, such as lowercase English letters. **State.** `count[c - 'a']` is the processed count. **False friend.** General characters or words require Chapter 04 maps.

- **Build - Author exercise: Vowel Counts.** Count lowercase vowels in `s`.
- **Vary - LC 389 Find the Difference.** Increment characters from one string and decrement from the other.
- **Boundary - Author exercise: Invalid Alphabet.** Reject or document any character outside the declared alphabet.
- **Recognize - LC 383 Ransom Note.** Count the available lowercase letters in `magazine`, consume them while scanning `ransomNote`, and fail as soon as a required count becomes negative.

### Run Construction

**Recognition cue.** Equal adjacent characters form one completed run. **State.** The current character and run length describe the suffix not yet emitted. **False friend.** Arbitrary duplicate grouping needs a map or sort.

- **Build - LC 443 String Compression.** Compress adjacent runs in place.
- **Vary - LC 38 Count and Say.** Read one run and construct the next string.
- **Boundary - Author exercise: Final Run.** Ensure `"aaab"` emits both `3a` and `1b`.
- **Recognize - Author exercise: Run-Length Encoding.** Convert a string such as `"aaabbc"` to `"3a2b1c"` by emitting each maximal run exactly once.

### Center Expansion

**Recognition cue.** A substring is defined by symmetry around one character or one gap. **State.** `left` and `right` expand only while characters match; the center remains fixed for one attempt. **False friend.** This is not opposite-end validation of the whole string.

- **Build - LC 647 Palindromic Substrings.** Expand around every odd and even center.
- **Vary - LC 5 Longest Palindromic Substring.** Preserve the best interval rather than only a count.
- **Boundary - Author exercise: Even Center.** `"abba"` must discover a palindrome centered between the middle characters.
- **Recognize - Author exercise: Longest Even-Length Palindrome.** Return the longest palindromic substring whose center lies between two characters, using the same expansion invariant with different initial boundaries.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `StringBuilder` or `char[]` for repeated construction; do not concatenate immutable strings in a hot loop.
- Track indices and slice once when substring creation would occur repeatedly.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Deferred | Strings + Hash Maps | Chapter 04 supplies arbitrary-key state |
| Deferred | Strings + Two Pointers | Chapter 08 supplies opposite-end movement |
| Deferred | Strings + Sliding Window | Chapter 09 supplies moving-window state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** opposite-end palindrome checks, sliding window, hash/sort grouping.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

