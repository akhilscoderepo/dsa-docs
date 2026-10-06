from common import *
CH='17-heaps-and-priority-queues'; F='02-heap-orientation.md'
import heapq
d=[3,1,3,1]; h=[(x,i) for i,x in enumerate(d)]; heapq.heapify(h); st=[]; out=[]
st.append({"at":{"pick":-1},"vars":{"left":str([i for _,i in sorted(h)]),"order":"[]"},"note":"Four tasks wait. The rule is the smaller duration first and, for a tie, the smaller index."})
while h:
    x,i=heapq.heappop(h); out.append(i)
    tied=[j for _,j in h if d[j]==x]
    note=f"The task {i} with duration {x} leaves."+(f" Task {tied[0]} has the same duration, and the tie-break picks the smaller index {i}." if tied and min(tied)>i else "")
    st.append({"at":{"pick":i},"vars":{"left":str(sorted(j for _,j in h)),"order":str(out)},"note":note})
assert out==[1,3,0,2]
fill(CH,F,block(d,["pick"],st),"@@TRACE1@@")
def wrap(x): return (x+2**31)%2**32-2**31
cells=[2147483647,-1]
a,b=cells; diff=wrap(a-b)
st=[{"at":{"a":0,"b":1},"vars":{"a":a,"b":b,"true a - b":a-b},"note":"The values are Integer.MAX_VALUE and -1. The true difference is 2147483648, which is larger than the largest int."},
{"at":{"a":0,"b":1},"vars":{"a - b in int":diff,"sign":"negative"},"note":"The subtraction wraps to -2147483648. A negative sign says that a leaves first in a smallest-first queue."},
{"at":{"a":0,"b":1},"vars":{"Integer.compare":1,"leaves first":"b"},"note":"Integer.compare reads the two values directly and returns 1, so b leaves first, which is the correct answer."}]
assert diff<0 and (a>b)
fill(CH,F,block(cells,["a","b"],st),"@@TRACE2@@")
