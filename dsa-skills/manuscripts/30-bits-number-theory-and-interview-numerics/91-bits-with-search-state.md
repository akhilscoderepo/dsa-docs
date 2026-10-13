<!-- lesson-kind: combination -->
<!-- lesson-id: bits-with-search-state -->
## Bits With Search State

<!-- stage: context -->
### Why Sets Slow Down Search

A maintenance robot must inspect up to 12 stations that are joined by corridors. It may walk through a station twice, and it wants the fewest corridor steps that reach every station. A planner that stores the list of stations seen so far for each route copies that list at every step. A second tool must list every combination of 12 feature flags for a test run. A third tool scans a genome of one million letters for ten-letter reads that occur twice. A fourth tool picks two product names with no letter in common.

Each task asks about a small set of items. The set is a group of stations, a group of flags, a group of letters, or a window of ten letters. Collections of objects make the sets heavy to copy, to compare and to use as keys. The question for this lesson is how one integer can carry such a set through enumeration, a sliding window, a pairwise test and a graph search.

Formally, the input is a small list, a short string over a small alphabet, or an undirected graph with at most 12 nodes. The tasks are to list all subsets, to find repeated windows, to maximize a product over disjoint pairs, and to find a shortest walk that visits every node. The four tasks are independent, so you can read them one at a time.

<!-- stage: contributions -->
### What Earlier Lessons Contribute

#### Bit Masks Supply Set Membership

The bit-masks lesson stored a set in one `int`, which has 32 bits, or in one `long`, which has 64 bits. Loops that count through every mask stop at `n = 30` for an `int` and `n = 62` for a `long`. Bit `i` is 1 when item `i` belongs to the set. The expression `1 << i` builds a one-item set, `|` joins sets and `&` finds the common items. Two sets share nothing when the `&` of their integers is 0. This lesson relies on that exact encoding, because equal sets always have equal integers.

#### Shifts Supply Fixed Windows

The shifts lesson showed that `x << b` moves every bit left by `b` positions and that an `&` with a mask of ones cuts the result to a fixed width. A window of `k` letters, with two bits per letter, fits in `2k` bits. Moving to the next window shifts the old window left by two bits, adds the new letter and cuts the extra bits. This turns each window into one number without building a string.

#### Subset Masks Supply Enumeration

The subset-masks lesson counted from 0 to `2^n - 1` and read each number as one subset of `n` items. That loop lists all subsets in a fixed order, and `Integer.bitCount` gives the size of each one. This lesson reuses that loop and adds an ordering rule.

#### Breadth-First Search Supplies Shortest Walks

Earlier graph chapters taught breadth-first search, which visits states in order of their distance from the start and finds the first goal at the smallest number of edges. They also taught graph-state modeling, where a search state holds more than the current node. The robot task needs that idea, because the answer depends on the stations seen so far and not only on the current station.

<!-- stage: naive -->
### Keeping Sets As Objects

The direct approach stores each set as a Java collection. The method below runs breadth-first search for the robot task. A search state is a node together with a `TreeSet` of nodes seen, and a string built from that set marks the state as already queued.

```java
static int shortestVisitAllNaive(int[][] graph) {
    int n = graph.length;
    Deque<Object[]> queue = new ArrayDeque<>();
    Set<String> queued = new HashSet<>();
    for (int s = 0; s < n; s++) {
        TreeSet<Integer> seen = new TreeSet<>(List.of(s));
        queue.add(new Object[]{s, seen, 0});
        queued.add(s + ":" + seen);                       // the string key lists every seen node
    }
    while (!queue.isEmpty()) {
        Object[] cur = queue.poll();
        int node = (int) cur[0];
        @SuppressWarnings("unchecked")
        TreeSet<Integer> seen = (TreeSet<Integer>) cur[1];
        int dist = (int) cur[2];
        if (seen.size() == n) return dist;                // every node was seen
        for (int next : graph[node]) {
            TreeSet<Integer> copy = new TreeSet<>(seen);   // one copy per edge
            copy.add(next);
            if (queued.add(next + ":" + copy)) queue.add(new Object[]{next, copy, dist + 1});
        }
    }
    return -1;                                            // no walk covers all nodes
}
```

