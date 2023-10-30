import tkinter as tk
from tkinter import Canvas, PhotoImage
import time

MAP2 = [
"P  ",
"   ",
" E ",
]

# 定义地图符号
WALL = 'W'
PACMAN = 'P'
EMPTY = ' '
FOOD = 'E'

# 定义移动方向
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Node:
    def __init__(self, x, y, cost, parent=None):
        self.x = x
        self.y = y
        self.cost = cost  # ucs-cost / greedy-h_cost
        self.parent = parent

        # 用于定义节点之间的比较方式，根据成本排序
        return self.cost < other.cost
    
pacman_image = None  # 全局变量，用于保存Pac-Man图片