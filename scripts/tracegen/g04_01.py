from common import *
CH='04-hash-maps-and-sets'
F=lambda s:"{"+", ".join(map(str,s))+"}"
def run(nums, ph):
    seen=[]; st=[{"at":{"i":-1},"vars":{"seen":"{}"},"note":"Start: the seen set is empty."}]; ans=False
    for i,x in enumerate(nums):
        if x in seen:
            st.append({"at":{"i":i},"vars":{"value":x,"seen":F(seen)},"note":f"Value {x} is already in the seen set, so the method returns true."}); ans=True; break
        seen.append(x)
        st.append({"at":{"i":i},"vars":{"value":x,"seen":F(seen)},"note":f"Value {x} is not in the seen set. Store it."})
    if not ans: st.append({"at":{"i":len(nums)},"vars":{"seen":F(seen)},"note":"The loop ends with no repeat, so the method returns false."})
    fill(CH,'01-membership-sets.md',block(nums,["i"],st),ph); return ans
assert run([4,7,1,7,9],"@@TRACE1@@") is True
assert run([3,1,4,2],"@@TRACE2@@") is False
