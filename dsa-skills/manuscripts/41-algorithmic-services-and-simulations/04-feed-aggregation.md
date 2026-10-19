<!-- lesson-kind: standard -->
<!-- lesson-id: feed-aggregation -->
## Merge Feeds From Many Sources

<!-- stage: context -->
### A Timeline That Slows With Every Follow

A small messaging service shows each user the ten newest posts from the accounts that user follows. The first version works well in testing, where every account has a few dozen posts. After a month, one user follows 300 accounts that have posted 40,000 times in total. Opening the timeline now takes noticeable time, even though the screen shows only ten posts.

A second report arrives from support. A user deleted an account, and the posts of that account still appear in the timelines of its followers. A third report says the timeline of one user shows that user's own posts twice.

This lesson asks how to answer a timeline query by looking at a few posts, how to keep follow state and account lifecycle rules in step with the answer, and where a rule such as "skip deleted accounts" must run so the limit of ten still counts the right posts.

<!-- stage: naive -->
### Collect Everything And Sort

The direct design gathers every post of every followed account into one list. It sorts that list by time from newest to oldest and returns the first `k` entries.

```java
final class NaiveFeed {
    private final Map<Integer, List<int[]>> posts = new HashMap<>();   // author -> {time, id}
    private final Map<Integer, Set<Integer>> follows = new HashMap<>();
    private int clock = 0;

    void post(int user, int id) {
        posts.computeIfAbsent(user, x -> new ArrayList<>()).add(new int[] {clock++, id});
    }

    void follow(int a, int b) { follows.computeIfAbsent(a, x -> new HashSet<>()).add(b); }

    List<Integer> feed(int user, int k) {
        List<int[]> all = new ArrayList<>(posts.getOrDefault(user, List.of()));
        for (int b : follows.getOrDefault(user, Set.of())) all.addAll(posts.getOrDefault(b, List.of()));
        all.sort((p, q) -> q[0] - p[0]);                 // sorts every post, however few are needed
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < Math.min(k, all.size()); i++) out.add(all.get(i)[1]);
        return out;
    }
}
```

The answers are correct while the follow rules stay trivial. The cost grows with the total number of posts, and the code has no place to say that a followed account was deleted or that a user follows themselves.

```predict
A user follows 300 accounts with 40,000 posts in total and asks for the ten newest posts. How much work does the query above do, and how many of those posts does the answer actually need?

The query copies all 40,000 posts into one list and sorts them, which costs about 40,000 times the logarithm of 40,000 comparisons. The answer needs ten posts. Almost all of the copying and sorting is wasted, and the waste grows every time any followed account posts.
```

<!-- stage: bottleneck -->
### Work Proportional To All Posts

The query cost is O(n log n) for n posts held by the followed accounts, and n grows without bound while `k` stays at ten. Sorting is not even needed, because each account already stores its own posts in time order. The collect-and-sort code throws that order away and rebuilds it.

A second cost hides in the rules. Suppose the code applies the limit first and the filter second. It takes the ten newest posts and then removes the posts of deleted accounts. The user may then see four posts although more than ten eligible posts exist. The filter must run before the limit, so the limit counts only posts the user is allowed to see.

Both costs point to the same fix. The query should read as few posts as the answer needs, and it should never read a post from an account that fails the rules.

<!-- stage: insight -->
### Read One Post Per Account

Every account stores its posts in time order, so the newest post of an account is the only post of that account that can come next in the answer. Keep one entry per eligible account, which is the **frontier**. The frontier entry for an account is that account's newest post that the query has not yet returned.

#### The Merge With A Heap

Store the frontier entries in a **heap**, a priority queue that returns the entry with the newest time in O(log f) for f entries. Remove the top entry and append its post to the answer. Then push the next older post of the same account, if one exists, as the new frontier entry of that account. After `k` removals the answer is complete. This is a k-way merge, and the query reads at most `k` posts plus one starting post per account.

#### Where The Rules Run

The rules decide which accounts get a frontier entry at all. A **visibility check** runs before the first push: it admits the user's own account once, admits each followed account that is still live and skips every other account. Because skipped accounts never enter the heap, the limit of `k` counts only visible posts. A deleted account needs no cleanup in the follow sets of its followers, since the check skips it each time.

The invariant is that the heap holds exactly one entry for each eligible account that still has unreturned posts, so the top entry is always the newest unreturned visible post.

<!-- names: frontier, heap, visibility check -->

<!-- stage: variables -->
### State Behind One Timeline Query

The service keeps authoritative state and derived views apart, and each entry below has one owner.

- **Posts** is the authoritative list of posts per author, each stored with its time, and a post call appends to it.
- **Follow set** is the authoritative set of accounts each user follows, and follow and unfollow calls change it.
- **Deleted set** is the authoritative record of accounts that no longer exist, and the delete call adds an id to it.
- **Heap** is a local view built for one query, and it disappears when the query returns.
- **Clock** is a counter that gives every post a unique time, so two posts never tie.

