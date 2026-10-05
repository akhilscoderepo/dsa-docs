from common import *
CH='08-two-pointers'; F='02-read-and-write.md'
def t1():
    a=[1,2,2,3,2,4]; val=2; w=0; kept=[]; st=[]
    for r,x in enumerate(a):
        if x!=val:
            kept.append(x); st.append({"at":{"read":r,"write":w},"vars":{"value":str(x),"kept":str(kept)},"note":f"The value {x} differs from {val}, so it is copied to slot {w} and write advances."}); w+=1
        else:
            st.append({"at":{"read":r,"write":w},"vars":{"value":str(x),"kept":str(kept)},"note":f"The value {x} equals {val}, so only read advances."})
    assert kept==[v for v in a if v!=val] and w==3
    st.append({"at":{"read":len(a),"write":w},"vars":{"kept":str(kept)},"note":"The scan ends. The kept prefix [1, 3, 4] holds three values, so the method returns 3."})
    return block(a,["read","write"],st)
def t2():
    a=[1,1,1,2,2,3]; w=0; kept=[]; st=[]
    for r,x in enumerate(a):
        if w<2 or x!=kept[w-2]:
            why="fewer than two values are written" if w<2 else f"it differs from the value {kept[w-2]} two slots behind write"
            st.append({"at":{"read":r,"write":w},"vars":{"value":str(x),"kept":str(kept+[x])},"note":f"The value {x} is admitted because {why}."}); kept.append(x); w+=1
        else:
            st.append({"at":{"read":r,"write":w},"vars":{"value":str(x),"kept":str(kept)},"note":f"The value {x} equals the value {kept[w-2]} two slots behind write, so it is skipped."})
    assert kept==[1,1,2,2,3]
    st.append({"at":{"read":len(a),"write":w},"vars":{"kept":str(kept)},"note":"The scan ends with five kept values, so the method returns 5."})
    return block(a,["read","write"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
