from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(a,ph):
    first={0:-1}; bal=0; best=0
    def m(): return "{"+", ".join(f"{x}@{c}" for x,c in first.items())+"}"
    st=[{"at":{"i":-1},"vars":{"first":m(),"best":"0"},"note":"The map starts with balance 0 at index -1, the position before the first value."}]
    for i,v in enumerate(a):
        bal+=1 if v==1 else -1
        if bal in first:
            L=i-first[bal]; best=max(best,L)
            note=f"Balance {bal} appeared at index {first[bal]}, so the span has length {i}-({first[bal]}) = {L}. The best length is {best}."
        else:
            first[bal]=i; note=f"Balance {bal} is new, so the map stores it at index {i}."
        st.append({"at":{"i":i},"vars":{"bal":str(bal),"first":m(),"best":str(best)},"note":note})
    fill(CH,'05-earliest-balance.md',block(a,["i"],st),ph); return best
assert run([0,0,1,0,0,0,1,1],"@@TRACE1@@")==6
assert run([1,0],"@@TRACE2@@")==2
