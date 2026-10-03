# Lesson spec: Frequency Arrays

**Recognition cue.** Values lie in a small, explicitly stated integer domain. **State.** `count[v]` is the number of processed occurrences of `v`. **False friend.** Do not allocate an array indexed by arbitrary IDs; Chapter 04 owns general hash maps.

- **Build — Author exercise: Digit Counts.** Given digits `0..9`, return ten counts. `[2,0,2] → [1,0,2,0,0,0,0,0,0,0]`; `[] → ten zeroes`.
- **Vary — LC 1365 How Many Numbers Are Smaller Than the Current Number.** Turn counts into accumulated smaller-value totals.
- **Boundary — Author exercise: Dice Validation.** Reject a value outside `1..6` before indexing; test `[1,6,0]`.
- **Recognize — LC 1051 Height Checker.** A compact known range makes counting sort preferable to comparison sorting.
