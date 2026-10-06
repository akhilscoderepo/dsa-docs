from common import *
CH='19-recursion-and-backtracking'; F='01-call-state.md'
a=[4,1,3]; st=[]
for i in range(3):
    st.append({"at":{"i":i},"vars":{"phase":"down","value":"waiting"},"note":f"The call for i = {i} must add a[{i}] = {a[i]} to the sum of the range that starts at {i+1}, so it calls sum with i = {i+1}."})
st.append({"at":{"i":3},"vars":{"phase":"return","value":0},"note":"The call for i = 3 equals the array length, so it matches the base case and returns 0 without a further call."})
v=0
for i in (2,1,0):
    nv=a[i]+v
    st.append({"at":{"i":i},"vars":{"phase":"return","value":nv},"note":f"The call for i = {i} adds a[{i}] = {a[i]} to the received value {v} and returns {nv}."}); v=nv
assert v==8
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
n=10; ex=[]
while True:
    ex.append(n)
    if n==0: break
    n//=2
st=[]
for d,e in enumerate(ex[:-1]):
    st.append({"at":{"d":d},"vars":{"exponent":e,"value":"waiting"},"note":f"The call with exponent {e} is not the base case, so it asks for the power with exponent {e//2}."})
st.append({"at":{"d":len(ex)-1},"vars":{"exponent":0,"value":1},"note":"The call with exponent 0 matches the base case and returns 1."})
h=1
for d in range(len(ex)-2,-1,-1):
    e=ex[d]; nv=h*h*(2 if e%2 else 1)
    st.append({"at":{"d":d},"vars":{"exponent":e,"value":nv},"note":f"The call with exponent {e} squares the half result {h}"+(f" and multiplies by 2 because {e} is odd, so it returns {nv}." if e%2 else f", because {e} is even, so it returns {nv}.")}); h=nv
assert h==1024
fill(CH,F,block([str(x) for x in ex],["d"],st),"@@TRACE2@@")
