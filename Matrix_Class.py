import random
from copy import deepcopy


class Matrix:
    def __init__(self, td_arr):

        for row in td_arr:
            for col in row:
                if not isinstance(col, (int, float)):
                    raise Exception("Array should contain only numeric items!!!")

        tuple_of_len = tuple(map(lambda x: len(x), td_arr))
        if not all(elem == tuple_of_len[0] for elem in tuple_of_len):
            raise Exception("Rows should have the same length in array!!!")

        self.td_arr = td_arr
        self.num_of_row = len(td_arr)
        self.num_of_col = len(td_arr[0])

    def add(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise Exception("Matrix instance is expected")
        if self.num_of_row != other_matrix.num_of_row:
            raise Exception("Matrices should have the same number of rows")
        if self.num_of_col != other_matrix.num_of_col:
            raise Exception("Matrices should have the same number of columns")
        new_list = []
        for item in range(self.num_of_row):
            new_list.append([(item1[0] + item1[1]) for item1 in zip(other_matrix.td_arr[item], self.td_arr[item])])
        output = Matrix(new_list)
        return output

    def sub(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise Exception("Matrix instance is expected")
        if self.num_of_row != other_matrix.num_of_row:
            raise Exception("Matrices should have the same number of rows")
        if self.num_of_col != other_matrix.num_of_col:
            raise Exception("Matrices should have the same number of columns")
        new_list = []
        for item in range(self.num_of_row):
            new_list.append([(item1[1] - item1[0]) for item1 in zip(other_matrix.td_arr[item], self.td_arr[item])])
        output = Matrix(new_list)
        return output

    def mul(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise Exception("Matrix instance is expected")
        if self.num_of_col != other_matrix.num_of_row:
            raise Exception("Matrix should have the same number of rows as current matrix columns")
        new_list = []
        for item in self.td_arr:
            new_list.append([sum(item2[0]*item2[1] for item2 in zip(item, item1)) for item1 in zip(*other_matrix.td_arr)])
        output = Matrix(new_list)
        return output

    def str(self):
        for item in range(self.num_of_row):
            nums = " ".join([f"{str(item1):^5}" for item1 in self.td_arr[item]])
            if item == 0:
                print(f"⌈ {nums:^17} ⌉")
            elif item == self.num_of_row - 1:
                print(f"⌊ {nums:^17} ⌋")
            else:
                print(f"| {nums:^17} |")

    def same_dim_with(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise Exception("Matrix instance is expected")
        if self.num_of_row == other_matrix.num_of_row and self.num_of_col == other_matrix.num_of_col:
            return True
        return False

    def is_square(self):
        if self.num_of_row == self.num_of_col:
            return True
        return False

    @staticmethod
    def random_matrix(row, col, low=0, high=10):
        output = Matrix([[random.randint(low, high) for item1 in range(col)] for item in range(row)])
        return output

    def determinant(self, answer=0):
        if not self.is_square():
            raise Exception("Determinant is counted only for square matrices")
        if self.num_of_row == 1:
            return self.td_arr[0][0]
        for item in range(self.num_of_row):
            if item % 2 == 0:
                t = 1
            else:
                t = -1
            r = Matrix([item1[:item] + item1[item + 1:] for item1 in self.td_arr[1:]])
            answer += t * self.td_arr[0][item] * r.determinant()
        return answer

    @staticmethod
    def idt_mtx(row, col):
        new_list = Matrix([[1 if i == j else 0 for j in range(col)] for i in range(row)])
        return new_list

    def non_zero(self, row, col):
        for item in range(row, self.num_of_row):
            if self.td_arr[item][col] != 0:
                return item

    def inverse(self):
        if not self.is_square():
            raise Exception("Inverse is counted only for square matrices")
        if self.determinant() == 0:
            raise Exception("Inverse does not exist")
        mtx_new = deepcopy(self)
        num_of_rows = mtx_new.num_of_row
        num_of_cols = mtx_new.num_of_col
        id_m = Matrix.idt_mtx(num_of_rows, num_of_cols)
        for item in range(0, num_of_rows):
            mtx_new.td_arr[item] += id_m.td_arr[item]
        i = 0
        for j in range(0, num_of_cols):
            f_non0 = mtx_new.non_zero(i, j)
            if f_non0 != i:
                mtx_new.td_arr[f_non0], mtx_new.td_arr[i] = mtx_new.td_arr[i], mtx_new.td_arr[f_non0]
            mtx_new.td_arr[i] = [k / mtx_new.td_arr[i][j] for k in mtx_new.td_arr[i]]
            for q in range(0, num_of_rows):
                if q != i:
                    sc = [mtx_new.td_arr[q][j] * m for m in mtx_new.td_arr[i]]
                    mtx_new.td_arr[q] = [(mtx_new.td_arr[q][t] - sc[t]) for t in range(0, len(sc))]
            if i == num_of_rows or j == num_of_cols:
                break
            i += 1

        for idx in range(0, num_of_rows):
            mtx_new.td_arr[idx] = mtx_new.td_arr[idx][num_of_cols:]
        return mtx_new