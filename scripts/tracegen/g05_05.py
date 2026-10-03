from common import *
CH='05-sorting-and-java-comparators'
F='05-stability-and-ties.md'
ents=[("ann",3),("bob",1),("cy",3),("di",1),("eve",2)]
arr=[]; st=[]
for i,e in enumerate(ents):
    j=len(arr)
    while j>0 and arr[j-1][1]>e[1]: j-=1
    arr.insert(j,e)
    pref=", ".join(f"{n} {s}" for n,s in arr)
    eq=[x for x in arr if x[1]==e[1] and x is not e]
    why=f"It has the same score as {eq[-1][0]}, so it goes right after it and arrival order is kept." if eq else "No earlier entry has the same score, so only the scores decide."
    st.append({"at":{"i":i},"vars":{"insert":f"{e[0]} {e[1]}","list":pref},"note":f"Insert {e[0]} with score {e[1]}. {why} The list reads {pref}."})
assert [a[0] for a in arr]==["bob","di","eve","ann","cy"]
assert "same score as ann" in st[2]["note"]
fill(CH,F,block([f"{n} {s}" for n,s in ents],["i"],st),"@@TRACE1@@")
nums=[5,3,8,1,6]
bc=lambda x:bin(x).count("1")
arr=[]; st=[]
for i,x in enumerate(nums):
    j=len(arr)
    while j>0 and (bc(arr[j-1]),arr[j-1])>(bc(x),x): j-=1
    arr.insert(j,x)
    pref=", ".join(f"{bc(a)}/{a}" for a in arr)
    st.append({"at":{"i":i},"vars":{"insert":f"{bc(x)}/{x}","order":pref},"note":f"Insert {x}, which has {bc(x)} one-bits. The key is {bc(x)} over {x}. The order reads {pref}."})
assert arr==[1,8,3,5,6]
fill(CH,F,block([str(n) for n in nums],["i"],st),"@@TRACE2@@")