<!-- stage: trace -->
### Following Heap Pops And Service Calls

#### A Merge Of Three Streams

The first trace merges three accounts whose posts are stored newest first. The pointer `pop` marks the removal that happens at each step. The frontier lists the heap entries as time@account, and the output grows by one post per step.

```trace
{"cells":["pop 1","pop 2","pop 3","pop 4","pop 5"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"frontier":"8@1 6@0 5@2","output":"9"},"note":"Pop 1: the heap held 9@0 8@1 5@2, so the entry 9@0 leaves and the output gains 9. Account 0 pushes its next post 6."},{"at":{"pop":1},"vars":{"frontier":"7@1 6@0 5@2","output":"9,8"},"note":"Pop 2: the heap held 8@1 6@0 5@2, so the entry 8@1 leaves and the output gains 8. Account 1 pushes its next post 7."},{"at":{"pop":2},"vars":{"frontier":"6@0 5@2","output":"9,8,7"},"note":"Pop 3: the heap held 7@1 6@0 5@2, so the entry 7@1 leaves and the output gains 7. Account 1 has no older post, so it adds no entry."},{"at":{"pop":3},"vars":{"frontier":"5@2 2@0","output":"9,8,7,6"},"note":"Pop 4: the heap held 6@0 5@2, so the entry 6@0 leaves and the output gains 6. Account 0 pushes its next post 2."},{"at":{"pop":4},"vars":{"frontier":"2@0","output":"9,8,7,6,5"},"note":"Pop 5: the heap held 5@2 2@0, so the entry 5@2 leaves and the output gains 5. Account 2 has no older post, so it adds no entry."}]}
```

At the second pop, account 1 contributes its next post only after its first post leaves the heap. The heap never holds more than three entries, one for each account.

#### A Service With A Deleted Account

The second trace follows calls on a service. Account 1 follows account 2, tries to follow itself, and then account 2 is deleted. The pointer `call` sits on the newest call, while the column `follows` shows the stored follow set of account 1.

```trace
{"cells":["post(2,20)","post(1,10)","follow(1,2)","follow(1,1)","feed(1,5)","deleteUser(2)","feed(1,5)","unfollow(1,2)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"follows":"{}","result":"true"},"note":"Call 0: account 2 is live, so the post is stored."},{"at":{"call":1},"vars":{"follows":"{}","result":"true"},"note":"Call 1: account 1 is live, so the post is stored."},{"at":{"call":2},"vars":{"follows":"{2}","result":"true"},"note":"Call 2: both accounts are live and the edge is new, so account 1 follows account 2."},{"at":{"call":3},"vars":{"follows":"{2}","result":"false"},"note":"Call 3: the ids are equal, so the call returns false and the follow set does not change."},{"at":{"call":4},"vars":{"follows":"{2}","result":"10,20"},"note":"Call 4: the visibility check admits account 1 and account 2, so the merge returns 10,20."},{"at":{"call":5},"vars":{"follows":"{2}","result":"true"},"note":"Call 5: account 2 joins the deleted set, and no follow set changes."},{"at":{"call":6},"vars":{"follows":"{2}","result":"10"},"note":"Call 6: the visibility check admits account 1, so the merge returns 10."},{"at":{"call":7},"vars":{"follows":"{}","result":"true"},"note":"Call 7: the stale edge to the deleted account 2 is removed from the follow set."}]}
```

The self-follow call returns false and changes nothing, so the post of account 1 appears once in the feed. After the deletion the follow set still holds account 2, which is a stale entry. The second feed call skips it through the visibility check, and the unfollow call finally removes the entry.

<!-- stage: code -->
### The Merge With A Visibility Check

The class stores each author's posts in an `ArrayList` and merges only eligible authors.

```java
final class FeedService {
    private final Map<Integer, List<int[]>> posts = new HashMap<>();   // author -> {time, id}, oldest first
    private final Map<Integer, Set<Integer>> follows = new HashMap<>();
    private final Set<Integer> deleted = new HashSet<>();
    private int clock = 0;

    void post(int user, int id) {
        posts.computeIfAbsent(user, x -> new ArrayList<>()).add(new int[] {clock++, id});
    }

    List<Integer> feed(int user, int k) {
        List<Integer> out = new ArrayList<>();
        if (deleted.contains(user)) return out;
        List<Integer> authors = new ArrayList<>();
        authors.add(user);                                            // own account once
        for (int b : follows.getOrDefault(user, Set.of()))
            if (b != user && !deleted.contains(b)) authors.add(b);    // visibility check before the heap
        PriorityQueue<int[]> heap = new PriorityQueue<>((p, q) -> q[0] - p[0]);   // {time, id, author, index}
        for (int a : authors) {
            List<int[]> list = posts.getOrDefault(a, List.of());
            if (!list.isEmpty()) {
                int[] last = list.get(list.size() - 1);
                heap.add(new int[] {last[0], last[1], a, list.size() - 1});
            }
        }
        while (out.size() < k && !heap.isEmpty()) {                   // at most k pops
            int[] top = heap.poll();
            out.add(top[1]);
            if (top[3] > 0) {                                         // next older post of the same author
                int[] nxt = posts.get(top[2]).get(top[3] - 1);
                heap.add(new int[] {nxt[0], nxt[1], top[2], top[3] - 1});
            }
        }
        return out;
    }
}
```

