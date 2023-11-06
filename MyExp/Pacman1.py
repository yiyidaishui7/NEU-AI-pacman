import tkinter as tk
from tkinter import Canvas, PhotoImage
import time
import queue
import heapq

# 地图（a）的表示
MAP = [
    " WW W WWWWW W WW ",
    "    W   W   W    ",
    "WWW WWW W WWW WWW",
    "WWW W       W WWW",
    "WWW W WW WW W WWW",
    "      WE  W      ",
    "WWW W WWWWW W WWW",
    "WWW W       W WWW",
    "WWW W WWWWW W WWW",
    "        W        ",
    " WW WWW W WWW WW ",
    "  W     W     W  ",
    "W W W WWWWW W W W",
    "    W   W   W   P",
    " WWWWWW W WWWWWW ",
]  # 15行*17列


# 定义地图符号
WALL = 'W'
PACMAN = 'P'
EMPTY = ' '
FOOD = 'E'

# 定义移动方向
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Node:
    def __init__(self, x, y, cost, g_cost, h_cost, parent=None):
        self.x = x  # 行
        self.y = y  # 列
        self.cost = cost  # ucs-cost / greedy-h_cost
        self.g_cost = g_cost  # 从起点到当前节点的实际代价
        self.h_cost = h_cost  # 从当前节点到目标节点的估计代价（启发式）
        self.parent = parent

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        # 用于定义节点之间的比较方式，根据成本排序
        return self.f_cost() < other.f_cost()
        # or self.cost < other.cost


pacman_image = None  # 全局变量，用于保存Pac-Man图片
# wall_image = None
# 创建一个字典来存储图片
image_cache = {}


def load_image(image_path):
    # 检查缓存中是否已存在该图片
    if image_path in image_cache:
        return image_cache[image_path]

    # 如果图片不在缓存中，加载它并存储到缓存中
    image = PhotoImage(file=image_path)
    image_cache[image_path] = image
    return image


def draw_map(canvas, map_data):
    canvas.delete("all")  # 删除画布上的所有元素，以清空之前的绘画
    # 加载 Pac-Man 图像
    global pacman_image, wall_image
    for y, row in enumerate(map_data):  # enumerate可以同时遍历序列和元素
        for x, char in enumerate(row):
            if char == WALL:  # 画墙
                # wall_image = PhotoImage(file="MyExp/images/pinky.png")
                wall_image = load_image("MyExp/images/wall.png")
                canvas.create_image(x * CELL_SIZE, y * CELL_SIZE,
                                    image=wall_image, anchor="nw")
                # canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                #                         (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                #                        fill="BLUE")
            elif char == PACMAN:  # 画吃豆人
                pacman_image = PhotoImage(file="MyExp/images/pacmanR.png")
                canvas.create_image((x+0.2) * CELL_SIZE, (y+0.1)
                                    * CELL_SIZE, image=pacman_image, anchor="nw")

            elif char == FOOD:  # 画豆子
                canvas.create_oval((x + 0.2) * CELL_SIZE, (y + 0.2) * CELL_SIZE,
                                   (x + 0.8) * CELL_SIZE, (y + 0.8) * CELL_SIZE,
                                   fill="white")


# 用DFS搜索目标
def dfs(map_data, start, goal):

    visited = set()  # 用于存储已访问的节点
    stack = [Node(start[0], start[1], 0, 0, 0)]  # 用于DFS的栈

    while stack:
        current_node = stack.pop()  # 弹出栈顶节点
        x, y = current_node.x, current_node.y

        # 如果当前节点是目标节点，构建路径并返回
        if (x, y) == goal:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        # 将当前节点标记为已访问
        visited.add((x, y))

        # 探索邻居节点
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy

            # 检查新节点是否在地图范围内，不是墙，并且未访问过
            if (0 <= new_x < len(map_data) and
                0 <= new_y < len(map_data[0]) and
                map_data[new_x][new_y] != WALL and
                    (new_x, new_y) not in visited):
                # 创建新节点，并将其加入栈中
                new_node = Node(new_x, new_y, 0, 0, 0, parent=current_node)
                stack.append(new_node)

    # 如果没有找到路径，返回空路径
    return []


# 用BFS搜索目标
def bfs(map_data, start, goal):
    # 创建一个队列用于BFS的前沿
    frontier = queue.Queue()
    # 创建起始节点，并将其放入队列中
    start_node = Node(start[0], start[1], 0, 0, 0)
    frontier.put(start_node)
    # 创建一个集合，用于存储已访问过的节点
    visited = set()

    # 开始BFS搜索，直到队列为空
    while not frontier.empty():
        # 从队列中取出当前节点
        current_node = frontier.get()
        x, y = current_node.x, current_node.y

        # 如果是目标节点，返回路径
        if (x, y) == goal:
            path = []
            # 回溯路径，将节点坐标添加到路径中
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            # 返回反转后的路径，即从起点到目标点的最短路径
            return path[::-1]

        # 将当前节点标记为已访问
        visited.add((x, y))

        # 遍历当前节点的所有邻居节点
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            # 检查新节点是否在地图范围内，不是墙，并且未访问过
            if (0 <= new_x < len(map_data) and
                0 <= new_y < len(map_data[0]) and
                map_data[new_x][new_y] != WALL and
                    (new_x, new_y) not in visited):
                # 创建新节点，并将其加入栈中
                new_node = Node(new_x, new_y, 0, 0, 0, parent=current_node)
                frontier.put(new_node)

    # 如果队列为空，表示没有找到路径，返回空路径
    return []


