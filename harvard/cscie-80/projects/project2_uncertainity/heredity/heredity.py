import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # raise NotImplementedError
    print(f"One Gene:", one_gene)
    print(f"Two Genes:", two_genes)
    print(f"Have Trait:", have_trait)
    print(f"------------")

    # 1) One gene
    p_one_gene_all_members_in_set = 1
    for person in one_gene:
        print(f"Computing probability for {person} to have one gene")
        # if this person is a parent, just use the probablity from the PROBS dictionary (unconditional)
        if people[person]["mother"] == None:
            p_one_gene = PROBS["gene"][1]
        else:
            # Determine the mother's and father's gene count from the arguments
            mother_gene = 0
            father_gene = 0
            if people[person]["mother"] in one_gene:
                mother_gene = 1
            elif people[person]["mother"] in two_genes:
                mother_gene = 2
            else:
                mother_gene = 0

            if people[person]["father"] in one_gene:
                father_gene = 1
            elif people[person]["father"] in two_genes:
                father_gene = 2
            else:
                father_gene = 0

            # What are the chances for this person to have 1 gene?
            # He can get one from mother and none from father or one from father and none from mother
            # One from mother and none from Father
            # One from mother
            if mother_gene == 0:
                p_mother_one = PROBS["mutation"]
            elif mother_gene == 1:
                p_mother_one = .5
            else:
                p_mother_one = 1 * (1 - PROBS["mutation"])

            # None from father
            if father_gene == 0:
                p_father_none = 1 * (1 - PROBS["mutation"])
            if father_gene == 1:
                p_father_none = .5
            if father_gene == 2:
                p_father_none = 1 * PROBS["mutation"]

            p_mother_one_father_none = p_mother_one * p_father_none
            print(f"p_mother_one_father_none: {p_mother_one_father_none}")

            # One from father and none from mother
            # One from father
            if father_gene == 0:
                p_father_one = PROBS["mutation"]
            elif father_gene == 1:
                p_father_one = 0.5
            else:
                p_father_one = 1 * (1 - PROBS["mutation"])
            # None from mother
            if mother_gene == 0:
                p_mother_none = 1 * (1 - PROBS["mutation"])
            if mother_gene == 1:
                p_mother_none = 0.5
            if mother_gene == 2:
                p_mother_none = 1 * PROBS["mutation"]

            p_father_one_mother_none = p_father_one * p_mother_none
            print(f"p_father_one_mother_none: {p_father_one_mother_none}")

            # Probablity of mother one and father none OR father one and mother none
            p_one_gene = p_mother_one_father_none + p_father_one_mother_none

        p_one_gene_all_members_in_set = p_one_gene_all_members_in_set * p_one_gene

    # 2) Two genes
    p_two_gene_all_members_in_set = 1
    for person in two_genes:
        print(f"Computing probability for {person} to have two genes")
        # if this person is parent, just use the probablity from the PROBS dictionary (unconditional)
        if people[person]["mother"] == None:
            p_two_genes = PROBS["gene"][2]
        else:
            # Determine the mother's and father's gene count from the arguments. Need to move this to function
            mother_gene = 0
            father_gene = 0
            if people[person]["mother"] in one_gene:
                mother_gene = 1
            elif people[person]["mother"] in two_genes:
                mother_gene = 2
            else:
                mother_gene = 0

            if people[person]["father"] in one_gene:
                father_gene = 1
            elif people[person]["father"] in two_genes:
                father_gene = 2
            else:
                father_gene = 0

            # What are the changes this person will have two genes?
            # The person should receive one from each parent
            # One from mother
            if mother_gene == 0:
                p_mother_one = PROBS["mutation"]
            elif mother_gene == 1:
                p_mother_one = 0.5
            else:
                p_mother_one = 1 * (1 - PROBS["mutation"])

            # One from father
            if father_gene == 0:
                p_father_one = PROBS["mutation"]
            elif father_gene == 1:
                p_father_one = 0.5
            else:
                p_father_one = 1 * (1 - PROBS["mutation"])

            p_two_genes = p_mother_one * p_father_one

        p_two_gene_all_members_in_set = p_two_gene_all_members_in_set * p_two_genes

    # 3) Have Trait
    p_have_trait_all_members_in_set = 1
    for person in have_trait:
        print(f"Computing probability for {person} to have the trait")
        # Trait is affected by the number of genes this person has
        if person in one_gene:
            p_no_of_gene = 1
        elif person in two_genes:
            p_no_of_gene = 2
        else:
            p_no_of_gene = 0

        p_have_trait = PROBS["trait"][p_no_of_gene][True]

        p_have_trait_all_members_in_set = p_have_trait_all_members_in_set * p_have_trait

    # 4) No genes (everyone not in one_gene or two_genes)
    persons_not_in_gene_arguments = set(people.keys()) - (one_gene.union(two_genes))
    p_no_genes_all_members_in_set = 1
    for person in persons_not_in_gene_arguments:
        print(f"Computing probability for {person} to have no genes")
        # if this person is parent, just use the probablity from the PROBS dictionary (unconditional)
        if people[person]["mother"] == None:
            p_no_gene = PROBS["gene"][0]
        else:
            # Determine the mother's and father's gene count from the arguments.( Move this to a function)
            mother_gene = 0
            father_gene = 0
            if people[person]["mother"] in one_gene:
                mother_gene = 1
            elif people[person]["mother"] in two_genes:
                mother_gene = 2
            else:
                mother_gene = 0

            if people[person]["father"] in one_gene:
                father_gene = 1
            elif people[person]["father"] in two_genes:
                father_gene = 2
            else:
                father_gene = 0

            # What are the chances this person will have 0 genes.
            # He has to receive none from each of the parent
            # None from mother
            if mother_gene == 0:
                p_mother_none = 1 * (1 - PROBS["mutation"])
            elif mother_gene == 1:
                p_mother_none = 0.5
            else:
                p_mother_none = 1 * PROBS["mutation"]

            # None from father
            if father_gene == 0:
                p_father_none = 1 * (1 - PROBS["mutation"])
            elif father_gene == 1:
                p_father_none = 0.5
            else:
                p_father_none = 1 * PROBS["mutation"]

            p_no_gene = p_mother_none * p_father_none

        p_no_genes_all_members_in_set = p_no_genes_all_members_in_set * p_no_gene

    # 5) Have no trait
    persons_not_in_trait_arguments = set(people.keys()) - have_trait
    p_no_trait_all_members_in_set = 1
    for person in persons_not_in_trait_arguments:
        print(f"Computing probability for {person} to have no trait")
        # Trait is affected by the number of genes this person has
        if person in one_gene:
            p_no_of_gene = 1
        elif person in two_genes:
            p_no_of_gene = 2
        else:
            p_no_of_gene = 0

        p_no_trait = PROBS["trait"][p_no_of_gene][False]

        p_no_trait_all_members_in_set = p_no_trait_all_members_in_set * p_no_trait

    # No multiply al the probablities.

    joint_probability_value = (
        p_one_gene_all_members_in_set
        * p_two_gene_all_members_in_set
        * p_have_trait_all_members_in_set
        * p_no_genes_all_members_in_set
        * p_no_trait_all_members_in_set
    )

    print(f"The joint probablity computed: {joint_probability_value}")

    return joint_probability_value

    # Determine the persons for which we need to compute No genes and No traits
    # pretty completed
    # when you map it out.. may be simply it
    # lot of different cases.. based on who the mother.. and father and count
    # group it together more clean to read
    # conider than

    # mutation is related to gene count

    # Take a borad approach, and then work through the logic
    # all the differnt cases.. try to work out smaller


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # raise NotImplementedError
    for person in probabilities:
        # Update gene distribution
        for g_person in one_gene:
            if g_person == person:
                probabilities[person]["gene"][1] += p
        for g_person in two_genes:
            if g_person == person:
                probabilities[person]["gene"][2] += p
        # Update trait
        for t_person in have_trait:
            if t_person == person:
                probabilities[person]["trait"][True] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # raise NotImplementedError
    # Normalize gene
    for person in probabilities:
        p_gene_1 = person["gene"][1]
        p_gene_2 = person["gene"][2]
        p_gene_0 = person["gene"][0]
        ratio_1_2 = p_gene_2 / p_gene_1
        ratio_1_0 = p_gene_0 / p_gene_1
        new_p_gene_1 = 1 / ( 1 + ratio_1_2 + ratio_1_0 )
        new_p_gene_2 = ratio_1_2 * new_p_gene_1
        new_p_gene_0 = ratio_1_0 * new_p_gene_1
        probabilities[person]["gene"][1] = new_p_gene_1
        probabilities[person]["gene"][2] = new_p_gene_2
        probabilities[person]["gene"][0] = new_p_gene_0

    # Normalie trait
    for person in probabilities:
        # Find the relative propotion of True and False
        p_true = person["trait"][True]
        p_false = person["trait"][False]
        ratio = p_false / p_true
        # For the probabilities to sum to 1 propotionally
        new_p_true = 1 / (1 + ratio)
        new_p_false = ratio * new_p_true
        probabilities[person]["trait"][True] = new_p_true
        probabilities[person]["trait"][False] = new_p_false


if __name__ == "__main__":
    main()
