from ll import *
CH='14-linked-lists'
F='05-dummy-heads.md'
vals=[5,2,5,7,2,9];blocked={2,5}
nxt=[1,2,3,4,5,None]
first=0  # dummy.next
owner=None  # None means dummy
steps=[]
cand=first
def owner_idx(o): return -1 if o is None else o
while cand is not None:
    nx=nxt[cand]
    if vals[cand] in blocked:
        if owner is None: first=nx
        else: nxt[owner]=nx
        steps.append({"at":{"owner":owner_idx(owner),"cand":cand},"vars":{"list":chain(vals,nxt,first)},"note":f"The candidate holds {vals[cand]}, which is blocked, so the owner's next reference is pointed past it and the owner stays where it is. The list now reads {chain(vals,nxt,first).replace('>',', ') if first is not None else 'empty'}."})
    else:
        steps.append({"at":{"owner":owner_idx(owner),"cand":cand},"vars":{"list":chain(vals,nxt,first)},"note":f"The candidate holds {vals[cand]}, which is allowed, so the owner moves onto it."})
        owner=cand
    cand=nx
assert chain(vals,nxt,first)=="7>9"
fill(CH,F,block(vals,["owner","cand"],steps),"@@TRACE1@@")
A=[1,3,3,6];B=[2,3,6,8];cells=A+B
i=j=0;res=[];st=[]
def ia(i): return i if i<len(A) else -1
def ib(j): return len(A)+j if j<len(B) else -1
while i<len(A) or j<len(B):
    if j>=len(B) or (i<len(A) and A[i]<=B[j]): v=A[i];src="first";i+=1
    else: v=B[j];src="second";j+=1
    if not res or res[-1]!=v:
        res.append(v);act="attached behind the tail"
    else: act="skipped, because the tail already holds that value"
    st.append({"at":{"a":ia(i),"b":ib(j)},"vars":{"result":"["+",".join(map(str,res))+"]"},"note":f"The next node in merged order holds {v} from the {src} list and is {act}."})
assert res==[1,2,3,6,8]
fill(CH,F,block(cells,["a","b"],st),"@@TRACE2@@")
