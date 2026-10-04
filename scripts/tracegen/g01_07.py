from common import *
CH = '01-arrays-core-operations'
F = '07-majority-vote.md'

def run(nums):
    cand, votes, steps = None, 0, []
    for i, v in enumerate(nums):
        if votes == 0:
            cand, votes = v, 1
            note = f"The votes are zero, so {v} becomes the candidate with one vote."
        elif v == cand:
            votes += 1
            note = f"{v} equals the candidate, so the votes grow to {votes}."
        else:
            votes -= 1
            note = f"{v} differs from the candidate {cand}, so one cancellation leaves {votes} votes."
        steps.append({"at": {"i": i}, "vars": {"candidate": cand, "votes": votes}, "note": note})
    n = len(nums)
    occ = nums.count(cand)
    verdict = "more than" if occ > n // 2 else "not more than"
    steps.append({"at": {"i": n}, "vars": {"candidate": cand, "votes": votes, "occurrences": occ},
                  "note": f"The scan ends with candidate {cand}. The second count finds {occ} occurrences, which is {verdict} {n // 2}."})
    return steps, cand, occ

t1 = [3, 1, 3, 2, 3, 3, 1]
s, c, o = run(t1)
assert c == 3 and o == 4 and o > len(t1) // 2 and s[-2]["vars"]["votes"] == 1
fill(CH, F, block(t1, ["i"], s), "@@TRACE1@@")
t2 = [4, 5, 6]
s, c, o = run(t2)
assert c == 6 and o == 1 and not o > len(t2) // 2
fill(CH, F, block(t2, ["i"], s), "@@TRACE2@@")
