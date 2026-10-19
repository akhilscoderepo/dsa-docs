<!-- solutions-for: 04-feed-aggregation -->
### Solutions For Merge Feeds From Many Sources

#### Solution: [Build] Merge Recent User Streams (Author exercise)
<!-- id: sv-merge-streams -->

**Approach.** Each stream is already sorted, so the newest unreturned item of a stream is always the item at its current position. The heap holds one entry per stream that still has items, ordered by larger timestamp first and by smaller stream index when timestamps are equal. Each pop returns the newest remaining item overall. The code then pushes the next position of the popped stream, if there is one. Within one stream the next position always has a timestamp no larger than the popped one, and the heap holds only one entry per stream, so equal timestamps in one stream leave in position order.

The invariant is that the heap holds exactly the current position of every stream that has unreturned items. The answer is therefore complete after `k` pops.

**Complexity.**

- **Time** is O(m + k log m) for m streams, because building the heap costs one push per stream and each of the at most `k` pops costs O(log m).
- **Space** is O(m) for the heap, plus O(k) for the returned list.

```java run
import java.util.*;

public final class MergeStreamsSolution {
    /**
     * Returns the k newest items of sorted streams as {stream, position} pairs.
     * Time: O(m + k log m).
     * Space: O(m + k).
     * Invariant: the heap holds the current position of each non-exhausted stream.
     */
    static List<int[]> newest(int[][] streams, int k) {
        List<int[]> out = new ArrayList<>();
        // Larger timestamp first; the smaller stream index wins a tie.
        PriorityQueue<int[]> heap = new PriorityQueue<>((p, q) -> {
            int tp = streams[p[0]][p[1]], tq = streams[q[0]][q[1]];
            return tp != tq ? Integer.compare(tq, tp) : Integer.compare(p[0], q[0]);
        });
        // One starting entry per non-empty stream.
        for (int s = 0; s < streams.length; s++) if (streams[s].length > 0) heap.add(new int[] {s, 0});
        // At most k pops, each costing O(log m).
        while (out.size() < k && !heap.isEmpty()) {
            int[] top = heap.poll();
            out.add(top);
            // The next position of the same stream becomes its new entry.
            if (top[1] + 1 < streams[top[0]].length) heap.add(new int[] {top[0], top[1] + 1});
        }
        return out;
    }

    static String show(List<int[]> r) {
        StringBuilder sb = new StringBuilder();
        for (int[] p : r) sb.append('(').append(p[0]).append(',').append(p[1]).append(')');
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        if (!show(newest(new int[][] {{9, 6, 2}, {8, 7}, {5}}, 4)).equals("(0,0)(1,0)(1,1)(0,1)")) throw new AssertionError("e1");
        if (!show(newest(new int[][] {{5, 5}, {5}, {}}, 3)).equals("(0,0)(0,1)(1,0)")) throw new AssertionError("e2");
        // Random streams checked against sorting every item with the same tie rule.
        Random rnd = new Random(4101);
        for (int round = 0; round < 500; round++) {
            int m = rnd.nextInt(6);
            int[][] st = new int[m][];
            for (int s = 0; s < m; s++) {
                st[s] = new int[rnd.nextInt(6)];
                for (int i = 0; i < st[s].length; i++) st[s][i] = rnd.nextInt(8);
                Arrays.sort(st[s]);
                for (int i = 0; i < st[s].length / 2; i++) { int t = st[s][i]; st[s][i] = st[s][st[s].length - 1 - i]; st[s][st[s].length - 1 - i] = t; }
            }
            int k = rnd.nextInt(20);
            List<int[]> all = new ArrayList<>();
            for (int s = 0; s < m; s++) for (int i = 0; i < st[s].length; i++) all.add(new int[] {s, i});
            all.sort((p, q) -> {
                int tp = st[p[0]][p[1]], tq = st[q[0]][q[1]];
                if (tp != tq) return Integer.compare(tq, tp);
                return p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]);
            });
            String want = show(all.subList(0, Math.min(k, all.size())));
            if (!show(newest(st, k)).equals(want)) throw new AssertionError("random " + round);
        }
    }
}
```

