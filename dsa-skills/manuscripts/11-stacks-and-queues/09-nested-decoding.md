<!-- lesson-kind: standard -->
<!-- lesson-id: nested-decoding -->
## Decode Nested Repeat Groups

<!-- stage: context -->
### A Decoder That Breaks On Depth

A configuration file stores long repeated text in a short form. The text `3[ab]` stands for `ababab`, so the number before the brackets says how many times the text inside the brackets appears. A first decoder passes every test that the team wrote. It reads a digit, remembers it, and repeats the letters that follow.

Then a file contains `2[x3[yz]w]`. The decoder prints the wrong text, and for the entry `12[a]` it repeats the letter only twice. The bracketed text of one entry contains another entry, and the number can have more than one digit. The lesson answers one question. When a group can sit inside another group, how does a single left-to-right pass know which text each number repeats?

<!-- stage: naive -->
### Expand The Innermost Group Again And Again

The direct method looks for a group that contains no other group. The first `]` in the text always ends such a group, because no `]` comes before it. The nearest `[` to its left starts the group, and the digits just before that `[` give the number. The method replaces the whole entry by the repeated body and starts over. It stops when the text has no `]`.

```java
static String decodeByRewriting(String s) {
    while (true) {
        int close = s.indexOf(']');
        if (close < 0) return s;
        int open = s.lastIndexOf('[', close);
        int start = open;
        while (start > 0 && s.charAt(start - 1) >= '0' && s.charAt(start - 1) <= '9') start--;
        int times = Integer.parseInt(s.substring(start, open));
        String body = s.substring(open + 1, close);
        s = s.substring(0, start) + body.repeat(times) + s.substring(close + 1);
    }
}
```

The method is correct. For `2[x3[yz]w]` the first pass rewrites `3[yz]` to `yzyzyz`, and the second pass rewrites the remaining entry.

<!-- stage: bottleneck -->
### Every Rewrite Copies The Whole Text

```predict
A file holds 50,000 groups nested inside each other, each with the number 1, around the single letter x. The text is 50,000 copies of `1[`, then `x`, then 50,000 copies of `]`. About how many characters do the rewritten strings contain in total?

About 3.75 billion. The method makes 50,000 passes. Each pass builds a new string that is only 3 characters shorter than the one before, so the lengths add up to about 3 * 50,000^2 / 2.
```

Every pass builds a complete new string, even though it changes only one entry. With `d` levels of nesting the method makes at least `d` passes. The strings it builds have a length of about `n` each, so a deep input costs O(n * d), and a chain that is as deep as it is long costs O(n^2). A group with a large number also gets copied into every later string until the pass that expands its enclosing group.

The search is the repeated work. Pass after pass, the method reads past the same finished letters to find the next `]`. The scan already walked over every one of those characters. A method that keeps the unfinished entries while it reads can complete each group at the moment its `]` arrives.

<!-- stage: insight -->
### Keep The Text Outside The Open Group

At any index, some groups are open, which means their `[` was read and their `]` was not. The innermost open group is the one that the next `]` will close. The decoder needs the text of that group so far, plus whatever is needed to continue after it closes.

<!-- names: parent, frame, resolve -->

#### Each Group Has A Parent

The **parent** of a group is the group that directly contains it. The text outside every group is the top level, and the top level has no parent. When `[` is read, the text built so far belongs to the parent of the new group. The decoder must set that text aside, because the new group starts with empty text.

#### A Frame Holds What A Group Needs Later

A **frame** is a pair that the decoder saves on a stack when it reads `[`. The pair holds the parent text built so far and the number that the new group repeats. The top frame always belongs to the innermost open group. A frame stays on the stack until the matching `]` arrives, so a group at depth `d` has `d` frames below the current text.

#### Resolve At The Bracket, Not At The Digit

