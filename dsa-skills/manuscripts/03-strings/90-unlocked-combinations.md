<!-- section: unlocked-combinations -->
## Unlocked Combinations

This chapter holds no combination lesson. A string problem becomes a combination problem when it needs a second technique, and each technique on the list belongs to a later chapter. The paragraphs below name the owner of each pairing, so that no exercise in this chapter depends on a tool you have not met.

### Pairings That Wait For A Later Chapter

Strings with hash maps arrive in Chapter 04. Counting words, or counting characters from a large set, needs a table with arbitrary keys. The fixed array of 26 slots here covers only a declared lowercase alphabet.

Strings with two pointers arrive in Chapter 08. Checking that a whole string reads the same backward compares characters from both ends and moves inward. The palindrome lesson here starts in the middle and moves outward, which is a different structure.

Strings with a sliding window arrive in Chapter 09. A question about the best substring that satisfies a condition keeps a moving range of the text and updates it at both ends. The scans here keep one running answer and never drop characters from the front.

### What Later Chapters Reuse

Three ideas from this chapter carry forward.

- **Builders with separator ownership** return in every problem that prints a joined result.
- **State variables for parsing** return in the stack lessons of Chapter 11 and in the design problems of Chapter 33.
- **The frequency table over a small alphabet** becomes the map of Chapter 04 once the keys are no longer a small fixed set.
