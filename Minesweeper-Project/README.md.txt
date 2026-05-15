# 🤖 Minesweeper AI Solver (Logical Inference)

An advanced automated solver for Minesweeper built with **Python** and **Pygame**. This agent doesn't just play the game; it uses formal logic to deduce the board's state and make guaranteed safe moves.

## 🧠 AI Strategy & Logic
This project implements an intelligent agent based on **Constraint Satisfaction Problem (CSP)** principles:

- **Knowledge Representation:** The AI stores information in "Sentences" consisting of a set of cells and a specific mine count.
- **Inference Engine:** It uses **Subset Inference** to derive new knowledge. If one sentence is a subset of another, the AI calculates the difference to pinpoint mines or safe cells.
- **Safe Move Priority:** The agent always prioritizes moves that are logically proven to be safe.
- **Probabilistic Guessing:** When no safe move is logically available, the AI falls back to a random move to keep the game progressing.

## 🎨 Design & UI
- **Dark Industrial Theme:** A custom-designed UI with a modern dark palette for better visibility.
- **Real-time Status:** A status bar that tracks AI moves, showing whether a move was a "Safe Logic Move" or a "Random Guess".
- **Animations:** Smooth color transitions and reveal animations for an interactive experience.

## 🛠️ How to Run
1. Install Pygame: `pip install pygame`
2. Run the game: `python Minesweeper.py`