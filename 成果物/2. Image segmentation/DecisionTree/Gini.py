# -*- coding: utf-8 -*-
## 参考《机器学习》（Tom M. Mitchell） 第三章 决策树学习
## 《机器学习》（周志华）， 第四章 决策树

from math import log
import operator
import treePlotter

def calcShannonEnt(dataSet):
	"""
	输入：数据集
	输出：数据集的香农熵
	描述：计算给定数据集的香农熵
	"""
	numEntries = len(dataSet)      #统计数据实例个数
	labelCounts = {} 				#字典,一个键值对
	for featVec in dataSet:			#按照行遍历数据集，本质是记录键出现的次数
		currentLabel = featVec[-1] #又定义了一个变量，取得每行最后一个元素
		if currentLabel not in labelCounts.keys():  #如果最后一个元素不是键值
			labelCounts[currentLabel] = 0  #键值对的值为0，即这是第一次出现的键
		labelCounts[currentLabel] += 1		#这是个计数函数
	shannonEnt = 0.0				#初始为0
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries   #后面就是公式了
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt

def splitDataSet(dataSet, axis, value):
	"""
	输入：数据集，选择维度，选择值
	输出：划分数据集  这到底是是个啥！
	描述：按照给定特征划分数据集；去除选择维度中等于选择值的项  #如果等于选择值就是刚好处于分界点的值
	"""
	retDataSet = []  #存储分类完毕的集合
	for featVec in dataSet:
		if featVec[axis] == value: #若第 axis号元素等于初始给定的value值 则记录下来
			reduceFeatVec = featVec[:axis]  #python里第二个参数的实际含义应该是取多少个，实际位置为n - 1，但第一个参数不是
			reduceFeatVec.extend(featVec[axis+1:])  #以上两条语句是把featVec数组中除了特征值的元素给保留下来
													 #[1,0,yes] 若0零特征值 则最后保存的是[1,yes]
			retDataSet.append(reduceFeatVec)    #把剩下的项目放回去，因为树的子树不需要这个特征值了
	return retDataSet

def chooseBestFeatureToSplit(dataSet):
	"""
	输入：数据集
	输出：最好的划分维度
	描述：选择最好的数据集划分维度
	"""
	numFeatures = len(dataSet[0]) - 1		#特征值的数量，减去yes或no(就是列数)
	baseEntropy = calcShannonEnt(dataSet)  #先置最优熵为为划分是数据集的熵
	bestInfoGain = 0.0				#初始化Gain
	bestFeature = -1				# 默认最好的特征为-1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]		#每次循环取第i列所有特征值
		uniqueVals = set(featList)							#set集合中存放的是所有不同的特征值，本例为[0,1,2]
		newEntropy = 0.0
		for value in uniqueVals:  # 进行遍历 调用splitDataSet()进行划分
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))  #划分后在原集合中占的比例
			newEntropy += prob * calcShannonEnt(subDataSet) #比例乘以划分后集合的熵 相加表示两个比例相加为1然后各自乘以各自划分集合的熵 与原数据的熵比较
		infoGain = baseEntropy - newEntropy
		if (infoGain > bestInfoGain):  #与0相比 若大于则表示熵减小了 也就是这种划分方式是有利的
			bestInfoGain = infoGain
			bestFeature = i         #这两行记录最优划分的值和其对应位置
	return bestFeature

def majorityCnt(classList):
	"""
	输入：分类类别列表
	输出：子节点的分类
	描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
		  采用多数判决的方法决定该子节点的分类
	"""
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0  #iteritems是返回当前字典操作后的迭代
		classCount[vote] += 1	  #key是获取itemgetter的第一个域的值并保持 域从0开始 为排序的关键字，reverse默认False是升序 True表示降序
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reversed=True)
	return sortedClassCount[0][0]  #返回的是值最大的那个

