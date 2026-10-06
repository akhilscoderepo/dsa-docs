<!-- section: review -->
## Review

Return to this page after the lessons, and again after a few days. Each question describes a situation and hides the lesson name. Choose an answer before you read the explanation.

### Recognition Questions

```quiz
{"id": "gr-rev-discard-server", "q": "Jobs and servers are sorted in increasing order. The smallest remaining job needs 5, and the next server has 2. What does the pass do with the server?", "options": ["Gives it to the job anyway", "Gives it to the next job", "Discards it and moves to the next server", "Stops the pass"], "answer": 2, "explain": "A server smaller than the smallest remaining job is smaller than every remaining job, so it can never serve one. The pass discards it and advances the server pointer only."}
```

```quiz
{"id": "gr-rev-end-order", "q": "A scan sorts requests by end time. The last accepted request ends at 6, and the next request is the half-open interval [6,9). What does the scan do?", "options": ["Accepts it, because touching is allowed", "Rejects it, because 6 is not below 6", "Rejects it, because it is longer", "Accepts it only if no other request remains"], "answer": 0, "explain": "A half-open interval excludes its end, so [6,9) starts exactly when the previous request stops. The test start >= lastEnd holds, and the scan accepts the request."}
```

```quiz
{"id": "gr-rev-frontier-gap", "q": "A scan of the powers [2,0,0,1] keeps farthest. What does the scan return when it reaches index 3?", "options": ["True, because the array has a 1 at the end", "True, because 2 is at least 1", "False, because index 2 forwards nowhere", "False, because index 3 is beyond farthest, which is 2"], "answer": 3, "explain": "Indexes 0, 1 and 2 leave farthest at 2. Index 3 is greater than 2, so no scanned station forwards that far. The scan returns false at that index."}
```

```quiz
{"id": "gr-rev-samples-proof", "q": "A rule matches the best answer on ten thousand random inputs. What does that establish?", "options": ["The rule is correct for every input", "The rule is correct for every input of its size", "The rule has not failed on those inputs, and one failing input would still disprove it", "The rule runs in linear time"], "answer": 2, "explain": "Passing inputs show only that the rule has not failed so far. A proof needs an argument about an arbitrary input, such as an exchange step that keeps the answer valid and no worse."}
```

```quiz
{"id": "gr-rev-drop-longest", "q": "A scan holds retained durations 5 and keeps adding. The next course lasts 2 with a last day of 6, and the total becomes 7. Which duration does the scan drop?", "options": ["2, the new course", "5, the longest retained duration", "Both", "Neither, because the total is allowed to pass the last day"], "answer": 1, "explain": "The total 7 passes the last day 6, so one course must leave. Dropping the longest, 5, lowers the total most. The new course then fits, and the count stays at one course."}
```

```quiz
{"id": "gr-rev-stream-cut", "q": "In the stream abab, the scan has read index 1. May the first part close after index 1?", "options": ["Yes, because two letters have been read", "No, because b appears again at index 3, so end is 3", "Yes, because a appears twice", "No, because a part needs three letters"], "answer": 1, "explain": "The letters a and b last appear at indexes 2 and 3, so end is 3 after index 1. A cut after index 1 would place a and b in two parts."}
```

```quiz
{"id": "gr-rev-gap-type", "q": "A scan keeps intervals whose start is at least the previous end plus a gap. Ends reach 2^31 - 1 and the gap reaches 10^9. Which type holds the bound?", "options": ["int", "long", "short", "char"], "answer": 1, "explain": "An end of 2^31 - 1 plus a gap of 10^9 passes the int maximum of 2^31 - 1 and wraps to a negative bound, which would accept intervals that must be rejected. A long holds the sum."}
```
