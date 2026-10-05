from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(a,ph):
    n=len(a); out=[0]*n; run_=1
    st=[{"at":{"i":-1},"vars":{"running":"1"},"note":"The left pass starts with running = 1, the product of no values."}]
    for i in range(n):
        out[i]=run_; run_*=a[i]
        st.append({"at":{"i":i},"vars":{"out":str(out),"running":str(run_)},"note":f"Store the product before index {i} and multiply running by {a[i]}."})
    suf=1
    st.append({"at":{"i":n},"vars":{"out":str(out),"suffix":"1"},"note":"The right pass starts past the last index with suffix = 1."})
    for i in range(n-1,-1,-1):
        out[i]*=suf; suf*=a[i]
        st.append({"at":{"i":i},"vars":{"out":str(out),"suffix":str(suf)},"note":f"Multiply out[{i}] by the product after it, then multiply suffix by {a[i]}."})
    fill(CH,'03-exclusion-state.md',block(a,["i"],st),ph); return out
assert run([2,3,4,5],"@@TRACE1@@")==[60,40,30,24]
assert run([1,0,3,4],"@@TRACE2@@")==[0,12,0,0]
