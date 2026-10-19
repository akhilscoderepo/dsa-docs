<!-- lesson-kind: standard -->
<!-- lesson-id: hierarchical-namespaces -->
## Resolve Paths In A Tree

<!-- stage: context -->
### A Setting Stored Under A Missing Folder

A configuration service stores values under paths such as `/app/db/host`. A client writes `/app/db/host` before anyone has created `/app/db`. The store accepts the write, because it only checks that the full path is new. Now one value sits under a parent that does not exist.

Listing `/app` shows nothing, since no entry named `db` exists. Deleting `/app` later leaves the value behind, because nothing links it to its parent. A search finds it, and a walk from the top never reaches it.

This lesson asks how a service resolves a path so that every stored value has exactly one parent that exists, and how it keeps that true across thousands of calls. The same question appears in file systems, in routing tables and in database catalogs.

<!-- stage: naive -->
### Storing Every Path As One String

The direct design keeps one hash map from the full path string to its value. To create a path, it cuts the string at the last slash and asks whether that prefix is in the map. To list a directory, it scans every key and keeps those that start with the directory string.

```java
import java.util.*;

final class NaivePaths {
    private final Map<String, Integer> value = new HashMap<>();

    boolean createPath(String path, int v) {
        int cut = path.lastIndexOf('/');
        String parent = path.substring(0, cut);               // "" stands for the top
        if (!parent.isEmpty() && !value.containsKey(parent)) return false;
        return value.putIfAbsent(path, v) == null;
    }

    List<String> list(String dir) {
        List<String> out = new ArrayList<>();
        for (String key : value.keySet()) {                   // scans every stored path
            if (key.startsWith(dir)) out.add(key);
        }
        Collections.sort(out);
        return out;
    }
}
```

Creation works for clean input. The listing is wrong, and it is also slow.

```predict
The map holds the paths /a, /ab and /a/x. What does list("/a") return, and what should it return as the children of /a?

The call returns /a, /ab and /a/x, because each string starts with the characters of "/a". Only /a/x is a child of /a. The path /ab is a sibling, and /a is the directory itself. A string prefix is not a parent relation, and the scan also touches every stored path.
```

<!-- stage: bottleneck -->
### Strings Do Not Know Their Parents

The listing call reads all n stored paths, so one call costs O(n) even when the directory has two children. A service with 10^5 paths and 10^5 list calls does 10^10 string comparisons. The prefix test is also wrong, which makes the cost the smaller problem.

The map has no structure for the parent relation. It rediscovers the relation from string text on every call, and the text rules are easy to get wrong. A path such as `//a` or `/a/` produces a different key than `/a`, so the same directory can exist twice under two spellings.

Deleting or moving a directory has the same weakness. The code would have to find every key that belongs below it by scanning, and one missed key is an orphan. The structure must store the parent relation itself, and it must read each path by one fixed rule.

<!-- stage: insight -->
### Split The Path, Then Walk A Tree

Cut each path string into **components**, which are the names between the separators. The path `/a/b` has the components `a` and `b`. The top of the tree is the root, and it has zero components.

#### Normalize Once At The Entry

A service must **normalize** each incoming string before it does anything else. Normalizing applies a stated policy that turns many spellings of one location into one list of components. A policy says whether repeated separators collapse, whether a trailing separator counts and which names are illegal. After this step no other code reads raw path text.

#### Each Node Owns Its Children

Store a node for every location. A node holds its value and a map from a child name to the child node. A node is reachable only through its parent, so a node cannot exist without a parent that exists. Resolving a path means starting at the root and following one map lookup per component. The cost is O(d) lookups for a path of depth d.

#### Count Or Remove A Whole Subtree

A **subtree** is a node, its children and everything below them. Listing a directory reads one map, and a sorted map yields the names in lexicographic order. Counting or removing a subtree starts at one node and never scans unrelated paths. Extra data such as a count per node is a derived value. It changes in the same call that changes the tree.

The invariant is that every stored node is reachable from the root by its list of components, and each node has exactly one parent.

<!-- names: component, normalize, subtree -->

<!-- stage: variables -->
### State That A Call Reads And Writes

