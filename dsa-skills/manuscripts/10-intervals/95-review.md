<!-- section: review -->
## Review

Come back to this section after the lessons and again after a few days. The scenarios do not name a method, so decide the contract, the sort key and the carried number before you open the options. These questions test recall and recognition, which guided exercises cannot.

### Recognition Questions

```quiz
{"id":"iv-rev-sort-key","q":"A list of intervals is to be fused into blocks of overlap. Which sort key makes one scan enough?","options":["Sort by length.","Sort by start.","Sort by end descending.","No sort is needed."],"answer":1,"explain":"With the starts in order, a block that is closed to the next start can never be reopened, so the furthest end of the open block is all that has to be remembered."}
```

```quiz
{"id":"iv-rev-subtract","q":"Why is a comparator written as a[1] - b[1] unsafe for intervals?","options":["It is slower than compare.","The difference of two extreme ints can wrap around and flip the sign.","It sorts descending.","It copies the arrays."],"answer":1,"explain":"Subtracting a large negative end from a large positive one overflows int, so the sign that the sort depends on can be wrong."}
```

```quiz
{"id":"iv-rev-touch-closed","q":"Under closed intervals, do [1, 5] and [5, 9] overlap?","options":["No, they only touch.","Yes, they share the value 5.","Only if the list is sorted.","Only if one is longer."],"answer":1,"explain":"A closed interval contains both ends, so the value 5 belongs to both and the test is start at most end."}
```

```quiz
{"id":"iv-rev-half-open","q":"Under half-open intervals, a new interval starts exactly at the carried end. What does the scan conclude?","options":["A clash, so the block is extended.","No clash, so a new block begins.","The input is invalid.","The new interval is covered."],"answer":1,"explain":"A half-open interval does not contain its end, so the carried end is free for the next interval to start on, and nothing is shared."}
```

```quiz
{"id":"iv-rev-merge-vs-insert","q":"A new interval is added to a sorted, disjoint list. Why is a full sort unnecessary?","options":["Sorting is forbidden.","The list is ordered, so the intervals before, overlapping and after the new one form three contiguous regions.","The new interval is always last.","Disjoint lists are always short."],"answer":1,"explain":"Order and disjointness mean the overlapped intervals sit side by side, so one pass over three regions replaces the sort."}
```

```quiz
{"id":"iv-rev-intersection-advance","q":"After handling a pair of intervals from two sorted lists, which cursor advances?","options":["Both always.","The one whose interval ends first.","The one whose interval starts first.","The longer interval."],"answer":1,"explain":"The interval that ends earlier cannot meet anything later in the other list, while the one that ends later may still have a partner waiting."}
```

```quiz
{"id":"iv-rev-keep-most","q":"To keep the most mutually compatible intervals, which order does the greedy scan use?","options":["By start ascending.","By end ascending.","By length ascending.","By end descending."],"answer":1,"explain":"The interval that finishes first leaves the most room for the rest, and the exchange argument shows that swapping to it never reduces the count."}
```

```quiz
{"id":"iv-rev-covered-tie","q":"When removing covered intervals, why are equal starts ordered with the longer end first?","options":["To save memory.","So that a container is counted before the shorter interval it hides.","So that equal intervals are removed.","To make the sort stable."],"answer":1,"explain":"If the shorter interval came first, it would be counted visible and raise the reach, and its container would then be counted as a second visible interval."}
```

```quiz
{"id":"iv-rev-sweep-tie","q":"For half-open intervals, which entry is applied first when a start and an end share a coordinate in a sweep?","options":["The start.","The end.","Whichever was input first.","The longer interval."],"answer":1,"explain":"The interval that ends at the coordinate is already gone when the other begins, so the count must drop before it rises, otherwise a touching pair is counted as overlapping."}
```

```quiz
{"id":"iv-rev-group-test","q":"When a sweep asks for the first coordinate at which the count reaches a limit, when should the counter be tested?","options":["After every entry.","After the last entry of each coordinate group.","Only at the end.","Only at starts."],"answer":1,"explain":"A value inside a group depends on the order of its members and may never describe a real coordinate, so only the value after the whole group counts."}
```
