from utils import init_table, search, heuristic_one, heuristic_two, count_inversions


import time

from scipy.optimize import brentq
def effective_branching_factor(N: int, d: int) -> float:
    if d == 0:
        return 0
    if N <= d:
        return 1.0
    func = lambda b: sum(b**i for i in range(d+1)) - (N + 1)
    return brentq(func, 1.0, max(N + 1, 2.0), xtol=1e-4)
num_tests = 100



data = []
heuristics = {"one": heuristic_one, "two": heuristic_two}
depths = [2, 4, 8, 12, 16, 18, 20, 22, 24, 26]

for dep in depths:
    for i in range(10):
        table, desired_state = init_table(9, dep)
        assert count_inversions(table) % 2 == 0, "init_table gerou estado insolúvel"
        print(table)
        print(desired_state)

        for key in heuristics.keys():
            b=[1]
            start = time.perf_counter()

            solved, path = search(table, desired_state, b, heuristic=heuristics[key])
            d = len(path) - 1
            b_star = effective_branching_factor(b[0], d)

            print(f"Número de movimentos: {len(path)-1}")
            end = time.perf_counter()

            cell = {"tempo_exec": end-start, "b*": b_star, "sol": str(path), "heuristic": key, "depth": dep}

            data.append(cell)
            print(f"Tempo de execução: {end-start:.2f}")
            print(f"b* {b_star}z")

import pandas as pd

df = pd.DataFrame(data)
df.to_csv("experiments_result.csv", index=False)
