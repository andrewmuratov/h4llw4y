# Description

In **h4llw4y**, you control a player navigating through a hallway, with walls represented as characters. The game features:

- A **first-person view** of the hallway rendered using a **raycasting technique**.
- A **simple control system** to move and rotate the player.
  
The game runs in your terminal using the Python `curses` library, which enables the rendering of the display and handling of user input without the need for an external graphics engine.

# Math Behind the Game

The **raycasting** algorithm is used to simulate a 3D perspective on a 2D grid. Here's a breakdown of how it works:

1. **Player Position**: The player is represented by coordinates `player_x`, `player_y` and an `angle` that determines which direction the player is facing.

2. **Raycasting**: Rays are cast from the player's position in a series of directions (based on the player’s angle) across the 2D map.
   - The rays move in the direction defined by the player's angle and check for intersections with the walls (represented by `#`).
   - For each ray, the distance between the player and the closest wall is calculated. This distance is used to determine how high to render the wall on the screen (based on the inverse of the distance).

   The formula for calculating the intersection point of a ray with a wall is derived using basic trigonometry. For a given ray angle `θ`, the coordinates of the intersection point can be expressed as:

   ```
   ray_x = player_x + distance * cos(θ)
   ray_y = player_y + distance * sin(θ)
   ```

3. **Field of View (FOV)**: The field of view defines how wide the "camera" is, simulating the player's peripheral vision. A common FOV value for 3D games is 60 degrees. To calculate the rays from the player's position, we need to cast rays at angles between the player's angle minus half of the FOV and the player's angle plus half of the FOV:

   ```
   ray_angle = player_angle - (FOV / 2) + (col / ray_count) * FOV
   ```

   where `col` is the column in the screen and `ray_count` is the total number of rays to cast.

4. **Wall Rendering**: The distance to the wall is inversely proportional to the height of the wall on the screen. Closer walls will be rendered higher, while distant walls will appear shorter. The height of each wall is calculated using the following formula:

   ```
   wall_height = screen_height / (2 * distance)
   ```

5. **Minimap**: The minimap is a scaled-down representation of the hallway grid. It shows walls as `#` characters and the player’s position as the letter `i`. The map is scaled down to fit within a smaller area in the terminal.

# Controls

- **W or UP Arrow**: Move the player forward in the direction they are facing.
- **S or DOWN Arrow**: Move the player backward.
- **A or LEFT Arrow**: Rotate the player counterclockwise (turn left).
- **D or RIGHT Arrow**: Rotate the player clockwise (turn right).
- **Q**: Exit the game.

# Installation and Testing

## Dependencies

1. **Python 3**: The game requires Python 3, which you can download and install from [python.org](https://www.python.org/downloads/).
2. **Curses Library**: The game uses the `curses` library for rendering the game in the terminal. It is typically included by default in Unix-based systems (Linux/macOS). If you are using Windows, you will need to install the `windows-curses` package:
   ```bash
   pip install windows-curses
   ```

## Installation for All Operating Systems

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/andrewmuratov/h4llw4y.git
   ```

2. **Navigate to the project folder**:
   ```bash
   cd h4llw4y
   ```

3. **Install Dependencies**:
   If you're on Windows, you may need to install `windows-curses` as mentioned above. Otherwise, you can skip this step on Linux/macOS/Unix/BSD.

4. **Run the Game**:
   ```bash
   python3 main.py
   ```

## Testing the Game

The game should run directly in the terminal. Resize the terminal window and make sure the game adjusts accordingly. Use the arrow keys and the `W`, `A`, `S`, `D` keys to move and rotate the player. Make sure the interactions with the artifacts and box work correctly.

# Gameplay

In the **h4llw4y** game, you control a player navigating through a hallway. Your goal is to pick up an artifact and place it in a box.

![Example GIF](example.gif)

**Controls**:
- **W or UP Arrow**: Move the player forward.
- **S or DOWN Arrow**: Move the player backward.
- **A or LEFT Arrow**: Rotate the player counterclockwise.
- **D or RIGHT Arrow**: Rotate the player clockwise.
- **Q**: Exit the game.

When you approach the artifact, press `SPACE` to pick it up. Then, approach the box and press `SPACE` again to place the artifact inside and win the game.
