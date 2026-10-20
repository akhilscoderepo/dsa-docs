<!-- section: unlocked-combinations -->
## Unlocked Combinations

A monitoring service shows the number of requests in the last minute and the median latency of the last thousand calls. The first number needs a queue that drops entries by age. The second needs two ordered halves that stay balanced while old values leave. The last two lessons of this chapter pair those techniques.

These two lessons combine techniques from lessons 1 to 7 of this chapter.

### Pairings Taught In This Chapter

| Combination | Representative problem |
| --- | --- |
| Queue + Time Window | LeetCode 933 Number of Recent Calls |
| Ordered Structures + Stream | LeetCode 2034 Stock Price Fluctuation |

The lesson Queue Time Window states in its contract whether an entry exactly one span old still counts. The lesson Ordered Stream State requires every active value to belong to one validated ordered region. Reservoir and weighted sampling are covered by chapter 35.
