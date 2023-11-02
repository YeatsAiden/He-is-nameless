from settings import *
from .base_state import Base_state
from core_funcs import *
from load_map import Load_map
from player import Player


class Game(Base_state):
    def __init__(self) -> None:
        super().__init__()
        self.done = False
        self.quit = False
        self.next_state = None

        self.map = Load_map("./assets/world")
        self.current_level = self.map.levels["world"]
        self.offset = []
        self.areas = []
        self.rects =  []

        self.cam_pos = pg.Vector2(0, 400)
        self.player = Player((0, 0), "./assets/player")


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def update(self, window, dt):
        self.cam_pos[0] += (self.player.rect.x - self.cam_pos[0] - WINDOW_WIDTH/2)/10
        self.cam_pos[1] += (self.player.rect.y - self.cam_pos[1] - WINDOW_HEIGHT/2)/10

        keys_pressed = pg.key.get_pressed()

        current_time = time.time()

        self.areas, self.offset = self.map.get_area(window, self.cam_pos, self.current_level)
        self.rects = self.map.make_rects_array(self.areas, self.offset)

        self.player.move(keys_pressed, dt, self.rects, current_time)


    def draw(self, surf):
        surf.fill((7, 6, 5))
        self.map.draw_level(surf, self.cam_pos, self.offset, self.areas)
        self.player.draw(surf, self.cam_pos)