# Text-Based Snake Game

A text-based Snake game that runs in a web browser, built with Flask, Pygame, and Pybag.

## Features

- Text-based game board (50x50)
- Snake head represented by "O"
- Snake body represented by "#"
- Food represented by "+"
- Border walls represented by "-" and "|"
- Cross-platform controls (keyboard and touch)
- Settings:
  - Border behavior (kill or teleport)
  - Number of lives (1-3)
- Game state preservation
- High score tracking

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8080
```

## Controls

### Desktop
- Use WASD or arrow keys to control the snake
- Click "Start Game" to begin
- Click "Settings" to modify game settings

### Mobile
- Swipe in the desired direction to move the snake
- Use the on-screen buttons for precise control
- Tap "Start Game" to begin
- Tap "Settings" to modify game settings

## Game Rules

1. The snake grows when it eats food ("+")
2. Game over conditions:
   - Colliding with yourself
   - Colliding with walls (if borders set to "kill")
3. You have 1-3 lives (configurable in settings)
4. The game pauses when the window loses focus #   s n a k e  
 