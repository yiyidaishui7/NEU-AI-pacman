# NEU-AI-pacman
东北大学（沈阳） 人工智能导论小实验 Pac-Man CS188

## 1.实验一 (地图a) Pacman1.py
题目：使用深度优先、广度优先、一致代价、贪心和 A*五种搜索 策略搜索目标，并给出最后决策结果路径，动画显示出来
### 操作步骤：
1.运行python文件Pacman1.py
2.键盘键入选择的算法名称：DFS, BFS, UCS, Greedy, A*
### 修改Pac-Man初始位置以及Egg位置：
1.修改地图(pacman1.py line 8)中"P"和"E"所在位置。将原"P"、"E"替换为" ",并且选取新的位置，将" "替换为"P"或"E"
2.修改main函数中start与goal的坐标为新的"P"和"E"所在位置
3.保存修改后运行python文件Pacman1.py

## 2.实验二 (情景2) Pacman2.py
题目：使用值迭代方法计算各个状态值
### 操作步骤：
1.运行python文件Pacman2.py
### 修改迭代次数：
1.修改main函数中(pacman2.py line 207) value_interations(9, MAP) 第一个参数值
2.保存修改后运行python文件Pacman2.py
