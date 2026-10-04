from common import *
CH='01-arrays-core-operations'
def run(a):
    me=mo=ne=no=a[0]; tot=a[0]; st=[{"at":{"i":0},"vars":{"maxEnding":me,"maxOverall":mo,"minEnding":ne,"minOverall":no,"total":tot},"note":f"Index 0 holds {a[0]}. All four running values start at {a[0]} and the total is {tot}."}]
    for i in range(1,len(a)):
        x=a[i]; tot+=x; me=max(x,me+x); mo=max(mo,me); ne=min(x,ne+x); no=min(no,ne)
        st.append({"at":{"i":i},"vars":{"maxEnding":me,"maxOverall":mo,"minEnding":ne,"minOverall":no,"total":tot},"note":f"Index {i} holds {x}. The maximum scan ends here at {me} with best {mo}. The minimum scan ends here at {ne} with best {no}. The total is {tot}."})
    wrap=tot-no
    if mo<0: ans=mo; fin=f"The ordinary maximum {mo} is negative, so the wrapping candidate {tot} - ({no}) = {wrap} is an empty remainder and is rejected. The answer is {ans}."
    else:
        ans=max(mo,wrap); fin=f"The wrapping candidate is {tot} - ({no}) = {wrap}. It is compared with the ordinary maximum {mo}. The answer is {ans}."
    st.append({"at":{"i":len(a)},"vars":{"maxOverall":mo,"minOverall":no,"total":tot,"wrapCandidate":wrap,"answer":ans},"note":"Scans finished. "+fin})
    return st,ans
def brute(a):
    n=len(a); return max(sum(a[(s+k)%n] for k in range(l)) for s in range(n) for l in range(1,n+1))
for a,exp,ph in (([4,-5,2,-1,6],11,"@@TRACE1@@"),([-6,-1,-4],-1,"@@TRACE2@@")):
    s,ans=run(a); assert ans==exp==brute(a)
    fill(CH,'12-circular-kadane.md',block(a,["i"],s),ph)
