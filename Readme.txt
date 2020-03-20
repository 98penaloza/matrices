### READ ME ###
###  IN PROGRESS  ###

My repo/project matrix is a tool for people working (especially) with matrices and linear algebra.
It is a LEARNING/TEACHING tool but, by not means, I intent to substitute linear algebra introdutory courses,
nor I plan to provide a "cheating tool". Instead I'm trying to develop a tool that can be used along the
knowledge acquered from linear algebra courses.

###
CLASSES and METHODS (OUTDATED)
###
    Row
            A sequence of numerical values read from left to right. Its index start counting from 1 and it includes
        the last index number.

        __init__
            A row is initialized as followed Row([...]). Row forcefully has to be initialized with an instance of
        a sequence of ordered numerical values such as list, tuple (even Row or Column). and the values in such data structure
        have to be numerical values.

        dunder operators( __add__, __sub__, __mul__, __truediv__, __radd__, ...)
            A row can be added, substracted, etc... with numerical values or ordered sequences of numerical values
        with the same length. In the firts case, it returns a new instance of a Row and each element is addded, substracted, etc...
        In the second case, a new instance of a Row is returned in which every element of each data structured is added, substracted, etc...

        dunder methods (__iter__, __getitem__, __setitem__, __delitem__)
            - When __iter__ is called, it returns a generator that yields a value in the instance object Row.
            - When __getitem__ is called, it returns the entry position of the Row (index starts at 1, and includes the last index)
            - When __setitem__ is called it mutates the entry number given for any value given
            - __delitem__ will mutate any entry num so the numerical value becomes 0

        get_row
            Returns the sequence of numerical values as a list

        get_unit
            args
                entry_num: an entry index from which the Row will be divided such that that entry val becomes 1.
            return
                a instance of Row, such that every value in the row is divided by the value in the entry index given
            ex:
                Row([1,0,2,6]).get_unit(3) --> Row([.5, 0, 1, 3])

        add_entry
            args
                *entries: any number of numerical values which are added to an existing instance of a Row

        del_entry
            args
                entry_num: deletes the entry given by its index or entry_num



    Column
            A sequence of numerical values read from top to bottom. Its index start counting from 1 and it includes
        the last index number. Since Columns and Rows behave similar, I created Column from base class Row.
        It does not contains method get_row(), but instead it contains method get_column()



    Matrix
        #
        #
        #
        #
        #
        #
        #
        #











