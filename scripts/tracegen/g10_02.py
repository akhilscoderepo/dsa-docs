from common import *
CH='10-intervals'; FILE='02-touching-ends.md'
def walk(a,b,closed,ph):
    inn=(lambda iv,x: iv[0]<=x<=iv[1]) if closed else (lambda iv,x: iv[0]<=x<iv[1])
    st=[]; shared=[]
    for x in range(7):
        ia,ib=inn(a,x),inn(b,x)
        if ia and ib: shared.append(x)
        who="both" if ia and ib else ("A only" if ia else ("B only" if ib else "neither"))
        note={"both":f"Coordinate {x} is in both intervals.","A only":f"Coordinate {x} is in A only.","B only":f"Coordinate {x} is in B only.","neither":f"Coordinate {x} is in neither interval."}[who]
        st.append({"at":{"x":x},"vars":{"in A":str(ia).lower(),"in B":str(ib).lower()},"note":note})
    lo=max(a[0],b[0]); hi=min(a[1],b[1])
    test=(lo<=hi) if closed else (lo<hi)
    assert test==bool(shared)
    st.append({"at":{"x":7},"vars":{"lo":lo,"hi":hi,"overlap":str(test).lower()},"note":f"The walk ends. With lo = {lo} and hi = {hi}, the test gives {str(test).lower()}, which matches the shared coordinates."})
    fill(CH,FILE,block(list(range(7)),["x"],st),ph); return shared
assert walk([1,3],[3,5],True,"@@TRACE1@@")==[3]
assert walk([1,3],[3,5],False,"@@TRACE2@@")==[]
