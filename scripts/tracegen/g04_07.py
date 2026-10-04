from common import *
CH='04-hash-maps-and-sets'
def run(cells, idx, label, ph, lo=None):
    tbl={}; st=[{"at":{"i":-1},"vars":{"slots":"{}"},"note":"Start: every slot holds 0."}]
    for i,c in enumerate(cells):
        s=idx(c); tbl[s]=tbl.get(s,0)+1
        view="{"+", ".join(f"{k}: {v}" for k,v in sorted(tbl.items()))+"}"
        st.append({"at":{"i":i},"vars":{"key":c,"slot":s,"slots":view},"note":f"Key {c} maps to slot {s}, which now holds {tbl[s]}."})
    fill(CH,'07-direct-addressing.md',block(cells,["i"],st),ph); return tbl
t=run(list("dbdad"),lambda c:ord(c)-ord('a'),"letters","@@TRACE1@@")
assert t=={3:3,1:1,0:1}
t=run([103,101,103,105,101,103],lambda v:v-100,"codes","@@TRACE2@@")
assert t=={3:3,1:2,5:1}
