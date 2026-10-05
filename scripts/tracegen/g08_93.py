from common import *
CH='08-two-pointers'; F='93-duplicate-with-two-speeds.md'
a=[1,3,4,2,2]
def t1():
    s=f=0; k=0; st=[]
    while True:
        s=a[s]; f=a[a[f]]; k+=1
        st.append({"at":{"slow":s,"fast":f},"vars":{"links slow":str(k),"links fast":str(2*k),"gap":str(k)},"note":f"After round {k}, slow made {k} links and fast made {2*k} links. The gap is {k}."+(" The pointers meet because the gap 4 is a multiple of the loop length 2." if s==f else "")})
        if s==f: break
    assert k==4 and s==4
    return block(a,["slow","fast"],st)
def t2():
    s=0; f=4; r=0; st=[{"at":{"slow":0,"fast":4},"vars":{"rounds":"0"},"note":"Phase two starts. slow restarts at slot 0 and fast stays at the meeting point, slot 4."}]
    while s!=f:
        s=a[s]; f=a[f]; r+=1
        st.append({"at":{"slow":s,"fast":f},"vars":{"rounds":str(r)},"note":f"Round {r}: both pointers move one link, to slots {s} and {f}."+(f" They meet at slot {s}, the repeated value." if s==f else "")})
    assert s==2 and r==3
    return block(a,["slow","fast"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
