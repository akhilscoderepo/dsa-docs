<!-- section: orientation -->
## Orientation

A paging client calls `hasNext()` twice and then `next()`. The first call quietly advanced the source, so the second `next()` returns the wrong element. The code looked at a value and consumed it in the same step. This chapter teaches APIs that hand out a large or nested value one piece at a time, turn a structure into text and back, and answer questions about an earlier version.

### Prerequisites

You should know stacks, queues, binary trees, tries, prefix sums and binary search. An **iterator** is an object that returns the elements of a source one at a time. A **codec** is a pair of methods, `encode` and `decode`, that convert a value to a string and back. A **version** is a numbered state that a caller may query after later changes. The key words are **observation** (looking at the next value), **availability** (whether a next value exists), **consumption** (moving past it) and **exhaustion** (nothing is left).

### What Each Lesson Protects

Each lesson names one fact that every call must keep true.

- **Iterator Protocols** separates `peek` and `hasNext` from `next`, so looking never moves the source.
- **Nested Iteration** keeps unfinished cursors on a stack or in a queue, so the input is never flattened up front.
- **Structural Codecs** makes every encoding readable in exactly one way, so decoding consumes one representation and nothing more.
- **Version Histories** stores only the changes, so a query at any version reads a sorted list instead of a copy.
- **Query Objects** spend constructor work on an index, so each later query costs far less than a scan.
- **Incremental Trees** update traversal state as the tree changes, so the next insertion or step needs no full rescan.
- **Iterator Traversal State** joins lookahead, run skipping and bidirectional tree walks, so one cursor survives any call order.
- **Codec Structural Traversal** joins tree order, null markers and ownership of children, with length prefixes in one exercise, so decoding mirrors the shape that encoding wrote.

### Reading Order

Every lesson starts with a class that passes short tests and then fails on a longer call sequence. You predict the failure before the reasoning appears. Two traces follow the fields call by call, then Java code and the limits of the idea. The four exercises climb from a basic build to a variation, an edge case and a recognition problem. A **false friend** is a design that passes small tests and breaks the rule the lesson protects. A **transfer problem** is an interview prompt that applies the lesson to a new setting, with review notes before its solution. Solutions check each class against a brute-force **oracle**, a slow but obviously correct version, on random inputs. A LeetCode problem that appears twice carries a changed contract, and its text says what changed.

### What You Can Do After This Chapter

You can state for any iterator whether an exhausted `next()` throws, and you can keep that rule on every path. You can write a codec and argue that two different inputs never share an encoding. You can answer a query at a version before the first update or after the last. Cache design belongs to chapter 33, and concurrent iteration belongs to the separate senior curriculum.
