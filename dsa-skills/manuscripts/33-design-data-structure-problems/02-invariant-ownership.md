<!-- lesson-kind: standard -->
<!-- lesson-id: invariant-ownership -->
## One Method Repairs Each Link

<!-- stage: context -->
### Why The Tab Count Drifts

A browser-style tab strip keeps at most three tabs open. Its code stores the tabs in a linked list, an id lookup table and a counter named `size`. A user opens a fourth tab, and the strip correctly refuses it with an exception. Later the user closes one tab and tries again, and the strip still says it is full. The list shows two tabs, but the counter shows three.

Nothing crashed, and every method looks reasonable when read alone. The bug sits between the methods. Three fields describe one collection, and the failed call changed one of them before it noticed the problem. This lesson shows how to keep several fields in agreement across every operation, including the operations that fail.

<!-- stage: naive -->
### Editing Every Field Inside Each Operation

The direct approach writes each operation from scratch. Every public method edits the links, the lookup table and the counter itself, in whatever order feels natural. The class below shows the usual result. The class keeps sentinel nodes at both ends of the list, a lookup table `byId` and a counter `size`.

```java
final class NaiveTabs {
    private static final class Node {
        final int id; Node prev, next;
        Node(int id) { this.id = id; }
    }
    private final Node head = new Node(-1), tail = new Node(-1);
    private final java.util.Map<Integer, Node> byId = new java.util.HashMap<>();
    private final int capacity;
    private int size;

    NaiveTabs(int capacity) { this.capacity = capacity; head.next = tail; tail.prev = head; }

    void open(int id) {
        size++;                                   // the counter changes first
        if (size > capacity) throw new IllegalStateException("full");
        Node n = new Node(id);
        byId.put(id, n);
        n.prev = tail.prev; n.next = tail;
        tail.prev.next = n; tail.prev = n;
    }

    void close(int id) {
        Node n = byId.get(id);
        n.prev.next = n.next; n.next.prev = n.prev;
        byId.remove(id);
        size--;
    }
}
```

Each method is short, and each one works when the call succeeds. Opening a fourth tab with capacity three raises the exception, as required. The method has already incremented `size` before it checks the limit.

```predict
The strip holds tabs 4, 7 and 9 with capacity 3. The call open(5) throws. Then close(7) succeeds. What do size and the list say, and does open(5) work now?

After the failed open(5), size is 4 while the list still holds three tabs. After close(7), size is 3 and the list holds two tabs. A second open(5) throws again, because size is already 3 and the increment makes it 4. The counter now disagrees with the list for good.
```

<!-- stage: bottleneck -->
### The Cost Of Scattered Updates

Every operation here runs in O(1) time, so speed is not the problem. The cost is that correctness depends on each method remembering every field. With three fields and two operations, a reader can still check the code by eye. A real class has `open`, `close`, `reopenLast`, `moveToEnd` and `clear`, and each of them must touch the links, the table and the counter in a consistent way.

The number of places that can go wrong grows with the number of operations times the number of fields. A fix in one method does not reach the others, because each carries its own copy of the same edit. The failed call above shows a second cost. A method that changes a field and then discovers a problem has no cheap way back. The caller sees an exception, but the object keeps the half-finished change, and every later call starts from a wrong state.

<!-- stage: insight -->
### One Owner For Each Repair

#### Naming The Facts That Must Agree

The fields of a class encode one structure in several forms. Here the list gives the order, the table gives lookup by id, and `size` gives the count. The class keeps one statement true between calls. The list, the table and the counter describe the same set of tabs, and `size` equals the number of nodes between the sentinels. That statement is the **invariant** of the class, and every operation must leave it true when it returns, whether it succeeded or threw.

#### Giving Each Change One Owner

Instead of letting every public operation edit every field, give each cross-field change exactly one **owner**, which is a private method that performs the whole change. A method named `attach` links a node into the list, adds it to the table and increments `size` in one place. A method named `detach` does the reverse. The public operations never touch those fields directly. They decide what to do and then call the owner. A new operation reuses the owner and cannot forget the counter, because it never writes the counter. When the **repair** of a link or count is wrong, only one method needs a fix.

#### Checking Before Changing Anything

The second half of the idea covers failure. Every rejection happens before the first write. The operation first runs its **precheck**, which reads the state and tests every condition that could make the call illegal. Only after all checks pass does it call the owner. A rejected call then leaves every field exactly as it found it, and no undo code is needed, because nothing was done yet.

<!-- names: owner, repair, precheck -->