The other tasks look similar in this style. A genome scan would cut every ten-letter substring and store it in a `HashMap<String, Integer>`. A product-name search would build a `Set<Character>` for each name and test every pair with `retainAll`. A flag listing would copy a `List` at every recursive call.

<!-- stage: bottleneck -->
### Objects Cost Time And Memory

```predict
A genome has 1,000,000 letters and the program cuts every window of 10 letters into a separate Java String. Each String object and its array take about 50 bytes. About how much memory do the windows need together, and how many bits does the information in one window really need?

About 50 megabytes for the strings. One window has 10 letters from a 4-letter alphabet, which is 20 bits. A single int holds that, so one million windows fit in about 4 megabytes as ints.
```

#### Count The Copies And The Keys

In the robot search, each queued state owns a `TreeSet` of up to `n` nodes, and each edge copies it. A copy costs O(n log n) time. The key string costs O(n) more to build and to hash. With `n = 12` there are up to `12 * 2^12 = 49,152` states, so the work grows as the number of states times the number of edges times the cost of a copy. The same pattern gives O(N * k) time for `N` windows of length `k` when each window is a substring, and O(n^2 * L) time for all pairs of `n` words with `L` letters each when the sets are rebuilt per pair.

#### Name The Fixed Cost

The information in each set is small. A set of 12 nodes needs 12 bits, a window of ten letters needs 20 bits, and a word needs 26 bits. A collection pays object headers, pointers and hashing for that small amount of information. The target is a representation with O(1) copy, O(1) comparison and a size that matches the information. One integer meets all three conditions.

<!-- stage: insight -->
### Let One Integer Stand For The Set

#### Encode Items In A Membership Mask

A **membership mask** is an integer whose bit `i` is 1 exactly when item `i` is in the set. The empty set is 0, adding item `i` is `mask | (1 << i)`, and testing item `i` is `(mask & (1 << i)) != 0`. Two sets are disjoint when `(a & b) == 0`. Counting from 0 to `(1 << n) - 1` visits every subset once, for `n` up to 30 with an `int` and up to 62 with a `long`, and `Integer.bitCount(mask)` gives its size. Because the encoding is exact, two masks are equal exactly when their sets are equal, so a mask is also a safe map key.

<!-- names: membership mask, window mask, state key -->

#### Slide A Window Mask

A **window mask** holds the last `k` letters of a string, with a fixed number of bits per letter. For the alphabet A, C, G and T, the codes 0, 1, 2 and 3 use two bits each. The update `((w << 2) | code) & full`, where `full` is `(1L << (2 * k)) - 1`, drops the oldest letter and adds the new one in O(1). Two windows are equal exactly when their masks are equal. The mask must be a `long` when `2 * k` can exceed 31, because an `int` shift count wraps modulo 32 and `1 << 32` equals 1.

#### Pair Each Search Node With A Mask

A **state key** is the pair of the current node and the membership mask of nodes seen. It packs into one integer as `(node << n) | mask` and indexes an array of `n * 2^n` slots. Breadth-first search over these keys visits each state at most once, and the first state whose mask equals the full mask is the answer. Revisiting a node is allowed, because the same node with a larger mask is a different state. The invariant is that a state key records everything that can still affect the future of the search, so a key seen before can be skipped safely.

#### Compare The Total Cost

Subset listing costs O(n * 2^n) with the size filter. The window scan costs O(N) for `N` windows. The pairwise test costs O(n^2) mask tests after O(total letters) work to build the masks. The graph search costs O(n * 2^n * deg) time, which is at most about 540,000 edge checks for `n = 12`, and O(n * 2^n) space. Every operation on a set is a constant number of machine instructions.

