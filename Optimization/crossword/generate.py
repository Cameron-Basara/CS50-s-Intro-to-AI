import sys

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For all vars, remove all words that do not have the same length from the domain of var
        for v in self.crossword.variables:
            for x in self.crossword.words:
                if v.length != len(x):
                    self.domains[v].remove(x)
        # Returns void

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
         # Set revised to False
        revised = False

        # Check overlap
        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return revised  # No overlap means arc consistency

        i, j = overlap  # Overlap indices

        # Collect values to remove
        to_remove = set()
        for word_x in self.domains[x]:
            # Check if there is any value in y's domain that satisfies the constraint
            if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                to_remove.add(word_x)  # Mark word_x for removal

        # Remove invalid values
        for word_x in to_remove:
            self.domains[x].remove(word_x)
            revised = True  # Mark that a revision was made
            
        return revised    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
         # Initialize the queue of arcs
        if arcs is None:
            arcs = deque(
                (x, y)
                for x in self.crossword.variables
                for y in self.crossword.neighbors(x))
        else:
            arcs = deque(arcs)
        
        # Process each arc
        while arcs:
            x,y = arcs.popleft() # Get and remove the first arc
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False # csp is unsolvable
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z,x)) # add all arcs for the neighbors of x
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if every var has been assigned in assignment
        for var in self.crossword.variables:
            if var not in assignment or assignment[var] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Iterate over all vars
        for var, value in assignment.items():
            # Check node consistency
            if len(value) != var.length:
                return False
            
            # Check distinctness
            if list(assignment.values()).count(value) > 1:
                return False
            
            # Check arc consistency
            for n in self.crossword.neighbors(var):
                if n in assignment:
                    overlap = self.crossword.overlaps[var, n]
                    if overlap is not None:
                        i, j = overlap
                        # Ensure characters at the overlap point match
                        if value[i] != assignment[n][j]:
                            return False
                        
        # Otw return true
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Identify neighbors, compute the number of ruled out values, sort by least-constraining, then return ordered list
        def ruled_out(value):
            """
            Count number of values ruled out in the domains of vars neighboys
            if value is assigned to var.
            """
            out = 0
            for n in self.crossword.neighbors(var):
                if n in assignment:
                    continue # Ignore

                overlap = self.crossword.overlaps[var, n]
                if overlap is not None:
                    i, j = overlap
                    # count vals ruled out due to constraints
                    out += sum(1 for n_val in self.domains[n] if n_val[j] != value[i])
            return out

        # Return sorted values in vars doamin by number of values they rule out
        return sorted(self.domains[var], key=ruled_out)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Filter out already assigned variables
        unassigned = [
            var for var in self.crossword.variables if var not in assignment
        ]

        # Sort by MRV, then by degree heuristic
        def sort_key(var):
            remaining_values = len(self.domains[var]) # MRV
            degree = len(self.crossword.neighbors(var)) # Degree
            return (remaining_values, -degree)  

        return min(unassigned, key=sort_key)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If the assignment is complete return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Iterate over the ordered domain values for the selected variable
        for value in self.order_domain_values(var, assignment):
            # Try assigning the value to the variable
            assignment[var] = value

            # Check if the assignment is consistent
            if self.consistent(assignment):
                # Inference with ac3
                if self.ac3([(neighbor, var) for neighbor in self.crossword.neighbors(var)]):
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                    
                # Recursive call with the updated assignment
                result = self.backtrack(assignment)

                if result is not None:
                    return result  # Return the successful assignment

            # If not successful, undo the assignment
            del assignment[var]

        # If no assignment leads to a solution, return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
