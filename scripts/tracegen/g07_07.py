from common import *
CH='07-prefix-sums-and-difference-arrays'
def q(a,l,r,ph):
    px=[0]
    for v in a: px.append(px[-1]^v)
    st=[{"at":{"left":-1,"end":-1},"vars":{"query":f"[{l}, {r}]"},"note":f"The prefix XOR array is ready. The query asks for index {l} through index {r}, so the reads are px[{r+1}] and px[{l}]."},
        {"at":{"left":-1,"end":r+1},"vars":{"px[end]":str(px[r+1])},"note":f"Read px[{r+1}] = {px[r+1]}, the XOR of the first {r+1} values."},
        {"at":{"left":l,"end":r+1},"vars":{"px[end]":str(px[r+1]),"px[left]":str(px[l])},"note":f"Read px[{l}] = {px[l]}, the XOR of the first {l} values."},
        {"at":{"left":l,"end":r+1},"vars":{"answer":f"{px[r+1]} ^ {px[l]} = {px[r+1]^px[l]}"},"note":f"The first {l} values meet twice and cancel, so the answer is {px[r+1]^px[l]}."}]
    fill(CH,'07-prefix-xor.md',block(px,["left","end"],st),ph); return px[r+1]^px[l]
assert q([5,1,7,2,6],1,3,"@@TRACE1@@")==4
def cnt(a,k,ph):
    seen={0:1}; cur=0; c=0
    def m(): return "{"+", ".join(f"{x}={n}" for x,n in sorted(seen.items()))+"}"
    st=[{"at":{"i":-1},"vars":{"seen":m(),"count":"0"},"note":"The map starts with prefix XOR 0 once, for boundary 0."}]
    for i,v in enumerate(a):
        cur^=v; key=cur^k; hit=seen.get(key,0); c+=hit
        note=f"Prefix XOR is {cur}. The key {cur} ^ {k} = {key} occurs {hit} time{'s' if hit!=1 else ''} before, so the count becomes {c}."
        seen[cur]=seen.get(cur,0)+1
        st.append({"at":{"i":i},"vars":{"cur":str(cur),"look up":str(key),"seen":m(),"count":str(c)},"note":note})
    fill(CH,'07-prefix-xor.md',block(a,["i"],st),ph); return c
assert cnt([4,2,2,6,4],6,"@@TRACE2@@")==4
