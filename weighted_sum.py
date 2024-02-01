# Use enumerator and a function to compute weighted sum

def weighted_sum(weights, values, missing=0): # the optional parameter missing will have the default value of 0
    sum = 0
    for i, val in enumerate(values):
        sum += val * (weights[i] if i < len(weights) else missing)
    return sum
    
weights = [1, 2, 3]
values = [1, 2, 3, 4]

print(weighted_sum(weights, values))