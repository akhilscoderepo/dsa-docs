from common import *
CH='36-stateful-containers-and-histories'; F='01-operation-traces.md'
LIMIT=2
def run(naive):
    count=0; cells=["new(2)"]; st=[{"at":{"call":0},"vars":{"count":0,"result":"null"},"note":"Call 0: the constructor sets limit to 2 and count to 0, which is a legal state."}]
    calls=["inc","inc","inc","value"] if naive else ["inc","inc","inc","value","reset","inc","value"]
    for idx,c in enumerate(calls,1):
        cells.append(c if c!="value" else "value")
        if c=="inc":
            before=count
            if naive:
                count+=1; res=count<=LIMIT
                if res: note=f"Call {idx}: count counts first, goes from {before} to {count}, and the call returns true. The state satisfies 0 <= count <= 2."
                else: note=f"Call {idx}: count goes from {before} to {count} before the check, and the call returns false. The return value is right, but count {count} exceeds limit 2, so the state is illegal."
            else:
                if count==LIMIT:
                    res=False; note=f"Call {idx}: count equals limit 2, so the counter rejects the call, returns false and leaves count at {count}. The state is identical to the state before the call."
                else:
                    count+=1; res=True; note=f"Call {idx}: count {before} is below limit 2, so the counter accepts the call, raises count to {count} and returns true."
            r="true" if res else "false"
        elif c=="value":
            r=str(count)
            note=f"Call {idx}: value returns {count}."+(" The specification expects 2, so the earlier damage becomes visible here." if naive else " This matches the specification.")
        else:
            count=0; r="null"; note=f"Call {idx}: reset sets count to 0, which is legal for every limit."
        st.append({"at":{"call":idx},"vars":{"count":count,"result":r},"note":note})
    return cells,st,count
cells,st,count=run(False)
assert count==1 and st[4]["vars"]["result"]=="2" and st[3]["vars"]["result"]=="false" and st[3]["vars"]["count"]==2
fill(CH,F,block(cells,["call"],st),"@@TRACE1@@")
cells,st,count=run(True)
assert count==3 and st[3]["vars"]["result"]=="false" and st[4]["vars"]["result"]=="3"
fill(CH,F,block(cells,["call"],st),"@@TRACE2@@")
