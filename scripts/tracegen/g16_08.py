from common import *
CH='16-trees-bfs-and-bsts'; F='08-serialization-and-deserialization.md'
tokens=["7","3","#","5","#","#","9","#","#"]
# tree: 7 (3 (None,5), 9)
T=("7",("3",None,("5",None,None)),("9",None,None))
st=[]; out=[]
def enc(n,label):
    i=len(out)
    if n is None:
        out.append("#"); st.append({"at":{"at":i},"vars":{"slot":label},"note":f"The {label} is empty, so the writer emits the null marker."}); return
    out.append(n[0]); st.append({"at":{"at":i},"vars":{"slot":label},"note":f"The writer emits the value {n[0]} for the {label}."})
    enc(n[1],f"left slot of {n[0]}"); enc(n[2],f"right slot of {n[0]}")
enc(T,"root"); assert out==tokens
fill(CH,F,block(tokens,["at"],st),"@@TRACE1@@")
st=[]; idx=[0]; made=[0]
def dec(depth,label):
    i=idx[0]; t=tokens[i]; idx[0]+=1
    if t=="#":
        st.append({"at":{"at":i},"vars":{"depth":depth},"note":f"Token {i} is the null marker, so the {label} stays empty."}); return
    made[0]+=1
    st.append({"at":{"at":i},"vars":{"depth":depth},"note":f"Token {i} is {t}, so the reader creates a node for the {label} and reads its left subtree next."})
    dec(depth+1,f"left slot of {t}"); dec(depth+1,f"right slot of {t}")
dec(1,"root"); assert idx[0]==9 and made[0]==4
fill(CH,F,block(tokens,["at"],st),"@@TRACE2@@")
