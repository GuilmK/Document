# -*- coding: utf-8 -*-
from numpy import *
from math import sqrt
import matplotlib.pyplot as plt


# 读入文件数据,是一个二元列表的列表
def loadDataSet(fileName):
    dataSet = []
    fr = open(fileName)
    for line in fr.readlines():
        # strip()负责去处无效空白字符
        curLine = line.strip().split(' ')
        # 最后得到的是一个二元列表的列表
        fltLine = list(map(float, curLine))
        dataSet.append(fltLine)
    return dataSet


# 欧氏距离，用来判断聚类程度的好坏
def distEclud(a, b):
    return sqrt(sum(power(a - b, 2)))


# dataSet是数据集，k是需要设置的k个类别
# 随机生成k，输出为行2列
def randCent(dataSet, k):
    n = shape(dataSet)[1]  # n是列数
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j]) # 找到第j列最小值
        # 求第j列最大值与最小值的差
        rangeJ = float(max(dataSet[:, j]) - minJ)
        # 生成k行1列的在(0, 1)之间的随机数矩阵
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    print(centroids)  # 打印k比较算法前后中心值对比关系
    return centroids


def KMeans(dataSet, k, distMeas = distEclud, createCent = randCent):
    m = shape(dataSet)[0]  # 数据集的行数
    # 矩阵clusterAssment为m行2列，该矩阵和dataSet的行数相同，行行对应.
    # 第一列表示与对应行距离最近的质心下标，第二列表示欧式距离的平方。
    clusterAssment = mat(zeros((m, 2)))
    # 初始化随机中心
    centroids = createCent(dataSet, k)
    # 这个布尔值负责控制循环的终止
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m): # 遍历数据集中的每一行数据
            # 初始化最短距离和达到最短距离时对应的k值
            minDist = inf
            minIndex = -1
            for j in range(k):  # 寻找最近质心
                # 计算出来的是一个表示距离的double值,每个值计算j次, 一共计算i*j次
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist: # 更新最小距离和质心下标
                    minDist = distJI; minIndex = j
            # 判断是否修改了minIndex，如果修改了说明还没有达到最优值，需要继续循环
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            # 记录最小距离质心下标，最小距离的平方
            clusterAssment[i, :] = minIndex, minDist**2
        for cent in range(k):  # 更新质心位置
            # 获得距离同一个质心最近的所有点的下标，即同一簇的坐标
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            # 求同一簇的坐标平均值，axis=0表示按列求均值,用于下次更新或者最终结果
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids




if __name__ == "__main__":
    dataSet = mat(loadDataSet('watermelon4.txt'))
    k = 3
    a = KMeans(dataSet, k)
    print(a)