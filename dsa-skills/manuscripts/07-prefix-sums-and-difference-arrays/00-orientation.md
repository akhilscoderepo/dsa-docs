<!-- section: orientation -->
## Orientation

Many array problems ask the same kind of question over and over: what is the total of this stretch, or of that one, or of every stretch that satisfies some condition. The plain answer walks the stretch each time. This chapter teaches how to pay for the walk once, keep the results in a table, and let every later question reduce to reading a few numbers. It also teaches the opposite direction, where many updates are written as marks at the edges of ranges and the whole array is rebuilt in a single sweep.

### What You Need Before Starting

You should be comfortable with the material of Chapters 00 to 06: reading a contract before coding, looping over arrays and matrices with correct bounds, treating a string as a sequence of characters, using a hash map to count or to remember a position, sorting, and the habit of stating a loop invariant. You should know that Java `int` arithmetic wraps without warning, that `%` can return a negative value, and that `long` is the usual remedy for totals. Sliding windows, trees for changing data and the structures that answer range questions with updates are named here only as later destinations, and no exercise needs them.

### The Eleven Lessons

The first lesson builds the table of running totals with its zero slot, and the second turns it into constant-time questions about any stretch. The third drops the idea of a stretch and asks for everything except one element. The fourth through sixth pair the table with a map so that a question about equal totals, equal balances or equal remainders becomes a lookup. The seventh applies the same ideas to XOR, where the operation is its own undo. The eighth reverses the direction, recording updates as edge marks and rebuilding totals with a sweep. The ninth and tenth lift both ideas from lines to grids. The eleventh brings the map lessons together and shows how the key and the role of the map are chosen.

### How To Work Through A Lesson

Start with the story and try to name which numbers will be needed again and again before the lesson says so. The traces show a concrete input one step at a time, and the text names one step worth studying. Write your answer to each exercise on paper, check the hint only when stuck, and read the solution after you have an invariant. Every solution has Java that is compiled and run in the build against a slower oracle that is obviously correct, and several solutions include a deliberately flawed variant so you can see what the correct version protects against.

### Leaving The Chapter

By the end you should be able to look at a stretch or rectangle question and say whether a table, a table with a map, or a sweep fits, what the empty case contributes, which type holds the totals, and which end of each range is included. You should also be able to say what a table cannot do: it cannot follow changes to the data. The review section checks these habits with short scenarios and is worth repeating after a few days.
