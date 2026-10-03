# helpers for tree traces: trees are level-order arrays with None for absent children
def parse(arr):
    """returns (left, right) dicts mapping array index -> child array index (or None)."""
    left, right = {}, {}
    if not arr or arr[0] is None: return left, right
    q = [0]; nxt = 1; qi = 0
    while qi < len(q):
        i = q[qi]; qi += 1
        for side in (left, right):
            if nxt < len(arr) and arr[nxt] is not None:
                side[i] = nxt; q.append(nxt)
            else:
                side[i] = None
            nxt += 1
    return left, right
def cells(arr):
    return ["null" if v is None else str(v) for v in arr]
