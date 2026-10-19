from common import *
CH='39-dynamic-query-structures'; F='05-query-planning.md'
def run(pos, left, right):
    st=[]; n=len(pos)
    def lb(x, label):
        lo, hi = 0, n
        st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":x,"search":label},"note":f"{label}: find the first stored position that is at least {x}. The window from lo up to but not including hi starts as the whole list."})
        while lo < hi:
            mid = lo + (hi-lo)//2
            if pos[mid] < x:
                nlo, nhi, why = mid+1, hi, f"{pos[mid]} is below {x}, so lo moves to {mid+1}."
            else:
                nlo, nhi, why = lo, mid, f"{pos[mid]} is at least {x}, so hi moves to {mid}."
            st.append({"at":{"lo":nlo,"hi":nhi,"mid":mid},"vars":{"target":x,"search":label},"note":f"mid = {mid} holds {pos[mid]}. {why}"})
            lo, hi = nlo, nhi
        st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":x,"search":label,"first":lo},"note":f"lo equals hi at {lo}, so first = {lo}, the list index of the first stored position that is at least {x}."})
        return lo
    a = lb(left, "lower end")
    b = lb(right+1, "upper end")
    cnt = b - a
    st[-1]["vars"]["count"] = cnt
    st[-1]["note"] += f" The count is {b} - {a} = {cnt}."
    return st, cnt
pos1=[0,2,4,6]
st,c=run(pos1,1,5)
assert c==sum(1 for p in pos1 if 1<=p<=5)==2
refill(CH,F,block([str(p) for p in pos1],["lo","mid","hi"],st),0)
pos2=[1,4,5,8,9]
st,c=run(pos2,5,8)
assert c==sum(1 for p in pos2 if 5<=p<=8)==2
refill(CH,F,block([str(p) for p in pos2],["lo","mid","hi"],st),1)
