from common import *
CH='04-hash-maps-and-sets'
nums=[50,12,13,49,11,51,52,14]; al=set(nums); st=[]; best=(0,0)
for i,x in enumerate(nums):
    if x-1 in al:
        st.append({"at":{"i":i},"vars":{"value":x,"start":"no","best":str(list(best))},"note":f"Value {x}: {x-1} is in the set, so {x} is inside a chain. Skip it."})
    else:
        ln=1
        while x+ln in al: ln+=1
        if ln>best[1] or (ln==best[1] and x<best[0]): best=(x,ln)
        st.append({"at":{"i":i},"vars":{"value":x,"start":"yes","best":str(list(best))},"note":f"Value {x}: {x-1} is missing, so {x} starts a chain. Walking upward finds length {ln}. Best so far: start {best[0]}, length {best[1]}."})
assert best==(11,4)
fill(CH,'05-set-sequences.md',block(nums,["i"],st),"@@TRACE1@@")
pending={1,3,7}; b=[7,3,3,5,1,7]; out=[]; st=[]
F=lambda s:"{"+", ".join(map(str,sorted(s)))+"}"
for i,y in enumerate(b):
    if y in pending:
        pending.remove(y); out.append(y)
        st.append({"at":{"i":i},"vars":{"value":y,"pending":F(pending),"output":str(out)},"note":f"Value {y} is in the set, so report it and remove it. Output: {out}."})
    else:
        st.append({"at":{"i":i},"vars":{"value":y,"pending":F(pending),"output":str(out)},"note":f"Value {y} is not in the set, so skip it. Output: {out}."})
assert out==[7,3,1]
fill(CH,'05-set-sequences.md',block(b,["i"],st),"@@TRACE2@@")
