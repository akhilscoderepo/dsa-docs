from common import *
CH='39-dynamic-query-structures'; F='04-deferred-transforms.md'
M=10**9+7
def run(ops, ncells):
    raw=[]; mul=1; add=0; st=[]; truth=[]; res=[]
    for o,a in ops:
        ptr=-1; result=""
        if o=='a':
            x=(a-add)*pow(mul,M-2,M)%M; raw.append(x); truth.append(a); ptr=len(raw)-1
            note=f"append({a}) stores raw value ({a} - {add}) * inverse({mul}) = {x}, so that {x} * {mul} + {add} reads back as {a}."
        elif o=='+':
            add=(add+a)%M; truth=[(v+a)%M for v in truth]
            note=f"addAll({a}) changes only the addend, which becomes {add}. No entry is touched."
        elif o=='*':
            mul=mul*a%M; add=add*a%M; truth=[v*a%M for v in truth]
            note=f"multAll({a}) multiplies both parts of the pair, so mul = {mul} and add = {add}. No entry is touched."
        else:
            ptr=a
            if a<len(raw):
                v=(raw[a]*mul+add)%M; assert v==truth[a]; res.append(v); result=str(v)
                note=f"get({a}) computes {raw[a]} * {mul} + {add} mod M = {v}, which matches the naive loop."
            else:
                res.append(-1); result="-1"
                note=f"get({a}) is at or beyond the size {len(raw)}, so it returns -1."
        st.append({"at":{"i":ptr},"vars":{"mul":mul,"add":add,"raw":",".join(map(str,raw)) or "empty","result":result},"note":note})
    return st,res
st,res=run([('a',2),('+',3),('a',7),('*',2),('g',0),('g',1),('g',2)],3)
assert res==[10,14,-1]
fill(CH,F,block(["0","1","2"],["i"],st),"@@TRACE1@@")
st,res=run([('a',5)]+[('*',100)]*6+[('a',9),('g',0),('g',1)],2)
assert res==[999965007,9]
fill(CH,F,block(["0","1"],["i"],st),"@@TRACE2@@")
