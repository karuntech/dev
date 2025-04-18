from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # If A is a Knight, he cannot be a Knave and vice versa
    Biconditional(AKnight, Not(AKnave)),
    # If A is a Knight, he is telling the truth
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a Knave, he is not telling the truth
    Implication(AKnave, Not(And(AKnight, AKnave))),
)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # If A is a Knight, he cannot be a Knave and vice versa
    Biconditional(AKnight, Not(AKnave)),
    # If B is a Knight, he cannot be a Knave and vice versa
    Biconditional(BKnight, Not(BKnave)),
    # If A is a Knight, he is telling the truth (both A and B are Knaves)
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a Knave, he is not telling the truth
    Implication(AKnave, Not(And(AKnave, BKnave))),
)
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # If A is a Knight, he cannot be a Knave and vice versa
    Biconditional(AKnight, Not(AKnave)),
    # If B is a Knight, he cannot be a Knave and vice versa
    Biconditional(BKnight, Not(BKnave)),
    # A says A and B are of the same kind. That means either Knights or Knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # B says A and B are of different kind. That means when one is a Knight, the other is a Knave
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, And(AKnight, AKnave)),
    Implication(BKnight, And(AKnave, Not(AKnave))),
    Implication(BKnave, Not(And(AKnight, AKnave))),
    Implication(BKnight, Not(And(AKnave, Not(AKnave)))),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