<!-- stage: variables -->
### Fields That Describe One Collection

The tab strip has five fields, and the invariant ties four of them together. Each entity below has a single job, and only the owner methods write the first three.

- **head and tail** are sentinel nodes that hold no tab and always exist, so a real node always has a neighbour on each side.
- **byId** maps a tab id to its node, so the lookup table holds exactly the ids that appear in the list.
- **size** counts the real nodes and changes by one inside `attach` and `detach` only.
- **capacity** is the fixed limit and never changes after construction.

The invariant can be checked at any moment between calls by walking the list from `head.next` to `tail`. The number of nodes seen must equal `size` and `byId.size()`.

<!-- stage: trace -->
### Tracing Six Calls On Three Slots

#### The Version With One Owner

Run the script open 4, open 7, open 9, open 5, close 7, open 5 on a strip with capacity 3. The first three calls pass the precheck. Each one calls `attach`, so the list, the table and `size` grow together to three.

The fourth call, open 5, fails the precheck because `size` equals `capacity`. It throws before `attach` runs. The list, the table and `size` keep their values. The call to close 7 reaches `detach`, which unlinks the node, removes id 7 from the table and lowers `size` to two. The last open 5 now passes the precheck and ends with the list 4, 9, 5 and size 3.

```trace
{"cells":[4,7,9,5,7,5],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"list":"[]","size":0,"nodes":0,"result":"start"},"note":"Start: an empty strip with capacity 3. The counter, the list and the table all say empty."},{"at":{"op":0},"vars":{"list":"[4]","size":1,"nodes":1,"result":"ok"},"note":"open 4: the precheck passes and attach links the node, adds the id and raises size to 1."},{"at":{"op":1},"vars":{"list":"[4,7]","size":2,"nodes":2,"result":"ok"},"note":"open 7: the precheck passes and attach links the node, adds the id and raises size to 2."},{"at":{"op":2},"vars":{"list":"[4,7,9]","size":3,"nodes":3,"result":"ok"},"note":"open 9: the precheck passes and attach links the node, adds the id and raises size to 3."},{"at":{"op":3},"vars":{"list":"[4,7,9]","size":3,"nodes":3,"result":"throws"},"note":"open 5: the precheck sees size 3 equals capacity and throws before any write. Every field keeps its value."},{"at":{"op":4},"vars":{"list":"[4,9]","size":2,"nodes":2,"result":"ok"},"note":"close 7: detach unlinks the node, removes the id and lowers size to 2."},{"at":{"op":5},"vars":{"list":"[4,9,5]","size":3,"nodes":3,"result":"ok"},"note":"open 5: the precheck passes and attach links the node, adds the id and raises size to 3."},{"at":{"op":5},"vars":{"list":"[4,9,5]","size":3,"nodes":3,"result":"ok"},"note":"Done. The strip holds 4, 9 and 5, and size, nodes and the table all agree at 3."}]}
```

#### The Version With Scattered Edits

The same script on the naive code shows the drift. The fourth call increments `size` to 4 and then throws, so the list holds three tabs while the counter says four. The call to close 7 lowers the counter to 3 with only two tabs left. The final open 5 increments the counter to 4, exceeds the capacity and throws, although the strip has room. The step notes below show the counter and the real list length side by side.

```trace
{"cells":[4,7,9,5,7,5],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"list":"[]","size":0,"nodes":0,"result":"start"},"note":"Start: an empty strip with capacity 3. The counter, the list and the table all say empty."},{"at":{"op":0},"vars":{"list":"[4]","size":1,"nodes":1,"result":"ok"},"note":"open 4: counter and list both reach 1."},{"at":{"op":1},"vars":{"list":"[4,7]","size":2,"nodes":2,"result":"ok"},"note":"open 7: counter and list both reach 2."},{"at":{"op":2},"vars":{"list":"[4,7,9]","size":3,"nodes":3,"result":"ok"},"note":"open 9: counter and list both reach 3."},{"at":{"op":3},"vars":{"list":"[4,7,9]","size":4,"nodes":3,"result":"throws"},"note":"open 5: the counter rises to 4 first, then the capacity test throws. The list still holds 3 tabs, so the two now disagree."},{"at":{"op":4},"vars":{"list":"[4,9]","size":3,"nodes":2,"result":"ok"},"note":"close 7: the counter drops to 3, but the list holds 2 tabs."},{"at":{"op":5},"vars":{"list":"[4,9]","size":4,"nodes":2,"result":"throws"},"note":"open 5: the counter rises to 4 first, then the capacity test throws. The list still holds 2 tabs, so the two now disagree."},{"at":{"op":5},"vars":{"list":"[4,9]","size":4,"nodes":2,"result":"throws"},"note":"Done. The last open 5 threw although only two tabs are open, because the counter reads 3. The drift is permanent."}]}
```

