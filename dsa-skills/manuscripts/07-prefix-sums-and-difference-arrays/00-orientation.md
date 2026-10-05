<!-- section: orientation -->
## Orientation

A sales dashboard prints revenue to date next to every day, and the job adds up all earlier days again for each row. A booking screen adds seats to every leg between two stops, and a request that spans the chain touches every leg. A log tool counts the windows of minutes whose request total hits a quota, and it checks every pair of start and end. Each program repeats work that an earlier step already did. This chapter answers one question: when can a stored running value replace a loop over a range, and what must the program remember so that the replacement stays correct?

### Prerequisites

You should know Java arrays and loops, the cost words of Chapter 00, and the `HashMap` methods of Chapter 04, which the lessons on counting and on spans use. The chapter explains `long` sums, `Math.floorMod` and the XOR operator at the point where each one first matters. No sorting or searching is needed.

### The Ten Lessons

Each lesson fixes one stored quantity and one question that the quantity answers.

- **Build Running Totals** stores the sum of everything before a position, with an entry for zero values.
- **Answer Range Sum Queries** subtracts two stored totals to read any window in constant time.
- **Combine Totals From Both Sides** multiplies a left product and a right product, with no division.
- **Count Subarrays With A Target Sum** counts earlier boundaries that match, using a frequency map.
- **Find The Longest Balanced Span** keeps the earliest index of each balance.
- **Group Prefixes By Remainder** keys the map by a remainder that stays inside the valid range for negative totals.
- **Use XOR As A Running Total** shows that an operation which undoes itself also gives constant time windows.
- **Add To Ranges In Constant Time** records where a value starts and stops and reads all totals once.
- **Sum A Rectangle In Constant Time** extends the stored totals from a line to a grid.
- **Add To Rectangles In Constant Time** writes four signed values for each rectangle and reads the grid once.

### The Combination Lesson

One lesson joins the stored totals with the maps of Chapter 04. **Count And Measure Spans With Maps** opens with three reports that share one map and give three kinds of wrong answer. It then separates the two choices that every such solution makes, the meaning of the key and the meaning of the value.

### How To Work Through Each Lesson

Each lesson opens with a slow program and a short prediction that asks you to guess its cost before the answer appears. Two traces show the stored values as they change, and four exercises close the lesson. The exercises start from the basic case and end with a problem that you must recognize without a hint. Hints and solutions stay hidden until you open them, so make an attempt first. An exercise labeled Author exercise was written for this course. An exercise with a LeetCode number follows that problem, and its text states every rule that it changes.

### What You Can Do After This Chapter

You can state what a stored array holds before you write the loop that fills it, and you can write the formula that reads a window from it. You can choose between a frequency map and an earliest-index map from the wording of a question. You can name the inputs that break these methods: an empty array, a window that starts at index 0, a total that exceeds the `int` range, a negative remainder, a zero in a product, a range that ends at the last index and a rectangle in the last row or column.
