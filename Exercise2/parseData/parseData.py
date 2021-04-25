import os
import matplotlib.pyplot as plt 

# 解决作图中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

humidity = [[] for i in range(2)]
temperature = [[] for i in range(2)]
x = [[] for i in range(2)]
file_content = []
with open('data.txt', 'r') as f:
    file_content = f.readlines()
# print(file_content)
for eachline in file_content:
    LoraId = eachline[3:4]
    if LoraId == '1' :
        with open('1.txt', 'a+') as f1:
            f1.write(eachline)
        humidity[0].append(int(eachline.split(':')[2].split('%')[0]))
        temperature[0].append(float(eachline.split(':')[3].split('C')[0]))
    if LoraId == '2' :
        with open('2.txt', 'a+') as f2:
            f2.write(eachline)
        humidity[1].append(int(eachline.split(':')[2].split('%')[0]))
        temperature[1].append(float(eachline.split(':')[3].split('C')[0]))

#画图
for i in range(2):
    x[i] = range(len(humidity[i]))
    plt.figure(figsize=(10, 7))
    line1 = plt.plot(x[i], humidity[i], color='r', label = '湿度{}'.format(i+1))
    line2 = plt.plot(x[i], temperature[i], color='g', label = '温度{}'.format(i+1))
    plt.title("节点{}温湿度曲线".format(i+1))
    plt.xlabel('次数')
    plt.ylabel('湿度或温度')
    plt.xlim(0, len(x[i]))
    # plt.xlim(0, 100)
    plt.ylim(-5, 100)
    plt.legend()  # 显示label
    plt.grid()
    plt.savefig('{}.png'.format(i+1), format='png')
    plt.show()

