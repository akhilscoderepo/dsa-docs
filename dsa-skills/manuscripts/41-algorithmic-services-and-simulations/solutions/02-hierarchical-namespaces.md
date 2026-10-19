<!-- solutions-for: 02-hierarchical-namespaces -->
### Solutions For Resolve Paths In A Tree

#### Solution: [Build] Design File System (LeetCode 1166)
<!-- id: sv-hier-file-system -->

**Approach.** Each node holds a value and a hash map from a child name to a child node. The root is an empty node that always exists. A create call splits the path into names and walks from the root through all names except the last. If a lookup returns null, the parent is missing and the call returns false before it writes. When the walk succeeds, the call checks that the last name is free and then adds one node.

The invariant is that every stored node is reachable from the root through its names, so no node exists without its parent. The only write of a create call comes after all checks.

**Complexity.**

- **Time** is O(L) per call for a path of length L, because splitting reads each character once and the walk does one lookup per name.
- **Space** is O(N) for N stored nodes, plus O(L) for the split of one call.

```java run
import java.util.*;

public final class FileSystemSolution {
    static final class FileSystem {
        private static final class Node {
            final Map<String, Node> kids = new HashMap<>();
            int value = -1;
        }

        private final Node root = new Node();

        /**
         * Creates a path whose parent exists and whose own name is free.
         * Time: O(L) for a path of length L.
         * Space: O(L) for the split names.
         * Invariant: the node is added only after every ancestor has been found.
         */
        boolean createPath(String path, int value) {
            // Split into the names between separators.
            String[] part = path.substring(1).split("/");
            Node cur = root;
            // Walk to the parent: one lookup per name.
            for (int i = 0; i < part.length - 1; i++) {
                cur = cur.kids.get(part[i]);
                // A missing ancestor means the parent does not exist, so nothing is written.
                if (cur == null) return false;
            }
            String last = part[part.length - 1];
            // An existing name keeps its old value.
            if (cur.kids.containsKey(last)) return false;
            // The single write of the call.
            Node fresh = new Node();
            fresh.value = value;
            cur.kids.put(last, fresh);
            return true;
        }

        /** Returns the stored value or -1; O(L) time, O(L) space; invariant: read-only walk. */
        int get(String path) {
            Node cur = root;
            // One lookup per name.
            for (String name : path.substring(1).split("/")) {
                cur = cur.kids.get(name);
                if (cur == null) return -1;
            }
            return cur.value;
        }
    }

    /** Flat oracle: a map from the full path to the value, with the parent cut from the string. */
    static final class Oracle {
        final Map<String, Integer> m = new HashMap<>();
        boolean createPath(String p, int v) {
            String parent = p.substring(0, p.lastIndexOf('/'));
            if (!parent.isEmpty() && !m.containsKey(parent)) return false;
            if (m.containsKey(p)) return false;
            m.put(p, v);
            return true;
        }
        int get(String p) { return m.getOrDefault(p, -1); }
    }

    public static void main(String[] args) {
        // Example 1.
        FileSystem f = new FileSystem();
        check(f.createPath("/a", 1), "e1 a");
        check(f.createPath("/a/b", 2), "e1 b");
        if (f.get("/a/b") != 2) throw new AssertionError("e1 get");
        check(!f.createPath("/c/d", 3), "e1 missing parent");
        if (f.get("/c/d") != -1) throw new AssertionError("e1 no partial path");
        if (f.get("/c") != -1) throw new AssertionError("e1 no intermediate node");
        // Example 2.
        FileSystem g = new FileSystem();
        check(g.createPath("/a", 1), "e2 a");
        check(!g.createPath("/a", 5), "e2 duplicate");
        if (g.get("/a") != 1) throw new AssertionError("e2 old value kept");
        check(!g.createPath("/a/b/c", 4), "e2 deep");
        if (g.get("/a/b") != -1) throw new AssertionError("e2 no partial path");
        // Random calls against the flat oracle.
        Random rnd = new Random(1166);
        String[] names = {"a", "b", "c"};
        for (int round = 0; round < 300; round++) {
            FileSystem s = new FileSystem();
            Oracle o = new Oracle();
            for (int op = 0; op < 80; op++) {
                StringBuilder sb = new StringBuilder();
                int depth = 1 + rnd.nextInt(3);
                for (int i = 0; i < depth; i++) sb.append('/').append(names[rnd.nextInt(3)]);
                String p = sb.toString();
                if (rnd.nextBoolean()) {
                    int v = 1 + rnd.nextInt(100);
                    if (s.createPath(p, v) != o.createPath(p, v)) throw new AssertionError("create " + p);
                }
                if (s.get(p) != o.get(p)) throw new AssertionError("get " + p);
            }
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }
}
```

