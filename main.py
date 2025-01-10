import curses
import math
import time

hallway_length = 20
hallway_width = 5
field_of_view = math.radians(60)
ray_count = 120
speed = 0.2
rotation_speed = math.radians(5)

player_x = 2.5
player_y = hallway_length - 1
player_angle = 0.0
artifact_x = hallway_width / 2
artifact_y = hallway_length / 2
artifact_picked = False
box_x = hallway_width / 4
box_y = hallway_length / 4
game_won = False
steps_taken = 0

start_time = time.time()

min_terminal_height = 10
min_terminal_width = 40

paused = False
game_running = True

def cast_ray(px, py, angle):
    for depth in range(1, hallway_length * 10):
        ray_x = px + (depth / 10) * math.cos(angle)
        ray_y = py + (depth / 10) * math.sin(angle)

        if ray_x <= 0 or ray_x >= hallway_width or ray_y <= 0 or ray_y >= hallway_length:
            return depth / 10, ray_x, ray_y

        if not artifact_picked and abs(ray_x - artifact_x) < 0.2 and abs(ray_y - artifact_y) < 0.2:
            return depth / 10, ray_x, ray_y

        if abs(ray_x - box_x) < 0.2 and abs(ray_y - box_y) < 0.2:
            return depth / 10, ray_x, ray_y

    return hallway_length, None, None

