from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(a,k,ph):
    freq={0:1}; cur=0; cnt=0
    def m(): return "{"+", ".join(f"{x}={c}" for x,c in sorted(freq.items()))+"}"
    st=[{"at":{"i":-1},"vars":{"freq":m(),"count":"0"},"note":"Class 0 starts with one boundary, boundary 0 with prefix 0."}]
    for i,v in enumerate(a):
        cur+=v; cls=cur%k  # python mod = floorMod
        raw=int(cur-k*int(cur/k))
        hit=freq.get(cls,0); cnt+=hit
        note=f"Prefix {cur} has class {cls}. {hit} earlier boundar{'y' if hit==1 else 'ies'} share it, so the count becomes {cnt}."
        freq[cls]=hit+1
        vs={"cur":str(cur),"class":str(cls),"freq":m(),"count":str(cnt)}
        if raw!=cls: vs["cur % k"]=str(raw)
        st.append({"at":{"i":i},"vars":vs,"note":note})
    fill(CH,'06-remainder-classes.md',block(a,["i"],st),ph); return cnt
assert run([3,-1,2,4,-6,1],4,"@@TRACE1@@")==5
assert run([-3,-2],5,"@@TRACE2@@")==1
