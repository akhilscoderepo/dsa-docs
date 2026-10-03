<!-- section: orientation -->
## Orientation

A deque lets a program add and remove at both ends in constant time, and that single ability is what answers a family of questions about moving stretches of data. When the stretch has an edge that advances and the question asks for its largest or smallest value, a deque of positions can keep just the candidates that still have a chance, with the best one always at the front. The result is one pass instead of a rescan of every stretch. This chapter builds the structure from the mechanics of the Java class up to problems on negative numbers, and keeps asking the same two questions: which end is leaving because of age, and which end is leaving because it was beaten.

### Before You Begin

You should be comfortable with the earlier chapters on arrays, prefix sums, two pointers and the sliding window, with the monotonic stack of Chapter 12, and with `ArrayDeque` used as a plain stack or queue. The window chapter supplies the idea of edges that only move forward, and the stack chapter supplies the idea of discarding entries that can never answer. Graph search with a deque is named at the end of the chapter as a later topic and is not needed here.

### The Nine Lessons

The first lesson covers the methods of `ArrayDeque`, the exceptions it throws, and the rule that decides which end owns which job. The second states the two invariants that a monotonic deque keeps, one for position order and one for value order. The third and fourth take the two removals apart, so that removal from the back because of domination and removal from the front because of age are studied separately. The fifth puts them together as the sliding maximum, and the sixth mirrors it into the sliding minimum and into a pair of deques for ranges. The seventh generalises the age test to a lookback and to a supplied boundary array, and applies it to a recurrence over best scores. The eighth uses cumulative sums to handle negative numbers and finds the shortest run that reaches a target. The ninth combines the window with the deque and answers three new questions with one skeleton.

### How To Work Through A Lesson

Each lesson opens with a scene and a plain method, and then shows why the plain method repeats work. Before reading the insight, say aloud what the deque would have to hold. The traces print the deque after every step, and the text names the one step worth reading twice. Try each exercise before its hint. For every one, write down three things first: what the deque stores, what removes from the front, and what removes from the back. The Java in each solution is compiled, run, and compared with a slower method that tries everything.

### Leaving The Chapter

You should be able to say why the deque stores positions and not values, why age is tested before the front is read, why equal values need a deliberate policy, and why subtraction of two large integers needs a wider type. You should also be able to explain why a cumulative-sum deque is trimmed from the back and not only from the front. The review that follows poses short scenarios, and it is worth repeating after a few days.
