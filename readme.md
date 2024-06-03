### README for Isometric Tile-Based Game with Combat

## Overview

This is an isometric tile-based game developed using Pygame. The game features a player character that can move around an isometric map and engage in combat with enemies. Players can attack enemies by clicking on them, and the attack will continue until the enemy dies. The game includes basic stats and combat mechanics using d20 rolls.

## Features

- Isometric tile-based map
- Player and enemy characters with simple animations
- Combat system based on d20 rolls and stats
- Mouse click interaction for movement and attacking enemies

## Default Stats

### Player Stats:
- Strength (str): 1
- Defense (def): 1
- Accuracy (acc): 1
- Health Points (hp): 10

### Enemy Stats:
- Strength (str): 0
- Defense (def): 0
- Accuracy (acc): 0
- Health Points (hp): 5

## Controls

- **W**: Move Up
- **A**: Move Left
- **S**: Move Down
- **D**: Move Right
- **Mouse Click**: Move to location or attack enemy

## How to Play

1. **Movement**: Use the W, A, S, and D keys to move your character around the map. The character will always be centered on the screen.
2. **Attacking Enemies**: Click on an enemy to start attacking it. The attack will continue until the enemy's health drops to zero.
3. **Combat Mechanics**: Combat is resolved using d20 rolls. The attack roll is calculated as `d20 + strength`, and the defense roll is calculated as `d20 + defense`. The damage dealt is the difference between the attack roll and the defense roll.