#### Solution: [Vary] Design In-Memory File System (LeetCode 588)
<!-- id: sv-hier-in-memory-fs -->

**Approach.** A node is a directory with a sorted map of children, or a file with a text buffer. The root is a directory. A helper splits a path into names, where the root path gives an empty list.

Every writing call runs two passes. The first pass only reads. It follows existing nodes and stops at the first missing name, where it accepts, or at a file in the middle of the path, where it rejects. It also rejects when the last name exists with the wrong kind. The second pass walks again and creates the missing directories, and it creates the final file for an append. Because every name below a missing node is also missing, the second pass never meets a file, so a rejected call has written nothing.

The invariant is that every node is reachable from the root, and only directories have children. Listing a directory reads the keys of one sorted map, so the order is lexicographic without sorting.

**Complexity.**

- **Time** is O(L) per path of length L for walking and creating, plus O(k) to list k children and O(T) to append T characters.
- **Space** is O(N + C) for N nodes and C characters of file content.

```java run
import java.util.*;

public final class InMemoryFsSolution {
    static final class Fs {
        private static final class Node {
            final TreeMap<String, Node> kids; // null for a file
            final StringBuilder text;         // null for a directory
            Node(boolean file) {
                kids = file ? null : new TreeMap<>();
                text = file ? new StringBuilder() : null;
            }
            boolean isFile() { return text != null; }
        }

        private final Node root = new Node(false);

        private static String[] split(String path) {
            return path.equals("/") ? new String[0] : path.substring(1).split("/");
        }

        /**
         * Read-only check that the path can be created as a file or a directory.
         * Time: O(L).
         * Space: O(1) extra.
         * Invariant: no node changes during the check.
         */
        private boolean canCreate(String[] part, boolean wantFile) {
            // The root is a directory, so it can be a mkdir target and never a file.
            if (part.length == 0) return !wantFile;
            Node cur = root;
            for (int i = 0; i < part.length; i++) {
                Node child = cur.kids.get(part[i]);
                // The first missing name ends the walk; everything below it will be new.
                if (child == null) return true;
                boolean lastName = i == part.length - 1;
                // An existing file blocks the path unless it is the final name of an append.
                if (child.isFile()) return lastName && wantFile;
                // An existing directory at the final name is fine only for mkdir.
                if (lastName) return !wantFile;
                cur = child;
            }
            return true;
        }

        /** Creates missing directories for the first count names; the walk never meets a file after canCreate. */
        private Node ensureDirs(String[] part, int count) {
            Node cur = root;
            for (int i = 0; i < count; i++) {
                Node child = cur.kids.get(part[i]);
                if (child == null) { child = new Node(false); cur.kids.put(part[i], child); }
                cur = child;
            }
            return cur;
        }

        boolean mkdir(String path) {
            String[] part = split(path);
            // Validate before any write.
            if (!canCreate(part, false)) return false;
            ensureDirs(part, part.length);
            return true;
        }

        boolean addContentToFile(String path, String text) {
            String[] part = split(path);
            // Validate before any write.
            if (!canCreate(part, true)) return false;
            Node dir = ensureDirs(part, part.length - 1);
            String name = part[part.length - 1];
            Node file = dir.kids.get(name);
            if (file == null) { file = new Node(true); dir.kids.put(name, file); }
            file.text.append(text);
            return true;
        }

        String readContentFromFile(String path) {
            Node cur = root;
            for (String name : split(path)) {
                if (cur.isFile()) return "";
                cur = cur.kids.get(name);
                if (cur == null) return "";
            }
            return cur.isFile() ? cur.text.toString() : "";
        }

        List<String> ls(String path) {
            String[] part = split(path);
            Node cur = root;
            for (String name : part) {
                if (cur.isFile()) return List.of();
                cur = cur.kids.get(name);
                if (cur == null) return List.of();
            }
            // A file lists only its own name; a directory lists its sorted keys.
            if (cur.isFile()) return List.of(part[part.length - 1]);
            return new ArrayList<>(cur.kids.keySet());
        }
    }

    /** Flat oracle: sets of directory paths and a map of file paths, scanned linearly. */
    static final class Oracle {
        final Set<String> dirs = new HashSet<>(Set.of("/"));
        final Map<String, StringBuilder> files = new HashMap<>();
        static List<String> prefixes(String p, boolean includeSelf) {
            List<String> out = new ArrayList<>();
            String[] part = p.equals("/") ? new String[0] : p.substring(1).split("/");
            String cur = "";
            for (int i = 0; i < part.length; i++) {
                cur += "/" + part[i];
                if (includeSelf || i < part.length - 1) out.add(cur);
            }
            return out;
        }
        boolean mkdir(String p) {
            for (String q : prefixes(p, true)) if (files.containsKey(q)) return false;
            dirs.addAll(prefixes(p, true));
            return true;
        }
        boolean add(String p, String t) {
            if (p.equals("/") || dirs.contains(p)) return false;
            for (String q : prefixes(p, false)) if (files.containsKey(q)) return false;
            dirs.addAll(prefixes(p, false));
            files.computeIfAbsent(p, k -> new StringBuilder()).append(t);
            return true;
        }
        String read(String p) { return files.containsKey(p) ? files.get(p).toString() : ""; }
        List<String> ls(String p) {
            if (files.containsKey(p)) return List.of(p.substring(p.lastIndexOf('/') + 1));
            if (!dirs.contains(p)) return List.of();
            TreeSet<String> out = new TreeSet<>();
            List<String> all = new ArrayList<>(dirs);
            all.addAll(files.keySet());
            for (String q : all) {
                if (q.equals("/")) continue;
                String parent = q.substring(0, q.lastIndexOf('/'));
                if (parent.isEmpty()) parent = "/";
                if (parent.equals(p)) out.add(q.substring(q.lastIndexOf('/') + 1));
            }
            return new ArrayList<>(out);
        }
    }

    public static void main(String[] args) {
        // Example 1.
        Fs f = new Fs();
        check(f.mkdir("/a/b"), "e1 mkdir");
        check(f.addContentToFile("/a/b/f", "hi"), "e1 add");
        check(f.addContentToFile("/a/b/f", "yo"), "e1 append");
        if (!f.readContentFromFile("/a/b/f").equals("hiyo")) throw new AssertionError("e1 read");
        if (!f.ls("/a/b").equals(List.of("f"))) throw new AssertionError("e1 ls dir");
        if (!f.ls("/a/b/f").equals(List.of("f"))) throw new AssertionError("e1 ls file");
        // Example 2.
        Fs g = new Fs();
        check(g.mkdir("/m"), "e2 m");
        check(g.mkdir("/b"), "e2 b");
        check(g.addContentToFile("/z", "q"), "e2 file");
        check(!g.mkdir("/z/y"), "e2 blocked by a file");
        if (!g.ls("/").equals(List.of("b", "m", "z"))) throw new AssertionError("e2 ls root");
        if (!g.ls("/z/y").isEmpty()) throw new AssertionError("e2 missing");
        // A rejected call creates nothing, and a directory is not a file.
        check(!g.addContentToFile("/m", "x"), "directory as file");
        check(!g.addContentToFile("/z/y/w", "x"), "file above");
        check(!g.addContentToFile("/", "x"), "root as file");
        if (!g.ls("/z/y").isEmpty()) throw new AssertionError("no partial dirs");
        // Random calls against the flat oracle.
        Random rnd = new Random(588);
        String[] names = {"a", "b", "c"};
        for (int round = 0; round < 300; round++) {
            Fs s = new Fs();
            Oracle o = new Oracle();
            for (int op = 0; op < 80; op++) {
                StringBuilder sb = new StringBuilder();
                int depth = rnd.nextInt(4);
                for (int i = 0; i < depth; i++) sb.append('/').append(names[rnd.nextInt(3)]);
                String p = depth == 0 ? "/" : sb.toString();
                switch (rnd.nextInt(3)) {
                    case 0 -> { if (s.mkdir(p) != o.mkdir(p)) throw new AssertionError("mkdir " + p); }
                    case 1 -> {
                        String t = "t" + rnd.nextInt(5);
                        if (s.addContentToFile(p, t) != o.add(p, t)) throw new AssertionError("add " + p);
                    }
                    default -> { }
                }
                if (!s.ls(p).equals(o.ls(p))) throw new AssertionError("ls " + p + " " + s.ls(p) + " " + o.ls(p));
                if (!s.readContentFromFile(p).equals(o.read(p))) throw new AssertionError("read " + p);
            }
            if (!s.ls("/").equals(o.ls("/"))) throw new AssertionError("ls root");
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }
}
```

