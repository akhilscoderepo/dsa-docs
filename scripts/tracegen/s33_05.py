from common import *
CH='33-design-data-structure-problems'; F='05-randomized-sets.md'
def fmt_map(m):
    return ", ".join(f"{k}->{v}" for k, v in m.items())
def run(vals, target):
    cells = list(vals)
    arr = list(vals); idx = {v: i for i, v in enumerate(arr)}
    lastpos = len(arr) - 1
    st = [{"at":{"slot":-1,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx)},"note":f"Start: remove {target}. The array is {arr} and the last slot is {lastpos}."}]
    slot = idx[target]; last = arr[-1]
    st.append({"at":{"slot":slot,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx)},"note":f"The map gives slot {slot} for {target}. The last slot {lastpos} holds {last}."})
    arr[slot] = last
    st.append({"at":{"slot":slot,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx)},"note":f"Copy {last} into slot {slot}. The array reads {arr}."})
    idx[last] = slot
    st.append({"at":{"slot":slot,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx)},"note":f"Record slot {slot} for {last} in the map."})
    arr.pop()
    st.append({"at":{"slot":slot,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx)},"note":f"Drop the last slot. The array reads {arr}."})
    del idx[target]
    st.append({"at":{"slot":slot,"last":lastpos},"vars":{"array":str(arr),"map":fmt_map(idx) or "empty"},"note":f"Delete the entry for {target} as the final step. The map agrees with the array again."})
    # invariant check
    assert all(arr[i] == k for k, i in idx.items()) and len(arr) == len(idx)
    return cells, st, arr, idx
c, st, arr, idx = run([10,20,30,40], 20)
assert arr == [10,40,30] and idx == {10:0,30:2,40:1}
fill(CH,F,block(c,["slot","last"],st),"@@TRACE1@@")
c, st, arr, idx = run([10,20,40], 40)
assert arr == [10,20] and 40 not in idx
fill(CH,F,block(c,["slot","last"],st),"@@TRACE2@@")
