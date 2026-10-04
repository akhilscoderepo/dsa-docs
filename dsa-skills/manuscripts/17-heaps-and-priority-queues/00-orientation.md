<!-- section: orientation -->
## Orientation

Many programs have to answer one recurring question: of the items that are available right now, which one comes first. A sorted array answers it once. A heap answers it again and again while items arrive, leave and change their standing, and it does so by keeping only as much order as that question needs. The Java class `PriorityQueue` is the everyday form of it. This chapter begins with the mechanics of that class and ends with a median that survives a moving window, and in every lesson two questions come back: what exactly does the root promise, and what should happen when the root is no longer true.

### Before You Begin

You should be at ease with arrays and with the sorting and comparator chapter, since every heap in this chapter is steered by a comparator. The chapter on intervals supplies the sorted-by-start view that the final lesson builds on, the hash-map chapter supplies the counting that one exercise needs, and the chapters on queues and on linked lists supply the habit of moving through a structure one entry at a time. A glance at the binary-tree chapter helps with the picture of parents and children in an array, but nothing from it is assumed. Shortest paths on graphs also use a heap, and that composition is named at the end of this chapter and left for a later one.

### The Eight Lessons

The first lesson opens the class: what offer, poll and peek cost, why the array is only partly ordered, and what the queue does when it is empty. The second lesson turns to orientation, that is, how to build a maximum-first queue, how to rank a tuple of fields, and why arithmetic on priorities fails at the edges of the integer range. The third keeps only the best few items of a stream with a small heap. The fourth merges several sorted sources by holding one front entry per source. The fifth schedules work that becomes available over time, by admitting released tasks into a ready heap. The sixth teaches how to cancel or revise an entry without searching for it, by leaving stale entries and dropping them when they reach the root. The seventh keeps a median for a growing stream with two heaps. The eighth combines a sort by start time with a heap of end times to count the rooms, stages or groups that overlapping intervals demand.

### How To Work Through A Lesson

A lesson starts with a scene and a direct method, and then it shows what that method repeats. Before you read the insight, say aloud what extreme the heap would have to expose and which items it would have to hold. The traces print the heap or the frontier after each step, and the text points to the single step that repays a second look. Try each exercise before opening its hint, and for each one write down the comparator, the size of the heap that you expect, and the condition under which a root is discarded. The Java in every solution is compiled and run against a slower method that tries everything, so a mismatch would be reported as a failure and not left for you to find.

### Leaving The Chapter

You should be able to explain why iterating a queue does not give sorted output, why a comparator should compare and never subtract, why a top-k heap is a min-heap, and why a merge needs one entry per source and not one per value. You should also be able to say why tied arrivals are all admitted before one task is chosen, why a stale root is cleaned in a loop, and why the logical size of a structure with delayed deletion is kept apart from the size of its heap. The review that follows asks short questions without naming the technique, and it is worth repeating after a few days.
