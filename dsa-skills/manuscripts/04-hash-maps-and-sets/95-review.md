<!-- section: review -->
## Review

Return here after the lessons, and again once a few days have passed. Each scenario avoids naming the structure involved, so decide what the key and value should be before the options appear. Recognition and prediction are what these questions measure, and the guided exercises do not measure them.

### Recognition Questions

```quiz
{"id":"hm-rev-membership","q":"A scan must stop at the first repeated value in an array of 100,000 integers. Which structure keeps the work linear, and what does it store?","options":["A list of values seen so far, searched with contains.","A hash set of the values seen so far, tested before each insert.","A hash map from each value to its count, read at the end.","A sorted copy of the array, searched with binary search."],"answer":1,"explain":"Only presence matters, so a set answers each question in expected constant time. A list makes each test linear, a count map stores a number nobody reads, and a sorted copy costs more."}
```

```quiz
{"id":"hm-rev-counts","q":"Two strings have the same set of letters, but the first has three a characters and the second has two. A set-based comparison says they match. What is the repair?","options":["Compare the lengths only.","Use a frequency map for each string and compare the maps.","Sort both strings and use ==.","Compare the first characters."],"answer":1,"explain":"A set forgets multiplicity. The ledger of counts per key keeps it, and Map.equals compares keys and values regardless of order."}
```

```quiz
{"id":"hm-rev-index-rule","q":"A map from value to index is used to find two equal values at most k positions apart. When the same value appears again, what should happen to its stored index?","options":["Keep the first index, because it is earliest.","Overwrite it with the current index, because the latest copy is closest to later positions.","Delete the entry, because the pair was handled.","Store both indices in a list."],"answer":1,"explain":"For a distance limit, only the nearest earlier copy can be within range, so each sighting replaces the old entry."}
```

```quiz
{"id":"hm-rev-grouping","q":"Numbers are grouped by Math.floorMod(x, 4), and the answer must list the numbers in each group. Which map value type is right?","options":["An Integer count.","A Boolean flag.","A List of the numbers in that group.","A single int holding the sum."],"answer":2,"explain":"Grouped output needs the members, not just how many there are. A count map answers a different question."}
```

```quiz
{"id":"hm-rev-sequence","q":"To find the longest run of consecutive integers in an unsorted array in expected linear time, why does the scan begin only at values whose predecessor is absent?","options":["It avoids reading duplicates twice.","It makes each run get walked once, from its lowest value, so no value is walked many times.","It sorts the values as a side effect.","It reduces the memory used by the set."],"answer":1,"explain":"A walk from a middle value repeats work already done from the start of its run. Starting only at run starts gives each value to exactly one walk."}
```

```quiz
{"id":"hm-rev-array-key","q":"A program counts observations keyed by int[] {row, col} in a HashMap. Two observations have the same two numbers. What happens?","options":["They are merged into one key with count 2.","They become two separate keys, because arrays use identity equality.","The program throws an exception.","The second observation replaces the first and the count stays 1."],"answer":1,"explain":"Arrays do not override equals or hashCode, so equal contents are different keys. A record such as Point(int row, int col) fixes this."}
```

```quiz
{"id":"hm-rev-mutable","q":"A key object is stored in a HashMap, and then a field used in its hashCode is changed. What is the most likely result of containsKey on that same object?","options":["true, because it is the same object.","false, because the lookup searches the bucket for the new hash code, though the entry stays where it was filed.","An exception is thrown.","The entry is removed automatically."],"answer":1,"explain":"The entry stays in the bucket chosen by the old hash code. The lookup computes the new hash code and searches elsewhere, so the entry is unreachable by lookup while still counted in the size."}
```

```quiz
{"id":"hm-rev-direct","q":"Identifiers are integers between 0 and 1,000,000,000, and an input has ten of them. Which representation of the counts is appropriate?","options":["An int array of 1,000,000,001 slots.","A hash map keyed by identifier.","A boolean array of 26 slots.","A list sorted by identifier with linear search."],"answer":1,"explain":"The range is huge compared with the number of keys that occur, so memory should depend on the keys present. A direct table fits only a compact promised range."}
```

```quiz
{"id":"hm-rev-bijection","q":"Isomorphic strings are checked with only a map from characters of the first string to characters of the second. Which input does it wrongly accept?","options":["s = \"abab\", t = \"cdcd\".","s = \"ab\", t = \"cc\".","s = \"aa\", t = \"cd\".","s = \"a\", t = \"c\"."],"answer":1,"explain":"In ab versus cc, a maps to c and b maps to c, each consistently, so a forward map accepts it. A backward map notices that c is already taken by a."}
```

```quiz
{"id":"hm-rev-scopes","q":"A Sudoku validity check keeps one HashSet of digits for the whole board and rejects a repeat. What is wrong with it?","options":["It is too slow.","It rejects legal boards, since the same digit may appear in different rows, columns and boxes.","It accepts boards with two equal digits in a row.","It cannot read the dots."],"answer":1,"explain":"Uniqueness is required inside each row, column and box, not across the whole board. One set per scope is needed."}
```
