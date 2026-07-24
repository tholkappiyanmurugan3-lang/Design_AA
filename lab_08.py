import streamlit as st
from itertools import permutations

INF = float("inf")


def tsp_brute_force(cost, n):
    cities = list(range(1, n))
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        c = 0
        for i in range(n):
            c += cost[path[i]][path[i + 1]]

        if c < best_cost:
            best_cost = c
            best_path = path

    return best_path, best_cost


# ---------------- Streamlit UI ----------------

st.set_page_config(
    page_title="Travelling Salesman Problem",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Travelling Salesman Problem (Brute Force)")
st.write("Find the minimum-cost Hamiltonian cycle.")

cities = ["A", "B", "C", "D", "E"]
n = 5

default_matrix = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

st.subheader("Cost Matrix")

cost = []

for i in range(n):
    cols = st.columns(n)
    row = []

    for j in range(n):

        if i == j:
            cols[j].markdown("**∞**")
            row.append(INF)

        else:
            value = cols[j].number_input(
                f"{cities[i]}→{cities[j]}",
                min_value=1,
                value=default_matrix[i][j],
                key=f"{i}{j}"
            )
            row.append(value)

    cost.append(row)

if st.button("Find Optimal Tour"):

    best_path, best_cost = tsp_brute_force(cost, n)

    st.success("Optimal Tour Found!")

    st.metric("Minimum Cost", best_cost)

    tour = " → ".join(cities[i] for i in best_path)

    st.subheader("Optimal Tour")
    st.info(tour)

    st.subheader("Path Verification")

    for i in range(n):
        u = best_path[i]
        v = best_path[i + 1]

        st.write(
            f"**{cities[u]} → {cities[v]}** : {cost[u][v]}"
        )

    st.subheader("Cost Matrix")

    table = []

    for i in range(n):
        row = {}
        row["City"] = cities[i]

        for j in range(n):
            if cost[i][j] == INF:
                row[cities[j]] = "∞"
            else:
                row[cities[j]] = cost[i][j]

        table.append(row)

    st.table(table)