<!-- stage: code -->
### Implementing The Strip With Two Owners

```java
final class OpenTabs {
    private static final class Node {
        final int id; Node prev, next;
        Node(int id) { this.id = id; }
    }
    private final Node head = new Node(-1), tail = new Node(-1);   // sentinels, never removed
    private final java.util.Map<Integer, Node> byId = new java.util.HashMap<>();
    private final int capacity;
    private int size;

    OpenTabs(int capacity) { this.capacity = capacity; head.next = tail; tail.prev = head; }

    // Owner of every insertion: links, table and count change together here and nowhere else.
    private void attach(Node n) {
        n.prev = tail.prev; n.next = tail;
        tail.prev.next = n; tail.prev = n;
        byId.put(n.id, n);
        size++;
    }

    // Owner of every removal: the mirror of attach.
    private void detach(Node n) {
        n.prev.next = n.next; n.next.prev = n.prev;
        byId.remove(n.id);
        size--;
    }

    void open(int id) {
        if (byId.containsKey(id)) throw new IllegalArgumentException("already open");   // precheck
        if (size == capacity) throw new IllegalStateException("full");                  // precheck
        attach(new Node(id));                                                           // first write
    }

    void close(int id) {
        Node n = byId.get(id);
        if (n == null) throw new IllegalArgumentException("not open");                  // precheck
        detach(n);                                                                      // first write
    }

    int size() { return size; }
}
```

Both public operations follow one shape: test every condition, then make one call to an owner. Each operation runs in O(1) time with O(1) extra space. The only allocation, the `Node` created in `open`, happens after the checks pass, so a rejected call allocates nothing that stays reachable.

<!-- stage: applicability -->
### Applying One Owner Per Field Group

#### Recognizing The Pattern

Look for a class where two or more fields must change together. Typical cases are a list with a size counter, a map next to a list, or an array next to an index table. In each case the class keeps an **invariant**, which is a fact about the fields that must hold whenever no operation is running. Write that fact as one sentence before you write any method.

Then name the private method that owns each change to the fields. The test is simple. Search the class for each field, and every write must sit inside its owner. Each public operation reads the state, checks its conditions and then calls an owner once or a fixed number of times.

#### A False Friend And A Java Hazard

A **false friend** is a technique that looks like the right fix and fails in a quiet way. The nearest one here is a `try` block with a `catch` that undoes the edits after a failure. The undo code is a second copy of the repair, and it must itself run without error. It also misses any field that a later change adds. Checking first is simpler than rolling back.

The Java hazard is the exception thrown halfway through a mutation. Java does not restore fields when an exception leaves a method. Every assignment that ran before the throw stays in place, and an uncaught exception from the middle of a method leaves the object half updated.

Chapter 33 reuses this pattern in the cache lessons, where a map and a list must agree after every call.

<!-- stage: exercises -->
### Exercises

#### [Build] Size Ownership (Author exercise)
<!-- id: ds-size-ownership -->

**Prerequisites.** The owner and precheck idea in this lesson.

