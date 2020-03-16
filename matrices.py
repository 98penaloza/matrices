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
        for i in range( length):
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
        return Matrix([Row(c) for c in cols]).getTranspose()

    # Some dunnder methods
    def __str__(self):
        text = ''
        for row in self.matrix:
            text += '|'
            for col_num in range(self.get_length()[1]):
                maxi = max([len(str(row[col_num])) for row in self.matrix])
                text += eval("'{" + f":^{maxi+2}" + "}'.format(str(int(row[col_num])) if type(row[col_num]) == int else str(float(row[col_num])))")
            text += '|\n'
        return text

    def __repr__(self):
        return 'Matrix([' + ',\n        '.join([repr(row) for row in self.matrix]) + '])'

    def __getitem__(self, row_num):
        if row_num < 0 or row_num == self.get_length()[1]:
            raise IndexError(f"Matrix row out of range.")
        return self.matrix[row_num]

    def __delitem__(self, row_num):
        for i in range( self.get_length()[1] ):
            del self.matrix[row_num ][i]

    def __setitem__(self, i, row):
        self.matrix = [r if num != i else row for r, num in zip(self.matrix, range(self.get_length()[0] ))]

    def __iter__(self):
        return iter(self.matrix)

    def del_entry(self, row_num, entry_num):
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
            if self.get_length()[1] != val.get_length()[0]:
                raise AssertionError(f"Both matrices have different length.")
            return Matrix([[sum(col * row) for col in [Row(val.get_Col(i)) for i in range( val.get_length()[1])]] for row in self])

    def __rmul__(self, r):
        return self * r

    def __pow__(self, val):
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
        n = self.getTranspose()[1] * vector.getTranspose()[1]
        print(n)
        return sum(n)

    def __eq__(self, right):
        if type(right) == Matrix:
            if self.get_length() == right.get_length():
                return not( 0 in [1 if i==j else 0 for i, j in zip(self, right)])
            else:
                return False

    # iters
    def iter_rows(self):
        return iter(self.matrix)

    def iter_cols(self):
        return iter([self.get_Col(n) for n in range( self.get_length()[1])])

    # Mutators
    def reorder(self):
        self.matrix = sorted([r for r in self.matrix], key=lambda row: row.get_pivot_indx() if row.get_pivot_indx() != None else self.get_length()[1] )

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
        new = [c for c in self.getTranspose()]
        for c in cols:
            if len(c) != self.get_length()[0]:
                raise AssertionError(f'The col {c} has an inconsistent length. ')
            new.append(c)
        return Matrix(new).getTranspose()

    def get_concatenateMatrix(self, matrix):
        if self.get_length()[0] != matrix.get_length()[0]:
            raise AssertionError(f'The number of columns is inconsistent.')
        return Matrix(self.getTranspose().matrix + matrix.getTranspose().matrix).getTranspose()

    def get_removeRow(self, row_num):
        t = self.matrix[:]
        del t[row_num]
        return Matrix(t)

    def get_removeCol(self, col_num):
        r_matrix = self.getTranspose().matrix
        del r_matrix[col_num]
        return Matrix(r_matrix).getTranspose()

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

    def getEchelonForm(self, reduced=False):
        temp = self.get_copy()
        i = 0
        while True:
            temp.reorder()
            if i == temp.get_length()[0] :
                break
            j = temp[i].get_pivot_indx()

            if j == None:
                break
            if reduced:

                temp[i] = temp[i].get_unit(j) 

                for row in range( temp.get_length()[0]):
                    if row != i:
                        val = temp[row][j]

                        temp[row] = temp[row] - val * temp[i].get_unit(j) 

            else:
                for row in range(i, temp.get_length()[0]):
                    if row != i:
                        val = temp[row][j]
                        temp[row] = temp[row] - val * temp[i].get_unit(j)
            i += 1
        return temp

    def getInverse(self):
        temp = self.get_copy()
        if self.isSquare():
            temp.concatenateMatrix(Matrix.iMatrix(temp.get_length()[0]))
            temp = temp.getEchelonForm(reduced=True)
            for i in range(temp.get_length()[0]):
                temp.removeCol(0)
            return temp
        else:
            return

    def getTranspose(self):
        return Matrix([self.get_Col(num).get_column() for num in range(self.get_length()[1] )  ])



    def getDeterminant(self):
        if self.get_length() == (1,1):
            return None
        if not self.isSquare():
            return None
        else:
            if self.get_length() == (2,2):
                return self[0][0] * self[1][1] - self[0][1] * self[1][0]
            else:
                return Matrix._sumDet(   [  self[0][i] * Matrix._getNewM(self, (0, i)).getDeterminant() for i in range( len(self[0])  ) ]    )
    
    def _getNewM(m, r_c):
        n = m.get_copy()
        n.removeRow(r_c[0])
        n.removeCol(r_c[1])
        return n

    def _sumDet(l):
        return sum(num if e_o % 2 == 0 else -num  for num, e_o  in zip(l, [n for n in range(len(l))])     )



    # Getters
    def get_length(self):
        # rows, cols
        return (len(self.matrix), len(self.matrix[0]))

    def get_Col(self, col_num):
        if self.get_length()[1] == col_num or col_num < 0:
            raise IndexError(f"Matrix Col out of range.")
        return Column([row[col_num] for row in self.matrix])

    def get_Row(self, row_num):
        return self[row_num]

    

    def get_copy(self):
        return eval(repr(self))

    # some Is's
    def isVector(self):
        return self.get_length()[1] == 1

    def isSquare(self):
        return self.get_length()[0] == self.get_length()[1]

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

        return self.isSquare() and (self.getInverse() * self == self * self.getInverse() == Matrix.iMatrix(self.get_length()[0])) and True


if __name__ == '__main__':

    # tests
    m = Matrix([[2, -2, 4],
                [4, 1, 2],
                [6, 1, 2]])

    n = Matrix([[1, 2, 0, 2, 1],
                [1, 1, 1, 2, 3],
                [0, 0, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 2, 1, 2, 1]])


    print(m.getEchelonForm(reduced =True))
    print(m.getTranspose())
    print(m*m.getInverse())
    
    pass
    # test
    # TODO Add __eq__() method to compare whether two matrices are the same
