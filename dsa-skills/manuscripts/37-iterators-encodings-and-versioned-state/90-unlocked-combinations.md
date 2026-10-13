<!-- section: unlocked-combinations -->
## Unlocked Combinations

A text editor shows a folded outline of nested items. The user pages forward and back, and the editor saves the outline to disk. Paging needs an iterator that holds its place inside nested lists. Saving needs a codec whose decoder rebuilds the same shape. The two lessons that close this chapter pair those techniques.

These two lessons combine techniques from lessons 1 to 6 of this chapter.

### Pairings Taught In This Chapter

| Combination | Representative problem |
| --- | --- |
| Iterator + Traversal State | LeetCode 1586 Binary Search Tree Iterator II |
| Codec + Structural Traversal | LeetCode 297 Serialize and Deserialize Binary Tree |

The lesson Iterator Traversal State keeps a stack of unfinished positions valid across any order of `peek`, `next` and `prev` calls. The lesson Codec Structural Traversal gives encoding and decoding one shared grammar, so the decoder consumes exactly the tokens that the encoder wrote.
