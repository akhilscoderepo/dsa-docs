<!-- section: unlocked-combinations -->
## Unlocked Combinations

A path such as `/a/../b` looks like a plain string until a reader gives each piece a meaning and a stack keeps the unfinished part. This chapter releases one pairing that its prerequisites allow, and it names one pairing that waits for a later chapter.

### Pairing Taught In This Chapter

A stack and a reading step form the lesson Stack And Parsing State. The reading step turns text into tokens and decides what each token means. The stack keeps one frame for each unfinished level, so the reader can finish levels in reverse order. The lesson adds one idea: the contract decides what an empty pop, an unknown token or a size limit means. Its exercises cover a postfix formula with error codes, a nested decode with a length limit, a Unix path with a parent move at the root, and a calculator with named variables.

### One Stack Idea Comes Later

An ordinary stack keeps unfinished work in the order it started. It never removes a stored value because a newer value makes it useless. A later chapter adds that rule and uses it for next-larger-value and histogram problems. This chapter assigns none of those problems.

### What Later Chapters Reuse

Three ideas carry forward.

- **The saved frame** returns whenever a later method must restore a parent level after a child level ends.
- **The empty-stack rule** returns whenever a later reader pops and the contract says what a missing parent means.
- **The token check** returns whenever a later reader must reject a piece of text before it changes any state.
