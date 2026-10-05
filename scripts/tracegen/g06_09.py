from common import *
CH='06-binary-search'
def rounds(n,lo,hi,ok,desc,ph):
    cells=[f"round {i}" for i in range(n+1)]
    st=[{"at":{"round":0},"vars":{"lo":f"{lo:g}","hi":f"{hi:g}"},"note":f"Start with the interval [{lo:g}, {hi:g}]."}]
    for i in range(1,n+1):
        mid=lo+(hi-lo)/2
        r,d=ok(mid)
        if r: hi=mid
        else: lo=mid
        st.append({"at":{"round":i},"vars":{"mid":f"{mid:g}","lo":f"{lo:g}","hi":f"{hi:g}"},"note":desc(mid,r,d)})
    return cells,st,lo,hi,ph
def fin(c,s,ph): fill(CH,'09-continuous-answers.md',block(c,["round"],s),ph)
def d1(mid,r,sq): return f"The square of {mid:g} is {sq:g}, which is {'at least' if r else 'below'} 10, so {'hi' if r else 'lo'} becomes {mid:g}."
c,s,lo,hi,ph=rounds(7,0,10,lambda m:(m*m>=10,m*m),d1,"@@TRACE1@@"); assert abs(hi-10**.5)<0.1 ; fin(c,s,ph)
def ok2(d): n=int(10//d)+1; return n<4,n   # pass (feasible) -> lo moves up
def d2(mid,r,n): return f"A gap of {mid:g} fits {n} points, which is {'fewer than' if r else 'at least'} 4... "
# feasible means n>=4: lo=mid ; infeasible: hi=mid
def rounds2():
    lo,hi=0.0,10.0; cells=[f"round {i}" for i in range(7)]
    st=[{"at":{"round":0},"vars":{"lo":f"{lo:g}","hi":f"{hi:g}"},"note":"Start with the gap range [0, 10]."}]
    for i in range(1,7):
        mid=lo+(hi-lo)/2; n=int(10//mid)+1
        if n>=4: lo=mid; note=f"A gap of {mid:g} fits {n} points, which is at least 4, so lo becomes {mid:g}."
        else: hi=mid; note=f"A gap of {mid:g} fits {n} points, which is fewer than 4, so hi becomes {mid:g}."
        st.append({"at":{"round":i},"vars":{"mid":f"{mid:g}","lo":f"{lo:g}","hi":f"{hi:g}"},"note":note})
    assert abs(lo-10/3)<0.2
    fin(cells,st,"@@TRACE2@@")
rounds2()
