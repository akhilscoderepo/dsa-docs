<!-- section: orientation -->
## Orientation

A log tool reports that every word occurs once, because it stored each word in a set and never kept a count. A seating checker rejects a legal plan, because it used one set for the whole room. A lookup that should return at once takes a minute, because it scans a list for every request. Each failure has the same root. The program needed one remembered fact about the values it had already read, and it stored the wrong fact or stored it in a structure that cannot answer quickly. This chapter answers one question: which fact must the program keep, and which Java structure returns it in expected constant time?

### Prerequisites

You should know Java loops, arrays and the cost words of Chapter 00. Chapter 03 helps, mainly the table with 26 counters and the scan with an index. The chapter introduces `HashSet`, `HashMap` and `LinkedHashMap`. Sorting arrives in Chapter 05, and two pointers and windows come later, so no exercise depends on them.

### The Seven Lessons

Each lesson stores one kind of fact, and each ends with a rule for when the fact is enough.

- **Check Membership With A Set** stores which values have appeared and drops counts and positions.
- **Count Values With A Map** stores how often each value has appeared.
- **Remember Where A Value Appeared** stores one chosen position for each value.
- **Group Values In A Map** stores the full list of members for each key.
- **Extend Runs With A Set** tests neighbors of a value to find where a block of consecutive numbers begins.
- **Use Records As Keys** builds a key from several fields so that equal keys find one entry.
- **Choose An Array Or A Map** compares the cost of the key range with the cost of hashing.

### The Two Combination Lessons

Two lessons join this chapter with earlier ones. Each opens with the failure that forces the pairing.

- **Strings And Maps** pairs the characters of two strings and keeps the pairing in both directions.
- **Matrices And Sets** keeps one set for each row, column and block of a grid.

### How To Work Through Each Lesson

Every part of a lesson carries a label, so you always know where you are. A lesson opens with a failing case, and a prediction prompt asks you to guess the cause before the answer shows. A trace lets you step through the loop and watch each value change. A lesson closes with four exercises, and each has a hidden hint and a hidden solution. The exercise roles are Basic, Variation, Edge Cases and Pattern Recognition, and the change grows with each role. An exercise marked Author exercise was written for this course, and an exercise with a LeetCode number follows that problem with its own examples, and its text states any rule that it changes. Write your own attempt before you open a hint or a solution.

### What You Can Do After This Chapter

You can say what a key means and what its value means before you declare a map. You can pick between a set, a count, a position and a list for the fact that a question needs. You can explain why an array or a record behaves in a surprising way as a key, and you can decide between a table and a map from the number of possible keys. You can also name the inputs that break map code: an absent key, a negative remainder, a repeated start, a key that changes while stored, and a range that overflows `int`.
