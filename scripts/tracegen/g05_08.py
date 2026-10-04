from common import *
CH='05-sorting-and-java-comparators'; N='08-sort-then-scan.md'
def run(vals,ph,tail):
    s=sorted(vals); n=len(s); rank=1
    st=[{"at":{"i":n-1},"vars":{"value":s[-1],"rank":1},"note":f"Start at the last index. The value {s[-1]} is the largest, so the rank is 1."}]
    ans=None
    for i in range(n-2,-1,-1):
        if s[i]!=s[i+1]:
            rank+=1
            st.append({"at":{"i":i},"vars":{"value":s[i],"rank":rank},"note":f"The value {s[i]} differs from its right neighbor {s[i+1]}, so the rank becomes {rank}."+(" The rank is 3, so the scan returns this value." if rank==3 else "")})
            if rank==3: ans=s[i]; break
        else:
            st.append({"at":{"i":i},"vars":{"value":s[i],"rank":rank},"note":f"The value {s[i]} equals its right neighbor, so the rank stays {rank}."})
    if ans is None:
        ans=s[-1]; st.append({"at":{"i":-1},"vars":{"rank":rank},"note":tail})
    fill(CH,N,block(s,["i"],st),ph); return ans
assert run([2,9,9,4,7],"@@TRACE1@@","")==4
assert run([8,8],"@@TRACE2@@","The loop ends with rank 1, below 3, so the method returns the fallback, the largest value 8.")==8
