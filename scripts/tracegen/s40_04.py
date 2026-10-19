from common import *
CH='40-composite-indexes-and-allocation'; F='04-frequency-buckets.md'
def run(calls):
    cnt={}; cells=[f"{o}({k})" for o,k in calls]; st=[]
    for n,(o,k) in enumerate(calls):
        c=cnt.get(k,0)
        if o=="inc":
            cnt[k]=c+1
            note=f"Call {n}: {k} moves from count {c} to count {c+1}."if c else f"Call {n}: {k} is new, so it enters bucket 1."
        else:
            if c==1: del cnt[k]; note=f"Call {n}: {k} drops from count 1 to 0, so it leaves the counter."
            else: cnt[k]=c-1; note=f"Call {n}: {k} moves from count {c} to count {c-1}."
        b={}
        for key,v in cnt.items(): b.setdefault(v,[]).append(key)
        if c and (o=="inc" or c==1) and not any(v==c for v in cnt.values()): note+=f" Bucket {c} is empty now, so the call removes it."
        elif c and o=="dec" and c>1 and not any(v==c for v in cnt.values()): note+=f" Bucket {c} is empty now, so the call removes it."
        view=" ".join(f"{v}:{{{','.join(sorted(b[v]))}}}" for v in sorted(b)) or "empty"
        st.append({"at":{"call":n},"vars":{"buckets":view,"top":max(b) if b else 0},"note":note})
    return cells,st,cnt
c,s,cnt=run([("inc","a"),("inc","b"),("inc","b"),("inc","c"),("inc","b"),("inc","a")])
assert cnt=={"a":2,"b":3,"c":1}
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s,cnt=run([("inc","x"),("inc","y"),("inc","y"),("dec","y"),("dec","y"),("dec","x")])
assert cnt=={"y":0} or cnt=={}
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
