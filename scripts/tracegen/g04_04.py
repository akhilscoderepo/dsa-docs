from common import *
CH='04-hash-maps-and-sets'
def run(jobs,m,ph,expect):
    g={}; st=[{"at":{"i":-1},"vars":{"groups":"{}"},"note":"Start: the grouping map is empty."}]
    for i,x in enumerate(jobs):
        k=x%m; new=k not in g
        g.setdefault(k,[]).append(x)
        s="{"+", ".join(f"{a}: {b}" for a,b in g.items())+"}"
        st.append({"at":{"i":i},"vars":{"job":x,"key":k,"groups":s},"note":(f"Job {x} has key {k}, which has no bucket yet. Create the bucket and add the job." if new else f"Job {x} has key {k}. Append it to the existing bucket.")})
    assert [v for v in g.values()]==expect
    fill(CH,'04-grouping-maps.md',block(jobs,["i"],st),ph)
run([7,-1,4,2,10,5],3,"@@TRACE1@@",[[7,4,10],[-1,2,5]])
run([8,3,12,5,4],4,"@@TRACE2@@",[[8,12,4],[3],[5]])
