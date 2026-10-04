from common import *
CH='03-strings'; F='07-center-expansion.md'
def run(s):
    n=len(s); best=0
    st=[{"at":{"left":-1,"right":0},"vars":{"best":0},"note":"Start: no middle has been tried, so best is 0."}]
    for c in range(n):
        for kind,(l,r) in (("odd center",(c,c)),("gap after",(c,c+1))):
            first=True
            while True:
                lab=f"{kind} index {c}" 
                if l>=0 and r<n and s[l]==s[r]:
                    st.append({"at":{"left":l,"right":r},"vars":{"best":best},"note":f"{lab.capitalize()}: indexes {l} and {r} hold '{s[l]}' and '{s[r]}', which match, so both ends move outward."})
                    l-=1; r+=1
                else:
                    L=r-l-1; best=max(best,L)
                    if l<0 or r>=n: why="a bound is crossed"
                    else: why=f"'{s[l]}' and '{s[r]}' differ"
                    st.append({"at":{"left":l,"right":r},"vars":{"best":best},"note":f"{lab.capitalize()}: at indexes {l} and {r}, {why}, so the attempt ends with length {L}. The best length is {best}."})
                    break
    return st,best
def brute(s): return max((j-i for i in range(len(s)) for j in range(i+1,len(s)+1) if s[i:j]==s[i:j][::-1]),default=0)
for ph,s,exp in (("@@TRACE1@@","aba",3),("@@TRACE2@@","abba",4)):
    st,b=run(s); assert b==exp==brute(s)
    fill(CH,F,block(list(s),["left","right"],st),ph)
