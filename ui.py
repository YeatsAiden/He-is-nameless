from settings import *
import settings
from core_funcs import *


class Speech_bubble:
    def __init__(self, text, rect):
        # will iterate over full string, and use x coordinates to check if is out of bounds not accumulation of surface.widths
        self.text = text
        self.character_index = 0

        self.rect = rect
        self.x_pos = self.rect.x
        
        self.render_sentence = ""

        self.done_rendering = False

        self.rendering_times = {"super_slow": 500, "slow": 200, "normal": 100, "fast": 50, "super_fast": 20}
        self.text_render = pg.event.custom_type()
        pg.time.set_timer(self.text_render, self.rendering_times["normal"])


class Text:
    def __init__(self, path, size):
        # Path is the path to the font image
        # Size is the size of the font
        # Size is irrelevant
        
        self.spacing = 2
        self.sentences = {}

        self.font_image = pg.image.load(path).convert()
        self.character_set = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        self.character_index = 0
        self.character_width = 0
        self.characters = {}

        self.speech_bubble_text_offset = self.calculate_offset() 

        for x in range(self.font_image.get_width()):
            color = self.font_image.get_at((x, 0))
            if color == (0, 0, 255, 255):
                character_img = clip_img(self.font_image, x - self.character_width, 0, self.character_width, self.font_image.get_height())
                self.characters[self.character_set[self.character_index]] = character_img
                self.character_width = 0
                self.character_index += 1
            else:
                 self.character_width += 1


    def render_text(self, surf, text, x, y):
        # Will render text, and make new lines if there is the AMOGUS character in the string :|
        x_offset = 0
        y_offset = 0
        for index, letter in enumerate(text):
            if letter != ' ' and letter != "ඞ":
                character_img = self.characters[letter]
                character_img.set_colorkey((0, 0, 0))
                surf.blit(character_img, (x + x_offset , y + y_offset))
                x_offset += self.characters[letter].get_width() + self.spacing
            elif letter == ' ':
                x_offset += 5
            else:
                if index != 0:
                    x_offset = 0
                    y_offset += self.speech_bubble_text_offset[1] + 5


    def create_speech_bubble(self, name, text, rect):
        # Creates a new speech_bubble process, similar process like the particle system and bullet system.
        # Dunno it might eat up all your ram, I haven't tested all these thing enough ¯\_(ツ)_/¯
        #          /\
        # old text ||
        self.sentences[name] = Speech_bubble(text, rect)


    def render_speech_bubble(self, surf, name):
        # AAAAHHHHHHGHGHGHGHGHGHHGHGH my brain is fried and isn't capable of explaining this, try yourself, or if you are a prompt engineer and earn 25000$ a month from asking ChatGPT questions, then ask him :|
        # take note that settings.event is a global variable containing all events happening, put the events variable in a seperate file :\
        # This took all my blood, sweat and tears to make. (╯°□°）╯︵ ┻━┻
        # I was to lazy to look for a tutorial ._.
        # I need to change this horrible dict system to OOP
        # Ps this is old text I actually understand now how this works and am capable to explain but don't want to :|
        # I also changed it a lot so it's doesn't really need explaining since I'm such a good programmer hehehehe (the previous version was waaayyy to overengineered so now it's simplified :3)

        @event_loop
        def add_letter(event):
            if event.type == self.sentences[name].text_render:
                if self.sentences[name].character_index != len(self.sentences[name].text):
                    letter = self.sentences[name].text[self.sentences[name].character_index]
                    self.sentences[name].render_sentence += letter
                    self.sentences[name].character_index += 1
                    
                    if self.sentences[name].x_pos >= self.sentences[name].rect.topright[0]:
                        sentence_list = self.sentences[name].render_sentence.split()
                        sentence_list[-1] = "ඞ" + sentence_list[-1]
                        self.sentences[name].render_sentence = " ".join(sentence_list) if self.sentences[name].render_sentence[-1] != ' ' else " ".join(sentence_list) + ' '
                        self.sentences[name].x_pos = self.sentences[name].rect.x
                    
                    self.sentences[name].x_pos += self.characters[letter].get_width() + self.spacing if letter in self.characters else 5

        add_letter(settings.EVENT)

        self.render_text(surf, self.sentences[name].render_sentence, self.sentences[name].rect.x, self.sentences[name].rect.y)


    def calculate_offset(self):
        # It just calculates where the text should start in the speech bubble
        return [self.font_image.get_width() / len(self.character_set), self.font_image.get_height()]
    



class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.clicked = False
    

    def check_click(self):
        # get mouse position
        pos = list(pg.mouse.get_pos())
        mouse_pressed = pg.mouse.get_pressed()
        click = False

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and mouse_pressed[0] and not self.clicked:
            self.clicked = True
            click = True
        else:
            self.clicked = False

        # return if clicked
        return click

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        
