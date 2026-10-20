<!-- lesson-kind: standard -->
<!-- lesson-id: expiring-state -->
## Expiring State

<!-- stage: context -->
### Why A Logged-Out Session Still Works

A web shop stores each login session in a map from session id to a record. The record holds the user and the time at which the session ends. A background job removes ended sessions once a minute. One afternoon the job stalls behind a long garbage collection pause. A customer who logged out ten minutes earlier replays an old cookie, the map still holds the record, and the shop accepts the request. On the same day the map grows without limit, because ended sessions pile up faster than the stalled job removes them.

Both failures have one cause. The program let the physical content of the map decide what is valid. A record in the map is only a claim that the session was valid at some earlier moment. This lesson asks how a class can answer every call as if ended entries were gone, while it removes them whenever it finds it convenient.

This stream is **expiring**. Every entry carries an end time, calls arrive with a clock reading that never moves backward, and an answer depends on which entries have not ended at that reading. An append-only stream never forgets, and a correctable stream rewrites old values. An expiring stream forgets on its own schedule, and the class has to know exactly when.

<!-- stage: naive -->
### Keeping Every Event In A List

The direct design for a message rate limiter records every print in a list. A message may print again only when the previous print of the same text is at least `gap` time units old. The class below scans the list from the end to find the latest print of the text.

```java
final class NaiveLogger {
    private final long gap;
    private final java.util.ArrayList<String> texts = new java.util.ArrayList<>();
    private final java.util.ArrayList<Long> times = new java.util.ArrayList<>();

    NaiveLogger(long gap) { this.gap = gap; }

    boolean shouldPrint(long now, String text) {
        for (int i = texts.size() - 1; i >= 0; i--) {                 // newest event first
            if (texts.get(i).equals(text)) {
                if (now - times.get(i) < gap) return false;           // printed too recently
                break;                                                // older prints cannot matter
            }
        }
        texts.add(text);                                              // remember this print
        times.add(now);
        return true;
    }
}
```

With `gap` 10, the calls `(1, "a")`, `(8, "a")`, `(11, "a")` return `true`, `false` and `true`. The answers are correct and the code is short.

```predict
A service logs 10^6 different error texts over a day and then logs one text that it has never seen before. How many list entries does that last call look at, and what happens to memory when the service runs for a month?

The call compares the new text with every stored entry, so it looks at all 10^6 entries and finds none. The list never shrinks, so after a month it holds every print the service ever made, even though only prints from the last few seconds can change an answer. Both time per call and memory grow with the age of the service, not with the amount of state that matters.
```

<!-- stage: bottleneck -->
### Cost That Grows With Age

Let `n` be the number of prints made so far. A call that meets a new text scans all `n` entries, so one call costs O(n) time. A stream of `n` calls costs O(n^2) in total. The list also stores `n` entries, so memory is O(n) and never decreases.

The scan repeats work that the clock already settled. A print made 10^6 time units ago cannot block anything when `gap` is 10. The class still stores that print and still reads it on every miss. The list also mixes two different questions into one structure. The first question is which texts have a block that is still running. The second is when each block ends. A text that is looked up by comparing against the whole history never gets a direct answer to either question.

A better design must meet three needs. A call must find the state for its own text without reading other texts. A call must decide from the stored time and the clock alone whether the old print still blocks. The class must be free to drop old state without any caller noticing the difference.

<!-- stage: insight -->
### Store One Deadline Per Key

#### One Deadline Replaces The History

<!-- names: deadline, live, purge -->

A **deadline** is the first clock reading at which a stored entry no longer counts. For the rate limiter, the deadline of a text is the time of its latest print plus `gap`. A hash map from text to deadline holds the whole answer. The history of earlier prints adds nothing, because each new print replaces the deadline of its text. The map has one entry per distinct text and a call costs O(1) expected time.

An entry is **live** at clock reading `now` when its deadline is greater than `now`. The comparison is strict, so an entry whose deadline equals `now` is already not live. That choice is a contract, and the class must apply it in every method in the same way. A print at time 1 with `gap` 10 has deadline 11, and a call at time 11 may print again.

#### Validate On Every Read

Every method that reads an entry compares its deadline with `now` first. A method that finds a deadline at or below `now` treats the entry as absent, whatever the map physically contains. This is the rule behind the invariant of the lesson. A query never exposes expired state, even when cleanup runs late or never.

