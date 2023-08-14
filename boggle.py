from graphics import Button
from game import Game
import pygame as pg
from boggleboard import BoggleBoard
from gambler import Shuffler, NonShuffler, SixSidedDie, PredictableDie
from lexicon import read_lexicon


class CubeGraphic(Button):

    def __init__(self, cube, x, y, width):
        """Initializes a visual representation of a BoggleCube.
        
        By default, the cubes are gray with the provided specifications.

        Parameters
        ----------
        cube : BoggleCube
            the BoggleCube that this graphic represents
        x : int
            x-coordinate of the upper left corner
        y : int
            y-coordinate of the upper left corner
        width : int
            the width of the visual representation (in pixels)
        """
        super().__init__(x, y, width, width, cube.get_letter(), up_color="gray", down_color="dark gray", font_color="black")
        self._cube = cube
        self._width = width

    def draw(self):
        """Returns a visual representation of the cube for the graphics window.
        The most recently selected cube will be colored green, other selected cubes will be blue, and
        all other cubes will remain gray.
        """  
        if self._cube.get_status() == "selected":
            self._up_color = "light blue"
            self._font_color = "blue"
        elif self._cube.get_status() == "most recently selected":
            self._up_color = "light green"
            self._font_color = "dark green"
        else:
            self._up_color = "gray"
            self._font_color = "black"
        return super().draw()
        
        
    def notify(self, event):
        """Notification that a user event (e.g. a mouse click) has occurred. If a cube has been pressed,
        it will be informed that it has been selected, and the status / word so far / completed words
        will be updated accordingly (or not, if the cube wasn't adjacent or if the word was invalid)
        """
        
        super().notify(event)
        if self.check_if_pushed():
            self._cube.select()
            self.reset()
        

        

class BoggleGame(Game):

    def __init__(self, lexicon, shuffler, die):
        """Initializes a new game of Boggle. The game board is shuffled using the provided
        shuffler & die. The play area is divided into sixteen squares to represent the visual
        layout of the game, and each square corresponds to a cube.

        Parameters
        ----------
        lexicon : set[str]
            A set of valid Boggle words.
        die : SixSidedDie
            A six-sided die that we can use to generate random numbers from 0 to 5.
        shuffler : Shuffler
            An object that shuffles a list (used for shuffling the BoggleCubes)        
        """
        super().__init__("soggle!")
        self._lexicon = lexicon
        
        # makes game board & shuffles board
        self._boggleboard = BoggleBoard(lexicon)
        self._boggleboard.shake_cubes(shuffler=shuffler, die=die)

        # divides play area into 16 squares
        cube_graphic_width = self.get_playarea_width() / 4
        playarea_x = self.get_playarea_x()
        playarea_y = self.get_playarea_y()

        # creates a CubeGraphic widget for each cube in these squares
        for row in range(4):
            for col in range(4):
                cube_x = playarea_x + cube_graphic_width * col
                cube_y = playarea_y + cube_graphic_width * row
                cube_widget = CubeGraphic(self._boggleboard.get_cube(row, col), cube_x, cube_y, cube_graphic_width)
                self._window.add_widget(cube_widget)


    def handle_event(self, event):
        """Handles user events (e.g. mouse clicks, keyboard presses).
        
        If the user pushes the ESC button, the board & word so far resets. Otherwise,
        any other action (that corresponds to clicking a letter on the board) will
        make updates to the word so far/completed words lists if applicable.
        """
        if event.type == pg.KEYDOWN and event.key == 27: # ESC was pressed
            self._boggleboard.reset_word()
            self._lower_left.reset_message(msg="") 

            
        else:
            self._lower_left.reset_message(self._boggleboard.get_word_so_far())
            self._upper_right.reset_words(self._boggleboard.get_completed_words())     



def play_boggle(shuffler, die):
    """Starts a game of Boggle!
    
    DO NOT CHANGE.
    """
    lexicon = read_lexicon('bogwords.txt')
    quit_now = False
    while not quit_now:
        game = BoggleGame(lexicon, shuffler, die)
        quit_now = game.play()
 

if __name__ == "__main__":
    #lay_boggle(NonShuffler(), PredictableDie(0)) 
    # replace the above line with the following line, when you want to play a random game:  
    play_boggle(Shuffler(), SixSidedDie())
