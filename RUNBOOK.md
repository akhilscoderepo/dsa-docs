# Runbook for scheduled generation sessions

Goal: build chapters 05 to 41 of the Java DSA curriculum, one chapter at a time, with every gate passing, pushing each chapter to this repo the moment it is done. Chapters 00 to 04 are finished and are the quality exemplars (read ONE lesson from `dsa-skills/manuscripts/03-strings/` and its solutions file as the style model; do not read whole chapters).

Pipeline law: `skill/dsa-chapter-pipeline/SKILL.md`. Status vocabulary is exactly "content complete, human review pending". Never write `review-log.md`. Never claim verification that was not run (JDK 25, Windows, phones, printing, teaching quality are unverified).

## Quality and token policy (set by the user)
- Do NOT shorten the teaching stages (context, naive, bottleneck, insight, trace, applicability). Writing quality is the product.
- Allowed savings only: no restating code in prose, no repeated boilerplate, targeted fixes instead of rewrites, audit only the lesson in hand until the chapter is complete.
- Quick turnaround: finish and push each chapter as soon as it passes; do not batch.

## Writing rules (set by the user, Oct 4). Rules contain principles only; never copy a sample from anywhere in this file as the fix.
### Sentence voice
- One idea per sentence, about 25 words at most. Split a sentence that carries several abstract actions into short sentences or concrete cases.
- Active voice with a concrete subject. Present tense only. No arrows in prose; use connecting words that state the logical relation.
- Turn noun phrases into verbs. Name the real variable, call, index range or data structure instead of a vague filler noun.
- This changes wording only. Keep all stages, content depth and the format rules below.
- No colloquial analogies and no invented definitions. Explain with standard computer science definitions (index relationships, complexity classes, memory footprints, preconditions and postconditions). A concrete scenario is allowed only when it is a real software case, never a metaphor for the algorithm.
- Run `python3 scripts/voice_lint.py NN` (advisory) and fix flagged sentences with targeted edits.

### Plain wording with one anchor term
Write headings and prose the way an experienced engineer explains the topic aloud. Use ordinary words, and add a technical term only where it names something a reader can look up.
- **Searchable test:** use a technical phrase only if it appears in a textbook, the language documentation or a standard interview guide with one clear meaning. Otherwise say it in plain words.
- **One anchor per heading:** a heading carries at most one established technical term. Every other word is ordinary.
- **No stacked abstractions:** never place two abstract nouns side by side, and never join a list of technical nouns in one title.
- **No coined phrases:** never build a technical-sounding phrase by joining two real words. If no established term exists, use plain words.
- **Concrete verb and object:** headings prefer a verb with a concrete object over a noun phrase.
- **Define once:** define each term in plain words the first time it appears in a lesson, then use it consistently without synonyms.
- **Scope:** lesson titles, stage headings, sub-headings, prose, hints, exercise text and code comments.
- **Check:** read every heading aloud. If it sounds like an index entry and not like something a person would say, rewrite it.

### Reader flow (set by the user, Oct 4). The goal is that a first-time reader reaches flow state.
- **Hook first:** every chapter orientation and every lesson opens with a concrete problem or failure the reader recognizes, then states the question the section answers. Never open by announcing what the text does not cover. Keep everything before the first lesson short.
- **Predict, then reveal:** after the simple approach, add a `predict` block (a fenced block whose first paragraph is the question and whose remaining text is the answer). The reader commits to a guess before the explanation. The builder hides the answer.
- **Internal consistency:** every count in prose equals the length of the list it introduces. Every back-reference ("earlier", "the previous lesson", "above") points to something that exists at that spot. Prose may refer to a widget or table only after it appears or with an explicit "below". A term has one name across the prose, code identifiers and comments; when a defined term and a code identifier differ, rename the identifier or say once that they mean the same thing.
- **Natural required wording:** the audit requires certain words, so place them inside sentences that explain the idea in plain language. A required word never becomes a standalone label sentence.
- **Orientation inside a lesson:** the builder shows a part label on every stage and a clickable list of the lesson's parts. Write each stage so it makes sense under its label.
- **Exercises scan easily:** the problem specification is short and states one task. Input Constraints with several facts are a short list of limits, one fact per line. Anything about the method's own cost belongs in the solution, not the constraints.
- **Learner text only:** never mention the build, the audit, the stamp, lint, assertions run during build, or any pipeline step. Describe the topic.
- **One self-check per lesson in plain language,** shown by the builder at the end.
- The audit warns on a missing `predict` block, a count that does not match its list, tooling words in learner text, and an exercise Constraints paragraph of more than four sentences. Resolve each warning by editing the text, not by silencing the check.

