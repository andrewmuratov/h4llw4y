import curses
import math

hallway_length = 20
hallway_width = 5
field_of_view = math.radians(60)
ray_count = 120
speed = 0.2
rotation_speed = math.radians(5)

player_x = 2.5
player_y = hallway_length - 1
player_angle = 0.0

def cast_ray(px, py, angle):
    for depth in range(1, hallway_length * 10):
        ray_x = px + (depth / 10) * math.cos(angle)
        ray_y = py + (depth / 10) * math.sin(angle)

        if ray_x <= 0 or ray_x >= hallway_width or ray_y <= 0 or ray_y >= hallway_length:
            return depth / 10

    return hallway_length

def render_hallway(stdscr, key_pressed):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    for col in range(ray_count):
        ray_angle = player_angle - field_of_view / 2 + (col / ray_count) * field_of_view
        distance = cast_ray(player_x, player_y, ray_angle)

        wall_height = int(height / (distance * 2))

        column = int(col / ray_count * width)

        for row in range(height // 2 - wall_height, height // 2 + wall_height):
            if 0 <= row < height:
                stdscr.addch(row, column, '#')

    stdscr.addstr(0, 0, f"Position: ({player_x:.2f}, {player_y:.2f}) Angle: {math.degrees(player_angle):.2f} Key: {key_pressed}")

    minimap_height = 6
    minimap_width = 12
    minimap_offset_y = height - minimap_height - 1
    minimap_offset_x = width - minimap_width - 1

    minimap_scale_x = hallway_width / minimap_width
    minimap_scale_y = hallway_length / minimap_height

    for y in range(minimap_height):
        for x in range(minimap_width):
            map_x = int(x * minimap_scale_x)
            map_y = int(y * minimap_scale_y)

            if map_x == 0 or map_x == hallway_width - 1 or map_y == 0 or map_y == hallway_length - 1:
                stdscr.addch(minimap_offset_y + y, minimap_offset_x + x, '#')
            else:
                stdscr.addch(minimap_offset_y + y, minimap_offset_x + x, ' ')

    minimap_player_x = int(player_x / hallway_width * minimap_width)
    minimap_player_y = int(player_y / hallway_length * minimap_height)

    stdscr.addch(minimap_offset_y + minimap_player_y, minimap_offset_x + minimap_player_x, 'i')

    stdscr.refresh()

def move_player(dx, dy):
    global player_x, player_y

    new_x = player_x + dx
    new_y = player_y + dy

    if 0 < new_x < hallway_width and 0 < new_y < hallway_length:
        player_x = new_x
        player_y = new_y

def main(stdscr):
    global player_x, player_y, player_angle

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('w'):
            move_player(speed * math.cos(player_angle), speed * math.sin(player_angle))
            key_pressed = "Up/W"
        elif key == curses.KEY_DOWN or key == ord('s'):
            move_player(-speed * math.cos(player_angle), -speed * math.sin(player_angle))
            key_pressed = "Down/S"
        elif key == curses.KEY_LEFT or key == ord('a'):
            player_angle -= rotation_speed
            key_pressed = "Left/A"
        elif key == curses.KEY_RIGHT or key == ord('d'):
            player_angle += rotation_speed
            key_pressed = "Right/D"
        elif key == ord('q'):
            break
        else:
            key_pressed = ""

        render_hallway(stdscr, key_pressed)

if __name__ == "__main__":
    curses.wrapper(main)
