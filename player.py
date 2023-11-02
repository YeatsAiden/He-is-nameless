from settings import *
from core_funcs import *
from animation import Animation

class Player():
    def __init__(self, pos, animation_path):
        self.animation = Animation()
        self.animation_dirs = get_dir_names(animation_path)
        self.animation.animations["idle"] = self.animation.load_animation("assets/player/idle", [1])
        self.animation.animations["run"] = self.animation.load_animation("assets/player/run", [5, 5, 5, 5, 5, 5, 5, 5])
        self.animation.animations["jump"] = self.animation.load_animation("assets/player/jump", [20])
        self.animation.animations["fly"] = self.animation.load_animation("assets/player/fly", [1])
        self.animation.animations["fall"] = self.animation.load_animation("assets/player/fall", [1])
        self.animation.animations["skid"] = self.animation.load_animation("assets/player/skid", [1])

        self.animation_frame = 0
        self.flip = False

        self.pos = pos
        self.image = self.animation.animations['idle'][0]
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.speed = 5
        self.max_speed = 2
        self.mass = 10
        self.jump_force = 200
        self.max_fall_speed = 5

        self.vel = pg.Vector2(0, 0)
        self.momentum = pg.Vector2(0, 0)

        self.can_jump = False
        self.will_jump = False
        self.prev_jump = 0
        self.prev_on_land = 0
        self.prev_pressed_jump = 0

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.player_state = "idle"


    def draw(self, surf, cam_pos):
        self.image, self.animation_frame = self.animation.animate(self.animation_frame, self.player_state, self.flip)
        surf.blit(self.image, self.rect.topleft - cam_pos)
    

    def move(self, keys_pressed, dt, rects, current_time):
        self.vel = pg.Vector2(0, 0)

        self.momentum.x += self.speed * dt * (keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT])
        self.momentum.x -= self.speed * dt * (keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT])

        if not (keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]) and not (keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]):
            if -0.1 < self.momentum.x < 0.1:
                self.momentum.x = 0
            else:
                self.momentum.x /= 1.2

        self.momentum.x = max(min(self.momentum.x, self.max_speed), -self.max_speed)

        self.momentum.y += self.mass * dt
        self.prev_on_land = current_time if self.collision_state["bottom"] else self.prev_on_land
        self.can_jump = True if (self.collision_state["bottom"] or not self.timer(current_time, self.prev_on_land, 0.1)) else False

        if (keys_pressed[pg.K_w] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.K_UP]) and self.can_jump:
            self.prev_pressed_jump = current_time if not self.will_jump else self.prev_pressed_jump
            self.will_jump = True
            self.can_jump = False

        if self.will_jump and self.timer(current_time, self.prev_pressed_jump, 0.15):
            self.momentum.y = 0
            self.momentum.y -= self.jump_force * dt
            self.will_jump = False
            self.prev_jump = current_time

        self.momentum.y = min(self.momentum.y, self.max_fall_speed)

        self.vel.x += self.momentum.x
        self.vel.y += self.momentum.y

        self.collision_state_check(rects)
        self.player_state_check(keys_pressed)


    def collision_check(self, rects):
        collide_rects = []
        for rect in rects:
            if rect.colliderect(self.rect):
                collide_rects.append(rect)
        
        return collide_rects
    

    def collision_state_check(self, rects):
        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }
        
        self.rect.x += self.vel.x
        for rect in self.collision_check(rects):
            if self.vel.x > 0:
                self.rect.right = rect.left
                self.momentum.x = 0
                self.collision_state["right"] = True
            if self.vel.x < 0:
                self.rect.left = rect.right
                self.momentum.x = 0
                self.collision_state["left"] = True
        
        self.rect.y += self.vel.y
        for rect in self.collision_check(rects):
            if self.vel.y > 0:
                self.rect.bottom = rect.top
                self.momentum.y = 0
                self.collision_state["bottom"] = True
            if self.vel.y < 0:
                self.rect.top = rect.bottom
                self.momentum.y = 0
                self.collision_state["top"] = True
    

    def player_state_check(self, keys_pressed):
        if self.momentum.x == 0 and self.momentum.y == 0:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'idle', self.animation_frame)

        if (keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]) and self.collision_state['bottom']:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'run', self.animation_frame)

        if keys_pressed[pg.K_w] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.K_UP]:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'jump', self.animation_frame)

        if self.momentum.y < 0 and not self.collision_state["bottom"]:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'fly', self.animation_frame)

        if not self.collision_state["bottom"] and self.momentum.y > 0:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'fall', self.animation_frame)

        if (((keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]) and self.momentum.x < 0) or ((keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]) and self.momentum.x > 0)) and self.collision_state['bottom']:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'skid', self.animation_frame)
        
        if keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]:
            self.flip = False
        elif keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]:
            self.flip = True

    def timer(self, current_time, previous_time, cool_down):
        return current_time - previous_time > cool_down
        