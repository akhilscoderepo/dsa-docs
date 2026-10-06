# Lesson spec: Decode Nested Repeat Groups

**Recognition cue.** A repetition count applies to a bracketed substring that may itself contain encoded groups. **Invariant.** On `[`, save the parent string state and repeat count; on `]`, resolve the current group into its parent. **False friend.** Repeating immediately at each digit fails for multi-digit counts and nesting.

- **Build - Author exercise: Decode One Flat Group.** Decode a single form such as `3[ab]`.
- **Vary - Author exercise: Multi-Digit Repeat Count.** Accumulate `count = count * 10 + digit`.
- **Boundary - Author exercise: Adjacent And Nested Groups.** Decode an input such as `2[a]3[b2[c]]` without mixing frames.
- **Recognize - LC 394 Decode String.** Implement the complete nested grammar using saved counts and parent builders.
