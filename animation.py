from settings import *


class Animation:
    def __init__(self) -> None:
        self.animations = {}


    def load_animation(self, path, durations):
        animation_name = path.split("/")[-1]
        animation = []

        for index, frames in enumerate(durations):
            img_name = animation_name + "_" + str(index)
            img_path = path + "/" + img_name + ".png"
            img = pg.image.load(img_path)
            for frame in range(frames):
                animation.append(img)
        
        return animation
    

    def animate(self, animation_frame, state, flip):
        animation_frame = 0 if animation_frame == len(self.animations[state]) else animation_frame
        image = pg.transform.flip(self.animations[state][animation_frame], flip, False)
        return image, animation_frame + 1
    

    def change_state(self, state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame
        

