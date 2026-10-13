import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '32-selection-and-ordered-data-techniques'
FILE = '04-merge-counting.md'

def run(left, right):
    cells = left + right
    mid = len(left); hi = len(cells)
    i, j, count = 0, mid, 0
    steps = [{"at": {"i": i, "j": j}, "vars": {"count": 0},
              "note": f"The left half {left} and the right half {right} are both sorted. The count starts at 0."}]
    while i < mid and j < hi:
        if cells[i] <= cells[j]:
            steps.append({"at": {"i": i, "j": j}, "vars": {"count": count},
                          "note": f"The left value {cells[i]} is at most the right value {cells[j]}, so it forms no pair with any right value still unread. The left pointer moves on."})
            i += 1
        else:
            count += mid - i
            steps.append({"at": {"i": i, "j": j}, "vars": {"count": count},
                          "note": f"The left value {cells[i]} is greater than the right value {cells[j]}, and so are all {mid - i} unread left values. The count grows by {mid - i} and becomes {count}. The right pointer moves on."})
            j += 1
    steps.append({"at": {"i": i, "j": j}, "vars": {"count": count},
                  "note": f"One half is used up, so no further pair can form. The answer for this merge is {count}."})
    brute = sum(1 for x in left for y in right if x > y)
    assert brute == count, (brute, count)
    return cells, steps, count

c1, s1, a1 = run([3, 6, 9], [1, 7, 8])
c2, s2, a2 = run([2, 4, 4, 8], [4, 4, 6])
assert (a1, a2) == (5, 3)
fill(CH, FILE, block(c1, ["i", "j"], s1), "@@TRACE1@@")
fill(CH, FILE, block(c2, ["i", "j"], s2), "@@TRACE2@@")
print(a1, a2)
