# Lesson spec: Direct Scans

**Recognition cue.** The input is unsorted, every element may matter, and the answer is determined by inspecting one element at a time. **State.** The loop index marks the next unexamined position; the answer records the result required by the contract. **False friend.** Do not sort just to make search look easier: sorting changes index semantics and costs more than one scan.

- **Build — Author exercise: First Match.** Given an integer array `nums` and integer `target`, return the first index containing `target`, or `-1` when it does not occur. `[7, 4, 7], 7 → 0`; `[], 3 → -1`. Hint: ask what reaching the end proves.
- **Vary — Author exercise: Last Match.** Keep scanning after a match and return the last matching index. `[7, 4, 7], 7 → 2`; `[1], 9 → -1`. The changed decision is whether a match permits early return.
- **Boundary — Author exercise: Target Absent.** Given an unsorted array and a target that may not occur, return `-1` after a complete scan. `[3,2,2,3], 5 → -1`; `[], 3 → -1`.
- **Recognize — LC 1920 Build Array from Permutation.** Given a valid permutation `nums`, return `ans[i] = nums[nums[i]]`. The direct indexed-read contract, not a search, selects the method.
