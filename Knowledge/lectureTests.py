import random

# # On the topic of classes
# class ComplexClass():
#     def __init__(self, real, im):
#         self.r = real
#         self.i = im
#         self.comb = "%lf + %lfi" % (real, im)
#         self.l = []
#     def apList(self, object):
#         self.l.append(object)


# print(ComplexClass(1,2).r)

# val = ComplexClass(1.5,4.0)
# print(val.comb)

# val1 = ComplexClass(1,1)
# val1.apList(1)

# print(val1.l)

# class Bag:
#     def __init__(self):
#         self.data = []

#     def add(self, x):
#         self.data.append(x)

#     def addtwice(self, x):
#         self.add(x)
#         self.add(x)
    
#     def returner(self):
#         return self.data

# b = Bag()
# b.addtwice(1)

# print(b.returner())

# import termcolor as t
# import sys


# text = t.colored("Hello, World!", "red", attrs=["reverse", "blink"])
# print(text)
# t.cprint("Hello, World!", "green", "on_red")

# print_red_on_cyan = lambda x: t.cprint(x, "red", "on_cyan")
# print_red_on_cyan("Hello, World!")
# print_red_on_cyan("Hello, Universe!")

# for i in range(10):
#     t.cprint(i, "magenta", end=" ")

# t.cprint("Attention!", "red", attrs=["bold"], file=sys.stderr)


# class MinesweeperAI():
#     """
#     Minesweeper game player
#     """

#     def __init__(self, height=8, width=8):

#         # Set initial height and width
#         self.height = height
#         self.width = width

#         # Keep track of which cells have been clicked on
#         self.moves_made = set()

#         # Keep track of cells known to be safe or mines
#         self.mines = set()
#         self.safes = set()

#         # List of sentences about the game known to be true
#         self.knowledge = []

#     def mark_mine(self, cell):
#         """
#         Marks a cell as a mine, and updates all knowledge
#         to mark that cell as a mine as well.
#         """
#         self.mines.add(cell)
#         for sentence in self.knowledge:
#             sentence.mark_mine(cell)

#     def mark_safe(self, cell):
#         """
#         Marks a cell as safe, and updates all knowledge
#         to mark that cell as safe as well.
#         """
#         self.safes.add(cell)
#         for sentence in self.knowledge:
#             sentence.mark_safe(cell)

#     def add_knowledge(self, cell, count):
#         """
#         Called when the Minesweeper board tells us, for a given
#         safe cell, how many neighboring cells have mines in them.

#         This function should:
#             1) mark the cell as a move that has been made
#             2) mark the cell as safe
#             3) add a new sentence to the AI's knowledge base
#                based on the value of `cell` and `count`
#             4) mark any additional cells as safe or as mines
#                if it can be concluded based on the AI's knowledge base
#             5) add any new sentences to the AI's knowledge base
#                if they can be inferred from existing knowledge
#         """
#         raise NotImplementedError

#     def make_safe_move(self):
#         """
#         Returns a safe cell to choose on the Minesweeper board.
#         The move must be known to be safe, and not already a move
#         that has been made.

#         This function may use the knowledge in self.mines, self.safes
#         and self.moves_made, but should not modify any of those values.
#         """
#         # First, check if any moves in safe
#         for s in self.safes:
#             if s not in self.moves_made:
#                 return s

#     def make_random_move(self):
#         """
#         Returns a move to make on the Minesweeper board.
#         Should choose randomly among cells that:
#             1) have not already been chosen, and
#             2) are not known to be mines
#         """
#         pmoves = set()
        
#         if len(self.moves_made) != 0:
#             for s in self.moves_made:
#                 pmoves.add(s)
#         if len(self.mines) != 0:
#             for s in self.mines:
#                 pmoves.add(s)
        
#         while(True):
#             i = random.randrange(0,7)
#             j = random.randrange(0,7)
#             if (i,j) not in pmoves:
#                 return (i,j)





# newClass = MinesweeperAI()
# newClass.mark_mine((0,2))
# s = newClass.make_random_move()
# print(s)

# print(range(*(1,4)))

a = set((1,2,3))
b = set((0,1,4,5))
print(f"Union: {a | b}, Intersection: {a & b}, Difference: {a - b}, Symm Diff: {a ^ b}")

cell1 = [set(((1,2),(0,2),(2,3))), 1]
cell2 = [set(((1,0),(0,2),(2,3))), 2]
inte = cell1[0]
inte &= cell2[0]
print(f"symm diff {cell1[0] ^ cell2[0]}, inter update {inte}, ")

# dealing with sets

# case 1: No interaction -> then just add knowledge sentance

# case 2: All interaction -> remove repeats, but shouldnt occur unless created from a seperate operation
c1 = set((1,1),(0,0))
c2 = set((1,1),(0,0))

if (c1 & c2) == c1:
    # remove c2 from knowledge base, keep added square etc
    c2.clear() # our case will just be removing c2 from knowledge base

# case 3: Interaction 1 >, and cells that are not overallaping is SMALLER
# Than the amount of BOMBS in BOTH

"""
Pseudocode:

Compare the two sets and note which elements are the same

Given case 3: we have 3 possible scenarios
A) Bombs are planted in non-overlapping sections, given the quantity of bombs
is greater than 1
B) Bombs are planted in both overlapping sections and non-overlapping sections
C) Bombs are solely planted in overlapping sections

How to deal with this?

Add to knowledge base

Or(
And(cell1difference, cell2differnce # will be the remainder of the cells) # and of course this is with the amount of bombs so [(c1,c2..,cn),count]
And(cell1difference, cellintersect, cell2difference# maybe )
cellintersect
)

""" 

# Case 4: bombs 1 =, (each) same appraoch but easier

"""
Pseudocode:
add to knowledge
Or(
    And(Cell1difference, cell2difference),
    cellintersect
)

"""

# Then this will recursively call untill its either a safe square or new knoweldge

# This also means we need to check if the cells are safe, or mines at before each recurssion

