from common import *
CH='33-design-data-structure-problems'; F='02-invariant-ownership.md'
CAP=3
SCRIPT=[("open",4),("open",7),("open",9),("open",5),("close",7),("open",5)]
def run(naive):
    lst=[]; size=0; table=set(); steps=[]
    def vars_(res):
        return {"list":"["+",".join(map(str,lst))+"]","size":size,"nodes":len(lst),"result":res}
    steps.append({"at":{"op":-1},"vars":vars_("start"),"note":"Start: an empty strip with capacity 3. The counter, the list and the table all say empty."})
    cells=[v for _,v in SCRIPT]
    for i,(op,v) in enumerate(SCRIPT):
        if op=="open":
            if naive:
                size+=1
                if size>CAP:
                    res="throws"; note=f"open {v}: the counter rises to {size} first, then the capacity test throws. The list still holds {len(lst)} tabs, so the two now disagree."
                else:
                    lst.append(v); table.add(v); res="ok"; note=f"open {v}: counter and list both reach {size}."
            else:
                if size==CAP:
                    res="throws"; note=f"open {v}: the precheck sees size {size} equals capacity and throws before any write. Every field keeps its value."
                else:
                    lst.append(v); table.add(v); size+=1; res="ok"; note=f"open {v}: the precheck passes and attach links the node, adds the id and raises size to {size}."
        else:
            lst.remove(v); table.discard(v); size-=1; res="ok"
            note=f"close {v}: detach unlinks the node, removes the id and lowers size to {size}." if not naive else f"close {v}: the counter drops to {size}, but the list holds {len(lst)} tabs."
        steps.append({"at":{"op":i},"vars":vars_(res),"note":note})
    return cells,steps,lst,size
c,st,lst,size=run(False); assert lst==[4,9,5] and size==3
assert all(s["vars"]["size"]==s["vars"]["nodes"] for s in st)
steps1=st
c2,st2,lst2,size2=run(True); assert lst2==[4,9] and size2==4
st2.append({"at":{"op":5},"vars":st2[-1]["vars"],"note":"Done. The last open 5 threw although only two tabs are open, because the counter reads 3. The drift is permanent."})
st.append({"at":{"op":5},"vars":st[-1]["vars"],"note":"Done. The strip holds 4, 9 and 5, and size, nodes and the table all agree at 3."})
fill(CH,F,block(c,["op"],steps1),"@@TRACE1@@")
fill(CH,F,block(c2,["op"],st2),"@@TRACE2@@")
