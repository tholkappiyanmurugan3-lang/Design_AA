import streamlit as st


def is_safe(board, row, col):
    for i in range(row):
        # Same column
        if board[i] == col:
            return False

        # Same diagonal
        if abs(board[i] - col) == abs(i - row):
            return False

    return True


def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board.copy())
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack_count[0] += 1
                backtrack(row + 1)
                board[row] = -1

    backtrack(0)
    return solutions, backtrack_count[0]


def board_to_html(solution, n):
    html = """
    <table style="border-collapse: collapse;">
    """

    for row in range(n):
        html += "<tr>"
        for col in range(n):
            color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"

            if solution[row] == col:
                cell = "♛"
            else:
                cell = ""

            html += f"""
            <td style="
                width:45px;
                height:45px;
                text-align:center;
                font-size:28px;
                border:1px solid black;
                background:{color};
            ">
            {cell}
            </td>
            """
        html += "</tr>"

    html += "</table>"
    return html


# ---------------- Streamlit UI ----------------

st.set_page_config(
    page_title="N-Queens Solver",
    page_icon="♛",
    layout="wide"
)

st.title("♛ N-Queens Problem Solver")
st.write("Solve the N-Queens problem using Backtracking.")

n = st.slider(
    "Select Number of Queens",
    min_value=4,
    max_value=10,
    value=8
)

if st.button("Solve"):
    with st.spinner("Finding all solutions..."):

        solutions, backtrack_count = solve_n_queens(n)

    st.success("Completed!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Solutions", len(solutions))

    with col2:
        st.metric("Backtracking Steps", backtrack_count)

    st.divider()

    show = st.number_input(
        "Show first N solutions",
        min_value=1,
        max_value=len(solutions),
        value=min(5, len(solutions))
    )

    for i in range(show):
        st.subheader(f"Solution {i+1}")
        st.markdown(
            board_to_html(solutions[i], n),
            unsafe_allow_html=True
        )
