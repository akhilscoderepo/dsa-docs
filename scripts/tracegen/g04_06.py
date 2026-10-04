from common import *
CH='04-hash-maps-and-sets'
def run(pairs,ph,expect,norm=False):
    cnt={}; st=[{"at":{"i":-1},"vars":{"counts":"{}"},"note":"Start: the map is empty."}]
    for i,(a,b) in enumerate(pairs):
        k=(min(a,b),max(a,b)) if norm else (a,b)
        new=k not in cnt; cnt[k]=cnt.get(k,0)+1
        s="{"+", ".join(f"({x},{y}): {c}" for (x,y),c in cnt.items())+"}"
        if norm:
            note=f"Pair ({a}, {b}) becomes the key ({k[0]}, {k[1]})." + (" The key is new, so create its entry." if new else f" The entry exists, so its count rises to {cnt[k]}.")
        else:
            note=f"Order ({a}, {b})." + (" The key is new, so create its entry." if new else f" A new Point equals the stored key, so its count rises to {cnt[k]}.")
        st.append({"at":{"i":i},"vars":{"key":f"({k[0]},{k[1]})","counts":s},"note":note})
    assert max(cnt.values())==expect
    fill(CH,'06-key-equality.md',block([f"({a},{b})" for a,b in pairs],["i"],st),ph)
run([(1,2),(0,0),(1,2),(2,1),(1,2)],"@@TRACE1@@",3)
run([(3,1),(1,3),(2,5),(5,2),(3,1)],"@@TRACE2@@",3,True)
