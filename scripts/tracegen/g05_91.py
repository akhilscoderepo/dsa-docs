from common import *
CH='05-sorting-and-java-comparators'; N='91-strings-maps-and-sorting.md'
W=["rat","tar","tab","art","bat"]; m={}
st=[{"at":{"i":-1},"vars":{"groups":"{}"},"note":"Start: the group map is empty."}]
fmt=lambda m:"{"+", ".join(f"{k}={v}" for k,v in m.items()).replace("'","")+"}"
for i,w in enumerate(W):
    k="".join(sorted(w)); new=k not in m; m.setdefault(k,[]).append(w)
    st.append({"at":{"i":i},"vars":{"word":w,"key":k,"groups":fmt({a:"["+", ".join(b)+"]" for a,b in m.items()})},"note":(f"The key {k} is new, so the map gets a list with {w}." if new else f"The key {k} exists, so {w} joins its list.")})
st.append({"at":{"i":len(W)},"vars":{"groups":fmt({a:"["+", ".join(b)+"]" for a,b in m.items()})},"note":"The loop ends. The map holds two keys and five words."})
assert m=={"art":["rat","tar","art"],"abt":["tab","bat"]}
fill(CH,N,block(W,["i"],st),"@@TRACE1@@")
a=list("tea"); cells=list("tea")
st=[{"at":{"i":0,"j":-1},"vars":{"chars":"".join(a)},"note":"Start: the character at index 0 is a sorted prefix of length 1."}]
for i in range(1,3):
    j=i
    while j>0:
        if a[j]<a[j-1]:
            st.append({"at":{"i":i,"j":j-1},"vars":{"chars":"".join(a)},"note":f"The character {a[j]} is smaller than {a[j-1]}. Swap them."})
            a[j],a[j-1]=a[j-1],a[j]; j-=1
        else:
            st.append({"at":{"i":i,"j":j-1},"vars":{"chars":"".join(a)},"note":f"The character {a[j]} is not smaller than {a[j-1]}. This insertion stops."}); break
st.append({"at":{"i":3,"j":-1},"vars":{"key":"".join(a)},"note":"The characters are sorted, so the key of tea is "+"".join(a)+"."})
assert "".join(a)=="aet"
fill(CH,N,block(cells,["i","j"],st),"@@TRACE2@@")
