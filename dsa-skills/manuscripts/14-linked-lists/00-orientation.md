<!-- section: orientation -->
## Orientation

A music player deletes the first song of a playlist, and the song stays. An undo history loses every step after the third. A file browser walks down through the open folders in the right order and walks back up in the wrong one. Each program stores items in a linked list, and each bug comes from one overwritten reference. This chapter shows how to change the references of a list without losing a node, and how a few patterns with two references answer most list questions in one pass.

### Prerequisites

You should know loops, arrays and the cost words from Chapter 00. Chapter 04 introduced hash maps, which the last lesson uses. Chapter 11 introduced stacks, which one exercise in the last core lesson uses. Each lesson defines its own terms the first time they matter. Code samples assume `import java.util.*;` and a recent JDK, and every list node is a small class with a `val` field and a `next` field.

### The Ten Lessons

Each lesson adds one rule about which references to keep before a link changes.

- **Follow References Through A List** shows how a walk reaches nodes, why a lost reference deletes a node, and why saving the successor comes first.
- **Reverse A List In One Pass** turns every link around with three references.
- **Reverse Blocks Inside A List** reverses a range or every group of `k` nodes and checks that a group exists before it writes.
- **Merge Two Sorted Lists** joins two lists by taking the smaller front node each time.
- **Use A Dummy Node At The Head** removes the special case for the first node.
- **Find Where A Cycle Starts** detects a cycle with two speeds and names its first node.
- **Find Where Two Lists Meet** lines up two lists that share an ending.
- **Find The Middle Node** reaches the center in one pass.
- **Find The Kth Node From The End** keeps a fixed gap between two references.
- **Flatten Child Lists Into One List** moves nested lists into a doubly linked list with both link directions correct.

### The Combination Lesson

One lesson joins the list lessons with the hash map lessons of Chapter 04.

- **Copy A List With Random Links** pairs each node with its copy in a map, so every link of the copy can be wired by lookup.

### How To Work Through Each Lesson

Each lesson begins with a program that fails or slows down on a real input and then shows a plain version that works but costs too much. A prediction question follows, and you commit to an answer before the explanation opens. The remaining parts give the rule, the state, a step-by-step trace, the code and a check of when the method does not apply. The exercises climb from a basic version to a full interview problem. Each exercise has a role in brackets, either Build, Vary, Boundary or Recognize, and the list of exercises names the role first. Each exercise also lists a Changed decision, which names the one choice that differs from the exercise before it, and the tag Author exercise marks a problem written for this chapter. Try the hint before you read a solution.

### What You Can Do After This Chapter

You can say which reference holds each part of a list at every statement of a method, and you can order the writes so no node becomes unreachable. You can choose between a dummy node, a fixed gap and two speeds from the wording of a problem. You can read a list problem and name its edge cases before you code: the empty list, the one-node list, the head that changes and the end that is `null`.

### What Later Chapters Reuse

Three ideas carry forward.

- **Save before you overwrite** returns whenever a later structure changes a link that is the only path to other data.
- **Two references with a rule** returns whenever a later problem needs a position relative to the end or a repeat in a walk.
- **One owner for the head** returns whenever a method can replace the first element of a structure and must return the right one.
