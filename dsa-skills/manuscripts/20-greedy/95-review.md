<!-- section: review -->
## Review

Return to this section after the lessons and once more a few days later. The scenarios avoid naming the technique, so decide what the choice is and what would make it safe before you look at the options. The questions probe the reasons behind the code, which the guided exercises seldom do.

### Recognition Questions

```quiz
{"id": "gr-rev-coin-counter", "q": "Coins of 1, 3 and 4 must make 6. A rule takes the largest coin that fits at each step. What does this show?", "options": ["The rule is optimal, since 4 and 2 make six.", "It gives 4, 1, 1 while 3 and 3 use fewer coins, so choosing the largest needs a proof that it lacks.", "It proves that greedy rules never work for coins.", "It gives 3 and 3, which matches the best."], "answer": 1, "explain": "Largest-first takes 4 and then needs two ones, three coins, while two threes are enough. A rule that sounds natural is not safe until an exchange argument backs it, and one failing input settles the question."}
```

```quiz
{"id": "gr-rev-smallest-fit", "q": "Parties of sizes 2 and 6 are waiting, and rooms of 3, 7 and 9 beds are free. Which room should the party of 2 receive?", "options": ["The room of 9 beds, to keep the guest comfortable.", "The room of 7 beds.", "The room of 3 beds, the smallest that fits.", "Any room, since the choice cannot matter."], "answer": 2, "explain": "The smallest room that fits dominates the others. Anything the party of 6 could use after another choice is still available after this one."}
```

```quiz
{"id": "gr-rev-start-order", "q": "Why does sorting events by start time fail for choosing the largest set of non-overlapping events?", "options": ["Start times are often equal.", "Sorting by start is slower than sorting by end.", "The first event by start can be long and block many short ones that end earlier.", "A sort by start cannot be done in place."], "answer": 2, "explain": "With events 0 to 10, 1 to 2 and 3 to 4, start order takes the long one first and holds a single event, while end order holds two."}
```

```quiz
{"id": "gr-rev-touching", "q": "Spans 1 to 3 and 3 to 5 touch at one point. How many of the two can be chosen as non-overlapping spans?", "options": ["One under the closed model and two under the half-open model.", "Two under both models.", "One under both models.", "Two under the closed model and one under the half-open model."], "answer": 0, "explain": "Closed spans share the point 3, so only one can be chosen. Half-open spans do not share it, so both fit. The acceptance test is a strict comparison in one model and a non-strict one in the other."}
```

```quiz
{"id": "gr-rev-reach-prefix", "q": "In the relay towers, why can everything reachable be summarised by one number?", "options": ["Every tower has the same strength.", "The farthest tower is always the best to pass the message to.", "A jump covers every tower between its start and its target, so the reachable towers form an unbroken prefix.", "The message is passed to every tower in turn."], "answer": 2, "explain": "Because no reachable tower is ever skipped over, the highest reachable index tells the whole story, and an index beyond it proves failure."}
```

```quiz
{"id": "gr-rev-layer-stuck", "q": "In the layered count of jumps, the scan reaches the end of a layer and the best reach recorded is equal to that end. What does it mean?", "options": ["The last tower has been reached.", "Another layer can start immediately.", "The count so far is the answer.", "Nothing in the layer can forward the message, so the summit cannot be reached."], "answer": 3, "explain": "A new layer extends past the old one only if some member reaches beyond it. A record equal to the layer end means no extension is possible."}
```

```quiz
{"id": "gr-rev-counterexample", "q": "Which one input is enough to disprove the rule always take the shortest interval for maximum scheduling?", "options": ["Any input on which the rule finishes in under a second.", "A large random input where the rule agrees with the best answer.", "A single input on which the rule selects fewer intervals than the best answer.", "Ten inputs on which the rule agrees with the best answer."], "answer": 2, "explain": "A counterexample is a complete disproof. Agreeing examples can only support intuition, and the failure of the shortest-first rule appears on three intervals."}
```

```quiz
{"id": "gr-rev-retract-longest", "q": "Courses are processed by deadline with a heap of retained durations, and the total now exceeds the current deadline. Which course is removed?", "options": ["The earliest course in the heap.", "The newcomer, always.", "The shortest retained course.", "The longest retained course, which may be the newcomer."], "answer": 3, "explain": "Removing the longest keeps the count and gives the smallest total, which leaves the most room for later courses."}
```

```quiz
{"id": "gr-rev-heap-direction", "q": "In the furthest-building problem, each climb takes a winch at first. Which heap holds them, and which end is retracted when winches run out?", "options": ["A min-heap, and the smallest climb is retracted and paid in timber.", "A max-heap, and the largest climb is retracted.", "A max-heap, and the smallest climb is retracted.", "A min-heap, and the largest climb is retracted."], "answer": 0, "explain": "Winches belong on the biggest climbs, so the smallest climb on a winch is the one to give up, and it sits on top of a min-heap."}
```

```quiz
{"id": "gr-rev-affordable-pool", "q": "Why is a max-heap of the profits of all projects the wrong tool for the capital problem?", "options": ["It could hand back a project whose required capital is not yet met.", "Max-heaps cannot hold duplicate values.", "Profits are not comparable.", "It is slower than sorting once."], "answer": 0, "explain": "Only projects whose capital is at most the current capital may be chosen, so they enter the pool as the capital grows and the best of the pool is taken."}
```

```quiz
{"id": "gr-rev-return-promise", "q": "When may the top letter be popped in the smallest subsequence with each letter once?", "options": ["Whenever it is larger than the incoming letter.", "Only when it is smaller than the incoming letter.", "When it is larger than the incoming letter and the same letter appears again later in the string.", "When the stack is longer than the number of distinct letters."], "answer": 2, "explain": "Popping a letter that never returns would lose it for good. A letter that is already on the stack is skipped when it comes again, because its earlier copy sits in a better place."}
```

```quiz
{"id": "gr-rev-pop-budget", "q": "What does the competitive-subsequence problem need that the plain next-smaller stack does not?", "options": ["A check that enough elements remain to refill the stack to the required length.", "A second stack.", "A sort of the input.", "A hash map of positions."], "answer": 0, "explain": "A pop is allowed only while the elements still unread can bring the stack back to length k, which is the budget for this contract."}
```

```quiz
{"id": "gr-rev-heaviest-alone", "q": "Sorted passengers, a boat for at most two, and the lightest plus the heaviest exceed the limit. What follows?", "options": ["The lightest should ride alone.", "The heaviest rides alone, since every other partner is at least as heavy as the lightest.", "Both must ride in separate boats and the pointers stay in place.", "The limit has been entered incorrectly."], "answer": 1, "explain": "Any partner of the heaviest weighs at least as much as the lightest, so none fits, and the heaviest leaves the problem alone."}
```

```quiz
{"id": "gr-rev-int-sum", "q": "Two people each weigh 2147483647 and the limit is 2147483647. Which hazard decides the answer in Java?", "options": ["Sorting would reorder equal values.", "An int sum of the two weights wraps to a negative number and wrongly passes the limit test.", "Arrays cannot hold values this large.", "The limit is not an int."], "answer": 1, "explain": "The true total is far above the limit. Adding in long before comparing keeps the test honest and gives two boats."}
```