#### Solution: [Vary] Design Twitter (LeetCode 355)
<!-- id: sv-twitter-feed -->

**Approach.** The authoritative state is a map from author to the list of that author's last five tweets, each stored with its post time, and a map from user to a set of followees. A post call appends to the author's list and drops the oldest entry when the list exceeds five. A follow call with `a == b` returns at once, so a user never appears in their own followee set and never contributes two sources.

A feed call builds the source list from the user and the followees, then runs the heap merge. Each heap entry names an author and an index into that author's list, starting at the newest index. A pop returns one tweet id and pushes the next older index of the same author.

The invariant is that the heap holds the newest unreturned tweet of each source that has one. The merge stops after `k` pops.

**Complexity.**

- **Time** is O(f + k log f) per feed call for f followees, and O(1) for post, follow and unfollow, because each list has at most five entries.
- **Space** is O(f) for the heap per query, and O(5u + e) overall for u authors and e follow edges.

```java run
import java.util.*;

public final class TwitterSolution {
    static final class Twitter {
        private static final int KEEP = 5;
        private final Map<Integer, ArrayList<int[]>> posts = new HashMap<>();   // author -> {time, id}, oldest first
        private final Map<Integer, Set<Integer>> follows = new HashMap<>();
        private int clock = 0;

        /** Records a tweet and keeps the newest five; O(1) time and space; invariant: list size at most KEEP. */
        void postTweet(int user, int id) {
            ArrayList<int[]> list = posts.computeIfAbsent(user, x -> new ArrayList<>());
            list.add(new int[] {clock++, id});
            // The list never exceeds five entries, so the removal costs O(1).
            if (list.size() > KEEP) list.remove(0);
        }

        // A self follow changes nothing; O(1) time and space.
        void follow(int a, int b) { if (a != b) follows.computeIfAbsent(a, x -> new HashSet<>()).add(b); }

        // Removing an absent edge is allowed and changes nothing; O(1) time and space.
        void unfollow(int a, int b) { if (follows.containsKey(a)) follows.get(a).remove(b); }

        /**
         * Returns up to k tweet ids, newest first, from the user and the followees.
         * Time: O(f + k log f).
         * Space: O(f).
         * Invariant: the heap holds the newest unreturned tweet of each source.
         */
        List<Integer> getNewsFeed(int user, int k) {
            List<Integer> authors = new ArrayList<>();
            authors.add(user);
            authors.addAll(follows.getOrDefault(user, Set.of()));
            // Entries are {time, id, author, index}; the newest time leaves first.
            PriorityQueue<int[]> heap = new PriorityQueue<>((p, q) -> Integer.compare(q[0], p[0]));
            // One starting entry per source that has at least one tweet.
            for (int a : authors) {
                ArrayList<int[]> list = posts.get(a);
                if (list != null && !list.isEmpty()) {
                    int[] last = list.get(list.size() - 1);
                    heap.add(new int[] {last[0], last[1], a, list.size() - 1});
                }
            }
            List<Integer> out = new ArrayList<>();
            // At most k pops.
            while (out.size() < k && !heap.isEmpty()) {
                int[] top = heap.poll();
                out.add(top[1]);
                // The next older tweet of the same author becomes its entry.
                if (top[3] > 0) {
                    int[] nxt = posts.get(top[2]).get(top[3] - 1);
                    heap.add(new int[] {nxt[0], nxt[1], top[2], top[3] - 1});
                }
            }
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Twitter a = new Twitter();
        a.postTweet(1, 101); a.postTweet(2, 201); a.postTweet(2, 202); a.follow(1, 2);
        if (!a.getNewsFeed(1, 2).equals(List.of(202, 201))) throw new AssertionError("e1");
        // Example 2: only five tweets remain, and an unfollow removes the source.
        Twitter b = new Twitter();
        for (int i = 1; i <= 7; i++) b.postTweet(1, i);
        if (!b.getNewsFeed(1, 10).equals(List.of(7, 6, 5, 4, 3))) throw new AssertionError("e2 cap");
        b.follow(2, 1); b.unfollow(2, 1);
        if (!b.getNewsFeed(2, 3).isEmpty()) throw new AssertionError("e2 unfollow");
        // A self follow must not repeat the user's own tweets.
        Twitter c = new Twitter();
        c.postTweet(1, 9); c.follow(1, 1);
        if (!c.getNewsFeed(1, 5).equals(List.of(9))) throw new AssertionError("self follow");
        // Random calls checked against a full scan of all stored tweets.
        Random rnd = new Random(355);
        for (int round = 0; round < 400; round++) {
            Twitter s = new Twitter();
            List<int[]> log = new ArrayList<>();                        // {time, id, author}
            Map<Integer, Set<Integer>> fol = new HashMap<>();
            int nextId = 1;
            for (int op = 0; op < 80; op++) {
                int t = rnd.nextInt(5), u = rnd.nextInt(4), v = rnd.nextInt(4);
                if (t <= 1) { s.postTweet(u, nextId); log.add(new int[] {log.size(), nextId, u}); nextId++; }
                else if (t == 2) { s.follow(u, v); if (u != v) fol.computeIfAbsent(u, x -> new HashSet<>()).add(v); }
                else if (t == 3) { s.unfollow(u, v); if (fol.containsKey(u)) fol.get(u).remove(v); }
                else {
                    int k = 1 + rnd.nextInt(12);
                    Set<Integer> src = new HashSet<>(fol.getOrDefault(u, Set.of()));
                    src.add(u);
                    List<int[]> keep = new ArrayList<>();
                    for (int a2 : src) {
                        List<int[]> mine = new ArrayList<>();
                        for (int[] p : log) if (p[2] == a2) mine.add(p);
                        keep.addAll(mine.subList(Math.max(0, mine.size() - 5), mine.size()));
                    }
                    keep.sort((p, q) -> Integer.compare(q[0], p[0]));
                    List<Integer> want = new ArrayList<>();
                    for (int i = 0; i < Math.min(k, keep.size()); i++) want.add(keep.get(i)[1]);
                    if (!s.getNewsFeed(u, k).equals(want)) throw new AssertionError("feed " + round);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Follow Self And Deleted Source (Author exercise)
<!-- id: sv-follow-self-deleted -->

**Approach.** The authoritative state has three parts: a list of tweets per author, a follow set per user and a set of deleted ids. Every rule is a check on those parts. A post call checks that the author is not deleted. A follow call rejects equal ids, deleted endpoints and an existing edge. An unfollow call checks only that the actor is live and that the edge exists, so a stale edge to a deleted user can still be removed. A delete call adds the id to the deleted set and touches nothing else.

The feed call applies the visibility check before any heap entry exists. It returns an empty list for a deleted user, admits the user once, and admits each followee that is not deleted. The followee count call counts the same admitted followees. Because deleted sources never enter the heap, the limit `k` counts only visible tweets.

The invariant is that every source in the heap is live and appears once. Follow sets may hold stale entries, and only the check at query time hides them.

**Complexity.**

- **Time** is O(1) for post, follow, unfollow and delete, O(f) for the followee count and O(f + k log f) for a feed call with f stored followees.
- **Space** is O(t + e + d) for t tweets, e edges and d deleted ids, plus O(f) per query.

```java run
import java.util.*;

