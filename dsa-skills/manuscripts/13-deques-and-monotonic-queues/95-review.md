<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios do not name the method, so decide what the deque stores, which end is removed for age and which for domination, before you read the options. Recall and recognition are what these questions test, which guided exercises cannot.

### Recognition Questions

```quiz
{"id":"dq-rev-owner-ends","q":"In a window deque of positions, which end receives new positions and which end is read for the answer?","options":["New positions go to the front and the back is read.","New positions go to the back and the front is read.","Both ends receive and both are read.","Positions go to the middle."],"answer":1,"explain":"Positions arrive in increasing order at the back, and the front is the oldest survivor, which is also the best one."}
```

```quiz
{"id":"dq-rev-store-positions","q":"Why does the deque keep positions and not values?","options":["Positions use less memory.","The age test needs the position, and the value can be read from it.","Values cannot be compared.","Java forbids a deque of values."],"answer":1,"explain":"A position gives both the age and the value, while a stored value alone cannot be tested for expiry and loses which of two equal values is older."}
```

```quiz
{"id":"dq-rev-expiry-first","q":"Why is the front tested for age before the front is read as an answer?","options":["Reading is slower than testing.","An expired position may still sit at the front and would give a value from outside the window.","The back must be trimmed first.","The deque would be empty."],"answer":1,"explain":"The front stays where it is until it is removed, so reading it before the age test can return a record that has already left the window."}
```

```quiz
{"id":"dq-rev-expiry-test","q":"For a window of length k ending at right, which stored position is expired?","options":["Any position below right - k.","Any position at most right - k.","Any position above right - k.","Any position equal to k."],"answer":1,"explain":"The window covers right - k + 1 through right, so a position equal to right - k is already outside it."}
```

```quiz
{"id":"dq-rev-equal-values","q":"A maximum deque removes only strictly smaller values from the back. What happens to an equal earlier value?","options":["It is removed immediately.","It stays behind the newcomer and expires on its own schedule.","It is counted twice.","It blocks the newcomer."],"answer":1,"explain":"With a strict comparison an equal value stays in the deque in age order, so it is still there when a newer equal value would otherwise have been needed after the older one leaves."}
```

```quiz
{"id":"dq-rev-mirror","q":"Which change turns the maximum deque into a minimum deque?","options":["Read the back instead of the front.","Flip the comparison in the back loop and keep the expiry test as it is.","Flip the expiry test.","Reverse the array."],"answer":1,"explain":"Only the order of values changes, and age works the same way for both, so the back comparison is the one line that differs."}
```

```quiz
{"id":"dq-rev-two-deques","q":"Why does a range over a window need two deques?","options":["One deque is too short.","The order that suits the maximum is the opposite of the one that suits the minimum.","Java limits a deque to one extreme.","The front holds the sum."],"answer":1,"explain":"A position beaten for the maximum may be needed for the minimum, so each extreme keeps its own order, and both fronts share the same expiry."}
```

```quiz
{"id":"dq-rev-negative-window","q":"Why does a two-pointer window fail for the shortest run reaching a target when values can be negative?","options":["It runs out of memory.","Dropping a negative value from the left can raise the total, so the shrink rule is no longer safe.","The target is too large.","The window is too short."],"answer":1,"explain":"The plain window assumes that removing an element never raises the sum, and a negative element breaks that assumption."}
```

```quiz
{"id":"dq-rev-prefix-trim","q":"In the prefix-sum deque, why is a stored start removed from the back when a newer cut point has a value that is not larger?","options":["It is expired.","The newer start is closer to every later end and gives a difference that is no smaller.","Equal values cannot be stored.","It has already been used."],"answer":1,"explain":"The older start can never beat the newer one, so keeping it only blocks the order that lets the front be the single start worth testing."}
```

```quiz
{"id":"dq-rev-long-sums","q":"For the values 2000000000 and -2000000000 in an int array, why is the difference of the two unsafe in int?","options":["Subtraction is never safe.","The true difference is outside the int range and wraps.","Java turns it into a double.","The result is always zero."],"answer":1,"explain":"The int range ends near 2147483647, so a difference of four billion wraps, and widening one operand to long before the subtraction keeps it exact."}
```
