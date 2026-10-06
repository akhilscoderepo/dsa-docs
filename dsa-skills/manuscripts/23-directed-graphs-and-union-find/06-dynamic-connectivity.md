<!-- lesson-kind: standard -->
<!-- lesson-id: dynamic-connectivity -->
## Dynamic Connectivity

<!-- stage: context -->
### Answering Link Questions While Links Arrive

A fraud-detection service watches events of two kinds. One kind says that account 7 and account 19 share a device. The other kind asks whether account 7 and account 40 are linked through any chain of shared devices. The events interleave, and the answer to a question must reflect every link that arrived before it. Another service merges user records that share an email address, and its final output is one record for each person.

Both services need the same capability. They must keep groups of items up to date while the groups merge. They must also tell quickly whether two items are in the same group.

This lesson asks how to answer a question after each new link, without searching the whole graph again.

<!-- stage: naive -->
### Searching The Graph For Every Question

The direct approach stores all links in a list. For each question, it builds the adjacency lists from the stored links and runs a depth-first search from the first item. It reports whether the search reaches the second item.

```java
static boolean connectedBySearch(int n, List<int[]> links, int a, int b) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] link : links) {
        adj.get(link[0]).add(link[1]);
        adj.get(link[1]).add(link[0]);
    }
    boolean[] seen = new boolean[n];
    ArrayDeque<Integer> stack = new ArrayDeque<>();
    stack.push(a);
    seen[a] = true;
    while (!stack.isEmpty()) {
        int v = stack.pop();
        if (v == b) return true;
        for (int w : adj.get(v)) {
            if (!seen[w]) { seen[w] = true; stack.push(w); }
        }
    }
    return false;
}
```

Suppose 50,000 link events arrive first, and then 50,000 questions follow.

```predict
Roughly how many link reads does this method perform in total, and does saving the result of one search help after the next link arrives?

Each question rebuilds the lists from all 50,000 links and then searches, so it reads at least 50,000 links. Fifty thousand questions give about 2.5 billion reads. A saved result describes the graph at one moment. The next link can join two groups, and the saved answer for those groups is then wrong, so the program must search again.
```

<!-- stage: bottleneck -->
### Every Question Pays For The Whole Graph

Each call costs O(n + m) for n items and m links, because it rebuilds the adjacency lists and may visit every item. With q questions the total is O(q * (n + m)). For the numbers above, that is billions of operations for a task that only compares two items.

A cheaper variant keeps the adjacency lists and a label array from the last search, so a question compares two labels in constant time. That variant breaks on every new link that joins two groups. The labels of one whole group must change, and relabeling costs O(n) in the worst case. A feed that alternates links and questions pays that price again and again.

The program needs a structure in which one link updates a constant number of values, and in which a question reads two values. The next stage shows what to store so that both operations stay short.

<!-- stage: insight -->
### Two Items Connected Means Equal Finds

The searching approach recomputes an answer that the structure could have kept. Each group needs one name, and a name check answers every question.

<!-- names: representative, component count, group key -->

#### One Representative For Each Group

Every group of linked items keeps exactly one **representative**, which is the root of its tree in the structure from the previous lesson. The call `find(x)` returns the representative of the group of x. Two items are connected exactly when `find(a) == find(b)`. A question therefore costs two finds, and with union by size each find is O(log n).

#### One Merge For Each New Link

A link between a and b runs the same two finds. If the representatives differ, the link joins two groups, and the program merges the two trees. If they are equal, the link adds nothing new, because a path between the items already exists. A repeated link, a reversed link and a link that closes a cycle all fall into this second case.

#### Counting Groups While They Merge

The **component count**, stored in the variable `components`, starts at n, because every item is alone. It drops by one exactly when a link merges two different groups. It never changes on a link that finds equal representatives. At any moment, the count equals n minus the number of merges so far, so no search is needed to report it.

#### Collecting Items By Group

A program that must output the groups, such as a record merge, runs `find(i)` for every item at the end. The returned representative is the **group key**, and all items with the same key belong in one output group. This works because connected items always share one key.

