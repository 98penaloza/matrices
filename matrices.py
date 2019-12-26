import math


class Row:
    def __init__(self, row):
        self.row = row

    def __pos__(self):
        return Row(self.row)

    def __neg__(self):
        return Row([-entry for entry in self.row])

    def __add__(self, val):
        if type(val) in [int, float]:
            return Row([entry + val for entry in self.row])
        elif type(val) in (Row, list):
            return Row([e1 + e2 for e1, e2 in zip(self, val)])

    def __sub__(self, val):
        return self + -val

    def __rsub__(self, l_val):
        return self - l_val

    def __radd__(self, l_val):
        return self + l_val

    def __mul__(self, val):
        if type(val) in (int, float):
            return Row([val * entry for entry in self.row])
        elif type(val) in [list, Row]:
            return Row([e1 * e2 for e1, e2 in zip(self, val)])

    def __rmul__(self, l_val):
        return self * l_val

    def __truediv__(self, val):
        return Row([entry / val for entry in self.row])

    def __rtruediv__(self, l_val):
        return Row([l_val / entry for entry in self.row])

    def __rmul__(self, l_val):
        return self * l_val

    def __iter__(self):
        return iter(self.row)

    def __getitem__(self, entry_num):
        return (self.row[entry_num - 1])

    def __delitem__(self, entry_num):
        self.row[entry_num - 1] = 0

    def get_row(self):
        return self.row

    def __str__(self):
        return '| ' + ' '.join([str(entry) for entry in self.row]) + ' |'

    def __repr__(self):
        return f"Row({self.row})"

    def __len__(self):
        return len(self.row)

    def __setitem__(self, entry, val):
        self.row[entry - 1] = val


class Matrix:

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

        self.row_tot_num = len(self.matrix)
        self.col_tot_num = len(self.matrix[0])

    @classmethod
    def iMatrix(self, length):
        matrix = []
        for i in range(1, 1 + length):
            r = Row([0 for t in range(length)])
            r[i] = 1
            matrix.append(r)

        return Matrix(matrix)

        pass

    def __str__(self):
        text = ''
        for row in self.matrix:
            text += '|'
            for col_num in range(1, self.col_tot_num + 1):
                maxi = max([len(str(row[col_num])) for row in self.matrix])

                text += eval("'{" + f":^{maxi+2}" + "}'.format(str(int(row[col_num])) if type(row[col_num]) == int else str(float(row[col_num])))")
            text += '|\n'
        return (text)

    def __repr__(self):
        return 'Matrix([' + ',\n        '.join([repr(row) for row in self.matrix]) + '])'

    def __pos__(self):
        return Matrix([row for row in self.matrix])

    def __neg__(self):
        return Matrix([-row for row in self.matrix])

    def __add__(self, right_val):

        if type(right_val) in (int, float):
            return Matrix([row + right_val for row in self.matrix])

        elif type(right_val) in (Matrix,):
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
            if self.col_tot_num != val.row_tot_num:
                raise AssertionError(f"Both matrices have different length.")

            return Matrix([[sum(col * row) for col in [Row(val.get_col_num(i)) for i in range(1, val.col_tot_num + 1)]] for row in self])

            # print(row * col)

            # return Matrix([sum(col * row) for row in val] for col in [Row(self.get_col_num(i)) for i in range(1, self.col_tot_num + 1)])

    def __pow__(self, val):

        new_matrix = Matrix([r for r in self.matrix])
        return eval('*'.join([repr(Matrix(self.matrix)) for t in range(val)]))

    def __getitem__(self, row_num):

        if row_num < 1 or row_num > self.row_tot_num:
            raise IndexError(f"Matrix row out of range.")
        return self.matrix[row_num - 1]

    def __delitem__(self, row_num):
        for i in range(1, self.get_length()[1] + 1):
            del self.matrix[row_num - 1][i]

        # self.matrix[row_num - 1] = [0 for entry in range(self.row_tot_num)]

    def get_length(self):
        return [self.row_tot_num, self.col_tot_num]

    def get_col_num(self, col_num):
        if self.col_tot_num < col_num or col_num < 1:
            raise IndexError(f"Matrix row out of range.")
        return [row[col_num] for row in self.matrix]

    def get_row_num(self, row_num):
        return self[row_num]

    def get_transpose(self):
        return Matrix([self.get_col_num(num) for num in range(1, self.get_length()[1] + 1)])

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

    def __iter__(self):
        return iter(self.matrix)

    def del_entry(row_num, entry_num):
        new_row = self[row_num]
        del new_row[entry_num]
        return Matrix([row if num != row_num else new_row for row, num in zip(self.matrix, range(1, self.row_tot_num + 1))])

        # e stands for elementary row operations

    def e_row_interchange(self, first, second):
        temp = self[second]
        self[second] = self[first]
        self[first] = temp

    def e_row_multiplication(self, row, val):
        new_matrix[row] = self[row] * val
        return new_matrix

    def e_row_addition(self, first, second):

        new_m[second] = self[first] + self[second]
        return new_m

    def __setitem__(self, i, row):
        self.matrix = [r if num != i else row for r, num in zip(self.matrix, range(1, self.get_length()[0] + 1))]


if __name__ == '__main__':

    # tests
    pass
