# Laboratory 2: Simple Spatial Objects in Python

## Required Dependencies
Before starting, make sure that you have installed the following dependencies:

- **[Python](https://www.python.org/downloads/) >= 3.14**
- **[pip](https://pip.pypa.io/en/stable/installation/) >= 26.2.1**

# Set up the Virtual Environment

## Create a Python Virtual Environment
Create a Python virtual env (venv):

```
python3 -m venv .venv
```

Run the virtual environment:
```
source .venv/bin/activate
```

## Install pandas and matplotlib
Upgrade pip and install libraries.

```
# Update and upgrade pip version
pip install --upgrade pip
# Install pandas and matplotlib
pip install pandas matplotlib
```

Save the installed packages.

```
pip freeze > requirements.txt
```

## How to run Python scripts
Run the runner script using the following command:

```
python3 src/run_lab2.py
```

# Directory Structure
```
├── data                    # Data files
│   └── points.csv          # Contains the point data
├── output                  # Output files
├── src                     # Source files
│   ├── demo.py             # Demo code
│   ├── run_lab2.py         # Running and generation of outpus
│   └── spatial.py          # Main logic
├── test                    # Test files
│   └── test_spatial.py     # File of unit testing
└── requirements.txt        # List of dependencies
```
#### Notes on files:
- **run_lab2.py** was not written in classes and methods since wrapping the execution steps / orchestrator / entry point in an artificial class will only introduce unnecessary complexity (over-engineering) without delivering any OOP benefits like code reusability.
- **test_spatial.py** is empty since no unit testing was done in this lab exercise.

# Reflections
### 1. Object vs Geometry
#### *How did modeling points as objects change the way you thought about the data compared to treating them as rows in a table?*

Instead of viewing a point as just an X and Y column in a spreadsheet, the Point object became a self-contained unit responsible for validating its own coordinates and executing spatial operations like distance calculations. Similarly, instead of viewing a dataset as just a passive shapefile layer, the PointSet object became a "manager" capable of controlling how a set of points interact. This shifted my thinking from "what database operations do I run on this table?" to "what capabilities should this spatial object possess?"


### 2. Responsibility
#### *Which behaviors belonged in Point, which belonged in PointSet, and which belonged in the runner script? Give one concrete example.*

For the Point object, an example behavior is calculating the distance from itself to another point. For PointSet, it is calculating the bounding box. For the runner script, it is the generation of outputs (scatter plots and data dictionaries).

In this setup, each component only owns the logic that belongs to it. The Point class owns the distance calculation since this only requires knowledge about individual coordinate pairs, which is an intrinsic property of points. The PointSet class owns the bounding box calculation because individual points are unaware of the existence of other points. Finally, the runner script owns output generation so that non-spatial operations remain decoupled from the core spatial objects.


### 3. Modeling Insight
#### *How did separating geometry, meaning, and behavior make the spatial logic easier (or harder) to understand?*

Separating geometry and behavior made the overall spatial logic much easier to understand and debug, despite adding initial setup complexity. In a flat GIS attribute table, coordinates and metadata are lumped together, and calculations depend entirely on external software tools. By separating them, the logic became modular. In this case, the Point class handles coordinate math, PointSet manages collection boundaries, and the runner script handles visualization.


## 👤 Author
**ALLAN FRITZGERALD N. AMISTOSO** <br>
2014-73618 <br>
MS Geomatics Engineering - Geoinformatics
