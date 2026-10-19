<!-- solutions-for: 91-map-ordered-index -->
### Solutions For Lookup By ID And Order

#### Solution: [Build] Number Container With Floor (LeetCode 2349)
<!-- id: ci40-nc-floor -->

**Approach.** A hash map from index to number is the record that decides. A hash map from number to a tree set of indexes is the ordered view. One helper, `store`, takes an index and a new number, or none for a clear. It removes the index from the set of the old number, deletes an empty set and inserts the index into the set of the new number when there is one. Both `change` and `clear` call that helper.

A find call takes the set for the number and asks for the `ceiling` of the floor, which is the smallest element that is at least the floor.

The invariant is that an index sits in the set of a number exactly when the record holds that number for the index. Only `store` writes the two maps.

**Complexity.**

- **Time** is O(log n) per call. Each call runs hash lookups and at most two tree operations.
- **Space** is O(n), since a filled slot appears once in each map.

```java run
import java.util.*;

public final class NumberContainerFloorSolution {
    static final class FloorContainers {
        private final Map<Integer, Integer> numberAt = new HashMap<>();
        private final Map<Integer, TreeSet<Integer>> indexesOf = new HashMap<>();

        /**
         * The only method that writes the two maps.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the index leaves the old set before it enters the new one.
         */
        private void store(int index, Integer number) {
            Integer old = number == null ? numberAt.remove(index) : numberAt.put(index, number);
            // An unchanged value needs no repair.
            if (old != null && old.equals(number)) return;
            if (old != null) {
                TreeSet<Integer> set = indexesOf.get(old);
                set.remove(index);
                if (set.isEmpty()) indexesOf.remove(old);
            }
            if (number != null) indexesOf.computeIfAbsent(number, k -> new TreeSet<>()).add(index);
        }

        void change(int index, int number) { store(index, number); }

        void clear(int index) { store(index, null); }

        /** Returns the smallest index at least floor that holds number, or -1; O(log n) time, O(1) space. */
        int find(int number, int floor) {
            TreeSet<Integer> set = indexesOf.get(number);
            if (set == null) return -1;
            Integer hit = set.ceiling(floor);
            return hit == null ? -1 : hit;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        FloorContainers a = new FloorContainers();
        a.change(1, 10); a.change(5, 10); a.change(9, 10);
        if (a.find(10, 2) != 5) throw new AssertionError("e1 first");
        a.clear(5);
        if (a.find(10, 2) != 9) throw new AssertionError("e1 second");
        FloorContainers b = new FloorContainers();
        if (b.find(10, 10) != -1 || b.find(7, 0) != -1) throw new AssertionError("e2");
        // Random calls checked against a scan of an array.
        Random rnd = new Random(9101);
        for (int round = 0; round < 300; round++) {
            FloorContainers s = new FloorContainers();
            int[] ref = new int[10];
            for (int op = 0; op < 100; op++) {
                int t = rnd.nextInt(3), i = rnd.nextInt(10);
                if (t == 0) { int v = 1 + rnd.nextInt(3); ref[i] = v; s.change(i, v); }
                else if (t == 1) { ref[i] = 0; s.clear(i); }
                else {
                    int v = 1 + rnd.nextInt(3), f = rnd.nextInt(11), want = -1;
                    for (int x = f; x < 10 && want == -1; x++) if (ref[x] == v) want = x;
                    if (s.find(v, f) != want) throw new AssertionError("find");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Food Ratings With Retirement (LeetCode 2353)
<!-- id: ci40-food-retire -->

**Approach.** A map from food name to an immutable record of cuisine and rating is the record that decides. A map from cuisine to a tree set of immutable entries is the ordered view. The entries order by higher rating and then smaller name. A rating change and a retire call both go through one helper that removes the entry built from the stored record. A rating change then stores a new record and inserts a new entry, and a retire call stops after the removal.

A top-two query iterates the first two entries of the cuisine's set.

The invariant is that each food on the menu has exactly one entry in its cuisine's set, and the entry carries the stored rating. A retired food has no record and no entry.

**Complexity.**

- **Time** is O(log n) per update and O(1 + log n) per query, because the iterator starts at the first entry and reads two entries.
- **Space** is O(n), since every food on the menu keeps one record and one set entry.

```java run
import java.util.*;

public final class FoodRetireSolution {
    static final class FoodMenu {
        private record Item(String cuisine, int rating) {}
        private record Entry(String name, int rating) {}
        private static final Comparator<Entry> ORDER = (a, b) -> {
            int c = Integer.compare(b.rating(), a.rating());
            return c != 0 ? c : a.name().compareTo(b.name());
        };
        private final Map<String, Item> itemOf = new HashMap<>();
        private final Map<String, TreeSet<Entry>> byCuisine = new HashMap<>();

