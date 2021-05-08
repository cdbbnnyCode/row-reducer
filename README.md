# RREF: Matrix row reduction calculator
Something I made for linear algebra class. Row reduces matrices using a
relatively slow and simple three-step algorithm:  
1. Sort and combine rows until the matrix is in echelon form
2. Scale each row so that each pivot position is 1
3. Combine rows upward so that pivot columns only contain a pivot position.

### How to use
This is a command-line tool, and does not have a graphical interface (for now).

You will need Python 3 or above to run this tool.

* First, clone the code onto your computer (using the Code button on GitHub)
* Unzip the downloaded file and open a command prompt in the unzipped folder
* Type `python rref.py` and press Enter.
* Type in the matrix you want to reduce and hit Enter again. The program will
  output each step of the process until it is completed.

Matrix entries are comprised of integers (0, 1, -5, 23907, etc.) or fractions
(1/2, 22/7, etc.) Entries are separated by spaces, for example:
```
1    0 -1
0  1/4  5
2 -1/2  3
```

`rref.py` can also load a matrix from a file, if the filename is passed as a
command-line argument:
```
python rref.py file.txt
```

There is an additional tool, `invert.py`, which can invert matrices via
row operations. Usage is very similar to `rref.py`.

### Pitfalls
A few matrices will fail to row reduce due to 0/0 appearing in some rows.
I am not entirely sure why this happens.

### License
This project is released into the public domain. See LICENSE.txt for details.
The license text is also available at [http://creativecommons.org/publicdomain/zero/1.0/](http://creativecommons.org/publicdomain/zero/1.0/).