A path service keeps four kinds of state, and only one of them is authoritative.

- **Node** is the authoritative entity, holding a value or content and a map from child name to child node.
- **Components** is the list of names that the entry step produces from the raw string, and it exists only during one call.
- **Cursor** is the node that the walk has reached so far, starting at the root.
- **Derived count** is an optional number per node, such as the nodes below it, and it changes only in the same call as the tree.

A call first normalizes the string and then walks with the cursor. It validates every precondition during the walk and writes only after the walk has succeeded.

<!-- stage: trace -->
### Following Creates And Spellings

#### Creating Under A Parent That Must Exist

The first trace runs six calls on a small tree. The pointer `call` marks the latest call, and the tree column lists the stored paths with their values.

```trace
{"cells":["create(/a,1)","create(/a/b,2)","create(/c/d,3)","create(/a,5)","get(/a/b)","get(/a/x)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"tree":"/a=1","result":"true"},"note":"Call 0: the parent exists and /a is new, so the walk adds the node with value 1."},{"at":{"call":1},"vars":{"tree":"/a=1 /a/b=2","result":"true"},"note":"Call 1: the parent exists and /a/b is new, so the walk adds the node with value 2."},{"at":{"call":2},"vars":{"tree":"/a=1 /a/b=2","result":"false"},"note":"Call 2: the walk stops because /c is missing, so the call returns false and writes nothing."},{"at":{"call":3},"vars":{"tree":"/a=1 /a/b=2","result":"false"},"note":"Call 3: the path /a exists already, so the call returns false and keeps the old value 1."},{"at":{"call":4},"vars":{"tree":"/a=1 /a/b=2","result":"2"},"note":"Call 4: the walk reaches /a/b, so the call returns 2."},{"at":{"call":5},"vars":{"tree":"/a=1 /a/b=2","result":"-1"},"note":"Call 5: the walk cannot reach /a/x, so the call returns -1."}]}
```

Call 2 names `/c/d`. The walk stops at the root because `c` is missing, so the call returns false and writes nothing. Call 3 fails for a different reason: the full path exists already.

#### Many Spellings, One Location

The second trace feeds raw strings through the entry step. Each step shows the list of components the policy produces, or the reason the string is rejected. The policy collapses repeated separators, ignores a trailing separator and rejects the names `.` and `..`. It also rejects a string that does not start with a separator.

```trace
{"cells":["/a/b","//a///b/","/","a/b","/a/./b","/a/b."],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"components":"a,b"},"note":"Call 0: the components a,b name a new location."},{"at":{"call":1},"vars":{"components":"a,b"},"note":"Call 1: the components a,b name the same location as call 0."},{"at":{"call":2},"vars":{"components":"(none)"},"note":"Call 2: the components (none) name the root."},{"at":{"call":3},"vars":{"components":"rejected"},"note":"Call 3: the string is rejected because no leading separator."},{"at":{"call":4},"vars":{"components":"rejected"},"note":"Call 4: the string is rejected because the name . is illegal."},{"at":{"call":5},"vars":{"components":"a,b."},"note":"Call 5: the components a,b. name a new location."}]}
```

The first two strings denote the same location, so they resolve to the same node. The empty list of components is the root itself, and a name with a trailing dot such as `b.` stays legal.

<!-- stage: code -->
### Creating And Reading With A Tree

The class below stores the tree and resolves clean paths of the form `/a/b`. The walk to the parent is read-only, and the new node is added only after it succeeds.

```java
import java.util.*;

final class TreeFs {
    private static final class Node {
        final Map<String, Node> kids = new HashMap<>();
        int value = -1;
    }

    private final Node root = new Node();

    boolean createPath(String path, int v) {
        String[] part = path.substring(1).split("/");          // names between separators
        Node cur = root;
        for (int i = 0; i < part.length - 1; i++) {            // O(d) lookups to reach the parent
            cur = cur.kids.get(part[i]);
            if (cur == null) return false;                     // missing parent: nothing is written
        }
        String last = part[part.length - 1];
        if (cur.kids.containsKey(last)) return false;          // the path exists already
        Node fresh = new Node();                               // the only write of the call
        fresh.value = v;
        cur.kids.put(last, fresh);
        return true;
    }

    int get(String path) {
        Node cur = root;
        for (String name : path.substring(1).split("/")) {     // one lookup per name
            cur = cur.kids.get(name);
            if (cur == null) return -1;
        }
        return cur.value;
    }
}
```

