import itertools
import random
from logic import *


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
    
        """
        # Known mines can only be considered known if we absolutely know them to be true
        # The only cases given a set self.cells (meaning not multiple) is if the count of mines 
        # Is the same as the amount of cells, then we have logical statements
        if len(self.cells) == self.count:
            return self.cells
        # elif len(self.cells) != self.count and self.count != 0:
        #     statements = set()
        #     for i in self.cells:
        #         statements
        else: return set()
        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Same as known mines but the opposite
        if self.count == 0:
            return self.cells
        else: return set()
        


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check if cell is one of the cells included in the sentence
        # if true -> update sentence so cell is out, but still represents a logically correct sentence, given the cell is a mine
        # if false -> continue
        if cell in self.cells:
            if cell in self.known_mines(cell):
                self.mines_found.add(cell)
                self.cells.remove(cell)
            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Same logic but if not in self mines, board is set to false by default, so passes
        if cell in self.cells:
            if cell not in self.known_mines(cell):
                self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
    
    def check_knowledge(self, cell, count):
        """
        Recursively checks if new knowledge creates any inferences based on old
        knowledge untill a deadend is reached
        """
        # Implement knowledge adding algorithm based on related cells
        compareCount = None
        compareCell = set()

        # Need to check existing knowlege base
        if len(self.knowledge) == 0:
            self.knowledge.append([cell, count])
        
        # Now, iterate through knowledge base, and create cases for difference scenarios
        for knowledge in len(self.knowledge):
            for places in len(cell):
                # Now we need to go through cases of knowledge base
                for i in knowledge:
                    if len(cell&i) == 0:
                        self.knowledge.append([cell, count])
                    elif (cell>=i) and (cell<=i):
                        self.mark_mine(cell)

                    #implement case 3
                    elif (count > 1): # (A,B)
                        self.knowledge.append([]) # Nee
                        
                        


                         
                        
        return NotImplementedError

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # add cell to made move and safe
        self.moves_made.add(cell)
        self.safes.add(cell)

        # # add to knowledge base
        # self.knowledge.append()

        # creating a neighbourhood
        cell_neighbours = set()

        # create iterations
        if cell[0] != 7:
            cei = (cell[0] - 1, cell[0]+1) if cell[0] != 0 else (cell[0], cell[0]+1)
        if cell[1] != 7:
            cej = (cell[1] - 1, cell[1]+1) if cell[1] != 0 else (cell[1], cell[1]+1)
        else: cei = (cell[0] - 1, cell[0]); cej = (cell[1] - 1, cell[1])

        # proceed w iterations
        for i in range(*cei):
            for j in range(*cej):
                cell_neighbours.add(i,j)

        # update knowledge based on neighbours
        for cells in cell_neighbours:
            if cells in self.safes:
                cell_neighbours.remove(cells)
            elif cells in self.mines:
                cell_neighbours.remove(cells)
                count -= 1
        
        # Change knowledge base so that all surronding cells pass some logic, it changes based on what we know
        # Finally add to knowledge base, then we will see what else can be infered
        self.knowledge.add((cell_neighbours, count))

        # From knowledge base, can anything be concluded?
        # We need to see if any sets are overlapping, and conclude if substracting any sets from distance of 3
        # Can we elimate any cell values in cells
        """
        This will be going in th function check_knowledge
        """
        self.check_knowledge(cell_neighbours, count)
        


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # First, check if any moves in safe
        for s in self.safes:
            if s not in self.moves_made:
                return s
        else: return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # create a set for moves that have been made or mines
        pmoves = set()
        
        # if non-empty, iterate through and and add to our set
        if len(self.moves_made) != 0:
            for s in self.moves_made:
                pmoves.add(s)
        if len(self.mines) != 0:
            for s in self.mines:
                pmoves.add(s)
        
        # Check random moves that arent in set
        for i in range(8):
            for j in range(8):
                if (i,j) not in pmoves:
                    return (i,j)
        return None # If no more available moves
