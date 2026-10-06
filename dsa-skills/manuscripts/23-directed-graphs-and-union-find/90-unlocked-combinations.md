<!-- section: unlocked-combinations -->
## Unlocked Combinations

A network tool receives link reports one at a time and must say after each report how many separate clusters remain. A fresh traversal per report costs O(V + E) each time. The fix stores each cluster under one representative and merges two representatives per report. This chapter releases that pairing in full and leaves one pairing for the next chapter.

### Pairing Taught In This Chapter

Graph edges say which elements belong together, and the union-find structure keeps one representative per group. The lesson Merge Groups As Edges Arrive joins them. The edge list supplies merge events, and the parent and size arrays supply group identity. The lesson adds one idea: an edge whose endpoints already share a root changes nothing, and that observation answers cycle, count and spanning-tree questions.

### Pairing That Waits For A Later Chapter

A group representative stores no route cost, so it cannot answer weighted shortest-path questions. Chapter 24 teaches distance relaxation for that case, and this chapter assigns no exercises for it.