**Problem.** Design a bounded sequence of nonnegative `int` values stored in an array of fixed capacity. It has the operations `insertAt(index, v)`, `add(v)` and `removeAt(index)`. Field `size` counts the stored values. Write two private methods, `openGap` and `closeGap`, that shift values and are the only code allowed to write `size`. A rejected call changes nothing. `insertAt` and `add` return `true` on success and `false` when rejected. `removeAt` returns the removed value, or `-1` when rejected.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 1000`, fixed at construction.
- **Values** are `int` in `0..10^6`.
- **Index** for `insertAt` is valid in `0..size`, and for `removeAt` it is valid in `0..size-1`.
- **Rejection** covers an invalid index and a full sequence, and leaves `size` and every stored value unchanged.

**Example 1.** Input capacity 3 and the calls `add(5)`, `add(6)` and `add(7)` return `true`. Then `add(8)`, and output `false` with `size` 3. Then `removeAt(0)` gives output 5 with `size` 2.

**Example 2.** Input the stored values `[5,6]` with capacity 3 and the call `insertAt(1, 9)`, output `[5,9,6]` with `size` 3. Then `removeAt(5)` gives output `-1` and `size` stays 3.

**Hint.** Which two methods move values and therefore know how many values exist afterward? How many writes to `size` should one successful call make?

**Changed decision.** The count moves out of the public operations and into the two shifting helpers, so every successful call changes `size` exactly once.

#### [Vary] Sentinel List Links (Author exercise)
<!-- id: ds-sentinel-links -->

**Prerequisites.** The size-ownership exercise above.

**Problem.** Design a doubly linked list of nonnegative `int` values with a head sentinel and a tail sentinel. Only two private methods may change links: `detach(node)` and `attachAfter(position, node)`. Provide `addFirst`, `addLast`, `removeFirst`, `removeLast`, `remove(node)` and `moveToFront(node)`. The add operations return the new node. The two remove operations that take no node return the removed value, or `-1` on an empty list. Every operation reaches the links only through the two helpers.

**Constraints.** The limits are:
- **Values** are `int` in `0..10^6`, and duplicates are allowed.
- **Length** is at most `10^5` nodes.
- **Node argument** is a node currently in this list, so no check for foreign nodes is needed.
- **Empty list** has `head.next == tail` and `tail.prev == head`.

**Example 1.** Input `addLast(1)`, `addLast(2)` and `addLast(3)`, output the list `[1,2,3]`. Then `moveToFront` on the node of 3 gives output `[3,1,2]`, and `removeLast()` gives output 2.

**Example 2.** Input `removeFirst()` on an empty list, output `-1`, and the sentinels still point at each other.

**Hint.** Which operation is just a detach followed by an attach? Which pointer pairs must change when a node leaves, and which when it enters?

**Changed decision.** The shifting array becomes linked nodes, and every link edit moves into one detach method and one attach method.

#### [Boundary] Failed Mutation (Author exercise)
<!-- id: ds-failed-mutation -->

**Prerequisites.** The two exercises above.

**Problem.** A bounded list stores up to `capacity` nonnegative `int` values in an array and tracks `size` and a counter `modCount` that rises by one on every successful change. The operation `insertAt(index, v)` throws `IndexOutOfBoundsException` when `index < 0` or `index > size`. It throws `IllegalStateException` when the list is full and the index is valid. A thrown call must leave `size`, `modCount` and every array slot exactly as before the call. Implement the operation so that this holds.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 1000`, fixed at construction.
- **Values** are `int` in `0..10^6`.
- **Check order** tests the index first and fullness second.
- **Rejected call** performs no write to `size`, `modCount` or the array.

**Example 1.** Input capacity 2, stored values `[4,5]` and the call `insertAt(0, 9)`, output an `IllegalStateException`. The list still reads `[4,5]`, and `size` and `modCount` keep their values.

**Example 2.** Input capacity 3, stored values `[4,5]` and the call `insertAt(4, 9)`, output an `IndexOutOfBoundsException`, and nothing changes.

**Hint.** What does the method read before it writes anything? Which version of the method increments `size` first, and what does a later `throw` leave behind?

**Changed decision.** The edge case is the rejected call, so every condition moves ahead of the first write.

#### [Recognize] LC 146 LRU Cache (LeetCode 146)
<!-- id: ds-lru-evicted-key -->

**Prerequisites.** All three exercises above.

**Problem.** Design a cache with a fixed `capacity` that maps nonnegative `int` keys to nonnegative `int` values. The operation `get(key)` returns the value and marks the key as most recently used, or returns `-1` when the key is absent. The operation `put(key, value)` stores the pair and marks the key as most recently used. When the key is new and the cache is full, `put` first removes the least recently used key and returns that evicted key. In every other case `put` returns `-1`. All list edits live in two private helpers, `detach` and `attach`. After every call the number of map entries equals the number of list nodes.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 3000`.
- **Keys and values** are `int` in `0..10^5`, so `-1` is never a real key or value.
- **Updating** an existing key never evicts and returns `-1`.
- **Cost** of each operation is O(1) on average.

**Example 1.** Input capacity 3 and the calls `put(5,50)`, `put(6,60)`, `put(7,70)`, `get(5)`, `put(8,80)`, `put(7,71)`, `put(9,90)`, output `-1`, `-1`, `-1`, 50, 6, `-1`, 5.

**Example 2.** Input capacity 1 and the calls `put(1,1)`, `put(2,2)`, `put(2,3)`, `get(1)`, `get(2)`, output `-1`, 1, `-1`, `-1`, 3.

**Hint.** Which fields describe the same set of keys? Which two helpers can be the only code that touches both the list and the map?

**Changed decision.** `put` reports the evicted key instead of returning nothing, and the list and map edits are fenced into two helpers.
