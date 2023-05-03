import math

import matplotlib.pyplot as plt
import numpy as np

f = open('data.txt', 'r')
text = f.readlines()

node_x = []
node_y = []

for i in range(len(text)-1):
    line = text[i+1]
    strs = line.split()
    x = math.floor(eval(strs[1]))
    y = math.floor(eval(strs[2]))
    node_x.append(x)
    node_y.append(y)



pic_x = np.array(node_x)
pic_y = np.array(node_y)

plt.figure(figsize=(8,8))
plt.scatter(pic_x, pic_y)
plt.show()