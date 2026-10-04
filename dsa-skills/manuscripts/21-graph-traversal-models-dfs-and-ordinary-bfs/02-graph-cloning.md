<!-- lesson-kind: standard -->
<!-- lesson-id: graph-cloning -->
## Graph Cloning

<!-- stage: context -->
### The Corkboard Of Pell Street

The claims office on Pell Street keeps its open cases on a big corkboard. Every case is an index card, and a red thread joins two cards whenever the cases touch each other: the same address, the same witness, the same broken pipe. By March the board looks like a bowl of noodles. Threads loop back to cards already visited, one card has a thread tied to itself because a claimant filed twice, and two different cards both say "Smith" in the corner.

The new branch across town needs its own board, an exact duplicate, and the manager hands Odile a stack of blank cards and a spool of red thread. She may copy any card she can reach by following threads from the top card. She may not move or cut anything on the original, and the finished copy must not share a single card or thread with it. Odile suspects that the hard part will not be writing cards. It will be knowing, every time a thread leads somewhere, whether she has already made the copy of that card.

<!-- stage: naive -->
### Search The Pairs List

The direct method keeps two lists side by side. One holds the original cards found so far, and the other holds their copies in the same positions. Odile works down the first list. For each thread leaving a card, she searches the originals list from the top for the card at the other end, comparing by identity and not by what is written on it. If the card is found, its copy is already in the matching slot of the second list. If it is not found, she adds the card to both lists and makes a blank copy.

```java
static Node copyBoard(Node top) {
    List<Node> originals = new ArrayList<>();
    List<Node> copies = new ArrayList<>();
    originals.add(top);
    copies.add(new Node(top.val));
    for (int i = 0; i < originals.size(); i++) {
        Node card = originals.get(i);
        for (Node other : card.neighbors) {
            int at = -1;
            for (int j = 0; j < originals.size(); j++) {
                if (originals.get(j) == other) { at = j; break; }
            }
            if (at < 0) {
                originals.add(other);
                copies.add(new Node(other.val));
                at = originals.size() - 1;
            }
            copies.get(i).neighbors.add(copies.get(at));
        }
    }
    return copies.get(0);
}
```

The method is correct for any shape, including loops and a card tied to itself, because the search by identity always finds a card that was already met. It needs a top card to start from.

<!-- stage: bottleneck -->
### Every Thread Triggers A Full Search

Each thread end costs a scan of the originals list, and that list can grow to V cards, so one lookup is O(V). A board has two ends per thread, which means 2E lookups, and the whole copy costs O(V * E). With ten thousand cards and thirty thousand threads that is sixty thousand lookups, each scanning up to ten thousand cards, so roughly six hundred million identity comparisons for a job that needed to touch every card and thread once.

The waste is that the question "have I already copied this card" is answered by searching, when the card itself could point to the answer. Comparing by what is written on the card is not an escape either. Two cards that both say "Smith" are different cases, so any shortcut that looks cards up by their text would quietly glue them together. A faster arrangement must find the copy of a card in constant expected time, and it must key that search on the card as an object.

<!-- stage: insight -->
### One Copy For Each Card

Replace the two parallel lists with a single **identity map**: a hash table whose key is the original card as an object and whose value is its copy. A lookup is then one hash probe instead of a scan, so asking whether a card has been copied costs O(1) on average. The key must be the object itself, never its label, because identity is the only thing that tells two "Smith" cards apart.

Copying a card is done by a **clone** step with a fixed order. Look the card up, and if its copy exists, return it. Otherwise make the blank copy, record it in the map at once, and only then walk the threads of the original. The record must come first. A thread that loops back to this card, or a card tied to itself, will ask for the copy again before the walk has finished, and the entry already in the map is what ends that regress.

The last part is the **wiring**: for each thread leaving the original card, the copy of the card at the other end is fetched, or created by the same step, and attached to the copy of this card. Wiring never touches the original, and it only ever connects copies to copies. Because every original card has exactly one entry, every thread becomes exactly one copied thread and no copy is shared.

