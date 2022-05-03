# ECE443 - Beamtracking Project

This is a project for ECE 443: Analog and Digital Communications to model beamtracking systems in wireless communications.
Based on a paper that can be found [here](https://arxiv.org/abs/2001.06595).

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)
- numpy
- scipy
- matplotlib
- imageio

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
python contiguous.py
```

```
python non-contiguous.py
```

### Other Scripts

- playground.py
    - Produces animations of each beam in the search algorithms as a plot and a gif in `./output/`.
    - Uncomment the desired functions in `if __name__ == "__main__"` block to produce the desired animation.
- algorithm_comp.py
    - Plots a comparison of each of the search algorithms.

## Examples

### Exhaustive Search - Single User

![exh-search-single-user](saved_examples/exh_search_demo.gif)

### Contiguous Beams - Single User

![contig-single-user-4](saved_examples/upper_cont_demo.gif)

![contig-single-user-18](saved_examples/upper_contiguous_search1_18beams.gif)

### Non-Contiguous Beams - Single user

![non-contig-single-user-3](saved_examples/non_contiguous_searchb3.gif)

![non-contig-single-user-5](saved_examples/non_contiguous_searchb5.gif)

### Exhaustive Search - Multi User

![exh-search-multi-user-10](saved_examples/exhaustive_search10.gif)

![exh-search-multi-user-7](saved_examples/exhaustive_search7.gif)
