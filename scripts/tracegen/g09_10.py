from common import *
CH = '09-sliding-window'
F = '10-window-frequency-state.md'

# trace 1: matches counter, fixed width 3
text = "bcxabdcab"
order = "abc"
m = len(order)
want = [0] * 26
for ch in order:
    want[ord(ch) - 97] += 1
have = [0] * 26
matches = sum(1 for c in range(26) if have[c] == want[c])
assert matches == 23
steps = []
found = -1
for right, ch in enumerate(text):
    inn = ord(ch) - 97
    if have[inn] == want[inn]:
        matches -= 1
    have[inn] += 1
    if have[inn] == want[inn]:
        matches += 1
    note = f"Letter {ch} enters at position {right}."
    if right >= m:
        out_ch = text[right - m]
        out = ord(out_ch) - 97
        if have[out] == want[out]:
            matches -= 1
        have[out] -= 1
        if have[out] == want[out]:
            matches += 1
        note += f" Letter {out_ch} leaves from position {right - m}."
    left = max(0, right - m + 1)
    if right >= m - 1:
        note += f" Matches counter is {matches}" + (", so this range is a rearrangement and the answer is start " + str(left) + "." if matches == 26 else ", so it is not a rearrangement.")
        steps.append({"at": {"left": left, "right": right}, "vars": {"matches": matches}, "note": note})
        if matches == 26:
            found = left
            break
    else:
        # fill phase: show it as a step so the counter's start is visible
        steps.append({"at": {"left": 0, "right": right}, "vars": {"matches": matches}, "note": note + f" The range is still filling, and the counter reads {matches}."})
assert found == 6
print([s["vars"]["matches"] for s in steps])
fill(CH, F, block(list(text), ["left", "right"], steps), "@@TRACE1@@")

# trace 2: longest repeat free, shrink steps
s = "tmmzuxt"
have = {}
left = 0
shr = 0
bs, bl = 0, 0
steps = []
for right, ch in enumerate(s):
    have[ch] = have.get(ch, 0) + 1
    steps.append({"at": {"left": left, "right": right}, "vars": {"shrinkSteps": shr, "bestLen": bl},
                  "note": f"Letter {ch} enters at position {right}." + (" It now occurs twice, so the left end must move." if have[ch] > 1 else " Every count is at most one.")})
    if have[ch] > 1:
        moved = 0
        while have[ch] > 1:
            y = s[left]
            have[y] -= 1
            left += 1
            shr += 1
            moved += 1
        steps.append({"at": {"left": left, "right": right}, "vars": {"shrinkSteps": shr, "bestLen": bl},
                      "note": f"The left end moved {moved} times and now sits at {left}, with all counts at most one."})
        if right == 2:
            assert moved == 2
    if right - left + 1 > bl:
        bs, bl = left, right - left + 1
        steps[-1]["vars"]["bestLen"] = bl
        steps[-1]["note"] += f" Width {bl} beats the record, so the best range is now {bs} to {right}."
assert (bs, bl, shr) == (2, 5, 2)
fill(CH, F, block(list(s), ["left", "right"], steps), "@@TRACE2@@")
