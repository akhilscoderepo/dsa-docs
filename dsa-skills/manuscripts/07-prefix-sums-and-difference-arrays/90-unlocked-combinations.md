<!-- section: unlocked-combinations -->
## Unlocked Combinations

Stored totals and hash maps each solve a part of the same questions. Counting windows needs a total that names each earlier boundary, and it needs a map that finds the matching boundary quickly. This chapter teaches that pairing as a lesson with exercises. Two other pairings wait for later chapters and are only named here.

### Pairing Taught In This Chapter

Prefix state with a hash map forms the lesson Count And Measure Spans With Maps. The total at each boundary names the earlier position, and the map stores either how many earlier boundaries share a state or where the first one sits. The lesson separates the choice of the key from the choice of the value, and its exercises change one of the two choices at a time.

### Pairings That Wait

Prefix sums with a sliding window are deferred to Chapter 09. A sliding window keeps two moving ends and one running total, and it needs the comparison of the window against a bound as the ends move. That comparison belongs to the sliding window chapter. No exercise here assigns those problems.

Range updates and range queries on the same changing array are deferred to the chapter on range query structures. A segment tree or a Fenwick tree answers both operations in logarithmic time. This chapter handles updates before one read, or queries on unchanged data, and it names the limit of each method. No exercise here assigns the mixed case.

### What Later Chapters Reuse

Three ideas carry forward.

- **The entry for zero values** returns in every later chapter that stores a quantity for the part of the input before a position.
- **The partner key of a boundary** returns when later chapters match an earlier state with the current one.
- **The four corner writes** return when a later chapter processes rectangles or events by sorting them and sweeping across.
