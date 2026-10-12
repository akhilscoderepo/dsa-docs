# Lesson spec: Take Or Skip

**Recognition cue.** At each position, choosing it forbids a nearby choice. **Invariant.** `dp[i]` is the best answer for a stated prefix; transition compares skipping with taking plus the last compatible state.

- **Build - Author exercise: Nonadjacent Sum.** Write `max(skip, take)` explicitly.
- **Vary - LC 198 House Robber.** Apply the recurrence to money values.
- **Boundary - Author exercise: All Zero And Singleton.** Preserve the empty-choice contract.
- **Recognize - LC 213 House Robber II.** Split the cycle into two legal linear cases.
