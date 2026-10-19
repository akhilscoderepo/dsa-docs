from common import *
import heapq
CH='40-composite-indexes-and-allocation'; F='92-availability-priority.md'
def counter():
    nxt=1; rel=[]; calls=["reserve","reserve","reserve","unreserve(2)","reserve","reserve"]; st=[]; out=[]
    for k,c in enumerate(calls):
        if c=="reserve":
            if rel: s=heapq.heappop(rel); note=f"Call {k}: the released heap holds a seat, so the call returns the smallest one, {s}."
            else: s=nxt; nxt+=1; note=f"Call {k}: the released heap is empty, so the call returns the counter value {s} and raises the counter to {nxt}."
            r=str(s)
        else:
            s=2; heapq.heappush(rel,s); r="null"; note=f"Call {k}: seat {s} goes into the released heap, and the counter stays at {nxt}."
        st.append({"at":{"call":k},"vars":{"next":nxt,"released":"{"+",".join(map(str,sorted(rel)))+"}","result":r},"note":note}); out.append(r)
    assert out==["1","2","3","null","2","4"]
    return calls,st
def room():
    n=8; occ=[]; heap=[]; calls=["seat","seat","seat","seat","leave(3)","leave(5)","seat","seat"]; st=[]; out=[]
    def seat_of(g):
        l,r=g; return 0 if l==-1 else (n-1 if r==n else l+(r-l)//2)
    def dist(g):
        l,r=g; return r if l==-1 else (n-1-l if r==n else (r-l)//2)
    def push(g):
        if dist(g)>0: heapq.heappush(heap,(-dist(g),seat_of(g),g))
    def valid(g):
        l,r=g
        if l==-1: return bool(occ) and occ[0]==r
        if r==n: return bool(occ) and occ[-1]==l
        return l in occ and r in occ and not any(l<x<r for x in occ)
    for k,c in enumerate(calls):
        if c=="seat":
            if not occ:
                occ.append(0); push((0,n)); r="0"; note=f"Call {k}: the room is empty, so the first student takes seat 0 and the candidate (0,{n}) enters the heap."
            else:
                skipped=[]
                while True:
                    _,s,g=heapq.heappop(heap)
                    if valid(g): break
                    skipped.append(g)
                l,rr=g; occ.append(s); occ.sort(); push((l,s)); push((s,rr)); r=str(s)
                note=f"Call {k}: "+(f"the call drops {len(skipped)} stale candidate{'s' if len(skipped)>1 else ''}, then " if skipped else "")+f"the current candidate ({l},{rr}) gives seat {s}. Its two halves ({l},{s}) and ({s},{rr}) enter the heap."
        else:
            p=int(c[6:-1]); occ.remove(p); L=max([x for x in occ if x<p],default=-1); R=min([x for x in occ if x>p],default=n); push((L,R)); r="null"
            note=f"Call {k}: seat {p} leaves, so its neighbors {L} and {R} form the new candidate ({L},{R}). The old candidates that name seat {p} stay in the heap."
        st.append({"at":{"call":k},"vars":{"occupied":"{"+",".join(map(str,occ))+"}","heapSize":len(heap),"result":r},"note":note}); out.append(r)
    assert out==["0","7","3","5","null","null","3","5"],out
    return calls,st
c,s=counter(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=room(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
