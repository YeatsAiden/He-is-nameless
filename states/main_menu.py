from settings import *
from .base_state import Base_state
from ui import *

class Main_menu(Base_state):
    def __init__(self) -> None:
        super().__init__()
        self.done = False
        self.quit = False
        self.next_state = None

        self.ui_images = load_images('assets/ui')
        self.play_button = Button(120, 100, self.ui_images["play_button"])
        self.quit_button = Button(220, 100, self.ui_images["quit_button"])


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def update(self, surf, dt):
        if self.play_button.check_click():
            self.done = True
            self.next_state = "game"
        if self.quit_button.check_click():
            self.quit = True


    def draw(self, surface):
        surface.fill("black")
        self.play_button.draw(surface)
        self.quit_button.draw(surface)