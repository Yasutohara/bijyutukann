import sys
import csv
import time
import numpy as np
from itertools import product
from mip import *

start_time = time.time() # 開始時間

# model
md = Model(name="Kakkuro_MIP")
md.verbose = 0 # 最適化状況を表示しない
basename = sys.argv[1]
with open(basename+'.csv') as inp_f:
  reader = csv.reader(inp_f)
  data = [row for row in reader]

sizes = data.pop(0)
rows = int(sizes[1]) # 行数
cols = int(sizes[0]) # 列数



#ランダムに
for i in range(rows):
    for j in range(cols):
     if not data[i][j]:
        if np.random.randint(1,3) == 1:
            data[i][j] = 'w'

print(data)


# 変数
x = [[md.add_var('x_{}_{}'.format(i,j), var_type='B') for j in range(cols)] for i in range(rows)]

#数字があるマスの数字と縦横の照明の数が等しい
for i in range(rows):
    for j in range(cols):
        if 'x' in data[i][j]:
            pass
        elif 'w' in data[i][j]:
            pass
        elif not data[i][j]:
            pass
        else:
            md += xsum(x[i + dy][j + dx] for dy, dx in [(0, -1), (1, 0), (0, 1), (-1, 0)]if 0 <= i + dy < rows and 0 <= j + dx < cols and not data[i + dy][j + dx]) == int(data[i][j])

#上下あるいは左右に連続している白マス中には，2つ以上の照明があってはならない
for i in range(rows):
    for j in range(cols):
        group_x = []
        if data[i][j]:
            x_count = 0
            while j - x_count - 1 >= 0 and not data[i][j - x_count - 1]:
                x_count += 1
                group_x.append((i, j - x_count))
            if x_count > 0:
                md += xsum(x[dy][dx] for dy, dx in group_x) <= 1
        elif j + 1 == cols:
            x_count = 0
            group_x.append((i, j))
            while j - x_count - 1 >= 0 and not data[i][j - x_count - 1]:
                x_count += 1
                group_x.append((i, j - x_count))
            md += xsum(x[dy][dx] for dy, dx in group_x) <= 1

for j in range(cols):
    for i in range(rows):
        group_y = []
        if data[i][j]:
            y_count = 0
            while i - y_count - 1 >= 0 and not data[i - y_count - 1][j]:
                y_count += 1
                group_y.append((i - y_count, j))
            if y_count > 0:
                md += xsum(x[dy][dx] for dy, dx in group_y) <= 1
        elif i + 1 == rows:
            y_count = 0
            group_y.append((i, j))
            while i - y_count - 1 >= 0 and not data[i - y_count - 1][j]:
                y_count += 1
                group_y.append((i - y_count, j))
            md += xsum(x[dy][dx] for dy, dx in group_y) <= 1

#十字方向の全ての白マスを足した和が１以上
for i in range(rows):
    for j in range(cols):
        if not data[i][j]:
            x_right_count = 0
            x_left_count = 0
            y_up_count = 0
            y_down_count = 0
            boss = [(i, j)]
            while j + x_right_count + 1 < cols and not data[i][j + x_right_count + 1]:
                x_right_count += 1
                boss.append((i, j + x_right_count))
            while j - x_left_count - 1 >= 0 and not data[i][j - x_left_count - 1]:
                x_left_count += 1
                boss.append((i, j - x_left_count))
            while i + y_down_count + 1 < rows and not data[i + y_down_count + 1][j]:
                y_down_count += 1
                boss.append((i + y_down_count, j))
            while i - y_up_count - 1 >= 0 and not data[i - y_up_count - 1][j]:
                y_up_count += 1
                boss.append((i - y_up_count, j))
            md += xsum(x[dy][dx] for dy, dx in boss) >= 1

# 最適化
md.objective = minimize(xsum(x[i][j] for j in range(cols) for i in range(rows)))
# 求解
status = md.optimize()

for i, j in product(range(rows),range(cols)):
    print(x[i][j].x)
for i, j in product(range(rows),range(cols)):
    if x[i][j].x > 0:
        data[i][j] = 'o'

print(data)

for i, j in product(range(rows),range(cols)):
    suji = 0
    if data[i][j] == 'w':
        suji = sum(x[i + dy][j + dx].x for dy, dx in [(0, -1), (1, 0), (0, 1), (-1, 0)]if 0 <= i + dy < rows and 0 <= j + dx < cols and data[i + dy][j + dx] == 'o')
        if suji > 0:
            data[i][j] = int(suji)

    if data[i][j] == 'o':
        data[i][j] = ""
    if data[i][j] == 'w':
        if np.random.randint(1,7) == 1:
            data[i][j]="0"
        else:
           data[i][j]=""



data.insert(0, sizes)

with open('ka-bi'+'_sol.csv', 'w') as out_f:
  writer = csv.writer(out_f)
  writer.writerows(data)

elapsed_time = time.time() - start_time

print("Running time: {0}".format(elapsed_time)+" [sec]")
