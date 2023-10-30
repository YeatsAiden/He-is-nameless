from settings import *
from .base_state import Base_state
from load_map import Load_map


class Game(Base_state):
    def __init__(self) -> None:
        super().__init__()
        self.done = False
        self.quit = False
        self.next_state = None
        self.map = Load_map("../assets/world/world.json")


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def update(self, dt):
        pass


    def draw(self, surface):
        surface.fill("black")