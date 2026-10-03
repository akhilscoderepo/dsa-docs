<!-- section: orientation -->
## Orientation

This chapter teaches the family of problems that ask for the best contiguous range of an array or string, where "best" depends on a condition the range must satisfy. It assumes you can write a nested loop over an array, read a Big-O bound, and count items with an array or a hash map. Chapter 00 supplied the habit of reading constraints first, and Chapter 08 showed two indices moving through a sequence under a rule that makes each move safe. A sliding window keeps that habit and adds one more idea: the range between the two indices carries a summary that is updated incrementally instead of being recomputed.

### What You Need Before Starting

Before you open any lesson, confirm three facts about the problem in front of you. First, the answer concerns contiguous ranges, not subsequences or arbitrary subsets. Second, you know whether the input may be modified, and whether the lengths and values can overflow an `int`. Third, you can say what the range summarizes: a sum, a count, a table of symbol counts, or a number of violations. If you cannot name the summary, a window is not yet the right tool, and the rest of this chapter will not rescue the choice.

### The Nine Shapes

The chapter separates nine window shapes because they differ in what the window summarizes and in when it is allowed to shrink. A fixed-size aggregate window never changes length and carries one number. A fixed frequency window also keeps its length but carries a table of counts. The longest-valid window shrinks only after validity breaks, and the minimum-cover window does the opposite and shrinks while validity holds. The at-most-K distinct window limits variety, the exactly-K lesson turns an unmanageable exact count into a difference of two manageable ones, and the replacement-budget window prices a stretch by its length minus its most common symbol. The counting lesson adds a whole block of valid ranges at once, and the policy lesson asks when a window may give up being valid and keep only its length.

Treating all of these as one technique is the usual reason a learner can follow a solution and still fail to produce one. Each lesson therefore names its recognition cue, the invariant that makes the move safe, the false friend that looks similar, and a Java hazard, and each has its own ladder of four or five exercises.

### How To Work Through A Lesson

Read the story and the brute-force code first, and try to predict where the time goes before you read the bottleneck section. Step through the trace with the Next button and say aloud what each pointer move does. Then open the exercises in order. Write your own solution in the notes box before you reveal the hint, and reveal the solution only after you have run your own version against both examples. The status buttons record what you could do alone, what needed a hint, and what you could not do, and the My Notes section at the end of the page is where recognition cues you missed belong.

### What Is Deliberately Left For Later

A window that must report the maximum or minimum value inside every window cannot be maintained with a table of counts, because a table has no order. That composition needs the ordered-candidate structure taught in the chapter on deques and monotonic queues, and this chapter only names it. Prefix sums with a hash map solve the neighboring problems where values may be negative, and they are taught in Chapter 07 rather than repeated here.

### Java Habits Used Throughout

Keep indices, never substrings, inside the loop and build the output once. Use a primitive count array only when the contract states the character domain, and say which domain. Use `long` for totals that can exceed two billion, as the counting lessons do. Remove a map key when its count reaches zero, so that its size means what you think it means.
