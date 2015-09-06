import numpy

class Graph:
	sz = 0
	grid = numpy.zeros((sz,sz), dtype=numpy.int)
	INF = 1000000007

	def __init__(self, n):
		self.sz = n
		self.grid = numpy.zeros((n, n), dtype=numpy.int)
		self.grid.fill(self.INF)

	def addEdge(self, i, j, dist):
		self.grid[i][j] = dist

	def removeEdge(self, i, j):
		self.grid[i][j] = self.INF

	def FloydWarshall(self):
		size = self.sz
		cost_matrix = numpy.zeros((size, size), dtype=numpy.int)
		path_matrix = numpy.zeros((size, size), dtype=numpy.int)
		cost_matrix.fill(self.INF)
		path_matrix.fill(-1)
		for i in range(size):
			for j in range(size):
				if(self.grid[i][j] != self.INF):
					cost_matrix[i][j] = self.grid[i][j]
					path_matrix[i][j] = i
		for k in range(size):
			for i in range(size):
				for j in range(size):
					if(cost_matrix[i][j] > cost_matrix[i][k] + cost_matrix[k][j]):
						cost_matrix[i][j] = cost_matrix[i][k] + cost_matrix[k][j]
						path_matrix[i][j] = path_matrix[k][j]
		return (cost_matrix, path_matrix)
