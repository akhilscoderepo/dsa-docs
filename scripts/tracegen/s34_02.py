from common import *
CH='34-advanced-strings'; F='02-prefix-matching.md'
def pfun(p):
    pi=[0]*len(p); k=0
    for i in range(1,len(p)):
        while k>0 and p[i]!=p[k]: k=pi[k-1]
        if p[i]==p[k]: k+=1
        pi[i]=k
    return pi
# Trace 1: build the prefix function of ababaca, with fallbacks at index 5.
p="ababaca"; pi=[0]*len(p); k=0; st=[]
st.append({"at":{"i":0,"k":0},"vars":{"pi":"0"},"note":"pi[0] is 0 because a one-character text has no proper prefix. The matched length k starts at 0."})
for i in range(1,len(p)):
    while k>0 and p[i]!=p[k]:
        old=k; k=pi[k-1]
        st.append({"at":{"i":i,"k":k},"vars":{"pi":",".join(map(str,pi[:i]))},"note":f"i = {i}: p[{old}] is '{p[old]}' and rejects '{p[i]}'. A fallback sets k to pi[{old-1}] = {k}, the next shorter border, without moving i."})
    if p[i]==p[k]:
        k+=1; msg=f"i = {i}: the character '{p[i]}' matches p[{k-1}], the next expected pattern character, and k rises to {k}, which is also the new border length."
    else:
        msg=f"i = {i}: no border is left to try. The character '{p[i]}' is not p[0], and pi[{i}] stays 0."
    pi[i]=k
    st.append({"at":{"i":i,"k":k},"vars":{"pi":",".join(map(str,pi[:i+1]))},"note":msg})
assert pi==pfun(p)==[0,0,1,2,3,0,1]
fill(CH,F,block(list(p),["i","k"],st),"@@TRACE1@@")
# Trace 2: scan a text with pattern ababaca using the same array.
text="abababaca"; pat="ababaca"; pi=pfun(pat); k=0; st=[]; found=-1
for i,c in enumerate(text):
    while k>0 and c!=pat[k]:
        old=k; k=pi[k-1]
        st.append({"at":{"i":i,"k":k},"vars":{"matched":k},"note":f"i = {i}: p[{old}] is '{pat[old]}' but the text holds '{c}'. One fallback replaces {old} by pi[{old-1}] = {k}, and the same text index is compared again."})
    if c==pat[k]:
        k+=1; msg=f"i = {i}: text character '{c}' agrees with p[{k-1}], so the match is now {k} {'character' if k==1 else 'characters'} long."
    else:
        msg=f"i = {i}: text character '{c}' cannot begin the pattern, so the match length remains 0."
    st.append({"at":{"i":i,"k":k},"vars":{"matched":k},"note":msg})
    if k==len(pat):
        found=i-len(pat)+1
        st[-1]["note"]+=f" k equals the pattern length 7, so the first occurrence starts at {i} - 7 + 1 = {found}."
        break
assert found==2==text.find(pat)
fill(CH,F,block(list(text),["i","k"],st),"@@TRACE2@@")
