grid_size = 32
quarter_grid_size = grid_size//4
half_grid_size = grid_size//2
belts = []
items = []
gens = []
collectors = []
objects = [belts,gens,collectors,items]
add_rectangle:bool = True
add_item:bool = True
add_belt:bool = True
add_gen:bool = True
camera_offset_x = 0
camera_offset_y = 0
grid_offset = 0
grid = []
grid2 = []
grid_state = 0
x = []
y = []
move_delay = 30
belt_anim_speed = 5
belt_anim_frame = 0
belt_anim = []
counter = 0
money = 0
moves = []
last_used_direction = 0
directions = ["up", "down", "left", "right"]
offsets = {
    "up": (0, -grid_size),
    "down": (0, grid_size),
    "left": (-grid_size, 0),
    "right": (grid_size, 0)
}
direction_angle = {
        "right": 270,
        "up": 0,
        "left": 90,
        "down": 180,
}