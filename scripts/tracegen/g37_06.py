from common import *
CH='37-iterators-encodings-and-versioned-state'; F='06-incremental-trees.md'

class N:
    def __init__(s, v): s.v=v; s.l=None; s.r=None
def level(root):
    out=[]; q=[root]
    while q:
        n=q.pop(0); out.append(n.v)
        if n.l: q.append(n.l)
        if n.r: q.append(n.r)
    return out
def build(vals):
    ns=[N(v) for v in vals]
    for i,n in enumerate(ns):
        if 2*i+1<len(ns): n.l=ns[2*i+1]
        if 2*i+2<len(ns): n.r=ns[2*i+2]
    return ns[0]
def frontier_of(root):
    f=[]; q=[root]
    while q:
        n=q.pop(0)
        if n.l: q.append(n.l)
        if n.r: q.append(n.r)
        if not n.l or not n.r: f.append(n)
    return f
fs=lambda f:",".join(str(n.v) for n in f)

def run(buggy):
    root=build([1,2,3]); fr=frontier_of(root); added=0
    cells=[str(i) for i in range(1,9 if not buggy else 7)]
    steps=[{"at":{"parent":fr[0].v-1,"fresh":-1},"vars":{"frontier":fs(fr),"root":",".join(map(str,level(root))),"result":"none"},
            "note":"The constructor reads the tree 1, 2, 3 once. Nodes 2 and 3 have no children, so the frontier is 2, 3 and parent will be node 2."}]
    for val in range(4, 9 if not buggy else 7):
        parent=fr[0]; fresh=N(val); ordinal=val-3
        if parent.l is None:
            parent.l=fresh; side="left"; popped=False; lost=None
        else:
            side="right"; lost=parent.r
            parent.r=fresh; popped=not buggy
        if popped: fr.pop(0)
        fr.append(fresh)
        reach=level(root)
        head=fr[0].v-1
        if not buggy:
            if side=="left":
                note=f"Insert {val}: parent is node {parent.v}, the head of the frontier, and its left slot is open. The call attaches {val} as its left child, keeps node {parent.v} in the frontier and appends node {val}. The call returns {parent.v}."
            else:
                note=f"Insert {val}: parent is node {parent.v}, the head of the frontier, and its left slot is taken. The call attaches {val} as its right child, removes node {parent.v} because it is full and appends node {val}. The call returns {parent.v}."
        else:
            if lost is None:
                note=f"Insert {val}: parent is node {parent.v}, the head of the frontier, with an open {side} slot. The call attaches {val} and appends node {val}. The class does not remove full nodes, so node {parent.v} stays at the head."
            else:
                note=f"Insert {val}: parent is still node {parent.v}, the head of the frontier, which already has two children. The call overwrites its right child {lost.v} with {val}. The class returns {parent.v} and counts {val} nodes, but only {len(reach)} nodes are reachable from the root."
        steps.append({"at":{"parent":parent.v-1,"fresh":val-1},"vars":{"frontier":fs(fr),"root":",".join(map(str,reach)),"result":parent.v},"note":note})
    return cells,steps,root
c1,s1,r1=run(False)
assert level(r1)==list(range(1,9)) and s1[-1]["vars"]["frontier"]=="4,5,6,7,8" and len(s1)==6
c2,s2,r2=run(True)
assert level(r2)==[1,2,3,4,6] and len(s2)==4
fill(CH,F,block(c1,["parent","fresh"],s1),"@@TRACE1@@")
fill(CH,F,block(c2,["parent","fresh"],s2),"@@TRACE2@@")