Each call costs O(d) map lookups plus O(L) to split a string of length L. The space is O(n) for n stored nodes.

<!-- stage: applicability -->
### Names That Resolve Through Parents

#### Recognizing The Pattern

The cue is a string made of names that identify an object, together with a rule that a parent must exist first. File paths, URL routes, configuration keys and database table names all fit. Ask what the root is, what separates the names and which spelling counts as the same location. The invariant is that each stored node is reachable from the root and has one parent.

#### Choosing The Node Contents

A plain directory tree needs a map per node. Use a sorted map when a call lists children in order, and a hash map when it only looks names up. A database catalog is the same tree with fixed depth: the table name is the first name, and the row identifier is the second.

#### False Friends

A flat map from full path to value is a false friend. It passes the creation tests and fails on listings, on subtree counts and on alternate spellings of one path. A trie over characters is another false friend, because the units here are whole names and not letters. Skip the tree when the service never lists, deletes or counts by parent, because then a flat map is enough.

<!-- stage: exercises -->
### Exercises

#### [Build] Design File System (LeetCode 1166)
<!-- id: sv-hier-file-system -->

**Prerequisites.** Hash maps and string splitting.

**Problem.** Design a class `FileSystem` that stores integer values at paths. A path is the character `/` followed by one or more names, with exactly one `/` between neighbouring names. The call `createPath(path, value)` stores the value and returns `true` only when the path does not exist and its parent path exists. The parent of a one-name path is the root, which always exists. Otherwise the call returns `false` and stores nothing. The call `get(path)` returns the stored value, or -1 if the path does not exist.

**Constraints.** The limits are:
- **Path** has length from 2 to 100 and contains lowercase letters and `/` in the form above.
- **Value** is an integer from 1 to 10^9.
- **Calls** number at most 10^4.

**Example 1.** Input calls `createPath(/a,1)`, `createPath(/a/b,2)`, `get(/a/b)`, `createPath(/c/d,3)`, `get(/c/d)`, output `true`, `true`, 2, `false`, -1.

**Example 2.** Input calls `createPath(/a,1)`, `createPath(/a,5)`, `get(/a)`, `createPath(/a/b/c,4)`, `get(/a/b)`, output `true`, `false`, 1, `false`, -1.

**Hint.** Which node must the walk reach before any node is added?

**Changed decision.** The call walks to the parent first and adds a node only after that walk succeeds, so a failed call leaves no partial path behind.

#### [Vary] Design In-Memory File System (LeetCode 588)
<!-- id: sv-hier-in-memory-fs -->

**Prerequisites.** The file system exercise above and sorted maps.

**Problem.** The rules below are this chapter's own wording and may differ in detail from LeetCode. Design a class `Fs` whose tree holds directories and files. A path is `/` for the root, or `/` followed by names with one `/` between neighbours. The call `mkdir(path)` creates the directory and every missing directory above it, and it returns `true`. It returns `false` and changes nothing if the path or any directory above it is a file. The call `addContentToFile(path, text)` appends the text to the file at the path, creating the file and its missing directories first. It returns `false` and changes nothing if the path is a directory, the root, or has a file above it. The call `readContentFromFile(path)` returns the content of the file, or the empty string if the path is not a file. The call `ls(path)` returns the names of the children of a directory in lexicographic order. For a file it returns a list holding only the file's own name, and for a missing path it returns an empty list.

**Constraints.** The limits are:
- **Names** use lowercase letters and digits, with length from 1 to 10.
- **Text** has length from 1 to 20, and a file never grows beyond 10^5 characters.
- **Calls** number at most 10^4.
- **Return** of `ls` is a list of strings.

**Example 1.** Input calls `mkdir(/a/b)`, `addContentToFile(/a/b/f,hi)`, `addContentToFile(/a/b/f,yo)`, `readContentFromFile(/a/b/f)`, `ls(/a/b)`, `ls(/a/b/f)`, output `true`, `true`, `true`, `hiyo`, the list f, the list f.

