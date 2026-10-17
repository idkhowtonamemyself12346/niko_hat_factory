from vars import *
import pygame
global belt_anim_speed, belt_anim_frame, belt_anim
money = 0
pygame.init()
class Rectangle:
    def __init__(self, xposition, yposition, width, height, offsetx, offsety, color:tuple):
        self.xcenter = xposition
        self.ycenter = yposition
        self.xpos = xposition
        self.ypos = yposition
        self.width = width
        self.height = height
        self.offsetx = offsetx
        self.offsety = offsety
        self.color = color
class Belt(Rectangle):
    def __init__(self, xposition, yposition, width, height, offsetx, offsety, color, direction):
        super().__init__(xposition, yposition, width, height, offsetx, offsety, color)
        self.direction = direction
        self.frame_index = 0
        self.frame_timer = 0
    frames = []
    belt_anim_frame = 0
    frame_timer = 0
    direction_angle = {
        "right": 270,
        "up": 0,
        "left": 90,
        "down": 180,
    }
    @classmethod
    def load_frames(cls, sheet, frame_width, frame_height, frame_count):
        cls.frames = [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)).copy() for i in range(frame_count)]
        cls.belt_anim_frame = 0
        cls.frame_timer = 0

    @classmethod
    def advance_animation(cls):
        if not cls.frames:
            return
        cls.frame_timer += 1
        if cls.frame_timer >= belt_anim_speed:
            cls.frame_timer = 0
            cls.belt_anim_frame = (cls.belt_anim_frame + 1) % len(cls.frames)

    def animate(self):
        if not Belt.frames:
            return None
        frame = Belt.frames[Belt.belt_anim_frame]
        angle = self.direction_angle.get(self.direction)
        if angle is None:
            return frame
        frame = pygame.transform.scale(frame, (grid_size, grid_size))
        return pygame.transform.rotate(frame, angle)

    def item_move(self):
        for item in items:
            if (item.xpos, item.ypos) == (
                self.xpos,
                self.ypos,):
                dx, dy = offsets[self.direction]
                return item, (item.xpos + dx, item.ypos + dy)
        return None
class Item(Rectangle):
    def __init__(self, xposition, yposition, width, height, offsetx, offsety, color):
        Rectangle.__init__(self, xposition, yposition, width, height, offsetx, offsety, color)
class Generator(Rectangle):
    def __init__(self, xposition, yposition, width, height, offsetx, offsety, color, direction):
        super().__init__(xposition, yposition, width, height, offsetx, offsety, color)
        self.direction = direction
    def generate_item(self):
        if self.direction not in offsets:
            return False
        dx, dy = offsets[self.direction]
        target_x = self.xpos + dx
        target_y = self.ypos + dy
        if any(item.xpos == target_x and item.ypos == target_y for item in items):
            return False
        items.append(Item(
            target_x, target_y,
            half_grid_size, half_grid_size,
            0, 0, (255, 0, 0)))
        return True
def update_money():
    global money
    money += 1
    print(money)
class Collector(Rectangle):
    global money
    def __init__(self, xposition, yposition, width, height, offsetx, offsety, color):
        Rectangle.__init__(self, xposition, yposition, width, height, offsetx, offsety, color)
    def collect_item(self):
        global money
        for item in items:
            if (item.xpos, item.ypos) == (self.xpos, self.ypos):
                items.remove(item)
                return True
        return False

class Selector(Rectangle):
    def __init__(self, xposition, yposition, width, height):
        Rectangle.__init__(self, xposition, yposition, width, height, 0, 0, (0,0,255))
    def update_pos(self):
        pos = pygame.mouse.get_pos()
        self.xpos, self.ypos = (pos[0] - pos[0] % grid_size), (pos[1] - pos[1] % grid_size)
        return