<!-- section: orientation -->
## Orientation

A checkout page looks for two items that add up to a gift card balance, and it freezes on a catalog of 100,000 prices because it tests every pair. A cleanup job removes deleted records from an array by shifting the tail after each deletion, and it runs for minutes. A table checker needs the repeated id in a read-only table and cannot write to it or copy it. Each program does too much work or breaks a rule, and in each case two indexes that move through the same array fix it. This chapter answers one question: when can two indexes replace a nested loop, and what must stay true about the range between them?

### Prerequisites

You should know Java arrays, `String` methods such as `charAt`, and the cost words of Chapter 00. The lessons use sorting from Chapter 05 and the idea of a prefix of an array from Chapter 01. The chapter explains `long` sums and the swap of two slots at the point where each first matters. No data structure beyond arrays and strings appears.

### The Seven Lessons

Each lesson fixes one rule for moving two indexes and states what the rule keeps true.

- **Scan From Both Ends** moves the left index or the right index of a sorted array after one comparison.
- **Read Ahead And Write Behind** copies the values that stay to the front of the same array.
- **Split An Array In Two** swaps misplaced values between two regions.
- **Split An Array In Three** adds a middle region and a rule for the value that arrives from the far end.
- **Skip Repeated Values** processes one value of each run and jumps over the rest.
- **Fix Values Then Scan A Pair** fixes the leading values and hands the last two to the pair scan.
- **Follow Values As Indexes** reads each value as the next place to read and finds a repeat with two speeds.

### The Three Combination Lessons

Three lessons join the rules with ideas from earlier chapters.

- **Find Sums In Sorted Arrays** sorts first and carries each value's original position through the sort.
- **Check Strings From Both Ends** applies the scan to text and compares it with a scan that moves one way.
- **Find A Duplicate With Two Speeds** separates what the table contributes from what the two speeds contribute.

### How To Work Through Each Lesson

Each lesson opens with a slow program and asks you to predict its cost before the answer appears. Two traces follow, with both indexes drawn above the array. Four exercises close the lesson, from the basic case to a problem that you must recognize without a hint. The hints and the solutions stay hidden until you open them, so make an attempt first. An exercise marked Author exercise was written for this course. An exercise with a LeetCode number follows that problem, and its text states every rule that it changes.

### What You Can Do After This Chapter

You can state the invariant of a two-index scan before you write the loop. You can decide whether a comparison removes one index with a proof, and you can name the input that breaks the proof: an unsorted array, a pair that pairs a value with itself, a skip that runs before the first match, a sum that leaves the `int` range and a value that is not a legal index. You can also say when a method may write to its input and when it may not.