# 用UCS搜索目标
def ucs(map_data, start, goal):
    visited = set()
    priority_queue = []  # 优先队列
    heapq.heappush(priority_queue, Node(start[0], start[1], 0, 0, 0))

    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        x, y = current_node.x, current_node.y

        if (x, y) == goal:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]
        visited.add((x, y))

        for dx, dy in DIRECTIONS:
            new_x, new_y = x+dx, y+dy
            if (0 <= new_x < len(map_data) and
                0 <= new_y < len(map_data[0]) and
                map_data[new_x][new_y] != WALL and
                    (new_x, new_y) not in visited):

                new_cost = current_node.cost + 1  # 此处假设每一步成本都为1
                new_node = Node(new_x, new_y, new_cost,
                                0, 0, parent=current_node)
                heapq.heappush(priority_queue, new_node)
    return []


def heuristic(node, goal):
    # 启发式函数（估计代价）：使用曼哈顿距离
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


# 用Greedy搜索目标
def greedy(map_data, start, goal):
    visited = set()  # 用于存储已访问的节点
    priority_queue = []  # 优先队列，用于Greedy的节点扩展
    heapq.heappush(priority_queue, Node(
        start[0], start[1], heuristic(start, goal), 0, 0))  # 初始节点入队

    while priority_queue:
        current_node = heapq.heappop(priority_queue)  # 弹出h_cost(cost)最低的节点
        x, y = current_node.x, current_node.y

        # 如果当前节点是目标节点，构建路径并返回
        if (x, y) == goal:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        # 将当前节点标记为已访问
        visited.add((x, y))

        # 探索邻居节点
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy

            # 检查新节点是否在地图范围内，不是墙，并且未访问过
            if (0 <= new_x < len(map_data) and
                0 <= new_y < len(map_data[0]) and
                map_data[new_x][new_y] != WALL and
                    (new_x, new_y) not in visited):
                # 创建新节点，并将其加入优先队列
                new_node = Node(new_x, new_y, heuristic(
                    (new_x, new_y), goal), 0, 0, parent=current_node)
                heapq.heappush(priority_queue, new_node)

    # 如果没有找到路径，返回空路径
    return []


# 用A*搜索目标
def astar(map_data, start, goal):
    visited = set()  # 用于存储已访问的节点
    priority_queue = []  # 优先队列，用于A*的节点扩展
    heapq.heappush(priority_queue, Node(
        start[0], start[1], 0, 0, heuristic(start, goal)))  # 初始节点入队

    while priority_queue:
        current_node = heapq.heappop(priority_queue)  # 弹出f_cost最低的节点
        x, y = current_node.x, current_node.y

        # 如果当前节点是目标节点，构建路径并返回
        if (x, y) == goal:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        # 将当前节点标记为已访问
        visited.add((x, y))

        # 探索邻居节点
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy

            # 检查新节点是否在地图范围内，不是墙，并且未访问过
            if (0 <= new_x < len(map_data) and
                0 <= new_y < len(map_data[0]) and
                map_data[new_x][new_y] != WALL and
                    (new_x, new_y) not in visited):
                # 计算新节点的实际代价（g_cost）
                new_g_cost = current_node.g_cost + 1  # 假设每一步的代价都是1，如果有不同的代价，可以根据实际情况调整
                # 创建新节点，并将其加入优先队列
                new_node = Node(new_x, new_y, 0, new_g_cost, heuristic(
                    (new_x, new_y), goal), parent=current_node)
                heapq.heappush(priority_queue, new_node)

    # 如果没有找到路径，返回空路径
    return []


def animate_search(map_data, start, goal, search_algorithm):
    root = tk.Tk()
    root.title(f"{search_algorithm} Search")
    canvas = tk.Canvas(root, width=len(
        map_data[0]) * CELL_SIZE, height=len(map_data) * CELL_SIZE, bg="BLACK")
    canvas.pack()

    draw_map(canvas, map_data)
    path = None

    if search_algorithm == "BFS":
        path = bfs(map_data, start, goal)
    elif search_algorithm == "DFS":
        path = dfs(map_data, start, goal)
    elif search_algorithm == "UCS":
        path = ucs(map_data, start, goal)
    elif search_algorithm == "Greedy":
        path = greedy(map_data, start, goal)
    elif search_algorithm == "A*":
        path = astar(map_data, start, goal)

    if path:
        print(search_algorithm, "length:", len(path)-1,
              "\n", search_algorithm, "path:\n", path)

        for x, y in path:
            # 清除上一步位置的Pac-Man
            if path.index((x, y)) > 0:
                prev_x, prev_y = path[path.index((x, y)) - 1]
                map_data[prev_x] = map_data[prev_x][:prev_y] + \
                    ' ' + map_data[prev_x][prev_y+1:]

        # 绘制新位置的Pac-Man
            map_data[x] = map_data[x][:y] + PACMAN + map_data[x][y+1:]
            draw_map(canvas, map_data)
            root.update()
            time.sleep(0.3)  # Adjust animation speed
    root.mainloop()


if __name__ == "__main__":
    CELL_SIZE = 30

    start = (13, 16)  # x,y
    goal = (5, 7)

    # Choose the search algorithm (DFS, BFS, UCS, Greedy, A*)
    print("请输入你要选择的算法(请输入:DFS, BFS, UCS, Greedy, A*)")
    search_algorithm = input()
    animate_search(MAP, start, goal, search_algorithm)
