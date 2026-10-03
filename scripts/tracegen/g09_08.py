from common import *
CH='09-sliding-window'
F='08-count-all-valid-subarrays-windows.md'
def run_sum(a,lim):
    left=0; tot=0; count=0; steps=[]
    for right,v in enumerate(a):
        tot+=v; moved=[]
        while left<=right and tot>=lim:
            tot-=a[left]; moved.append(a[left]); left+=1
        add=right-left+1; count+=add
        if moved: why=f"Adding {v} makes the total too large, so drop {', '.join(map(str,moved))} from the left; left becomes {left}."
        else: why=f"Adding {v} keeps the total under {lim}, so left stays at {left}."
        steps.append({"at":{"left":left,"right":right},"vars":{"total":tot,"added":add,"count":count},"note":f"Read position {right}. {why} Starts {left} to {right} each give a valid stretch ending here, so {add} is added and the count is {count}."})
    return steps,count
def run_prod(a,k):
    left=0; prod=1; count=0; steps=[]
    for right,v in enumerate(a):
        prod*=v; moved=[]
        while left<=right and prod>=k:
            prod//=a[left]; moved.append(a[left]); left+=1
        add=right-left+1; count+=add
        if left>right: why=f"The value {v} alone reaches {k}, so every start is dropped, left becomes {left} and the window is empty."
        elif moved: why=f"Multiplying by {v} makes the product too large, so divide out {', '.join(map(str,moved))}; left becomes {left}."
        else: why=f"Multiplying by {v} keeps the product under {k}, so left stays at {left}."
        steps.append({"at":{"left":left,"right":right},"vars":{"product":prod,"added":add,"count":count},"note":f"Read position {right}. {why} {add} valid stretches end here, and the count is {count}."})
    return steps,count
def brute_sum(a,lim): return sum(1 for i in range(len(a)) for j in range(i,len(a)) if sum(a[i:j+1])<lim)
def brute_prod(a,k):
    import math
    return sum(1 for i in range(len(a)) for j in range(i,len(a)) if math.prod(a[i:j+1])<k)
a1=[3,1,2,6,1,1,4]; st,c=run_sum(a1,7); assert c==brute_sum(a1,7)
assert any("drop" in s["note"] for s in st)
fill(CH,F,block(a1,["left","right"],st),"@@TRACE1@@")
a2=[3,25,2,4,1,6]; st,c=run_prod(a2,20); assert c==brute_prod(a2,20)
assert st[1]["at"]=={"left":2,"right":1} and st[1]["vars"]["added"]==0
fill(CH,F,block(a2,["left","right"],st),"@@TRACE2@@")
