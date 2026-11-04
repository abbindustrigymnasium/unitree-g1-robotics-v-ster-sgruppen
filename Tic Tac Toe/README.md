# Unitree G1 Tic-Tac-Toe — Game AI

## Description

Game AI for a Unitree G1 EDU humanoid robot playing
Swedish-style tic-tac-toe against a human.

Developed as Group 1 of the robotics project.

## Game Rules

- Human plays X.
- Robot plays O.
- Human goes first.
- Each player has three pieces.
- Players alternate placing pieces.
- Once all six pieces are placed, players move
  their existing pieces instead.
- Pieces can move to any empty square.
- Three pieces in a row wins.
- Repeated positions do not automatically end the game.

## Difficulty Levels

- easy
- medium
- hard
- expert

## Board Format

The board is represented as a 3x3 Python list.

Example:

```python
board = [
    ["X", "", "O"],
    ["", "X", ""],
    ["", "", ""]
]
```

Coordinates use (row, column), indexed from 0 to 2.

## API

Import:

```python
from game.api import get_robot_move
```

Call:

```python
move = get_robot_move(board, difficulty="medium")
```

Return values:

### Placement phase

```python
(None, (1, 2))
```

The robot should take an unused O piece and place
it at row 1, column 2.

### Movement phase

```python
((0, 0), (1, 2))
```

The robot should pick up its existing piece at
row 0, column 0 and move it to row 1, column 2.

### Finished game

Returns:

```python
None
```

If the game has already been won.

### Invalid input

Raises `ValueError` for invalid boards, difficulty
settings, or calls made on the wrong turn during placement.

During the movement phase, the task planner must
track whose turn it is.

## Running the Game

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Dependencies

Python 3.11 or newer.

No external packages required.

## Integration

Group 2 provides board states and difficulty selection.

Group 3 calls the game AI and executes the returned move.

Groups 4–6 handle physical movement of the Unitree G1.