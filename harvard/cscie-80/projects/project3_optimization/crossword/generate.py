import sys
from queue import Queue

from crossword import *


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
        
        # Check the variable's length with the the word's length
        for variable, words in self.domains.items():
            words_as_list = list(words) # To remove members from a set while iterating over it.
            for word in words_as_list:
                if variable.length != len(word):
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Loop through every value of x
        revised = False
        words_in_x_list = list(self.domains[x])
        for word_in_x in words_in_x_list:
            if self.crossword.overlaps[x, y] is not None:  # Process only the overalapping words
                # Check if there is a value in y's domain for x
                y_corresponding_x = False
                for word_in_y in self.domains[y]:
                    # check if a corresponding word exists in y that does not cause a conflict
                    i, j = self.crossword.overlaps[x, y]
                    if word_in_x[i] == word_in_y[j]:  # Overlapping word found
                        y_corresponding_x = True
                        break   # We can skip the next y values
                if not y_corresponding_x:   # No possible values found in y corresponding to x
                    self.domains[x].remove(word_in_x)
                    revised = True
        return revised 

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        arcs_queue = []

        # Find overallping variables and add them to the arcs_queue list
        if arcs is None:
            for x in self.domains.keys():
                for y in self.domains.keys():
                    if x == y:
                        continue
                    if self.crossword.overlaps[x, y] is not None:
                        arcs_queue.append((x, y))
        else:
            arcs_queue = arcs

        while arcs_queue:
            x, y = arcs_queue.pop(0)
            # Call revise to make x arc consitent with y
            if self.revise(x, y):
                if not self.domains[x]:  # Empth set. We didn't revise
                    return False
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                if neighbors:
                    for z in neighbors:
                        arcs_queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Return false if assignment does not have all the variables
        if len(self.domains.keys()) != len(assignment.keys()):
            return False

        # Return false if the assignment does not have values for all the variables
        for variable in assignment.keys():
            if assignment[variable] is None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check if every value is of correct length
        for variable, word in assignment.items():
            if variable.length != len(word):
                return False

        # Check if all the values are unique. Use a set as a set will only store unique values
        all_words_set = set(assignment.values())
        all_words_list = list(assignment.values())
        if len(all_words_set) != len(all_words_list):
            return False

        # Check for conflicts.i.e overlaps don't agree
        for var1, value1 in assignment.items():
            for var2, value2 in assignment.items():
                if var1 == var2:
                    continue
                if self.crossword.overlaps[var1, var2] is not None:
                    i, j = self.crossword.overlaps[var1, var2]
                    if value1[i] != value2[j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        neighbors = list(self.crossword.neighbors(var))

        # Create a list of values along with the number of values it rules out
        value_list = []

        for value in self.domains[var]:
            eliminate_values = 0
            # Loop through each neighbour and it's overlaps
            for neighbor in neighbors:
                if neighbor not in assignment: 
                    i, j = self.crossword.overlaps[var, neighbor]
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            eliminate_values += 1
            value_list.append((value, eliminate_values))

        # Sort the list based on the number of values it rules out
        sorted_value_list = sorted(value_list, key=lambda x: x[1])
        
        # Return the values
        ordered_domain_values = [item[0] for item in sorted_value_list]

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Create a list of all avaialble variables along with the number of values in its domain, and its degree
        avaialble_variables = [var for var in self.domains.keys() if var not in assignment]
        value_list = []
        for var in avaialble_variables:
            value_list.append((var, len(self.domains[var]), len(self.crossword.neighbors(var))))

        # Sort the list by number of values in ascending order, and the degrees by decending order.
        sorted_value_list = sorted(value_list, key=lambda x: (x[1], -x[2]))

        return sorted_value_list[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            new_assignment = assignment.copy()
            new_assignment[variable] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
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
