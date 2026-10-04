from common import *
CH='04-hash-maps-and-sets'
M=lambda d: "{"+", ".join(f"{k}:{v}" for k,v in d.items())+"}" if d else "{}"
def run(codes, ph):
    cnt={}; st=[{"at":{"i":-1},"vars":{"count":"{}"},"note":"Start of the counting pass: the map is empty."}]
    for i,c in enumerate(codes):
        cnt[c]=cnt.get(c,0)+1
        st.append({"at":{"i":i},"vars":{"code":c,"count":M(cnt)},"note":f"Counting pass: code {c} now has count {cnt[c]}."})
    ans=-1
    for i,c in enumerate(codes):
        if cnt[c]==1:
            st.append({"at":{"i":i},"vars":{"code":c,"count":M(cnt)},"note":f"Scan pass: code {c} has count 1, so the method returns {i}."}); ans=i; break
        st.append({"at":{"i":i},"vars":{"code":c,"count":M(cnt)},"note":f"Scan pass: code {c} has count {cnt[c]}, so move on."})
    if ans==-1: st.append({"at":{"i":len(codes)},"vars":{"count":M(cnt)},"note":"The scan ends with no count of 1, so the method returns -1."})
    fill(CH,'02-frequency-maps.md',block(codes,["i"],st),ph); return ans
assert run([4,7,4,9,7,2],"@@TRACE1@@")==3
assert run([5,5,6,6],"@@TRACE2@@")==-1
