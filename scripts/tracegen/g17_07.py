from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='07-running-median.md'
def wrap(x): return (x+2**31)%2**32-2**31
def run(vals):
    lo=[]; up=[]; st=[]
    for i,v in enumerate(vals):
        note=""
        if not lo or v<=-lo[0]: heapq.heappush(lo,-v); side="lower"
        else: heapq.heappush(up,v); side="upper"
        note=f"The value {v} goes to the {side} half."
        if len(lo)>len(up)+1:
            x=-heapq.heappop(lo); heapq.heappush(up,x); note+=f" The lower half is two ahead, so its root {x} moves to the upper half."
        elif len(up)>len(lo):
            x=heapq.heappop(up); heapq.heappush(lo,-x); note+=f" The upper half is ahead, so its root {x} moves to the lower half."
        else: note+=" The sizes already follow the rule."
        med=-lo[0] if len(lo)>len(up) else (-lo[0]+up[0])/2
        st.append({"at":{"next":i},"vars":{"lower":str(sorted(-x for x in lo)),"upper":str(sorted(up)),"median":med},"note":note+f" The median is {med}."})
    return st
st=run([5,2,8,1,9]); assert [s["vars"]["median"] for s in st]==[5,3.5,5,3.5,5]
fill(CH,F,block([5,2,8,1,9],["next"],st),"@@TRACE1@@")
vals=[2147483647,2147483646]; st=run(vals)
a,b=vals; st[-1]["note"]=f"The value {b} goes to the lower half, and the rebalance leaves one value in each half. In int arithmetic {a} + {b} wraps to {wrap(a+b)}. With a long sum, the average is {(a+b)/2}."
assert st[-1]["vars"]["median"]==2147483646.5
fill(CH,F,block(vals,["next"],st),"@@TRACE2@@")
