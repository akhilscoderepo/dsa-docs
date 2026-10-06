<!-- section: unlocked-combinations -->
## Unlocked Combinations

An index that shortens words tests every root against every word, and a puzzle solver tries every dictionary word on every square. This chapter releases one pairing that its prerequisites allow, and it names one pairing that waits for a later chapter.

### Pairing Taught In This Chapter

A prefix tree and string positions form the lesson Look Up Prefixes In A Dictionary. The position in the string supplies the next symbol. The tree node supplies every dictionary entry that agrees with the symbols read so far. The lesson adds one idea. The walk stops at the first flagged node when the shortest entry is wanted, and it enters only flagged children when every shorter prefix must also be present. Its exercises cover a longest-match query, a smallest wildcard match, a sentence rewrite and the longest word built from its own prefixes.

### One Pairing Waits For A Later Chapter

A trie can also prune many board searches at once, because all words that share a prefix reuse one walk. A board search must mark cells as used, explore a neighbor and then restore the cell. That choose, explore and restore cycle belongs to Chapter 19. Chapter 19 owns the problems of this pairing, and this chapter assigns none of them.
