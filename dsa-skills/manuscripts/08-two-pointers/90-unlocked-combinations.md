<!-- section: unlocked-combinations -->
## Unlocked Combinations

Two indexes alone only describe a way of moving. They become a method when something else supplies a reason for the move: sorted order, character rules, or the links in a table. This chapter teaches the three pairings that its prerequisites already allow, and it names three pairings that need material from later chapters.

### Pairings Taught In This Chapter

Sorting with two indexes forms the lesson Find Sums In Sorted Arrays. Sorting creates the order that makes an elimination safe, and the scan uses it. The lesson adds one more idea, a key that carries the original position through the sort, and its exercises report positions of the unsorted array.

Strings with two indexes form the lesson Check Strings From Both Ends. The string supplies indexed characters and rules for which characters count, and the indexes supply the movement. The lesson contrasts a scan that moves inward with a scan that moves in one direction.

Array values read as links, with two speeds, form the lesson Find A Duplicate With Two Speeds. The bounded table supplies the links and the guarantee of a repeat. The two speeds find the entry slot of the loop, which holds a repeated value, without writing to the table.

### Pairings That Wait

Two indexes that bound a window of a sequence belong to the chapter on sliding windows. A window keeps a range that grows and shrinks with a state inside it, and that chapter owns the rule for when the state allows the left end to move. No exercise here assigns those problems.

Two indexes that make a locally best choice belong to the chapter on greedy methods. This chapter proves each move by elimination of indexes, and a greedy argument proves each choice by an exchange of choices. The chapter on greedy methods owns that proof style.

Two pointers on linked nodes belong to the chapter on linked lists. Nodes are objects with references, and the arrays of this chapter are not. The chapter on linked lists owns the list version of the two-speed idea, and it owns the in-place reversal of links.

### What Later Chapters Reuse

Three ideas carry forward.

- **The range between two indexes** returns whenever a later method shrinks a candidate range after each comparison.
- **The kept prefix of a read and write scan** returns when a later method builds an output inside its input.
- **The key that carries a position through a sort** returns when a later method sorts records but must report where they came from.
