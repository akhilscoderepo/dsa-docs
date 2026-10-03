# Staircase Coverage Audit

**Audit date:** 2026-10-02  
**Scope:** Active chapter specifications 00-41.  
**Result:** **PASS: 42/42 chapter specifications satisfy the structural staircase contract.**

## What Was Checked

Each row in `Independent Micro-Patterns` must have one named lesson under `Lesson Blueprints`. Every lesson must contain concrete **Build**, **Vary**, **Boundary**, and **Recognize** exercises. Each `Teach now` row must have one non-deferred lesson under `Released Combination Lessons` with the same four roles. A role may not assign a problem that its own text calls deferred.

This is a source-plan audit. It verifies coverage, prerequisite placement, and problem progression before PDF writing. The later PDF pass must still expand each selected exercise into full wording, constraints, examples, hints, reasoning, complexity, and annotated Java.

## Aggregate Result

- Independent micro-patterns planned: **307**
- Authored standalone lesson staircases: **307**
- Teach-now combinations: **57**
- Authored combination staircases: **57**
- Required role steps: **1456**
- Authored role steps: **1456**
- Candidate-bank records: **554**
- Passing chapters: **42/42**

## Chapter Evidence

| Ch. | Topic | Patterns | Lessons | Teach now | Combo lessons | Role steps | LC refs | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 00 | Problem contracts, complexity, and sequence language | 8 | 8 | 0 | 0 | 32/32 | 0 | PASS |
| 01 | Arrays: Core operations | 10 | 10 | 0 | 0 | 40/40 | 23 | PASS |
| 02 | Matrices and 2D arrays | 7 | 7 | 0 | 0 | 28/28 | 14 | PASS |
| 03 | Strings | 7 | 7 | 0 | 0 | 28/28 | 15 | PASS |
| 04 | Hash maps and sets | 7 | 7 | 2 | 2 | 36/36 | 30 | PASS |
| 05 | Sorting and Java comparators | 8 | 8 | 1 | 1 | 36/36 | 26 | PASS |
| 06 | Binary search | 9 | 9 | 2 | 2 | 44/44 | 32 | PASS |
| 07 | Prefix sums and difference arrays | 10 | 10 | 1 | 1 | 44/44 | 32 | PASS |
| 08 | Two pointers | 7 | 7 | 3 | 3 | 40/40 | 40 | PASS |
| 09 | Sliding window | 9 | 9 | 1 | 1 | 40/40 | 24 | PASS |
| 10 | Intervals | 6 | 6 | 1 | 1 | 28/28 | 15 | PASS |
| 11 | Stacks and queues | 11 | 11 | 1 | 1 | 48/48 | 20 | PASS |
| 12 | Monotonic stacks | 7 | 7 | 1 | 1 | 32/32 | 16 | PASS |
| 13 | Deques and monotonic queues | 8 | 8 | 1 | 1 | 36/36 | 13 | PASS |
| 14 | Linked lists | 10 | 10 | 1 | 1 | 44/44 | 21 | PASS |
| 15 | Trees: DFS | 9 | 9 | 1 | 1 | 40/40 | 22 | PASS |
| 16 | Trees: BFS and BSTs | 9 | 9 | 2 | 2 | 44/44 | 31 | PASS |
| 17 | Heaps and priority queues | 7 | 7 | 1 | 1 | 32/32 | 21 | PASS |
| 18 | Tries | 5 | 5 | 1 | 1 | 24/24 | 12 | PASS |
| 19 | Recursion and backtracking | 10 | 10 | 1 | 1 | 44/44 | 18 | PASS |
| 20 | Greedy | 5 | 5 | 4 | 4 | 36/36 | 38 | PASS |
| 21 | Graph traversal: models, DFS, and ordinary BFS | 9 | 9 | 1 | 1 | 40/40 | 19 | PASS |
| 22 | BFS variations | 5 | 5 | 1 | 1 | 24/24 | 15 | PASS |
| 23 | Directed graphs and union-find | 7 | 7 | 1 | 1 | 32/32 | 17 | PASS |
| 24 | Shortest paths and graph state modeling | 6 | 6 | 2 | 2 | 32/32 | 18 | PASS |
| 25 | Advanced graph optimization | 8 | 8 | 1 | 1 | 36/36 | 15 | PASS |
| 26 | Dynamic programming: foundations | 8 | 8 | 1 | 1 | 36/36 | 22 | PASS |
| 27 | Dynamic programming: capacity and partition patterns | 7 | 7 | 1 | 1 | 32/32 | 16 | PASS |
| 28 | Dynamic programming: state machines and sequences | 6 | 6 | 1 | 1 | 28/28 | 20 | PASS |
| 29 | Dynamic programming: intervals and advanced states | 7 | 7 | 1 | 1 | 32/32 | 13 | PASS |
| 30 | Bits, number theory, and interview numerics | 10 | 10 | 1 | 1 | 44/44 | 21 | PASS |
| 31 | Range-query structures and sweep processing | 5 | 5 | 2 | 2 | 28/28 | 15 | PASS |
| 32 | Selection and ordered-data techniques | 4 | 4 | 1 | 1 | 20/20 | 14 | PASS |
| 33 | Design-data-structure problems | 6 | 6 | 3 | 3 | 36/36 | 31 | PASS |
| 34 | Advanced strings | 5 | 5 | 1 | 1 | 24/24 | 16 | PASS |
| 35 | Advanced search, sampling, and geometric state | 6 | 6 | 2 | 2 | 32/32 | 15 | PASS |
| 36 | Stateful containers and histories | 7 | 7 | 2 | 2 | 36/36 | 53 | PASS |
| 37 | Iterators, encodings, and versioned state | 6 | 6 | 2 | 2 | 32/32 | 62 | PASS |
| 38 | Streaming and temporal state | 7 | 7 | 2 | 2 | 36/36 | 57 | PASS |
| 39 | Dynamic query structures | 6 | 6 | 2 | 2 | 32/32 | 42 | PASS |
| 40 | Composite indexes and allocation | 6 | 6 | 2 | 2 | 32/32 | 54 | PASS |
| 41 | Algorithmic services and simulations | 7 | 7 | 2 | 2 | 36/36 | 69 | PASS |

## Findings

- No structural gaps remain in the 42 source specifications.

## Publication Boundary

A passing source specification is ready to drive PDF authoring; it is not itself a finished textbook chapter. Keep the publication gate in every chapter: generate, render, visually inspect, extract text, and correct the PDF before accepting it.
