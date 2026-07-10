import streamlit as st
import heapq

# ----------------------------
# Dijkstra Algorithm
# ----------------------------
def dijkstra(graph, source):
    n = len(graph)
    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# ----------------------------
# Reconstruct Path
# ----------------------------
def reconstruct_path(prev, source, target):
    path = []

    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(
    page_title="Dijkstra Algorithm",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Dijkstra Shortest Path Algorithm")

st.markdown(
    "Enter the graph edges below in the format:\n\n"
    "`source destination weight`"
)

num_vertices = st.number_input(
    "Number of Vertices",
    min_value=2,
    value=6,
    step=1
)

source = st.number_input(
    "Source Vertex",
    min_value=0,
    max_value=int(num_vertices - 1),
    value=0
)

edge_text = st.text_area(
    "Graph Edges",
    value="""0 1 4
0 2 1
1 3 1
2 1 2
2 3 5
3 4 3
4 5 2""",
    height=220
)

if st.button("Run Dijkstra"):

    graph = {i: [] for i in range(num_vertices)}

    try:
        for line in edge_text.strip().split("\n"):
            u, v, w = map(int, line.split())
            graph[u].append((v, w))

        dist, prev = dijkstra(graph, source)

        st.success("Shortest Paths Computed Successfully!")

        result = []

        for v in range(num_vertices):

            path = reconstruct_path(prev, source, v)

            path_str = " → ".join(map(str, path)) if path else "No Path"

            distance = dist[v] if dist[v] != float("inf") else "INF"

            result.append({
                "Vertex": v,
                "Distance": distance,
                "Path": path_str
            })

        st.table(result)

    except Exception as e:
        st.error(f"Invalid Input!\n\n{e}")
