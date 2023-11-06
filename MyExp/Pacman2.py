import tkinter as tk
import numpy as np
from tkinter import Canvas, PhotoImage
import time

# mapdata
MAP = [
    "   G",
    " W R",
    "P   ",
]

# 定义地图符号
WALL = 'W'
PACMAN = 'P'
EMPTY = ' '
GREEN = 'G'
RED = 'R'


class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent


CELL_SIZE = 150
pacman_image = None  # 全局变量，用于保存Pac-Man图片


def draw_map(canvas, map_data):
    canvas.delete("all")  # 删除画布上的所有元素，以清空之前的绘画
    # 加载 Pac-Man 图像
    global pacman_image, wall_image
    for y, row in enumerate(map_data):  # enumerate可以同时遍历序列和元素
        for x, char in enumerate(row):
            if char == WALL:  # 画墙
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                        fill="GRAY", outline="")
            elif char == PACMAN:  # 画吃豆人
                pacman_image = PhotoImage(file="MyExp/images/pacmanR2.png")
                canvas.create_image((x + 0.1) * CELL_SIZE, (y + 0.1)
                                    * CELL_SIZE, image=pacman_image, anchor="nw")

            elif char == GREEN:  #
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                        fill="GREEN", outline="")
            elif char == RED:  #
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                        fill="RED", outline="")


# 定义参数
discount = 0.9  # 折扣因子
noise = 0.2  # 噪声

# 初始化值函数
num_rows = len(MAP)
num_cols = len(MAP[0])
new_value_function = np.zeros((num_rows, num_cols))
for x in range(num_cols):
    for y in range(num_rows):
        if MAP[y][x] == GREEN:
            new_value_function[y][x] = 1
        elif MAP[y][x] == RED:
            new_value_function[y][x] = -1

# 定义移动方向
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ACTIONS = ["up", "down", "left", "right"]


def value_interations(max, map_data):
    # 迭代值函数
    text_list = []
    while (max > 0):
        max -= 1
        value_function = new_value_function.copy()  # 深拷贝
        # print(new_value_function)
        # print(value_function)
        for y in range(4):
            for x in range(3):
                if MAP[x][y] == WALL:
                    continue  # 这些位置没有值或者值不变
                if MAP[x][y] == GREEN:
                    # new_value_function[x][y] = 1
                    continue
                if MAP[x][y] == RED:
                    # new_value_function[x][y] = -1
                    continue
                else:
                    # 创建一个变量 max_value，用来存储当前状态的最大值，初始化为负无穷大。
                    max_value = float("-inf")
                    for action in ACTIONS:
                        # 初始化一个变量 value 用于计算当前状态的新值。
                        value = 0
                        if action == "up":
                            if (x == 0 or (x == 2 and y == 1)):  # 上方墙
                                value += (1-noise) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (1-noise) * (discount *
                                                      value_function[x-1][y])

                            if (y == 0 or (x == 1 and y == 2)):  # 左边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x][y-1])

                            if (y == 3 or (x == 1 and y == 0)):  # 右边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x][y+1])

                            if value > max_value:
                                max_value = value
                        if action == "down":
                            if (x == 2 or (x == 0 and y == 1)):  # 下方墙
                                value += (1-noise) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (1-noise) * (discount *
                                                      value_function[x+1][y])

                            if (y == 0 or (x == 1 and y == 2)):  # 右边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x][y-1])

                            if (y == 3 or (x == 1 and y == 0)):  # 左边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x][y+1])
                            if value > max_value:
                                max_value = value
                        if action == "left":
                            if (y == 0 or (x == 1 and y == 2)):  # 前方墙
                                value += (1-noise) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (1-noise) * (discount *
                                                      value_function[x][y-1])

                            if (x == 2 or (x == 0 and y == 1)):  # 左边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x+1][y])

                            if (x == 0 or (x == 2 and y == 1)):  # 右边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x-1][y])
                            if value > max_value:
                                max_value = value
                        if action == "right":
                            if (y == 3 or (x == 1 and y == 0)):  # 前方墙
                                value += (1-noise) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (1-noise) * (discount *
                                                      value_function[x][y+1])

                            if (x == 2 or (x == 0 and y == 1)):  # 右边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x+1][y])

                            if (x == 0 or (x == 2 and y == 1)):  # 左边墙
                                value += (noise/2) * \
                                    (discount*value_function[x][y])
                            else:
                                value += (noise/2) * (discount *
                                                      value_function[x-1][y])
                            if value > max_value:
                                max_value = value
                    # print(max_value)
                    new_value_function[x][y] = round(max_value, 2)
                    # print(value_function)

        # 遍历数组并在Canvas上绘制文本
        print(new_value_function)
        for row_idx, row in enumerate(new_value_function):
            for col_idx, value in enumerate(row):
                x1 = col_idx * CELL_SIZE
                y1 = row_idx * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill="")
                text_list.append(canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, text=str(value), font=("黑体", 30)))

        # for row in value_function:
        #     print(" ".join([f"{v:.2f}" for v in row]))
        root.update()
        time.sleep(0.1)
        if (max > 0):
            for text in text_list:
                canvas.delete(text)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("value_interations值迭代")
    canvas = tk.Canvas(root, width=len(
        MAP[0]) * CELL_SIZE, height=len(MAP) * CELL_SIZE, bg="WHITE")
    canvas.pack()
    draw_map(canvas, MAP)  # 画图

    value_interations(12, MAP)  # 可以用 3，9，11，100测试

    root.mainloop()
