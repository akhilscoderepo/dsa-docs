from common import *
CH='36-stateful-containers-and-histories'; F='06-resource-pools.md'
def run(n, ops):
    free=[True]*n; low=0; st=[]; res=[]
    def fr(): return ",".join(str(i) for i in range(n) if free[i]) or "none"
    for o,a in ops:
        if o=='a':
            r=-1
            for i in range(low,n):
                if free[i]: r=i; break
            if r>=0:
                free[r]=False; low=r+1
                note=f"allocate scans from low and returns {r}. The flag of {r} becomes false and low moves to {low}."
            else:
                low=n
                note=f"allocate scans from low and reads no true flag, so it returns -1 and leaves every flag unchanged."
            res.append(r); ptr=r if r>=0 else n
        else:
            ok = 0<=a<n and not free[a]
            if ok:
                free[a]=True; old=low; low=min(low,a)
                note=f"release({a}) finds the flag false, sets it true and returns true. low becomes min({old}, {a}) = {low}."
            else:
                why="is outside the pool" if not 0<=a<n else "is already free"
                note=f"release({a}) {why}, so it returns false and changes nothing."
            res.append(ok); ptr=a if 0<=a<n else n
        st.append({"at":{"id":ptr,"low":min(low,n)},"vars":{"free":fr(),"result":str(res[-1]).lower()},"note":note})
    return st,res
st,res=run(5,[('a',0)]*3+[('r',1),('a',0),('a',0),('a',0),('a',0)])
assert res==[0,1,2,True,1,3,4,-1]
fill(CH,F,block([str(i) for i in range(5)],["id","low"],st),"@@TRACE1@@")
st,res=run(4,[('a',0),('a',0),('r',1),('r',1),('r',7),('a',0),('a',0),('a',0),('a',0)])
assert res==[0,1,True,False,False,1,2,3,-1]
fill(CH,F,block([str(i) for i in range(4)],["id","low"],st),"@@TRACE2@@")
