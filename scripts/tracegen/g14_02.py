from common import *
CH='14-linked-lists'; F='02-reverse.md'
vals=[1,2,3]
def run(correct):
    nxt={0:1,1:2,2:None}
    prev=None; curr=0; steps=[]
    def seq(h):
        out=[];i=h
        while i is not None and len(out)<10: out.append(str(vals[i])); i=nxt[i]
        return ",".join(out) if out else "empty"
    def at(): return {"prev":-1 if prev is None else prev,"curr":len(vals) if curr is None else curr}
    if correct:
        steps.append({"at":at(),"vars":{"prefix":seq(prev),"suffix":seq(curr)},"note":"Start: the reversed prefix is empty and the untouched suffix is the whole list."})
        while curr is not None:
            saved=nxt[curr]; v=vals[curr]
            nxt[curr]=prev; prev=curr; curr=saved
            steps.append({"at":at(),"vars":{"prefix":seq(prev),"suffix":seq(curr)},"note":f"saved keeps the rest, then the node {v} is redirected at the old prefix. The prefix now starts at the node {v}."})
        assert seq(prev)=="3,2,1" and curr is None
    else:
        steps.append({"at":at(),"vars":{"reachable":"1,2,3"},"note":"Start: curr is the node 1, and no variable holds saved."})
        v=vals[curr]; nxt[curr]=prev
        steps.append({"at":at(),"vars":{"reachable":seq(curr)},"note":f"The node {v} is redirected first. Its next is now null, so the nodes 2 and 3 lose their only link."})
        assert seq(curr)=="1"
        prev=curr; curr=nxt[curr]
        steps.append({"at":at(),"vars":{"reachable":seq(prev)},"note":"The advance reads the new null, so curr is null and the loop ends. The list is the single node 1."})
        assert curr is None
    return steps
fill(CH,F,block(vals,["prev","curr"],run(True)),"@@TRACE1@@")
fill(CH,F,block(vals,["prev","curr"],run(False)),"@@TRACE2@@")
