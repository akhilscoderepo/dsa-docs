<!-- section: unlocked-combinations -->
## Unlocked Combinations

One combination is released by this chapter, since each ingredient has been taught, and it has its own lesson and its own four-rung ladder. One more is named as deferred, with the chapter that owns it.

### Teach Now

Sliding windows with frequency state is the tenth lesson. Chapter 04 supplied counts kept per symbol, and this chapter supplied edges that move forward with one item entering and one leaving. Together they decide whether a stretch has the right letters, how long a repeat-free stretch can be, how much repair a stretch needs, and which shortest stretch covers a demand. The ladder moves from a matching counter through a leftmost longest stretch and an exact maximum to a count of minimal covers. The false friend is a set, which forgets how many copies were seen.

### Deferred

A window that must report its maximum or minimum at every position needs a structure that keeps ordered candidates and drops expired ones by index. That idea has not been taught, and Chapter 13 owns it. No problem of that kind is assigned here. Windows over sorted intervals belong to Chapter 10.

### Already Covered

Prefix sums were taught in Chapter 07, and the lessons here use them only as an oracle and as the alternative for stretches with negative values. Pointer movement with an invariant was taught in Chapter 08, and the window lessons assume it. Hash-map counts were taught in Chapter 04 and are used without being re-taught.
