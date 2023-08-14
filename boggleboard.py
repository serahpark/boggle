from bogglecube import BoggleCube
from gambler import Shuffler, PredictableShuffler, SixSidedDie, PredictableDie

# The sixteen letter cubes provided with the standard game of Boggle.
CUBE_FACES = [("A", "A", "C", "I", "O", "T"),  # cube 0
              ("T", "Y", "A", "B", "I", "L"),  # cube 1
              ("J", "M", "O", "Qu", "A", "B"), # cube 2
              ("A", "C", "D", "E", "M", "P"),  # cube 3
              ("A", "C", "E", "L", "S", "R"),  # cube 4
              ("A", "D", "E", "N", "V", "Z"),  # cube 5
              ("A", "H", "M", "O", "R", "S"),  # cube 6
              ("B", "F", "I", "O", "R", "X"),  # cube 7
              ("D", "E", "N", "O", "S", "W"),  # cube 8
              ("D", "K", "N", "O", "T", "U"),  # cube 9
              ("E", "E", "F", "H", "I", "Y"),  # cube 10
              ("E", "G", "I", "N", "T", "V"),  # cube 11
              ("E", "G", "K", "L", "U", "Y"),  # cube 12
              ("E", "H", "I", "N", "P", "S"),  # cube 13
              ("E", "L", "P", "S", "T", "U"),  # cube 14
              ("G", "I", "L", "R", "U", "W")]  # cube 15


