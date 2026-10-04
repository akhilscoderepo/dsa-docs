<!-- section: orientation -->
## Orientation

A sign-up form counts the words in a bio and reports three where the user wrote two, because the user typed a double space. A product search treats `ab-12` and `AB 12` as different items. A password check times out on a pasted string of one repeated character. The three failures share one cause. Each program treated a string as one value, when the string is an ordered sequence of characters that a loop must read with a rule. This chapter answers one question: what must a loop remember about the characters it has read, so that it stays correct and fast on long text?

### Prerequisites

You should know Java loops, arrays and the cost vocabulary of Chapter 00. Chapter 01 helps, especially the read index and the write index. The chapter needs no other data structure, except that one exercise in lesson 02 stores words in an `ArrayList<String>`, Java's growable list. It does not use maps, two pointers or windows, because later chapters own them.

### What The Seven Lessons Cover

Each lesson adds one habit for reading text, together with the invariant that keeps it correct.

- **Scan A String By Index** reads each character once and keeps a small running answer.
- **Build Strings With StringBuilder** appends to one buffer and gives each separator an owner.
- **Parse One Character At A Time** keeps a state variable that decides which character may come next.
- **Normalize Before Comparing** converts equivalent inputs to one standard form.
- **Count Letters In An Array** gives each of 26 letters its own array slot.
- **Compress Runs Of Characters** closes each block of equal neighbors at its boundary.
- **Expand Palindromes From The Center** grows a symmetric substring outward from a fixed middle.

### How To Work Through Each Lesson

Every part of a lesson carries a label, so you always see where you are. A lesson opens with a failing case, and a prediction prompt asks you to name the cause before the answer appears. A trace lets you step through the loop and watch its values change. Each lesson closes with four exercises, and each has a hidden hint and a hidden solution. The exercise roles are Basic, Variation, Edge Cases and Pattern Recognition, in rising order of change. An exercise marked Author exercise was written for this course, and an exercise with a LeetCode number follows that problem with its own examples. Write your own attempt before you open a hint or a solution.

### What You Can Do After This Chapter

You can pick the right tool for building text, a loop or a builder, and you can explain why repeated `+` and `insert(0, ...)` cost quadratic time. You can write a small parser from a list of states, and you can state the equality rule behind a normalizer before you code it. You can also say which inputs break string code: the empty string, a single character, text made only of separators, a final run, and a character outside the stated alphabet.
