import copy
import random
import sys

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for var in self.domains:
            removals = set(word for word in self.domains[var] if len(word) != var.length)
            for word in removals:
                self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        # Check if an overlap exists between variables x and y
        if overlap:

            removals = set()

            # Loop over every word in the domain of x
            for word_x in self.domains[x]:
                overlap_char = word_x[overlap[0]]
                corresponding_y_chars_set = set()
                # Loop over every word in the domain of y
                for word_y in self.domains[y]:
                    corresponding_y_chars_set.add(word_y[overlap[1]])
                # If every char value in the domain of y causes a conflict,
                # remove the corresponding word for the domain of x
                if overlap_char not in corresponding_y_chars_set:
                    removals.add(word_x)
                    revised = True

            # Remove words from the domain of x
            self.domains[x] = {word for word in self.domains[x] if word not in removals}

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            queue = [(var_1, var_2)
                     for var_1 in self.crossword.variables
                     for var_2 in self.crossword.variables]
            queue = [arc for arc in queue
                     if arc[0] != arc[1]
                     if self.crossword.overlaps[arc[0], arc[1]] is not None]
        else:
            queue = arcs
        while queue:
            arc = queue.pop(0)
            x, y = arc[0], arc[1]
            # Check for arc consistency
            if self.revise(x, y):
                if self.domains[x]:
                    # Add arc to queue after modifying the domain
                    other_neighbors = (self.crossword.neighbors(x) - {y})
                    for z in other_neighbors:
                        queue.append((z, x))
                else:
                    return False
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Assignment complete if each variable has a key in the assignment dictionary
        # and its corresponding value is a non-empty string
        complete = False
        if set(assignment.keys()) == self.crossword.variables and all(assignment.values()):
            return not complete
        return complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consistent = True

        # Check if every value has the correct length
        condition_1 = not all(var.length == len(word) for var, word in assignment.items())

        # Check if values are different from each other
        condition_2 = not len(set(assignment.values())) == len(set(assignment.keys()))

        if condition_1 or condition_2:
            return not consistent

        # Check for conflicts between neighboring variables
        for var, word in assignment.items():
            for neighbor in self.crossword.neighbors(var).intersection(assignment.keys()):
                overlap = self.crossword.overlaps[var, neighbor]
                if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                    return not consistent

        # If no condition applies, return True
        return consistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)

        # Initialize dictionary for removed options for each word in var's domain
        num_removed_choices = dict()
        # Loop through every word in the domain of var
        for word in self.domains[var]:
            num_removed_choices[word] = 0

        for word in self.domains[var]:
            # Loop through unassigned neighbors
            unassigned_neighbors = neighbors - assignment.keys()
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                # Loop through every word in the neighbor's domain
                for word_neighbor in self.domains[neighbor]:
                    if word[overlap[0]] != word_neighbor[overlap[1]]:
                        num_removed_choices[word] += 1

        # Sort the domain of var accoring to the number of choices ruled out
        sorted_words = sorted(num_removed_choices.items(), key=lambda x: x[1])
        return [x[0] for x in sorted_words]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Extract unassigned variables
        unassigned_vars = self.crossword.variables - assignment.keys()

        # For every variable, extract the number of remaining values for ordering
        num_values_left = dict()
        for var in unassigned_vars:
            num_values_left[var] = len(self.domains[var])
        # Sort by dict.value() for every item
        sorted_num_values_left = sorted(num_values_left.items(), key=lambda x: x[1])

        first_list_element = sorted_num_values_left[0][0]
        # If only one element is left in the list, return that one
        if len(sorted_num_values_left) == 1:
            return first_list_element
        # In case there are no equal values, return var with minimum number
        elif sorted_num_values_left[0][1] != sorted_num_values_left[1][1]:
            return first_list_element

        # In case there is a tie, return the element with the highest degree
        else:
            num_degrees = dict()
            for var in unassigned_vars:
                num_degrees[var] = len(self.crossword.neighbors(var))
            sorted_num_degrees = sorted(num_degrees.items(), key=lambda x: x[1])
            # Invert the list and extract first item
            sorted_num_degrees.reverse()
            return sorted_num_degrees[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # In case the assignment is complete, return it as a solution
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise, loop over unassigned var recursively
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                # Continue the recursive process until a solution is found
                solution = self.backtrack(assignment)
                if solution:
                    return solution
            # Once the values in var have all been assigned, pop var
            assignment.pop(var)
        # If no solution is possible, simply return None
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