<!-- stage: variables -->
### Quantities Across The Four Tasks

These quantities appear across the four methods.

- **mask** is the membership mask, an `int` for up to 30 items and a `long` for up to 62 items when a loop counts through every mask.
- **full** in the subset and graph methods is the mask `(1 << n) - 1` with one bit per item.
- **full** in the window method is the mask `(1L << (2 * k)) - 1` with two bits per letter.
- **window** is the window mask of the last `k` letters, kept as a `long`.
- **node** is the current graph node in a search state.
- **state** is the state key `(node << n) | mask`, and `dist[state]` is its distance, or -1 when unvisited.

In the first trace, a **level** is the set of states at one distance from the start. In the code, the variable `mask` holds a membership mask, and `full` holds the full mask with every item present. In the second trace, `window` is the value of the window mask after each letter, shown as a decimal number.

<!-- stage: trace -->
### Follow One Search And One Scan

#### Search A Small Graph Level By Level

Take four nodes with the corridors 0-1, 1-2, 0-2 and 2-3. The adjacency lists are `[1,2]`, `[0,2]`, `[0,1,3]` and `[2]`. A state is a node and a mask over 4 bits, so there are `4 * 16 = 64` possible states.

Level 0 holds the four start states, one per node, each with only its own bit set. Level 1 holds the states one corridor away. Level 2 and level 3 grow in the same way. The full mask is 15, which is `1111` in binary. The search stops when it pops a state with that mask, and the trace shows the level of that state as the answer. The trace lists the number of states in each level and the number of distinct states seen up to the end of that level.

```trace
{"cells":[0,1,2,3],"pointers":["d"],"steps":[{"at":{"d":-1},"vars":{"seenStates":0},"note":"No state exists yet. There are 64 possible states in total."},{"at":{"d":0},"vars":{"levelSize":4,"seenStates":4},"note":"Level 0 holds the 4 start states, one per node, each with only its own bit set."},{"at":{"d":1},"vars":{"levelSize":8,"seenStates":12},"note":"Level 1 holds 8 new states, reached by one more corridor step. The distinct states seen so far number 12."},{"at":{"d":2},"vars":{"levelSize":7,"seenStates":19},"note":"Level 2 holds 7 new states, reached by one more corridor step. The distinct states seen so far number 19."},{"at":{"d":3},"vars":{"levelSize":5,"seenStates":24},"note":"Level 3 is reached after 24 distinct states are queued. Popping a state with the full mask 15 ends the search, so the answer is 3."}]}
```

#### Scan Windows Of Three Letters

The window scan handles the genome task, and it does not use the graph above. It starts from a new string.

Take the string `ACGACGTACGT` and windows of 3 letters, with A, C, G and T coded as 0, 1, 2 and 3. The first window `ACG` has codes 0, 1 and 2, so its mask is `0*16 + 1*4 + 2 = 6`. Each later step multiplies the mask by 4, adds the new code and keeps only 6 bits. The window `CGA` has mask 24, and the trace shows each later value in the same way. A mask seen before marks a repeated window. The mask 6 appears three times and the mask for `CGT` twice.

