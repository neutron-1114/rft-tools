import numpy as np

# 假设我们有一个二维数组，表示一个简单的图形
# 其中1表示白边，0表示非白边
# 例如：
graph = np.array([
    [0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0]
])

# 给定点的坐标
point = (2, 2)  # 假设点位于(2, 2)，即数组的第3行第3列

# 寻找最近的上下左右四个方向的白边
def find_closest_edges(graph, point):
    rows, cols = graph.shape
    x, y = point
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
    closest_edges = {}

    for direction in directions:
        dx, dy = direction
        distance = 1
        while 0 <= x + dx < rows and 0 <= y + dy < cols and graph[x + dx, y + dy] != 1:
            x, y = x + dx, y + dy
            distance += 1
        if distance != 1:
            closest_edges[direction] = distance

    return closest_edges

# 调用函数并打印结果
closest_edges = find_closest_edges(graph, point)
print("最近的白边距离：", closest_edges)