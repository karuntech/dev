import itertools
import random


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
        
        # The cells are mines if the count is equal to the number of cells in the sentence
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Cells are safe if the count is 0
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # The cell is a mine. Remove from the setence, and reduce the count
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # The cell is safe. Remove from the sentence.
        if cell in self.cells:
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
        
        self.printStatus()  # For debugging purposes
        
        # 1) Mark the cell as a move that has been made

        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        
        self.mark_safe(cell)

        #  3) Add a new setence based the cell clicked and the count revealed
        neighbors = set()
        count_in_new_knowledge = count  # Use a temporary count variable as we may have to change the count if the neighbor is already known.
        for i in range(cell[0] - 1, cell[0] + 2 ):
            for j in range(cell[1] - 1, cell[1] + 2):
                # ignore the cell itself as we are only interested in the neighbors
                if (i, j) == cell:
                    continue
                # ignore the cell if it has already been determined as a mine or as a safe
                if (i,j) in self.mines:
                    count_in_new_knowledge -= 1
                    continue
                if (i,j) in self.safes:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width: # i and j must be within the board boundaries
                    neighbors.add((i,j))

        # Form a sentence based on the neighbors and count
        new_knowledge = Sentence(neighbors, count_in_new_knowledge)
        self.knowledge.append(new_knowledge)

        # 4) Mark any additional cells as safes are mines
        while(True):
            safes_found = False # Boolean to keep track of safes
            mines_found = False # Boolean to keep track of mines
            for sentence in self.knowledge:
                if(sentence.known_safes()):    # Safes found
                    for cell in list(sentence.known_safes()):
                        self.mark_safe(cell)
                        safes_found = True
                if(sentence.known_mines()):    # Mines found
                    for cell in list(sentence.known_mines()):
                        self.mark_mine(cell)
                        mines_found = True

        # 5) Add any new sentences to the knowledge if possible
        
            new_sentence_formed = False # Boolean to keep track of updates

            for sentence1 in self.knowledge:
                if sentence1.cells: # Ignore if the sentence is empty
                    for sentence2 in self.knowledge:
                        if sentence2.cells: # Ignore if the sentence is empty
                            if sentence1.cells != sentence2.cells and sentence1.cells.issubset(sentence2.cells):
                                # subset found, let's make a new sentence
                                new_knolwedge = Sentence(
                                    sentence2.cells - sentence1.cells,
                                    sentence2.count - sentence1.count,
                                )
                                self.knowledge.append(new_knolwedge)
                                self.knowledge.remove(sentence2) # Remove the bigger set from the knowledge, otherwise it can cause infinite loop
                                new_sentence_formed = True

            if not (safes_found or mines_found or new_sentence_formed): # Only if all the three conditions are false, break out of this loop
                self.printStatus()
                break


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # choose a cell from the safe cells, and ensure that the move has not been made before
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_not_eligible = self.mines.union(self.moves_made)  # Add mines and moves_made
        total_possible_moves_in_board = set()
        for i in range(self.height):
            for j in range(self.width):
                total_possible_moves_in_board.add((i,j))

        eligible_moves = total_possible_moves_in_board - moves_not_eligible
        if eligible_moves:
            return random.choice(tuple(eligible_moves))
        else:
            return None

    def printStatus(self):
        """
        print values of variables for debugging purposes
        """
        print(f"")
        print(f"CURRENT SAFES: {self.safes}")
        print(f"CURRENT MINES: {self.mines}")
        print(f"CURRENT MOVES MADE: {self.moves_made}")
        print(f"CURRENT KB {[str(x) for x in self.knowledge]}")
