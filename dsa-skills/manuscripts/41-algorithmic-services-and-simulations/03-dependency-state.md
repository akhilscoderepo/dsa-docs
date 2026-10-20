<!-- lesson-kind: standard -->
<!-- lesson-id: dependency-state -->
## Update Values That Depend On Others

<!-- stage: context -->
### A Total That Ignores The Edit

A budget sheet has a cell `rent` that holds 900, a cell `food` that holds 800, and a cell `total` that holds the formula `rent + food`. The sheet shows 1700 in `total`. The user raises `rent` to 1000, and `total` still shows 1700.

The sheet answered the first read correctly and the second read wrongly. Nothing crashed, so the error stays invisible until someone adds the numbers by hand. Another cell may read `total`, and then that cell is wrong too.

This lesson asks how a sheet, an expression tree or a rule engine can keep every computed value correct after any edit, without recomputing the whole sheet on each read.

<!-- stage: naive -->
### Storing The Sum When It Is Set

The direct design computes a formula once, at the moment the user enters it. It stores the resulting number in the cell and treats it like any other number.

```java
final class NaiveSheet {
    private final Map<String, Long> value = new HashMap<>();

    void setLiteral(String cell, long v) { value.put(cell, v); }

    void setSum(String cell, String... refs) {
        long sum = 0;
        for (String r : refs) sum += value.getOrDefault(r, 0L);   // reads the other cells once
        value.put(cell, sum);                                      // the result is saved as a plain number
    }

    long get(String cell) { return value.getOrDefault(cell, 0L); }
}
```

Every read costs one hash lookup, which is fast. The saved result stays the same after a later edit of a cell that the formula read.

```predict
The sheet runs setLiteral("a", 3), setLiteral("b", 4), setSum("c", "a", "b") and setLiteral("a", 10). What does get("c") return, and what should it return?

The call returns 7, because the sum was saved when c was set and nothing touched c afterward. It should return 14, because c is defined as a plus b and a is now 10. The saved number lost the link to the cells it came from.
```

<!-- stage: bottleneck -->
### Stale Results Or Full Recomputation

The design gives a wrong answer, so correctness is the first problem. Two quick repairs exist, and each has a cost. The first repair stores only the formulas and evaluates the whole chain on every read. A read costs O(n) for n formula cells only while no cell is referenced twice. Take a diamond: cell `top` sums `left` and `right`, and both of those sum `base`. The read of `top` evaluates `base` twice. Stack k such diamonds in a row and the read evaluates the bottom cell 2^k times. The worst-case cost grows exponentially.

The second repair recomputes every formula cell after each edit. An edit then costs O(n) even when it touches one cell that nothing reads. A sheet with thousands of formulas and mostly local edits wastes nearly all of that work.

Both repairs miss the key fact. An edit affects only the cells that read the edited cell, directly or through other formulas. The sheet has no record of who reads whom, so it cannot find those cells without scanning everything.

<!-- stage: insight -->
### Recompute Only Cells Affected By Edits

Keep the formula of every cell as authoritative data, and keep two derived structures beside it. The first is a **cached value** for each formula cell. A read returns it in O(1) time. The second is a map from each cell to its **dependents**, which are the cells whose formulas name that cell.

#### Propagating An Edit

When a cell changes, the sheet visits its dependents, then their dependents, and so on. It recomputes each visited cell once, and it does so in an order where every cell comes after all the cells it reads. A depth-first search over the dependents map gives that order when the search records each cell after its dependents and the sheet reverses the list. After the cycle check, the cost of propagating an edit is the size of the affected region, not the size of the sheet.

#### Rejecting A Bad Formula First

A new formula can name a cell that already reads the edited cell. Then the two cells would wait for each other, and no evaluation order exists. The **cycle check** runs before any write. It searches from the proposed references along the existing formulas, and it rejects the formula if the search reaches the edited cell. A rejected call changes nothing.

#### Replacing A Formula

Before an edited cell gets a new definition, the sheet removes the cell from the dependents of each cell its old formula read. Skipping that step leaves stale entries that later trigger recomputation of a cell that no longer reads them.

The invariant is that every cached value equals its formula applied to the current values of the cells it reads, and the dependents map lists exactly the cells that name each cell.

<!-- names: cached value, dependents, cycle check -->

<!-- stage: variables -->
### State Kept For Each Cell