def render_walls(stdscr, height, width):
    for col in range(ray_count):
        ray_angle = player_angle - field_of_view / 2 + (col / ray_count) * field_of_view
        distance, ray_x, ray_y = cast_ray(player_x, player_y, ray_angle)

        wall_height = int(height / (distance * 2))
        column = int(col / ray_count * width)

        wall_char = ' '
        color_pair = curses.color_pair(5)

        if ray_x is not None and ray_y is not None:
            if not artifact_picked and abs(ray_x - artifact_x) < 0.2 and abs(ray_y - artifact_y) < 0.2:
                wall_char = '|'
                color_pair = curses.color_pair(6)
            elif abs(ray_x - box_x) < 0.2 and abs(ray_y - box_y) < 0.2:
                wall_char = 'X'
                color_pair = curses.color_pair(7)
            elif ray_x <= 0:
                wall_char = 'L'
                color_pair = curses.color_pair(3)
            elif ray_x >= hallway_width:
                wall_char = 'R'
                color_pair = curses.color_pair(4)
            elif ray_y <= 0:
                wall_char = 'B'
                color_pair = curses.color_pair(2)
            elif ray_y >= hallway_length:
                wall_char = 'F'
                color_pair = curses.color_pair(1)

        for row in range(height // 2 - wall_height, height // 2 + wall_height):
            if 0 <= row < height:
                stdscr.addch(row, column, wall_char, color_pair)

def render_hud(stdscr, height, width):
    hud_message = "Inventory: Artifact" if artifact_picked else "Inventory: Empty"
    stdscr.addstr(1, (width - len(hud_message)) // 2, hud_message, curses.A_BOLD)

    if game_won:
        win_message = "Congratulations! You have won the game!"
        stdscr.addstr(height - 2, (width - len(win_message)) // 2, win_message, curses.A_BOLD)

    elapsed_time = int(time.time() - start_time) if not paused else int(start_time - paused_time)
    time_message = f"Time: {elapsed_time // 60:02}:{elapsed_time % 60:02}"
    stdscr.addstr(2, (width - len(time_message)) // 2, time_message, curses.A_BOLD)

    steps_message = f"Steps: {steps_taken}"
    stdscr.addstr(3, (width - len(steps_message)) // 2, steps_message, curses.A_BOLD)

def render_scene(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    render_walls(stdscr, height, width)
    render_hud(stdscr, height, width)

    stdscr.refresh()

def move_player(dx, dy):
    global player_x, player_y, steps_taken

    new_x = player_x + dx
    new_y = player_y + dy

    if 0 < new_x < hallway_width and 0 < new_y < hallway_length:
        if not (abs(new_x - artifact_x) < 0.2 and abs(new_y - artifact_y) < 0.2 and not artifact_picked):
            if not (abs(new_x - box_x) < 0.2 and abs(new_y - box_y) < 0.2):
                player_x = new_x
                player_y = new_y
                steps_taken += 1

def reset_game():
    global player_x, player_y, player_angle, artifact_picked, game_won, steps_taken, start_time
    player_x = 2.5
    player_y = hallway_length - 1
    player_angle = 0.0
    artifact_picked = False
    game_won = False
    steps_taken = 0
    start_time = time.time()

def main_menu(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    menu_options = ["Start Game", "Instructions", "Exit"]
    selected = 0

    while True:
        stdscr.clear()
        for idx, option in enumerate(menu_options):
            if idx == selected:
                stdscr.addstr(height // 2 + idx, (width - len(option)) // 2, option, curses.A_REVERSE)
            else:
                stdscr.addstr(height // 2 + idx, (width - len(option)) // 2, option)

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu_options) - 1:
            selected += 1
        elif key == ord('\n'):
            return selected

        stdscr.refresh()

def settings_menu(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    settings_options = ["Back to Menu"]
    selected = 0

    while True:
        stdscr.clear()
        for idx, option in enumerate(settings_options):
            if idx == selected:
                stdscr.addstr(height // 2 + idx, (width - len(option)) // 2, option, curses.A_REVERSE)
            else:
                stdscr.addstr(height // 2 + idx, (width - len(option)) // 2, option)

        key = stdscr.getch()

        if key == ord('\n'):
            return

        stdscr.refresh()

def pause_menu(stdscr):
    global paused_time
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    pause_message = "Game Paused. Press P to Resume."
    stdscr.addstr(height // 2, (width - len(pause_message)) // 2, pause_message, curses.A_BOLD)
    stdscr.refresh()

    paused_time = time.time()

    while True:
        key = stdscr.getch()
        if key == ord('p'):
            break

def main_game(stdscr):
    global player_x, player_y, player_angle, artifact_picked, game_won, paused, game_running, start_time, paused_time

    curses.curs_set(0)
    stdscr.nodelay(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)

    last_input_time = time.time()

    while game_running:
        key = stdscr.getch()
        current_time = time.time()

        if key == curses.KEY_UP or key == ord('w'):
            if not paused:
                move_player(speed * math.cos(player_angle), speed * math.sin(player_angle))
                last_input_time = current_time
        elif key == curses.KEY_DOWN or key == ord('s'):
            if not paused:
                move_player(-speed * math.cos(player_angle), -speed * math.sin(player_angle))
                last_input_time = current_time
        elif key == curses.KEY_LEFT or key == ord('a'):
            player_angle -= rotation_speed
            last_input_time = current_time
        elif key == curses.KEY_RIGHT or key == ord('d'):
            player_angle += rotation_speed
            last_input_time = current_time
        elif key == ord(' '):
            if not artifact_picked and abs(player_x - artifact_x) < 0.5 and abs(player_y - artifact_y) < 0.5:
                artifact_picked = True
            elif artifact_picked and abs(player_x - box_x) < 0.5 and abs(player_y - box_y) < 0.5:
                game_won = True
            last_input_time = current_time
        elif key == ord('r'):
            reset_game()
            last_input_time = current_time
        elif key == ord('e'):
            settings_menu(stdscr)
        elif key == ord('p'):
            pause_menu(stdscr)
        elif key == ord('q'):
            game_running = False

        if current_time - last_input_time < 0.2 or game_won:
            render_scene(stdscr)

def main(stdscr):
    selection = main_menu(stdscr)

    if selection == 0:
        main_game(stdscr)
    elif selection == 1:
        stdscr.clear()
        instructions = "Use WASD or Arrow keys to move. Space to interact. P to pause, Q to quit. R to restart, E to go to settings."
        stdscr.addstr(0, 0, instructions)
        stdscr.refresh()
        stdscr.getch()
        main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
