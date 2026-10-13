from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='03-reservoir-sampling.md'
def one(items,draws,ph,final):
    held=items[0]; st=[{"at":{"t":0},"vars":{"bound":"none","draw":"none","held":held},"note":f"Item {items[0]} enters without a draw. The held item is {held}."}]; di=iter(draws)
    for t in range(2,len(items)+1):
        d=next(di); x=items[t-1]
        if d==0: held=x; n=f"Bound {t}, draw {d}. The draw is 0, so {x} replaces the held item."
        else: n=f"Bound {t}, draw {d}. The draw is not 0, so the held item stays."
        st.append({"at":{"t":t-1},"vars":{"bound":t,"draw":d,"held":held},"note":n})
    assert held==final; fill(CH,N,block(items,["t"],st),ph)
def many(items,k,draws,ph,final):
    res=[]; st=[]; di=iter(draws)
    for t in range(1,len(items)+1):
        x=items[t-1]
        if t<=k: res.append(x); st.append({"at":{"t":t-1},"vars":{"bound":"none","draw":"none","reservoir":" ".join(res)},"note":f"Item {x} fills slot {t-1} without a draw."}); continue
        d=next(di)
        if d<k: res[d]=x; n=f"Bound {t}, draw {d}. The draw is below {k}, so {x} overwrites slot {d}."
        else: n=f"Bound {t}, draw {d}. The draw is not below {k}, so {x} is dropped."
        st.append({"at":{"t":t-1},"vars":{"bound":t,"draw":d,"reservoir":" ".join(res)},"note":n})
    assert res==final; fill(CH,N,block(items,["t"],st),ph)
one(list("ABCDE"),[1,0,2,0],"@@TRACE1@@","E")
many(list("PQRSTU"),2,[2,1,0,4],"@@TRACE2@@",["T","S"])
