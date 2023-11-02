from settings import *
from state_manager import State

pg.init()

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pg.SCALED | pg.RESIZABLE)

game = State(window, 60)
game.run(window)

