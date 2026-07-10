import streamlit as st
import heapq

# -------------------------------
# Union Find for Kruskal
# -------------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# -------------------------------
# Kruskal Algorithm
# -------------------------------
def kruskal(n, edges):
    edges.sort()

    uf = UnionFind(n)

    mst = []
    cost = 0

    for w, u, v in edges:

        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


# -------------------------------
# Prim Algorithm
# -------------------------------
def prim(n, adj):

    INF = float("inf")

    key = [INF] * n
    parent = [-1] * n
    visited = [False] * n

    pq = []

    key[0] = 0

    heapq.heappush(pq, (0, 0))

    mst = []
    cost = 0

    while pq:

        w, u = heapq.heappop(pq)

        if visited[u]:
            continue

        visited[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj[u]:

            if not visited[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(
    page_title="Minimum Spanning Tree Visualizer",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 Minimum Spanning Tree")
st.subheader("Kruskal's Algorithm & Prim's Algorithm")

st.markdown("Enter graph edges below.")

n = st.number_input(
    "Number of Vertices",
    min_value=2,
    value=7
)

edge_text = st.text_area(
    "Edges (Format: source destination weight)",
    value="""0 1 7
0 3 5
1 2 8
1 3 9
1 4 7
2 4 5
3 4 15
3 5 6
4 5 8
4 6 9
5 6 11""",
    height=220
)

if st.button("Run Algorithms"):

    edges = []
    adj = {i: [] for i in range(n)}

    try:

        for line in edge_text.strip().split("\n"):

            u, v, w = map(int, line.split())

            edges.append((w, u, v))

            adj[u].append((v, w))
            adj[v].append((u, w))

        kruskal_mst, kruskal_cost = kruskal(n, edges.copy())
        prim_mst, prim_cost = prim(n, adj)

        col1, col2 = st.columns(2)

        with col1:

            st.success("Kruskal's Algorithm")

            st.table(
                {
                    "Edge": [f"{u} - {v}" for u, v, w in kruskal_mst],
                    "Weight": [w for u, v, w in kruskal_mst],
                }
            )

            st.metric("Total Cost", kruskal_cost)

        with col2:

            st.success("Prim's Algorithm")

            st.table(
                {
                    "Edge": [f"{u} - {v}" for u, v, w in prim_mst],
                    "Weight": [w for u, v, w in prim_mst],
                }
            )

            st.metric("Total Cost", prim_cost)

    except Exception as e:

        st.error(f"Invalid Input\n\n{e}")
