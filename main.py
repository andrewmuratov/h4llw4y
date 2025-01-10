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
min_terminal_height = 10
min_terminal_width = 40

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

def render_hallway(stdscr, show_prompt, box_prompt, artifact_message, box_interaction_message):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

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

    if show_prompt:
        interaction_prompt = "Press SPACE to pick up the artifact"
        stdscr.addstr(height - 3, (width - len(interaction_prompt)) // 2, interaction_prompt, curses.A_BOLD)

    if box_prompt:
        box_interaction_prompt = "Press SPACE to place the artifact in the box"
        stdscr.addstr(height - 3, (width - len(box_interaction_prompt)) // 2, box_interaction_prompt, curses.A_BOLD)

    if artifact_message:
        stdscr.addstr(height - 2, (width - len(artifact_message)) // 2, artifact_message, curses.A_BOLD)

    if box_interaction_message:
        stdscr.addstr(height - 2, (width - len(box_interaction_message)) // 2, box_interaction_message, curses.A_BOLD)

    if game_won:
        win_message = "Congratulations! You have won the game!"
        stdscr.addstr(height - 3, (width - len(win_message)) // 2, win_message, curses.A_BOLD)

    stdscr.refresh()

def move_player(dx, dy):
    global player_x, player_y

    new_x = player_x + dx
    new_y = player_y + dy

    if 0 < new_x < hallway_width and 0 < new_y < hallway_length:
        if not (abs(new_x - artifact_x) < 0.2 and abs(new_y - artifact_y) < 0.2 and not artifact_picked):
            if not (abs(new_x - box_x) < 0.2 and abs(new_y - box_y) < 0.2):
                player_x = new_x
                player_y = new_y

def main(stdscr):
    global player_x, player_y, player_angle, artifact_picked, game_won

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

    last_height, last_width = stdscr.getmaxyx()
    needs_render = True

    while True:
        key = stdscr.getch()
        height, width = stdscr.getmaxyx()

        if height < min_terminal_height or width < min_terminal_width:
            stdscr.clear()
            stdscr.addstr(0, 0, "Make the terminal window bigger in order to play.", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.1)
            continue

        if (height, width) != (last_height, last_width):
            last_height, last_width = height, width
            needs_render = True
            continue

        show_prompt = not artifact_picked and abs(player_x - artifact_x) < 0.5 and abs(player_y - artifact_y) < 0.5
        box_prompt = artifact_picked and abs(player_x - box_x) < 0.5 and abs(player_y - box_y) < 0.5
        artifact_message = "You have the artifact in your inventory" if artifact_picked else None
        box_interaction_message = "Congratulations! You have won the game!" if game_won else None

        if key == curses.KEY_UP or key == ord('w'):
            move_player(speed * math.cos(player_angle), speed * math.sin(player_angle))
            needs_render = True
        elif key == curses.KEY_DOWN or key == ord('s'):
            move_player(-speed * math.cos(player_angle), -speed * math.sin(player_angle))
            needs_render = True
        elif key == curses.KEY_LEFT or key == ord('a'):
            player_angle -= rotation_speed
            needs_render = True
        elif key == curses.KEY_RIGHT or key == ord('d'):
            player_angle += rotation_speed
            needs_render = True
        elif key == ord(' '):
            if show_prompt:
                artifact_picked = True
                needs_render = True
            elif box_prompt and artifact_picked:
                game_won = True
                needs_render = True
        elif key == ord('q'):
            break

        if needs_render:
            render_hallway(stdscr, show_prompt, box_prompt, artifact_message, box_interaction_message)
            needs_render = False

if __name__ == "__main__":
    curses.wrapper(main)
