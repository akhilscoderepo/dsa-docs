from common import *
CH = '37-iterators-encodings-and-versioned-state'
NAME = '02-nested-iteration.md'

def page_trace():
    pages = [["a", "b"], [], ["c"], []]
    page = 0; col = 0
    cells = ["[a,b]", "[]", "[c]", "[]"]
    st = [{"at": {"page": 0}, "vars": {"col": 0, "call": "new", "result": "none"}, "note": "Start: the position is page 0, column 0, and nothing is settled yet."}]
    def settle():
        nonlocal page, col
        while page < len(pages) and col == len(pages[page]):
            page += 1; col = 0
    def has():
        settle(); return page < len(pages)
    def nxt():
        nonlocal col
        settle(); assert page < len(pages)
        v = pages[page][col]; col += 1; return v
    def log(call, res, note):
        st.append({"at": {"page": page}, "vars": {"col": col, "call": call, "result": res}, "note": note})
    r = has(); log("hasNext()", str(r).lower(), "hasNext finds a at column 0 of page 0 and returns true.")
    r = nxt(); log("next()", r, "next returns a and moves col to 1.")
    r = nxt(); log("next()", r, "next returns b and moves col to 2, which equals the size of page 0. The position stays on page 0 until a call needs more.")
    r = has(); log("hasNext()", str(r).lower(), "hasNext passes page 0 because col equals its size, passes the empty page 1, and stops at page 2 with col 0. It returns true.")
    assert page == 2 and col == 0
    r = nxt(); log("next()", r, "next returns c and moves col to 1.")
    r = has(); log("hasNext()", str(r).lower(), "hasNext passes page 2 and the empty page 3, reaches page 4 (one past the last page) and returns false.")
    assert not r and page == 4
    return block(cells, ["page"], st)

def nested_trace():
    root = ["x", [], [["y"], "z"]]
    stack = [[root, 0]]  # [list, index of next item]
    ready = None
    cells = ["x", "[]", "[[y],z]"]
    st = [{"at": {"top": 0}, "vars": {"depth": 1, "ready": "none", "call": "new", "result": "none"}, "note": "Start: the stack holds one cursor for the outer list, and nothing is taken."}]
    def has():
        nonlocal ready
        while ready is None and stack:
            lst, i = stack[-1]
            if i == len(lst):
                stack.pop(); continue
            stack[-1][1] += 1
            o = lst[i]
            if isinstance(o, list): stack.append([o, 0])
            else: ready = o
        return ready is not None
    def nxt():
        nonlocal ready
        assert has(); r = ready; ready = None; return r
    def log(call, res, note):
        top = stack[0][1] if stack else len(root)
        st.append({"at": {"top": top}, "vars": {"depth": len(stack), "ready": ready if ready else "none", "call": call, "result": res}, "note": note})
    r = has(); log("hasNext()", str(r).lower(), "hasNext takes x from the outer list, stores it in ready and returns true.")
    r = nxt(); log("next()", r, "next returns x and clears ready.")
    r = has(); log("hasNext()", str(r).lower(), "hasNext opens the empty list and pops it, then opens [[y],z] and [y], and finds y at depth 3. It returns true.")
    assert len(stack) == 3
    r = nxt(); log("next()", r, "next returns y and clears ready.")
    r = has(); log("hasNext()", str(r).lower(), "hasNext pops the finished cursor of [y] and finds z at depth 2. It returns true.")
    assert len(stack) == 2
    r = nxt(); log("next()", r, "next returns z and clears ready.")
    r = has(); log("hasNext()", str(r).lower(), "hasNext pops the two remaining cursors, reaches depth 0 and returns false.")
    assert not r and not stack
    return block(cells, ["top"], st)

fill(CH, NAME, page_trace(), "@@TRACE1@@")
fill(CH, NAME, nested_trace(), "@@TRACE2@@")