The invariant is that the map holds exactly one copy for each original card discovered so far, and every neighbor of a finished copy is a copy taken from the map.

<!-- names: identity map, clone, wiring -->

<!-- stage: variables -->
### Map, Twin And Cursor

The parameter `cur` is the original card being copied right now, and `nb` is the card at the far end of one of its threads. The map `twin` sends each discovered original to its copy, and `t` is the copy of `cur`, which is stored in `twin` before the loop over `cur.neighbors` begins. The value returned by the recursive call for `nb` is always some entry of `twin`, either found or newly made. A counter of created copies is not needed in the code, since it always equals the size of `twin`, but it is the number the trace follows.

<!-- stage: trace -->
### Four Cards With A Triangle

The first trace copies a board of four cards. Cards 0, 1 and 2 form a triangle by threads, and card 3 hangs off card 2. Each step is one call of the copy step, shown in the order the calls happen, and the cell names the card the call asks about. The count `copies` is the number of copies made so far, and it ends at 4, the number of cards. Calls that find their card already in the map return at once, and those are exactly the calls that would have looped forever without the early record.

@@TRACE1@@

The second trace is the false friend. It files three cards in discovery order, where cards a and b both carry the label 7 and card c carries 5. The pointer `i` marks the card just discovered. The column `by_label` is how many entries a map keyed by label would hold, and `by_object` is the size of the identity map. They agree until the second card with label 7 arrives, and from then on the label-keyed map has lost a card.

@@TRACE2@@

<!-- stage: code -->
### Copy Through The Map

```java
final class Board {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node cloneGraph(Node start) {
        if (start == null) return null;
        return visit(start, new HashMap<>());
    }

    private static Node visit(Node cur, Map<Node, Node> twin) {
        Node found = twin.get(cur);
        if (found != null) return found;
        Node t = new Node(cur.val);
        twin.put(cur, t);
        for (Node nb : cur.neighbors) t.neighbors.add(visit(nb, twin));
        return t;
    }
}
```

Each card is created once and each thread end is wired once, so the time is O(V + E) with O(V) for the map and for the recursion stack. The `twin.put` placed before the loop is the whole point of the method. A long chain of cards makes the recursion V levels deep, which is the reason to prefer a queue when V can reach the hundreds of thousands.

<!-- stage: applicability -->
### Copying Anything With Loops

Use this pattern whenever a reachable web of objects must be duplicated and the duplicate has to keep the same shape: a linked list with random pointers, a network of settings that refer to each other, a game world whose rooms have doors leading back. The cue is that the thing has cycles or shared parts, so a plain recursive copy would either never stop or would copy a shared part twice. The invariant to protect is one map entry per original object, written before that object's neighbors are visited.

The nearest false friend is cloning by value. If the map is keyed by a label, two distinct objects with equal labels collapse into one copy, and the duplicate has fewer nodes than the original. A second false friend is the tree copy, which recurses on children without any map. It is perfect for a tree and loops forever, or doubles shared nodes, on a graph.

Do not use it when the structure is guaranteed to be a tree or a plain list, where the map is wasted memory, and do not expect it to copy what cannot be reached from the start node. In Java the hazard is the key type. If `Node` overrides `equals` and `hashCode` by its value, a `HashMap` merges distinct cards, so use the default object identity or an `IdentityHashMap`, and keep a null start from reaching `cur.neighbors`.

<!-- stage: exercises -->
### Exercises

#### [Build] Clone One Edge (Author exercise)
<!-- id: gt-clone-one-edge -->

**Prerequisites.** The copy-through-a-map step, and the idea that a thread joins two cards.

**Problem.** A board has `n` cards numbered `0` to `n - 1`, where `n` is 1 or 2. When `n` is 2, one undirected thread joins card 0 and card 1, and when `n` is 1 there is no thread. Each card is a node object with its number as `val` and a list of neighbors. Copy the board starting from card 0, and return for each number the numbers of its copy's neighbors, in order. The copies must be new objects that the original board does not contain.

