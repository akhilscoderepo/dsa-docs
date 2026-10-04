<!-- section: review -->
## Review

Return to this page after the lessons and again a few days later. Each question describes a situation and hides the lesson name. Commit to an answer before you open the explanation.

### Recognition Questions

```quiz
{"id":"st-rev-word-start","q":"A loop counts the words of a text that may contain repeated, leading and trailing spaces. Which test marks index `i` as the first character of a word?","options":["`s.charAt(i) != ' '`","`s.charAt(i) == ' '`","`s.charAt(i) != ' '` and either `i == 0` or `s.charAt(i - 1) == ' '`","`s.charAt(i - 1) != ' '`"],"answer":2,"explain":"A word starts at a non-space character that follows a space or sits at index 0. The first option also fires inside a word, and the last option reads before the string when `i` is 0."}
```

```quiz
{"id":"st-rev-insert-front","q":"A loop reverses a string by calling `out.insert(0, ch)` on a `StringBuilder` once for each of n characters. What is the total cost?","options":["O(n)","O(n log n)","O(1)","O(n^2)"],"answer":3,"explain":"Each insert at index 0 shifts every character that is already in the builder, so the shifts add up to about n squared over 2. Appending in reverse order costs O(n)."}
```

```quiz
{"id":"st-rev-parser-state","q":"A parsing loop keeps one variable named `state`. What should that variable record?","options":["Every character read so far","Only the facts that decide which next character is legal","The number of characters read","The result of the last comparison"],"answer":1,"explain":"The state is a summary of the accepted prefix. It keeps what the next decision needs and drops everything else, so the loop stays O(1) in space."}
```

```quiz
{"id":"st-rev-normalize","q":"Two product codes must count as equal when they hold the same letters and digits in the same order, ignoring letter case and every other character. What is the first step of a correct comparison?","options":["Build, for each code, a string of its lowercase letters and digits","Lowercase both codes and compare them","Delete the dashes from both codes","Compare the lengths of the two codes"],"answer":0,"explain":"The rule has two kinds of noise, case and separators. Only a standard form that removes both lets one `equals` call decide, and each side must use the same function."}
```

```quiz
{"id":"st-rev-table-slot","q":"A text holds only lowercase English letters, and a program counts each letter in an `int[26]`. Which expression gives the slot of the character `c`?","options":["`c`","`c + 'a'`","`c % 26`","`c - 'a'`"],"answer":3,"explain":"Subtracting `'a'` maps `'a'` to 0 and `'z'` to 25. Any character outside that range gives an index that is not legal and throws an exception."}
```

```quiz
{"id":"st-rev-final-run","q":"A loop measures runs of equal characters and closes a run only when it meets a different character. Which run does it leave open?","options":["The first run","The final run, which ends at the end of the string","The middle runs","None, because every run has a boundary"],"answer":1,"explain":"The last run has no character after it, so nothing triggers its closing. The loop must treat the end of the string as a boundary."}
```

```quiz
{"id":"st-rev-middles","q":"A string holds 6 characters. How many middles, odd centers and gaps together, does center expansion try?","options":["11","6","7","12"],"answer":0,"explain":"There are 6 odd centers and 5 gaps between neighbors, so the total is `2n - 1 = 11`. Every palindromic substring has exactly one of these middles."}
```
