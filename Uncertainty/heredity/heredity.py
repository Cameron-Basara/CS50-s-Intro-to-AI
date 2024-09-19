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
    joint_p = 1  # Start with total probability of 1

    for person, info in people.items():
        # Determine gene count for the person
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        # Determine if person has the trait
        has_trait = person in have_trait

        # Calculate gene probability
        if info["mother"] is None and info["father"] is None:
            # No parental information, use unconditional probability
            gene_p = PROBS["gene"][gene_count]
        else:
            # Calculate probability based on parents' genes
            mom = info["mother"]
            dad = info["father"]

            # Probability that mother and father pass on the gene
            mom_p = calculate_parent_prob(mom, one_gene, two_genes)
            dad_p = calculate_parent_prob(dad, one_gene, two_genes)

            # Calculate the probability that the child has `gene_count` genes
            if gene_count == 2:
                gene_p = mom_p * dad_p  # Both parents pass on the gene
            elif gene_count == 1:
                gene_p = (mom_p * (1 - dad_p)) + (dad_p * (1 - mom_p))  # One parent passes the gene
            else:
                gene_p = (1 - mom_p) * (1 - dad_p)  # Neither parent passes the gene

        # Calculate trait probability for the person
        trait_p = PROBS["trait"][gene_count][has_trait]

        # Multiply the gene and trait probabilities to the joint probability
        joint_p *= gene_p * trait_p

    return joint_p

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Iterate over each person in the probabilities dictionary
    for person in probabilities:
        # Determine the number of gene copies the person has
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        # Determine if the person has the trait
        has_trait = person in have_trait

        # Update the gene distribution for the person
        probabilities[person]["gene"][gene_count] += p

        # Update the trait distribution for the person
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene distribution
        gene_total = sum(probabilities[person]["gene"].values())
        if gene_total > 0:
            for gene_count in probabilities[person]["gene"]:
                probabilities[person]["gene"][gene_count] /= gene_total
        
        # Normalize trait distribution
        trait_total = sum(probabilities[person]["trait"].values())
        if trait_total > 0:
            for has_trait in probabilities[person]["trait"]:
                probabilities[person]["trait"][has_trait] /= trait_total



def calculate_parent_prob(parent, one_gene, two_genes):
    """
    Calculate the probability that a parent passes on the gene to their child.
    """
    # Determine how many copies of the gene the parent has
    if parent in two_genes:
        return 1 - PROBS["mutation"]  # The parent has two copies and passes it on unless it mutates
    elif parent in one_gene:
        return 0.5  # The parent has one copy, so 50% chance of passing it on
    else:
        return PROBS["mutation"]  # The parent has no copies, so it mutates to pass it on


if __name__ == "__main__":
    main()
