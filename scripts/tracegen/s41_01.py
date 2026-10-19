from common import *
CH='41-algorithmic-services-and-simulations'; F='01-board-simulations.md'
def board():
    n=3; owner={}; row=[0]*n; col=[0]*n; dg=0; an=0; over=False
    calls=[(1,1,1),(1,1,2),(0,0,2),(0,1,1),(2,2,2),(2,1,1),(1,0,2)]
    expect=[0,-1,0,0,0,1,-1]
    cells=[f"({r},{c}) p{p}" for r,c,p in calls]; st=[]
    for k,(r,c,p) in enumerate(calls):
        if over or (r,c) in owner:
            res=-1; why="the game is already won" if over else f"cell ({r},{c}) already holds a mark"
            note=f"Call {k}: {why}, so the call returns -1 and every sum stays as it was."
        else:
            d=1 if p==1 else -1; owner[(r,c)]=p; row[r]+=d; col[c]+=d
            if r==c: dg+=d
            if r+c==n-1: an+=d
            res=0
            if n in map(abs,(row[r],col[c],dg if r==c else 0,an if r+c==n-1 else 0)):
                res=p; over=True
            note=f"Call {k}: player {p} marks ({r},{c}), which changes the row {r} and column {c} sums"
            if r==c: note+=" and the main diagonal sum"
            if r+c==n-1: note+=" and the anti-diagonal sum"
            note+=f". The call returns {res}."
            if res: note+=f" A sum reaches {n} in absolute value, so player {p} wins."
        assert res==expect[k]
        st.append({"at":{"call":k},"vars":{"rows":",".join(map(str,row)),"cols":",".join(map(str,col)),"diag":str(dg),"anti":str(an),"result":str(res)},"note":note})
    return cells,st
def snake():
    W=H=3; food=[(0,1),(1,1),(1,0)]; body=[(0,0)]; nf=0; over=False
    moves="RDLUDR"; expect=[1,2,3,3,-1,-1]
    D={'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}; cells=list(moves); st=[]
    for k,m in enumerate(moves):
        if over:
            res=-1; note=f"Call {k}: the game is over, so the call returns -1 and writes nothing."
        else:
            r,c=body[-1][0]+D[m][0],body[-1][1]+D[m][1]
            if not(0<=r<H and 0<=c<W):
                over=True; res=-1; note=f"Call {k}: the head would leave the grid, so the game ends."
            else:
                eat=nf<len(food) and food[nf]==(r,c); tail=body[0]
                if (r,c) in body and (eat or (r,c)!=tail):
                    over=True; res=-1; note=f"Call {k}: the head would enter ({r},{c}), which a body segment other than a released tail holds, so the game ends and the body stays as it was."
                else:
                    if eat: nf+=1; note=f"Call {k}: the head enters the food cell ({r},{c}), the tail stays and the score becomes {nf}."
                    elif (r,c)==tail: note=f"Call {k}: the head enters ({r},{c}), where the tail was. The move does not eat, so the tail leaves first and the move is legal."
                    else: note=f"Call {k}: the head enters ({r},{c}) and the tail leaves {tail}."
                    if not eat: body.pop(0)
                    body.append((r,c)); res=nf
        assert res==expect[k],(k,res)
        st.append({"at":{"call":k},"vars":{"body":" ".join(f"{a}{b}" for a,b in body),"score":str(nf),"result":str(res)},"note":note})
    return cells,st
c,s=board(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=snake(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
