# Dungeon Descent

A turn-based card game where you battle through a dungeon, using attack and defense cards to defeat enemies and progress through floors.

## Game Overview

Dungeon Descent is a Python-based card game built with Pygame. Players take on the role of an adventurer descending through a dungeon, battling various enemies using a deck of attack and defense cards. The game features turn-based combat, card management, and progressive difficulty as you advance through floors.

## Features

- Turn-based combat system
- Card-based gameplay with attack and defense mechanics
- Energy management system
- Progressive difficulty through multiple floors
- Animated character and enemy sprites
- Sound effects and background music
- Health and energy tracking
- Card selection and management

## Requirements

- Python 3.x
- Pygame
- MoviePy (for video playback)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jasrulete/dungeon-descent.git
```

2. Install the required dependencies:
```bash
pip install pygame moviepy
```

3. Run the game:
```bash
python start.py
```

## Game Controls

- Mouse: Click to select and play cards
- Mouse: Click "End Turn" button to end your turn
- Mouse: Click "Retry" button when game over

## Game Mechanics

### Cards

The game features several types of cards:

#### Attack Cards:
- Basic Attack (5 damage, 1 energy)
- Slash (2 damage, 1 energy)
- Poison Stab (5 damage, 1 energy)
- Havoc (10 damage, 2 energy)
- Heavy Slash (10 damage, 2 energy)
- Die (20 damage, 3 energy)

#### Defense Cards:
- Shield (5 shield, 1 energy)
- Acrobatics (0 energy)

### Energy System

- Players start each turn with 3 energy
- Cards have different energy costs
- Energy resets at the start of each turn

### Health System

- Both player and enemies have health points
- Health is displayed via health bars
- Game over when player health reaches 0

## Directory Structure

- `main.py` - Main game logic
- `start.py` - Game initialization and main menu
- `cards.py` - Card class definitions
- `mob.py` - Enemy definitions
- `gamestate.py` - Game state management
- `sounds.py` - Sound effects and music
- `reward.py` - Reward system
- `Sprites/` - Contains all game sprites
- `Cards/` - Contains card images
- `Audio/` - Contains sound effects and music
- `Video/` - Contains game videos
- `Scripts/` - Contains fonts and other scripts
