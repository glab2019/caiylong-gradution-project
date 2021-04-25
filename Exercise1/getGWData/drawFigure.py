import os
import numpy as np 
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 因为只有三个文件，所以直接这样定义变量了
# 实际应用中可以通过os库获取文件夹中内容，
# 并可以通过txt的扩展名获取txt文件的列表，直接对列表进行操作
# 同时可以获的txt文件列表的长度length
# 这样的话就可以使用humidity = [[] for i in range(length)]进行定义了
# humidity = [[],[],[]]
# temperature = [[],[],[]]
# file_content = [[],[],[]]
# file_length = 0
# x = [[],[],[]]

# 遍历三次文件，画三张图
# for i in range(3):
#     with open('{}.txt'.format(i+1), 'r') as f:
#         file_content[i] = f.readlines()
#         # print(len(file_content[i]))
#     file_length.append(len(file_content[i]))
#     x[i] = 100
#     # print(x1)
#     for eachline in file_content[i]:
#         humidity[i].append(int(eachline.split('H:')[1].split('%')[0]))
#         # print(int(eachline.split('H:')[1].split('%')[0]))
#         temperature[i].append(float(eachline.split('T:')[1].split('C')[0]))
#         # print(float(eachline.split('T:')[1].split('C')[0]))
#     fig[i] = plt.figure(figsize=(10, 7))
#     line1 = plt.plot(x[i], humidity[i], color='r', label = '湿度{}'.format(i+1))
#     line2 = plt.plot(x[i], temperature[i], color='g', label = '温度{}'.format(i+1))
#     plt.title("节点{}温湿度曲线".format(i+1))
#     plt.xlabel('次数')
#     plt.ylabel('湿度或温度')
#     plt.xlim(0, file_length[i])
#     # plt.xlim(0, 100)
#     plt.ylim(-5, 100)
#     plt.legend()  # 显示label
#     plt.grid()
#     # plt.savefig('{}.png'.format(i+1), format='png')
#     plt.show()
humidity = []
temperature = []
file_content = []
file_length = 0
x = []
length = 0
fig = plt.figure(figsize=(10,7))
plt.ion()
while 1:
    fig.clf()
    with open('1.txt', 'r') as f:
        file_content = f.readlines()
        # print(len(file_content[i]))
    # file_length = len(file_content)
    # print(x1)
    for eachline in file_content:
        humidity.append(int(eachline.split('H:')[1].split('%')[0]))
        # print(int(eachline.split('H:')[1].split('%')[0]))
        temperature.append(float(eachline.split('T:')[1].split('C')[0]))
        # print(float(eachline.split('T:')[1].split('C')[0]))
    length += 1
    x = range(len(humidity))
    line1 = plt.plot(x, humidity, color='r', label = '湿度3')
    line2 = plt.plot(x, temperature, color='g', label = '温度3')
    plt.title("节点1温湿度曲线")
    plt.xlabel('次数')
    plt.ylabel('湿度或温度')
    plt.xlim(0, length)
    # plt.xlim(0, 100)
    plt.ylim(-5, 100)
    plt.legend()  # 显示label
    plt.grid()
    # plt.savefig('{}.png'.format(i+1), format='png')
    # humidity = []
    # temperature = []
    plt.pause(3)
    if length == 101:
        break
plt.ioff()
plt.show()