import curses, random, time
from lib.pixels import *
from lib.pixels import Color as rgb
from lib.words import WORDS
from lib.shapes import SHAPES, NO_SHAPE
from lib.numbers import NUMBERS


# Screen dimensions
WIDTH, HEIGHT = 8, 32

START_WIDTH, START_HEIGHT = 2, 0

# rgbs
WHITE = rgb(255, 255, 255)
BLACK = rgb(0, 0, 0)

PURPLE1 = rgb(86, 24, 127)
PURPLE2 = rgb(138, 38, 204)
PURPLE3 = rgb(173, 48, 255)
PURPLE4 = rgb(209, 140, 255)
PURPLE5 = rgb(218, 163, 215)

COLORS = [PURPLE1, PURPLE2, PURPLE3, PURPLE4, PURPLE5, WHITE]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]
        self.current_piece = self.new_piece(SHAPES)
        self.game_over = False
        self.score = 0

    def new_piece(self, shapes):
        """ Create new piece """
        shape = random.choice(shapes)
        return Tetromino(x=START_WIDTH, y=START_HEIGHT, shape=shape)

    def valid_move(self, piece, x, y, rotation):
        """ Check if next move is valid """
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(self.current_piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[piece.y + i +y][piece.x + j + x] != 0):
                        return False
                except IndexError:
                    print("error ++")
                    return False

        return True


    def clear_lines(self):
        """ Clear line once line is full with piece """
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        """ Lock piece when unable to move anymore """
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.current_piece = self.new_piece(SHAPES)

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def update(self):
        """ move piece down """
        if not self.game_over:
            if self.valid_move(piece=self.current_piece, x=0, y=1, rotation=0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)


    def convert_to_vertical(self, game_position):
        return 31 - game_position


    def draw_shape(self, screen: Pixels):
        """ draw piece on the screen with current position """
        screen.clear()

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != 0:
                    xx = self.convert_to_vertical(game_position=y)
                    yy = x
                    screen.set(x=xx, y=yy, color=cell)
        screen.show()

        if self.current_piece:
            current_shape = self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]
            for i, row in enumerate(current_shape):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        game_position = self.current_piece.y + i
                        xx = self.convert_to_vertical(game_position=game_position)
                        yy = self.current_piece.x + j
                        screen.set(x=xx, y=yy, color=self.current_piece.color)
            screen.show()

            for i, row in enumerate(current_shape):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        game_position = self.current_piece.y + i
                        xx = self.convert_to_vertical(game_position=game_position)
                        yy = self.current_piece.x + j
                        screen.set(x=xx, y=yy, color=BLACK)

def set_score(screen, score, s, x, y, start_x, start_y):
    for i, row in enumerate(NUMBERS[score[s]]):
                for j, col in enumerate(row):
                    if col == 'O':
                        screen.set(x - start_x - i, start_y + y + j, WHITE)
    start_y += 3
    return start_y


def draw_score(screen, score, x, y):
    """Draw the score on the screen"""
    screen.clear()

    score = str(score)
    start_y = 0
    start_x = 0

    for s in range(0, len(score)):
        if start_y <= 7:
            start_y = set_score(screen=screen, score=score, s=s, x=x, y=y, 
                                start_x=start_x, start_y=start_y)
        else:
            start_y = 0
            start_x += 6
            start_y = set_score(screen=screen, score=score, s=s, x=x, y=y, 
                                start_x=start_x, start_y=start_y)

    screen.show()
    time.sleep(0.7)


def draw_game_over(screen: Pixels, x: int, y: int, letter_sp: int):
    """Draw the game over text on the screen"""
    screen.clear()

    pos_x: int = x
    pos_y: int = y

    word_game = WORDS[0]
    word_over = WORDS[1]

    space_char_game = 0

    for c, char in enumerate(word_game):
        for i, row in enumerate(char):
            for j, col in enumerate(row):
                if col == 'O':
                    screen.set((pos_x - i) - (space_char_game + letter_sp), pos_y + j, WHITE)
        space_char_game += 6

    space_char_over = 0
    pos_y_over = 5
    for c, char in enumerate(word_over):
        for i, row in enumerate(char):
            for j, col in enumerate(row):
                if col == 'O':
                    screen.set((pos_x - i) - (space_char_over + letter_sp), pos_y_over + pos_y + j, WHITE)
        space_char_over += 6

    screen.show()
    time.sleep(0.7)
 

def main(stdscr, pixels: Pixels):

    curses.curs_set(False)
    stdscr.nodelay(True)

    game = Tetris(WIDTH, HEIGHT)
    
    fall_time = 0
    fall_speed = 200
    refresh_rate = 0.6

    running = True
    while running:
        ch = stdscr.getch()

        is_clear = game.clear_lines()
        if is_clear:
            game.draw_shape(pixels)

        if ch == curses.KEY_LEFT and game.valid_move(piece=game.current_piece, x=-1, y=0, rotation=0):
            if game.current_piece.x != 0:
                game.current_piece.x -= 1
        if ch == curses.KEY_RIGHT and game.valid_move(piece=game.current_piece, x=1, y=0, rotation=0):
            game.current_piece.x += 1  
        if ch == curses.KEY_DOWN and game.valid_move(piece=game.current_piece, x=0, y=1, rotation=0):
            game.current_piece.y += 1
        if ch == curses.KEY_UP and game.valid_move(piece=game.current_piece, x=0, y=0, rotation=1):
            game.current_piece.rotation += 1
        if ch == ord(' '):
            while game.valid_move(piece=game.current_piece, x=0, y=1, rotation=0):
                game.current_piece.y += 1  
            game.lock_piece(game.current_piece) 
        
        pixels.show()
        
        fall_time += 1
        if fall_time >= fall_speed:
            fall_time = 0
            if refresh_rate <= 0:
                refresh_rate = 0.6
            #make the falling time faster
            refresh_rate -= 0.02

        game.update()
        game.draw_shape(pixels)

        if game.game_over:
            #reset screen
            game.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
            game.current_piece = game.new_piece(NO_SHAPE)

            draw_game_over(screen=pixels, x=31, y=0, letter_sp=1)
            draw_score(screen=pixels, score=game.score, x=31, y=0)

            if ch == curses.KEY_DOWN:
                game = Tetris(WIDTH, HEIGHT)

        time.sleep(refresh_rate)


if __name__ == "__main__":
    with Pixels(brightness=10) as pixels:
        curses.wrapper(main, pixels)
