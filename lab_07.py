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


def display_board(solution, n):
    print("  +" + "---+" * n)
    for row in range(n):
        print("  |", end="")
        for col in range(n):
            if solution[row] == col:
                print(" Q |", end="")
            else:
                print("   |", end="")
        print()
        print("  +" + "---+" * n)


for n in [4, 6, 8]:
    print(f"\nSolving {n}-Queens Problem:")
    solutions, backtrack_count = solve_n_queens(n)

    print(f"Number of solutions: {len(solutions)}")
    print(f"Number of backtracking steps: {backtrack_count}")

    for index, solution in enumerate(solutions):
        print(f"\nSolution {index + 1}:")
        display_board(solution, n)