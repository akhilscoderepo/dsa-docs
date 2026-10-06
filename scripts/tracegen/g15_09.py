from common import *
CH='15-trees-dfs'; F='09-quadtree-construction.md'
def run(grid):
    n=len(grid); flat=[str(v) for row in grid for v in row]; steps=[]
    def go(r,c,s,name):
        first=grid[r][c]; bad=None
        for i in range(r,r+s):
            for j in range(c,c+s):
                if grid[i][j]!=first: bad=(i,j); break
            if bad: break
        a,b=r*n+c,(r+s-1)*n+(c+s-1)
        reg=f"row {r}, column {c}, side {s}"
        if bad is None:
            steps.append({"at":{"start":a,"end":b},"vars":{"region":reg,"result":f"leaf {first}"},"note":f"The {name} has every cell equal to {first}, so the call returns one leaf with the value {first}."})
            return
        steps.append({"at":{"start":a,"end":b},"vars":{"region":reg,"result":"cut"},"note":f"The {name} holds {first} and also a different value at row {bad[0]}, column {bad[1]}, so the call cuts it into four quadrants."})
        h=s//2
        go(r,c,h,"top-left quadrant"); go(r,c+h,h,"top-right quadrant"); go(r+h,c,h,"bottom-left quadrant"); go(r+h,c+h,h,"bottom-right quadrant")
    go(0,0,n,"whole grid"); return flat,steps
g=[[1,1,0,0],[1,1,0,0],[1,1,1,1],[1,1,1,1]]; f,s=run(g); assert len(s)==5
fill(CH,F,block(f,["start","end"],s),"@@TRACE1@@")
g=[[0,0,1,1],[0,0,1,0],[1,1,1,1],[1,1,1,1]]; f,s=run(g); assert len(s)==9
fill(CH,F,block(f,["start","end"],s),"@@TRACE2@@")
