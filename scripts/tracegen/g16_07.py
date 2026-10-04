from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '07-iterator-foundations.md'
def run(arr, calls):
    L, R = parse(arr)
    stack = []
    def push_left(i):
        while i is not None:
            stack.append(i); i = L[i]
    def show():
        return " ".join(str(arr[j]) for j in reversed(stack)) or "empty"
    steps = []
    push_left(0)
    steps.append({"at": {"node": stack[-1]}, "vars": {"returned": "none", "stack": show()}, "note": f"The constructor loads the left spine, so the stack holds {show()} from the top down and the smallest card {arr[stack[-1]]} is on top."})
    out = []
    for _ in range(calls):
        top = stack.pop()
        pushed = []
        c = R[top]
        before = len(stack)
        push_left(R[top])
        pushed = [arr[j] for j in stack[before:]]
        out.append(arr[top])
        extra = f"Its right child starts a new spine, so {' '.join(map(str, pushed))} is pushed." if pushed else "It has no right child, so nothing is pushed."
        nxt = stack[-1] if stack else -1
        tail = f"The next card is {arr[nxt]}." if stack else "The stack is empty, so no card is left."
        steps.append({"at": {"node": nxt}, "vars": {"returned": arr[top], "stack": show()}, "note": f"The request pops {arr[top]} and returns it. {extra} {tail}"})
    return steps, out
arr = [10, 5, 15, 3, 7, 12, 20, 2, None, 6]
st, out = run(arr, 5); assert out == [2, 3, 5, 6, 7]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE1@@")
arr = [1, None, 2, None, 3]
st, out = run(arr, 3); assert out == [1, 2, 3]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE2@@")