#### Solution: [Boundary] Root And Repeated Separators (Author exercise)
<!-- id: sv-hier-root-separators -->

**Approach.** One function normalizes every incoming string into a list of names, or reports it as invalid. It rejects a string without a leading separator and any name equal to `.` or `..`, and it drops empty names. Every public call starts with this function, so no other code reads raw text.

A node holds a value, a hash map of children and a count of stored nodes below it. An add call first checks that the list is not empty. It then walks from the root and records the nodes it passes. A missing ancestor or an existing last name returns false. Only then does the call create the node and raise the count of every recorded ancestor by one. The count of the root is therefore the total number of stored paths.

The invariant is that each node's count equals the number of stored nodes in its subtree, excluding itself. The count changes only in the add call, after all checks pass.

**Complexity.**

- **Time** is O(L) per call for a string of length L, because normalizing reads each character. The walk and the count update touch at most one node per name. The call `below` reads the stored count of one node, so it costs O(depth) and not O(stored paths).
- **Space** is O(N + L) for N stored nodes and the names of one call.

```java run
import java.util.*;

public final class RootSeparatorsSolution {
    static final class Registry {
        private static final class Node {
            final Map<String, Node> kids = new HashMap<>();
            int value = -1;
            int below = 0;
        }

        private final Node root = new Node();

        /**
         * Turns a raw string into names, or returns null for an invalid string.
         * Time: O(L).
         * Space: O(L).
         * Invariant: the result has no empty name and no "." or ".." name.
         */
        static List<String> normalize(String path) {
            // The policy needs a leading separator.
            if (path.isEmpty() || path.charAt(0) != '/') return null;
            List<String> out = new ArrayList<>();
            int i = 0;
            while (i < path.length()) {
                // Skip every separator, which drops empty names.
                if (path.charAt(i) == '/') { i++; continue; }
                int j = i;
                while (j < path.length() && path.charAt(j) != '/') j++;
                String name = path.substring(i, j);
                // Only the exact names "." and ".." are illegal.
                if (name.equals(".") || name.equals("..")) return null;
                out.add(name);
                i = j;
            }
            return out;
        }

        boolean add(String path, int value) {
            List<String> part = normalize(path);
            // An invalid string or the root cannot hold a value.
            if (part == null || part.isEmpty()) return false;
            Node cur = root;
            List<Node> seen = new ArrayList<>();
            seen.add(root);
            // Walk to the parent and remember each ancestor.
            for (int i = 0; i < part.size() - 1; i++) {
                cur = cur.kids.get(part.get(i));
                if (cur == null) return false;
                seen.add(cur);
            }
            String last = part.get(part.size() - 1);
            if (cur.kids.containsKey(last)) return false;
            // All checks passed: write the node and then the counts of its ancestors.
            Node fresh = new Node();
            fresh.value = value;
            cur.kids.put(last, fresh);
            for (Node n : seen) n.below++;
            return true;
        }

        private Node find(String path) {
            List<String> part = normalize(path);
            if (part == null) return null;
            Node cur = root;
            for (String name : part) {
                cur = cur.kids.get(name);
                if (cur == null) return null;
            }
            return cur;
        }

        int get(String path) {
            Node n = find(path);
            // The root holds no value, so its stored -1 is the answer too.
            return n == null ? -1 : n.value;
        }

        int below(String path) {
            Node n = find(path);
            return n == null ? 0 : n.below;
        }
    }

    /** Oracle: canonical strings built with split, counted by scanning every key. */
    static final class Oracle {
        final Map<String, Integer> m = new HashMap<>();
        static String canon(String p) {
            if (!p.startsWith("/")) return null;
            StringBuilder sb = new StringBuilder();
            for (String s : p.split("/", -1)) {
                if (s.isEmpty()) continue;
                if (s.equals(".") || s.equals("..")) return null;
                sb.append('/').append(s);
            }
            return sb.length() == 0 ? "/" : sb.toString();
        }
        boolean add(String p, int v) {
            String c = canon(p);
            if (c == null || c.equals("/") || m.containsKey(c)) return false;
            String parent = c.substring(0, c.lastIndexOf('/'));
            if (!parent.isEmpty() && !m.containsKey(parent)) return false;
            m.put(c, v);
            return true;
        }
        int get(String p) {
            String c = canon(p);
            return c == null ? -1 : m.getOrDefault(c, -1);
        }
        int below(String p) {
            String c = canon(p);
            if (c == null) return 0;
            if (!c.equals("/") && !m.containsKey(c)) return 0;
            int n = 0;
            for (String k : m.keySet()) if (c.equals("/") || k.startsWith(c + "/")) n++;
            return n;
        }
    }

    public static void main(String[] args) {
        // Example 1.
        Registry r = new Registry();
        check(r.add("//a//", 1), "e1 a");
        check(r.add("/a/b/", 2), "e1 b");
        if (r.get("/a///b") != 2) throw new AssertionError("e1 get");
        check(!r.add("/", 5), "e1 root");
        if (r.below("/") != 2) throw new AssertionError("e1 below root");
        if (r.below("a") != 0) throw new AssertionError("e1 invalid");
        // Example 2.
        Registry q = new Registry();
        check(!q.add("/a/../b", 1), "e2 dotdot");
        check(q.add("/x", 4), "e2 x");
        check(q.add("/x/..y", 6), "e2 dotted name");
        check(!q.add("/x/.", 7), "e2 dot");
        if (q.get("/x//..y/") != 6) throw new AssertionError("e2 get");
        if (q.below("//x") != 1) throw new AssertionError("e2 below");
        // A failed add leaves the counts unchanged.
        check(!q.add("/p/q", 3), "missing parent");
        if (q.below("/") != 2) throw new AssertionError("failed add changed a count");
        // Random messy strings against the oracle.
        Random rnd = new Random(7702);
        String[] tok = {"a", "b", ".", "..", "x.", "..y"};
        for (int round = 0; round < 400; round++) {
            Registry s = new Registry();
            Oracle o = new Oracle();
            for (int op = 0; op < 60; op++) {
                String p = messy(rnd, tok);
                if (rnd.nextInt(3) != 0) {
                    int v = 1 + rnd.nextInt(50);
                    if (s.add(p, v) != o.add(p, v)) throw new AssertionError("add " + p);
                }
                String t = messy(rnd, tok);
                if (s.get(t) != o.get(t)) throw new AssertionError("get " + t);
                if (s.below(t) != o.below(t)) throw new AssertionError("below " + t);
            }
            if (s.below("/") != o.below("/")) throw new AssertionError("total");
        }
    }

    static String messy(Random rnd, String[] tok) {
        StringBuilder sb = new StringBuilder();
        if (rnd.nextInt(8) != 0) sb.append("/".repeat(1 + rnd.nextInt(3)));
        int n = rnd.nextInt(4);
        for (int i = 0; i < n; i++) {
            // Mostly valid names so that creates succeed often.
            sb.append(rnd.nextInt(5) == 0 ? tok[rnd.nextInt(tok.length)] : tok[rnd.nextInt(2)]);
            sb.append("/".repeat(1 + rnd.nextInt(2)));
        }
        return sb.toString();
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }
}
```

