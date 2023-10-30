from settings import *


class Base_state:
    def __init__(self) -> None:
        self.done = False
        self.quit = False
        self.next_state = None


    def event_loop(self):
        pass


    def update(self, dt):
        pass


    def draw(self, surface):
        pass