<!-- solutions-for: 01-multi-index-records -->
### Solutions For Multi-Index Records

#### Solution: [Build] Number Container System (LeetCode 2349)
<!-- id: ci40-number-container -->

**Approach.** The class keeps a hash map from index to number as the source of truth. A second hash map from number to a tree set of indexes is the secondary index.

A change call reads the old number with `put`, which returns the previous value. When the old number equals the new one, both structures already agree and the call stops. Otherwise it removes the index from the old number's set, deletes that set if it is empty, and inserts the index into the new number's set. A find call returns the first element of the set for the number.

The invariant is that index `i` appears in the set of number `v` exactly when the map holds `v` for `i`. Removal happens before insertion, so the index never sits in two sets at once.

**Complexity.**

- **Time** is O(log n) for both calls. One hash lookup and at most three tree operations touch a set of at most n indexes.
- **Space** is O(n), because each index appears once in the map and once in one set.

```java run
import java.util.*;

public final class NumberContainerSolution {
    static final class NumberContainers {
        private final Map<Integer, Integer> numberAt = new HashMap<>();             // index -> number, source of truth
        private final Map<Integer, TreeSet<Integer>> indexesOf = new HashMap<>();   // number -> sorted indexes

        /**
         * Stores number at index and repairs the secondary index.
         * Time: O(log n), because it does a constant number of hash and tree operations.
         * Space: O(1) extra, because only one entry moves.
         * Invariant: each index sits in exactly the set of its current number.
         */
        void change(int index, int number) {
            // put returns the old value, which names the set that must lose the index.
            Integer old = numberAt.put(index, number);
            // Equal values need no repair, and skipping avoids removing then re-adding.
            if (old != null && old == number) return;
            if (old != null) {
                // Remove the exact old entry before the new one enters.
                TreeSet<Integer> set = indexesOf.get(old);
                set.remove(index);
                // Drop empty sets so find sees a missing key, not an empty set.
                if (set.isEmpty()) indexesOf.remove(old);
            }
            // Create the set on demand and insert the index in sorted position.
            indexesOf.computeIfAbsent(number, k -> new TreeSet<>()).add(index);
        }

        /**
         * Returns the smallest index holding number, or -1.
         * Time: O(log n) for the hash lookup and tree first element.
         * Space: O(1).
         * Invariant: the first element of a set is its minimum.
         */
        int find(int number) {
            // A missing key means no index holds the number.
            TreeSet<Integer> set = indexesOf.get(number);
            return set == null ? -1 : set.first();
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        NumberContainers a = new NumberContainers();
        if (a.find(10) != -1) throw new AssertionError("e1 empty");
        a.change(2, 10); a.change(1, 10);
        if (a.find(10) != 1) throw new AssertionError("e1 smallest");
        NumberContainers b = new NumberContainers();
        b.change(1, 10); b.change(1, 20);
        if (b.find(10) != -1 || b.find(20) != 1) throw new AssertionError("e2");
        // Random calls checked against a scan of an array that holds the current numbers.
        Random rnd = new Random(2349);
        for (int round = 0; round < 300; round++) {
            NumberContainers s = new NumberContainers();
            int[] ref = new int[12];                       // 0 means empty
            for (int op = 0; op < 150; op++) {
                if (rnd.nextBoolean()) {
                    int i = 1 + rnd.nextInt(11), v = 1 + rnd.nextInt(4);
                    ref[i] = v; s.change(i, v);
                } else {
                    int v = 1 + rnd.nextInt(4), want = -1;
                    for (int i = 1; i < 12 && want == -1; i++) if (ref[i] == v) want = i;
                    if (s.find(v) != want) throw new AssertionError("random find");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Food Rating System (LeetCode 2353)
<!-- id: ci40-food-rating -->

**Approach.** A record holds a food's cuisine and current rating. A map from food name to record is the source of truth. A map from cuisine to a tree set of entries is the secondary index, where an entry is an immutable pair of name and rating.

The set orders entries by higher rating first and then by smaller name, using `Integer.compare` on the ratings. A rating change removes the entry built from the stored rating, writes the new rating into the record, and inserts the new entry. The highest-rated food is the first entry of its cuisine's set.

The invariant is that every food has exactly one entry in its cuisine set, and the entry holds the same rating as the record. The removal runs first, because the set finds an entry through its rating.

**Complexity.**

- **Time** is O(log n) for a change call and for a query. Each runs hash lookups and tree operations on at most n entries. The constructor adds O(n log n).
- **Space** is O(n), because each food owns one record and one entry.

```java run
import java.util.*;

