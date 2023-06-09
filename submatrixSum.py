def submatrix_sum(matrix, p, q, r, s):
    rows = len(matrix)
    cols = len(matrix[0])

    if p >= r or q >= s:
        return 0, []

    prefixSum = [[0] * cols for _ in range(rows)]
    prefixSum[0][0] = matrix[0][0]
    for i in range(1, rows):
        prefixSum[i][0] = matrix[i][0] + prefixSum[i-1][0]
    for j in range(1, cols):
        prefixSum[0][j] = matrix[0][j] + prefixSum[0][j-1]

    for i in range(1, rows):
        for j in range(1, cols):
            prefixSum[i][j] = matrix[i][j] + prefixSum[i-1][j] + prefixSum[i][j-1] - prefixSum[i-1][j-1]

    submatrixSum = prefixSum[r][s]
    if p > 0:
        submatrixSum -= prefixSum[p-1][s]
    if q > 0:
        submatrixSum -= prefixSum[r][q-1]
    if p > 0 and q > 0:
        submatrixSum += prefixSum[p-1][q-1]

    submatrix = []
    for i in range(p, r+1):
        row = matrix[i][q:s+1]
        submatrix.append(row)

    return submatrixSum, submatrix

matrix = [
    [2, 2, 5, 4, 1],
    [4, 8, 2, 3, 7],
    [6, 3, 4, 6, 2],
    [7, 3, 1, 8, 3],
    [1, 5, 7, 9, 4]
]
p, q = 1, 1
r, s = 2, 3

sum_result, submatrix_result = submatrix_sum(matrix, p, q, r, s)
print("Sum is", sum_result)
print("Submatrix:")
for row in submatrix_result:
    print(row)
