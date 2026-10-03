from common import *
CH='06-binary-search'
F='09-continuous-answers.md'
def nr(v): return int(v+0.5)
x=10.0; lo,hi=0.0,10.0; st=[]
for _ in range(7):
    mid=(lo+hi)/2; sq=mid*mid
    if sq<=x:
        note=f"Try {mid:g}. Its area is {sq:.4g}, which is too small, so lo moves up to {mid:g} and the interval keeps its upper half."; nlo,nhi=mid,hi
    else:
        note=f"Try {mid:g}. Its area is {sq:.4g}, which is too big, so hi moves down to {mid:g} and the interval keeps its lower half."; nlo,nhi=lo,mid
    st.append({"at":{"lo":nr(lo),"hi":nr(hi),"mid":nr(mid)},"vars":{"mid":mid,"area":round(sq,4)},"note":note}); lo,hi=nlo,nhi
assert "lo moves up to 2.5" in st[1]["note"] and "too small" in st[1]["note"]
st.append({"at":{"lo":nr(lo),"hi":nr(hi),"mid":-1},"vars":{"lo":round(lo,4),"hi":round(hi,4),"width":round(hi-lo,4)},"note":f"After 7 halvings the width is {hi-lo:.4g}, the answer is between {lo:.4g} and {hi:.4g}, and about 20 more halvings would pass one millionth."})
fill(CH,F,block([str(i) for i in range(11)],["lo","hi","mid"],st),"@@TRACE1@@")
sites=[1,2,4,8,9]; k=3
def can(g):
    c,last=1,sites[0]
    for s in sites[1:]:
        if s-last>=g: c+=1; last=s
    return c
lo,hi=0.0,8.0; st=[]
for _ in range(6):
    mid=(lo+hi)/2; c=can(mid)
    if c>=k:
        note=f"Try a gap of {mid:g}. Greedy placement finds {c} sites, enough, so lo moves up to {mid:g}."; nlo,nhi=mid,hi
    else:
        note=f"Try a gap of {mid:g}. Greedy placement finds {c} sites, fewer than {k}, so hi moves down to {mid:g}."; nlo,nhi=lo,mid
    st.append({"at":{"lo":nr(lo),"hi":nr(hi),"mid":nr(mid)},"vars":{"gap":mid,"sites":c},"note":note}); lo,hi=nlo,nhi
assert "lo moves up to 3" in st[2]["note"] and "enough" in st[2]["note"]
st.append({"at":{"lo":nr(lo),"hi":nr(hi),"mid":-1},"vars":{"lo":lo,"hi":hi},"note":f"The answer is between {lo:g} and {hi:g}, and more halvings close in on 3."})
fill(CH,F,block([str(i) for i in range(9)],["lo","hi","mid"],st),"@@TRACE2@@")
