from graph import Graph

g = Graph(4)

g.addEdge(0, 0, 0)
g.addEdge(1, 1, 0)
g.addEdge(2, 2, 0)
g.addEdge(3, 3, 0)
g.addEdge(0, 1, 5)
g.addEdge(0, 3, 10)
g.addEdge(1, 2, 3)
g.addEdge(2, 3, 1)

(cost_matrix, path_matrix) = g.FloydWarshall()
print cost_matrix