To **resolve** a group is to replace it by its repeated text. The decoder resolves a group only at its `]`, because only then the body is complete. It pops the top frame, appends the body to the parent text as many times as the frame says, and continues with the parent text as the current text. Digits only build the number: each digit changes it to `count * 10 + digit`. The number gets used at the next `[` and never earlier. The invariant is that the current text holds the decoded part of the open group nearest the cursor, and the stack holds one frame for each open group around it.

<!-- stage: variables -->
### What The Single Pass Keeps

The pass keeps three pieces of state.

- **cur** is the decoded text of the innermost open group so far, and it starts as the empty top level.
- **count** is the number formed by the digits since the last non-digit character, and it resets to 0 after each `[`.
- **stack** holds one frame per open group, and each frame stores the parent text and the number for that group.

A letter changes only `cur`. A digit changes only `count`. Each `[` pushes a frame and gives `cur` and `count` fresh values, and each `]` pops a frame and changes `cur`.

<!-- stage: trace -->
### Reading Two Encoded Texts

#### A Group Inside A Group

The first trace reads `2[x3[yz]w]`. The cells are the characters, and the pointer `i` marks the character that was just read. The vars show `cur`, `count` and the stack, where each frame is written as the parent text in quotes and the number for its group.

The first `[` saves the empty top-level text with the number 2. The second `[` saves the text `x` with the number 3. At the first `]`, the body `yz` appears three times after `x`, so `cur` becomes `xyzyzyz`. The letter `w` joins that text. The last `]` repeats it twice after the empty parent text.

```trace
{"cells":["2","[","x","3","[","y","z","]","w","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":"","count":2,"stack":"[]"},"note":"The digit 2 makes count 2."},{"at":{"i":1},"vars":{"cur":"","count":0,"stack":"[(\"\", 2)]"},"note":"[ saves the parent text \"\" with the number 2, then cur and count start fresh."},{"at":{"i":2},"vars":{"cur":"x","count":0,"stack":"[(\"\", 2)]"},"note":"The letter x joins cur."},{"at":{"i":3},"vars":{"cur":"x","count":3,"stack":"[(\"\", 2)]"},"note":"The digit 3 makes count 3."},{"at":{"i":4},"vars":{"cur":"","count":0,"stack":"[(\"\", 2), (\"x\", 3)]"},"note":"[ saves the parent text \"x\" with the number 3, then cur and count start fresh."},{"at":{"i":5},"vars":{"cur":"y","count":0,"stack":"[(\"\", 2), (\"x\", 3)]"},"note":"The letter y joins cur."},{"at":{"i":6},"vars":{"cur":"yz","count":0,"stack":"[(\"\", 2), (\"x\", 3)]"},"note":"The letter z joins cur."},{"at":{"i":7},"vars":{"cur":"xyzyzyz","count":0,"stack":"[(\"\", 2)]"},"note":"] pops the frame, so the body \"yz\" is appended 3 times after \"x\"."},{"at":{"i":8},"vars":{"cur":"xyzyzyzw","count":0,"stack":"[(\"\", 2)]"},"note":"The letter w joins cur."},{"at":{"i":9},"vars":{"cur":"xyzyzyzwxyzyzyzw","count":0,"stack":"[]"},"note":"] pops the frame, so the body \"xyzyzyzw\" is appended 2 times after \"\"."},{"at":{"i":10},"vars":{"cur":"xyzyzyzwxyzyzyzw","count":0,"stack":"[]"},"note":"The text ends with an empty stack, and cur holds the decoded text."}]}
```

#### A Number With Two Digits

The second trace reads `2[ab]10[c]`. The group `2[ab]` closes before the next group starts, so the stack is empty again. The digits `1` and `0` read in turn give `count` the values 1 and then 10. The decoder does not repeat anything after the digit `1`, because the next character could be another digit. The `[` after `10` saves the number 10 together with the finished text of the first group.

