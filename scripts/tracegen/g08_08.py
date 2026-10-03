from common import *
CH='08-two-pointers'
F='08-sorting-and-two-pointers.md'

# trace 1: pair by original index through an index order
nums=[8,3,11,5,2,9]; target=17
order=sorted(range(len(nums)),key=lambda k:nums[k])
row=[nums[k] for k in order]
lo,hi=0,len(row)-1; st=[]; ans=None
while lo<hi:
    s=row[lo]+row[hi]
    base={"at":{"lo":lo,"hi":hi},"vars":{"sum":s,"slots":f"{order[lo]} and {order[hi]}"}}
    if s==target:
        base["note"]=f"{row[lo]} plus {row[hi]} is {s}, which equals {target}. The tokens came from slots {min(order[lo],order[hi])} and {max(order[lo],order[hi])}."
        st.append(base); ans=[min(order[lo],order[hi]),max(order[lo],order[hi])]; break
    if s<target:
        base["note"]=f"{row[lo]} plus {row[hi]} is {s}, too small, so {row[lo]} fits no partner in the window and lo becomes {lo+1}."
        lo+=1
    else:
        base["note"]=f"{row[lo]} plus {row[hi]} is {s}, too big, so {row[hi]} fits no partner in the window and hi becomes {hi-1}."
        hi-=1
    st.append(base)
assert ans==[0,5] and len(st)==5 and "too big" in st[3]["note"], (ans,len(st))
fill(CH,F,block(row,["lo","hi"],st),"@@TRACE1@@")

# trace 2: count distinct zero-sum triples
a=[-2,-2,0,1,1,2]
st=[]; count=0
n=len(a)
for i in range(n-2):
    if a[i]>0: break
    if i>0 and a[i]==a[i-1]:
        st.append({"at":{"i":i,"lo":-1,"hi":-1},"vars":{"count":count},"note":f"Anchor {a[i]} at position {i} equals the previous anchor, so it is skipped before any pointer moves."}); continue
    lo,hi=i+1,n-1
    while lo<hi:
        s=a[i]+a[lo]+a[hi]
        v={"sum":s,"count":count}
        if s<0:
            st.append({"at":{"i":i,"lo":lo,"hi":hi},"vars":v,"note":f"Sum {s} is below zero, so lo becomes {lo+1}."}); lo+=1
        elif s>0:
            st.append({"at":{"i":i,"lo":lo,"hi":hi},"vars":v,"note":f"Sum {s} is above zero, so hi becomes {hi-1}."}); hi-=1
        else:
            count+=1; v["count"]=count
            l0,h0=lo,hi
            while lo<hi and a[lo]==a[l0]: lo+=1
            while lo<hi and a[hi]==a[h0]: hi-=1
            st.append({"at":{"i":i,"lo":l0,"hi":h0},"vars":v,"note":f"Sum 0: {a[i]}, {a[l0]}, {a[h0]} is counted. Both pointers then step past copies of their values, so lo becomes {lo} and hi becomes {hi}."})
assert count==2 and len(st)>=5
assert any("previous anchor" in s["note"] for s in st)
fill(CH,F,block(a,["i","lo","hi"],st),"@@TRACE2@@")
