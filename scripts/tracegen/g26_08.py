from common import *
CH='26-dynamic-programming-foundations'
F='08-transition-discipline.md'
start=[1,2,1,0,0]
def turn_ref(r): return [r[0]]+[r[j]+r[j-1] for j in range(1,len(r))]
def run(order,note_ok):
    row=list(start); cells=["col %d"%j for j in range(5)]
    steps=[{"at":{"j":-1},"vars":{"old":0,"written":0},"note":"Before the turn, the row reads %s."%row}]
    for j in order:
        old=row[j-1]; row[j]=row[j]+old
        extra=" That left neighbor still holds its value from the previous turn." if note_ok else (" That left neighbor was just overwritten, so the sum uses a changed value." if j>1 else " Column 0 is never written, so this read is still correct.")
        steps.append({"at":{"j":j},"vars":{"old":old,"written":row[j]},"note":"Column %d reads %d on its left and stores %d, so the row becomes %s.%s"%(j,old,row[j],row,extra)})
    return cells,steps,row
cells,steps,row=run([4,3,2,1],True)
assert row==turn_ref(start)==[1,3,3,1,0]
fill(CH,F,block(cells,["j"],steps),"@@TRACE1@@")
cells,steps,row=run([1,2,3,4],False)
assert row==[1,3,4,4,4] and row!=turn_ref(start)
fill(CH,F,block(cells,["j"],steps),"@@TRACE2@@")
# exercise values
def falling(m):
    n=len(m);prev=list(m[0])
    for r in range(1,n):
        prev=[m[r][c]+min(prev[x] for x in (c-1,c,c+1) if 0<=x<n) for c in range(n)]
    return min(prev)
def brute(m,r,c):
    n=len(m)
    if r==n-1: return m[r][c]
    return m[r][c]+min(brute(m,r+1,x) for x in (c-1,c,c+1) if 0<=x<n)
for m in ([[5,-2,4],[3,8,-1],[2,6,7]],[[4,-9],[7,1]]):
    assert falling(m)==min(brute(m,0,c) for c in range(len(m)))
    print(falling(m))
e1=falling([[5,-2,4],[3,8,-1],[2,6,7]]);e2=falling([[4,-9],[7,1]])
p=ROOT/CH/F;t=p.read_text();t=t.replace("@@EX1@@",str(e1)).replace("@@EX2@@",str(e2));p.write_text(t)
mx=lambda pr,co:[co[j]+max(pr[j],pr[j-1] if j else pr[j]) for j in range(len(pr))]
print(mx([3,1,4],[1,5,9]),mx([-6,-2,-8],[2,-1,3]))
