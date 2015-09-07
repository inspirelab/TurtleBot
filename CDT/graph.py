import numpy
import heapq

class Graph:
	sz = 0
	grid = numpy.zeros((sz,sz), dtype=numpy.int)
	INF = 1000000007
	guard = []

	def __init__(self, n):
		self.sz = n
		self.grid = numpy.zeros((n, n), dtype=numpy.int)
		self.grid.fill(self.INF)

	def addEdge(self, i, j, dist):
		self.grid[i][j] = dist
		self.grid[j][i] = dist

	def removeEdge(self, i, j):
		self.grid[i][j] = self.INF
		self.grid[j][i] = self.INF

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

	def GraphReduction(self):
		min = INF
		mini = -1
		minj = -1
		redG = Graph(self.sz)
		vertexList = []
		heapq prq

		guardFlag = numpy.zeros(self.sz, dtype=numpy.bool)
		guardFlag.fill(True)
		guardCount = len(guard)

		for i in range(len(self.guard)):
			for j in range(i+1, len(self.guard)):
				if (min > cost_matrix[i][j])
					min = cost_matrix[i][j]
					mini = i
					minj = j
		AddPathToGraph(mini, minj, redG, vertexList, guardFlag)

		prevsize = 0
		while guardCount != 0:
			for i in range(prevsize, len(vertexList))
				for j in range(len(self.guard)))
					if (guardFlag[guard[j]])
						heappush(prq, (cost_matrix[vertexList[i]][guard[j]],vertexList[i],guard[j]))
			
			prevsize = len(vertexList)
			el = heappop(prq)
			if (guardFlag[el[2]])
				AddPathToGraph(el[1], el[2], redG, vertexList, guardFlag)

	def AddPathToGraph( start, end, gr, vertexList, guardFlag):
		cur1 = pathmatrix[start][end]
		cur2 = end
		while True:
			(guardflag[cur2] = False && guardCount--) if guardFlag[cur2]

			vertexList.append(cur2)
			gr.addEdge(cur1, cur2, cost_matrix[cur1][cur2])
			
			cur2 = cur1
			cur1 = pathmatrix[start][cur2]
			
			if (cur1 != start)
				break;

