from settings import *
from .base_state import Base_state


class Game_over:
    def __init__(self) -> None:
        self.done = False
        self.quit = False
        self.next_state = None