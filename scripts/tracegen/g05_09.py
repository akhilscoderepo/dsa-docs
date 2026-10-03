from common import *
from collections import Counter
CH='05-sorting-and-java-comparators'
F='09-strings-maps-and-sorting.md'
words=["stop","pots","opts","cat","act","dog","tops"]
piles={}; st=[]
for i,w in enumerate(words):
    k="".join(sorted(w)); new=k not in piles
    piles.setdefault(k,[]).append(w)
    desc="; ".join(f"{kk}: {' '.join(v)}" for kk,v in piles.items())
    note=(f"{w} sorts to {k}, a key not seen before, so a new pile starts." if new else f"{w} sorts to {k}, which already names a pile, so it joins {' '.join(piles[k][:-1])}.")
    st.append({"at":{"i":i},"vars":{"word":w,"key":k,"piles":len(piles)},"note":note+f" There are {len(piles)} piles."})
assert list(piles.values())==[["stop","pots","opts","tops"],["cat","act"],["dog"]]
assert "joins stop pots opts" in st[6]["note"]
fill(CH,F,block(words,["i"],st),"@@TRACE1@@")
a,b="cabbba","abbccc"
ca,cb=Counter(a),Counter(b); st=[]
for i,ch in enumerate("abc"):
    st.append({"at":{"i":i},"vars":{"letter":ch,"countInFirst":ca[ch],"countInSecond":cb[ch]},"note":f"The letter {ch} occurs {ca[ch]} times in the first word and {cb[ch]} times in the second. It is present in both."})
sa,sb=sorted(ca.values()),sorted(cb.values())
assert set(ca)==set(cb) and sa==sb==[1,2,3]
st.append({"at":{"i":3},"vars":{"sortedCountsFirst":"1,2,3","sortedCountsSecond":"1,2,3","verdict":"close"},"note":"The letter sets are equal and the sorted counts are 1, 2, 3 on both sides, so the strings are close even though no single letter has the same count in both."})
fill(CH,F,block(list("abc"),["i"],st),"@@TRACE2@@")
