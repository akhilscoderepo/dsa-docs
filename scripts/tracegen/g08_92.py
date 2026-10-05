from common import *
CH='08-two-pointers'; F='92-strings-from-both-ends.md'
def t1():
    s="Madam, I'm Adam"; cells=list(s); l,r=0,len(s)-1; st=[]
    ok=lambda c:c.isalnum()
    while l<r:
        at={"left":l,"right":r}
        if not ok(s[l]): st.append({"at":at,"vars":{},"note":f"The character {s[l]!r} at left is ignored, so left moves right."}); l+=1
        elif not ok(s[r]): st.append({"at":at,"vars":{},"note":f"The character {s[r]!r} at right is ignored, so right moves left."}); r-=1
        else:
            assert s[l].lower()==s[r].lower()
            st.append({"at":at,"vars":{"pair":f"{s[l].lower()} and {s[r].lower()}"},"note":f"The letters {s[l].lower()} and {s[r].lower()} match, so both pointers move inward."}); l+=1; r-=1
    st.append({"at":{"left":l,"right":r},"vars":{},"note":"The pointers have met, so every counted pair matched and the answer is true."})
    return block(cells,["left","right"],st)
def t2():
    s="abcddcbea"; cells=list(s); l,r=0,len(s)-1; st=[]
    while l<r and s[l]==s[r]:
        st.append({"at":{"left":l,"right":r},"vars":{"pair":f"{s[l]} and {s[r]}"},"note":f"The characters {s[l]} and {s[r]} match, so both pointers move inward."}); l+=1; r-=1
    st.append({"at":{"left":l,"right":r},"vars":{"pair":f"{s[l]} and {s[r]}"},"note":f"The characters {s[l]} and {s[r]} differ. The scan now tests two ranges."})
    A=s[l+1:r+1]; B=s[l:r]
    st.append({"at":{"left":l+1,"right":r},"vars":{"range":A},"note":f"Without the left character, the range {A} is not a palindrome."})
    st.append({"at":{"left":l,"right":r-1},"vars":{"range":B},"note":f"Without the right character, the range {B} is a palindrome, so the answer is true."})
    assert A!=A[::-1] and B==B[::-1]
    return block(cells,["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
