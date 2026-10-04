from common import *
CH='04-hash-maps-and-sets'
def run(s,t,ph,expect):
    f={};r={}; st=[{"at":{"i":-1},"vars":{"forward":"{}","reverse":"{}"},"note":"Start: both maps are empty."}]; ans=True
    V=lambda d:"{"+", ".join(f"{k}:{v}" for k,v in d.items())+"}"
    for i,(a,b) in enumerate(zip(s,t)):
        if (a in f and f[a]!=b):
            st.append({"at":{"i":i},"vars":{"pair":f"{a}/{b}","forward":V(f),"reverse":V(r)},"note":f"Source letter {a} is already paired with {f[a]}, not {b}. One letter would split, so return false."}); ans=False; break
        if (b in r and r[b]!=a):
            st.append({"at":{"i":i},"vars":{"pair":f"{a}/{b}","forward":V(f),"reverse":V(r)},"note":f"Target letter {b} already comes from {r[b]}, not {a}. Two letters would merge, so return false."}); ans=False; break
        new=a not in f
        f[a]=b; r[b]=a
        st.append({"at":{"i":i},"vars":{"pair":f"{a}/{b}","forward":V(f),"reverse":V(r)},"note":(f"Both letters are new. Store {a} with {b} in both maps." if new else f"The stored pairing {a} with {b} matches. Nothing changes.")})
    if ans: st.append({"at":{"i":len(s)},"vars":{"forward":V(f),"reverse":V(r)},"note":"The scan ends with no conflict, so return true."})
    assert ans==expect
    fill(CH,'91-strings-and-maps.md',block([f"{a}/{b}" for a,b in zip(s,t)],["i"],st),ph)
run("egg","add","@@TRACE1@@",True)
run("badc","baba","@@TRACE2@@",False)
