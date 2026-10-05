from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(a,k,ph):
    seen={0:1}; cur=0; cnt=0
    st=[{"at":{"i":-1},"vars":{"seen":"{0=1}","count":"0"},"note":"The map starts with the seed: prefix 0 occurs once, for boundary 0."}]
    def m(): return "{"+", ".join(f"{x}={c}" for x,c in seen.items())+"}"
    for i,v in enumerate(a):
        cur+=v; hit=seen.get(cur-k,0); cnt+=hit
        note=f"Prefix is {cur}. The key {cur-k} occurs {hit} time{'s' if hit!=1 else ''} before, so the count becomes {cnt}. Then the map records {cur}."
        seen[cur]=seen.get(cur,0)+1
        st.append({"at":{"i":i},"vars":{"cur":str(cur),"look up":str(cur-k),"seen":m(),"count":str(cnt)},"note":note})
    fill(CH,'04-prefix-counts.md',block(a,["i"],st),ph); return cnt
assert run([3,4,7,2,-3,1,4,2],7,"@@TRACE1@@")==4
assert run([0,0,0],0,"@@TRACE2@@")==6