public final class FoodRatingSolution {
    static final class FoodRatings {
        private record Entry(String name, int rating) {}                    // immutable, so tree order cannot drift
        private final Map<String, int[]> ratingOf = new HashMap<>();        // food -> {rating}
        private final Map<String, String> cuisineOf = new HashMap<>();      // food -> cuisine
        private final Map<String, TreeSet<Entry>> byCuisine = new HashMap<>();
        private static final Comparator<Entry> ORDER = (x, y) -> {
            int c = Integer.compare(y.rating(), x.rating());                // higher rating first
            return c != 0 ? c : x.name().compareTo(y.name());               // then smaller name
        };

        /**
         * Builds both maps from the starting arrays.
         * Time: O(n log n), because each food enters a tree set.
         * Space: O(n).
         * Invariant: each food appears once in its cuisine set with its record's rating.
         */
        FoodRatings(String[] foods, String[] cuisines, int[] ratings) {
            for (int i = 0; i < foods.length; i++) {
                // Record first, then the matching entry in the cuisine index.
                ratingOf.put(foods[i], new int[] {ratings[i]});
                cuisineOf.put(foods[i], cuisines[i]);
                byCuisine.computeIfAbsent(cuisines[i], k -> new TreeSet<>(ORDER)).add(new Entry(foods[i], ratings[i]));
            }
        }

        /**
         * Sets the rating of a food.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: the old entry leaves before the rating changes.
         */
        void changeRating(String food, int newRating) {
            int[] cell = ratingOf.get(food);
            TreeSet<Entry> set = byCuisine.get(cuisineOf.get(food));
            // Remove using the stored rating, because the set locates entries by rating.
            set.remove(new Entry(food, cell[0]));
            cell[0] = newRating;
            // Insert the entry that carries the new rating.
            set.add(new Entry(food, newRating));
        }

