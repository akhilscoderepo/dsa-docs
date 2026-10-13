from common import *
from collections import OrderedDict
CH='33-design-data-structure-problems'; F='91-map-and-linked-list.md'
def run(cap, ops):
    lst=[]  # hot end first
    ref=OrderedDict()
    cells=[o[1] for o in ops]
    st=[{"at":{"op":-1},"vars":{"list":"[]","mapKeys":"{}"},"note":f"Start: capacity {cap}, an empty list and an empty map."}]
    for i,(kind,k) in enumerate(ops):
        if kind=='put':
            if k in lst:
                lst.remove(k); lst.insert(0,k); note=f"put {k}: the key exists, so its node moves to the hot end."
            else:
                note=f"put {k}: the key is new."
                if len(lst)==cap:
                    ev=lst.pop(); note+=f" The cache is full, so cold node {ev} is detached and removed from the map."
                lst.insert(0,k); note+=f" Node {k} joins the hot end."
            if k in ref: ref.move_to_end(k,last=False)
            else:
                if len(ref)==cap: ref.popitem()
                ref[k]=1; ref.move_to_end(k,last=False)
        else:
            if k in lst:
                lst.remove(k); lst.insert(0,k); note=f"get {k}: the map finds node {k}, which is detached and inserted at the hot end."
                ref.move_to_end(k,last=False)
            else:
                note=f"get {k}: the map has no such key, so the call returns -1 and the list is unchanged."
        assert list(ref.keys())==lst
        st.append({"at":{"op":i},"vars":{"list":str(lst).replace(' ',''),"mapKeys":str(sorted(lst)).replace(' ','')},"note":note+f" The list reads {lst} from hot to cold."})
    return cells,st,lst
c,st,l=run(2,[('put',1),('put',2),('get',1),('put',3),('get',2)]); assert l==[3,1]
fill(CH,F,block(c,["op"],st),"@@TRACE1@@")
c,st,l=run(3,[('put',1),('put',2),('put',3),('get',1),('get',1),('put',4)]); assert l==[4,1,3]
fill(CH,F,block(c,["op"],st),"@@TRACE2@@")