public final class FollowSelfDeletedSolution {
    static final class Network {
        private final Map<Integer, List<int[]>> posts = new HashMap<>();   // author -> {time, id}, oldest first
        private final Map<Integer, Set<Integer>> follows = new HashMap<>();
        private final Set<Integer> deleted = new HashSet<>();
        private int clock = 0;

        /** Stores a tweet for a live author; O(1) time and space; invariant: deleted authors gain no tweets. */
        boolean post(int u, int id) {
            if (deleted.contains(u)) return false;
            posts.computeIfAbsent(u, x -> new ArrayList<>()).add(new int[] {clock++, id});
            return true;
        }

        // Every precondition is checked before the single write; O(1) time and space.
        boolean follow(int a, int b) {
            if (a == b || deleted.contains(a) || deleted.contains(b)) return false;
            return follows.computeIfAbsent(a, x -> new HashSet<>()).add(b);   // false when the edge exists
        }

        // A stale edge to a deleted user is removable; O(1) time and space.
        boolean unfollow(int a, int b) {
            if (deleted.contains(a)) return false;
            Set<Integer> s = follows.get(a);
            return s != null && s.remove(b);
        }

        // Lazy delete: follow sets are not touched; O(1) time and space.
        boolean deleteUser(int u) { return deleted.add(u); }

