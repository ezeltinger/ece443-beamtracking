# ECE443 - Beamtracking Project

This is a project for ECE 443: Analog and Digital Communications to model beamtracking systems in wireless communications.

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)

## Python Virtual Environment

Before running the python scripts, install the virtual environment using these steps in a terminal from the root of the repo:

```cmd
cd scripts
create_venv.bat
```

## Running the Simulation

There is a script for each beam search method.

```cmd
cd src
python exhaustive.py
```

or

```
python upper_bound.py
```

## Examples

### Exhaustive Search - Single User

![exh-search-single-user](saved_examples/exh_search_demo.gif)

### Contiguous Beams - Single User

![contig-single-user-4](saved_examples/upper_cont_demo.gif)

![contig-single-user-18](saved_examples/upper_contiguous_search1_18beams.gif)

### Exhaustive Search - Multi User

![exh-search-multi-user-10](saved_examples/exhaustive_search10.gif)

![exh-search-multi-user-7](saved_examples/exhaustive_search7.gif)
