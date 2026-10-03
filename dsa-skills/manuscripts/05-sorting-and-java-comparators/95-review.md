<!-- section: review -->
## Review

Come back to this section after the lessons and again after a few days. The scenarios do not name the technique, so decide what order, tie rule or signature the situation needs before you read the options. These questions test recognition and prediction, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"so-rev-subtraction","q":"A comparator is written as (a, b) -> a - b and used on an Integer[] that may contain Integer.MIN_VALUE and Integer.MAX_VALUE. What can go wrong?","options":["It sorts in descending order.","The difference can wrap around, so a smaller value may be reported as larger.","It throws a NullPointerException on every call.","It is slower than Integer.compare by a factor of two."],"answer":1,"explain":"Subtraction of two ints can exceed 32 bits and wrap, which flips the sign. Integer.compare returns the sign without computing a difference."}
```

```quiz
{"id":"so-rev-primitive-comparator","q":"You need int values in descending order and write Arrays.sort(a, Comparator.reverseOrder()) with a declared as int[]. What happens?","options":["It compiles and sorts descending.","It does not compile, because the comparator form needs an object array.","It sorts ascending and ignores the comparator.","It compiles and throws at run time."],"answer":1,"explain":"Arrays.sort(int[]) has no comparator overload. Box the values into Integer[] or sort ascending and read the result backwards."}
```

```quiz
{"id":"so-rev-slice","q":"Arrays.sort(a, 2, 5) is called on an array of length 8. Which positions can change?","options":["Positions 2, 3, 4 and 5.","Positions 2, 3 and 4.","Positions 3, 4 and 5.","Positions 0 to 4."],"answer":1,"explain":"The range is half-open: the start is included and the end is excluded, so the slice has length 3 and position 5 stays where it was."}
```

```quiz
{"id":"so-rev-laws","q":"A comparator returns 1 whenever a is not smaller than b, including for equal elements. Which law does it break?","options":["Transitivity only.","Antisymmetry, since two equal elements are each reported as coming after the other.","None, because equal elements may be ordered either way.","The overflow rule."],"answer":1,"explain":"For equal elements compare(a, b) and compare(b, a) must both be zero. Returning 1 in both directions breaks antisymmetry, even though many inputs still sort correctly."}
```

```quiz
{"id":"so-rev-ties","q":"Orders are sorted by priority only, with a comparator that returns zero on equal priorities, in a List of objects. The business rule says earlier orders win ties. Is the code correct?","options":["No, because the sort is unstable.","Yes, because the object sort is stable and equal priorities keep their input order, provided the list was in arrival order.","No, because a comparator must never return zero.","Yes, but only for lists shorter than 32 elements."],"answer":1,"explain":"List.sort on objects is stable by contract, so tied elements keep the order they had in the input. The rule is satisfied as long as the input is in arrival order, and writing the index into the comparator would make that explicit."}
```

```quiz
{"id":"so-rev-primitive-stability","q":"You must report original positions of equal values in increasing position order after sorting an int[]. What is the safest approach?","options":["Sort the int[] and trust the result keeps positions.","Sort boxed indices with a comparator that compares the value and then the index.","Sort twice.","Use a smaller array."],"answer":1,"explain":"Sorting the primitive values loses positions and offers no stability promise. A comparator that ends in the index makes the tie rule explicit and independent of the algorithm."}
```

```quiz
{"id":"so-rev-case","q":"A TreeSet is created with String::compareToIgnoreCase, and the words Bob and bob are added. How many words does the set hold?","options":["Two.","One, because the comparator returns zero and the set treats them as the same element.","Zero.","It depends on the JDK version."],"answer":1,"explain":"A sorted set decides equality with the comparator, not with equals. A zero means already present, so the second word is silently dropped."}
```

```quiz
{"id":"so-rev-frontier","q":"Requests may only be raised, and every final value must be unique, with the smallest total raise wanted. After sorting, what single piece of state is enough for the sweep?","options":["A set of all earlier requests.","The largest final value assigned so far.","The count of equal values seen.","The median of the requests."],"answer":1,"explain":"After sorting, each request is placed at the larger of its own value and one more than the last assigned value, so only that last value matters."}
```

```quiz
{"id":"so-rev-run-start","q":"A distinct-values routine keeps previous = 0 and emits a value whenever it differs from previous. Which input exposes the flaw?","options":["[1, 2, 3].","[0, 0, 0].","[5, 5].","[]."],"answer":1,"explain":"The first zero equals the made-up previous value, so it is skipped and the result is empty. The first position must start a run without comparing to anything."}
```

```quiz
{"id":"so-rev-kth","q":"To find the k-th largest distinct value, a solution sorts ascending and returns a[a.length - k]. When is it wrong?","options":["When k is 1.","When duplicates are present, because the position counts copies and not distinct values.","When the array is empty only.","Never."],"answer":1,"explain":"With duplicates, the position from the end counts repeated values several times. Counting changes of value while scanning gives distinct places, and the stated fallback covers too few of them."}
```

```quiz
{"id":"so-rev-binary-search","q":"A problem gives a sorted array. Does that alone make binary search a valid tool?","options":["Yes, always.","No, binary search also needs a yes-or-no question over positions that is monotone, with all the no answers on one side and all the yes answers on the other.","Yes, but only for integers.","No, sorted arrays must be reversed first."],"answer":1,"explain":"Order is only part of the contract. The search needs a monotone question so that discarding half the positions is safe."}
```

```quiz
{"id":"so-rev-signature","q":"Which statement about anagram grouping keys is correct?","options":["A sorted string needs the alphabet to be lowercase English letters.","A 26-slot count array is valid only under a stated alphabet, while a sorted string works for any characters.","A char[] can be used directly as a HashMap key.","Sorted keys cannot be used with a LinkedHashMap."],"answer":1,"explain":"Sorting needs no alphabet contract. A fixed-size count array is a faster alternative that depends on one, and a char[] must be converted to a String because arrays compare by identity."}
```

```quiz
{"id":"so-rev-close","q":"Two strings may be changed by swapping any two positions, or by exchanging two existing letters everywhere. Which comparison correctly decides whether they can match?","options":["Their sorted strings are equal.","Their letter sets are equal and their sorted lists of counts are equal.","Their lengths are equal.","Their first letters are equal."],"answer":1,"explain":"Swapping positions removes arrangement, and exchanging letters moves counts between letters that already occur. So the set of letters and the multiset of counts are the facts that survive."}
```
