# Unitree G1 — Tic Tac Toe Arm Movement

## Project

Reinforcement-learning reaching controller for
the Unitree G1 EDU humanoid robot.

Part of the Unitree G1 Tic Tac Toe project.

## Goal

Train the G1 to move its right arm toward
a specified 3D target position.

The robot will be sitting at a table and
playing Swedish tic-tac-toe.

## Responsibilities

This component handles:

- Right arm reaching
- Target position tracking
- Smooth joint movement
- Reaching accuracy

It does not handle:

- Finger control
- Grasping
- Object placement
- Computer vision
- Tic-tac-toe decision-making

## Project Structure

reaching/
- rewards.py
- observations.py
- actions.py
- terminations.py
- env_cfg.py

tests/
- test_reaching.py

train.py

## Reward Functions

### reaching_reward()

Rewards proximity to a target.

### success_reward()

Rewards reaching within 2 cm.

### movement_penalty()

Penalizes excessive joint velocities.

## Running Tests

From the TTT Arm Movement directory:

```powershell
python -m unittest discover -s tests -v
```

## Current Status

Reward prototypes and unit tests implemented.

Observations, actions, terminations,
Isaac Lab environment and training
are not yet implemented.

## Requirements

Offline reward tests:
- Python 3.11+
- No external dependencies

Future reinforcement-learning training:
- Isaac Sim
- Isaac Lab
- Compatible Unitree G1 EDU robot model
- Right Inspire hand model

## Note

The current XYZ coordinates are placeholders and have not been calibrated for the Unitree G1.

They must be replaced with verified coordinates once the robot's reachable workspace and coordinate system have been established in Isaac Lab.