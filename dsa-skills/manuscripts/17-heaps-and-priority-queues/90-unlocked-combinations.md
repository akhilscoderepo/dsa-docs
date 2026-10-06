<!-- section: unlocked-combinations -->
## Unlocked Combinations

A booking tool that counts overlapping pairs reports three rooms where two suffice, and a graph search that trusts an old distance returns a wrong route. This chapter releases one pairing that its prerequisites allow, and it names one pairing that waits for a later chapter.

### Pairing Taught In This Chapter

Sorted intervals and a priority queue form the lesson Reuse Meeting Rooms With A Heap. Sorting by start time supplies the order in which meetings arrive. The queue of end times supplies the earliest finish among the rooms in use. The lesson adds one idea. A meeting reuses a room when the earliest finish does not pass the new start, and the strictness of that test follows from whether endpoints belong to the interval. Its exercises cover a yes or no check, the room count, the group count for closed intervals and the smallest interval that contains a query.

### One Pairing Waits For A Later Chapter

A shortest path search also takes the smallest entry from a queue. Its correctness depends on relaxing edges and on discarding an entry when a shorter distance is already known. That stale-entry rule needs the graph model and the relaxation step, which Chapter 24 teaches. Chapter 24 owns the problems of that pairing, and this chapter assigns none of them.
