import streamlit as st

# -------------------------------------------------------
# Matrix Chain Multiplication using Dynamic Programming
# -------------------------------------------------------
def matrix_chain_order(dims):
    n = len(dims) - 1

    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):

        for i in range(1, n - l + 2):

            j = i + l - 1

            m[i][j] = float("inf")

            for k in range(i, j):

                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


# -------------------------------------------------------
# Print Optimal Parenthesization
# -------------------------------------------------------
def print_optimal_parens(s, i, j):

    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# -------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------
st.set_page_config(
    page_title="Matrix Chain Multiplication",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Matrix Chain Multiplication")
st.subheader("Dynamic Programming Approach")

st.write(
    "Enter the matrix dimensions separated by commas.\n\n"
    "**Example:** 10,30,5,60,10"
)

dimension_input = st.text_input(
    "Matrix Dimensions",
    value="10,30,5,60,10"
)

if st.button("Compute"):

    try:

        dims = [int(x.strip()) for x in dimension_input.split(",")]

        if len(dims) < 2:
            st.error("Please enter at least two dimensions.")
            st.stop()

        n = len(dims) - 1

        st.subheader("Matrices")

        matrix_table = []

        for i in range(n):
            matrix_table.append({
                "Matrix": f"A{i+1}",
                "Dimension": f"{dims[i]} × {dims[i+1]}"
            })

        st.table(matrix_table)

        m, s = matrix_chain_order(dims)

        st.success("Computation Completed Successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Minimum Scalar Multiplications",
                m[1][n]
            )

        with col2:
            st.metric(
                "Number of Matrices",
                n
            )

        st.subheader("Optimal Parenthesization")

        st.code(
            print_optimal_parens(s, 1, n),
            language="text"
        )

        st.subheader("Dynamic Programming Cost Table")

        table = []

        for i in range(1, n + 1):

            row = {"Matrix": f"A{i}"}

            for j in range(1, n + 1):

                if j < i:
                    row[f"A{j}"] = "---"
                else:
                    row[f"A{j}"] = m[i][j]

            table.append(row)

        st.table(table)

        st.subheader("Time & Space Complexity")

        st.info("""
Time Complexity : **O(n³)**

Space Complexity : **O(n²)**

Where **n** is the number of matrices.
""")

    except ValueError:
        st.error("Please enter only integers separated by commas.")
