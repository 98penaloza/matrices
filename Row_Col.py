

class Row:
    def __init__(self, row):
        if type(row) not in (list, tuple, Row, Column):
            raise AssertionError(f'{row} is not an instance of a sequancial ordered numbers. \n')
        if False in [type(e) in (int, float) for e in row]:
            raise AssertionError(f'{row} contains a non numerical value. \n')
        self.row = [int(entry) if float(entry) == int(entry) else float(entry) for entry in row]

    def _check_operational(self, val):
        return True if type(val) in (Row, Column, list, tuple) else False

    def _raise_length(self, val):
        if len(self) != len(val):
            raise AssertionError(f'The length of {val} is inconsistent. \n')

    def _raise_index(self, val):
        if type(val) != int:
            raise TypeError(f"Row indices must be integers, not str")

    def __str__(self):
        return '| ' + ' '.join([str(entry) for entry in self.row]) + ' |'

    def __repr__(self):
        return f"{type(self).__name__}({self.row})"

    def __pos__(self):
        return eval(repr(self))

    def __neg__(self):
        return eval(f'{type(self).__name__}(' + str([-entry for entry in self.row]) + ')')

    def __add__(self, val):
        if type(val) in [int, float]:
            return eval(f'{type(self).__name__}(' + str([entry + val for entry in self.row]) + ')')
        elif self._check_operational(val):
            self._raise_length(val)
            return eval(f'{type(self).__name__}(' + str([e1 + e2 for e1, e2 in zip(self, val)]) + ')')

    def __radd__(self, l_val):
        return self + l_val

    def __sub__(self, val):
        return self + -val

    def __rsub__(self, l_val):
        return -self + l_val

    def __mul__(self, val):
        if type(val) in (int, float):
            return eval(f'{type(self).__name__}(' + str([val * entry for entry in self.row]) + ')')
        elif self._check_operational(val):
            self._raise_length(val)
            return eval(f'{type(self).__name__}(' + str([e1 * e2 for e1, e2 in zip(self, val)]) + ')')

    def __rmul__(self, l_val):
        return self * l_val

    def __truediv__(self, val):
        if type(val) in (int, float):
            return eval(f'{type(self).__name__}(' + str([entry / val for entry in self.row]) + ')')
        elif self._check_operational(val):
            self._raise_length(val)
            return eval(f'{type(self).__name__}(' + str([e1 / e2 for e1, e2 in zip(self, val)]) + ')')

    def __rtruediv__(self, l_val):
        if type(val) in (int, float):
            return eval(f'{type(self).__name__}(' + str([l_val / entry for entry in self.row]) + ')')
        elif self._check_operational(l_val):
            self._raise_length(val)
            return eval(f'{type(self).__name__}(' + str([e2 / e1 for e1, e2 in zip(self, val)]) + ')')

    def __iter__(self):
        return iter(self.row)

    def __getitem__(self, entry_num):
        self._raise_index(entry_num)
        return (self.row[entry_num - 1])

    def __delitem__(self, entry_num):
        self.row[entry_num - 1] = 0

    def __len__(self):
        return len(self.row)

    def __setitem__(self, entry, val):
        self.row[entry - 1] = val

    def get_row(self):
        return self.row

    def get_unit(self, entry_num):
        val = self[entry_num]
        return self / val

    def add_entry(self, *entries):
        for e in entries:
            if type(e) not in (int, float):
                raise AssertionError(f'{e} is not an instance of a numerical value. ')
            self.row.append(e)

    def del_entry(self, entry_num):
        del self.row[entry_num - 1]


class Column(Row):
    def __str__(self):
        maxi = max([len(str(e)) for e in self.row])
        return '\n'.join(['|' + eval("'{" + f":^{maxi+2}" + "}'.format( str(e))") + '|' for e in self.row])

    def get_column(self):
        return self.row

    del Row.get_row