```trace
{"cells":["2","[","a","b","]","1","0","[","c","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":"","count":2,"stack":"[]"},"note":"The digit 2 makes count 2."},{"at":{"i":1},"vars":{"cur":"","count":0,"stack":"[(\"\", 2)]"},"note":"[ saves the parent text \"\" with the number 2, then cur and count start fresh."},{"at":{"i":2},"vars":{"cur":"a","count":0,"stack":"[(\"\", 2)]"},"note":"The letter a joins cur."},{"at":{"i":3},"vars":{"cur":"ab","count":0,"stack":"[(\"\", 2)]"},"note":"The letter b joins cur."},{"at":{"i":4},"vars":{"cur":"abab","count":0,"stack":"[]"},"note":"] pops the frame, so the body \"ab\" is appended 2 times after \"\"."},{"at":{"i":5},"vars":{"cur":"abab","count":1,"stack":"[]"},"note":"The digit 1 makes count 1."},{"at":{"i":6},"vars":{"cur":"abab","count":10,"stack":"[]"},"note":"The digit 0 makes count 10."},{"at":{"i":7},"vars":{"cur":"","count":0,"stack":"[(\"abab\", 10)]"},"note":"[ saves the parent text \"abab\" with the number 10, then cur and count start fresh."},{"at":{"i":8},"vars":{"cur":"c","count":0,"stack":"[(\"abab\", 10)]"},"note":"The letter c joins cur."},{"at":{"i":9},"vars":{"cur":"ababcccccccccc","count":0,"stack":"[]"},"note":"] pops the frame, so the body \"c\" is appended 10 times after \"abab\"."},{"at":{"i":10},"vars":{"cur":"ababcccccccccc","count":0,"stack":"[]"},"note":"The text ends with an empty stack, and cur holds the decoded text."}]}
```

<!-- stage: code -->
### Writing The Single Pass

#### One Method With Two Stacks

The code keeps the parent text and the number of each frame on two stacks that always have the same size. The `ArrayDeque` is the stack, and the `push` and `pop` calls work on its first position.

```java
static String decode(String s) {
    ArrayDeque<StringBuilder> parents = new ArrayDeque<>();
    ArrayDeque<Integer> repeats = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder();
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') {
            count = count * 10 + (c - '0');
        } else if (c == '[') {
            parents.push(cur);
            repeats.push(count);
            cur = new StringBuilder();
            count = 0;
        } else if (c == ']') {
            StringBuilder parent = parents.pop();
            int times = repeats.pop();
            for (int t = 0; t < times; t++) parent.append(cur);
            cur = parent;
        } else {
            cur.append(c);
        }
    }
    return cur.toString();
}
```

#### Cost Of The Pass

The pass reads each input character once. Each `]` copies the body into its parent as many times as the number says. The time is O(n + L * d) for the decoded length `L` and the nesting depth `d`, because a character is copied once for each group that encloses it. The stack holds `d` frames, so the extra space is O(d) plus the text that those frames store. The test `c >= '0' && c <= '9'` is deliberate, because `Character.isDigit` also accepts digits from other scripts.

<!-- stage: applicability -->
### Recognizing Repeat Groups In Other Problems

#### Recognize The Cue

Use saved frames when a number applies to a bracketed part of the text, and that part can contain further bracketed parts. The invariant of this lesson is that the current text belongs to the innermost open group, and each frame on the stack belongs to one open group around it. Other formats have the same shape, such as nested template blocks that repeat a section a given number of times.

#### Repeating At The Digit Is A False Friend

A decoder that repeats the next letters as soon as it reads a digit looks reasonable. It is a false friend. It works on `3[ab]`, fails on `12[a]` because the number is not complete yet, and fails on nesting because one number variable cannot hold two pending groups. A string replace that handles one level and runs once fails the same way for `2[x3[yz]w]`.

#### When Not To Build The Text

The decoded length can grow exponentially with the input length, because `9[9[9[9[a]]]]` already produces 6,561 letters. When a problem asks only for the length or for one character, keep a number per frame instead of text. The same stack works, and memory stays proportional to the depth. A format without nesting needs no stack, and one `cur` with one `count` is enough.

<!-- stage: exercises -->
### Exercises

#### [Build] Decode One Flat Group (Author exercise)
<!-- id: sq-decode-flat-group -->

