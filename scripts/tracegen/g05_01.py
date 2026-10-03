from common import *
CH='05-sorting-and-java-comparators'
MIN,MAX=-2**31,2**31-1
def wrap(x): return (x+2**31)%2**32-2**31
cells=["MIN","0","MAX"]; vals={"MIN":MIN,"0":0,"MAX":MAX}
sgn=lambda x:(x>0)-(x<0)
st=[]
for i,(a,b) in enumerate([("MIN","MAX"),("MIN","0"),("0","MAX")]):
    x,y=vals[a],vals[b]
    sub=sgn(wrap(x-y)); cmp=sgn(x-y)
    note=f"Compare {a} with {b}. Subtraction gives sign {sub:+d} and Integer.compare gives {cmp:+d}."
    if sub!=cmp: note+=" They disagree: the difference wrapped around, so the subtraction comparator would put them in the wrong order."
    else: note+=" They agree, since this difference fits in 32 bits."
    st.append({"at":{"i":i},"vars":{"pair":f"{a},{b}","bySubtraction":sub,"byCompare":cmp},"note":note})
assert sgn(wrap(MIN-MAX))==1 and sgn(MIN-MAX)==-1
fill(CH,'01-ordering-contracts.md',block(cells,["i"],st),"@@TRACE1@@")
# trace 2: insertion sort by concatenation order
parts=["3","30","34","5","9"]
before=lambda x,y:(x+y)>(y+x)  # x goes before y
arr=[]; st=[]
for i,p in enumerate(parts):
    j=len(arr)
    notes=[]
    while j>0 and before(p,arr[j-1]):
        notes.append(f"{p}{arr[j-1]} = {int(p+arr[j-1])} beats {arr[j-1]}{p} = {int(arr[j-1]+p)}, so {p} moves ahead of {arr[j-1]}")
        j-=1
    if j>0 and not notes: notes.append(f"{arr[j-1]}{p} = {int(arr[j-1]+p)} is at least {p}{arr[j-1]} = {int(p+arr[j-1])}, so {p} stays behind {arr[j-1]}")
    elif j>0: notes.append(f"{arr[j-1]}{p} = {int(arr[j-1]+p)} is at least {p}{arr[j-1]} = {int(p+arr[j-1])}, so it stops there")
    arr.insert(j,p)
    first = "It is the first element, so the prefix is just itself." if not notes else "; ".join(notes)+"."
    st.append({"at":{"i":i},"vars":{"insert":p,"sortedPrefix":",".join(arr)},"note":f"Insert {p}. {first} The prefix is now {', '.join(arr)}."})
assert arr==["9","5","34","3","30"] and "".join(arr)=="9534330"
fill(CH,'01-ordering-contracts.md',block(parts,["i"],st),"@@TRACE2@@")