**Constraints.** n is 1 or 2, there is at most one edge, it is never a self loop, and the edge may be written `[0,1]` or `[1,0]`.

**Example 1.** Input `n = 2, edges = [[0,1]]`, output `[[1],[0]]`.

**Example 2.** Input `n = 1, edges = []`, output `[[]]`.

**Hint.** The copy of card 0 needs the copy of card 1 to point at, and the copy of card 1 needs the copy of card 0. Which of them can exist first?

**Changed decision.** Both copies are created before either copied thread is attached, so each end has something to point at.

#### [Vary] Clone A Cycle (Author exercise)

<!-- id: gt-clone-a-cycle -->

**Prerequisites.** The Clone One Edge rung.

**Problem.** The threads are now one-way, so the pair `[u, v]` is a pointer from card `u` to card `v`, and the board may contain cycles of any length. Copy only the cards reachable from card 0 by following pointers. Return a list of `n` lists in which the entry for card `v` is the numbers of its copy's neighbors in the order the pointers arrived, and an empty list for every card that is not reachable from card 0.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, no pair repeats, and a card may point at itself or back at a card above it.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[2,0],[3,0]]`, output `[[1],[2],[0],[]]`.

**Example 2.** Input `n = 5, edges = [[0,2],[2,4],[4,2],[1,0]]`, output `[[2],[],[4],[],[2]]`.

**Hint.** When the walk comes back around a cycle to a card whose copy is half finished, what must the map already contain?

**Changed decision.** The copy of a card is placed in the map before its pointers are followed, so a pointer that returns to it finds the half finished copy.

#### [Boundary] Null And Self-Loop (Author exercise)
<!-- id: gt-null-and-self-loop -->

**Prerequisites.** The Clone A Cycle rung.

**Problem.** The board arrives as an adjacency array `adj`, where `adj[v]` lists the numbers that card `v` points at, in order, and a card may list itself. Build the node objects, copy the board from card 0, and return the neighbor numbers of the copies as lists indexed by card. When `adj` is empty there is no top card at all and the answer is `null`. A card with no pointers must come back with an empty list, not with a missing one, and a card that points at itself must have a copy that points at itself and not at the original.

**Constraints.** 0 <= adj.length <= 60, every card is reachable from card 0, no list repeats a number, and every number is a valid card.

**Example 1.** Input `adj = []`, output `null`.

**Example 2.** Input `adj = [[1,0],[1]]`, output `[[1,0],[1]]`.

**Hint.** What should the method do before it touches the top card, and what must the copy of a self-pointing card find in the map?

**Changed decision.** Absence is answered before any traversal, and a self pointer is wired to the copy itself through the same map lookup as any other pointer.

#### [Recognize] Clone Graph (LeetCode 133)
<!-- id: gt-clone-graph -->

**Prerequisites.** The Null And Self-Loop rung.

**Problem.** A connected undirected graph has `n` nodes numbered `0` to `n - 1`, given as `edges`. Each node is an object with an `int val` equal to its number and a list of neighbors, filled in the order the edges arrived, with both ends of an edge receiving an entry. Return a deep copy, starting from node 0, and report it as the neighbor numbers of each copied node in order. (This chapter numbers nodes from 0, where the original statement starts at 1.)

**Constraints.** 1 <= n <= 100, the graph is connected, there are no repeated edges and no self loops.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[2,3],[3,0]]`, output `[[1,3],[0,2],[1,3],[2,0]]`.

**Example 2.** Input `n = 3, edges = [[2,0],[0,1],[1,2]]`, output `[[2,1],[2,0],[0,1]]`.

**Hint.** Every neighbor of a copy must be a copy, and nothing ties a node to its copy except one map entry per original node.

**Changed decision.** A queue visits every reachable node once, and each neighbor of a copy is fetched from the map, which makes the copy share nothing with the original.
