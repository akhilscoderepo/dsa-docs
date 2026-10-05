from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(n,ups,ph):
    d=[0]*(n+1)
    for l,r,v in ups: d[l]+=v; d[r+1]-=v
    cur=0; tot=[]
    st=[{"at":{"i":-1},"vars":{"cur":"0"},"note":"The deltas are written. The pass starts with cur = 0 before index 0."}]
    for i in range(n):
        cur+=d[i]; tot.append(cur)
        st.append({"at":{"i":i},"vars":{"diff[i]":str(d[i]),"cur":str(cur),"total":str(tot)},"note":f"Add the delta {d[i]} to cur, which gives the total {cur} for index {i}."})
    st.append({"at":{"i":n},"vars":{"diff[n]":str(d[n])},"note":f"Index {n} is the extra slot. It holds {d[n]} and the pass never reads it."})
    fill(CH,'08-difference-arrays.md',block(d,["i"],st),ph); return tot
assert run(6,[(1,3,2),(2,4,3)],"@@TRACE1@@")==[0,2,5,5,3,0]
assert run(6,[(3,5,4)],"@@TRACE2@@")==[0,0,0,4,4,4]
