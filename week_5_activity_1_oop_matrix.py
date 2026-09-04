
class Matrix:
    """A class representing a 2D matrix supporting matrix operations."""

    def __init__(self, data: list[list[float | int]]):
        """Initializes the matrix and validates the input structure."""
        if not data or not isinstance(data, list):
            raise ValueError("Matrix data must be a non-empty 2D list.")

        self.rows = len(data)
        self.cols = len(data[0])

        # Validate that all rows have the same number of columns
        for row in data:
            if not isinstance(row, list) or len(row) != self.cols:
                raise ValueError("All rows in the matrix must have equal length.")

        self.data = data

    def __repr__(self) -> str:
        """Returns a nicely formatted string representation of the matrix."""
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """Overloads the `@` operator to support direct multiplication: m1 @ m2."""
        return self.multiply(other)

    def multiply(self, other: "Matrix") -> "Matrix":
        """Multiplies two matrices (self * other) using the standard matrix multiplication algorithm."""
        if not isinstance(other, Matrix):
            raise TypeError("Multiplication requires another Matrix instance.")

        # Check dimension compatibility: cols of first matrix must equal rows of second matrix
        if self.cols != other.rows:
            raise ValueError(
                f"Cannot multiply matrices! Matrix A columns ({self.cols}) "
                f"must equal Matrix B rows ({other.rows})."
            )

        # Initialize the result matrix with zeros (dimension: self.rows x other.cols)
        result_data = [[0 for _ in range(other.cols)] for _ in range(self.rows)]

        # Perform row-by-column multiplication
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result_data[i][j] += self.data[i][k] * other.data[k][j]

        return Matrix(result_data)


# ==========================================
# Test Execution (Testing 3*5 and 5*2 Matrix Multiplication)
# ==========================================
if __name__ == "__main__":
    print("--- Matrix Multiplication OOP Assignment Test ---\n")

    # Define a 3x5 matrix (M1)
    m1_data = [
        [1, 2, 3, 4, 5],
        [2, 0, 1, 3, 1],
        [0, 1, 2, 1, 4],
    ]

    # Define a 5x2 matrix (M2)
    m2_data = [
        [1, 2],
        [3, 4],
        [0, 1],
        [2, 0],
        [1, 3],
    ]

    # Instantiate Matrix objects
    m1 = Matrix(m1_data)
    m2 = Matrix(m2_data)

    print(f"Matrix M1 ({m1.rows}x{m1.cols}):")
    print(m1)
    print(f"\nMatrix M2 ({m2.rows}x{m2.cols}):")
    print(m2)

    print("\n----------------------------------")

    # Perform matrix multiplication using the multiply method
    result_matrix = m1.multiply(m2)

    print(
        f"Resulting Matrix M1 * M2 ({result_matrix.rows}x{result_matrix.cols}):"
    )
    print(result_matrix)