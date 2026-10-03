from common import *
CH='09-sliding-window'
F='01-fixed-size-aggregate-windows.md'

def sums(a,k):
    total=sum(a[:k]); best=total; st=[]
    st.append({"at":{"left":0,"right":k-1},"vars":{"total":total,"best":best},
               "note":f"Build the first block by adding {k} values: the total is {total}, and it is the best so far."})
    for right in range(k,len(a)):
        out=a[right-k]; inn=a[right]
        total+=inn-out; best=max(best,total)
        st.append({"at":{"left":right-k+1,"right":right},"vars":{"total":total,"best":best},
                   "note":f"The value {out} leaves and the value {inn} enters, so the total becomes {total}. The best total so far is {best}."})
    return st,best

def vowels(s,k):
    isv=lambda c:1 if c in "aeiou" else 0
    cnt=sum(isv(c) for c in s[:k]); best=cnt; st=[]
    st.append({"at":{"left":0,"right":k-1},"vars":{"vowels":cnt,"best":best},
               "note":f"Count the vowels among the first {k} letters: {cnt}, which is the best so far."})
    for right in range(k,len(s)):
        out=s[right-k]; inn=s[right]
        cnt+=isv(inn)-isv(out); best=max(best,cnt)
        kind=lambda c:"a vowel" if isv(c) else "a consonant"
        st.append({"at":{"left":right-k+1,"right":right},"vars":{"vowels":cnt,"best":best},
                   "note":f"{out} leaves ({kind(out)}) and {inn} enters ({kind(inn)}), so the count is {cnt}. The best count so far is {best}."})
    return st,best

a=[4,2,-1,6,3,5,1]
s1,b=sums(a,3)
assert b==max(sum(a[i:i+3]) for i in range(len(a)-2)) and s1[1]["vars"]["total"]==7 and len(s1)==5
fill(CH,F,block(a,["left","right"],s1),"@@TRACE1@@")
w="sequoiaxyz"
s2,b=vowels(w,4)
assert b==4 and len(s2)==7 and s2[3]["vars"]["best"]==4
assert any(s2[i]["vars"]["vowels"]<s2[i-1]["vars"]["vowels"] for i in range(1,len(s2)))
fill(CH,F,block(list(w),["left","right"],s2),"@@TRACE2@@")