### Heading hierarchy
Levels are fixed and never skipped:
- Page title (H1) comes from the builder. Never write `# ` in a manuscript.
- `## Lesson Title` (H2) equals the spec lesson heading. One per lesson file. The audit allows at most 7 words (a hyphenated word counts as one), no colon, no period.
- `### Stage heading` (H3). One per stage. It states what the stage teaches.
- `#### Sub-heading` (H4). Split any stage longer than about 200 words into 2 to 4 parts, each with its own H4. Exercises keep `#### [Role] Title`; never put a plain `####` inside the exercises stage, because the builder treats `#### [` as an exercise start.
- H3 and H4 follow the plain-wording rule, at most 7 words, no colon, no period, parallel form among siblings. Headings state the concept, data-structure state, memory condition or analysis method under study, never a story or metaphor.
- When a lesson is retitled, edit the same heading in the working spec files first (`dsa-skills/chapter-specs/NN-slug.md` and the slice `NN-slug/MM-*.md`), then the manuscript. `lesson-id`, file names and exercise ids never change. Chapter titles passed to `build.sh` and orientation and review headings follow the same rules.
- `voice_lint.py` cannot detect metaphors or coined phrases; check headings yourself before you build.

### Exercise and solution presentation
Machine keys stay fixed (the audit parses them): `#### [Build|Vary|Boundary|Recognize] Title`, `<!-- id: -->`, bold field labels `Problem`, `Constraints`, `Example 1/2`, `Hint`, `Changed decision`, `Prerequisites`, and `#### Solution:` records with `Approach` and `Complexity`. The builder shows display names: roles Basic / Variation / Edge Cases / Pattern Recognition, `Problem` as "Problem Specification", `Constraints` as "Input Constraints", and the solution toggle as "Algorithmic Solution". Do not invent other names.
- **Problem Specification:** a formal textbook specification that defines the input, the output and every term used. No story filler, slang or metaphors.
- **Input Constraints:** precise value ranges, lengths including empty input, integer types, ties, return convention and mutation rules.
- **Approach:** the algorithm, its invariant and why each step exists. **Complexity:** a Time bullet and a Space bullet, each with its reason.
- **Java in solutions:** Javadoc on each solution method with purpose, Time, Space and the invariant. A comment on every primary statement (loop header, condition, update, return) explaining the execution logic, why it runs and where cost or memory comes from. Comments only describe and never change executable code. The test harness gets one comment per group of assertions.

### Bullets versus paragraphs
Bullets are reserved for multi-item parameter lists, technical entity definitions and complexity or other metrics. Sequential narrative logic is never bulleted.
- **Prose for sequences:** every approach overview, strategy breakdown, step-by-step explanation, trace commentary and reasoning chain is written as cohesive, flowing paragraphs. Weave the separate logical steps and programmatic actions into one structural story with clear transition markers that state how each step follows from the last.
- **No checklist drops:** never collapse an explanation into a vertical list of isolated single-sentence fragments. A list of fragments reads like a design to-do list and destroys narrative continuity.
- **Where bullets belong:** parameter lists with several items, definitions of technical entities, and metric summaries such as time and space cost.
- **Bullet shape:** every bullet starts with a **bolded key technical entity**, then a short active-voice fragment that states its exact meaning or constraint. One fact per bullet, parallel form within a list.
- **Audit limits:** context, naive, bottleneck and insight obey the audit limit of 30% bullet lines. Trace and applicability keep their allowance for entity or metric lists, but their explanatory sequences stay prose.
- **Solution Approach:** a prose paragraph (or a few) that explains the algorithm, its invariant and why each step exists. Complexity stays a Time bullet and a Space bullet, each with its reason.

## Session start
1. `git pull --rebase origin main`; read `PROGRESS.md`. Pick the lowest chapter number that is neither `done` nor claimed within the last 6 hours. Claim it: add a line to PROGRESS.md (`claimed NN <UTC time>`), commit, push.
2. Tooling: `cd dsa-skills && [ -d node_modules ] || npm ci`. JDK 21 and Python 3 must exist (`java -version`). Chromium is at `/opt/pw-browsers` (do not run playwright install).
3. Spec slices: `python3 dsa-skills/experience-first-dsa-teaching/scripts/split_spec.py inputs/chapter-specs/NN-slug.md dsa-skills/chapter-specs/NN-slug` and `cp inputs/chapter-specs/NN-slug.md dsa-skills/chapter-specs/`. Read `chapter-map.md` and ONE lesson slice at a time. If the spec lists a released combination (Teach now row), write a combination lesson for it.

