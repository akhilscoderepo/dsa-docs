from common import *
CH='39-dynamic-query-structures'; F='03-ordered-structures.md'
KEYS=[3,7,12,18,25,31,40,52]
LV=[(i+1 & -(i+1)).bit_length() for i in range(len(KEYS))]  # trailing zeros + 1
assert LV==[1,2,1,3,1,2,1,4]
TOP=max(LV)
def nxt(cur,l):
    # next index on level l after cur (cur=-1 is the head); len(KEYS) means none
    for j in range(cur+1,len(KEYS)):
        if LV[j]>l: return j
    return len(KEYS)
def walk(x,strict):
    cur=-1; st=[]; upd={}
    for l in range(TOP-1,-1,-1):
        while True:
            j=nxt(cur,l)
            if j==len(KEYS):
                st.append({"at":{"cur":cur,"probe":j},"vars":{"level":l,"cmp":"none"},"note":f"Level {l}: no node follows, so the search drops to level {l-1}." if l else "Level 0: no node follows, so the search stops."}); break
            ok = KEYS[j]<x if strict else KEYS[j]<=x
            op="<" if strict else "<="
            if ok:
                st.append({"at":{"cur":cur,"probe":j},"vars":{"level":l,"cmp":f"{KEYS[j]} {op} {x}"},"note":f"Level {l}: key {KEYS[j]} {op} {x} holds, so the cursor moves to index {j}."}); cur=j
            else:
                st.append({"at":{"cur":cur,"probe":j},"vars":{"level":l,"cmp":f"{KEYS[j]} {op} {x} false"},"note":f"Level {l}: key {KEYS[j]} {op} {x} fails, so the search drops one level."}); break
        upd[l]=cur
    return cur,st,upd
cur,st,_=walk(31,False)
assert cur==5 and KEYS[cur]==31
st.append({"at":{"cur":cur,"probe":cur},"vars":{"level":0,"answer":KEYS[cur]},"note":"The cursor rests on index 5, so floor(31) is key 31."})
fill(CH,F,block([str(k) for k in KEYS],["cur","probe"],st),"@@TRACE1@@")
cur,st,upd=walk(18,True)
assert upd=={3:-1,2:-1,1:1,0:2}
target=nxt(cur,0); assert KEYS[target]==18 and LV[target]==3
st.append({"at":{"cur":cur,"probe":target},"vars":{"level":0,"unlink":"levels 0,1,2"},"note":"The level 0 successor of index 2 is index 3 with key 18, so erase unlinks index 3 on levels 0, 1 and 2."})
# simulate the unlink and check the survivors on each level
keep=[i for i in range(len(KEYS)) if i!=3]
assert [i for i in keep if LV[i]>1]==[1,5,7] and [i for i in keep if LV[i]>2]==[7]
fill(CH,F,block([str(k) for k in KEYS],["cur","probe"],st),"@@TRACE2@@")
