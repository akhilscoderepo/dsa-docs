---
name: markdown-textbook-html
description: Build self-contained interactive HTML textbook chapters from Markdown manuscripts. Produces one offline file per chapter with expandable hints, hidden solutions, per-exercise notes boxes, status and progress tracking, step-through traces, quizzes, chapter search, and notes export and import. Use when a chapter's manuscripts are ready to publish or preview, or when asked for an interactive or HTML version of the study material. Not for writing the lessons themselves and not for form-filling PDFs.
---

# Markdown to interactive HTML textbook

The Markdown manuscripts are the single source of truth. This skill turns a chapter directory into one HTML file with the CSS and JavaScript inlined, so it opens by double-click, works offline and on a phone, and makes no network requests. Fix content in the Markdown and rebuild; never hand-edit the HTML.

## Setup

```
pip install -r requirements.txt   # pinned: markdown-it-py==4.0.0
```

The shared look and behavior live in `assets/textbook.css` and `assets/textbook.js`. They are written once and inlined into each build, so changing a style means editing one file and rebuilding.

## Build

```
python3 scripts/build_html.py manuscripts/09-sliding-window -o output/09-sliding-window.html \
        --chapter 09 --title "Sliding Window" --validation stamp.json
```

`stamp.json` is written by the auditor (`audit_manuscripts.py --stamp`). It records which JDK compiled the Java and what was run. The "verified" badges on `java run` blocks and the footer text come from that file, so a page cannot claim more than was executed. Without `--validation` the footer says the Java was not machine-validated.

Before building, audit the manuscripts without `--draft`. After building, run `audit_html.py` with `--manuscripts` and `--smoke`, then `render_check.mjs` in a real Chromium for desktop and phone layout. A person should still open one file and read it for comfort; the scripts cannot judge that.

## What the learner gets

- Contents sidebar with lesson completion ticks, search across the chapter, light/dark/auto theme, and a print stylesheet (browser Print then Save as PDF gives a clean linear copy).
- Per exercise: role and source badges, a status selector (Not started, Attempted, Solved, Needs review), a collapsed hint, a notes box that autosaves, and a collapsed solution to open after trying.
- Per lesson: a rebuild-check box. Progress bar at the top counts solved exercises and completed lessons.
- Trace stepper for `trace` blocks (arrays with pointers, or multi-actor schedules with a predict-then-reveal question) and quizzes for `quiz` blocks, with immediate explanations. Formats are in `experience-first-dsa-teaching/references/lesson-architecture.md`.
- Chapter-end My Notes: a large notes box plus Export notes (.md), Copy notes, Backup (.json), Import backup, and Reset.

## Where notes live

Notes, statuses, progress and quiz answers are stored in the browser's `localStorage`, keyed by the chapter number (`dsa:chapter-09`), so retitling a chapter does not orphan them. They are private to that browser and that file location. Moving to another browser, another computer, or a different folder or URL starts with an empty state, and clearing site data erases them. Backups carry a schema version and the chapter key; importing a file from another chapter or an unknown version is refused instead of overwriting the page. Tell the learner to export a backup (.json) regularly and import it on the new device. If the page is hosted somewhere that blocks downloads or storage, "Copy notes" still works and a banner explains the storage problem.

## Rules

- Manuscripts must pass the auditor first. The builder skips files with no `lesson-kind` or `section` marker and warns.
- Do not add external fonts, scripts, images or stylesheets. The HTML auditor fails the file if it finds any.
- Lesson and exercise ids are the explicit `<!-- lesson-id: -->` and `<!-- id: -->` markers, not the titles. Titles may be edited freely; an id must never change, because notes, status and progress are stored under it. Quiz questions take an optional `id` for the same reason.
- To adapt the look, edit `assets/textbook.css`; to add behavior, edit `assets/textbook.js` and rerun the smoke test.