Validation alone fixes the wrong answers but not the memory. Entries for texts that never return stay in the map. A **purge** is the physical removal of entries that are not live. The class may purge in any of three ways. It may do nothing, as validation already keeps answers correct. It may purge on a cadence, such as every `k` calls. It may purge exactly when time passes a deadline, with a min-heap of deadlines. All three produce identical answers, and they differ only in how much memory they hold and when the work happens.

#### Counting Live Entries Without A Scan

The second class in this lesson is an authentication manager. It hands out tokens that expire after a fixed time to live, called `ttl`. The method `generate` creates a token, `renew` extends a live token, and `count` reports how many tokens are still live.

A method that counts live entries needs more than validation, because a scan of all entries costs O(size). When every entry gets the same time to live and the clock never moves backward, the deadlines appear in the order of the latest touch. A map that keeps insertion order then holds the earliest deadline at its front. A purge removes entries from the front until it finds one that is live, and the size after the purge is the exact count. When time to live differs per entry, the order breaks, and the min-heap takes over.

<!-- stage: variables -->
### Fields Of Both Maps

The trace follows a rate limiter with `gap` 10 and then an authentication manager with a fixed time to live.

- **gap** is the number of time units after a print during which the same text stays blocked.
- **deadline** is the stored value for one key, equal to the latest accepted time plus `gap`.
- **now** is the clock reading passed to the call, and it never decreases from one call to the next.
- **ttl** is the fixed time to live of a token in the authentication manager.
- **expiry** is the stored deadline of one token, equal to its latest generate or renew time plus `ttl`.

The map is rewritten only when a call is accepted. A rejected call leaves every deadline unchanged. For the authentication manager, the front of the ordered map always holds the smallest expiry.

<!-- stage: trace -->
### Tracing Two Expiring Maps

#### The Rate Limiter With Gap Ten

The first trace replays six prints with `gap` 10, and the pointer `i` marks the call in progress. Text `a` arrives at time 1 with no stored deadline, so it prints and the map records 11. Text `b` at time 3 records 13. A second `a` at time 8 faces deadline 11, stays blocked and leaves the map alone. When `a` returns at time 11, its deadline equals the clock, so the entry no longer counts, and the print goes through with a new deadline of 21. Text `b` at time 11 is still blocked by 13. At time 13 the same text meets its deadline exactly and prints. Calls with equal times can differ in outcome, since each decision reads only the deadline of its own key.

```trace
{"cells":["1:a","3:b","8:a","11:a","11:b","13:b"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"now":1,"text":"a","printed":"true","deadlines":"a=11"},"note":"Text a has no deadline, so the call prints and stores 11."},{"at":{"i":1},"vars":{"now":3,"text":"b","printed":"true","deadlines":"a=11, b=13"},"note":"Text b has no deadline, so the call prints and stores 13."},{"at":{"i":2},"vars":{"now":8,"text":"a","printed":"false","deadlines":"a=11, b=13"},"note":"Text a has deadline 11 and 8 is below it, so the call is blocked and the map is unchanged."},{"at":{"i":3},"vars":{"now":11,"text":"a","printed":"true","deadlines":"a=21, b=13"},"note":"Text a has deadline 11 and 11 is not below it, so the call prints and stores 21."},{"at":{"i":4},"vars":{"now":11,"text":"b","printed":"false","deadlines":"a=21, b=13"},"note":"Text b has deadline 13 and 11 is below it, so the call is blocked and the map is unchanged."},{"at":{"i":5},"vars":{"now":13,"text":"b","printed":"true","deadlines":"a=21, b=23"},"note":"Text b has deadline 13 and 13 is not below it, so the call prints and stores 23."}]}
```

#### The Authentication Manager With Time To Live Five

The second trace feeds seven calls to a manager with `ttl` 5, and the pointer `i` marks the call in progress. Token `A` generated at 0 expires at 5, and token `B` generated at 2 expires at 7. Renewing `A` at 4 succeeds because 4 is below 5. It receives expiry 9 and moves behind `B`. The count at 5 inspects the front, finds `B` with expiry 7, removes nothing and reports 2. At 7 the front entry `B` has reached its expiry, so the purge deletes it before the renew looks for it, and the renew finds nothing to extend. The count at 7 therefore reports 1. The count at 9 deletes `A` and reports 0. The strict comparison has to run before any mutation, as the renew at 7 shows.

