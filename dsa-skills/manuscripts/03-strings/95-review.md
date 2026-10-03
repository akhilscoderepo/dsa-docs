<!-- section: review -->
## Review

Take this review when the lessons are finished, then retake it after a few days. The scenarios leave out the technique name on purpose, so choose your answer before reading the options. What is tested is spotting the situation and predicting what the code does, which the exercise ladders touch only indirectly.

### Recognition Questions

```quiz
{"id":"st-rev-concat","q":"A loop appends one character at a time to a Java String with += for a result of n characters. What is the cost, and what is the usual repair?","options":["O(n) overall, and nothing needs repairing.","O(n * n) overall, because each += copies the growing result; use a StringBuilder.","O(n * n) overall, because the loop is nested; use a HashMap.","O(log n) overall, because strings are compared by hash."],"answer":1,"explain":"Strings are immutable, so every += builds a new string and copies everything so far. A StringBuilder appends in amortized constant time and is converted once at the end."}
```

```quiz
{"id":"st-rev-scan","q":"A scan returns -1 for a missing character. At which moment is that answer justified?","options":["After the first non-matching character.","After half the string has been read.","After the loop has examined every position without a match.","Never, because a missing character cannot be proved."],"answer":2,"explain":"The invariant says everything before the current index has been ruled out, so only when the loop ends does it cover the whole string."}
```

```quiz
{"id":"st-rev-parse","q":"A parser reads digits left to right to build a number. Which update keeps the invariant that the value covers the digits read so far?","options":["value = value + digit","value = value * 10 + digit","value = digit * 10 + value","value = value * digit"],"answer":1,"explain":"Reading a new digit shifts the existing digits one place left, which is a multiplication by ten, and then adds the new digit in the units place."}
```

```quiz
{"id":"st-rev-normalize","q":"Two strings should match if they contain the same letters ignoring case and punctuation. What should happen before comparing?","options":["Sort both strings and compare lengths.","Convert both to a common case and drop the characters that do not count, then compare.","Compare with == and fall back to equals.","Reverse both strings."],"answer":1,"explain":"Normalization maps every input to one canonical form first, so that the comparison itself is plain and the rules for what counts live in one place."}
```

```quiz
{"id":"st-rev-alphabet","q":"A letter table of 26 counters is indexed by c - 'a'. For which input does indexing it break?","options":["A string of repeated letters.","An empty string.","A string that contains an uppercase letter or a digit.","A string of 100,000 characters."],"answer":2,"explain":"The index c - 'a' is negative for uppercase letters and above 25 for digits and many symbols, so the alphabet contract must be checked or promised."}
```

```quiz
{"id":"st-rev-runs","q":"The string abab is encoded with count-then-character for maximal runs. What is the result, and what does it show?","options":["2a2b, because totals are kept.","1a1b1a1b, because equal characters that are not neighbours stay separate.","2a2b1, because the last run is dropped.","ab, because duplicates are removed."],"answer":1,"explain":"No two neighbours are equal, so there are four runs of length one. Grouping equal characters wherever they sit would need a table and would lose the positions."}
```

```quiz
{"id":"st-rev-final","q":"A run encoder writes the pending run whenever the next character differs. For the input aaab, what does it produce if it stops after the loop?","options":["3a1b","3a","1b","The empty string."],"answer":1,"explain":"The last run never meets a different character, so nothing triggers its write. The end of the input must flush the pending run once more."}
```

```quiz
{"id":"st-rev-center","q":"A palindrome search tries only centers that sit on a single character. Which string does it handle incorrectly?","options":["racecar","aaa","abba","x"],"answer":2,"explain":"abba is symmetric around the gap between its two b characters, so only an even center, with the boundaries starting on adjacent indices, finds it."}
```

```quiz
{"id":"st-rev-ends","q":"Which question is a false friend for center expansion?","options":["Count all palindromic substrings of a string.","Return the longest palindromic substring.","Decide whether one given string reads the same forwards and backwards.","Find the longest even-length palindromic substring."],"answer":2,"explain":"A single string has one candidate, so there is no middle to search for. Walking inward from the two ends is enough, and that technique belongs to a later chapter."}
```
