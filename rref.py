# rref.py - A naive implementation of row reduction
# Written in 2021 by Aidan Yaklin
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from frac import fraction
import math
import sys
import time
import re

###########################
# Utility functions
# -- scroll down to the main() function for the actual algorithm

# Format a matrix (array of same-length arrays) to a string.
def strmat(mat):
    if len(mat) == 0:
        return '[]'
    # find out how many characters wide each column should be
    widths = [0] * len(mat[0])

    for y in range(len(mat)):
        for x in range(len(mat[0])):
            widths[x] = max(widths[x], len(str(mat[y][x])))

    # format each column
    out = ''
    for y in range(len(mat)):
        out += '[ '
        for x in range(len(mat[0])):
            # '%%%ds' creates a variable-length string
            #    %%,%d,s -> e.g. '%3s'
            out += ('%%%ds ' % widths[x]) % mat[y][x]
        out += ']\n'
    return out

# Read a matrix from stdin or a file
def load_matrix(f):
    width = -1
    data = []
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        values = [fraction(x) for x in re.split(r'\s+', line)]
        if width < 0:
            width = len(values)
        else:
            if len(values) != width:
                raise IndexError("All rows must be the same size")
        data.append(values)
    return data

def leading(mat, row):
    for i in range(len(mat[0])):
        if mat[row][i] != 0:
            return i
    return -1

def row_swap(mat, row1, row2, interactive=False, delay=1):
    temp = mat[row2]
    mat[row2] = mat[row1]
    mat[row1] = temp
    if interactive:
        print("Swap row %d <-> row %d:" % (row1, row2))
        print(strmat(mat))
        time.sleep(delay)

def row_mul(mat, row, factor, interactive=False, delay=1):
    for i in range(len(mat[0])):
        mat[row][i] *= factor
    if interactive:
        print("row %d *= %s:" % (row, factor))
        print(strmat(mat))
        time.sleep(delay)

def row_combine(mat, dst, src, factor, interactive=False, delay=1):
    for i in range(len(mat[0])):
        mat[dst][i] += mat[src][i] * factor
    if interactive:
        print("row %d += %s * row %d" % (dst, factor, src))
        print(strmat(mat))
        time.sleep(delay)

def is_reduced(mat, col):
    has_leading = False
    for i in range(len(mat)):
        if mat[i][col] == 1:
            pass # TODO

def row_reduce(data, interactive=False, delay=1):
    # Augmented matrix must be at least 1x2
    if len(data) < 1 or len(data[0]) < 2:
        raise IndexError("Augmented matrix must be at least 1x2")

    # step 1: echelon form
    if interactive: print(strmat(data))

    while True:
        if interactive: print('[iterate]')
        changes = False
        curr_lead = -1
        curr_lead_row = -1
        for row in range(len(data)):
            new_lead = leading(data, row)
            if new_lead < 0: # all zeros
                if interactive: print('[row %d empty]' % row)
            elif new_lead < curr_lead:
                if interactive: print('[row %d behind row %d -- rearrange]' % (row, curr_lead_row))
                row_swap(data, row, curr_lead_row, interactive, delay)
                changes = True
                break
            elif new_lead == curr_lead:
                if interactive: print('[lead in row %d directly below row %d -- eliminate]' % (row, curr_lead_row))
                # eliminate using elements along the diagonal--these should be
                # pivot points by the time we get to them
                value_to_remove = data[row][new_lead]
                elim_factor = -value_to_remove / data[new_lead][new_lead]
                row_combine(data, row, new_lead, elim_factor, interactive, delay)
                changes = True
            else: # new_lead > curr_lead
                if interactive: print("[leading row OK]")
                curr_lead_row = row
                curr_lead = new_lead
        if not changes:
            break

    # step 2: normalize
    if interactive: print("Echelon form found--normalizing")
    for row in range(len(data)):
        lcol = leading(data, row)
        if lcol >= 0:
            row_mul(data, row, 1 / data[row][lcol], interactive, delay)

    # step 3: reduce
    if interactive: print("Normalization complete--reducing")
    for row in reversed(range(len(data))):
        lcol = leading(data, row)
        if lcol >= 0:
            for nrow in reversed(range(0, row)):
                if data[nrow][lcol] != 0:
                    # subtract off with row
                    factor = -data[nrow][lcol] / data[row][lcol]
                    row_combine(data, nrow, row, factor, interactive, delay)

def main():
    data = None
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = load_matrix(f)
    else:
        print("Enter matrix:")
        data = load_matrix(sys.stdin)
    if data is None:
        return
    # print(strmat(data))
    row_reduce(data, interactive=True)
    print("->")
    print()
    print(strmat(data))


if __name__ == '__main__':
    main()