```trace
{"cells":["gen A@0","gen B@2","renew A@4","count @5","renew B@7","count @7","count @9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"now":0,"call":"gen A","result":"none","order":"A=5"},"note":"Token A is stored with expiry 5 at the back of the order."},{"at":{"i":1},"vars":{"now":2,"call":"gen B","result":"none","order":"A=5, B=7"},"note":"Token B is stored with expiry 7 at the back of the order."},{"at":{"i":2},"vars":{"now":4,"call":"renew A","result":"renewed","order":"B=7, A=9"},"note":"Token A is live, so its expiry becomes 9 and it moves to the back."},{"at":{"i":3},"vars":{"now":5,"call":"count","result":"2","order":"B=7, A=9"},"note":"After the purge from the front, 2 token(s) remain, so the count is 2."},{"at":{"i":4},"vars":{"now":7,"call":"renew B","result":"ignored","order":"A=9"},"note":"Token B ended at 7 or before, so the purge removed it and the renew does nothing."},{"at":{"i":5},"vars":{"now":7,"call":"count","result":"1","order":"A=9"},"note":"After the purge from the front, 1 token(s) remain, so the count is 1."},{"at":{"i":6},"vars":{"now":9,"call":"count","result":"0","order":"empty"},"note":"After the purge from the front, 0 token(s) remain, so the count is 0."}]}
```

<!-- stage: code -->
### Two Maps With Validated Reads

#### The Rate Limiter

The class stores one deadline per text. The decision reads the stored deadline and the clock only. The optional method `purge` removes entries that are not live and never changes any answer.

```java
final class RateLogger {
    private final long gap;
    private final java.util.HashMap<String, Long> deadline = new java.util.HashMap<>();

    RateLogger(long gap) { this.gap = gap; }

    boolean shouldPrint(long now, String text) {
        Long d = deadline.get(text);                       // one hash lookup, no scan of other texts
        if (d != null && now < d) return false;            // still live, so the print is blocked
        deadline.put(text, now + gap);                     // accepted, so the deadline moves forward
        return true;
    }

    void purge(long now) {
        deadline.values().removeIf(d -> d <= now);         // physical cleanup only, answers do not change
    }
}
```

#### The Authentication Manager

This class uses one fixed `ttl`. The ordered map moves a renewed token to the back, so the front always holds the smallest expiry. Every public method purges the front first.

```java
final class AuthManager {
    private final long ttl;
    private final java.util.LinkedHashMap<String, Long> expiry = new java.util.LinkedHashMap<>();

    AuthManager(long ttl) { this.ttl = ttl; }

    private void purge(long now) {
        var it = expiry.entrySet().iterator();
        while (it.hasNext() && it.next().getValue() <= now) it.remove();   // stops at the first live entry
    }

    void generate(String id, long now) {
        purge(now);
        expiry.remove(id);                                 // a re-generated id moves to the back
        expiry.put(id, now + ttl);
    }

    void renew(String id, long now) {
        purge(now);                                        // an entry that ended at now is gone before the check
        if (expiry.remove(id) != null) expiry.put(id, now + ttl);   // only a live token is renewed
    }

    int countLive(long now) { purge(now); return expiry.size(); }
}
```

#### A Heap Of Deadlines

When each key has its own time to live, the front of an ordered map no longer holds the smallest expiry. The Expiring Key Store exercise adds a min-heap of end-time records. The map stays the truth, and a heap record counts only when it matches the map.

```java
final class StoreSketch {
    private final java.util.HashMap<String, long[]> map = new java.util.HashMap<>();   // key to {value, end}
    private final java.util.PriorityQueue<Object[]> heap =
        new java.util.PriorityQueue<>((a, b) -> Long.compare((long) a[0], (long) b[0]));   // {end, key}

    void put(String key, long value, long ttl, long now) {
        map.put(key, new long[]{value, now + ttl});        // the newest entry replaces the old one
        heap.add(new Object[]{now + ttl, key});            // the old heap record stays and goes stale
    }

    int liveCount(long now) {
        while (!heap.isEmpty() && (long) heap.peek()[0] <= now) {   // records at or below now have ended
            Object[] r = heap.poll();
            long[] e = map.get((String) r[1]);
            if (e != null && e[1] == (long) r[0]) map.remove((String) r[1]);   // delete only a matching record
        }
        return map.size();
    }
}
```