```trace
{"cells":[0,1,2,0,1,2,3,0,1,2,3],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"window":0},"note":"No letter is read yet. The window mask is 0."},{"at":{"i":0},"vars":{"window":0},"note":"The letter A fills the window. Fewer than 3 letters are present, so no window is complete."},{"at":{"i":1},"vars":{"window":1},"note":"The letter C fills the window. Fewer than 3 letters are present, so no window is complete."},{"at":{"i":2},"vars":{"window":6},"note":"The window is ACG with mask 6. The mask is new."},{"at":{"i":3},"vars":{"window":24},"note":"The window is CGA with mask 24. The mask is new."},{"at":{"i":4},"vars":{"window":33},"note":"The window is GAC with mask 33. The mask is new."},{"at":{"i":5},"vars":{"window":6},"note":"The window is ACG with mask 6. The mask has now occurred 2 times, so ACG is a repeat."},{"at":{"i":6},"vars":{"window":27},"note":"The window is CGT with mask 27. The mask is new."},{"at":{"i":7},"vars":{"window":44},"note":"The window is GTA with mask 44. The mask is new."},{"at":{"i":8},"vars":{"window":49},"note":"The window is TAC with mask 49. The mask is new."},{"at":{"i":9},"vars":{"window":6},"note":"The window is ACG with mask 6. The mask has now occurred 3 times, so ACG is a repeat."},{"at":{"i":10},"vars":{"window":27},"note":"The window is CGT with mask 27. The mask has now occurred 2 times, so CGT is a repeat."}]}
```

The hardest step is the cut `& 63`. It first matters at `GAC`. The raw value is `24 * 4 + 1 = 97`, which is `1100001` in binary and has 7 bits. The top bit belongs to the letter C that has left the window. The cut removes it, so the mask for `GAC` is 33 and holds only the letters G, A and C.

<!-- stage: code -->
### Implement Four Mask Methods

#### List Subsets And Pick Word Pairs

```java
static List<List<Integer>> subsetsBySize(int[] nums) {
    int n = nums.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int size = 0; size <= n; size++) {
        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != size) continue;       // keep one size at a time
            List<Integer> subset = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) subset.add(nums[i]);   // bit i selects nums[i]
            }
            out.add(subset);
        }
    }
    return out;                                                  // sizes ascend, then mask values ascend
}

static long[] bestWordPair(String[] words) {
    int n = words.length;
    int[] letters = new int[n];
    for (int i = 0; i < n; i++) {
        for (char c : words[i].toCharArray()) letters[i] |= 1 << (c - 'a');   // one bit per distinct letter
    }
    long best = 0;
    int bi = -1, bj = -1;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if ((letters[i] & letters[j]) != 0) continue;       // a shared letter rejects the pair
            long product = (long) words[i].length() * words[j].length();   // widen before multiplying
            if (product > best) { best = product; bi = i; bj = j; }
        }
    }
    return new long[]{best, bi, bj};
}
```

The subset method visits `2^n` masks once for each size. The word method keeps the first pair that reaches the best product, because only a strictly larger product replaces it.

#### Scan Repeated Windows

The next two methods handle the genome windows and the robot search. They do not call the two methods above, and they do not call each other.

```java
static List<String> repeatedWindows(String s, int k) {
    Map<Long, Integer> count = new HashMap<>();
    Map<Long, Integer> firstStart = new HashMap<>();
    long full = (1L << (2 * k)) - 1;                            // 2k one-bits, long so k up to 31 is safe
    long window = 0;
    for (int i = 0; i < s.length(); i++) {
        window = ((window << 2) | "ACGT".indexOf(s.charAt(i))) & full;   // slide by one letter
        if (i >= k - 1) {
            count.merge(window, 1, Integer::sum);               // the mask is an exact key
            firstStart.putIfAbsent(window, i - k + 1);
        }
    }
    TreeSet<String> out = new TreeSet<>();
    for (var e : count.entrySet()) {
        if (e.getValue() >= 2) out.add(s.substring(firstStart.get(e.getKey()), firstStart.get(e.getKey()) + k));
    }
    return new ArrayList<>(out);                      // sorted text order
}
```

The window method keeps the first start of each mask so it can return the text.

#### Search Graph States

