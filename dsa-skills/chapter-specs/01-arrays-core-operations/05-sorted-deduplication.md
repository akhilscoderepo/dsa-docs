# Lesson spec: Sorted Deduplication

**Recognition cue.** Equal values occur in adjacent runs because the input is sorted. **Invariant.** The written prefix contains one representative of every completed value run. **False friend.** This is not general duplicate removal from unsorted data; sorting or a set would be a different prerequisite.

- **Build — LC 26 Remove Duplicates from Sorted Array.** `[1,1,2] → k=2, [1,2]`; `[] → k=0`.
- **Vary — LC 80 Remove Duplicates from Sorted Array II.** Permit two representatives, so the admission check reads `nums[write-2]`.
- **Boundary — Author exercise: Keep One Per Run.** Verify all-equal `[5,5,5] → k=1` and already-unique `[1,2,3] → k=3`.
- **Recognize — LC 443 String Compression.** The representation changes to `char[]`, but each completed run still owns one write decision.
