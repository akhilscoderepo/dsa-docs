# Lesson spec: Fixed Alphabet Counts

**Recognition cue.** The character set is explicitly small, such as lowercase English letters. **State.** `count[c - 'a']` is the processed count. **False friend.** General characters or words require Chapter 04 maps.

- **Build - Author exercise: Vowel Counts.** Count lowercase vowels in `s`.
- **Vary - LC 389 Find the Difference.** Increment characters from one string and decrement from the other.
- **Boundary - Author exercise: Invalid Alphabet.** Reject or document any character outside the declared alphabet.
- **Recognize - LC 383 Ransom Note.** Count the available lowercase letters in `magazine`, consume them while scanning `ransomNote`, and fail as soon as a required count becomes negative.
