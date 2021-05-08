# invert.py -- Matrix inversion using row reduction (with rref.py)
# Written in 2021 by Aidan Yaklin
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

import rref
import sys
from frac import fraction

def main():
    data = None
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = rref.load_matrix(f)
    else:
        data = rref.load_matrix(sys.stdin)
    if data is None:
        return

    if len(data) != len(data[0]):
        print("Matrix not invertible -- invalid dimension")
        return
    mat = []
    i = 0
    for row in data:
        col = [fraction(0)] * len(data)
        col[i] = fraction(1)
        mat.append(row + col)
        i += 1
    print(rref.strmat(mat))

    print("Row reduce...")
    rref.row_reduce(mat)

    print(rref.strmat(mat))

    i = 0
    for row in mat:
        expected = [fraction(0)] * len(mat)
        expected[i] = fraction(1)
        if row[0:len(mat)] != expected:
            print("Matrix not invertible")
            return
        i += 1

    result = [row[len(mat):2*len(mat)] for row in mat]
    print("Result: ")
    print(rref.strmat(result))

if __name__ == '__main__':
    main()