        // Counts only live followees, so stale edges do not count; O(f) time, O(1) space.
        int liveFollowees(int u) {
            if (deleted.contains(u)) return 0;
            int n = 0;
            for (int b : follows.getOrDefault(u, Set.of())) if (!deleted.contains(b)) n++;
            return n;
        }

        /**
         * Returns up to k visible tweet ids, newest first.
         * Time: O(f + k log f).
         * Space: O(f).
         * Invariant: only live, distinct sources enter the heap.
         */
        List<Integer> feed(int u, int k) {
            List<Integer> out = new ArrayList<>();
            if (deleted.contains(u)) return out;
            List<Integer> authors = new ArrayList<>();
            authors.add(u);
            // The visibility check runs here, before any heap entry exists.
            for (int b : follows.getOrDefault(u, Set.of())) if (!deleted.contains(b)) authors.add(b);
            PriorityQueue<int[]> heap = new PriorityQueue<>((p, q) -> Integer.compare(q[0], p[0]));
            for (int a : authors) {
                List<int[]> list = posts.get(a);
                if (list != null && !list.isEmpty()) {
                    int[] last = list.get(list.size() - 1);
                    heap.add(new int[] {last[0], last[1], a, list.size() - 1});
                }
            }
            // At most k pops.
            while (out.size() < k && !heap.isEmpty()) {
                int[] top = heap.poll();
                out.add(top[1]);
                if (top[3] > 0) {
                    int[] nxt = posts.get(top[2]).get(top[3] - 1);
                    heap.add(new int[] {nxt[0], nxt[1], top[2], top[3] - 1});
                }
            }
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Network n = new Network();
        boolean[] r1 = {n.post(1, 10), n.post(2, 20), n.follow(1, 2), n.follow(1, 1), n.follow(1, 2)};
        if (!r1[0] || !r1[1] || !r1[2] || r1[3] || r1[4]) throw new AssertionError("e1 calls");
        if (!n.feed(1, 5).equals(List.of(20, 10))) throw new AssertionError("e1 feed");
        if (!n.deleteUser(2) || !n.feed(1, 5).equals(List.of(10)) || n.liveFollowees(1) != 0) throw new AssertionError("e1 delete");
        if (n.follow(1, 2) || !n.unfollow(1, 2)) throw new AssertionError("e1 stale");
        // Example 2 from the problem text.
        Network m = new Network();
        boolean ok = m.post(3, 30) && m.post(3, 31) && m.deleteUser(3) && !m.post(3, 32);
        if (!ok || !m.feed(3, 5).isEmpty() || m.deleteUser(3)) throw new AssertionError("e2");
        // The limit counts visible tweets only: a deleted source with newer tweets must not use up a slot.
        Network p = new Network();
        p.post(1, 1); p.post(2, 2); p.post(2, 3); p.follow(1, 2); p.deleteUser(2);
        if (!p.feed(1, 1).equals(List.of(1))) throw new AssertionError("limit before filter");
        // Random calls checked against a full scan with the same rules.
        Random rnd = new Random(4103);
        for (int round = 0; round < 500; round++) {
            Network s = new Network();
            List<int[]> log = new ArrayList<>();                        // {time, id, author}
            Map<Integer, Set<Integer>> fol = new HashMap<>();
            Set<Integer> dead = new HashSet<>();
            int nextId = 1;
            for (int op = 0; op < 80; op++) {
                int t = rnd.nextInt(7), u = rnd.nextInt(4), v = rnd.nextInt(4);
                if (t == 0 || t == 1) {
                    boolean want = !dead.contains(u);
                    if (want) { log.add(new int[] {log.size(), nextId, u}); }
                    if (s.post(u, nextId) != want) throw new AssertionError("post");
                    nextId++;
                } else if (t == 2) {
                    boolean want = u != v && !dead.contains(u) && !dead.contains(v) && !fol.getOrDefault(u, Set.of()).contains(v);
                    if (want) fol.computeIfAbsent(u, x -> new HashSet<>()).add(v);
                    if (s.follow(u, v) != want) throw new AssertionError("follow");
                } else if (t == 3) {
                    boolean want = !dead.contains(u) && fol.getOrDefault(u, Set.of()).contains(v);
                    if (want) fol.get(u).remove(v);
                    if (s.unfollow(u, v) != want) throw new AssertionError("unfollow");
                } else if (t == 4) {
                    if (s.deleteUser(u) != dead.add(u)) throw new AssertionError("delete");
                } else {
                    int k = 1 + rnd.nextInt(8);
                    List<Integer> want = new ArrayList<>();
                    int live = 0;
                    if (!dead.contains(u)) {
                        Set<Integer> src = new HashSet<>();
                        for (int b : fol.getOrDefault(u, Set.of())) if (!dead.contains(b)) { src.add(b); live++; }
                        src.add(u);
                        List<int[]> vis = new ArrayList<>();
                        for (int[] q : log) if (src.contains(q[2])) vis.add(q);
                        vis.sort((x, y) -> Integer.compare(y[0], x[0]));
                        for (int i = 0; i < Math.min(k, vis.size()); i++) want.add(vis.get(i)[1]);
                    }
                    if (!s.feed(u, k).equals(want)) throw new AssertionError("feed " + round);
                    if (s.liveFollowees(u) != live) throw new AssertionError("count");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Design Video Sharing Platform (LeetCode 2254)
<!-- id: sv-video-platform -->

**Approach.** The authoritative state is a map from id to a record of the video text and its three counters. The derived index is the id pool, made of a counter `next` for never-used ids and a min-heap of freed ids. An upload call takes the smallest freed id when the heap is not empty and otherwise takes `next` and advances it. This returns the smallest id that no stored video holds, because every id below `next` is either stored or in the freed heap.

A remove call deletes the record and pushes the id onto the freed heap, and it rejects an id that is not stored. A reused id gets a fresh record, so the counters of the earlier video never leak into the new one. A watch call validates the id and `start` before it writes, then adds one view and returns the substring. Like and dislike calls change one counter of a stored record.

The invariant is that each id is either a key of the record map or in the freed heap or at least `next`, and never in two of these places.

**Complexity.**

- **Time** is O(log n) for upload and remove because of the heap, and O(L) for a watch call that returns L characters. Likes, dislikes and views take O(1).
- **Space** is O(T + n), where T is the total length of the stored texts and n is the number of ids ever issued.

```java run
import java.util.*;

public final class VideoPlatformSolution {
    static final class Videos {
        private static final class Video {
            final String text; int views, likes, dislikes;
            Video(String text) { this.text = text; }
        }
        private final Map<Integer, Video> store = new HashMap<>();            // id -> record, source of truth
        private final PriorityQueue<Integer> freed = new PriorityQueue<>();   // derived: reusable ids
        private int next = 0;

        /** Stores a video under the smallest unused id; O(log n) time, O(1) extra space; invariant: ids are never shared. */
        int upload(String text) {
            int id = freed.isEmpty() ? next++ : freed.poll();
            store.put(id, new Video(text));
            return id;
        }

        // The id returns to the pool only when it was stored; O(log n) time, O(1) space.
        boolean remove(int id) {
            if (store.remove(id) == null) return false;
            freed.add(id);
            return true;
        }

        /** Returns the requested slice and counts a view; O(L) time for L returned characters, O(L) space. */
        String watch(int id, int start, int end) {
            Video v = store.get(id);
            // Both preconditions are checked before any counter changes.
            if (v == null || start >= v.text.length()) return "-1";
            v.views++;
            return v.text.substring(start, Math.min(end, v.text.length() - 1) + 1);
        }

        void like(int id) { Video v = store.get(id); if (v != null) v.likes++; }          // O(1)
        void dislike(int id) { Video v = store.get(id); if (v != null) v.dislikes++; }    // O(1)

        int[] getLikesAndDislikes(int id) {
            Video v = store.get(id);
            return v == null ? new int[] {-1} : new int[] {v.likes, v.dislikes};         // O(1)
        }

        int getViews(int id) { Video v = store.get(id); return v == null ? -1 : v.views; }   // O(1)
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Videos a = new Videos();
        if (a.upload("123") != 0 || a.upload("456") != 1 || !a.remove(0) || a.upload("789") != 0) throw new AssertionError("e1 ids");
        if (!a.watch(0, 1, 5).equals("89") || a.getViews(0) != 1) throw new AssertionError("e1 watch");
        // Example 2 from the problem text.
        Videos b = new Videos();
        if (b.upload("12") != 0 || !b.watch(0, 2, 3).equals("-1")) throw new AssertionError("e2 watch");
        b.like(0);
        if (!Arrays.equals(b.getLikesAndDislikes(0), new int[] {1, 0}) || b.remove(5) || !b.remove(0) || b.getViews(0) != -1) throw new AssertionError("e2");
        // A failed watch must not add a view, and a reused id starts clean.
        Videos c = new Videos();
        c.upload("99"); c.watch(0, 5, 6); c.like(0); c.dislike(0);
        if (c.getViews(0) != 0) throw new AssertionError("failed watch counted");
        c.watch(0, 0, 0); c.remove(0); c.upload("7");
        if (c.getViews(0) != 0 || !Arrays.equals(c.getLikesAndDislikes(0), new int[] {0, 0})) throw new AssertionError("stale counters");
        // Random calls checked against a list of slots where the oracle scans for the first empty slot.
        Random rnd = new Random(2254);
        for (int round = 0; round < 500; round++) {
            Videos s = new Videos();
            List<String> text = new ArrayList<>();
            List<int[]> cnt = new ArrayList<>();                         // {views, likes, dislikes}
            for (int op = 0; op < 80; op++) {
                int t = rnd.nextInt(7), id = rnd.nextInt(6);
                if (t == 0 || t == 1) {
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0, n = 1 + rnd.nextInt(5); i < n; i++) sb.append(rnd.nextInt(10));
                    int slot = text.indexOf(null);
                    if (slot < 0) { text.add(sb.toString()); cnt.add(new int[3]); slot = text.size() - 1; }
                    else { text.set(slot, sb.toString()); cnt.set(slot, new int[3]); }
                    if (s.upload(sb.toString()) != slot) throw new AssertionError("upload id");
                } else {
                    boolean live = id < text.size() && text.get(id) != null;
                    if (t == 2) {
                        if (s.remove(id) != live) throw new AssertionError("remove");
                        if (live) text.set(id, null);
                    } else if (t == 3) {
                        int st = rnd.nextInt(6), en = st + rnd.nextInt(6);
                        String want = "-1";
                        if (live && st < text.get(id).length()) { want = text.get(id).substring(st, Math.min(en, text.get(id).length() - 1) + 1); cnt.get(id)[0]++; }
                        if (!s.watch(id, st, en).equals(want)) throw new AssertionError("watch");
                    } else if (t == 4) { s.like(id); if (live) cnt.get(id)[1]++; }
                    else if (t == 5) { s.dislike(id); if (live) cnt.get(id)[2]++; }
                    else {
                        int[] wantLd = live ? new int[] {cnt.get(id)[1], cnt.get(id)[2]} : new int[] {-1};
                        if (!Arrays.equals(s.getLikesAndDislikes(id), wantLd)) throw new AssertionError("likes");
                        if (s.getViews(id) != (live ? cnt.get(id)[0] : -1)) throw new AssertionError("views");
                    }
                }
            }
        }
    }
}
```
