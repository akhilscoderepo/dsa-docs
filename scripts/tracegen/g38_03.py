from common import *
CH = '38-streaming-and-temporal-state'
NAME = '03-online-prefixes.md'

def sum_trace():
    sizes = [5, 3, 8, 2, 6]
    sums = [0]
    st = [{"at": {"n": -1}, "vars": {"sums": "[0]", "call": "new", "result": "none"}, "note": "Start: no entry is recorded, so sums holds only the empty total 0."}]
    def rec(i):
        sums.append(sums[-1] + sizes[i])
        st.append({"at": {"n": i}, "vars": {"sums": str(sums), "call": f"record({sizes[i]})", "result": "none"},
                   "note": f"record adds {sizes[i]} to the last stored total and stores {sums[-1]}."})
    def query(k, note):
        n = len(sums) - 1
        r = sums[n] - sums[n - k]
        assert r == sum(sizes[n - k:n])
        st.append({"at": {"n": n - 1}, "vars": {"sums": str(sums), "call": f"lastTotal({k})", "result": str(r)}, "note": note})
        return r
    for i in range(3): rec(i)
    assert query(2, "lastTotal(2) computes sums[3] - sums[1] = 16 - 5 = 11, which equals 3 + 8.") == 11
    rec(3); rec(4)
    assert query(4, "lastTotal(4) computes sums[5] - sums[1] = 24 - 5 = 19.") == 19
    assert query(5, "lastTotal(5) computes sums[5] - sums[0] = 24 - 0 = 24, the total of all entries.") == 24
    return block([str(s) for s in sizes], ["n"], st)

def prod_trace():
    vals = [4, 3, 0, 5, 2, 6]
    products = [1]; zero = -1
    st = [{"at": {"n": -1, "zero": -1}, "vars": {"products": "[1]", "call": "new", "result": "none"}, "note": "Start: no entry is recorded and the list holds the empty product 1."}]
    def rec(i):
        nonlocal products, zero
        v = vals[i]
        if v == 0:
            products = [1]; zero = i
            note = "A zero has no inverse, so record discards the list and keeps only the empty product 1. The pointer zero moves here."
        else:
            products.append(products[-1] * v)
            note = f"record multiplies the last stored product by {v} and stores {products[-1]}."
        st.append({"at": {"n": i, "zero": zero}, "vars": {"products": str(products), "call": f"record({v})", "result": "none"}, "note": note})
    def query(i, k, note):
        m = len(products) - 1
        r = 0 if k > m else products[m] // products[m - k]
        assert r == __import__("math").prod(vals[i + 1 - k:i + 1])
        st.append({"at": {"n": i, "zero": zero}, "vars": {"products": str(products), "call": f"lastProduct({k})", "result": str(r)}, "note": note})
        return r
    rec(0); rec(1)
    assert query(1, 2, "lastProduct(2) computes 12 / 1 = 12, which equals 4 * 3.") == 12
    rec(2); rec(3); rec(4); rec(5)
    assert query(5, 3, "lastProduct(3) computes 60 / 1 = 60, which equals 5 * 2 * 6.") == 60
    assert query(5, 2, "lastProduct(2) computes 60 / 5 = 12, which equals 2 * 6.") == 12
    assert query(5, 4, "Four entries reach back to the zero, since only three entries follow it, so the answer is 0 without any division.") == 0
    return block([str(v) for v in vals], ["n", "zero"], st)

fill(CH, NAME, sum_trace(), "@@TRACE1@@")
fill(CH, NAME, prod_trace(), "@@TRACE2@@")