<!-- stage: variables -->
### What The Program Keeps

The program keeps two arrays, one counter, one result list and one map for the whole stream of events. It reads the events once and does not store them.

- **parent** is an int array; `parent[x]` is the parent of x, and a representative is its own parent.
- **size** is an int array; `size[r]` counts the items under the representative r.
- **components** is an int that starts at n and drops by one for each real merge.
- **answers** is the list of results, one boolean for each question in input order; the code below names it `out`.
- **x** and **y** are the two representatives that the code finds for each event; the trace pointers `ra` and `rb` mark that same pair.
- **owner** is a map used only for shared identifiers; it stores the first item that listed a given identifier. The code below leaves out `components` and `owner`, and the traces show them.

<!-- stage: trace -->
### Two Event Streams Traced

#### Links And Questions In One Stream

The first stream has six items and seven events. Each event is either a link or a question. A question reads the two representatives and compares them. The pointers `ra` and `rb` mark the representatives that the event found. The variable `components` changes only on a link that merges two groups. The fifth event asks again about the pair 0 and 3, and its answer changed because the fourth event joined their groups. The sixth event repeats a connection, so it leaves the count at 3.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["ra","rb"],"steps":[{"at":{"ra":0,"rb":1},"vars":{"event":"link 0,1","parent":"0 0 2 3 4 5","components":5,"answer":"none"},"note":"The link 0,1 finds the representatives 0 and 1, which differ, so it merges the two groups and the count drops to 5."},{"at":{"ra":2,"rb":3},"vars":{"event":"link 2,3","parent":"0 0 2 2 4 5","components":4,"answer":"none"},"note":"The link 2,3 finds the representatives 2 and 3, which differ, so it merges the two groups and the count drops to 4."},{"at":{"ra":0,"rb":2},"vars":{"event":"ask 0,3","parent":"0 0 2 2 4 5","components":4,"answer":"false"},"note":"The question 0,3 finds the representatives 0 and 2, so the answer is false."},{"at":{"ra":0,"rb":2},"vars":{"event":"link 1,2","parent":"0 0 0 2 4 5","components":3,"answer":"none"},"note":"The link 1,2 finds the representatives 0 and 2, which differ, so it merges the two groups and the count drops to 3."},{"at":{"ra":0,"rb":0},"vars":{"event":"ask 0,3","parent":"0 0 0 0 4 5","components":3,"answer":"true"},"note":"The question 0,3 finds the representatives 0 and 0, so the answer is true."},{"at":{"ra":0,"rb":0},"vars":{"event":"link 3,0","parent":"0 0 0 0 4 5","components":3,"answer":"none"},"note":"The link 3,0 finds the same representative 0 twice, so the groups and the count stay as they are."},{"at":{"ra":4,"rb":5},"vars":{"event":"ask 4,5","parent":"0 0 0 0 4 5","components":3,"answer":"false"},"note":"The question 4,5 finds the representatives 4 and 5, so the answer is false."}]}
```

#### Merging Records That Share An Email

The second stream has five accounts. Each account lists emails, and an email that two accounts share links those accounts. The program stores the first account that lists an email in `owner`. A later account that lists the same email merges with that owner. The pointer `acct` marks the account being read, and `other` marks the owner it merged with, or -1 when no merge happened. After the last account, the groups are read by representative.

```trace
{"cells":[0,1,2,3,4],"pointers":["acct","other"],"steps":[{"at":{"acct":0,"other":-1},"vars":{"emails":"a b","parent":"0 1 2 3 4","components":5},"note":"Account 0 lists only new emails, so it stores itself as the owner of each and merges with nothing."},{"at":{"acct":1,"other":-1},"vars":{"emails":"c d","parent":"0 1 2 3 4","components":5},"note":"Account 1 lists only new emails, so it stores itself as the owner of each and merges with nothing."},{"at":{"acct":2,"other":0},"vars":{"emails":"b e","parent":"2 1 2 3 4","components":4},"note":"Account 2 lists the email b, which account 0 listed first, so the two accounts merge."},{"at":{"acct":3,"other":-1},"vars":{"emails":"f","parent":"2 1 2 3 4","components":4},"note":"Account 3 lists only new emails, so it stores itself as the owner of each and merges with nothing."},{"at":{"acct":4,"other":1},"vars":{"emails":"d g","parent":"2 4 2 3 4","components":3},"note":"Account 4 lists the email d, which account 1 listed first, so the two accounts merge."},{"at":{"acct":-1,"other":-1},"vars":{"emails":"none","parent":"2 4 2 3 4","components":3},"note":"The final pass groups the accounts by representative and finds the groups 0 and 2, 1 and 4, and 3 alone."}]}
```

<!-- stage: code -->
### Online Queries And Grouping In Java

The first method processes a list of events. An event is `{0, a, b}` for a link or `{1, a, b}` for a question, and the method returns one boolean for each question. The second method groups all items by their final representative.

```java
final class Connectivity {
    static boolean[] process(int n, int[][] events) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        List<Boolean> out = new ArrayList<>();
        for (int[] ev : events) {
            int x = find(parent, ev[1]);
            int y = find(parent, ev[2]);
            if (ev[0] == 1) { out.add(x == y); continue; }
            if (x == y) continue;
            if (size[x] < size[y]) { int t = x; x = y; y = t; }
            parent[y] = x;
            size[x] += size[y];
        }
        boolean[] res = new boolean[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static Map<Integer, List<Integer>> byGroup(int[] parent) {
        Map<Integer, List<Integer>> groups = new TreeMap<>();
        for (int i = 0; i < parent.length; i++)
            groups.computeIfAbsent(find(parent, i), k -> new ArrayList<>()).add(i);
        return groups;
    }
}
```

The method `find` halves the path while it climbs, which keeps later walks short. A question never writes to either array except through path halving, and path halving never changes who the representative is. Each event costs O(log n), so the stream costs O(e log n) for e events, and the arrays take O(n) space.

<!-- stage: applicability -->
### Recognizing Merging Groups With Queries

#### Reading The Cue

Use this structure when items join groups over time and the question is about group identity. Statements say that two users become friends or that two accounts share an identifier. Some ask for the number of groups after each new edge. If the final output must list the members of each group, collect the items by representative once at the end.

#### Checking The Invariant

The invariant is that two items are connected exactly when their finds return the same representative. It holds when every link merges the trees of both endpoints, and when the program never compares raw items or stale parent entries. The program must turn a shared identifier into a merge of the two items. Otherwise the invariant fails for every group that depends on it.

#### Avoiding The False Friend

The false friend is a static depth-first search. It answers one snapshot of the graph correctly, and it fits a graph that never changes. Repeated merges make each new question restart that search from nothing. If the whole input is known up front and only one answer is needed, a single search is simpler and just as fast.

<!-- stage: exercises -->
### Exercises

#### [Build] Online Connect And Query (Author exercise)
<!-- id: dg-online-connect-query -->

**Prerequisites.** Union by size and the representative test of this lesson.

**Problem.** Items are numbered `0` to `n - 1`, and no two items are linked at the start. Each event is an array `[t, a, b]`. When `t = 0`, the event links `a` and `b`. When `t = 1`, the event asks whether a chain of earlier links joins `a` and `b`. An item is joined to itself. Return a `boolean[]` that holds one answer for each question, in input order.

**Constraints.** The limits are:
- **Items** satisfy `1 <= n <= 1000`.
- **Events** satisfy `0 <= events.length <= 3000`, and `t` is 0 or 1.
- **Values** `a` and `b` are in `0..n-1`, and they may be equal.
- **Result** has one entry per question, and it is empty when no question appears.

**Example 1.** Input `n = 5`, `events = [[1,0,1],[0,0,1],[0,1,2],[1,0,2],[1,3,4]]`, output `[false,true,false]`.

**Example 2.** Input `n = 4`, `events = [[0,3,2],[1,2,3],[1,0,0],[0,0,3],[1,2,0]]`, output `[true,true,true]`.

**Hint.** Which earlier events can influence the answer to a question, and which later ones cannot?

**Changed decision.** The method answers each question with two finds at the moment the question arrives, and it merges only on link events.

#### [Vary] Provinces After Each Edge (LeetCode 547)
<!-- id: dg-provinces-per-edge -->

**Prerequisites.** The first exercise above.

**Problem.** A country has `n` cities numbered `0` to `n - 1`. A province is a maximal set of cities that are joined by chains of direct connections. Here the connections arrive as a list `links`, where each entry `[a, b]` is a direct connection. Return an `int[]` of the same length as `links`, where entry `k` is the number of provinces after the first `k + 1` connections exist.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 1000`.
- **Links** satisfy `0 <= links.length <= 3000`, and every value is in `0..n-1`.
- **Equal values** `a == b` are allowed and add no connection.
- **Result** has `links.length` entries, and each entry is at least 1.

**Example 1.** Input `n = 4`, `links = [[0,1],[2,3],[1,0],[1,2]]`, output `[3,2,2,1]`.

**Example 2.** Input `n = 3`, `links = [[0,0],[1,2]]`, output `[3,2]`.

**Hint.** After which kind of link does the number of provinces change, and by how much?

**Changed decision.** The method reports the province count after every link, and it lowers the count only when the two endpoints have different representatives.

#### [Boundary] Duplicate Union (Author exercise)
<!-- id: dg-duplicate-union -->

**Prerequisites.** The two exercises above.

**Problem.** Items are numbered `0` to `n - 1`, and `pairs` lists links `[a, b]` that arrive in order. A link is effective when it joins two groups that were separate just before it arrived. Return an `int[]` of length 2 that holds the final number of groups and the number of effective links.

**Constraints.** The limits are:
- **Items** satisfy `1 <= n <= 1000`.
- **Pairs** satisfy `0 <= pairs.length <= 3000`, and every value is in `0..n-1`.
- **Repeats** of a pair, in either order, and pairs with `a == b` are allowed.
- **Result** is `[groups, effective]`, and the two numbers add up to `n`.

**Example 1.** Input `n = 5`, `pairs = [[0,1],[1,0],[0,1],[3,3],[3,4]]`, output `[3,2]`.

**Example 2.** Input `n = 3`, `pairs = [[2,1],[1,2],[0,2],[2,0],[0,1]]`, output `[1,2]`.

**Hint.** What do the two finds return for a link that arrives a second time?

**Changed decision.** The method counts a link as effective only when the representatives differ, so a repeated pair leaves both numbers unchanged.

#### [Recognize] Accounts Merge (LeetCode 721)
<!-- id: dg-accounts-merge -->

**Prerequisites.** All three exercises above.

**Problem.** Each account is a list whose first entry is a name and whose other entries are emails. Two accounts belong to the same person when they share at least one email, or when a chain of accounts joins them through shared emails. Two accounts with the same name but no such chain are different people. Return the merged accounts. Each result list holds the name, followed by the distinct emails of that person in ascending order. The result lists may appear in any order.

**Constraints.** The limits are:
- **Accounts** satisfy `1 <= accounts.length <= 1000`.
- **Entries** per account number between 2 and 10, so each account has at least one email.
- **Emails** are strings that contain `@`, and one email belongs to one name only.
- **Input** may be read but is not changed.

**Example 1.** Input `accounts = [["Ana","a@x.com","b@x.com"],["Ben","c@x.com"],["Ana","b@x.com","d@x.com"],["Ana","e@x.com"]]`, output `[["Ana","a@x.com","b@x.com","d@x.com"],["Ben","c@x.com"],["Ana","e@x.com"]]`.

**Example 2.** Input `accounts = [["Kim","k1@m.com","k2@m.com"],["Kim","k3@m.com"],["Kim","k4@m.com","k3@m.com"],["Kim","k2@m.com","k4@m.com"],["Kim","z@m.com"]]`, output `[["Kim","k1@m.com","k2@m.com","k3@m.com","k4@m.com"],["Kim","z@m.com"]]`.

**Hint.** Which map lets the second account that lists an email find the first one?

**Changed decision.** The method merges accounts through shared emails and groups the emails by the final representative of their account.
