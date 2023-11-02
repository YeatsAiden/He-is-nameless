from settings import *
from states.game import Game
from states.cutscene import Scene
from states.game_over import Game_over
from states.pause_menu import Pause_menu
from states.main_menu import Main_menu


class State:
    def __init__(self, window, fps) -> None:
        self.window = window

        self.states = {
            "game": Game(),
            "cutscene": Scene(),
            "game_over": Game_over(),
            "pause_menu": Pause_menu(),
            "main_menu": Main_menu(),
        }
        self.current_state = "main_menu"
        self.next_state = None
        self.previous_state = None
        self.state = self.states[self.current_state]

        self.fps = fps
        self.clock = pg.time.Clock()
        self.done = False


    def switch_state(self):
        if self.state.quit:
            pg.quit()
            sys.exit()
        if self.state.done:
            self.state.done = False
            self.next_state = self.state.next_state
            self.previous_state = self.current_state
            self.current_state = self.next_state
            self.state = self.states[self.current_state]

    
    def event_loop(self):
        self.state.event_loop()


    def update(self, surf, dt):
        self.state.update(surf, dt)


    def draw(self, surf):
        self.state.draw(surf)


    def run(self, window):
        while not self.done:
            dt = self.clock.tick(FPS)/1000
            self.switch_state()
            self.event_loop()
            self.update(window, dt)
            self.draw(window)
            pg.display.update()
            # self.clock.tick(self.fps)
