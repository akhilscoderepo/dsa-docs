from common import *
CH = '08-two-pointers'
F = '02-read-and-write.md'

def remove_value(cells, val):
    a = list(cells)
    write = 0
    steps = []
    for read in range(len(a)):
        v = a[read]
        if v == val:
            note = f"Value {v} equals {val}, so it is skipped and the read index moves on while the write index stays at {write}."
            steps.append({"at": {"read": read, "write": write}, "vars": {"value": v, "kept": write}, "note": note})
        else:
            note = f"Value {v} is accepted and copied to slot {write}, then the write index becomes {write + 1}."
            steps.append({"at": {"read": read, "write": write}, "vars": {"value": v, "kept": write + 1}, "note": note})
            a[write] = a[read]
            write += 1
    return steps, a[:write]

def one_per_run(cells):
    a = list(cells)
    write = 0
    steps = []
    for read in range(len(a)):
        v = a[read]
        if write == 0 or v != a[write - 1]:
            note = f"Value {v} differs from the newest accepted value, so it goes to slot {write} and the write index becomes {write + 1}."
            steps.append({"at": {"read": read, "write": write}, "vars": {"value": v, "kept": write + 1}, "note": note})
            a[write] = v
            write += 1
        else:
            note = f"Value {v} equals the value just behind the write index, so the kept prefix refuses it and the write index stays at {write}."
            steps.append({"at": {"read": read, "write": write}, "vars": {"value": v, "kept": write}, "note": note})
    return steps, a[:write]

c1 = [4, 1, 4, 2, 3, 4, 5]
s, out = remove_value(c1, 4)
assert out == [1, 2, 3, 5] and s[2]["at"] == {"read": 2, "write": 1}
fill(CH, F, block(c1, ["read", "write"], s), "@@TRACE1@@")
c2 = [2, 2, 3, 3, 3, 5, 7, 7]
s, out = one_per_run(c2)
assert out == [2, 3, 5, 7] and "refuses" in s[4]["note"] and s[4]["at"]["read"] == 4
fill(CH, F, block(c2, ["read", "write"], s), "@@TRACE2@@")
