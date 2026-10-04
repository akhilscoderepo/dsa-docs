from common import *
CH='01-arrays-core-operations'; F='01-direct-scans.md'
# Trace 1: first match with early return.
nums=[5,2,7,9,9,4]; target=9; st=[]; res=-1
for i,x in enumerate(nums):
    if x==target:
        res=i
        st.append({"at":{"i":i},"vars":{"target":target,"result":res},"note":f"i = {i}: {x} equals {target}, so the scan returns {i} and never reads the later 9."})
        break
    st.append({"at":{"i":i},"vars":{"target":target,"result":-1},"note":f"i = {i}: {x} differs from {target}, so the scan moves on."})
assert res==3
fill(CH,F,block(nums,["i"],st),"@@TRACE1@@")
# Trace 2: absent target, the loop ends.
nums=[3,8,1,6]; target=5; st=[]
for i,x in enumerate(nums):
    st.append({"at":{"i":i},"vars":{"target":target,"result":-1},"note":f"i = {i}: {x} differs from {target}, so the scan moves on."})
st.append({"at":{"i":len(nums)},"vars":{"target":target,"result":-1},"note":"i = 4 equals nums.length, so every position was examined. The method returns -1."})
assert len(st)==5
fill(CH,F,block(nums,["i"],st),"@@TRACE2@@")