## Per-lesson loop (one lesson at a time)
1. Write `dsa-skills/manuscripts/NN-slug/0K-lesson.md` and `solutions/0K-lesson.md` in one go. Put `@@TRACE1@@` and `@@TRACE2@@` placeholders in the trace stage.
2. Fill traces with a script modelled on `scripts/tracegen/*.py` (simulate the algorithm, assert the final answer, replace the placeholders). Never hand-write trace JSON.
3. `scripts/aud.sh NN` and read only lines with ERROR or "run failed". Fix by targeted edit.
4. When all lessons exist, also write `00-orientation.md`, `90-unlocked-combinations.md`, `95-review.md`, then `scripts/build.sh NN "Chapter Title"`. The only acceptable remaining error is `no-human-review`.
5. After EVERY lesson (not only at chapter end), commit and push the work in progress (`git pull --rebase origin main` first; on a PROGRESS.md conflict keep both sides' lines). A session can be cut off by its token budget at any moment, and unpushed work is lost. When you start a claimed or stale chapter that already has lesson files in `dsa-skills/manuscripts/NN-*`, continue from the first missing lesson instead of rewriting.
6. When the chapter is complete, commit and push the chapter (manuscripts, `output/NN-*.html`, ids.lock), update PROGRESS.md to `done`, and print the output path. Then start the next chapter.

Overlap note: scheduled runs can overlap. Claims in PROGRESS.md keep two sessions on different chapters; never work on a chapter claimed within the last 6 hours by another session.

## Format rules learned the hard way (these cause most rework)
- Every `##` and `###` heading: at most 7 words, no colon, no period. The `## Title` must equal the spec lesson heading.
- File markers: `<!-- lesson-kind: standard|combination -->`, `<!-- lesson-id: slug -->`; stages in order `context, [contributions for combination], naive, bottleneck, insight, variables, trace, code, applicability, exercises`, each as `<!-- stage: x -->`.
- Minimum prose words: context 60, naive 30, bottleneck 60 (must contain `O(`), insight 120 (must have `<!-- names: a, b, c -->`; each name appears in the insight prose and NOT in context or naive), variables 40, trace 100, code 30, applicability 80 (must contain the word "invariant" and "false friend"), contributions 60. Naive and code stages need a ```java block. Narrative stages at most 30% bullet lines.
- Trace block: ```trace JSON `{"cells":[...],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{},"note":""}]}`; at least 3 steps; pointer values are ints from -1 to len(cells).
- Exercise: `#### [Role] Title (LeetCode N | Author exercise)`, then `<!-- id: hm-slug -->`, then bold fields Prerequisites, Problem, Constraints, Example 1, Example 2, Hint, Changed decision. Roles: Build, Vary, Boundary, Recognize. Use a chapter-specific id prefix.
- Solutions file: `<!-- solutions-for: NN-slug -->`, then `#### Solution: [Role] Title (...)` with the same id, **Approach.**, **Complexity.**, and a ```java run block with a main class that throws AssertionError, checked against a brute-force oracle on random inputs. Every prose claim about Java behaviour needs an assertion.
- Code-stage ```java blocks without a class must be methods only; if they contain `record` or other types, wrap everything in `final class X { ... }`.
- Cross-file checks: the same sentence or 8-word sequence in 4 or more files is an error. Vary the wording of complexity sentences, Constraints lines, applicability openers, and orientation, review and unlocked-combination text per chapter. Never repeat identical Java blocks.
- LeetCode problems reused from earlier chapters must change the contract or the invariant, with different examples and different code.
- Review quizzes: ```quiz JSON with permanent `id`, `q`, `options`, `answer` (zero-based index), `explain`. About one per lesson.
- Examples are recomputed by code, never copied from LeetCode statements.

## Finishing
When PROGRESS.md shows chapters 05 to 41 all `done`: run the full-corpus audit (`python3 dsa-skills/dsa-curriculum-auditor/scripts/audit_manuscripts.py dsa-skills/manuscripts --spec dsa-skills/chapter-specs`), fix everything except `no-human-review`, rebuild the index with `python3 dsa-skills/markdown-textbook-html/scripts/build_index.py dsa-skills/manuscripts output --title "Java DSA Curriculum"`, push, and disable the scheduled task (update_trigger with enabled=false).
Final report: what passed, remaining warnings, what is unverified, human review pending.
