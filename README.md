
# Dynamic Maze Solver

## Overview
This project implements a **Dynamic Maze Solver** in Python using **Pygame** for visualization. The program dynamically adjusts the maze as the agent solves it, showcasing pathfinding algorithms like **Manhattan Distance**, **A\***, and **Dynamic A\***. It provides an interactive interface to visualize and analyze these algorithms' behavior in real-time.

## Features
- **Dynamic Maze Generation:** Walls dynamically change after each agent move.
- **Pathfinding Algorithms:**
  - **Manhattan Distance**
  - **A*** with real-time updates
  - **Dynamic A***
- **Real-Time Visualization:** See the agent’s decisions and maze changes step-by-step.
- **Metrics Tracking:** Steps taken and nodes expanded are recorded for analysis.

## Requirements
- Python 3.x
- Libraries:
  - `pygame`
  - `numpy`

To install the required dependencies, run:
```bash
pip install pygame matplotlib numpy
```

## How to Run
1. Clone the repository or download the `main.py` file.
2. Ensure the required dependencies are installed.
3. Run the script using:
   ```bash
   python main.py
   ```
4. The program starts with a menu:
   - Select a pathfinding algorithm to visualize.
   - Use the GUI to interact with the maze.

## Controls
- **Arrow Keys:** Move the agent manually (if the game is stopped).
- **Spacebar:** Toggle the origin indicator.
- **S Key:** Start/Stop the agent's automated solving process.

## Visualization
The maze and agent are displayed in a **720x720 grid**. The interface includes:
- **Sidebar:** Start/Stop controls and navigation back to the menu.
- **Indicators:** Highlighted cells for the agent's position, goal, and path.

## Customization
You can modify the following constants in the script to adjust the behavior:
- `N_ITERATION`: Number of mazes to solve.
- `WALL_CHANGE_COEFF`: Walls changed after each move.
- `INITIAL_WALL_CHANGE`: Walls changed during initial maze generation.
- `TICKS`: Speed of the simulation.

## Authors
- **Mher Beginyan**
- **Sofi Khachatryan**
- **Veronika Khachatryan**

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to use and expand this project for educational purposes or further research on dynamic pathfinding algorithms!
