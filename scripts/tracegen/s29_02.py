from common import *
CH='29-dynamic-programming-intervals-and-advanced-states'; FILE='02-palindrome-partitions.md'
S="aaba"; n=len(S)
# Trace 1: fill the palindrome table, rows from the bottom, columns left to right.
pal=[[False]*n for _ in range(n)]; steps=[]
for i in range(n-1,-1,-1):
    for j in range(i,n):
        same=S[i]==S[j]
        if j-i<2: inner="empty"; v=same
        else: inner="true" if pal[i+1][j-1] else "false"; v=same and pal[i+1][j-1]
        pal[i][j]=v
        if not same: why=f"The end characters '{S[i]}' and '{S[j]}' differ, so the entry is false."
        elif inner=="empty": why=f"The end characters '{S[i]}' and '{S[j]}' match and nothing lies between them, so the entry is true."
        elif v: why=f"The end characters match and the inner interval {i+1} to {j-1} is true, so the entry is true."
        else: why=f"The end characters match, but the inner interval {i+1} to {j-1} is false, so the entry is false."
        steps.append({"at":{"cell":i*n+j},"vars":{"i":i,"j":j,"ends":"match" if same else "differ","inner":inner,"pal":1 if v else 0},"note":f"Substring {S[i:j+1]!r} spans indexes {i} to {j}. "+why})
assert sum(pal[i][j] for i in range(n) for j in range(i,n))==6
t1=block(list(range(n*n)),["cell"],steps)
# Trace 2: prefix pieces using the table.
d=[0]+[10**9]*n; steps=[]; fmt=lambda l:"["+", ".join("-" if x>=10**9 else str(x) for x in l)+"]"
for end in range(1,n+1):
    for st in range(end):
        ok=pal[st][end-1]; piece=S[st:end]
        if ok and d[st]+1<d[end]: d[end]=d[st]+1; why=f"The piece {piece!r} is a palindrome, so pieces[{end}] becomes pieces[{st}] + 1 = {d[end]}."
        elif ok: why=f"The piece {piece!r} is a palindrome, but pieces[{st}] + 1 = {d[st]+1} does not beat {d[end]}."
        else: why=f"The piece {piece!r} is not a palindrome, so this start is skipped."
        steps.append({"at":{"start":st,"end":end-1},"vars":{"end":end,"start":st,"piece":piece,"pal":1 if ok else 0,"pieces":fmt(d)},"note":f"Prefix length {end}, last piece starts at {st}. "+why})
assert d[n]==2 and d[n]-1==1
t2=block(list(S),["start","end"],steps)
fill(CH,FILE,t1,"@@TRACE1@@"); fill(CH,FILE,t2,"@@TRACE2@@")