        /**
         * Returns the best food of a cuisine.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: the first entry has the highest rating, then the smallest name.
         */
        String highestRated(String cuisine) {
            return byCuisine.get(cuisine).first().name();
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        FoodRatings f = new FoodRatings(new String[] {"a", "b", "c"}, new String[] {"x", "x", "x"}, new int[] {5, 9, 9});
        if (!f.highestRated("x").equals("b")) throw new AssertionError("e1");
        f.changeRating("b", 1);
        if (!f.highestRated("x").equals("c")) throw new AssertionError("e2");
        // Random updates checked against a scan of all foods in the cuisine.
        Random rnd = new Random(2353);
        for (int round = 0; round < 300; round++) {
            int n = 2 + rnd.nextInt(8);
            String[] foods = new String[n], cuis = new String[n];
            int[] rat = new int[n];
            for (int i = 0; i < n; i++) { foods[i] = "f" + (char) ('a' + i); cuis[i] = "c" + rnd.nextInt(2); rat[i] = 1 + rnd.nextInt(4); }
            FoodRatings s = new FoodRatings(foods, cuis, rat.clone());
            for (int op = 0; op < 80; op++) {
                if (rnd.nextBoolean()) {
                    int i = rnd.nextInt(n), v = 1 + rnd.nextInt(4);
                    rat[i] = v; s.changeRating(foods[i], v);
                } else {
                    String c = cuis[rnd.nextInt(n)];
                    int best = -1;
                    for (int i = 0; i < n; i++)
                        if (cuis[i].equals(c) && (best == -1 || rat[i] > rat[best] || (rat[i] == rat[best] && foods[i].compareTo(foods[best]) < 0))) best = i;
                    if (!s.highestRated(c).equals(foods[best])) throw new AssertionError("random best");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Update To Same Value (Author exercise)
<!-- id: ci40-same-value -->

**Approach.** A map from player to team is the source of truth. A map from team to a tree set of players is the secondary index, and a counter per team is a third derived view.

The call reads the old team first. When the old team equals the new team, the call returns `false` before it touches any counter or set. Otherwise it removes the player from the old team's set, lowers the old counter, inserts the player into the new team's set, raises the new counter and returns `true`.

The invariant is that each counter equals the size of its set. An update that skips the early return raises the counter without adding a new set element, because adding an existing element to a set changes nothing. The counter then exceeds the true size.

**Complexity.**

- **Time** per call is O(log n), which comes from two hash lookups and at most two tree operations.
- **Space** is O(n), because each player appears once in the map and once in one set.

```java run
import java.util.*;

public final class SameValueSolution {
    static final class Roster {
        private final Map<Integer, Integer> teamOf = new HashMap<>();            // player -> team, source of truth
        private final Map<Integer, TreeSet<Integer>> members = new HashMap<>();  // team -> sorted players
        private final Map<Integer, Integer> counter = new HashMap<>();           // team -> number of players

        /**
         * Assigns a player and reports whether the stored team changed.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: counter(team) equals members(team).size() after every call.
         */
        boolean setTeam(int player, int team) {
            Integer old = teamOf.get(player);
            // Same team: no index entry moves, so no counter may move either.
            if (old != null && old == team) return false;
            if (old != null) {
                // Leave the old team in both the set and the counter.
                members.get(old).remove(player);
                counter.merge(old, -1, Integer::sum);
            }
            // Enter the new team in the source of truth, the set and the counter.
            teamOf.put(player, team);
            members.computeIfAbsent(team, k -> new TreeSet<>()).add(player);
            counter.merge(team, 1, Integer::sum);
            return true;
        }

        /** Returns the counter; O(1) time and space, equal to the set size by the invariant. */
        int size(int team) { return counter.getOrDefault(team, 0); }

        /** Returns the players of a team in order; O(k) time for k players, O(k) space for the copy. */
        List<Integer> members(int team) { return new ArrayList<>(members.getOrDefault(team, new TreeSet<>())); }
    }

    public static void main(String[] args) {
        // Example 1: a repeated assignment returns false and keeps the count at 1.
        Roster r = new Roster();
        if (!r.setTeam(7, 1) || r.setTeam(7, 1) || r.size(1) != 1) throw new AssertionError("e1");
        // Example 2: a real move changes both counters.
        Roster q = new Roster();
        if (!q.setTeam(7, 1) || !q.setTeam(7, 2) || q.size(1) != 0 || q.size(2) != 1) throw new AssertionError("e2");
        // Random calls checked against a plain array of teams.
        Random rnd = new Random(40);
        for (int round = 0; round < 300; round++) {
            Roster s = new Roster();
            int[] team = new int[8];                                // 0 means unassigned
            for (int op = 0; op < 120; op++) {
                int p = 1 + rnd.nextInt(7), t = 1 + rnd.nextInt(3);
                boolean want = team[p] != t;
                team[p] = t;
                if (s.setTeam(p, t) != want) throw new AssertionError("return value");
                for (int x = 1; x <= 3; x++) {
                    List<Integer> ref = new ArrayList<>();
                    for (int i = 1; i < 8; i++) if (team[i] == x) ref.add(i);
                    if (!s.members(x).equals(ref) || s.size(x) != ref.size()) throw new AssertionError("counter or members");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Movie Rental System (LeetCode 1912)
<!-- id: ci40-movie-rental -->

**Approach.** A record is an immutable entry of price, shop and movie. One tree set holds all rented entries. A map from movie to a tree set holds the unrented entries of that movie. A map from the pair of shop and movie to the entry is the source of truth for the price.

All sets use one order: price first, then shop, then movie, compared with `Integer.compare`. A rent call removes the entry from its movie's unrented set and inserts it into the rented set. A drop call moves the entry back. A search reads the first five entries of one movie's set. A report reads the first five entries of the rented set.

The invariant is that every entry sits in exactly one of its movie's unrented set and the rented set. Each call removes before it inserts, so no entry is ever in both.

**Complexity.**

- **Time** is O(log n) for rent and drop, and O(log n) for search and report. Each of those reads at most five entries from the start of a tree set.
- **Space** is O(n), because each copy owns one entry and one map slot.

```java run
import java.util.*;

public final class MovieRentalSolution {
    static final class MovieRental {
        private record Copy(int price, int shop, int movie) {}
        private static final Comparator<Copy> ORDER = (a, b) -> {
            int c = Integer.compare(a.price(), b.price());
            if (c != 0) return c;
            c = Integer.compare(a.shop(), b.shop());
            return c != 0 ? c : Integer.compare(a.movie(), b.movie());
        };
        private final Map<Long, Copy> copyAt = new HashMap<>();               // pair key -> copy, source of truth
        private final Map<Integer, TreeSet<Copy>> unrented = new HashMap<>();  // movie -> unrented copies
        private final TreeSet<Copy> rented = new TreeSet<>(ORDER);

        private static long key(int shop, int movie) { return ((long) shop << 32) | movie; }

        /**
         * Builds the views with every copy unrented.
         * Time: O(n log n).
         * Space: O(n).
         * Invariant: each copy sits in its movie's unrented set.
         */
        MovieRental(int[][] entries) {
            for (int[] e : entries) {
                Copy c = new Copy(e[2], e[0], e[1]);
                copyAt.put(key(e[0], e[1]), c);
                unrented.computeIfAbsent(e[1], k -> new TreeSet<>(ORDER)).add(c);
            }
        }

        /** Returns up to 5 cheapest shops with an unrented copy; O(log n + 5) time, O(1) extra space. */
        List<Integer> search(int movie) {
            List<Integer> out = new ArrayList<>();
            // Walk the sorted set and stop after five entries.
            for (Copy c : unrented.getOrDefault(movie, new TreeSet<>(ORDER))) {
                if (out.size() == 5) break;
                out.add(c.shop());
            }
            return out;
        }

        /** Moves a copy from its unrented set to the rented set; O(log n) time, O(1) space; invariant: one view at a time. */
        void rent(int shop, int movie) {
            Copy c = copyAt.get(key(shop, movie));
            unrented.get(movie).remove(c);   // leave the old view first
            rented.add(c);                   // then enter the new view
        }

        /** Moves a copy back to its unrented set; O(log n) time, O(1) space; invariant: one view at a time. */
        void drop(int shop, int movie) {
            Copy c = copyAt.get(key(shop, movie));
            rented.remove(c);
            unrented.get(movie).add(c);
        }

        /** Returns up to 5 cheapest rented copies as {shop, movie}; O(log n + 5) time, O(1) extra space. */
        List<int[]> report() {
            List<int[]> out = new ArrayList<>();
            for (Copy c : rented) {
                if (out.size() == 5) break;
                out.add(new int[] {c.shop(), c.movie()});
            }
            return out;
        }
    }

    public static void main(String[] args) {
        // Examples from the problem text.
        MovieRental m = new MovieRental(new int[][] {{0, 1, 5}, {0, 2, 6}, {1, 1, 4}});
        if (!m.search(1).equals(List.of(1, 0))) throw new AssertionError("e1");
        m.rent(1, 1);
        List<int[]> rep = m.report();
        if (!m.search(1).equals(List.of(0)) || rep.size() != 1 || rep.get(0)[0] != 1 || rep.get(0)[1] != 1) throw new AssertionError("e2");
        // Random calls checked against a scan over a boolean array of rented flags.
        Random rnd = new Random(1912);
        for (int round = 0; round < 200; round++) {
            int shops = 4, movies = 3;
            List<int[]> list = new ArrayList<>();
            for (int s = 0; s < shops; s++) for (int v = 0; v < movies; v++) if (rnd.nextInt(3) > 0) list.add(new int[] {s, v, 1 + rnd.nextInt(5)});
            int[][] entries = list.toArray(new int[0][]);
            MovieRental sut = new MovieRental(entries);
            boolean[] out = new boolean[entries.length];
            for (int op = 0; op < 100; op++) {
                int k = rnd.nextInt(entries.length);
                int t = rnd.nextInt(3);
                if (t == 0 && !out[k]) { out[k] = true; sut.rent(entries[k][0], entries[k][1]); }
                else if (t == 1 && out[k]) { out[k] = false; sut.drop(entries[k][0], entries[k][1]); }
                else if (t == 2) {
                    int mv = rnd.nextInt(movies);
                    List<int[]> cand = new ArrayList<>();
                    for (int i = 0; i < entries.length; i++) if (entries[i][1] == mv && !out[i]) cand.add(entries[i]);
                    cand.sort((x, y) -> x[2] != y[2] ? Integer.compare(x[2], y[2]) : Integer.compare(x[0], y[0]));
                    List<Integer> want = new ArrayList<>();
                    for (int i = 0; i < Math.min(5, cand.size()); i++) want.add(cand.get(i)[0]);
                    if (!sut.search(mv).equals(want)) throw new AssertionError("search");
                    List<int[]> rented = new ArrayList<>();
                    for (int i = 0; i < entries.length; i++) if (out[i]) rented.add(entries[i]);
                    rented.sort((x, y) -> x[2] != y[2] ? Integer.compare(x[2], y[2]) : x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
                    List<int[]> got = sut.report();
                    if (got.size() != Math.min(5, rented.size())) throw new AssertionError("report size");
                    for (int i = 0; i < got.size(); i++)
                        if (got.get(i)[0] != rented.get(i)[0] || got.get(i)[1] != rented.get(i)[1]) throw new AssertionError("report order");
                }
            }
        }
    }
}
```