A query costs O(f + k log f) for f eligible accounts. The space is O(f) for the heap and the author list.

<!-- stage: applicability -->
### Queries That Return The Newest Few

#### Recognizing The Pattern

The cue is a query that returns the newest or highest-ranked `k` items from several sources, where each source already holds its items in order. Examples are a timeline, a merged log from several files and the next events from several calendars. Name the sources, name the order inside each source, and name every rule that removes a source or an item. The invariant is that filtering runs before the limit, and that the heap holds one entry for each source that still has items.

#### Policies To State

Write down the tie policy, such as the smaller source index first when two items have equal time. Write down what a user following themselves means, what a follow of a deleted account returns, and whether ids can be reused. A policy stated in the contract becomes an assertion in the tests. A policy left unstated becomes an argument later.

#### False Friends

Sorting the union and cutting it at `k` looks like the same answer, and it is a false friend whenever the sources are large. Applying the limit first and the filter second is a false friend of the correct order, because the answer shrinks below `k`. Removing a deleted account from every follower set on delete looks tidy, yet it costs time proportional to the number of followers, while a check at query time costs nothing extra. A single source needs no heap, because its own list is already the answer.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Recent User Streams (Author exercise)
<!-- id: sv-merge-streams -->

**Prerequisites.** Priority queues and sorted arrays.

**Problem.** Given `m` streams, where `streams[s]` is an array of integer timestamps in non-increasing order, and an integer `k`, return the `k` newest items across all streams. An item is the pair `(s, p)` of a stream index and a position in that stream. Item `(s, p)` is newer than `(t, q)` when its timestamp is larger, and when timestamps are equal, the item with the smaller stream index is newer. When both are in the same stream with equal timestamps, the smaller position is newer. Return the pairs from newest to oldest, or all items if fewer than `k` exist.

**Constraints.** The limits are:
- **Streams** number from 0 to 1000, and each stream has from 0 to 1000 timestamps.
- **Timestamps** are integers from 0 to 10^9.
- **k** is an integer from 0 to 10^5.
- **Return** is a list of `int[]{s, p}` pairs.

**Example 1.** Input `streams = [[9,6,2],[8,7],[5]]`, `k = 4`, output `(0,0)`, `(1,0)`, `(1,1)`, `(0,1)`.

**Example 2.** Input `streams = [[5,5],[5],[]]`, `k = 3`, output `(0,0)`, `(0,1)`, `(1,0)`.

**Hint.** Which single entry of each stream can be the next answer?

**Changed decision.** The heap holds one entry per stream, and the code pushes the next position of a stream only after that stream's current entry leaves.

#### [Vary] Design Twitter (LeetCode 355)
<!-- id: sv-twitter-feed -->

**Prerequisites.** The merge exercise above and hash sets.

**Problem.** This contract is the chapter's own and differs from LeetCode in the feed size and the storage rule. Design a class `Twitter`. The call `postTweet(userId, tweetId)` records a tweet with the next time value. A user keeps only their five newest tweets, and older ones are dropped. The call `follow(a, b)` adds `b` to the followees of `a`, and `unfollow(a, b)` removes it. A call with `a == b` changes nothing. The call `getNewsFeed(userId, k)` returns up to `k` tweet ids, newest first, from the user's own tweets and the tweets of the user's followees.

**Constraints.** The limits are:
- **Users** are integers from 1 to 10^5, and **tweet ids** are distinct integers from 1 to 10^9.
- **Calls** number at most 10^5, and `k` is an integer from 1 to 100.
- **Followees** of one user number at most 10^3.
- **Return** of `getNewsFeed` is a list of ids, empty when no tweet is visible.

**Example 1.** Input calls `postTweet(1,101)`, `postTweet(2,201)`, `postTweet(2,202)`, `follow(1,2)`, `getNewsFeed(1,2)`, output the list 202, 201.

