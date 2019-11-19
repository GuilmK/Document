import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")  #格式 格子类型是sawtooth 锯齿形 亮度是0.8
leafNode = dict(boxstyle="round4", fc="0.8")       #fc是rnage（0-1） 0黑色 1白色
arrow_args = dict(arrowstyle="<-")  				#箭头标签格式

def plotNode(nodeTxt, centerPt, parentPt, nodeType): #绘制带箭头的注解 节点文字，子节点，父节点，节点类型
	"""
	输入：
	输出：
	描述：绘制一个点
	"""
	createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', \
							xytext=centerPt, textcoords='axes fraction', \
							va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
	#首先这是一句调用createPlot.ax1 该值存放在createPlot()函数中，Python所有变量都是
	#全局变量，可以直接访问，不像java/C一样需要调用函数内变量时通过 
	#bbox表示边框类型 va，ha表示给定坐标是node的中心 而不是左侧或者右侧 xycoords是轴对称
	#createPlot.createPlot.ax1来调用

def getNumLeafs(myTree):
	"""
	输入：决策树
	输出：决策树的叶子数量
	描述：
	"""
	numLeafs = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			numLeafs += getNumLeafs(secondDict[key])  #递归
		else:
			numLeafs += 1
	return numLeafs

def getTreeDepth(myTree):
	"""
	输入：决策树
	输出：树的深度
	描述：
	"""
	maxDepth = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = getTreeDepth(secondDict[key]) + 1
		else:
			thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
	"""
	输入：
	输出：
	描述：
	"""
	xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
	yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
	createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
	"""
	输入：
	输出：
	描述：
	"""
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = list(myTree.keys())[0]
	cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalw, plotTree.yOff)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalw
			plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def createPlot(inTree):
	"""
	输入：决策树
	输出：
	描述：绘制整个决策树
	"""
	fig = plt.figure(1, facecolor='white')  #建立白色绘图区
	fig.clf()		#清除场景 用在绘制之前清除之前留下的图像
	axprops = dict(xticks=[], yticks=[])
	createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  #不用框架
	plotTree.totalw = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	plotTree.xOff = -0.5 / plotTree.totalw
	plotTree.yOff = 1.0
	plotTree(inTree, (0.5, 1.0), '')
	plt.show()