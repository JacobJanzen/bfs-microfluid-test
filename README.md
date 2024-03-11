# Breadth-First Search Microfluidic Grid Mixing Test

Generate every possible output of microfluidic grid mixing up to a specified depth.
The results are dumped to a csv file. It also looks for the maximum denominator on
every path. Any outputs which have a maximum denominator greater than the largest
denominator in the output is printed to the screen. There does not seem to ever be
any outputs of that type.

To run: `python3 main.py [num_zeros] [num_ones] [max_depth]`.
