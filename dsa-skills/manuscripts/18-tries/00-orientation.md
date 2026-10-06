<!-- section: orientation -->
## Orientation

A search box freezes while the user types, because the program rereads 200,000 product names after every key. A word game takes seconds to answer a pattern with one blank letter. A hashtag splitter builds half a million substrings for one tag. An id checker times out on 100,000 numbers, because it compares every pair. Each program holds a set of strings or numbers that share their first symbols, and each asks a question that depends on those shared symbols. This chapter shows how a prefix tree stores the shared symbols once, so a query reads only its own symbols and never rereads the rest of the data.

### Prerequisites

You should know loops, recursion on a tree and array indexing. Chapter 03 introduced strings and character positions, which every lesson uses. Chapter 04 introduced hash maps and sets, which serve as the baseline that each lesson compares against. Chapter 15 introduced tree nodes and recursive walks, and the wildcard lesson builds on both. The last lesson uses the bitwise exclusive or, and it defines the operation before it uses it. Code samples assume `import java.util.*;` and a recent JDK.

### The Five Lessons

Each lesson adds one rule that turns a repeated scan of the data into a short walk on a tree.

- **Store Words By Shared Prefix** builds the tree and separates a path that exists from a word that ends.
- **Insert And Look Up Words** walks one character at a time with an index and states what an array of 26 children assumes about the input.
- **Match Words With Wildcards** follows one edge at a letter and tries every child at a blank.
- **Cut A String Into Dictionary Words** lists the words that begin at one position and shows why the same position repeats in a plain recursion.
- **Pick The Best XOR Partner** stores integers as bit paths and prefers the opposite edge at each bit.

### The Combination Lesson

One lesson joins this chapter with the string chapter.

- **Look Up Prefixes In A Dictionary** lets a word drive the walk through a tree of roots, so one pass finds the longest matching prefix, the shortest root, the smallest wildcard match or the longest word built from its own prefixes.

### How To Work Through Each Lesson

A lesson starts from a program that slows down or fails on a real input, and then shows a plain version that costs too much. A prediction question follows, and you commit to an answer before the explanation opens. The remaining parts give the rule, the state, a trace, the code and a check of where the method stops fitting. The exercises climb from a basic version to a recognition problem. A role in brackets labels each exercise. Build implements the new idea, Vary changes one decision, Boundary tests an edge case and Recognize applies the idea to a problem that does not name it. The Changed decision line names what differs from the exercise before it, and the tag Author exercise marks a problem written for this chapter. Read the hint before you open a solution.

### What You Can Do After This Chapter

You can tell whether a question about many strings asks for a prefix, a whole word, a pattern or a best match. You can state which character set a node layout assumes, and you can choose between an array and a map. You can list the edge cases before you code: the empty string, a word that is a prefix of another word, a pattern longer than every word and a value with the highest allowed bit set.

### What Later Chapters Reuse

Three ideas carry forward.

- **Walk one edge per symbol** returns wherever a set of sequences shares starting symbols.
- **Read the flag separately from the path** returns wherever a structure must tell a prefix from a complete item.
- **Prefer the greedy edge by weight** returns wherever the highest position in a number or key decides the result.