class BoggleBoard:
    """A BoggleBoard represents a 4x4 grid of BoggleCube objects."""

    def __init__(self, lexicon):
        """Initializes a new BoggleBoard.
        
        Parameters
        ----------
        lexicon : set[str]
            The set of valid Boggle words.
        """
        self._lexicon = lexicon
        
        # a list of all cubes in the order that they are on the board
        self._cubes = []
        for element_index in range(len(CUBE_FACES)):
            cube = BoggleCube(element_index, CUBE_FACES[element_index], self)
            self._cubes.append(cube)

        # a nested list of lists of the order of all cubes in each row
        self._cube_grid = []
        for i in range(0, len(self._cubes), 4):
            row = []
            for j in range(i, i+4):
                row.append(self._cubes[j])
            self._cube_grid.append(row)

        # a dictionary storing the locations of each cube; the cube_id is the key
        # and the value is a list of the row and column
        self._locations = {}
        for row in range(4):
            for col in range(4):
                cube = self._cube_grid[row][col]
                self._locations[cube.get_id()] = [row, col]

        # initializes an empty list of the cubes selected by the player so far
        self._selected_cubes = []

        # initializes an empty string of the word formed by the player's selections so far
        self._word_so_far = ''

        # initializes an empty list of the words completed by the player so far
        self._completed_words = []

        # self._score = 0  -> initializes a score int for the implementation of scoring in textboggle


    def get_cube(self, row, col):
        """Returns the BoggleCube currently at the specified row and column.
        
        Parameters
        ----------
        row : int
            The desired row (should be between 0 and 3)
        col : int
            The desired column (should be between 0 and 3)
        
        Returns
        -------
        BoggleCube
            the cube currently at the specified row and column.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.get_cube(0, 0).get_letter()
        'A'
        >>> board.get_cube(3, 3).get_letter()
        'G'
        """
        return self._cube_grid[row][col]
    
    def update_grid_locations(self):
        """Updates the locations attribute, a dictionary storing the locations of each cube.
        Keeps the dictionary sorted in the order of cube ids. This method is called whenever
        the order of the cubes changes, since it also updates the cube_grid attribute."""
        
        # empties cube_grid list and updates the order of the cubes on the grid into nested lists
        self._cube_grid = []
        for i in range(0, len(self._cubes), 4):
            row = []
            for j in range(i, i+4):
                row.append(self._cubes[j])
            self._cube_grid.append(row)

        # empties locations dictionary and updates the values for each cube_id key
        self._locations = {}
        for row in range(4):
            for col in range(4):
                cube = self._cube_grid[row][col]
                self._locations[cube.get_id()] = [row, col]
                
                # since dictionary is out of order, cube_ids are sorted so dictionary can be sorted
                sorted_keys = sorted(self._locations.keys())
                self._locations = {key:self._locations[key] for key in sorted_keys}
                
        
    def shake_cubes(self, shuffler=Shuffler(), die=SixSidedDie()):
        """Shakes the cubes.
        
        First, the cubes should be shuffled by the provided Shuffler.
        Then, each cube should be independently rolled using the provided SixSidedDie.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).get_letter()
        'U'
        >>> board.get_cube(1, 2).get_letter()
        'T'

        """

        # reorders the placement of each cube & updates cubes attribute
        self._cubes = shuffler.shuffle(self._cubes)

        # updates location of each cube
        self.update_grid_locations()
        
        # rolls individual cube to change cube faces
        for cube in self._cubes:
                cube.roll(die)
        


    def adjacent(self, cube1, cube2):
        """Determines whether two cubes are adjacent.
        
        Two cubes are adjacent if they are vertically, horizontally, or diagonally adjacent.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.adjacent(board.get_cube(1, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 1), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(0, 1))
        False
        """

        # gets row & col of each cube to check for adjacency
        cube1_row = self._locations[cube1.get_id()][0]
        cube1_col = self._locations[cube1.get_id()][1]
        cube2_row = self._locations[cube2.get_id()][0]
        cube2_col = self._locations[cube2.get_id()][1]

        # check if cubes are in the same row
        if cube1_row == cube2_row and abs(cube2_col - cube1_col) == 1:
            return True
        
        # check if cubes are in the same column
        elif cube1_col == cube2_col and abs(cube2_row - cube1_row) == 1:
            return True
        
        # check if cubes are in a diagonal or antidiagonal
        elif abs(cube2_row - cube1_row) == 1 and abs(cube2_col - cube1_col) == 1:
            return True
        
        # returns False if cubes are not adjacent
        return False

    def unselect_all(self):
        """Sets the status of all cubes to 'unselected'.
        
        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).set_status("selected")
        >>> board.get_cube(2, 3).set_status("selected")
        >>> board.unselect_all()
        >>> board.get_cube(0, 0).get_status()
        'unselected'
        >>> board.get_cube(2, 3).get_status()
        'unselected'
        """        
        for cube in self._cubes:
            cube._status = "unselected"

    def reset_word(self):
        """Resets the string of the word so far and resets all selections of cubes
        on the board."""
        
        self._word_so_far = ''
        self._selected_cubes = []
        self.unselect_all()

    def report_selection(self, cube_id):
        """Reports that the cube with the specified id has been selected by the player.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        >>> board = BoggleBoard({'GET', 'PUT', 'APT'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(9)
        >>> board.get_word_so_far()
        'PUT'
        >>> board.report_selection(9)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(11)
        >>> board.get_word_so_far()
        'PU'
        >>> board.report_selection(12)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        """
        row = self._locations[cube_id][0]
        col = self._locations[cube_id][1]
        curr_cube = self.get_cube(row, col)

        # check if the cube is the first cube selected
        if self._selected_cubes == []:
            
            # add cube's id to list of cubes selected, add letter to word_so_far attribute, and change cube's status
            self._selected_cubes.append(cube_id)
            self._word_so_far += curr_cube.get_letter()
            curr_cube.set_status("most recently selected")

        # check if cube has not been selected yet
        elif curr_cube.get_status() == "unselected":
        
        # get previous BoggleCube with the most recent cube's id
            prev_row = self._locations[self._selected_cubes[-1]][0]
            prev_col = self._locations[self._selected_cubes[-1]][1]
            prev_cube = self.get_cube(prev_row, prev_col)

            # check if selected cube is adjacent to previous BoggleCube, change status of both cubes, word_so_far, selected_cubes lists
            if self.adjacent(curr_cube, prev_cube):
                self._selected_cubes.append(cube_id)
                self._word_so_far += curr_cube.get_letter()
                curr_cube.set_status("most recently selected")
                prev_cube.set_status("selected")
        
        # check if player wants to finalize word with a second selection of the same cube
        elif curr_cube.get_status() == "most recently selected":
            
            # check if word is valid; if so, word is added to completed words list & board is reset
            if self._word_so_far in self._lexicon:
                self.get_completed_words().append(self._word_so_far)
                # self.score(self._word_so_far)
                self.reset_word()

            else:
                self.reset_word()

    def get_completed_words(self):
        """Returns the list of completed words.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        """
        return self._completed_words

    def get_word_so_far(self):
        """Returns the word corresponding to the letters selected so far.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        
        """
        return self._word_so_far
    
    # def score(self, word): -> based on gamepigeon word hunt's scoring!
    #     scoring = {3: 100, 4: 400, 5: 800, 6: 1400, 7: 1800, 8: 2200}
    #     self._score += scoring[len(word)]
    #     return self._score


    def __str__(self):
        """A string representation of the BoggleBoard."""
        row_strs = []
        for row in range(4):
            column = [str(self.get_cube(row, col)) for col in range(4)]
            row_strs.append(' '.join(column))
        return '\n'.join(row_strs)

if __name__ == "__main__":
    from doctest import testmod
    testmod()