**Example 2.** Input calls `mkdir(/m)`, `mkdir(/b)`, `addContentToFile(/z,q)`, `mkdir(/z/y)`, `ls(/)`, `ls(/z/y)`, output `true`, `true`, `true`, `false`, the list b, m, z, the empty list.

**Hint.** Before anything is created, is any name on the path already a file?

**Changed decision.** A node is now a directory or a file, and directories keep children in a sorted map. A read-only walk checks the kinds first, and the second pass creates missing directories.

#### [Boundary] Root And Repeated Separators (Author exercise)
<!-- id: sv-hier-root-separators -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Registry` that accepts messy path strings. The normalization policy has four rules. A path must start with `/`. Empty names from repeated or trailing separators are dropped. The names `.` and `..` make the path invalid. A path with no names left is the root. The call `add(path, value)` stores the value and returns `true` only if the path is valid, is not the root, does not exist, and its parent exists. The root never holds a value, and every other call that fails changes nothing. The call `get(path)` returns the value, or -1 for an invalid, root or missing path. The call `below(path)` returns the number of stored paths strictly under the location, and 0 for an invalid or missing path.

**Constraints.** The limits are:
- **Path** has length from 1 to 200 and contains lowercase letters, `.` and `/`.
- **Value** is an integer from 1 to 10^9.
- **Calls** number at most 10^4.
- **Names** such as `...` and `a.` are valid, because only `.` and `..` alone are rejected.

**Example 1.** Input calls `add(//a//,1)`, `add(/a/b/,2)`, `get(/a///b)`, `add(/,5)`, `below(/)`, `below(a)`, output `true`, `true`, 2, `false`, 2, 0.

**Example 2.** Input calls `add(/a/../b,1)`, `add(/x,4)`, `add(/x/..y,6)`, `add(/x/.,7)`, `get(/x//..y/)`, `below(//x)`, output `false`, `true`, `true`, `false`, 6, 1.

**Hint.** Which spellings must reach the same node, and which must be rejected before the walk?

**Changed decision.** Every call normalizes first, and the count of stored paths below each node rises only after the whole add has been validated.

#### [Recognize] Design SQL (LeetCode 2408)
<!-- id: sv-hier-sql-tables -->

**Prerequisites.** All three exercises above.

**Problem.** This contract is written for the chapter, because LeetCode 2408 is a premium problem and its statement may differ. Design a class `Sql` built from distinct table names and the number of columns of each table. The call `insertRow(name, row)` appends a row of strings to the table and returns its row id. Ids of one table start at 1, grow by one for each successful insert, and are never reused after a delete. It returns -1 and changes nothing if the table is unknown or the row length differs from the column count. The call `deleteRow(name, id)` removes a live row and returns `true`, or returns `false` otherwise. The call `selectCell(name, id, column)` returns the string in a 1-based column of a live row, or the empty string for any invalid argument. The call `count(name)` returns the number of live rows, or -1 for an unknown table.

**Constraints.** The limits are:
- **Tables** number from 1 to 100, and **columns** are integers from 1 to 10.
- **Cells** are strings of length from 1 to 10.
- **Calls** number at most 10^5.
- **Ids** are `int` values assigned per table.

**Example 1.** Tables `a` with 2 columns and `b` with 1 column. Input calls `insertRow(a,[x,y])`, `insertRow(a,[p])`, `insertRow(a,[p,q])`, `selectCell(a,2,1)`, `deleteRow(a,1)`, `insertRow(a,[m,n])`, `count(a)`, output 1, -1, 2, `p`, `true`, 3, 2.

**Example 2.** The same tables. Input calls `insertRow(c,[z])`, `insertRow(b,[k])`, `deleteRow(b,1)`, `deleteRow(b,1)`, `selectCell(b,1,1)`, `insertRow(b,[w])`, output -1, 1, `true`, `false`, the empty string, 2.

**Hint.** Which name resolves the container, and which counter must a failed insert leave alone?

**Changed decision.** The table name is the first level of the tree, and the row id is the second level. The id counter advances only after the table and the row length have been validated.
