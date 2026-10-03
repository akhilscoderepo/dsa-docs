from common import *
CH='14-linked-lists'
F='10-multilevel-flattening.md'
def fwd(vals,nxt,head):
    out=[];i=head
    while i is not None: out.append(str(vals[i])); i=nxt[i]
    return ",".join(out)
def bwd(vals,prv,tail):
    out=[];i=tail
    while i is not None: out.append(str(vals[i])); i=prv[i]
    return ",".join(out)
vals=[1,2,3,4,5,7,6]
nxt={0:1,1:2,2:None,3:4,4:5,5:None,6:None}
prv={0:None,1:0,2:1,3:None,4:3,5:4,6:None}
child={1:3,4:6}
stack=[];cur=0;steps=[]
def stk(): return "["+",".join(str(vals[i]) for i in stack)+"]"
while cur is not None:
    note=f"The walker is on the node holding {vals[cur]}."
    if cur in child and child[cur] is not None:
        c=child[cur]
        if nxt[cur] is not None:
            stack.append(nxt[cur]);note+=f" It has a child chain, so its successor, holding {vals[nxt[cur]]}, is pushed onto the stack of deferred successors."
        else: note+=" It has a child chain and no successor, so nothing is pushed."
        nxt[cur]=c;prv[c]=cur;child[cur]=None
        note+=f" The child head, holding {vals[c]}, now follows it, and the child reference is cleared."
        nxtcur=c
    elif nxt[cur] is None and stack:
        s=stack.pop();nxt[cur]=s;prv[s]=cur
        note+=f" This chain has ended, so the deferred successor holding {vals[s]} is popped and linked after it."
        nxtcur=s
    else:
        nxtcur=nxt[cur]
        if nxtcur is None: note+=" There is no child, no successor and nothing deferred, so the walk is complete."
        else: note+=" There is no child, so the walker follows the next link."
    steps.append({"at":{"cur":cur},"vars":{"stack":stk(),"flat_so_far":fwd(vals,nxt,0)},"note":note})
    cur=nxtcur
assert fwd(vals,nxt,0)=="1,2,4,5,6,7,3"
fill(CH,F,block(vals,["cur"],steps),"@@TRACE1@@")
# trace 2: splice one chain: main [1,2,3,4], p=1, child [7,8]
v2=[1,2,3,4,7,8]
n2={0:1,1:2,2:3,3:None,4:5,5:None}
p2={0:None,1:0,2:1,3:2,4:None,5:4}
parent=1;ch=4;ct=5;sv=2
st=[{"at":{"parent":1,"childHead":4,"childTail":5,"saved":-1},"vars":{"forward":fwd(v2,n2,0),"backward":bwd(v2,p2,3)},"note":"The parent holds 2 and has a child chain 7, 8. The main chain reads 1, 2, 3, 4 in both directions."}]
sv=n2[parent]
st.append({"at":{"parent":1,"childHead":4,"childTail":5,"saved":sv},"vars":{"forward":fwd(v2,n2,0),"backward":bwd(v2,p2,3)},"note":"The parent's old successor, the node holding 3, is saved before any link changes."})
n2[ct]=sv;p2[sv]=ct
st.append({"at":{"parent":1,"childHead":4,"childTail":5,"saved":sv},"vars":{"forward":fwd(v2,n2,0),"backward":bwd(v2,p2,3)},"note":"The child tail is linked forward to the saved node and the saved node is linked back to the child tail. The main chain does not show the child yet, but the saved node's back link already reads 8."})
n2[parent]=ch;p2[ch]=parent
st.append({"at":{"parent":1,"childHead":4,"childTail":5,"saved":sv},"vars":{"forward":fwd(v2,n2,0),"backward":bwd(v2,p2,3)},"note":"The parent is linked forward to the child head and the child head back to the parent, and the child reference is cleared. Forward the list reads 1, 2, 7, 8, 3, 4, and backward from the end it reads 4, 3, 8, 7, 2, 1."})
assert fwd(v2,n2,0)=="1,2,7,8,3,4" and bwd(v2,p2,3)=="4,3,8,7,2,1"
fill(CH,F,block(v2,["parent","childHead","childTail","saved"],st),"@@TRACE2@@")
