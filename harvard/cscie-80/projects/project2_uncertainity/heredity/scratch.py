people = {
    "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
    "James": {"name": "James", "mother": None, "father": None, "trait": True},
    "Lily": {"name": "Lily", "mother": None, "father": None, "trait": False},
}

for person in people:
    print(person)

print(people["Harry"]["mother"])
one_gene = {"Harry"}
two_genes = {""}

not_in_arguments = set(people.keys()) - (one_gene.union(two_genes))

print(f"Not in arguments set {not_in_arguments}")