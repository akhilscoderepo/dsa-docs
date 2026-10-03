# DSA curriculum acceptance gates

Each gate says how it is checked. "Script" means the named check code appears in the output of `audit_manuscripts.py` (M) or `audit_html.py` (H). "Review" means a person or the auditor reads the text.

## Canonical inventory

- Every chapter number has exactly one spec, one manuscript directory and one HTML file. Review, plus M `spec-lesson-missing`, H manuscript parity.
- No orphaned or legacy artifacts in the reader package. Review.

## Lesson structure and substance

- All stages present, in order: M `stage-missing`, `stage-order`.
- No stage is a stub: M `stage-thin`.
- Explanations are prose, not bullet lists or tables: M `bullet-heavy`, `trace-table`.
- The bottleneck states a Big-O cost: M `no-complexity`. Whether the waste is visible in a concrete run: review.
- The insight names its vocabulary once, and the names are absent from context and naive: M `no-names`, `name-not-introduced`, `jargon-early`.
- Applicability states the invariant and a false friend: M `no-invariant`, `no-false-friend`.
- Trace data is valid and matches the code: M `bad-trace` for validity; accuracy by review.
- Headings are short and descriptive: M `heading-style`.

## Practice quality

- 4 to 7 exercises with Build, Vary, Boundary, Recognize in order: M `ladder-gap`, `ladder-short`, `ladder-long`, `role-order`, `bad-role`.
- Every exercise has prerequisites, problem, constraints, two examples with input and output, hint and changed decision: M `field-missing`, `field-thin`, `example-shape`, `no-source`.
- Every exercise has a solution with approach, complexity and Java: M `no-solutions`, `solution-missing`, `solution-field`, `solution-code`.
- Every spec exercise appears in the manuscript: M `spec-exercise-missing`.
- No exercise needs an untaught technique, and difficulty rises by one dimension: review.

## Identity and human review

- Every lesson and exercise has an explicit permanent id; ids are unique and well formed; released ids are never removed or renamed: M `lesson-id-missing`, `exercise-id-missing`, `id-format`, `id-duplicate`, `id-removed` (via `ids.lock`).
- A person has judged each lesson and recorded it in `review-log.md`: M `no-human-review`, `review-log-format`, `review-missing`, `review-revise`. The AI never writes this file.

## Duplication and filler

- No paragraph repeated, no sentence repeated three times, no identical Java block across lessons: M `duplicate-paragraph`, `repeated-sentence`, `duplicate-code`.
- No stock filler phrases: M `filler`.

## Java correctness

- Every Java block compiles; `java run` blocks execute with assertions: M `java`. If no JDK: M `java-not-validated` and the report says NOT VALIDATED.
- Input assumptions match the problem contract, numeric types hold all valid values, equality and hashing are correct, library calls do not invalidate the stated complexity, and mutation order preserves the invariant. Review.

## HTML artifact

- One self-contained file; no external requests: H external resource errors.
- Notes box, status selector and solution block per exercise; chapter notes box: H element-count errors.
- Trace and quiz JSON valid; JS parses: H JSON and syntax errors.
- Exercise count in HTML equals the manuscript: H parity.
- Interactions work (notes persist, progress, steppers, quiz, search, export, reset): H `--smoke`.
- Desktop and phone layout in real Chromium (no horizontal scroll, text size, tap targets, persistence across reload, dark-mode contrast): `render_check.mjs`. Print and reading comfort: review.
- The footer and the verified badges match the Java validation stamp: H footer check.

## Reader package

- A reading-order index explains prerequisites and optional advanced chapters.
- A manifest lists canonical files with exercise counts.
- The archive opens and its file count matches the manifest.