A stale record names an end time that differs from the map, so the check skips it. Each record leaves the heap once, which gives O(log n) amortized time per call.

#### Cost

- **RateLogger.shouldPrint** costs O(1) expected time. Memory is O(d) for `d` distinct texts until a purge runs.
- **AuthManager** takes O(1) amortized time per call, because each entry is removed once, and O(t) space for `t` live tokens.
- **StoreSketch** costs O(log n) amortized time per `put`, since each heap record is added and removed once.

<!-- stage: applicability -->
### When To Store A Deadline

#### Recognizing The Pattern

Use this method when entries become invalid after a time and the class answers with the clock as part of the question. Words such as "within the last", "expires after" or "renew" in a problem statement signal it. Before coding, write the stream kind, the exact meaning of equality at the deadline, and whether the clock can repeat a value. The invariant to keep is that each read compares the stored deadline with `now` before it uses the entry. Physical removal is a separate optimization and never decides an answer.

#### A False Friend

A fixed-size sliding window over the last `k` values is a false friend. It looks like expiry, but entries leave by count and not by a deadline, so a deque of values is enough and no per-key deadline exists. A second false friend is a cache with least-recently-used eviction. It removes entries because of capacity, and a removed entry was still valid.

#### When The Method Does Not Apply

If the clock can move backward, a purge from the front loses entries that become valid again, and the class needs a different design. If entries must be reported in the order they expired, a plain map does not keep that order, and a heap or an ordered map keyed by deadline is the starting point. If many threads share the map, the check and the update need one lock, which this lesson does not cover.

<!-- stage: exercises -->
### Exercises

#### [Build] Logger Rate Limiter (LeetCode 359)
<!-- id: st38-logger-rate-limiter -->

**Prerequisites.** The deadline and live definitions from this lesson. The stream is expiring: each printed text blocks itself for a fixed gap.

**Problem.** Design the class `Logger` with a constructor that receives a positive integer `gap`. The method `shouldPrint(timestamp, message)` returns `true` and records the print when no print of `message` exists with a timestamp greater than `timestamp - gap`. Otherwise it returns `false` and records nothing.

**Constraints.** The limits are:
- **Gap** is from 1 to 10^9.
- **Timestamps** are `long` values from 0 to 10^12 and never decrease between calls. Equal timestamps are allowed.
- **Messages** are non-empty strings of at most 30 lowercase letters.
- **Calls** number at most 10^5 per object.

**Example 1.** Input calls `["Logger","shouldPrint","shouldPrint","shouldPrint","shouldPrint"]` with arguments `[[4],[2,"x"],[5,"x"],[6,"x"],[6,"y"]]`, output `[null,true,false,true,true]`.

**Example 2.** Input calls `["Logger","shouldPrint","shouldPrint","shouldPrint"]` with arguments `[[3],[0,"q"],[0,"q"],[3,"q"]]`, output `[null,true,false,true]`.

**Hint.** Which single number per message is enough to decide the next call, and when does a rejected call write it?

**Changed decision.** Basic case: the class stores the next allowed time per message and never stores a history.

#### [Vary] Authentication Manager (LeetCode 1797)
<!-- id: st38-authentication-manager -->

**Prerequisites.** The Logger Rate Limiter exercise above. This exercise adds renewal and a count of live entries, so a read must also drop ended entries from the count.

**Problem.** Design the class `AuthenticationManager` with a constructor that receives `timeToLive`. The method `generate(tokenId, currentTime)` creates a token that ends at `currentTime + timeToLive`. The method `renew(tokenId, currentTime)` sets the end of a token to `currentTime + timeToLive` only when the token exists and has not ended at `currentTime`. Otherwise it does nothing. The method `countUnexpiredTokens(currentTime)` returns the number of tokens that have not ended at `currentTime`. A token ends at time `e` when `currentTime >= e`.

**Constraints.** The limits are:
- **Time to live** is from 1 to 10^9.
- **Current times** are `long` values from 1 to 10^12 and never decrease between calls. Equal values are allowed.
- **Token ids** are non-empty strings of at most 5 lowercase letters or digits, and `generate` may reuse an id that has ended.
- **Calls** number at most 2000 per object.

**Example 1.** Input calls `["AuthenticationManager","generate","generate","renew","countUnexpiredTokens","countUnexpiredTokens"]` with arguments `[[6],["p",1],["q",3],["p",6],[8],[12]]`, output `[null,null,null,null,2,0]`.