def createTree(dataSet, labels):  #最核心的函数
	"""
	输入：数据集，特征标签
	输出：决策树
	描述：递归构建决策树，利用上述的函数
	"""
	classList = [example[-1] for example in dataSet]   #取出双重列表里的最后一列元素，也就是一整列标记的值（Y或者N）
	if classList.count(classList[0]) == len(classList): #如果classlist中的第一个值在classlist中的总数等于长度，也就是classlist中所有值都一样
		# 类别完全相同，停止划分
		return classList[0]
	if len(dataSet[0]) == 1:   #说明属性栏中目前只有一项属性，又由于上一个IF没有执行故属性还不相同
		# 遍历完所有特征时返回出现次数最多的
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)  #最优的特征 先划分出判断节点
	bestFeatLabel = labels[bestFeat]  #最优特征对应的标签
	myTree = {bestFeatLabel:{}}		#把标签存在树中 这时候树是用循环字典来保存的
	del(labels[bestFeat])			#在标签中删除已经选择过的标签
	# 得到列表包括节点所有的属性值
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]  #去掉已经删除过的标签后的标签集合
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels) #循环字典的值，这里是根据最优特征划分出来的集合，然后把该集合放入树中
	return myTree

def classify(inputTree, featLabels, testVec):
	"""
	输入：决策树，分类标签，测试数据
	输出：决策结果
	描述：跑决策树
	"""
	firstStr = list(inputTree.keys())[0]		#得到决策树第一个分类标签
	secondDict = inputTree[firstStr]			#得到第一个标签对应的第二个目录？
	featIndex = featLabels.index(firstStr)		#得到在分类标签中决策树第一个标签的位置
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':  #要么继续区分
				classLabel = classify(secondDict[key], featLabels, testVec)  #这里是一个递归
			else:
				classLabel = secondDict[key]  #要么不是一个目录，说明到叶子节点了，得到分类标签
	return classLabel

def classifyAll(inputTree, featLabels, testDataSet):
	"""
	输入：决策树，分类标签，测试数据集
	输出：决策结果
	描述：跑决策树
	"""
	classLabelAll = []
	for testVec in testDataSet:  #循环遍历测试数据集
		classLabelAll.append(classify(inputTree, featLabels, testVec)) #循环测试完每个数据集
	return classLabelAll			#返回测试结果


def createDataSet():
	"""
	outlook->  0: sunny | 1: overcast | 2: rain
	temperature-> 0: hot | 1: mild | 2: cool
	humidity-> 0: high | 1: normal
	windy-> 0: false | 1: true 
	"""
	dataSet = [[0, 0, 0, 0, 'N'], 
			   [0, 0, 0, 1, 'N'], 
			   [1, 0, 0, 0, 'Y'], 
			   [2, 1, 0, 0, 'Y'], 
			   [2, 2, 1, 0, 'Y'], 
			   [2, 2, 1, 1, 'N'], 
			   [1, 2, 1, 1, 'Y']]
	labels = ['outlook', 'temperature', 'humidity', 'windy']
	return dataSet, labels

def createTestSet():
	"""
	outlook->  0: sunny | 1: overcast | 2: rain
	temperature-> 0: hot | 1: mild | 2: cool
	humidity-> 0: high | 1: normal
	windy-> 0: false | 1: true 
	"""
	testSet = [[0, 1, 0, 0], 
			   [0, 2, 1, 0], 
			   [2, 1, 1, 0], 
			   [0, 1, 1, 1], 
			   [1, 1, 0, 1], 
			   [1, 0, 1, 0], 
			   [2, 1, 0, 1]]
	return testSet

def main():
	dataSet, labels = createDataSet()   #函数返回了两个参数
	labels_tmp = labels[:] # 拷贝，createTree会改变labels
	desicionTree = createTree(dataSet, labels_tmp)
	print('desicionTree:\n', desicionTree)
	treePlotter.createPlot(desicionTree)
	testSet = createTestSet()
	print('classifyResult:\n', classifyAll(desicionTree, labels, testSet))

if __name__ == '__main__':   #如果是通过命令行启动，则直接启动
	main()