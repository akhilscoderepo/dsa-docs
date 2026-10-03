from common import *
CH='08-two-pointers'
F='09-strings-and-two-pointers.md'

# trace 1: palindrome ignoring noise
s="Madam, I'm Adam"
cells=list(s)
def alnum(c): return c.isalnum()
l,r=0,len(s)-1; st=[]
while l<r:
    if not alnum(s[l]):
        st.append({"at":{"left":l,"right":r},"vars":{"skipped":repr(s[l])},"note":f"Position {l} holds {s[l]!r}, which is noise, so left becomes {l+1} before any comparison."}); l+=1; continue
    if not alnum(s[r]):
        st.append({"at":{"left":l,"right":r},"vars":{"skipped":repr(s[r])},"note":f"Position {r} holds {s[r]!r}, which is noise, so right becomes {r-1} before any comparison."}); r-=1; continue
    assert s[l].lower()==s[r].lower()
    st.append({"at":{"left":l,"right":r},"vars":{"pair":f"{s[l].lower()}{s[r].lower()}"},"note":f"{s[l]!r} and {s[r]!r} are equal after lowercasing, so left becomes {l+1} and right becomes {r-1}."}); l+=1; r-=1
assert len(st)>=5 and "noise" in st[6]["note"], st[6]
fill(CH,F,block(cells,["left","right"],st),"@@TRACE1@@")

# trace 2: one repair
s="abcxcbda"
st=[]
def window(l,r,label):
    while l<r:
        ok=s[l]==s[r]
        st.append({"at":{"left":l,"right":r},"vars":{"test":label},"note":(f"{label}: {s[l]!r} and {s[r]!r} "+("match, so both pointers move inward." if ok else "differ, so this window is not a palindrome and the test fails."))})
        if not ok: return False
        l+=1; r-=1
    st.append({"at":{"left":min(l,len(s)),"right":max(r,-1)},"vars":{"test":label},"note":f"{label}: the pointers met with every pair equal, so this window is a palindrome."})
    return True
l,r=0,len(s)-1; res=None
while l<r:
    if s[l]!=s[r]:
        st.append({"at":{"left":l,"right":r},"vars":{"test":"first mismatch"},"note":f"{s[l]!r} at {l} and {s[r]!r} at {r} differ. Only these two characters can be the one removed, so two windows are tested."})
        res=window(l+1,r,"drop left") or window(l,r-1,"drop right"); break
    st.append({"at":{"left":l,"right":r},"vars":{"test":"scan"},"note":f"{s[l]!r} and {s[r]!r} match, so both pointers move inward."}); l+=1; r-=1
assert res is True and "fails" in "".join(x["note"] for x in st) and len(st)>=5
fill(CH,F,block(list(s),["left","right"],st),"@@TRACE2@@")
