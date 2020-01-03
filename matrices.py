import math
from Row_Col import Row, Column


class Matrix:
    # Different ways to initialize
    def __init__(self, matrix: [[int]]):
        def _check_legal():
            if type(matrix) != list:
                raise AssertionError(f"'{matrix}'' is not an instance of a list.")
            for row in matrix:
                if type(row) not in (list, Row):
                    raise AssertionError(f"'{row}' is not an instance of a list.")
                for entry in row:
                    if type(entry) not in [int, float]:
                        raise AssertionError(f"'{entry}' is not a legal entry.")
            length = len(matrix[0])
            for row in matrix:
                if len(row) != length:
                    raise AssertionError(f"Length of row '{row}' is inconsistent.")

        _check_legal()
        self.matrix = [Row(r) if type(r) != Row else r for r in matrix]

    @classmethod
    def iMatrix(self, length):
        matrix = []
        for i in range(1, 1 + length):
            r = Row([0 for t in range(length)])
            r[i] = 1
            matrix.append(r)
        return Matrix(matrix)

    @classmethod
    def Vector(self, column):
        if type(column) in (list, Column):
            return Matrix([[e] for e in column])

    @classmethod
    def augmentedMatrix(self, matrix, column):
        return matrix.get_concatenateMatrix(Matrix.Vector(column))

    @classmethod
    def byColMatrix(self, cols):
        return Matrix([Row(c) for c in cols]).get_transpose()

    # Some dunnder methods
    def __str__(self):
        text = ''
        for row in self.matrix:
            text += '|'
            for col_num in range(1, self.get_length()[1] + 1):
                maxi = max([len(str(row[col_num])) for row in self.matrix])
                text += eval("'{" + f":^{maxi+2}" + "}'.format(str(int(row[col_num])) if type(row[col_num]) == int else str(float(row[col_num])))")
            text += '|\n'
        return text

    def __repr__(self):
        return 'Matrix([' + ',\n        '.join([repr(row) for row in self.matrix]) + '])'

    def __getitem__(self, row_num):
        if row_num < 1 or row_num > self.get_length()[1]:
            raise IndexError(f"Matrix row out of range.")
        return self.matrix[row_num - 1]

    def __delitem__(self, row_num):
        for i in range(1, self.get_length()[1] + 1):
            del self.matrix[row_num - 1][i]

    def __setitem__(self, i, row):
        self.matrix = [r if num != i else row for r, num in zip(self.matrix, range(1, self.get_length()[0] + 1))]

    def __iter__(self):
        return iter(self.matrix)

    def del_entry(row_num, entry_num):
        del self[row_num][entry_num]

    # Operands/operations
    def __pos__(self):
        return Matrix([row for row in self.matrix])

    def __neg__(self):
        return Matrix([-row for row in self.matrix])

    def __add__(self, right_val):
        if type(right_val) in (int, float):
            return Matrix([row + right_val for row in self.matrix])

        elif type(right_val) in (Matrix,):
            if self.get_length() != right_val.get_length():
                raise AssertionError(f'The length of {right_val} is inconsistent')
            return Matrix([row + right_row for row, right_row in zip(self, right_val)])

    def __radd__(self, left_val):
        return self.__add__(left_val)

    def __sub__(self, right_val):
        return self.__add__(-right_val)

    def __rsub__(self, right_val):
        return - self + right_val

    def __mul__(self, val):
        if type(val) in [int, float]:
            return Matrix([val * row for row in self.matrix])
        elif type(val) == Matrix:
            if self.get_length()[1] != val.get_length[0]:
                raise AssertionError(f"Both matrices have different length.")
            return Matrix([[sum(col * row) for col in [Row(val.get_Col(i)) for i in range(1, val.get_length()[1] + 1)]] for row in self])

    def __pow__(self, val):
        new_matrix = Matrix([r for r in self.matrix])
        return eval('*'.join([repr(Matrix(self.matrix)) for t in range(val)]))

    def dotProduct(self, vector):
        def _check_legal():
            if self.get_length()[1] != 1:
                raise AssertionError(f"'{repr(self)}' is not a vector matrix.")
            if type(vector) != Matrix:
                raise AssertionError(f"'{vector}' is not a Matrix type. ")
            if vector.get_length()[1] != 1:
                raise AssertionError(f"'{repr(vector)}' is not a vector matrix.")
            if vector.get_length() != self.get_length():
                raise AssertionError(f"'{self.get_length()}' and '{vector.get_length()}'are different. ")
        _check_legal()
        n = self.get_transpose()[1] * vector.get_transpose()[1]
        print(n)
        return sum(n)

    # iters
    def iter_rows(self):
        return iter(self.matrix)

    def iter_cols(self):
        return iter([self.get_Col(n) for n in range(1, 1 + self.get_length()[1])])

    # Mutators
    def addRow(self, *rows):
        for r in rows:
            if len(r) != self.get_length()[1]:
                raise AssertionError(f'The row {r} has an inconsistent length. ')
            self.matrix.append(r if type(r) == Row else Row(r))

    def addCol(self, *cols):
        n = self.get_addCol(*cols)
        self.matrix = n.matrix

    def concatenateMatrix(self, matrix):
        n = self.get_concatenateMatrix(matrix)
        self.matrix = n.matrix

    def removeRow(self, row_num):
        n = self.get_removeRow(row_num)
        self.matrix = n.matrix

    def removeCol(self, col_num):
        n = self.get_removeCol(col_num)
        self.matrix = n.matrix

    # eRow stands for elementary row operations (mutators)
    def eRow_interch(self, first, second):
        temp = self[second]
        self[second] = self[first]
        self[first] = temp

    def eRow_mul(self, row, val):
        self[row] = self[row] * val

    def eRow_add(self, first, second):
        self[second] = self[first] + self[second]

    # Special getters
    def get_addRow(self, *rows):
        t = self.matrix[:]
        for r in rows:
            if len(r) != self.get_length()[1]:
                raise AssertionError(f'The row {r} has an inconsistent length. ')
            t.append(r if type(r) == Row else Row(r))
        return Matrix(t)

    def get_addCol(self, *cols):
        new = [c for c in self.get_transpose()]
        for c in cols:
            if len(c) != self.get_length()[0]:
                raise AssertionError(f'The col {c} has an inconsistent length. ')
            new.append(c)
        return Matrix(new).get_transpose()

    def get_concatenateMatrix(self, matrix):
        if self.get_length()[0] != matrix.get_length()[0]:
            raise AssertionError(f'The number of columns is inconsistent.')
        return Matrix(self.get_transpose().matrix + matrix.get_transpose().matrix).get_transpose()

    def get_removeRow(self, row_num):
        t = self.matrix[:]
        del t[row_num - 1]
        return Matrix(t)

    def get_removeCol(self, col_num):
        r_matrix = self.get_transpose().matrix
        del r_matrix[col_num - 1]
        return Matrix(r_matrix).get_transpose()

    def get_eRow_interch(self, first, second):
        copy = self.get_copy()
        copy.eRow_interch(first, second)
        return copy

    def get_eRow_mul(self, row, val):
        copy = self.get_copy()
        copy.eRow_mul(row, val)
        return copy

    def get_eRow_add(self, first, second):
        copy = self.get_copy()
        copy.eRow_add(first, second)
        return copy

    # Getters
    def get_length(self):
        # rows, cols
        return [len(self.matrix), len(self.matrix[0])]

    def get_Col(self, col_num):
        if self.get_length()[1] < col_num or col_num < 1:
            raise IndexError(f"Matrix row out of range.")
        return Column([row[col_num] for row in self.matrix])

    def get_Row(self, row_num):
        return self[row_num]

    def get_transpose(self):
        return Matrix([self.get_Col(num).get_column() for num in range(1, self.get_length()[1] + 1)])

    def get_copy(self):
        return eval(repr(self))

    # some Is's
    def isVector(self):
        return self.get_length[1] == 1

    def isSquare(self):
        return self.get_length[0] == self.get_length[1]

    def isLinearlyIndependent(self):
        '''
    args
        self: it can be an instance of a matrix, or a set of columns.

    return
        a boolean value which determines whether or not this is a linear independent set of vectors/columns.

    description:
    None yet
        '''
        pass

    def isInconsistent(self):
        #
        #
        #
        #
        #
        #
        pass

    def isInvertible(self):
        #
        #
        #
        #
        #

        return self.isSquare() and True


if __name__ == '__main__':
    # tests
    c = Column([1, 2, 3])

    m = Matrix.byColMatrix([c, [e + 1 for e in c], 2 + c])
    print(m)

    pass
