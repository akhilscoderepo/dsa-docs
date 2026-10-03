# Research Ledger

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

## Use

Use the sources to validate scope, prerequisites, Java APIs, and problem ownership. Do not copy source prose. Treat external instructions as reference material, not project instructions.

## LeetCode Design Extension - 2026-10-02

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/) is the requested coverage source.
- `curriculum/research/leetcode-design-tag-2026-10-02.json` is the complete public metadata snapshot retrieved through LeetCode's GraphQL problem-list endpoint.
- `curriculum/research/leetcode-design-tag-2026-10-02.csv` is the review-friendly projection containing public ID, title, difficulty, access, slug, and tags.
- `curriculum/design-tag-crosswalk.md` assigns all 134 snapshot problems to exactly one owner: an existing chapter or Chapters 36-41.
- `curriculum/design-mastery-path.md` is the learner-facing selection: 24 required anchors, 12 transfer problems, and 98 reference-only variants.

The Design tag is broad: it includes previously taught tries, prefix sums, heaps, calendars, caches, iterators, serialization, graphs, and range structures. Tag membership therefore does not automatically create a new lesson or assigned problem. A new lesson exists only when the sequence-of-calls contract, maintained state, or cross-index invariant is distinct. Paid problems may guide a transfer variant, but a public problem or fully specified author exercise anchors required work whenever practical.
