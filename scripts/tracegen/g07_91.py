from common import *
CH='07-prefix-sums-and-difference-arrays'
F='91-prefix-state-maps.md'
def ending(a,k,ph):
    seen={0:1}; cur=0; out=[]
    def m(): return "{"+", ".join(f"{x}={c}" for x,c in sorted(seen.items()))+"}"
    st=[{"at":{"i":-1},"vars":{"seen":m(),"out":"[]"},"note":"The map starts with the total 0 once, for boundary 0."}]
    for i,v in enumerate(a):
        cur+=v; hit=seen.get(cur-k,0); out.append(hit); seen[cur]=seen.get(cur,0)+1
        st.append({"at":{"i":i},"vars":{"cur":str(cur),"partner":str(cur-k),"seen":m(),"out":str(out)},"note":f"Total {cur} has partner {cur-k}, which occurs {hit} time{'s' if hit!=1 else ''}. So {hit} window{'s' if hit!=1 else ''} end at index {i}."})
    fill(CH,F,block(a,["i"],st),ph); return out
assert ending([3,1,0,4,-4,4],4,"@@TRACE1@@")==[0,1,1,2,1,3]
def cong(a,k,r,ph):
    seen={0:1}; cur=0; cnt=0
    def m(): return "{"+", ".join(f"{x}={c}" for x,c in sorted(seen.items()))+"}"
    st=[{"at":{"i":-1},"vars":{"seen":m(),"count":"0"},"note":"The map starts with class 0 once, for boundary 0."}]
    for i,v in enumerate(a):
        cur+=v; s=cur%k; p=(cur-r)%k; hit=seen.get(p,0); cnt+=hit; seen[s]=seen.get(s,0)+1
        st.append({"at":{"i":i},"vars":{"cur":str(cur),"state":str(s),"partner":str(p),"seen":m(),"count":str(cnt)},"note":f"Total {cur} has class {s} and partner class {p}. The partner occurs {hit} time{'s' if hit!=1 else ''}, so the count becomes {cnt}."})
    fill(CH,F,block(a,["i"],st),ph); return cnt
assert cong([2,-1,3,-3,4],3,1,"@@TRACE2@@")==6
