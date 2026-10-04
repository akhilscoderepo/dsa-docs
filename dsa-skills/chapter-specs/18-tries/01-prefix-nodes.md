# Lesson spec: Prefix Nodes

**Recognition cue.** Many stored strings share prefixes and queries repeatedly ask whether a prefix exists. **Invariant.** The path from the root spells exactly one prefix; terminal state is separate from path existence. **False friend.** A hash set answers whole-word membership but cannot directly represent all prefixes.

- **Build - Author exercise: Store Shared Prefixes.** Insert `car` and `cat` and identify which nodes are shared.
- **Vary - Author exercise: Prefix Count.** Maintain how many inserted words pass through each node.
- **Boundary - Author exercise: Empty Word And Prefix-Only Node.** Distinguish the root terminal flag from a node that merely has children.
- **Recognize - LC 208 Implement Trie.** Support exact word and prefix queries from the same paths.
