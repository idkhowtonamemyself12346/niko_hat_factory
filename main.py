from classes import *
from pathlib import Path
import sys, threading
import controls
global money

t1 = threading.Thread(target=controls.show_window, daemon=True)
t1.start()
pos = pygame.mouse.get_pos()
xmousepos = (pos[0] - pos[0] % grid_size)
ymousepos = (pos[1] - pos[1] % grid_size)
BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
font_path = BASE_DIR / "assets" / "font" / "Tiny5" / "Tiny5-Regular.ttf"
belt_path = BASE_DIR / "assets" / "belt" / "belt2-Sheet.png"
item_path = BASE_DIR / "assets" / "item" / "niko_hat.png"
selector_path = BASE_DIR / "assets" / "selector" / "selector.png"
gen_path = BASE_DIR / "assets" / "generator" / "gen.png"
gen2_path = BASE_DIR / "assets" / "generator" / "gen2.png"
pygame.init()
pygame.font.init()
money_text = pygame.font.Font(font_path, 32)
screen = pygame.display.set_mode((512, 512))
screen_width = pygame.display.get_window_size()[0]
screen_height = pygame.display.get_window_size()[1]
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("niko hat factory")
belt_sheet = pygame.image.load(belt_path)
item_png = pygame.image.load(item_path)
selector = Selector(xmousepos, ymousepos, grid_size, grid_size)
selector_png = pygame.image.load(selector_path)
gen_png = pygame.image.load(gen_path)
gen2_png = pygame.image.load(gen2_path)
Belt.load_frames(belt_sheet, frame_width=32, frame_height=32, frame_count=16)
for column in range((screen_width-screen_width%grid_size)//grid_size):
    for row in range((screen_height-screen_height%grid_size)//grid_size):
        grid.append(Rectangle((row-1)*grid_size*2+grid_offset, column*grid_size, grid_size, grid_size,0,0,(80,80,80)))
    if grid_offset == grid_size:
        grid_offset = 0
    else:
        grid_offset += grid_size

for i in grid:
    grid2.append(Rectangle(i.xpos+grid_size, i.ypos, i.width, i.height, 0,0,(80,80,80)))
def place_belt(direction):
    global pos,xpos,ypos,add_belt
    pos = pygame.mouse.get_pos()

    xpos = (pos[0] - pos[0] % grid_size)
    ypos = (pos[1] - pos[1] % grid_size)
    for _ in belts:
        if _.xpos == xpos and _.ypos == ypos:
            del belts[belts.index(_)]
            add_belt = False
    if add_belt:
        belts.append(Belt(xpos, ypos, grid_size, grid_size, camera_offset_x, camera_offset_y, (63, 230, 252), direction))
def place_generator(direction):
    global pos,xpos,ypos,add_gen
    pos = pygame.mouse.get_pos()
    xpos = (pos[0] - pos[0] % grid_size)
    ypos = (pos[1] - pos[1] % grid_size)
    for _ in gens:
        if _.xpos == xpos and _.ypos == ypos:
            del gens[gens.index(_)]
            add_gen = False
    if add_gen:
        gens.append(Generator(xpos, ypos, grid_size, grid_size, camera_offset_x, camera_offset_y, (239, 222, 35), direction))
def rotate_belt(direction):
    global pos,xpos,ypos, last_used_direction
    pos = pygame.mouse.get_pos()
    xpos = (pos[0] - pos[0] % grid_size)
    ypos = (pos[1] - pos[1] % grid_size)
    if direction == 0 % 360:
        direction = "up"
        last_used_direction = "up"
    elif direction == 180 % 360:
        direction = "down"
        last_used_direction = "down"
    elif direction == 270 % 360:
        direction = "right"
        last_used_direction = "right"
    elif direction == 90 % 360:
        direction = "left"
        last_used_direction = "left"
    else:
        direction = "up"

    for belt_ in belts:
        if belt_.xpos == xpos and belt_.ypos == ypos:
            belt_.direction = direction
def rotate_gen(direction):
    global pos,xpos,ypos, last_used_direction
    pos = pygame.mouse.get_pos()
    xpos = (pos[0] - pos[0] % grid_size)
    ypos = (pos[1] - pos[1] % grid_size)
    if direction == 0 % 360:
        direction = "up"
        last_used_direction = "up"
    elif direction == 180 % 360:
        direction = "down"
        last_used_direction = "down"
    elif direction == 270 % 360:
        direction = "right"
        last_used_direction = "right"
    elif direction == 90 % 360:
        direction = "left"
        last_used_direction = "left"
    else:
        direction = "up"

    for gen_ in gens:
        if gen_.xpos == xpos and gen_.ypos == ypos:
            gen_.direction = direction
last_used_direction = "up"
def generator_occupies(x_, y_):
    return any(x_ == generator.xpos + grid_size // 4 and y_ == generator.ypos + grid_size // 4 for generator in gens)
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                grid_state += 1
                for j in objects:
                    for i in j:
                        i.offsetx += grid_size
                        i.xpos = i.xcenter + i.offsetx
                        pygame.time.delay(10)
            if event.key == pygame.K_d:
                grid_state += 1
                for j in objects:
                    for i in j:
                        i.offsetx -= grid_size
                        i.xpos = i.xcenter + i.offsetx
                        pygame.time.delay(10)
            if event.key == pygame.K_w:
                grid_state += 1
                for j in objects:
                    for i in j:
                        i.offsety += grid_size
                        i.ypos = i.ycenter + i.offsety
                        pygame.time.delay(10)
            if event.key == pygame.K_s:
                grid_state += 1
                for j in objects:
                    for i in j:
                        i.offsety -= grid_size
                        i.ypos = i.ycenter + i.offsety
                        pygame.time.delay(10)
            if event.key == pygame.K_1:
                place_belt(last_used_direction)
            if event.key == pygame.K_2:
                add_collector = True
                pos = pygame.mouse.get_pos()
                xpos = (pos[0] - pos[0] % grid_size)
                ypos = (pos[1] - pos[1] % grid_size)
                for i in collectors:
                    if i.xpos == xpos and i.ypos == ypos:
                        del collectors[collectors.index(i)]
                        add_collector = False
                if add_collector:
                    collectors.append(
                        Collector(
                            xpos,
                            ypos,
                            grid_size,
                            grid_size,
                            0,
                            0,
                            (0, 255, 0)))
            if event.key == pygame.K_3:
                place_generator(last_used_direction)
            if event.key == pygame.K_q:
                pos = pygame.mouse.get_pos()
                xpos = (pos[0] - pos[0] % grid_size)
                ypos = (pos[1] - pos[1] % grid_size)
                temp = 0
                for i in [belts, gens]:
                    for j in i:
                        if j.direction == "up":
                            temp = 0
                        elif j.direction == "down":
                            temp = 180
                        elif j.direction == "left":
                            temp = 90
                        elif j.direction == "right":
                            temp = 270
                        else:
                            temp = 0
                        if isinstance(j, Belt) and xpos == j.xpos and ypos == j.ypos:
                            rotate_belt((temp + 90) % 360)
                        elif isinstance(j, Generator) and xpos == j.xpos and ypos == j.ypos:
                            rotate_gen((temp + 90) % 360)
            if event.key == pygame.K_e:
                pos = pygame.mouse.get_pos()
                xpos = (pos[0] - pos[0] % grid_size)
                ypos = (pos[1] - pos[1] % grid_size)
                temp = 0
                for i in [belts, gens]:
                    for j in i:
                        if j.direction == "up":
                            temp = 0
                        elif j.direction == "down":
                            temp = 180
                        elif j.direction == "left":
                            temp = 90
                        elif j.direction == "right":
                            temp = 270
                        else:
                            temp = 0
                        if isinstance(j, Belt) and xpos == j.xpos and ypos == j.ypos:
                            rotate_belt((temp + 270)%360)
                        elif isinstance(j, Generator) and xpos == j.xpos and ypos == j.ypos:
                            rotate_gen((temp + 270)%360)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            xpos = (pos[0] - pos[0] % grid_size)
            ypos = (pos[1] - pos[1] % grid_size)
            for j in objects:
                for i in j:
                    if i.xpos == xpos and i.ypos == ypos:
                        del j[j.index(i)]

    if counter%move_delay == 0:
        for belt in belts:
            move = belt.item_move()
            if move is not None:
                item, destination = move
                moves.append((item, destination))
        for gen in gens:
            gen.generate_item()
        for i in collectors:
            if i.collect_item():
                money += 1
        for item, (new_x, new_y) in moves:
            occupied = any((other.xpos, other.ypos) == (new_x, new_y) for other in items)
            if not occupied and not generator_occupies(new_x, new_y):
                dx = new_x - item.xpos
                dy = new_y - item.ypos
                item.xpos = new_x
                item.ypos = new_y
                item.xcenter += dx
                item.ycenter += dy

    if grid_state%2 == 1:
        for i in grid:
            pygame.draw.rect(screen, i.color, pygame.Rect(i.xpos, i.ypos, i.width, i.height))
    else:
        for i in grid2:
            pygame.draw.rect(screen, i.color, pygame.Rect(i.xpos, i.ypos, i.width, i.height))
    Belt.advance_animation()
    for group in objects:
        for obj in group:
            if isinstance(obj, Belt):
                sprite = obj.animate()
                if sprite is not None:
                    screen.blit(sprite, (obj.xpos, obj.ypos))
            elif isinstance(obj, Item):
                screen.blit(pygame.transform.scale(item_png,(grid_size, grid_size)), (obj.xpos, obj.ypos))
            elif isinstance(obj, Generator):
                screen.blit(pygame.transform.scale(gen_png,(grid_size, grid_size)), (obj.xpos, obj.ypos))
                screen.blit(pygame.transform.scale(pygame.transform.rotate(gen2_png, direction_angle.get(obj.direction)+180), (grid_size, grid_size)), (obj.xpos, obj.ypos))
            else:
                pygame.draw.rect(screen, obj.color, pygame.Rect(obj.xpos, obj.ypos, obj.width, obj.height))
    selector.update_pos()
    screen.blit(pygame.transform.scale(selector_png,(grid_size, grid_size)),(selector.xpos, selector.ypos))
    text_surface = money_text.render(f"you have {money} pancakes", False, (255, 255, 255))
    screen.blit(text_surface, (quarter_grid_size, 0))
    pygame.display.flip()
    clock.tick(60)
    grid_state = grid_state%2
    add_rectangle = True
    add_item = True
    add_belt = True
    add_collector = True
    add_gen = True
    counter += 1
pygame.quit()