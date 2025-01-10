# Hallway Adventure Game

A simple 2D raycasting game where you explore a hallway, interact with objects, and collect an artifact to win the game.

## Features
- **Raycasting Visualization**: The game uses raycasting to simulate a first-person view of the hallway, rendering walls and objects.
- **Movement**: Move around the hallway using the WASD keys or arrow keys.
- **Interaction**: Pick up an artifact and bring it to a box to win the game.
- **Pause Menu**: Pause the game and resume at any time by pressing "P".
- **HUD**: Displays important game information such as inventory status, time elapsed, and steps taken.
- **Menus**: Includes a main menu, instructions screen, and a settings menu.
- **Restart**: Restart the game using the "R" key.

## Requirements
- Python 3.x
- `curses` library (built-in on most Unix-like systems, such as Linux or macOS)
  - On Windows, you may need to install `windows-curses` via `pip install windows-curses`.

## Controls
- **W** or **Up Arrow**: Move forward
- **S** or **Down Arrow**: Move backward
- **A** or **Left Arrow**: Rotate left
- **D** or **Right Arrow**: Rotate right
- **Space**: Interact (Pick up artifact or place it in the box)
- **P**: Pause the game
- **Q**: Quit the game
- **R**: Reset the game
- **E**: Open the settings menu

## Instructions
1. Start the game from the main menu.
2. Use the arrow keys or WASD to navigate through the hallway.
3. Look for the artifact (represented by `|`) and pick it up by pressing Space.
4. Once you have the artifact, head to the box (represented by `X`) and press Space again to win the game.
5. You can pause the game at any time by pressing "P" and resume by pressing "P" again.
6. If you wish to restart, press "R".

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/andrewmuratov/h4llw4y.git
   cd h4llw4y
   ```

2. Ensure you have Python 3.x installed on your system.

3. If using Windows, install `windows-curses` to enable `curses` support:
   ```bash
   pip install windows-curses
   ```

4. Run the game:
   ```bash
   python game.py
   ```

## Demo
Here’s an example of the gameplay in action:

![Gameplay Demo](example.gif)

## License
This project is licensed under the **Unlicense** - see the [LICENSE](LICENSE) file for details.