        FoodMenu(String[] foods, String[] cuisines, int[] ratings) {
            for (int i = 0; i < foods.length; i++) put(foods[i], new Item(cuisines[i], ratings[i]));
        }

        // Inserts a record and its entry; O(log n) time, O(1) space.
        private void put(String food, Item item) {
            itemOf.put(food, item);
            byCuisine.computeIfAbsent(item.cuisine(), k -> new TreeSet<>(ORDER)).add(new Entry(food, item.rating()));
        }

        // Removes a record and its exact entry; O(log n) time, O(1) space; invariant: no entry outlives its record.
        private Item take(String food) {
            Item item = itemOf.remove(food);
            byCuisine.get(item.cuisine()).remove(new Entry(food, item.rating()));
            return item;
        }

        /** Sets a rating by removing the old pair and inserting the new one; O(log n) time, O(1) space. */
        void changeRating(String food, int rating) {
            Item old = take(food);
            put(food, new Item(old.cuisine(), rating));
        }

        /** Deletes a food from the menu; O(log n) time, O(1) space; invariant: take is the only removal path. */
        void retire(String food) { take(food); }

        /** Returns up to two best names of a cuisine; O(log n) time, O(1) space. */
        List<String> topTwo(String cuisine) {
            List<String> out = new ArrayList<>();
            for (Entry e : byCuisine.getOrDefault(cuisine, new TreeSet<>(ORDER))) {
                if (out.size() == 2) break;
                out.add(e.name());
            }
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        String[] foods = {"a", "b", "c", "d"}, cuis = {"x", "x", "x", "y"};
        int[] rat = {5, 9, 9, 4};
        FoodMenu m = new FoodMenu(foods, cuis, rat);
        if (!m.topTwo("x").equals(List.of("b", "c"))) throw new AssertionError("e1 first");
        m.retire("b");
        if (!m.topTwo("x").equals(List.of("c", "a"))) throw new AssertionError("e1 second");
        m.changeRating("a", 9);
        if (!m.topTwo("x").equals(List.of("a", "c"))) throw new AssertionError("e2");
        // Random calls checked against a sort of the live foods.
        Random rnd = new Random(9102);
        for (int round = 0; round < 300; round++) {
            int n = 2 + rnd.nextInt(7);
            String[] f = new String[n], c = new String[n];
            int[] r = new int[n];
            boolean[] live = new boolean[n];
            for (int i = 0; i < n; i++) { f[i] = "f" + i; c[i] = "c" + rnd.nextInt(2); r[i] = 1 + rnd.nextInt(3); live[i] = true; }
            FoodMenu s = new FoodMenu(f, c, r.clone());
            for (int op = 0; op < 60; op++) {
                int i = rnd.nextInt(n), t = rnd.nextInt(3);
                if (t == 0 && live[i]) { r[i] = 1 + rnd.nextInt(3); s.changeRating(f[i], r[i]); }
                else if (t == 1 && live[i]) { live[i] = false; s.retire(f[i]); }
                else if (t == 2) {
                    String cu = "c" + rnd.nextInt(2);
                    List<Integer> ids = new ArrayList<>();
                    for (int k = 0; k < n; k++) if (live[k] && c[k].equals(cu)) ids.add(k);
                    ids.sort((x, y) -> r[x] != r[y] ? Integer.compare(r[y], r[x]) : f[x].compareTo(f[y]));
                    List<String> want = new ArrayList<>();
                    for (int k = 0; k < Math.min(2, ids.size()); k++) want.add(f[ids.get(k)]);
                    if (!s.topTwo(cu).equals(want)) throw new AssertionError("topTwo");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Movie Desk With Strict Moves (LeetCode 1912)
<!-- id: ci40-movie-desk -->

**Approach.** Each copy is an object with its price, shop, movie and a mutable state flag. A hash map from the pair of shop and movie to the copy is the record that decides. Two views exist: an array of two sets indexed by state, where the unrented view is a map from movie to a tree set, and the rented view is one tree set. A move helper checks that the copy exists and holds the expected state before it writes anything. It then removes the copy from the view of its old state, flips the flag and inserts the copy into the view of its new state.

The flag changes after the removal and before the insertion, and the sets order only by price, shop and movie, never by the flag, so a flag change cannot disturb a set. A rejected call returns `false` before any write.

The invariant is that a copy with state unrented sits in exactly its movie's unrented set, and a copy with state rented sits in the rented set.

**Complexity.**

- **Time** is O(log n) per rent and drop, and O(log n + 3) per search.
- **Space** is O(n), because each copy sits in one map slot and one set.

```java run
import java.util.*;

public final class MovieDeskSolution {
    static final class MovieDesk {
        private static final class Copy {
            final int price, shop, movie;
            boolean rented;
            Copy(int price, int shop, int movie) { this.price = price; this.shop = shop; this.movie = movie; }
        }
        private static final Comparator<Copy> ORDER = (a, b) -> {
            int c = Integer.compare(a.price, b.price);
            if (c != 0) return c;
            c = Integer.compare(a.shop, b.shop);
            return c != 0 ? c : Integer.compare(a.movie, b.movie);
        };
        private final Map<Long, Copy> copyAt = new HashMap<>();
        private final Map<Integer, TreeSet<Copy>> unrented = new HashMap<>();
        private final TreeSet<Copy> rented = new TreeSet<>(ORDER);

        private static long key(int shop, int movie) { return ((long) shop << 32) | movie; }

        MovieDesk(int[][] entries) {
            for (int[] e : entries) {
                Copy c = new Copy(e[2], e[0], e[1]);
                copyAt.put(key(e[0], e[1]), c);
                unrented.computeIfAbsent(e[1], k -> new TreeSet<>(ORDER)).add(c);
            }
        }

        /**
         * Moves a copy from one state to the other, or rejects the call.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the checks run before the first write.
         */
        private boolean move(int shop, int movie, boolean fromRented) {
            Copy c = copyAt.get(key(shop, movie));
            if (c == null || c.rented != fromRented) return false;
            if (fromRented) rented.remove(c); else unrented.get(movie).remove(c);
            c.rented = !fromRented;
            if (c.rented) rented.add(c); else unrented.get(movie).add(c);
            return true;
        }

        boolean rent(int shop, int movie) { return move(shop, movie, false); }

        boolean drop(int shop, int movie) { return move(shop, movie, true); }

        /** Returns up to 3 cheapest shops with an unrented copy; O(log n) time, O(1) extra space. */
        List<Integer> search(int movie) {
            List<Integer> out = new ArrayList<>();
            for (Copy c : unrented.getOrDefault(movie, new TreeSet<>(ORDER))) {
                if (out.size() == 3) break;
                out.add(c.shop);
            }
            return out;
        }

        /** Returns the number of rented copies; O(1) time and space. */
        int rentedCount() { return rented.size(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        int[][] entries = {{0, 1, 5}, {1, 1, 4}, {2, 1, 4}};
        MovieDesk a = new MovieDesk(entries);
        if (!a.search(1).equals(List.of(1, 2, 0))) throw new AssertionError("e1 search");
        if (!a.rent(1, 1) || a.rent(1, 1) || !a.search(1).equals(List.of(2, 0))) throw new AssertionError("e1 rent");
        MovieDesk b = new MovieDesk(entries);
        if (b.drop(0, 1) || b.rent(9, 9) || !b.rent(0, 1) || b.rentedCount() != 1) throw new AssertionError("e2");
        // Random calls checked against boolean flags and a sort.
        Random rnd = new Random(9103);
        for (int round = 0; round < 200; round++) {
            List<int[]> list = new ArrayList<>();
            for (int s = 0; s < 4; s++) for (int v = 0; v < 3; v++) if (rnd.nextInt(3) > 0) list.add(new int[] {s, v, 1 + rnd.nextInt(4)});
            int[][] es = list.toArray(new int[0][]);
            MovieDesk sut = new MovieDesk(es);
            boolean[] out = new boolean[es.length];
            for (int op = 0; op < 100; op++) {
                int s = rnd.nextInt(5), v = rnd.nextInt(4), t = rnd.nextInt(3), idx = -1;
                for (int i = 0; i < es.length; i++) if (es[i][0] == s && es[i][1] == v) idx = i;
                if (t == 0) { boolean want = idx >= 0 && !out[idx]; if (want) out[idx] = true; if (sut.rent(s, v) != want) throw new AssertionError("rent"); }
                else if (t == 1) { boolean want = idx >= 0 && out[idx]; if (want) out[idx] = false; if (sut.drop(s, v) != want) throw new AssertionError("drop"); }
                else {
                    List<int[]> cand = new ArrayList<>();
                    for (int i = 0; i < es.length; i++) if (es[i][1] == v && !out[i]) cand.add(es[i]);
                    cand.sort((x, y) -> x[2] != y[2] ? Integer.compare(x[2], y[2]) : Integer.compare(x[0], y[0]));
                    List<Integer> want = new ArrayList<>();
                    for (int i = 0; i < Math.min(3, cand.size()); i++) want.add(cand.get(i)[0]);
                    int cnt = 0;
                    for (boolean o : out) if (o) cnt++;
                    if (!sut.search(v).equals(want) || sut.rentedCount() != cnt) throw new AssertionError("search or count");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Task Desk With Two Exits (LeetCode 3408)
<!-- id: ci40-task-desk -->

**Approach.** A hash map from task id to an immutable task is the record that decides. The global index is a tree set of all tasks, and the owner index is a map from user to a tree set of that user's tasks. Both sets order by higher priority and then larger task id. Two private helpers write every structure. The insert helper writes the record and both indexes. The drop helper removes the task from the record and both indexes, and deletes an owner set that becomes empty.

An add call inserts. An edit call drops the stored task and inserts a copy with the new priority. A remove call drops the stored task. Each execute call reads the first task of its index and then drops it, so the other index loses the task in the same call.

The invariant says all three structures hold the same tasks with equal fields after every call. No public method writes a structure except through the helpers.

**Complexity.**

- **Time** is O(log n) per call, from a constant number of hash and tree operations.
- **Space** is O(n), because a task appears in the record and in two sets.

```java run
import java.util.*;

public final class TaskDeskSolution {
    static final class TaskDesk {
        private record Task(int priority, int id, int user) {}
        private static final Comparator<Task> ORDER = (a, b) ->
                a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(b.id(), a.id());
        private final Map<Integer, Task> byId = new HashMap<>();
        private final TreeSet<Task> global = new TreeSet<>(ORDER);
        private final Map<Integer, TreeSet<Task>> perUser = new HashMap<>();

        // Writes the record and both indexes; O(log n) time, O(1) space.
        private void insert(Task t) {
            byId.put(t.id(), t);
            global.add(t);
            perUser.computeIfAbsent(t.user(), k -> new TreeSet<>(ORDER)).add(t);
        }

        // Removes the exact task from the record and both indexes; O(log n) time, O(1) space; invariant: the only removal path.
        private void drop(Task t) {
            byId.remove(t.id());
            global.remove(t);
            TreeSet<Task> mine = perUser.get(t.user());
            mine.remove(t);
            // An empty owner set is deleted so unknown users and idle users look alike.
            if (mine.isEmpty()) perUser.remove(t.user());
        }

        void add(int user, int id, int priority) { insert(new Task(priority, id, user)); }

        void edit(int id, int priority) {
            Task old = byId.get(id);
            drop(old);
            insert(new Task(priority, id, old.user()));
        }

        void rmv(int id) { drop(byId.get(id)); }

        /** Runs the best task overall; O(log n) time, O(1) space; invariant: the task leaves every structure. */
        int execGlobal() {
            if (global.isEmpty()) return -1;
            Task t = global.first();
            drop(t);
            return t.id();
        }

        /** Runs the best task of one user; O(log n) time, O(1) space; invariant: the task leaves every structure. */
        int execUser(int user) {
            TreeSet<Task> mine = perUser.get(user);
            if (mine == null) return -1;
            Task t = mine.first();
            drop(t);
            return t.id();
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        TaskDesk a = new TaskDesk();
        a.add(1, 101, 5); a.add(1, 102, 7); a.add(2, 103, 7);
        if (a.execUser(1) != 102 || a.execGlobal() != 103 || a.execGlobal() != 101) throw new AssertionError("e1");
        TaskDesk b = new TaskDesk();
        if (b.execUser(3) != -1) throw new AssertionError("e2 empty");
        b.add(3, 200, 1);
        if (b.execGlobal() != 200 || b.execUser(3) != -1) throw new AssertionError("e2 after");
        // Random calls checked against a scan of a plain map.
        Random rnd = new Random(9104);
        for (int round = 0; round < 300; round++) {
            TaskDesk s = new TaskDesk();
            Map<Integer, int[]> ref = new HashMap<>();
            int next = 0;
            for (int op = 0; op < 120; op++) {
                int t = rnd.nextInt(5);
                List<Integer> ids = new ArrayList<>(ref.keySet());
                if (t == 0) { int u = 1 + rnd.nextInt(3), p = rnd.nextInt(4); ref.put(next, new int[] {u, p}); s.add(u, next++, p); }
                else if (t == 1 && !ids.isEmpty()) { int id = ids.get(rnd.nextInt(ids.size())), p = rnd.nextInt(4); ref.get(id)[1] = p; s.edit(id, p); }
                else if (t == 2 && !ids.isEmpty()) { int id = ids.get(rnd.nextInt(ids.size())); ref.remove(id); s.rmv(id); }
                else {
                    int user = t == 3 ? 0 : 1 + rnd.nextInt(3), best = -1;
                    for (int id : ids) {
                        if (user != 0 && ref.get(id)[0] != user) continue;
                        if (best == -1 || ref.get(id)[1] > ref.get(best)[1] || (ref.get(id)[1] == ref.get(best)[1] && id > best)) best = id;
                    }
                    if (best != -1) ref.remove(best);
                    int got = user == 0 ? s.execGlobal() : s.execUser(user);
                    if (got != best) throw new AssertionError("exec");
                }
            }
        }
    }
}
```
