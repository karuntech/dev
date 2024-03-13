import scipy.optimize

result = scipy.optimize.linprog(
    [-400, -500],
    A_ub = [[2, 3]],
    b_ub = [12],
    bounds = [(0, 4), [0, 10]]
)

if result.success:
    print(f"C1: {round(result.x[0], 2)} acres")
    print(f"C2: {round(result.x[1], 2)} acres")
else:
    print("No solution")