```java
static int shortestVisitAll(int[][] graph) {
    int n = graph.length, full = (1 << n) - 1;
    int[] dist = new int[n << n];
    Arrays.fill(dist, -1);                            // -1 marks an unvisited state
    int[] queue = new int[n << n];
    int head = 0, tail = 0;
    for (int s = 0; s < n; s++) {
        int state = (s << n) | (1 << s);                        // node s with only its own bit
        dist[state] = 0;
        queue[tail++] = state;
    }
    while (head < tail) {
        int state = queue[head++];
        int node = state >> n, mask = state & full;
        if (mask == full) return dist[state];                   // the first full mask is the shortest
        for (int next : graph[node]) {
            int nextState = (next << n) | (mask | (1 << next));
            if (dist[nextState] == -1) {
                dist[nextState] = dist[state] + 1;
                queue[tail++] = nextState;                      // each state is queued once
            }
        }
    }
    return -1;                                                  // unreachable for a connected graph
}
```

The search method uses arrays of `n << n` slots, so its memory is fixed in advance. The tests `mask == full` and `dist[nextState] == -1` run on integers, with no hashing.

<!-- stage: applicability -->
### When A Mask Fits The Search

#### Recognize The Pattern

Use this combination when the set to remember has at most about 20 items, or when a window has a fixed width over a small alphabet. The cue is a statement that asks about every subset, repeated fixed-length pieces, disjoint pairs, or a walk that must cover all nodes. The invariant is that the mask is an exact encoding of the set, with one bit for each item or one code for each letter. Under that invariant, equal integers mean equal sets, and a visited array indexed by state is sound.

#### Watch For The Nearest False Friend

A plain `visited[node]` array is a false friend of the state key. It is correct when a node may be entered once. The robot task allows entering a node many times, and a node entered with a larger mask is new progress. A `visited[node]` array rejects that second visit and returns a wrong answer or no answer. A mask also stores which items are present and not their order, so a task that charges for the order of visits needs more state than a mask. Sets with 30 or more items make `2^n` masks too many to enumerate, and a sorted-order or greedy method then fits better.

#### Avoid The Java Hazards

The expression `1 << i` is an `int`, and its shift count wraps modulo 32. Use `1L << i` when `i` can reach 31, and keep the mask in a `long`. The window update needs `long` when `2 * k` can exceed 31. Put parentheses around every shift, since `+` binds tighter than `<<`. The product of two lengths can pass `Integer.MAX_VALUE`, so cast one factor to `long` before multiplying. A right shift `>>` keeps the sign bit, and `>>>` fills with zeros, so use `>>>` on masks that may use bit 31.

<!-- stage: exercises -->
### Exercises

#### [Build] Subsets Listed By Size (LeetCode 78)
<!-- id: bt91-subsets-by-size -->

**Prerequisites.** The membership mask and the contributions above.

**Problem.** Given an array `nums` of distinct integers, return every subset. This version fixes the order that the original leaves open. Subset lists appear by increasing size. Among subsets of one size, they appear by increasing mask value, where bit `i` of the mask stands for `nums[i]`. Each subset lists its elements in increasing index order.

**Constraints.** The limits are:
- **`n`** is the length of `nums`, an `int` with `0 <= n <= 12`.
- **Values** are distinct `int` values with absolute value at most 100.
- **Return** is a `List<List<Integer>>` with `2^n` lists.
- **Empty** input returns one list that holds the empty subset.

**Example 1.** Input `nums = [5, 2, 9]`, output `[[], [5], [2], [9], [5, 2], [5, 9], [2, 9], [5, 2, 9]]`, from the masks 0, 1, 2, 4, 3, 5, 6 and 7.

**Example 2.** Input `nums = []`, output `[[]]`, because the only mask is 0, which is the empty subset.

**Hint.** Each number from 0 to `2^n - 1` is one subset. Which built-in method gives the size of a mask?

**Changed decision.** Baseline case: reads every mask as one subset and orders the output by a fixed rule.

#### [Vary] Repeated Windows Of Chosen Length (LeetCode 187)
<!-- id: bt91-repeated-windows -->

**Prerequisites.** The exercise above and the window mask.

