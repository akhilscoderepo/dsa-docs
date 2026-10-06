<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "dq-rev-poll-null", "q": "A program calls `pollFirst()` on an empty `ArrayDeque<Integer>` and assigns the result to an `int`. What happens?", "options": ["It throws NullPointerException when the null is unboxed", "It throws NoSuchElementException from the call", "It returns 0", "It returns -1"], "answer": 0, "explain": "The call returns `null` on an empty deque. Unboxing that `null` into an `int` throws NullPointerException. The throwing form `removeFirst()` is the one that raises NoSuchElementException."}
```

```quiz
{"id": "dq-rev-equal-stay", "q": "A deque holds the values 9, 6, 2 from front to back and keeps non-increasing order. The value 6 arrives, and equal values stay. What does the deque hold afterwards?", "options": ["9, 6", "6", "9, 6, 6", "9, 6, 2, 6"], "answer": 2, "explain": "The back value 2 is strictly smaller than 6 and leaves. The next back value is 6, which is equal, so it stays. The new 6 is appended, which gives 9, 6, 6."}
```

```quiz
{"id": "dq-rev-newer-wins", "q": "The scores 4 and then 7 arrive. Every later window that contains 4 also contains 7. What does the maximum deque do with 4?", "options": ["Keeps it until it expires", "Removes it from the front", "Moves it behind 7", "Removes it from the back"], "answer": 3, "explain": "The score 7 is newer and larger, so 4 can never be the maximum of a window that holds both. The back removes 4 when 7 arrives."}
```

```quiz
{"id": "dq-rev-expiry-edge", "q": "A range of length 4 ends at position 9. Which stored position is the largest expired position?", "options": ["Position 6", "Position 5", "Position 7", "Position 9"], "answer": 1, "explain": "The range covers positions 6 through 9, so the left bound is 6. Position 5 lies below it and is at most `9 - 4`, which makes it expired. Position 6 is still inside."}
```

```quiz
{"id": "dq-rev-read-last", "q": "In the window maximum method, the front is read before the new position is appended. What goes wrong?", "options": ["The age test removes the new position", "The answer misses a new position that is the largest in the range", "The deque loses its order", "The method reads an empty deque on every step"], "answer": 1, "explain": "The new position may be the maximum, and it is not in the deque until the append. Reading first returns the maximum of the previous range. The read belongs after the append."}
```

```quiz
{"id": "dq-rev-copied-max", "q": "A developer copies the window maximum method for a minimum and changes only the method name. What does the copy return?", "options": ["The minimum of each range", "An empty array", "The maxima of each range", "An exception"], "answer": 2, "explain": "The back comparison still removes smaller values, so the front holds the largest value. The copy runs without error and returns maxima under the name of minima."}
```

```quiz
{"id": "dq-rev-query-order", "q": "A query at position i must not see position i. Where does the read sit among the age test, the back removal and the append?", "options": ["After the append", "Right after the age test, before the back removal", "Before the age test", "After the back removal and before the append"], "answer": 1, "explain": "The age test makes every stored position eligible. The read then uses the front. The append comes last, because it would put position i into its own query."}
```

```quiz
{"id": "dq-rev-shrink-fails", "q": "The values are 4, -5, 6, -1, 7 and the target is 12. Why does a method that shrinks the window only when the total reaches the target miss the answer 3?", "options": ["The window is too short", "The total never reaches 12, so the method never tests the last three values alone", "The method removes the largest value first", "The values are not sorted"], "answer": 1, "explain": "The total of all five values is 11 and never reaches 12, so the method never shrinks. The last three values total 12, but a negative value earlier lowered the total. Prefix positions in a deque find that run."}
```

```quiz
{"id": "dq-rev-two-extremes", "q": "A window must keep its largest value minus its smallest value within a limit while its left end moves forward. Which state gives both extremes in constant time?", "options": ["One deque of positions", "Two deques of positions", "A running total", "A sorted copy of the window"], "answer": 1, "explain": "One deque gives one extreme, and a total gives neither. A sorted copy costs more per update. Two deques give the maximum and the minimum, and they expire the same positions."}
```

### Recall Exercises

Close this page and answer from memory, then check against the lessons. Write the three steps that run for each new position in a window maximum, in order, and say which end each step touches. State what the deque holds after the values 5, 3, 4, 4, 2, 6 under the maximum rule, and which position remains. Explain in two sentences why a start with a smaller prefix sum later in the array beats an earlier start with a larger one.
