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
    Or(AKnight,
       AKnave)
)
knowledge0.add(And(AKnave, AKnave))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnave,
       AKnight),
    Or(BKnight,
       BKnave)
)
knowledge1.add(And(BKnave,AKnave))
knowledge1.add(Or(And(AKnave,BKnight),
                  And(AKnight,BKnight),
                  And(AKnight,BKnave)))



# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnave,
       AKnight),
    Or(BKnight,
       BKnave)
)
# Opposite knight/knave polarity
# This can be accomplished through (Or, And)s but more writing, so I skipped that step
knowledge2.add(Implication(AKnight, BKnight))
knowledge2.add(Implication(AKnave, BKnight))
knowledge2.add(Implication(BKnight, AKnave))
knowledge2.add(Implication(BKnave, AKnave))



# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnave,
       AKnight),
    Or(BKnight,
       BKnave),
    Or(CKnight,
       CKnave)
)

# Statement 1 & 2, hard to address without any humam logic
knowledge3.add(Implication(AKnight, BKnave))
knowledge3.add(BKnave)

# Statement 4
knowledge3.add(Implication(CKnave, AKnave))
knowledge3.add(Implication(CKnight, AKnight))

# Statement 3
knowledge3.add(Implication(BKnight, CKnave))
knowledge3.add(Implication(BKnave, CKnight))






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
