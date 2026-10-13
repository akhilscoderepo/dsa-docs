from common import *
CH = '33-design-data-structure-problems'; F = '06-cache-design.md'

def lru(cap, ops):
    order = []  # most recent first
    vals = {}
    st = []
    for i, (kind, k, v) in enumerate(ops):
        note = ""
        if kind == 'put':
            if k in vals:
                order.remove(k); note = f"put({k}, {v}) overwrites and refreshes key {k}."
            elif len(order) == cap:
                ev = order.pop(); del vals[ev]; note = f"put({k}, {v}) finds the cache full, so key {ev} leaves from the back."
            else:
                note = f"put({k}, {v}) adds key {k} at the front."
            vals[k] = v; order.insert(0, k)
        else:
            if k in vals:
                order.remove(k); order.insert(0, k); note = f"get({k}) returns {vals[k]} and moves key {k} to the front."
            else:
                note = f"get({k}) is a miss and changes nothing."
        st.append({"at": {"op": i}, "vars": {"order": str(order).replace(" ", ""), "size": len(order)}, "note": note + f" Order is {order}."})
    return st, order

ops = [('put',1,10),('put',2,20),('get',1,0),('put',3,30),('get',2,0),('put',4,40)]
st, order = lru(2, ops)
assert order == [4, 3]
assert [o[1] for o in ops] == [1, 2, 1, 3, 2, 4]
fill(CH, F, block([o[1] for o in ops], ["op"], st), "@@TRACE1@@")

def lfu(cap, ops):
    cnt = {}; stamp = {}; clock = 0; st = []; mn = 0
    for i, (kind, k) in enumerate(ops):
        clock += 1
        if kind == 'put':
            if k in cnt:
                cnt[k] += 1; stamp[k] = clock; note = f"put({k}) overwrites and raises its count to {cnt[k]}."
            else:
                note = f"put({k}) adds key {k} with count 1."
                if len(cnt) == cap:
                    ev = min(cnt, key=lambda x: (cnt[x], stamp[x])); note = f"put({k}) finds the cache full, so key {ev} with count {cnt[ev]} leaves from the back of its bucket, then key {k} enters with count 1."
                    del cnt[ev]; del stamp[ev]
                cnt[k] = 1; stamp[k] = clock
        else:
            cnt[k] += 1; stamp[k] = clock; note = f"get({k}) raises its count to {cnt[k]}."
        mn = min(cnt.values())
        st.append({"at": {"op": i}, "vars": {"counts": str(dict(sorted(cnt.items()))).replace(" ", ""), "minFreq": mn}, "note": note + f" The minimum frequency is {mn}."})
    return st, cnt

ops = [('put',1),('put',2),('get',2),('get',1),('put',3),('put',4)]
st, cnt = lfu(2, ops)
assert cnt == {1: 2, 4: 1}, cnt
fill(CH, F, block([o[1] for o in ops], ["op"], st), "@@TRACE2@@")
