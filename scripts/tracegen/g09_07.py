from common import *
CH='09-sliding-window'
F='07-replacement-budget-windows.md'
def run(s,k):
    tally={}; record=0; left=0; steps=[]
    for right,ch in enumerate(s):
        tally[ch]=tally.get(ch,0)+1
        old=record; record=max(record,tally[ch])
        width=right-left+1
        cost=width-record
        if cost>k:
            gone=s[left]; tally[gone]-=1; left+=1
            note=f"Read {ch} at position {right}: the record is {record} and the window of width {width} would cost {cost}, more than {k}. Drop {gone}; left becomes {left} and the window slides at width {right-left+1}."
        else:
            raise_txt=f" The record rises from {old} to {record}." if record>old else f" The record stays {record}."
            note=f"Read {ch} at position {right}:{raise_txt} The window of width {width} costs {cost}, which fits {k}, so it grows."
        true=max(v for v in tally.values())
        steps.append({"at":{"left":left,"right":right},"vars":{"record":record,"true max":true,"width":right-left+1},"note":note})
    return steps,len(s)-left
def brute(s,k):
    best=0
    for i in range(len(s)):
        for j in range(i,len(s)):
            w=s[i:j+1]
            if len(w)-max(w.count(c) for c in set(w))<=k: best=max(best,len(w))
    return best
s1="AAABCDE"; st,ans=run(s1,1); assert ans==brute(s1,1)==4
assert st[4]["at"]=={"left":1,"right":4} and st[4]["vars"]["record"]==3 and st[4]["vars"]["true max"]==2 and "slides" in st[4]["note"]
fill(CH,F,block(list(s1),["left","right"],st),"@@TRACE1@@")
s2="QRRQSQQTU"; st,ans=run(s2,2); assert ans==brute(s2,2)==5
assert st[-1]["vars"]["record"]==3 and st[-1]["vars"]["true max"]==2 and st[-1]["vars"]["width"]==5
fill(CH,F,block(list(s2),["left","right"],st),"@@TRACE2@@")
