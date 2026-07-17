# Cayley Network Robustness Explorer

## Overview

This project explores network's structural properties by compare Cayley graph and other graphs. 

## Current Features 

- Generate undirected Cayley graphs of cyclic groups
- Support positive and negative generators using modular arithmetic
- Reject generators that create self-loops
- Print basic graph information
- Draw graphs using circular or spring layouts
- Validate behavior with pytest

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── cayley_graph.py
├── tests/
│   └── test_cayley_graph.py
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install networkx matplotlib pytest
```

## Running Tests

```bash
python -m pytest -v
```