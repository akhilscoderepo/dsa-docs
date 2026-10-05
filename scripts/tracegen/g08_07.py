from common import *
CH='08-two-pointers'; F='07-array-cycle-state.md'
def go(a,ph,entry):
    s=f=0; st=[]; rnd=0
    while True:
        s=a[s]; f=a[a[f]]; rnd+=1
        st.append({"at":{"slow":s,"fast":f},"vars":{"phase":"1","round":str(rnd)},"note":f"Phase one, round {rnd}: slow moves one step to index {s} and fast moves two steps to index {f}."+(" The pointers meet." if s==f else "")})
        if s==f: break
    meet=s; s=0; rnd=0
    st.append({"at":{"slow":s,"fast":f},"vars":{"phase":"2","round":"0"},"note":f"Phase two starts: slow returns to index 0 and fast stays at the meeting index {f}."})
    while s!=f:
        s=a[s]; f=a[f]; rnd+=1
        st.append({"at":{"slow":s,"fast":f},"vars":{"phase":"2","round":str(rnd)},"note":f"Phase two, round {rnd}: both pointers move one step, slow to index {s} and fast to index {f}."+(f" They meet at index {s}, the repeated value." if s==f else "")})
    assert s==entry
    fill(CH,F,block(list(a),["slow","fast"],st),ph)
go([3,1,3,4,2],"@@TRACE1@@",3); go([1,3,4,2,2],"@@TRACE2@@",2)
