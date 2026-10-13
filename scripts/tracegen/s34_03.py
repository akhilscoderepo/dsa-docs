from common import *
CH = '34-advanced-strings'; F = '03-palindrome-radii.md'

# Simulate again with explicit mirror values so every note is exact.
def trace(s, expected):
    t = '#' + '#'.join(s) + '#'
    m = len(t); rad = [0] * m; center = right = 0; st = []
    for i in range(m):
        if i < right:
            j = 2 * center - i
            cap = right - i
            start = min(cap, rad[j])
            if rad[j] < cap: how = f"Mirror {j} has radius {rad[j]}, below the edge distance {cap}, so the copy {start} is exact."
            elif rad[j] == cap: how = f"Mirror {j} has radius {rad[j]}, equal to the edge distance {cap}, so the copy {start} reaches the edge and expansion must test beyond it."
            else: how = f"Mirror {j} has radius {rad[j]}, above the edge distance {cap}, so the clamp reduces the copy to {start}."
        else:
            start = 0
            how = "No known palindrome covers this index, so the radius starts at 0."
        rad[i] = start
        while i - rad[i] - 1 >= 0 and i + rad[i] + 1 < m and t[i - rad[i] - 1] == t[i + rad[i] + 1]:
            rad[i] += 1
        if i + rad[i] > right: center, right = i, i + rad[i]
        grown = rad[i] - start
        st.append({"at": {"i": i, "c": center, "r": right},
                   "vars": {"rad": str(rad[i]), "copied": str(start), "expanded": str(grown)},
                   "note": f"i = {i}: {how} Expansion adds {grown}, so rad[{i}] = {rad[i]}."})
    assert rad == expected, (rad, expected)
    # brute-force oracle for the radii
    for i in range(m):
        k = 0
        while i - k - 1 >= 0 and i + k + 1 < m and t[i - k - 1] == t[i + k + 1]: k += 1
        assert k == rad[i]
    return block(list(t), ["i", "c", "r"], st)

fill(CH, F, trace('abaab', [0, 1, 0, 3, 0, 1, 4, 1, 0, 1, 0]), "@@TRACE1@@")
fill(CH, F, trace('abab', [0, 1, 0, 3, 0, 3, 0, 1, 0]), "@@TRACE2@@")
