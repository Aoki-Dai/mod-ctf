# prog-saibo

import json
import requests
import z3
import sys

# Config
PROBLEM_FILE = "problem.json"
URL = "http://10.2.4.11:5000/submit"


def solve():
    try:
        with open(PROBLEM_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {PROBLEM_FILE} not found.")
        return

    target_state = data["final_state"]
    rows = len(target_state)
    cols = len(target_state[0])

    print(f"Grid Size: {rows}x{cols}")

    solver = z3.Solver()

    # Helper to get neighbors sum
    def get_neighbors_sum(grid, r, c):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbors.append(z3.If(grid[nr][nc], 1, 0))
                else:
                    # Boundary is dead (0)
                    pass
        return z3.Sum(neighbors)

    # Variables for t=0
    gen0 = [[z3.Bool(f"g0_{r}_{c}") for c in range(cols)] for r in range(rows)]

    # Variables for t=1
    gen1 = [[z3.Bool(f"g1_{r}_{c}") for c in range(cols)] for r in range(rows)]

    # Add transition constraints t=0 -> t=1
    for r in range(rows):
        for c in range(cols):
            alive_neighbors = get_neighbors_sum(gen0, r, c)

            # Rule:
            # Alive next if (Neighbors == 3) OR (Alive current AND Neighbors == 2)
            is_alive_next = z3.Or(
                alive_neighbors == 3, z3.And(gen0[r][c], alive_neighbors == 2)
            )

            solver.add(gen1[r][c] == is_alive_next)

    # Add transition constraints t=1 -> t=2 (target)
    for r in range(rows):
        for c in range(cols):
            alive_neighbors = get_neighbors_sum(gen1, r, c)

            is_alive_next = z3.Or(
                alive_neighbors == 3, z3.And(gen1[r][c], alive_neighbors == 2)
            )

            target_val = True if target_state[r][c] == 1 else False
            solver.add(is_alive_next == target_val)

    print("Solving...")
    if solver.check() == z3.sat:
        print("Solution found!")
        model = solver.model()
        result_grid = []
        for r in range(rows):
            row_vals = []
            for c in range(cols):
                val = model.evaluate(gen0[r][c])
                row_vals.append(1 if z3.is_true(val) else 0)
            result_grid.append(row_vals)

        # Submit
        payload = {"initial_state": result_grid}
        print("Submitting to", URL)
        try:
            res = requests.post(URL, json=payload, timeout=5)
            print("Response status:", res.status_code)
            print("Response body:", res.text)
        except Exception as e:
            print("Failed to submit:", e)
            print("Please submit manually.")
            print(json.dumps(payload))
    else:
        print("No solution found.")


if __name__ == "__main__":
    solve()
