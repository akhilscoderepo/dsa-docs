from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='91-reuse-meeting-rooms-with-a-heap.md'
def run(iv,closed):
    s=sorted(iv); h=[]; st=[]
    for i,(a,b) in enumerate(s):
        reuse=bool(h) and (h[0]<a if closed else h[0]<=a)
        if reuse:
            old=heapq.heappop(h); msg=f"The earliest finish {old} {'is smaller than' if closed else 'is at most'} the start {a}, so the meeting takes over that room."
        elif h: msg=f"The earliest finish {h[0]} {'is not smaller than' if closed else 'is after'} the start {a}, so every room is busy and the program opens a new room."
        else: msg=f"No room exists, so the program opens the first room."
        heapq.heappush(h,b)
        st.append({"at":{"next":i},"vars":{"ends":str(sorted(h)),"rooms":len(h)},"note":msg+f" The end times are {sorted(h)}."})
    return [a for a,_ in s],st,len(h)
c,st,r=run([[1,4],[2,5],[4,6],[5,7]],False); assert r==2
fill(CH,F,block(c,["next"],st),"@@TRACE1@@")
c,st,r=run([[1,3],[3,5],[6,8]],True); assert r==2
fill(CH,F,block(c,["next"],st),"@@TRACE2@@")
