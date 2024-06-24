puzzle = [
    [4, 3, 5, 2, 6, 9, 7, 8, 1],
    [6, 8, 2, 5, 7, 1, 4, 9, 3],
    [1, 9, 7, 8, 3, 4, 5, 6, 2],
    [8, 2, 6, 1, 9, 5, 3, 4, 7],
    [5, 2, 4],
    [], []
]

def consistent(puzzle):
    print(f"Running consistent program ..")
    for row in puzzle:
        print(f"Checking row")
        observed = set()
        for value in row:
            print(f"Value: {value}")
            if value in observed:
                print(f"False")
                return False
            observed.add(value)

    for col in puzzle:
        print(f"Checking Col")
        observed = set()
        for value in col:
            print(f"Value: {value}")
            if value in observed:
                print(f"False")
                return False
            observed.add(value)
            
    # # Checking column
    # for col in range(0, 9):
    #     print(f"Checking column")
    #     observed = set()
    #     for row in puzzle:
    #         print(f"Value {row[col]}")
    #         if row[col] in observed:
    #             print(f"False")
    #             return False
    #         observed.add(row[col])

    print(f"True")
    return True

print(f"Run")
consistent(puzzle)
