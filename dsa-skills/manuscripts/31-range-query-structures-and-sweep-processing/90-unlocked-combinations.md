<!-- section: unlocked-combinations -->
## Unlocked Combinations

A booking system stores meeting times as seconds since 1970, which are numbers near 1.7 * 10^9. An array indexed by those seconds needs gigabytes, yet only a few thousand distinct times ever appear. A server also needs the busiest minute of the day after every new booking. The first pairing below solves the busiest-minute problem, the second solves the timestamp problem, and two more pairings wait for a later chapter.

### Pairings Taught In This Chapter

The lesson Sweep And Ordered State joins the sweep from lesson 05 with an ordered map, so the state between two event coordinates stays exact while events arrive. The sort fixes the order of changes, and the ordered structure answers questions such as the largest active height or the count of active bookings. Its four exercises find the first overloaded stop, the tallest skyline stretch, the order of events that share one coordinate and the busiest moment after every booking.

The lesson Compress Values Then Count Ranks joins coordinate compression with the Fenwick tree. Compression keeps the order of the values and shrinks the index range to the number of distinct values. The Fenwick tree then counts or sums how many compressed values lie below a rank. Its four exercises build the rank mapping, answer sums over sparse keys, handle negative and extreme values and compute an insertion cost.

### Pairings That Wait For A Later Chapter

Persistent trees keep every earlier version of a tree, and multidimensional range structures answer queries over several coordinates at once. Each needs an explicit rule for which version or which dimensions a query reads. A later chapter takes them over, so this chapter assigns no problems to them.
