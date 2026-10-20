<!-- solutions-for: 02-expiring-state -->
### Solutions For Expiring State

#### Solution: [Build] Logger Rate Limiter (LeetCode 359)
<!-- id: st38-logger-rate-limiter -->

**Approach.**
The class keeps one map from message to the first timestamp at which that message may print again. A call looks up its message. When a deadline exists and the call time is below it, the call returns `false` and writes nothing. Otherwise the call stores `timestamp + gap` and returns `true`. The invariant is that the stored deadline of a message equals the latest accepted timestamp plus `gap`, so no earlier print can matter. A call at exactly the deadline prints, because the print at `timestamp - gap` lies outside the blocking window.

The method `purge` removes entries whose deadline is at or below the given time. The harness runs purges at random moments and asserts that no answer changes, which shows that physical cleanup is separate from validity. The oracle keeps the full list of accepted prints and scans it.

**Complexity.**
- **Time** is O(1) expected per call, because one hash lookup and at most one hash write run, and `purge` costs O(size) when it is called.
- **Space** is O(d) for `d` distinct messages, since each message keeps one `long`, and a purge lowers it to the messages still blocked.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class LoggerBuild {
    static final class Logger {
        private final long gap;
        private final HashMap<String, Long> deadline = new HashMap<>();

        Logger(long gap) {
            // The gap is fixed for the object, so every deadline uses one rule.
            this.gap = gap;
        }

        /**
         * Decides whether a message may print at the given time.
         * Time: O(1) expected. Space: O(1) extra per new message.
         * Invariant: deadline.get(m) equals the latest accepted time of m plus gap.
         */
        boolean shouldPrint(long timestamp, String message) {
            // One lookup finds the only state that can block this message.
            Long d = deadline.get(message);
            // A stored deadline above the clock means the earlier print still blocks.
            if (d != null && timestamp < d) return false;
            // The call is accepted, so the deadline moves to timestamp + gap.
            deadline.put(message, timestamp + gap);
            return true;
        }

        /**
         * Removes entries that no longer block anything.
         * Time: O(size). Space: O(1).
         * Invariant: removed entries had deadline <= now, so answers do not change.
         */
        void purge(long now) {
            // Removal only touches entries that validation already ignores.
            deadline.values().removeIf(d -> d <= now);
        }

        int size() { return deadline.size(); }
    }

    /** Brute force: scans every accepted print. */
    static final class Oracle {
        private final long gap;
        private final List<String> texts = new ArrayList<>();
        private final List<Long> times = new ArrayList<>();
        Oracle(long gap) { this.gap = gap; }
        boolean shouldPrint(long t, String m) {
            // Blocked when some accepted print of m has time greater than t - gap.
            for (int i = 0; i < texts.size(); i++)
                if (texts.get(i).equals(m) && times.get(i) > t - gap) return false;
            texts.add(m);
            times.add(t);
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise.
        Logger a = new Logger(4);
        if (!a.shouldPrint(2, "x") || a.shouldPrint(5, "x") || !a.shouldPrint(6, "x") || !a.shouldPrint(6, "y"))
            throw new AssertionError("example 1");
        Logger b = new Logger(3);
        if (!b.shouldPrint(0, "q") || b.shouldPrint(0, "q") || !b.shouldPrint(3, "q")) throw new AssertionError("example 2");
        // Large timestamps stay exact because the deadline is a long.
        Logger big = new Logger(1_000_000_000L);
        if (!big.shouldPrint(1_000_000_000_000L, "z") || big.shouldPrint(1_000_000_000_000L + 999_999_999L, "z")
            || !big.shouldPrint(1_000_000_000_000L + 1_000_000_000L, "z")) throw new AssertionError("long width");
        // Random streams compare every answer with the brute force, with random purges in between.
        Random rnd = new Random(3801L);
        for (int t = 0; t < 3000; t++) {
            long gap = 1 + rnd.nextInt(6);
            Logger real = new Logger(gap);
            Oracle model = new Oracle(gap);
            long now = rnd.nextInt(3);
            int calls = rnd.nextInt(30);
            for (int c = 0; c < calls; c++) {
                // The clock repeats or advances, never decreases.
                now += rnd.nextInt(4);
                String m = String.valueOf((char) ('a' + rnd.nextInt(4)));
                if (real.shouldPrint(now, m) != model.shouldPrint(now, m)) throw new AssertionError("answer differs");
                if (rnd.nextInt(5) == 0) {
                    real.purge(now);
                    // After a purge every stored message is still blocked, so memory tracks live entries.
                    if (real.size() > 4) throw new AssertionError("purge left too much");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Authentication Manager (LeetCode 1797)
<!-- id: st38-authentication-manager -->

**Approach.**
Every token has the same time to live and the clock never decreases. The expiry of a token is therefore its latest generate or renew time plus `timeToLive`, so tokens sorted by latest touch are also sorted by expiry. A `LinkedHashMap` keeps tokens in that order when a renewed or regenerated token is removed and put again at the back. The front of the map always holds the smallest expiry.

Each public method first purges the front while the front expiry is at or below the current time. After the purge, every remaining token is live, so `countUnexpiredTokens` returns the map size. A renew then needs only to test membership, because an ended token was just removed. The invariant is that the map contains the tokens with expiry above the latest clock reading, in non-decreasing expiry order. The oracle stores expiries in a `HashMap` and counts them with a full scan.

**Complexity.**
- **Time** is O(1) amortized per call, because each token enters the map once per generate or renew and leaves the front at most once for each entry.
- **Space** is O(t) for `t` tokens not yet purged, and the purge on every call keeps `t` equal to the live tokens after the call.

```java run
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Random;

public final class AuthenticationManagerVary {
    static final class AuthenticationManager {
        private final long timeToLive;
        private final LinkedHashMap<String, Long> expiry = new LinkedHashMap<>();

        AuthenticationManager(long timeToLive) {
            // The shared time to live keeps expiry order equal to touch order.
            this.timeToLive = timeToLive;
        }

        /**
         * Removes tokens from the front while they have ended.
         * Time: O(r) for r removed entries, amortized O(1). Space: O(1).
         * Invariant: afterwards every stored expiry is above now.
         */
        private void purge(long now) {
            Iterator<Map.Entry<String, Long>> it = expiry.entrySet().iterator();
            // The loop stops at the first live entry, because later entries end later.
            while (it.hasNext() && it.next().getValue() <= now) it.remove();
        }

        /**
         * Creates or recreates a token.
         * Time: O(1) amortized. Space: O(1) per new token.
         * Invariant: the token sits at the back with the largest expiry.
         */
        void generate(String tokenId, long currentTime) {
            purge(currentTime);
            // Removing first makes a reused id move to the back instead of keeping an old slot.
            expiry.remove(tokenId);
            expiry.put(tokenId, currentTime + timeToLive);
        }

        /**
         * Renews a token that has not ended.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: an ended token is absent, so presence means live.
         */
        void renew(String tokenId, long currentTime) {
            purge(currentTime);
            // Presence after the purge proves the token has not ended at currentTime.
            if (expiry.remove(tokenId) != null) expiry.put(tokenId, currentTime + timeToLive);
        }

        /**
         * Counts tokens that have not ended.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: after the purge the map size is the live count.
         */
        int countUnexpiredTokens(long currentTime) {
            purge(currentTime);
            return expiry.size();
        }
    }

    /** Brute force: counts by scanning every expiry. */
    static final class Oracle {
        private final long ttl;
        private final HashMap<String, Long> expiry = new HashMap<>();
        Oracle(long ttl) { this.ttl = ttl; }
        void generate(String id, long now) { expiry.put(id, now + ttl); }
        void renew(String id, long now) {
            Long e = expiry.get(id);
            if (e != null && e > now) expiry.put(id, now + ttl);
        }
        int count(long now) {
            int c = 0;
            for (long e : expiry.values()) if (e > now) c++;
            return c;
        }
    }

    public static void main(String[] args) {
        // Example 1: renewing before the end keeps a token, and the count falls to 0 later.
        AuthenticationManager m1 = new AuthenticationManager(6);
        m1.generate("p", 1); m1.generate("q", 3); m1.renew("p", 6);
        if (m1.countUnexpiredTokens(8) != 2 || m1.countUnexpiredTokens(12) != 0) throw new AssertionError("example 1");
        // Example 2: a renew at the exact end time is ignored, and an id can be generated again.
        AuthenticationManager m2 = new AuthenticationManager(2);
        m2.generate("m", 5); m2.renew("m", 7);
        if (m2.countUnexpiredTokens(7) != 0) throw new AssertionError("example 2 renew at expiry");
        m2.generate("m", 7);
        if (m2.countUnexpiredTokens(8) != 1) throw new AssertionError("example 2 regenerate");
        // Large times keep exact arithmetic with long.
        AuthenticationManager big = new AuthenticationManager(1_000_000_000L);
        big.generate("t", 1_000_000_000_000L);
        if (big.countUnexpiredTokens(1_000_000_000_000L + 999_999_999L) != 1
            || big.countUnexpiredTokens(1_000_000_000_000L + 1_000_000_000L) != 0) throw new AssertionError("long width");
        // Random call sequences compare every count with the brute force.
        Random rnd = new Random(3802L);
        for (int t = 0; t < 4000; t++) {
            long ttl = 1 + rnd.nextInt(6);
            AuthenticationManager real = new AuthenticationManager(ttl);
            Oracle model = new Oracle(ttl);
            long now = 1 + rnd.nextInt(3);
            for (int c = rnd.nextInt(40); c > 0; c--) {
                // The clock repeats or advances, never decreases.
                now += rnd.nextInt(4);
                String id = String.valueOf((char) ('a' + rnd.nextInt(5)));
                int op = rnd.nextInt(3);
                if (op == 0) { real.generate(id, now); model.generate(id, now); }
                else if (op == 1) { real.renew(id, now); model.renew(id, now); }
                else if (real.countUnexpiredTokens(now) != model.count(now)) throw new AssertionError("count differs");
            }
        }
    }
}
```

#### Solution: [Boundary] Renew At Expiry (Author exercise)
<!-- id: st38-renew-at-expiry -->

**Approach.**
The class stores one end time per key in a `HashMap` and never purges; it relies on validated reads. A private method `held` returns true only when an end time exists and the end is strictly greater than `now`. All three public methods call `held` before they write, so the equality case is decided once. At `now` equal to the end, `held` is false. `acquire` therefore succeeds and starts a new lease, `renew` fails and writes nothing, and `isHeld` returns false.

The invariant is that a rejected call writes no field, and a stored end time that is at or below the clock is treated as missing. The oracle stores the start time of each lease and tests `now - start < ttl`, which is a different representation of the same rule. The harness also asserts the three equality cases directly, since the random clock often lands on them.

**Complexity.**
- **Time** is O(1) expected per call, because each call performs one lookup and at most one write.
- **Space** is O(k) for `k` distinct keys ever acquired, since validated reads leave ended entries in the map until they are overwritten.

```java run
import java.util.HashMap;
import java.util.Random;

public final class RenewAtExpiryBoundary {
    static final class LeaseBook {
        private final long ttl;
        private final HashMap<String, Long> end = new HashMap<>();

        LeaseBook(long ttl) {
            // One lease length applies to every key.
            this.ttl = ttl;
        }

        /**
         * Tells whether the key holds a lease that has not ended.
         * Time: O(1) expected. Space: O(1).
         * Invariant: the comparison is strict, so now == end means ended.
         */
        private boolean held(String key, long now) {
            Long e = end.get(key);
            // A missing entry and an entry with end <= now are both not held.
            return e != null && e > now;
        }

        /**
         * Starts a lease when none is held.
         * Time: O(1) expected. Space: O(1) per new key.
         * Invariant: a false result writes nothing.
         */
        boolean acquire(String key, long now) {
            // The check runs before any write, so a held lease stays untouched.
            if (held(key, now)) return false;
            end.put(key, now + ttl);
            return true;
        }

        /**
         * Extends a lease that is held.
         * Time: O(1) expected. Space: O(1).
         * Invariant: an ended lease is never revived by renew.
         */
        boolean renew(String key, long now) {
            // At now == end the lease has ended, so renew must refuse.
            if (!held(key, now)) return false;
            end.put(key, now + ttl);
            return true;
        }

        /**
         * Reports whether the lease has not ended.
         * Time: O(1) expected. Space: O(1).
         * Invariant: the call changes no field.
         */
        boolean isHeld(String key, long now) {
            return held(key, now);
        }
    }

    /** Brute force: stores the start of the latest lease and tests elapsed time. */
    static final class Oracle {
        private final long ttl;
        private final HashMap<String, Long> start = new HashMap<>();
        Oracle(long ttl) { this.ttl = ttl; }
        boolean held(String k, long now) { Long s = start.get(k); return s != null && now - s < ttl; }
        boolean acquire(String k, long now) { if (held(k, now)) return false; start.put(k, now); return true; }
        boolean renew(String k, long now) { if (!held(k, now)) return false; start.put(k, now); return true; }
    }

    public static void main(String[] args) {
        // Example 1: at the exact end time the lease has ended, so renew fails and acquire succeeds.
        LeaseBook a = new LeaseBook(5);
        if (!a.acquire("k", 2) || !a.renew("k", 6) || a.isHeld("k", 11) || a.renew("k", 11) || !a.acquire("k", 11))
            throw new AssertionError("example 1");
        // Example 2: a rejected acquire changes nothing, and an acquire at the end time starts a new lease.
        LeaseBook b = new LeaseBook(3);
        if (!b.acquire("a", 0) || b.acquire("a", 2) || b.isHeld("a", 3) || !b.acquire("a", 3) || !b.renew("a", 5))
            throw new AssertionError("example 2");
        // The rejected acquire at time 2 must not have moved the end from 3 to 5.
        LeaseBook c = new LeaseBook(3);
        c.acquire("z", 0); c.acquire("z", 2);
        if (c.isHeld("z", 3)) throw new AssertionError("rejected call wrote state");
        // Large values stay exact with long.
        LeaseBook big = new LeaseBook(1_000_000_000_000L);
        big.acquire("w", 1_000_000_000_000L);
        if (!big.isHeld("w", 1_999_999_999_999L) || big.isHeld("w", 2_000_000_000_000L)) throw new AssertionError("long width");
        // Random sequences compare all three methods with the brute force.
        Random rnd = new Random(3803L);
        for (int t = 0; t < 4000; t++) {
            long ttl = 1 + rnd.nextInt(5);
            LeaseBook real = new LeaseBook(ttl);
            Oracle model = new Oracle(ttl);
            long now = rnd.nextInt(3);
            for (int s = rnd.nextInt(40); s > 0; s--) {
                // Small clock steps make many calls land exactly on an end time.
                now += rnd.nextInt(3);
                String key = String.valueOf((char) ('a' + rnd.nextInt(3)));
                int op = rnd.nextInt(3);
                boolean r, m;
                if (op == 0) { r = real.acquire(key, now); m = model.acquire(key, now); }
                else if (op == 1) { r = real.renew(key, now); m = model.renew(key, now); }
                else { r = real.isHeld(key, now); m = model.held(key, now); }
                if (r != m) throw new AssertionError("op " + op + " differs");
            }
        }
    }
}
```

#### Solution: [Recognize] Expiring Key Store (Author exercise)
<!-- id: st38-expiring-key-store -->

**Approach.**
Two designs share one rule: an entry is live when its end is strictly above `now`. The lazy design keeps a `HashMap` and validates every `get`. Its `liveCount` scans all entries, which costs O(size), and its memory keeps every ended key until it is overwritten. The heap design adds a min-heap of cleanup records ordered by end time. A record holds the end time and the key. Each method first pops records whose end is at or below `now`. It removes the map entry only when the entry for that key still has the same end time. An overwrite leaves the older record in the heap, and the check against the map makes that record harmless when it surfaces.

The invariant of the heap design is that every live entry has a record in the heap, and a popped record deletes the entry only when it describes the entry's current end. After a purge, the map size equals the live count, so `liveCount` is O(1) after the pops. The design never calls `PriorityQueue.remove(Object)`, which costs O(n). The extra memory is one record per `put`, and those records leave the heap when their time passes.

The harness runs both designs and the oracle on random streams and asserts that all three agree. It also asserts that the heap design holds no ended entries in its map after `liveCount`, while the lazy design may hold some.

**Complexity.**
- **Time** is O(log h) amortized per `put`, `get` and `liveCount` in the heap design, where `h` is the heap size, because each record is pushed and popped once.
- **Space** is O(h) for `h` records pushed and not yet popped, which counts live entries plus overwritten or ended ones waiting for their time. The lazy design uses O(k) for `k` distinct keys and answers `liveCount` in O(k).

```java run
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class ExpiringKeyStoreRecognize {
    /** Lazy design: validation on read, no cleanup. */
    static final class LazyStore {
        private final HashMap<String, long[]> map = new HashMap<>();   // value, end

        /**
         * Stores a value with its own time to live.
         * Time: O(1) expected. Space: O(1) per new key.
         * Invariant: the entry of a key holds its latest value and end.
         */
        void put(String key, long value, long ttl, long now) {
            // Overwriting replaces both fields at once.
            map.put(key, new long[]{value, now + ttl});
        }

        /**
         * Reads a value that has not ended.
         * Time: O(1) expected. Space: O(1).
         * Invariant: an entry with end <= now is never returned.
         */
        long get(String key, long now) {
            long[] e = map.get(key);
            // The strict comparison hides ended entries without deleting them.
            return e != null && e[1] > now ? e[0] : -1;
        }

        /**
         * Counts entries that have not ended.
         * Time: O(k) for k stored keys. Space: O(1).
         * Invariant: the count uses the same comparison as get.
         */
        int liveCount(long now) {
            int c = 0;
            // The scan visits every stored entry because nothing is ordered by end time.
            for (long[] e : map.values()) if (e[1] > now) c++;
            return c;
        }

        int physicalSize() { return map.size(); }
    }

    /** Heap design: records ordered by end time remove ended entries when time passes them. */
    static final class HeapStore {
        private record Rec(long end, String key) {}

        private final HashMap<String, long[]> map = new HashMap<>();   // value, end
        private final PriorityQueue<Rec> heap = new PriorityQueue<>((x, y) -> Long.compare(x.end, y.end));

        /**
         * Removes every entry whose end is at or below now.
         * Time: O(r log h) for r popped records, amortized O(log h) per push. Space: O(1).
         * Invariant: a record deletes an entry only when it matches the entry's current end.
         */
        private void purge(long now) {
            // The smallest end sits at the top, so the loop stops at the first record still in the future.
            while (!heap.isEmpty() && heap.peek().end <= now) {
                Rec r = heap.poll();
                long[] e = map.get(r.key);
                // A mismatch means the key was overwritten, so this record is stale and is skipped.
                if (e != null && e[1] == r.end) map.remove(r.key);
            }
        }

        /**
         * Stores a value with its own time to live.
         * Time: O(log h). Space: O(1) per call for one record.
         * Invariant: the new end always has a record in the heap.
         */
        void put(String key, long value, long ttl, long now) {
            purge(now);
            long end = now + ttl;
            map.put(key, new long[]{value, end});
            // The older record, if any, stays in the heap and is skipped when it surfaces.
            heap.add(new Rec(end, key));
        }

        /**
         * Reads a value that has not ended.
         * Time: amortized O(log h). Space: O(1).
         * Invariant: the extra end check keeps the answer valid even without the purge.
         */
        long get(String key, long now) {
            purge(now);
            long[] e = map.get(key);
            return e != null && e[1] > now ? e[0] : -1;
        }

        /**
         * Counts entries that have not ended.
         * Time: amortized O(log h). Space: O(1).
         * Invariant: after the purge the map holds only live entries.
         */
        int liveCount(long now) {
            purge(now);
            return map.size();
        }

        int physicalSize() { return map.size(); }
    }

    /** Brute force with a plain list of events replayed on every query. */
    static long oracleGet(java.util.List<long[]> puts, java.util.List<String> keys, String key, long now) {
        long best = -1;
        // The latest put of the key decides, whether or not it has ended.
        for (int i = puts.size() - 1; i >= 0; i--)
            if (keys.get(i).equals(key)) { best = puts.get(i)[1] > now ? puts.get(i)[0] : -1; break; }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: a shorter time to live ends v early, and u is still held.
        HeapStore h1 = new HeapStore();
        h1.put("u", 7, 10, 0); h1.put("v", 8, 2, 1);
        if (h1.get("v", 3) != -1 || h1.get("u", 3) != 7 || h1.liveCount(3) != 1) throw new AssertionError("example 1");
        // Example 2: a shorter overwrite ends the key at once, and the stale longer record changes nothing.
        HeapStore h2 = new HeapStore();
        h2.put("w", 4, 9, 2); h2.put("w", 5, 1, 3);
        if (h2.get("w", 4) != -1 || h2.liveCount(4) != 0 || h2.get("w", 5) != -1) throw new AssertionError("example 2");
        // The same two examples through the lazy design.
        LazyStore l2 = new LazyStore();
        l2.put("w", 4, 9, 2); l2.put("w", 5, 1, 3);
        if (l2.get("w", 4) != -1 || l2.liveCount(4) != 0) throw new AssertionError("lazy example 2");
        // Random streams compare the lazy design, the heap design and the brute force.
        Random rnd = new Random(3804L);
        for (int t = 0; t < 4000; t++) {
            LazyStore lazy = new LazyStore();
            HeapStore heap = new HeapStore();
            java.util.List<long[]> puts = new java.util.ArrayList<>();   // value, end
            java.util.List<String> keys = new java.util.ArrayList<>();
            long now = rnd.nextInt(3);
            for (int s = rnd.nextInt(40); s > 0; s--) {
                // The clock repeats or advances, never decreases.
                now += rnd.nextInt(3);
                String key = String.valueOf((char) ('a' + rnd.nextInt(4)));
                int op = rnd.nextInt(3);
                if (op == 0) {
                    long value = rnd.nextInt(1000);
                    long ttl = 1 + rnd.nextInt(7);
                    lazy.put(key, value, ttl, now);
                    heap.put(key, value, ttl, now);
                    puts.add(new long[]{value, now + ttl});
                    keys.add(key);
                } else if (op == 1) {
                    long want = oracleGet(puts, keys, key, now);
                    if (lazy.get(key, now) != want || heap.get(key, now) != want) throw new AssertionError("get differs");
                } else {
                    // The oracle counts the distinct keys whose latest put has not ended.
                    int want = 0;
                    for (char c = 'a'; c <= 'd'; c++) if (oracleGet(puts, keys, String.valueOf(c), now) != -1) want++;
                    if (lazy.liveCount(now) != want || heap.liveCount(now) != want) throw new AssertionError("count differs");
                    // After liveCount the heap design stores only live entries, never more than the lazy design.
                    if (heap.physicalSize() != want || heap.physicalSize() > lazy.physicalSize())
                        throw new AssertionError("heap design kept ended entries");
                }
            }
        }
        // A long stream of one-tick entries shows memory staying small in the heap design.
        HeapStore many = new HeapStore();
        LazyStore keep = new LazyStore();
        for (int i = 0; i < 2000; i++) { many.put("k" + i, i, 1, i); keep.put("k" + i, i, 1, i); }
        many.liveCount(2000); 
        if (many.physicalSize() != 0 || keep.physicalSize() != 2000) throw new AssertionError("memory comparison");
    }
}
```
