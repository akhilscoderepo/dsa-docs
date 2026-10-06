<!-- section: orientation -->
## Orientation

A cleanup tool deletes a folder before the files inside it, and the system refuses. A formatter that reads a long chain of nested expressions stops with a stack overflow. A validator re-measures the same subtrees at every level and slows down on large inputs. Each program walks a tree, and each failure comes from one choice: when to act on a node, and what to remember while the walk goes down and comes back. This chapter shows how a depth-first walk keeps that state, and how small returned values let a single pass answer questions that look like they need many passes.

### Prerequisites

You should know loops, recursion at the level of a factorial method, and the cost words from Chapter 00. Chapter 04 introduced hash maps, which the rebuild lesson uses for lookups. Chapter 11 introduced stacks, which the lesson on walking without recursion uses as a `Deque`. Each lesson defines its own terms when they first matter. Two words recur at the end of each lesson. An invariant is a sentence that stays true after every step of a method. A false friend is a method or idea that looks right and gives a wrong answer in some case. Code samples assume `import java.util.*;` and a recent JDK, and a binary node is a small class with `val`, `left` and `right` fields.

### The Nine Lessons

Each lesson adds one rule about what a call on a node owns and what it hands back.

- **Store A Tree In Node Objects** shows how a node owns its subtree and why `null` is a valid empty subtree.
- **Visit Nodes In Three Orders** moves the action before, between or after the two child calls.
- **Walk A Tree With Your Own Stack** replaces the call stack with a `Deque` so that deep trees fit.
- **Track Depth And Paths Down A Tree** separates facts passed down as arguments from facts returned up.
- **Find The Longest Path In A Tree** returns one branch to the parent and records the best path at the node.
- **Check Balance In One Pass** uses a reserved return value so one call carries a height or a failure.
- **Rebuild A Tree From Two Orders** reads windows of a preorder list and an inorder list.
- **Walk A Tree Without A Stack** borrows an empty right reference to find the way back.
- **Split A Grid Into Four Parts** cuts a square grid only where both values appear.

### The Combination Lesson

One lesson joins four earlier lessons into a single design.

- **Return Results From Subtrees** has each call return a small record that its parent merges, so three facts come out of one walk.
