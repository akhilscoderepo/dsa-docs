from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='06-randomized-partitioning.md'
def run(a0,t,draws,ph):
    a=a0[:]; lo,hi=0,len(a)-1; di=iter(draws); f=lambda x:" ".join(map(str,x))
    st=[{"at":{"lo":0,"hi":hi,"p":-1},"vars":{"target":t,"array":f(a)},"note":f"Start: the active range is the whole array and the wanted rank is {t}."}]; fin=None
    while True:
        d=next(di); p=lo+d; pv=a[p]; lt,i,gt=lo,lo,hi
        while i<=gt:
            if a[i]<pv: a[lt],a[i]=a[i],a[lt]; lt+=1; i+=1
            elif a[i]>pv: a[i],a[gt]=a[gt],a[i]; gt-=1
            else: i+=1
        if t<lt: dec=f"The rank {t} is below the equal band, so the range becomes {lo} to {lt-1}."; nlo,nhi=lo,lt-1
        elif t>gt: dec=f"The rank {t} is above the equal band, so the range becomes {gt+1} to {hi}."; nlo,nhi=gt+1,hi
        else: dec=f"The rank {t} is inside the equal band, so the method returns {pv}."; nlo,nhi=lo,hi
        st.append({"at":{"lo":lo,"hi":hi,"p":p},"vars":{"draw":d,"pivot":pv,"array":f(a)},"note":f"Draw offset {d} picks position {p} with pivot value {pv}. The pivot value is read before any swap."})
        st.append({"at":{"lo":lo,"hi":hi,"p":p},"vars":{"lt":lt,"gt":gt,"array":f(a)},"note":f"The three-way scan ends. The equal band covers positions {lt} to {gt}. {dec}"})
        if lt<=t<=gt: fin=pv; break
        lo,hi=nlo,nhi
    assert fin==sorted(a0)[t]; fill(CH,N,block(a0,["lo","hi","p"],st),ph)
run([9,4,7,4,1,8],3,[0,1],"@@TRACE1@@")
run([5,5,5,2,5,9,5],3,[2],"@@TRACE2@@")