#### Solution: [Recognize] Design SQL (LeetCode 2408)
<!-- id: sv-hier-sql-tables -->

**Approach.** The table name is the first name of a two-level tree. A hash map from table name to a table record resolves it. A table record holds the column count, the next row id and a hash map from row id to the row array. The row id is the second name.

An insert validates the table name and the row length before it touches anything. Only after both checks does it read the counter, store the row and advance the counter by one. A failed insert therefore consumes no id. A delete removes the row from the map and never lowers the counter, so ids are not reused.

The invariant is that the counter of a table is larger than every id ever assigned, and the row map holds exactly the live rows.

**Complexity.**

- **Time** is O(c) per insert for c columns, because the row is copied, and O(1) expected for every other call.
- **Space** is O(R * c) for R live rows, plus O(T) for T tables.

```java run
import java.util.*;

public final class SqlSolution {
    static final class Sql {
        private static final class Table {
            final int columns;
            int nextId = 1;
            final Map<Integer, String[]> rows = new HashMap<>();
            Table(int columns) { this.columns = columns; }
        }

        private final Map<String, Table> tables = new HashMap<>();

        Sql(String[] names, int[] columns) {
            for (int i = 0; i < names.length; i++) tables.put(names[i], new Table(columns[i]));
        }

        /**
         * Appends a row and returns its id, or -1 with no change.
         * Time: O(c) for c columns.
         * Space: O(c) for the copied row.
         * Invariant: nextId advances only when a row is stored.
         */
        int insertRow(String name, String[] row) {
            Table t = tables.get(name);
            // Validate the table and the row length before any write.
            if (t == null || row.length != t.columns) return -1;
            int id = t.nextId++;
            t.rows.put(id, row.clone());
            return id;
        }

        boolean deleteRow(String name, int id) {
            Table t = tables.get(name);
            // The counter stays, so a deleted id is never handed out again.
            return t != null && t.rows.remove(id) != null;
        }

        String selectCell(String name, int id, int column) {
            Table t = tables.get(name);
            if (t == null || column < 1 || column > t.columns) return "";
            String[] row = t.rows.get(id);
            return row == null ? "" : row[column - 1];
        }

        int count(String name) {
            Table t = tables.get(name);
            return t == null ? -1 : t.rows.size();
        }
    }

    /** Oracle: a log of every successful insert per table, scanned linearly. */
    static final class Oracle {
        final List<String> names;
        final int[] cols;
        final List<List<Object[]>> log = new ArrayList<>(); // each entry: {id, row, live}
        Oracle(String[] n, int[] c) {
            names = Arrays.asList(n);
            cols = c;
            for (int i = 0; i < n.length; i++) log.add(new ArrayList<>());
        }
        int insert(String n, String[] row) {
            int t = names.indexOf(n);
            if (t < 0 || row.length != cols[t]) return -1;
            int id = log.get(t).size() + 1;
            log.get(t).add(new Object[] {id, row, true});
            return id;
        }
        boolean delete(String n, int id) {
            int t = names.indexOf(n);
            if (t < 0) return false;
            for (Object[] e : log.get(t)) if ((int) e[0] == id && (boolean) e[2]) { e[2] = false; return true; }
            return false;
        }
        String select(String n, int id, int c) {
            int t = names.indexOf(n);
            if (t < 0 || c < 1 || c > cols[t]) return "";
            for (Object[] e : log.get(t)) if ((int) e[0] == id && (boolean) e[2]) return ((String[]) e[1])[c - 1];
            return "";
        }
        int count(String n) {
            int t = names.indexOf(n);
            if (t < 0) return -1;
            int k = 0;
            for (Object[] e : log.get(t)) if ((boolean) e[2]) k++;
            return k;
        }
    }

    public static void main(String[] args) {
        String[] names = {"a", "b"};
        int[] cols = {2, 1};
        // Example 1.
        Sql s = new Sql(names, cols);
        if (s.insertRow("a", new String[] {"x", "y"}) != 1) throw new AssertionError("e1 first id");
        if (s.insertRow("a", new String[] {"p"}) != -1) throw new AssertionError("e1 bad length");
        if (s.insertRow("a", new String[] {"p", "q"}) != 2) throw new AssertionError("e1 failed insert kept its id");
        if (!s.selectCell("a", 2, 1).equals("p")) throw new AssertionError("e1 select");
        if (!s.deleteRow("a", 1)) throw new AssertionError("e1 delete");
        if (s.insertRow("a", new String[] {"m", "n"}) != 3) throw new AssertionError("e1 id reuse");
        if (s.count("a") != 2) throw new AssertionError("e1 count");
        // Example 2.
        Sql t = new Sql(names, cols);
        if (t.insertRow("c", new String[] {"z"}) != -1) throw new AssertionError("e2 unknown table");
        if (t.insertRow("b", new String[] {"k"}) != 1) throw new AssertionError("e2 first");
        if (!t.deleteRow("b", 1)) throw new AssertionError("e2 delete");
        if (t.deleteRow("b", 1)) throw new AssertionError("e2 second delete");
        if (!t.selectCell("b", 1, 1).isEmpty()) throw new AssertionError("e2 deleted cell");
        if (t.insertRow("b", new String[] {"w"}) != 2) throw new AssertionError("e2 next id");
        // Random calls against the log oracle.
        Random rnd = new Random(2408);
        String[] pool = {"a", "b", "c"};
        for (int round = 0; round < 300; round++) {
            Sql x = new Sql(names, cols);
            Oracle o = new Oracle(names, cols);
            for (int op = 0; op < 80; op++) {
                String n = pool[rnd.nextInt(3)];
                switch (rnd.nextInt(4)) {
                    case 0 -> {
                        String[] row = new String[1 + rnd.nextInt(3)];
                        for (int i = 0; i < row.length; i++) row[i] = "v" + rnd.nextInt(9);
                        if (x.insertRow(n, row) != o.insert(n, row)) throw new AssertionError("insert");
                    }
                    case 1 -> {
                        int id = 1 + rnd.nextInt(6);
                        if (x.deleteRow(n, id) != o.delete(n, id)) throw new AssertionError("delete");
                    }
                    case 2 -> {
                        int id = 1 + rnd.nextInt(6), c = rnd.nextInt(4);
                        if (!x.selectCell(n, id, c).equals(o.select(n, id, c))) throw new AssertionError("select");
                    }
                    default -> { if (x.count(n) != o.count(n)) throw new AssertionError("count"); }
                }
            }
        }
    }
}
```
