# Lesson spec: Match Many Patterns In One Pass

**Recognition cue.** Many patterns must be matched simultaneously against one text or stream. **Invariant.** Trie transitions consume characters; failure links move to the longest suffix that is also a stored prefix, and output links report terminal matches.

- **Build - Author exercise: Trie Failure Links.** Build fallback state level by level.
- **Vary - Author exercise: Multi-Pattern Scan.** Follow transitions and report all terminal outputs.
- **Boundary - Author exercise: Suffix Pattern Matches.** Preserve outputs inherited through failure links.
- **Recognize - LC 1032 Stream of Characters.** Maintain automaton state across successive query calls.
