# sud0ku_s0lver

A Python-based Sudoku solver with a graphical user interface (GUI) implemented using Tkinter.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Algorithm](#algorithm)
- [GUI](#gui)
- [Puzzle Generator](#puzzle-generator)
- [Visualization](#visualization)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to provide a Sudoku solver with an interactive GUI. The solver utilizes a backtracking algorithm to find solutions to Sudoku puzzles of varying difficulty levels. The GUI, implemented using Tkinter, allows users to input puzzles, trigger the solving process, and visualize each step.

## Features

- Sudoku solver algorithm with backtracking
- Tkinter-based GUI for user interaction
- Puzzle generator with varying difficulty levels
- Visual representation of the solving process

## Project Structure

The project is organized into the following main components:

- `src/`: Contains the source code for the Sudoku solver and GUI.
- `docs/`: Documentation files, including README, user guide, and any additional documentation.
- `tests/`: Unit tests for the solver and GUI components.
- `assets/`: Any additional assets, such as images or sample puzzles.

## Algorithm

The Sudoku solver algorithm uses a backtracking approach to explore possible solutions. Pseudocode for the solver can be found in the [Algorithm](#algorithm) section.

## GUI

The graphical user interface is implemented using Tkinter, providing users with an interactive platform to input Sudoku puzzles, trigger the solving process, and visualize the solution steps. The GUI code can be found in the `src/gui.py` file.

## Puzzle Generator

The project includes a puzzle generator that creates Sudoku puzzles of varying difficulty levels. The generator ensures that generated puzzles are solvable.

## Visualization

The GUI features visualization of the solving process, allowing users to see each step of the algorithm. Cells being considered are highlighted, and the solution progression is animated.

## Usage

To use the Sudoku solver:

1. Clone the repository: `git clone https://github.com/fletxcher/sud0ku_s0lver.git`
2. Navigate to the project directory: `cd sud0ku_s0lver`
3. Run the solver: `python src/main.py`

Follow the on-screen instructions to input Sudoku puzzles, trigger solving, and visualize the solution.

## Testing

The project includes unit tests to ensure the correctness of the solver and GUI components. Run tests using:
```bash
python -m unittest discover tests
'''