**Example 2.** Input calls `["AuthenticationManager","generate","renew","countUnexpiredTokens","generate","countUnexpiredTokens"]` with arguments `[[2],["m",5],["m",7],[7],["m",7],[8]]`, output `[null,null,null,0,null,1]`.

**Hint.** If every token has the same time to live and the clock never decreases, in what order do the expiry times appear when tokens are sorted by their latest touch?

**Changed decision.** The class now counts, so validation on each read is not enough. The ordered map lets a purge from the front keep the size exact.

#### [Boundary] Renew At Expiry (Author exercise)
<!-- id: st38-renew-at-expiry -->

**Prerequisites.** The Authentication Manager exercise above. This exercise drops the count and tests only the meaning of equality at the deadline, for acquiring as well as renewing.

**Problem.** Design the class `LeaseBook` with a constructor that receives `ttl`. A lease for a key starts at the time of a successful `acquire` and ends at that time plus `ttl`. The method `acquire(key, now)` returns `true` and starts a lease when the key has no lease or its lease has ended at `now`. Otherwise it returns `false` and changes nothing. The method `renew(key, now)` returns `true` and moves the end to `now + ttl` when the lease has not ended at `now`. Otherwise it returns `false`. The method `isHeld(key, now)` returns whether the lease has not ended at `now`. A lease has ended at `now` when `now` is greater than or equal to its end.

**Constraints.** The limits are:
- **Time to live** is from 1 to 10^12.
- **Times** are `long` values from 0 to 10^12 and never decrease between calls. Equal values are allowed.
- **Keys** are non-empty strings of at most 8 lowercase letters.
- **Calls** number at most 10^5 per object.
- **Mutation** by a returned `false` is forbidden: a rejected call leaves every lease as it was.

**Example 1.** Input calls `["LeaseBook","acquire","renew","isHeld","renew","acquire"]` with arguments `[[5],["k",2],["k",6],["k",11],["k",11],["k",11]]`, output `[null,true,true,false,false,true]`.

**Example 2.** Input calls `["LeaseBook","acquire","acquire","isHeld","acquire","renew"]` with arguments `[[3],["a",0],["a",2],["a",3],["a",3],["a",5]]`, output `[null,true,false,false,true,true]`.

**Hint.** Which comparison decides every method, and does it run before or after the method writes?

**Changed decision.** One strict comparison now guards three methods. An acquire at the exact end time succeeds, while a renew at the exact end time fails.

#### [Recognize] Expiring Key Store (Author exercise)
<!-- id: st38-expiring-key-store -->

**Prerequisites.** The Renew At Expiry exercise above. Each entry now has its own time to live, so the expiry order no longer matches the order of the latest touch.

**Problem.** Design the class `ExpiringStore` with methods `put(key, value, ttl, now)`, `get(key, now)` and `liveCount(now)`. The method `put` stores the value under the key with end time `now + ttl` and replaces any earlier entry of that key. The method `get` returns the stored value when the entry has not ended at `now`, and `-1` otherwise. The method `liveCount` returns the number of keys whose entries have not ended at `now`. An entry has ended at `now` when `now` is greater than or equal to its end.

**Constraints.** The limits are:
- **Time to live** per call is from 1 to 10^9.
- **Times** are `long` values from 0 to 10^12 and never decrease between calls. Equal values are allowed.
- **Values** are integers from 0 to 10^9, so `-1` never collides with a stored value.
- **Calls** number at most 10^5 per object.
- **Memory** after `liveCount` returns must be proportional to the live entries plus pending cleanup records.

**Example 1.** Input calls `["ExpiringStore","put","put","get","get","liveCount"]` with arguments `[[],["u",7,10,0],["v",8,2,1],["v",3],["u",3],[3]]`, output `[null,null,null,-1,7,1]`.

**Example 2.** Input calls `["ExpiringStore","put","put","get","liveCount","get"]` with arguments `[[],["w",4,9,2],["w",5,1,3],["w",4],[4],["w",5]]`, output `[null,null,null,-1,0,-1]`.

**Hint.** When a shorter time to live overwrites a longer one, which stored record must a cleanup step ignore, and how does it recognize that record?

**Changed decision.** Per-entry time to live breaks the front-of-the-map order. Validated reads stay correct, and a min-heap of expiry records with a check against the map keeps the count and the memory exact.
