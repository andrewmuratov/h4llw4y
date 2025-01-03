![Example GIF](example.gif)

# Description

In **h4llw4y**, you control a player navigating through a hallway, with walls represented as `#` characters. The game features:

- A **first-person view** of the hallway rendered using a **raycasting technique**.
- A **dynamic minimap** showing the player’s position relative to the walls.
- A **simple control system** to move and rotate the player.
  
The game runs in your terminal using the Python `curses` library, which enables the rendering of the display and handling of user input without the need for an external graphics engine.

# Math Behind the Game

The **raycasting** algorithm is used to simulate a 3D perspective on a 2D grid. Here's a breakdown of how it works:

1. **Player Position**: The player is represented by coordinates `(player_x, player_y)` and an `angle` that determines which direction the player is facing.
2. **Raycasting**: Rays are cast from the player's position in a series of directions (based on the player’s angle) across the 2D map.
   - The rays move in the direction defined by the player's angle and check for intersections with the walls (represented by `#`).
   - For each ray, the distance between the player and the closest wall is calculated. This distance is used to determine how high to render the wall on the screen (based on the inverse of the distance).
3. **Field of View (FOV)**: The field of view defines how wide the "camera" is, simulating the player's peripheral vision. A common FOV value for 3D games is 60 degrees.
4. **Minimap**: The minimap is a scaled-down representation of the hallway grid. It shows walls as `#` characters and the player’s position as the letter `i`. The map is scaled down to fit within a smaller area in the terminal.

The basic math involves using trigonometry to calculate the direction and distance of the rays relative to the player's position and angle.

# Controls

- **W or UP Arrow**: Move the player forward in the direction they are facing.
- **S or DOWN Arrow**: Move the player backward.
- **A or LEFT Arrow**: Rotate the player counterclockwise (turn left).
- **D or RIGHT Arrow**: Rotate the player clockwise (turn right).
- **Q**: Exit the game.

# Installation

1. **Download the Game**:
Clone the repository using Git:
```bash
git clone https://github.com/andrewmuratov/h4llw4y.git
```

2. **Dependencies**:
The game requires Python 3 and the `curses` module, which is typically included by default in Unix-based systems (Linux/macOS). If you are on Windows, you may need to install `windows-curses`:
```bash
pip install windows-curses
```

# Usage

1. **Navigate to the project folder**:
```bash
cd h4llw4y
```

2. **Run the game**:
```bash
python3 main.py
```

3. The game will start in the terminal. You can use the controls to move the player around the hallway.
