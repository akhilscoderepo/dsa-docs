from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '09-balanced-tree-concepts.md'
arr = [3, 2, None, 1]
st = [
    {"at": {"node": 0}, "vars": {"balance": 2, "inorder": "1 2 3"}, "note": "At the board 3 the left side has height 2 and the right side has height 0, so the balance factor is 2 and the left side is too deep."},
    {"at": {"node": 1}, "vars": {"balance": 1, "inorder": "1 2 3"}, "note": "The heavy child 2 is chosen as the pivot. Its right subtree is empty, so nothing needs to move to the left of 3."},
    {"at": {"node": 1}, "vars": {"balance": 0, "inorder": "1 2 3"}, "note": "After the right rotation 2 is on top with 1 on its left and 3 on its right. Both sides now have height 1, and the inorder listing is still 1 2 3."},
]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE1@@")
def search(arr, key, label):
    L, R = parse(arr)
    i = 0; st = []; n = 0
    while True:
        v = arr[i]; n += 1
        if v == key:
            st.append({"at": {"node": i}, "vars": {"tag": key, "visited": n}, "note": f"The board {v} holds the tag {key}, found after {n} boards."}); break
        if key < v:
            st.append({"at": {"node": i}, "vars": {"tag": key, "visited": n}, "note": f"The tag {key} is smaller than {v}, so the walk goes left."}); i = L[i]
        else:
            st.append({"at": {"node": i}, "vars": {"tag": key, "visited": n}, "note": f"The tag {key} is larger than {v}, so the walk goes right and everything on the left is dropped."}); i = R[i]
    return st, n
chain = []
for k in range(1, 8):
    chain += [k, None]
chain = chain[:-1]
st, n = search(chain, 7, "chain"); assert n == 7
fill(CH, F, block(cells(chain), ["node"], st), "@@TRACE2@@")
bal = [4, 2, 6, 1, 3, 5, 7]
st, n = search(bal, 7, "balanced"); assert n == 3
fill(CH, F, block(cells(bal), ["node"], st), "@@TRACE3@@")