The service lives in one object in memory. It has no files, no threads and no limit other than memory. The contract limits it to a few thousand cells. Four kinds of state describe each cell.

- **Literal** is the number a user typed, and it is authoritative until the cell gets a formula.
- **Formula** is the list of cells that the cell sums, with repeats, and it is authoritative for a formula cell.
- **Value** is the current number of a cell, and for a formula cell it is derived from the formula.
- **Dependents** is the derived set of cells that name this cell in a formula.

An edit rewrites the literal or the formula first. It then repairs the value and the dependents in the same call.

<!-- stage: trace -->
### Following Edits Through Formulas

#### A Chain That Updates

The first trace edits a sheet with the formula cells `c` and `d`. The pointer `call` marks the latest call, and the variables show every value after it.

```trace
{"cells":["a=3","b=4","c=a+b","d=c+a","a=10","b=1"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"values":"a=3","recomputed":"none"},"note":"Call 0: the sheet stores 3 in a, and it recomputes no formula cells."},{"at":{"call":1},"vars":{"values":"a=3 b=4","recomputed":"none"},"note":"Call 1: the sheet stores 4 in b, and it recomputes no formula cells."},{"at":{"call":2},"vars":{"values":"a=3 b=4 c=7","recomputed":"c"},"note":"Call 2: the sheet gives c the formula a+b, and it recomputes c."},{"at":{"call":3},"vars":{"values":"a=3 b=4 c=7 d=10","recomputed":"d"},"note":"Call 3: the sheet gives d the formula c+a, and it recomputes d."},{"at":{"call":4},"vars":{"values":"a=10 b=4 c=14 d=24","recomputed":"c,d"},"note":"Call 4: the sheet stores 10 in a, and it recomputes c,d."},{"at":{"call":5},"vars":{"values":"a=10 b=1 c=11 d=21","recomputed":"c,d"},"note":"Call 5: the sheet stores 1 in b, and it recomputes c,d."}]}
```

Call 4 changes `a`, which both `c` and `d` read. The sheet recomputes `c` first and `d` second, so `d` reads the fresh value of `c`.

#### Replacing And Rejecting Formulas

The second trace shows a repeated reference, a rejected formula and a replaced formula. The variables show the dependents of cell `a` after each call.

```trace
{"cells":["a=2","b=5","e=a+a","a=e","e=b","a=9","b=6"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"values":"a=2","dependents of a":"{}","result":"true"},"note":"Call 0: the literal 2 goes into a, and the sheet recomputes no formula cells."},{"at":{"call":1},"vars":{"values":"a=2 b=5","dependents of a":"{}","result":"true"},"note":"Call 1: the literal 5 goes into b, and the sheet recomputes no formula cells."},{"at":{"call":2},"vars":{"values":"a=2 b=5 e=4","dependents of a":"{e}","result":"true"},"note":"Call 2: e gets the formula a+a, and the sheet recomputes e."},{"at":{"call":3},"vars":{"values":"a=2 b=5 e=4","dependents of a":"{e}","result":"false"},"note":"Call 3: e already reads a, so the cycle check rejects the formula and nothing changes."},{"at":{"call":4},"vars":{"values":"a=2 b=5 e=5","dependents of a":"{}","result":"true"},"note":"Call 4: e gets the formula b, and the sheet recomputes e."},{"at":{"call":5},"vars":{"values":"a=9 b=5 e=5","dependents of a":"{}","result":"true"},"note":"Call 5: the literal 9 goes into a, and the sheet recomputes no formula cells."},{"at":{"call":6},"vars":{"values":"a=9 b=6 e=6","dependents of a":"{}","result":"true"},"note":"Call 6: the literal 6 goes into b, and the sheet recomputes e."}]}
```

Call 3 asks `a` to read `e`, which already reads `a`. The cycle check finds that loop and the call returns false with no change. Call 4 replaces the formula of `e`, so `e` leaves the dependents of `a`. Call 5 then edits `a` and recomputes nothing.

<!-- stage: code -->
### A Sheet That Refreshes Dependents

The class stores formulas, cached values and dependents, and it checks for a cycle before it writes anything.

