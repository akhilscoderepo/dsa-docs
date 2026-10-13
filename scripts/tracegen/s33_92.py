from common import *
CH='33-design-data-structure-problems'; F='92-map-and-dynamic-array.md'
def run(vals, target):
    items=list(vals); size=len(items); slot={v:i for i,v in enumerate(items)}
    for i,v in enumerate(items): assert slot[v]==i
    st=[]
    def snap(): return "["+",".join(map(str,items[:size]))+"]"
    s=slot[target]; last=size-1
    st.append({"at":{"removed":s,"last":last},"vars":{"items":snap(),"size":size},"note":f"remove({target}): the map says {target} sits at slot {s}, and the last slot is {last} holding {items[last]}."})
    moved=items[last]
    items[s]=moved
    st.append({"at":{"removed":s,"last":last},"vars":{"items":snap(),"size":size},"note":f"Copy {moved} from slot {last} into slot {s}." + (" The copy writes the value onto itself." if s==last else "")})
    slot[moved]=s
    st.append({"at":{"removed":s,"last":last},"vars":{"items":snap(),"size":size,"slotOf["+str(moved)+"]":s},"note":f"Repair the map: {moved} now lives at slot {s}."})
    del slot[target]; size-=1
    st.append({"at":{"removed":s,"last":size},"vars":{"items":snap(),"size":size},"note":f"Delete the key {target} and lower size to {size}. The meaningful array is {snap()}."})
    for i,v in enumerate(items[:size]): assert slot[v]==i
    assert len(slot)==size
    return st,items[:size]
st,r=run([5,8,2,9],8); assert r==[5,9,2]
fill(CH,F,block([5,8,2,9],["removed","last"],st),"@@TRACE1@@")
st,r=run([4,7,1],1); assert r==[4,7]
fill(CH,F,block([4,7,1],["removed","last"],st),"@@TRACE2@@")
