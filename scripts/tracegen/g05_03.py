from common import *
CH='05-sorting-and-java-comparators'
runs=[(52,4),(49,2),(52,1),(47,3)]
def cmp(a,b):
    if a[0]!=b[0]: return (-1 if a[0]<b[0] else 1),"time"
    return (-1 if a[1]<b[1] else (1 if a[1]>b[1] else 0)),"lane"
arr=[]; st=[]
for i,r in enumerate(runs):
    j=len(arr); notes=[]
    while j>0:
        s,key=cmp(r,arr[j-1])
        if s<0:
            notes.append(f"{r[0]}/{r[1]} against {arr[j-1][0]}/{arr[j-1][1]}: the {key} decides, so it moves ahead")
            j-=1
        else:
            notes.append(f"{r[0]}/{r[1]} against {arr[j-1][0]}/{arr[j-1][1]}: the {key} decides, so it stays behind")
            break
    arr.insert(j,r)
    txt="; ".join(notes)+"." if notes else "It is the first runner, so nothing is compared."
    pref=", ".join(f"{a}/{b}" for a,b in arr)
    st.append({"at":{"i":i},"vars":{"insert":f"{r[0]}/{r[1]}","sortedPrefix":pref},"note":f"Insert {r[0]}/{r[1]}. {txt} The list is now {pref}."})
assert arr==[(47,3),(49,2),(52,1),(52,4)]
# check the 52/1 against 52/4 step mentions lane
assert "the lane decides" in st[2]["note"]
fill(CH,'03-comparator-contracts.md',block([f"{a}/{b}" for a,b in runs],["i"],st),"@@TRACE1@@")
g=lambda x,y:(y+x)>(x+y)   # y+x larger means x goes after y ; compare(x,y)<0 when (y+x)<(x+y)
def before(x,y): return (x+y)>(y+x)
pairs=[("3","30"),("30","34"),("3","34")]
st=[]
for i,(x,y) in enumerate(pairs):
    b=before(x,y)
    first,second=(x,y) if b else (y,x)
    st.append({"at":{"i":i},"vars":{"pair":f"{x},{y}","glueXY":x+y,"glueYX":y+x,"first":first},"note":f"Compare {x} with {y}. Gluing {x} first gives {x+y} and gluing {y} first gives {y+x}. The larger string wins, so {first} goes ahead of {second}."})
assert before("34","3") and before("3","30") and before("34","30")
fill(CH,'03-comparator-contracts.md',block(["3","30","34"],["i"],st),"@@TRACE2@@")