**Example 2.** Input calls `postTweet(1,1)` to `postTweet(1,7)` in order, then `getNewsFeed(1,10)`, `follow(2,1)`, `unfollow(2,1)`, `getNewsFeed(2,3)`, output the list 7, 6, 5, 4, 3 and then the empty list.

**Hint.** Which index of an author's list holds the newest tweet, and what is the next entry after it leaves the heap?

**Changed decision.** The newest five tweets bound each author's list, and the feed length is a parameter, so the merge stops after `k` pops and not after a fixed ten.

#### [Boundary] Follow Self And Deleted Source (Author exercise)
<!-- id: sv-follow-self-deleted -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Network` of users with integer ids. Every id is a live user until `deleteUser(u)` marks it deleted, and a deleted id never becomes live again. The call `post(u, id)` stores a tweet and returns `true` when `u` is live. The call `follow(a, b)` returns `true` and adds the edge when `a` and `b` are different, both are live and the edge is new. The call `unfollow(a, b)` returns `true` and removes the edge when `a` is live and the edge exists, even if `b` is deleted. The call `deleteUser(u)` returns `true` when `u` was live. The call `feed(u, k)` returns up to `k` tweet ids, newest first, from `u` and from the live followees of `u`, and returns an empty list when `u` is deleted. The call `liveFollowees(u)` returns the number of live followees of `u`.

**Constraints.** The limits are:
- **Users** are integers from 1 to 10^5, and **tweet ids** are distinct integers.
- **Calls** number at most 10^5, and `k` is an integer from 1 to 100.
- **Tweets** are never removed from storage, and a deleted author's tweets stay hidden.
- **Return** types are `boolean` for `post`, `follow`, `unfollow` and `deleteUser`, a list for `feed` and an `int` for `liveFollowees`.

**Example 1.** Input calls `post(1,10)`, `post(2,20)`, `follow(1,2)`, `follow(1,1)`, `follow(1,2)`, `feed(1,5)`, `deleteUser(2)`, `feed(1,5)`, `liveFollowees(1)`, `follow(1,2)`, `unfollow(1,2)`, output `true`, `true`, `true`, `false`, `false`, the list 20, 10, then `true`, the list 10, 0, `false` and `true`.

**Example 2.** Input calls `post(3,30)`, `post(3,31)`, `deleteUser(3)`, `post(3,32)`, `feed(3,5)`, `deleteUser(3)`, output `true`, `true`, `true`, `false`, the empty list and `false`.

**Hint.** Where does the code check that an author is live, and does that place come before or after the limit of `k`?

**Changed decision.** Follow edges to a deleted user stay stored and the feed skips them, so the delete call costs O(1) and the unfollow call must still accept a stale edge.

#### [Recognize] Design Video Sharing Platform (LeetCode 2254)
<!-- id: sv-video-platform -->

**Prerequisites.** Priority queues and the three exercises above.

**Problem.** This contract is written from the title and is the chapter's own, so it can differ from LeetCode. Design a class `Videos`. The call `upload(video)` stores a digit string and returns the smallest id not held by a stored video, counting from 0. The call `remove(id)` deletes a stored video and returns `true`, and the id becomes free. The call `watch(id, start, end)` returns the characters at positions `start` through `min(end, length - 1)` and adds one view, but it returns `"-1"` and changes nothing when the id is not stored or `start >= length`. The calls `like(id)` and `dislike(id)` add one to the matching counter of a stored video and do nothing otherwise. The call `getLikesAndDislikes(id)` returns `[likes, dislikes]`, or `[-1]` for an unknown id. The call `getViews(id)` returns the view count, or -1 for an unknown id. A video that reuses a freed id starts with zero views, likes and dislikes.

**Constraints.** The limits are:
- **Video** strings have from 1 to 10^5 digits, and their total length is at most 10^5.
- **Ids** are integers from 0 to 10^5, and **positions** satisfy `0 <= start <= end <= 10^5`.
- **Calls** number at most 10^5.
- **Return** types are `int` for `upload` and `getViews`, `String` for `watch`, `boolean` for `remove` and `int[]` for `getLikesAndDislikes`.

**Example 1.** Input calls `upload("123")`, `upload("456")`, `remove(0)`, `upload("789")`, `watch(0,1,5)`, `getViews(0)`, output 0, 1, `true`, 0, `"89"` and 1.

**Example 2.** Input calls `upload("12")`, `watch(0,2,3)`, `like(0)`, `getLikesAndDislikes(0)`, `remove(5)`, `remove(0)`, `getViews(0)`, output 0, `"-1"`, then `[1,0]`, `false`, `true` and -1.

**Hint.** Which structure returns the smallest freed id, and when does the counter for a new id advance?

**Changed decision.** This is a transfer of the lesson: the id pool replaces the follow state and a removed video carries no stale index, so reuse must reset every counter. The contract is the chapter's own and need not match LeetCode.
