from common import *
CH = '08-two-pointers'
F = '01-opposite-ends.md'

def scan(tags, card):
    left, right = 0, len(tags) - 1
    steps = []
    found = None
    while left < right:
        s = tags[left] + tags[right]
        if s == card:
            steps.append({"at": {"left": left, "right": right}, "vars": {"sum": s}, "note": f"Tags {tags[left]} and {tags[right]} add up to {s}, which equals the card, so the pair is found."})
            found = (left + 1, right + 1)
            break
        if s < card:
            steps.append({"at": {"left": left, "right": right}, "vars": {"sum": s}, "note": f"Sum {s} is below {card}, so tag {tags[left]} is short even with the dearest partner and left moves to {left + 1}."})
            left += 1
        else:
            steps.append({"at": {"left": left, "right": right}, "vars": {"sum": s}, "note": f"Sum {s} is above {card}, so tag {tags[right]} is too dear even with the cheapest partner and right moves to {right - 1}."})
            right -= 1
    if found is None:
        steps.append({"at": {"left": left, "right": right}, "vars": {"sum": tags[left] * 2}, "note": "The two pointers meet on one position, so the live interval holds no pair and the answer is none."})
    return steps, found

t1 = [2, 5, 8, 11, 15, 19, 23]
s, f = scan(t1, 26)
assert f == (4, 5) and len(s) == 6
fill(CH, F, block(t1, ["left", "right"], s), "@@TRACE1@@")
t2 = [3, 3, 4, 9, 9, 14]
s, f = scan(t2, 20)
assert f is None and s[-1]["at"]["left"] == s[-1]["at"]["right"]
fill(CH, F, block(t2, ["left", "right"], s), "@@TRACE2@@")