```java
final class LiveSheet {
    private final Map<String, List<String>> formula = new HashMap<>();
    private final Map<String, Set<String>> dependents = new HashMap<>();
    private final Map<String, Long> value = new HashMap<>();

    long get(String cell) { return value.getOrDefault(cell, 0L); }

    void setLiteral(String cell, long v) {
        detach(cell);                                  // a literal has no formula and reads nothing
        value.put(cell, v);
        refresh(cell);                                 // dependents see the new number
    }

    boolean setFormula(String cell, List<String> refs) {
        if (reaches(refs, cell)) return false;         // reject before any write
        detach(cell);
        formula.put(cell, new ArrayList<>(refs));
        for (String r : refs) dependents.computeIfAbsent(r, k -> new HashSet<>()).add(cell);
        refresh(cell);
        return true;
    }

    private void detach(String cell) {
        List<String> old = formula.remove(cell);       // forget the old formula
        if (old != null) for (String r : old) dependents.get(r).remove(cell);
    }

    private boolean reaches(List<String> from, String target) {
        Deque<String> stack = new ArrayDeque<>(from);
        Set<String> seen = new HashSet<>();
        while (!stack.isEmpty()) {
            String c = stack.pop();
            if (c.equals(target)) return true;         // the target would read itself
            if (seen.add(c)) stack.addAll(formula.getOrDefault(c, List.of()));
        }
        return false;
    }

    private void refresh(String start) {
        List<String> post = new ArrayList<>();
        collect(start, new HashSet<>(), post);
        Collections.reverse(post);                     // each cell now follows every cell it reads
        for (String c : post) {
            List<String> f = formula.get(c);
            if (f == null) continue;                   // literal cells keep their number
            long sum = 0;
            for (String r : f) sum += get(r);
            value.put(c, sum);
        }
    }

    private void collect(String c, Set<String> seen, List<String> post) {
        if (!seen.add(c)) return;
        for (String d : dependents.getOrDefault(c, Set.of())) collect(d, seen, post);
        post.add(c);                                   // recorded after all of its dependents
    }
}
```

A read costs O(1). A formula edit first runs the cycle check, and `reaches` walks every cell upstream of the named cells. The worst case is O(n + e) for n cells and e formula entries. The refresh then adds O(A) for A affected cells and their formula entries. The space is O(n + e).

<!-- stage: applicability -->
### Values Computed From Other Values

#### Recognizing The Pattern

The cue is a stored value that the API defines in terms of other stored values, such as a spreadsheet cell, a tree of operators or a score built from sub-scores. Ask whether a read must show the result of the latest edit. If yes, list which values each formula reads, because those edges decide what an edit must touch.

#### Choosing Where To Compute

Compute on read when edits are frequent and reads are rare, or when the dependency chain is short. Cache and propagate when reads dominate. A query that is never stored, such as a formula passed to a single call, needs no edges at all.

#### False Friends

A cache without dependents looks fast and returns stale values, so it is a false friend of this lesson. A reverse map without the removal step in `detach` looks complete and keeps edges to formulas that were replaced. A recursive evaluation that skips the cycle check loops forever on a cyclic formula. The invariant of this lesson is what exposes each of these: after every call, each cached value must match a fresh evaluation of its formula.

<!-- stage: exercises -->
### Exercises

#### [Build] Expression Tree Evaluation (LeetCode 1628)
<!-- id: sv-dep-expression-tree -->

**Prerequisites.** Stacks and recursion.

**Problem.** This chapter states its own contract, which may differ in detail from LeetCode. Implement `build(postfix)`, which takes an array of string tokens in postfix order and returns an expression object. A token is either a nonnegative integer or one of the operators `+`, `-`, `*` and `/`. The object has the method `evaluate()`. It returns the value of the expression, where an operator applies to its left and right subexpressions and `/` truncates toward zero. Calling `evaluate()` again returns the same value.

**Constraints.** The limits are:
- **Tokens** number from 1 to 100, and the array is a valid postfix expression.
- **Operands** are integers from 0 to 100.
- **Values** at every step fit in an `int`, and no division has a zero divisor.
- **Return** is an `int`.

**Example 1.** Input `["3","4","+","2","*"]`, output 14.

**Example 2.** Input `["0","7","-","2","/"]`, output -3.

**Hint.** What does an operand return, and what does an operator need from its two children?

**Changed decision.** An operand node returns its own number and an operator node asks its two children, so evaluation follows the child edges and no node keeps a result.

#### [Vary] Excel Sum Formula (LeetCode 631)
<!-- id: sv-dep-excel-sum -->

