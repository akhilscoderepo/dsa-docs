from common import *
CH = '09-sliding-window'
F = '09-repeated-shrink-versus-non-shrinking-policy.md'

# trace 1: valid window, repeat-free rule, restore with while
a = list("dabcbeda")
inside = {}
l = 0
best = 0
steps = []
burst_at_second_b = None
for r, x in enumerate(a):
    inside[x] = inside.get(x, 0) + 1
    if inside[x] == 1:
        w = r - l + 1
        best = max(best, w)
        steps.append({"at": {"l": l, "r": r}, "vars": {"width": w, "best": best},
                      "note": f"Add {x} at position {r}. No letter repeats, so the window is valid and its width {w} is recorded."})
    else:
        steps.append({"at": {"l": l, "r": r}, "vars": {"width": r - l + 1, "best": best},
                      "note": f"Add {x} at position {r}. It now appears twice, so the window is broken and must not be measured."})
        removed = 0
        while inside[x] > 1:
            y = a[l]
            inside[y] -= 1
            l += 1
            removed += 1
            steps.append({"at": {"l": l, "r": r}, "vars": {"width": r - l + 1, "best": best},
                          "note": f"Remove {y} from the left, so l becomes {l}." + (" The repeat is still there." if inside[x] > 1 else " The repeat is gone, so the window is valid again.")})
        if r == 4:
            burst_at_second_b = removed
        best = max(best, r - l + 1)
steps[-1]["note"] += f" Best width so far is {best}."
assert best == 5 and burst_at_second_b == 3
fill(CH, F, block(a, ["l", "r"], steps), "@@TRACE1@@")

# trace 2: length bound with a tracked maximum, one removal at most
s = "MMMMNPQR"
k = 1
cells = list(s)
cnt = {}
l = 0
tracked = 0
steps = []
first_shift = None
for r, ch in enumerate(s):
    cnt[ch] = cnt.get(ch, 0) + 1
    tracked = max(tracked, cnt[ch])
    if r - l + 1 - tracked > k:
        y = s[l]
        cnt[y] -= 1
        l += 1
        if first_shift is None:
            first_shift = r
        note = f"Add {ch} at position {r}. Width minus tracked maximum {tracked} is more than {k}, so one letter ({y}) leaves and the frame shifts. Width stays {r - l + 1}."
    else:
        note = f"Add {ch} at position {r}. Width minus tracked maximum {tracked} is at most {k}, so nothing leaves and the width grows to {r - l + 1}."
    exact = max(v for v in cnt.values())
    steps.append({"at": {"l": l, "r": r}, "vars": {"width": r - l + 1, "tracked": tracked, "exact": exact}, "note": note})
assert first_shift == 5 and len(s) - l == 5
assert steps[-1]["vars"]["tracked"] == 4 and steps[-1]["vars"]["exact"] == 1
fill(CH, F, block(cells, ["l", "r"], steps), "@@TRACE2@@")