**Problem.** Given a string `s` over the letters `A`, `C`, `G` and `T`, and an integer `k`, return every distinct substring of length `k` that occurs at least twice in `s`. Occurrences may overlap. Return the substrings in increasing text order. This version takes the window length `k` as input, while the original fixes it at 10.

**Constraints.** The limits are:
- **`s`** has length `0 <= |s| <= 100,000`.
- **Letters** are only `A`, `C`, `G` and `T`.
- **`k`** is an `int` with `1 <= k <= 31`.
- **Return** is a `List<String>`, and it is empty when `|s| < k`.

**Example 1.** Input `s = "CCGGTTCCGGTTCCGGA"` and `k = 4`, output `["CCGG", "CGGT", "GGTT", "GTTC", "TCCG", "TTCC"]`, where `CCGG` occurs three times with overlap.

**Example 2.** Input `s` equal to 40 copies of `A` and `k = 31`, output a list with the single string of 31 copies of `A`. The window needs 62 bits, so an `int` mask fails.

**Hint.** The window needs `2k` bits. For which values of `k` does an `int` mask fail, and how does the `full` cut change?

**Changed decision.** The window width is no longer fixed at 10, so the mask must widen to a `long` for large `k`.

#### [Boundary] Best Disjoint Word Pair (LeetCode 318)
<!-- id: bt91-best-word-pair -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `words` of lowercase words, find two words with no common letter that maximize the product of their lengths. Return a `long[]` of length 3 with the best product and the two indexes `i < j`. When several pairs tie, return the pair with the smallest `i`, and then the smallest `j`. When no pair is disjoint, return `{0, -1, -1}`. This version returns the pair, and the original returns only the product.

**Constraints.** The limits are:
- **`n`** is the number of words, an `int` with `0 <= n <= 2,000`.
- **Each word** is nonempty, uses only `'a'` to `'z'`, and has at most 100,000 letters.
- **Total** length of all words is at most 1,000,000.
- **Return** is a `long[]`, because a product can exceed `Integer.MAX_VALUE`.

**Example 1.** Input `words = ["abcd", "ab", "xyz", "mnopq", "cde"]`, output `[20, 0, 3]`, since `abcd` and `mnopq` share no letter.

**Example 2.** Input two words, `a` repeated 100,000 times and `b` repeated 100,000 times, output `[10000000000, 0, 1]`. The product 10^10 exceeds the range of `int`.

**Hint.** Two lengths of 100,000 multiply to 10^10. Which type must hold the product, and which factor is cast first?

**Changed decision.** The product width grows past `int`, and the tie rule needs the pair as well as the value.

#### [Recognize] Shortest Walk Ending At A Node (LeetCode 847)
<!-- id: bt91-walk-ends-at-target -->

**Prerequisites.** All three exercises above and breadth-first search.

**Problem.** An undirected connected graph has nodes `0` to `n - 1`, given as adjacency lists. Given a node `t`, return the smallest number of edges in a walk that visits every node at least once and ends at `t`. The walk may start at any node, and it may reuse nodes and edges. This version fixes the end node, while the original accepts any end.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 12`.
- **Graph** is connected, has no self-loop and has no repeated edge.
- **`t`** is an `int` with `0 <= t < n`.
- **Return** is an `int`, and a single-node graph returns 0.

**Example 1.** Input `graph = [[1,2],[0,2],[0,1,3],[2]]` and `t = 3`, output 3, from the walk 0, 1, 2, 3. The same graph with `t = 2` gives 4.

**Example 2.** Input `graph = [[1],[0,2],[1,3],[2]]` and `t = 1`, output 4, from the walk 3, 2, 1, 0, 1. A one-node graph `[[]]` with `t = 0` gives 0.

**Hint.** The goal is one specific state and not any state with the full mask. Which pair of values identifies it?

**Changed decision.** The goal changes from any state with the full mask to one given node with the full mask.