**Prerequisites.** The expression tree exercise above and hash sets.

**Problem.** Design a class `Excel` for a grid with `height` rows numbered from 1 and `width` columns named from `A`. All cells start at 0. The call `set(row, col, v)` stores the number `v` and removes any formula from the cell. The call `get(row, col)` returns the current value. The call `sum(row, col, refs)` gives the cell a formula and returns its value. Each string in `refs` is a single cell such as `A1` or a rectangle such as `A1:B2`, and the formula adds the cell once for every time it is named. No formula reads its own cell, directly or through other cells.

**Constraints.** The limits are:
- **Grid** has at most 26 rows and the columns `A` to `Z`.
- **Values** passed to `set` are integers from 0 to 100.
- **Values** held by any cell fit in an `int`.
- **Return** of `get` and `sum` is an `int`.

**Example 1.** Input `Excel(3,"C")`, `set(1,"A",2)`, `sum(3,"C",["A1","A1:B2"])`, output 4.

**Example 2.** Input the same calls, then `set(2,"B",5)`, `get(3,"C")`, `sum(1,"A",["B2"])`, `get(3,"C")`, output 9, 5 and 15.

**Hint.** Which counts does a formula store when two references name the same cell?

**Changed decision.** A formula stores a count per cell and expands each rectangle into those counts, so a cell named twice adds twice and an edit of it recomputes each formula once.

#### [Boundary] Dependency Cycle Policy (Author exercise)
<!-- id: sv-dep-cycle-policy -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Sheet` for cells named by lowercase strings. The call `setLiteral(cell, v)` stores the number and removes any formula. The call `setFormula(cell, refs)` makes the cell the sum of the cells in `refs`, with repeats counted, and returns `true`. It returns `false` and changes nothing when the new formula would make the cell depend on itself, directly or through other cells. The call `get(cell)` returns the current value. A cell that was never set has the value 0.

**Constraints.** The limits are:
- **Names** are strings of 1 to 8 lowercase letters.
- **Literals** are integers from -1000 to 1000.
- **Refs** holds 1 to 5 names, and it may repeat a name or name an unset cell.
- **Values** at every cell fit in a `long`.

**Example 1.** Input `setLiteral(a,3)`, `setLiteral(b,4)`, `setFormula(c,[a,b])`, `get(c)`, `setFormula(a,[c])`, `get(a)`, output `true` for the formula, 7, `false` and 3.

**Example 2.** Input `setFormula(x,[x])`, `setFormula(x,[y,y])`, `setLiteral(y,5)`, `get(x)`, `setFormula(y,[x])`, output `false`, `true`, 10 and `false`.

**Hint.** Which cells does a search follow to find out whether any new reference already depends on the target?

**Changed decision.** The call rejects a cycle by searching before any edge changes, so a rejected formula leaves the old formula, the cached values and the dependents untouched.

#### [Recognize] Design Spreadsheet (LeetCode 3484)
<!-- id: sv-dep-spreadsheet-query -->

**Prerequisites.** All three exercises above.

**Problem.** This is the chapter's own contract and may differ from LeetCode. Design a class `Spreadsheet` built from `rows`, with columns `A` to `Z`. All cells start at 0. The call `setCell(cell, v)` stores the number. The call `resetCell(cell)` sets the cell to 0 and returns the value it held. The call `getValue(formula)` takes a string `=X+Y` where each of `X` and `Y` is a nonnegative integer or a cell name, and returns the sum of the current values. The formula is a question and the sheet does not store it.

**Constraints.** The limits are:
- **Rows** are integers from 1 to 1000, and cell names such as `B17` are valid.
- **Values** stored by `setCell` are integers from 0 to 100000.
- **Formula** has exactly one `+`, and each integer in it is at most 100000.
- **Return** is an `int`.

**Example 1.** Input `Spreadsheet(3)`, `setCell(A1,2)`, `setCell(B2,5)`, `getValue(=A1+B2)`, `getValue(=A1+10)`, output 7 and 12.

**Example 2.** Input the same calls, then `getValue(=C3+C3)`, `resetCell(A1)`, `getValue(=A1+B2)`, `getValue(=7+8)`, output 0, 2, 5 and 15.

**Hint.** Does the sheet keep anything that has to change when a cell changes?

**Changed decision.** No formula is stored, so there is no cached value and no dependents map to repair, and the call parses its argument and reads the current cell values.
