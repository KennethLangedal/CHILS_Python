# CHILS_Python

Python wrapper for the CHILS heuristic

## How to Use

The following example illustrates how to apply the heuristic. It creates a graph with three vertices and then runs the full CHILS algorithm using four concurrent solutions for 20 seconds.

```python
import chils

solver = chils.CHILS()

solver.add_vertex(10)
solver.add_vertex(10)
solver.add_vertex(20)

solver.add_edge(0, 1)
solver.add_edge(0, 2)

solver.run_full(20.0, 4, 0)

print(solver.get_solution_weight())
```

## Development

To clone this repository, including the CHILS submodule, run:

```bash
git clone --recursive https://github.com/KennethLangedal/CHILS_Python.git
```

If you have already cloned the repository, you can initialize the submodule with:

```bash
git submodule update --init --recursive
```
