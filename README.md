# POO-proyect
This project consists of the development of a domotic circuit simulator made in Python. The team members are Carlos Raul Rojas Vergara, Angel Arturo Varela Duque, and Javier Camilo Orduz Acero, all students of Electronic Engineering at the National University of Colombia, for the Object-Oriented Programming course.

Within the design process, the first stage is ideation and the creation of the conceptual design. At this step, we need to define the product’s functional and non-functional requirements, create graphical sketches of the UI, and develop high-level diagrams as part of the brainstorming for the technical design and the future software implementation. Everything related to this step is located in the folder "Workshop_1".


## Prototype (PyQt5)

This repository contains a working prototype of the simulator implemented with Python and PyQt5. Key files:

- `sourceCode/gui.py` — main PyQt5 UI and canvas
- `sourceCode/workSpace.py` — model and save/load logic
- `sourceCode/components.py` — component factory and simple behaviors
- `sourceCode/main.py` — example runner that spawns the GUI

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python sourceCode/main.py
```

There's a basic grid/snapping behavior, autosave to the currently open file, and a prototype simulation loop.

Tests are under `tests/` and can be run with `python -m unittest`.

If you modify the code, please run the tests and verify the GUI starts.
