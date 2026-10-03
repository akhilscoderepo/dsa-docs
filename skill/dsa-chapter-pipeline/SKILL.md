---
name: "dsa-chapter-pipeline"
description: "Write, audit and build one chapter of the Java DSA curriculum (any of chapters 00-41) into a verified, self-contained interactive HTML file, one lesson per run."
---

# DSA chapter pipeline (one skill, any topic)

Markdown manuscripts are the single source of truth. Scripts do everything mechanical. The model spends tokens only on judgment: explanation, insight, examples, exercises, hints, solution reasoning.

Input: a chapter number NN and slug (e.g. `09-sliding-window`), plus optionally one lesson id. Output: audited manuscripts, validated Java, one HTML file per chapter. Status vocabulary is exact: `Content complete, human review pending` until the user's own `review-log.md` exists. Never claim more.

## 0. Load only this per run (never the whole chapter)
1. `chapter-specs/NN-slug/chapter-map.md`
2. The one lesson spec being written
3. Summaries (not full text) of prerequisite lessons
4. Exercise/lesson schema (section 3 below)
5. One gold exemplar lesson (`references/exemplar/`); the finished chapter 09 lives in `fixtures/` as a regression test, not as prompt context

If a spec slice is missing, write a short one from the curriculum map first and get it confirmed. Do not invent scope.

## 1. Layout
```
chapter-specs/NN-slug/ chapter-map.md, 01-*.md ... 9x-*.md (combination)
manuscripts/NN-slug/   00-orientation.md, 01-*.md ..., 90-unlocked-combinations.md,
                       9x-*.md, 95-review.md, solutions/NN-*.md, ids.lock, review-log.md (human only)
```

## 2. Per-lesson loop (one lesson per run)
1. Scaffold with the script (markers, ids, empty stages). Do not hand-type structure.
2. Write the stages in order, judgment content only.
3. Generate traces from the family trace generator where one exists; otherwise write the trace JSON and let a script verify it.
4. Write solutions with `java run` blocks that assert every behavior claim (claim ledger: no prose claim about behavior without an assertion). Cross-check against a brute-force oracle and randomized tests.
5. Run the manuscript audit. Fix errors; justify or fix warnings.
6. Compile and run Java, write the stamp.
7. Only after the lesson passes, move to the next. Do not batch lessons.

## 3. Schema
Lesson markers: `lesson-kind: standard|combination`, `lesson-id`, stages in order: context, [contributions for combination], naive, bottleneck, insight, variables, trace, code, applicability, exercises.

Quality bar per stage: naive shows a real working brute force and its cost; bottleneck names the repeated work; insight states the invariant in one sentence; variables explain what each piece of state means and when it changes; trace is step-through with state; code carries the invariant in comments only where non-obvious; applicability includes at least one false friend (looks like this pattern, is not) and a no-go condition. Every technique states complexity and the exact conditions under which a shortcut is valid (e.g. monotone validity, objective type).

Exercise: `#### [Role] Title (LeetCode N | Author exercise)` then `<!-- id: slug -->`, fields: Prerequisites, Problem, Constraints, Example 1, Example 2, Hint, Changed decision. Roles ladder: Build, Vary, Boundary, Recognize, then optional Extend/Medium/Hard/Challenge. Solution record shares the id: Approach, Complexity, ```java run block with assertions. Reworded examples must differ from the LeetCode originals and be recomputed by code. Deliberate revisits of the same problem are allowed only when the contract or invariant differs.

Trace blocks: ```trace JSON (array pointers), several per lesson allowed, varied inputs (audit warns on low diversity). Quiz blocks: ```quiz JSON with permanent `id` per question (`qz.<id>`).

Ids: hidden comment ids are canonical; builder may accept `{#id}`. `ids.lock` records every id; removing one requires a retired entry.

## 4. Java validation
JDK 25 with `--release 21` for DSA; footer reports both accurately and derives from the stamp, never hard-coded. Scratch dir is a UUID-named directory made with plain mkdir (no `tempfile.mkdtemp`, Windows-safe). The stamp stores JDK info, and a SHA-256 digest over every validated block, its flags (`run`) and its source manuscript/solution identity. The builder recomputes the digest and fails on a stale stamp. If the sandbox lacks JDK 25, say what was actually used.

## 5. HTML build
One self-contained HTML per chapter, plus one generated curriculum index. Never one course-wide file.
- Storage key auto-derived: `dsa:chapter-NN`. Manual override only for migrations.
- Backup envelope `{schema:2, chapterKey, data}`. Strict import: reject other chapter, missing or unsupported schema, malformed JSON. Confirm before replacing existing notes.
- Search index built at build time from visible text only. Exclude hints, collapsed solutions, quiz explanations, notes. The audit fails if a solution token is findable by search.
- Phone: tap targets at least 36px (checkboxes 28px), no horizontal overflow.
- Browser checks use real Chromium; discover Chrome, Edge, Playwright Chromium or `CHROMIUM_PATH` automatically (Windows included). Must pass desktop, phone, dark mode, persistence and overflow.

## 6. Gates (all must pass before delivery)
manuscript audit 0 errors; Java compile and run; stamp fresh; HTML audit 0 errors; smoke test; render test. Warnings listed honestly. Human review gate stays open: the AI never writes `review-log.md`.

## 7. Token discipline
- Use scaffold, trace generators, oracles and randomized harnesses before writing prose by hand.
- Write each section once; fix by targeted edit, not rewrite.
- Do not re-read finished lessons; use their summaries.
- Do not rewrite a complete chapter for polish. Fix only audit warnings and issues the user flags while reading.

## 8. Never
- Claim verification you did not run (other JDKs, Windows, real phones, printing, teaching quality).
- Hide or soften a failing gate.
- Copy LeetCode statements or solutions verbatim.
- Generate several chapters, or the whole curriculum, in one run.

## 9. Delivery
Send the HTML, plus the manuscripts zip when asked. Reply with: what passed, remaining warnings, what is unverified, and that human review is pending. Name the next lesson to run.