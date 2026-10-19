# Lesson spec: Answer Prefix Queries With A Trie

**Recognition cue.** The API repeatedly inserts words and answers prefix, suffix, wildcard, stream, or encoded queries. **Invariant.** Trie/index state represents every currently searchable key and its required aggregate/rank metadata.

- **Build - LC 677 Map Sum Pairs.** Maintain prefix aggregates under key overwrite.
- **Vary - LC 676 Implement Magic Dictionary.** Search with exactly one substituted character.
- **Boundary - LC 1804 Implement Trie II.** Keep prefix and terminal counts correct through erase.
- **Recognize - LC 642 Design Search Autocomplete System.** Combine prefix lookup with frequency ranking and lexicographic ties.
