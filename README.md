# Yin-Yang-SAT-Solver

These are some programs for Yin-Yang solver with SAT solver algorithm and Prune-and-search algorithm.

### Requirements

* python 3.9.0
* pycosat 0.6.3

### How to run

Open cmd and run the .py files with the following command:

    python All-SAT-Solver.py
    
### Input/Output Format

The input for the first three programs with "All" in its name consists of two integers, representing the value of m and n, separated with a space.
The input format is as follows:

    3 3
    
The output consists of the number of solutions based on input, along with the duration of the algorithm. The program runs the algorithm three times to receive three different durations in a single run.
Output example:

    result =  34 , duration =  0.01975579999999999
    result =  34 , duration =  0.016975900000000044
    result =  34 , duration =  0.01856279999999999

The programs with "Alphabet" in its name requires different input. These programs can be accessed in folder "PS and SAT Comparison" folder, which is inside "Experiment" folder.
The input consist of a single integer, representing the number of empty cells.
The input format is as follows:

    e = 10

The program takes all alphabet Yin-Yang instance with e number of empty cells.
The output consists of the duration of finding a solution. The program runs the algorithm three times to receive three different durations in a single run. The program does the same thing for every alphabet variant.
Output example:

    A/Yin-Yang-A-10.in
    1
    duration =  0.04070220000000013
    1
    duration =  0.037778099999999704
    1
    duration =  0.05324649999999975
    B/Yin-Yang-B-10.in
    1
    duration =  0.0383568000000003
    1
    duration =  0.057743300000000275
    1
    duration =  0.03941870000000014
    
    ...
    
    Z/Yin-Yang-Z-10.in
    1
    duration =  0.04394699999999929
    1
    duration =  0.05061180000000043
    1
    duration =  0.06152219999999975

The program also generates a .csv file containing the running times with the format:

* ExecTimeX: For Prune-and-Search where X is the number of empty cells
* SAT-ExecTimeX: For SAT Solver where X is the number of empty cells

Feel free to edit the variable alphabet inside the program to exclude some words.

### Expeted Running Time

The more empty cells in a Yin-Yang instance, the longer the program runs.

### Experiment data

Spreadsheet of Experiment Result can be accessed in the Experiment Folder
