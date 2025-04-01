# 2048 As A Two-Player Game

## Overview

This project implements a two-player version of the 2048 game using the Expectiminimax algorithm. 2048 is played on a 4x4 grid where numbered tiles slide in one of four directions. In this variation, the game is modeled as a two-player interaction:

- The computer AI generates a 2 or 4 tile at a random position.

- The player selects a direction (up, down, left, or right) to move all tiles.

- Tiles continue moving until they either collide with another tile or reach the grid boundary.

- If two tiles of the same value collide, they merge into a single tile with the sum of the two values.

- Merged tiles cannot merge again in the same move.

## Features

- Implements the Expectiminimax Algorithm to model AI decision-making.

- Supports player vs. AI interaction.

- Handles tile movement, merging rules, and game-ending conditions.

- Random tile placement by AI to simulate natural gameplay.

## How It Works

1. Game Initialization:
  - A 4x4 grid is created.
  - Two random tiles (2 or 4) are placed on the board.

2. Player Move:

- The player selects a direction.
- Tiles slide accordingly, merging when necessary.

3. AI Move:

- The AI places a 2 or 4 at a random empty spot on the board.
- AI decisions are computed using Expectiminimax, which accounts for randomness and evaluates optimal moves.

4. Game Over Conditions:

- No available moves left (grid is full with no possible merges).
- Player reaches the 2048 tile (if considered a win condition).

## Installation

Make sure you have python3 installed then run:
```bash
python3 GameManager.py
