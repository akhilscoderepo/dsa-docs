<!-- section: orientation -->
## Orientation

A bank report ranks accounts by balance, and a debtor appears above a customer who owes nothing. A support desk serves a ticket from the evening before a ticket from the morning, although both have the same priority. A scoreboard shows the second-highest score as the third-highest. Each failure comes from the same step. The program asked a sort to put items in order, and the rule that decides which of two items goes first was incomplete. This chapter answers two questions. What must that rule promise, and which later decision does the sorted order make safe?

### Prerequisites

You should know Java arrays and loops, the cost words of Chapter 00, and the string scans of Chapter 03. The exercise on dictionary words uses `HashSet` from Chapter 04, and the combination lesson uses `HashMap`. The chapter introduces `Arrays.sort`, `Comparator`, `record` and a sweep over sorted data. Binary search, two pointers and intervals come in later chapters, so no exercise depends on them.

### The Eight Lessons

Each lesson fixes one decision about order and ends with a rule for when that decision is enough.

- **Compare Two Values Safely** shows why subtraction fails and what a comparison result may look like.
- **Sort A Primitive Array** sorts in place, sorts a copy, and sorts a range.
- **Write A Valid Comparator** lists the three properties that every comparator needs.
- **Sort Objects By Several Fields** moves whole items and states which field breaks a tie.
- **Keep Equal Items In Order** separates sorts that keep input order from sorts that do not.
- **Sweep A Sorted Array** replaces a repeated search by one summary that moves along the array.
- **Remove Duplicates After Sorting** turns equal values into runs and emits one entry for each run.
- **Scan The Sorted Array** counts changes between neighbors to answer a rank question.

### The Combination Lesson

One lesson joins this chapter with strings and maps. It opens with a word tool that compares every pair.

- **Group Strings By Sorted Letters** names each word by its sorted letters and collects the words with equal names.

### How To Work Through Each Lesson

Every part of a lesson carries a label, so you always know where you are. A lesson opens with a failing case, and a prediction prompt asks you to guess the cost or the cause before the answer shows. A trace lets you step through the algorithm and watch the state change. A lesson closes with four exercises, and each has a hidden hint and a hidden solution. The exercise roles are Basic, Variation, Edge Cases and Pattern Recognition, and the change grows with each role. An exercise marked Author exercise was written for this course. An exercise with a LeetCode number follows that problem with its own examples, and its text states any rule that it changes. Each exercise lists its prerequisites and ends with a line that says what is different from the exercise before it. A false friend, a term that appears in every lesson, is a look-alike that seems to fit a problem and fails on it. Write your own attempt before you open a hint or a solution.

### What You Can Do After This Chapter

You can write a comparator that stays correct on extreme values and on ties, and you can test it against the three properties. You can say whether a method may sort the caller's array or must sort a copy. You can state the tie rule of any sort in one sentence and choose between a stable sort and an explicit index key. You can recognize the problems where one pass over sorted data, with one small summary, finishes the work. You can also name the inputs that break sorting code: an overflowing difference, a comparator that never returns zero, an array that is too short for a fixed index, and a last run that no later value closes.
