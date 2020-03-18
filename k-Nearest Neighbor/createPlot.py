from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

n = 1000  # number of points to create
x_cord1 = []
y_cord1 = []
x_cord2 = []
y_cord2 = []
x_cord3 = []
y_cord3 = []
markers = []
colors = []
fw = open('testSet.txt', 'w')
for i in range(n):
    [r0, r1] = random.standard_normal(2)
    myClass = random.uniform(0, 1)
    if myClass <= 0.16:
        f_Flier = random.uniform(22000, 60000)
        tats = 3 + 1.6 * r1
        markers.append(20)
        colors.append(2.1)
        classLabel = 1  # 'didntLike'
        x_cord1.append(f_Flier)
        y_cord1.append(tats)
    elif (myClass > 0.16) and (myClass <= 0.33):
        f_Flier = 6000 * r0 + 70000
        tats = 10 + 3 * r1 + 2 * r0
        markers.append(20)
        colors.append(1.1)
        classLabel = 1  # 'didntLike'
        if tats < 0:
            tats = 0
        if f_Flier < 0:
            f_Flier = 0
        x_cord1.append(f_Flier)
        y_cord1.append(tats)
    elif (myClass > 0.33) and (myClass <= 0.66):
        f_Flier = 5000 * r0 + 10000
        tats = 3 + 2.8 * r1
        markers.append(30)
        colors.append(1.1)
        classLabel = 2  # 'smallDoses'
        if tats < 0:
            tats = 0
        if f_Flier < 0:
            f_Flier = 0
        x_cord2.append(f_Flier)
        y_cord2.append(tats)
    else:
        f_Flier = 10000 * r0 + 35000
        tats = 10 + 2.0 * r1
        markers.append(50)
        colors.append(0.1)
        classLabel = 3  # 'largeDoses'
        if tats < 0:
            tats = 0
        if f_Flier < 0:
            f_Flier = 0
        x_cord3.append(f_Flier)
        y_cord3.append(tats)

fw.close()
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.scatter(x_cord,y_cord, c=colors, s=markers)
type1 = ax.scatter(x_cord1, y_cord1, s=20, c='red')
type2 = ax.scatter(x_cord2, y_cord2, s=30, c='green')
type3 = ax.scatter(x_cord3, y_cord3, s=50, c='blue')
ax.legend([type1, type2, type3], ["Did Not Like", "Liked in Small Doses", "Liked in Large Doses"], loc=2)
ax.axis([-5000, 100000, -2, 25])
plt.xlabel('Frequent Flier Miles Earned Per Year')
plt.ylabel('Percentage of Time Spent Playing Video Games')
plt.show()