**Prerequisites.** The `cur` and `count` variables of this lesson.

**Problem.** A flat group is a text of the form `d[body]`, where `d` is one decimal digit and `body` is a possibly empty sequence of lowercase letters. The decoded text is `body` written `d` times in a row. Given one flat group, return its decoded text.

**Constraints.** The limits are:
- **Form** is exactly `d[body]` with `d` from 1 to 9.
- **Body** has 0 to 100 lowercase letters.
- **Return** is a `String`, empty when `body` is empty.
- **Mutation** is not allowed; the input is read once.

**Example 1.** Input `4[xy]`, output `xyxyxyxy`.

**Example 2.** Input `5[]`, output the empty string.

**Hint.** Read the digit into `count`, skip the `[`, and append each letter to `cur`. What must happen at the `]`?

**Changed decision.** Basic case: one pass keeps `count` and `cur`, and no stack is needed.

#### [Vary] Multi-Digit Repeat Count (Author exercise)
<!-- id: sq-multi-digit-repeat -->

**Prerequisites.** The exercise above.

**Problem.** A flat group has the form `n[body]`, where `n` is a decimal number written with one or more digits and no leading zero. The decoded text is `body` written `n` times in a row. Given one such group, return its decoded text.

**Constraints.** The limits are:
- **Number** `n` is from 1 to 999.
- **Body** has 0 to 100 lowercase letters.
- **Output** has at most 100000 characters.
- **Return** is a `String`, empty when `body` is empty.

**Example 1.** Input `10[z]`, output `zzzzzzzzzz`.

**Example 2.** Input `11[mn]`, output `mnmnmnmnmnmnmnmnmnmnmn`.

**Hint.** What does the number look like after the first digit and after the second digit? Which update builds a number digit by digit?

**Changed decision.** The number can have several digits, so `count` becomes `count * 10 + digit`.

#### [Boundary] Adjacent And Nested Groups (Author exercise)
<!-- id: sq-adjacent-nested-groups -->

**Prerequisites.** The two exercises above and the frames of this lesson.

**Problem.** Decode a text that has lowercase letters and groups `d[body]` with one-digit numbers. A body can have letters and further groups. Groups can follow each other directly, and a body can be empty. The decoded text replaces each group by its body written `d` times.

**Constraints.** The limits are:
- **Length** is 0 to 200 characters, and the text is well formed.
- **Numbers** `d` are single digits from 1 to 9.
- **Output** has at most 100000 characters.
- **Return** is a `String`, empty for empty input.

**Example 1.** Input `2[a]3[b2[c]]`, output `aabccbccbcc`.

**Example 2.** Input `2[2[]a]`, output `aa`.

**Hint.** After a `]`, which variable must hold the text of the group that just closed, and which number must the next `[` start from?

**Changed decision.** The invariant must hold across a group that closes and another that opens at once, so `count` resets at each `[` and `cur` returns to the parent.

#### [Recognize] Decode String (LeetCode 394)
<!-- id: sq-leetcode-decode-string -->

**Prerequisites.** All exercises above.

**Problem.** An encoded string follows this grammar. It is a sequence of lowercase letters and groups. A group is a positive decimal number, then `[`, then an encoded string, then `]`. The decoded string replaces each group by its inner decoded string written as many times as the number says. Given a well-formed encoded string, return its decoded string.

**Constraints.** The limits are:
- **Length** is 0 to 1000 characters, and the text is well formed.
- **Numbers** are from 1 to 300 and can have several digits.
- **Output** has at most 100000 characters.
- **Characters** are lowercase letters, digits, `[` and `]` only, and digits appear only as group numbers.

**Example 1.** Input `3[a2[b]]c`, output `abbabbabbc`.

**Example 2.** Input `a2[b3[c]]d`, output `abcccbcccd`.

**Hint.** Combine the multi-digit number with one frame per open group. What does the top frame hold when `]` arrives?

**Changed decision.** The full grammar combines multi-digit numbers, nesting and adjacent groups in one pass with one stack of frames.
