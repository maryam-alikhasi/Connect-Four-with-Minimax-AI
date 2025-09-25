# Connect-Four-with-Minimax-AI
This project implements the **Connect Four** game with an **AI opponent** powered by the **Minimax algorithm with Alpha-Beta Pruning**, built using **Python** and **Pygame**.  
It was developed as part of the **Fundamentals and Applications of Artificial Intelligence** course at the University of Isfahan.

---

## Project Summary

- **Language**: Python 3  
- **Libraries**: NumPy, Pygame, Math, Sys  
- **Game**: Connect Four (6x7 grid) with human vs AI mode  
- **AI Technique**:  
  - Minimax Algorithm  
  - Alpha-Beta Pruning for efficiency  
  - Heuristic evaluation of board states  

---

## Features

- **Interactive Gameplay**:
  - Human player (Red) vs AI (Yellow)  
  - Graphical interface built with Pygame  

- **AI Strategy**:
  - Looks ahead multiple moves (depth = 4)  
  - Evaluates board states with a scoring function  
  - Uses Alpha-Beta Pruning to reduce computation  

- **Scoring System**:
  - Player and AI scores displayed at the top  
  - End screen with final scores and winner announcement  

- **Winning Conditions**:
  - Horizontal, vertical, and diagonal checks  

---

## Usage

Run the game:

```bash
python minimax.py
```

## Learning Outcomes
Hands-on experience implementing the Minimax algorithm with Alpha-Beta Pruning.

Applying heuristic evaluation functions for game AI.

Practical use of Pygame for building interactive games.

Understanding adversarial search in classical AI.