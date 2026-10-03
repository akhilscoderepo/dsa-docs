from common import *
CH = '09-sliding-window'
F = '03-longest-valid-windows.md'


def one_zero(a):
    left = zeros = best = 0
    steps = []
    for right, v in enumerate(a):
        if v == 0:
            zeros += 1
        removed = 0
        while zeros > 1:
            if a[left] == 0:
                zeros -= 1
            left += 1
            removed += 1
        best = max(best, right - left + 1)
        if v == 0 and removed:
            note = f"Position {right} is a second zero, a violation, so {removed} stalls leave from the left and left becomes {left}. The window is healthy at length {right-left+1}."
        elif v == 0:
            note = f"Position {right} is the first zero in the window. It is allowed, so the window grows to length {right-left+1}."
        else:
            note = f"Position {right} is open. The window grows to length {right-left+1}."
        steps.append({"at": {"left": left, "right": right}, "vars": {"zeros": zeros, "best": best}, "note": note})
    return steps, best


a = [1, 1, 0, 1, 1, 1, 0, 1]
s, best = one_zero(a)
assert best == 6 and "second zero" in s[6]["note"] and s[6]["at"]["left"] == 3
fill(CH, F, block(a, ["left", "right"], s), "@@TRACE1@@")


def no_repeat(text):
    cnt = {}
    left = best = 0
    steps = []
    for right, c in enumerate(text):
        cnt[c] = cnt.get(c, 0) + 1
        removed = 0
        while cnt[c] > 1:
            cnt[text[left]] -= 1
            left += 1
            removed += 1
        best = max(best, right - left + 1)
        if removed:
            note = f"Letter {c} at position {right} repeats, so {removed} letters leave from the left and left becomes {left}. The window has length {right-left+1}."
        else:
            note = f"Letter {c} at position {right} is new to the window, so it grows to length {right-left+1}."
        steps.append({"at": {"left": left, "right": right}, "vars": {"removed": removed, "best": best}, "note": note})
    return steps, best


t = "kqnnkrsq"
s, best = no_repeat(t)
assert best == 5 and s[3]["note"].startswith("Letter n at position 3 repeats, so 3 letters")
fill(CH, F, block(list(t), ["left", "right"], s), "@@TRACE2@@")
