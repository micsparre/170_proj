# CS 170 Project Spring 2021

Take a look at the project spec before you get started!

Requirements:

Python 3.6+

You'll only need to install networkx to work with the starter code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html

If using pip to download, run `python3 -m pip install networkx`


Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `utils.py`: contains functions to compute cost and validate NetworkX graphs

- 'rando.py' : contains our random greedy solver which runs our greedy alg 8 times on 4 cores
  - we used the library: 'multiprocessing' to achieve parallelism on 4 cores

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
  - These are the functions run by the autograder to validate submissions


HOW TO RUN OUR PROJECT (done on instructional servers):
- run 'python3 solver.py' in terminal for our original solver w/o parallelism 
  - this will run a code block that runs our solver algorithm on all the inputs and creates the output files in the outputs folders. our main solver function in solver.py runs all four of our solver algorithms: solver1, solver2, solver3, and solver4 which create our outputs for each variation of our algorithm.
  - It also prints out the test in blocks of 300 (in order: large, medium, small)

- run 'python3 rando.py' in terminal for our updated random, greed algorithm
  - this will run a code block that runs our solver algorithm on all the inputs and creates the output files in the outputs folders. our main solver function in rando.py runs one solver algorithm, solver1, eight times which create our outputs for multiple random trials of deleting edges vs nodes
  - It also prints out the test in blocks of 300 (in order: large, medium, small)
