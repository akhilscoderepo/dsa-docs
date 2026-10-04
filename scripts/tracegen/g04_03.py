from common import *
CH='04-hash-maps-and-sets'
M=lambda d: "{"+", ".join(f"{k}@{v}" for k,v in d.items())+"}" if d else "{}"
nums=[8,2,11,3]; target=14; at={}; st=[]; ans=None
for i,x in enumerate(nums):
    c=target-x
    if c in at:
        st.append({"at":{"i":i},"vars":{"value":x,"complement":c,"map":M(at)},"note":f"Value {x}, complement {c}. The map holds {c} at position {at[c]}, so the answer is [{at[c]}, {i}]."}); ans=[at[c],i]; break
    st.append({"at":{"i":i},"vars":{"value":x,"complement":c,"map":M(at)},"note":f"Value {x}, complement {c}, which is missing from the map. Store {x} at position {i}."})
    at[x]=i
assert ans==[2,3]
fill(CH,'03-key-to-index-maps.md',block(nums,["i"],st),"@@TRACE1@@")
nums=[5,1,5,5]; k=1; last={}; st=[]; ans=False
for i,x in enumerate(nums):
    if x in last:
        gap=i-last[x]
        if gap<=k:
            st.append({"at":{"i":i},"vars":{"value":x,"gap":gap,"map":M(last)},"note":f"Value {x} was last seen at {last[x]}, a gap of {gap}, which is within {k}. Return true."}); ans=True; break
        st.append({"at":{"i":i},"vars":{"value":x,"gap":gap,"map":M(last)},"note":f"Value {x} was last seen at {last[x]}, a gap of {gap}, which is too wide. Overwrite its entry with {i}."})
    else:
        st.append({"at":{"i":i},"vars":{"value":x,"gap":"none","map":M(last)},"note":f"Value {x} is new. Store it at position {i}."})
    last[x]=i
assert ans
fill(CH,'03-key-to-index-maps.md',block(nums,["i"],st),"@@TRACE2@@")
