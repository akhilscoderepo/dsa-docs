from common import *
CH='08-two-pointers'; F='04-three-way-partition.md'
def go(a0,grp,labels,ph):
    a=list(a0); lo=mid=0; hi=len(a)-1; st=[]
    while mid<=hi:
        g=grp(a[mid]); v={"array":str(a)}
        at={"low":lo,"mid":mid,"high":hi}
        if g==0:
            x=a[mid]; a[lo],a[mid]=a[mid],a[lo]
            st.append({"at":at,"vars":{"array":str(a)},"note":f"The value {x} belongs to the {labels[0]}, so it swaps with the slot at low, and low and mid both advance."}); lo+=1; mid+=1
        elif g==1:
            st.append({"at":at,"vars":v,"note":f"The value {a[mid]} belongs to the {labels[1]}, so only mid advances."}); mid+=1
        else:
            x=a[mid]; a[mid],a[hi]=a[hi],a[mid]
            st.append({"at":at,"vars":{"array":str(a)},"note":f"The value {x} belongs to the {labels[2]}, so it swaps with the slot at high and high moves back. The value now at mid is unread, so mid stays."}); hi-=1
    st.append({"at":{"low":lo,"mid":mid,"high":hi},"vars":{"array":str(a)},"note":"The pointer mid has passed high, so no slot is unresolved."})
    fill(CH,F,block(list(a0),["low","mid","high"],st),ph); return a
r=go([2,0,2,1,1,0],lambda x:x,["first group","middle region","third group"],"@@TRACE1@@"); assert r==[0,0,1,1,2,2]
r=go([7,5,2,9,5,1],lambda x:0 if x<5 else (1 if x==5 else 2),["values below the pivot","values equal to the pivot","values above the pivot"],"@@TRACE2@@"); assert sorted(r[:2])==[1,2] and r[2:4]==[5,5] and sorted(r[4:])==[7,9]
