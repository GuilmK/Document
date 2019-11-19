# 创建一个简单的神经网络python代码
# 项目开始时间：2018年10月12日14:52
# 第一阶段完成时间：2018年10月12日16:52 （代码的初步建立，内容的理解）
# 第一阶段测试完成时间：2018年10月17日17:21 （测试完成，程序可以正常运行）
"""
基础准备知识：
numpy.array(object, dtype=None, copy=True, order=None, subok=False, ndmin=0)
作用：创建一个array
参数：
object：array_like：
一个数组，任何物体露出阵列接口，一个对象，其__array__方法返回一个数组，或任何（嵌套）序列。

dtype：data-type
可选，所需的数据类型为阵列。
如果没有给出，则类型将被确定为持有的序列中的对象所要求的最低的类型。
这种说法只能用来“向上转型”的阵列。对于向下转换，使用.astype（t）的方法。

copy：BOOL，可选，如果为true（默认值），那么对象被复制。
否则，副本将仅当__array__返回副本，如果obj是一个嵌套序列，或者做出是否需要拷贝，以满足任何其他要求（DTYPE，订单等）。

order：{'C'，'F'，'A'}，
可选，指定数组的顺序。
如果命令是'C'，那么阵列将在C-连续顺序（上次指数变化最快的）。
如果命令是'F'，则返回的数组将是FORTRAN连续顺序（先指数变化最快的）。
如果命令是'A'（默认），然后返回数组可以是任意顺序（无论是C-，Fortran的连续的，甚至是不连续的），除非需要一个副本，在这种情况下，这将是C-连续的。

subok：BOOL，
可选，如果为True，则子类将被传递，通过，否则返回数组将被迫成为一个基类数组（默认）。

ndmin：INT，
可选，指定结果数组应有尺寸的最小数目。的将根据需要来满足这一要求被预先挂起到的形状。

返回：
out：ndarray，满足规定要求的数组对象
"""

import numpy
# S函数所在的模块
import scipy.special
import pandas as pd

class neuralNetwork:
    # 神经网络的初始化
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):

        # 输入各自的输入结点、隐藏结点、输出结点
        self.input_nodes = inputnodes
        self.hidden_nodes = hiddennodes
        self.output_nodes = outputnodes

        # 学习率
        self.learning_rate = learningrate

        # 权重(通过减去0.5保证出现的数字一定在-1~1之间的权重）
        # self.wih = (numpy.random.rand(self.hidden_nodes, self.input_nodes)-0.5)
        # self.who = (numpy.random.rand(self.output_nodes, self.hidden_nodes)-0.5)
        # 上述是以前的权重标准，现在的权重标准为正态分布采样权重；
        # 以正态分布的方式进行采样：以0.0为正态分布的中心，标准方差，numpy数组的大小作为参数得到权重矩阵
        self.wih = numpy.random.normal(0.0, pow(self.hidden_nodes, -0.5), (self.hidden_nodes, self.input_nodes))
        self.who = numpy.random.normal(0.0, pow(self.output_nodes, -0.5), (self.output_nodes, self.hidden_nodes))

        # 神经网络的激活函数
        self.activation_function = lambda x: scipy.special.expit(x)
        pass

    """
    训练神经网络
    训练任务主要分为两个部分：
    1.将输入的样本序列进行计算（和query的计算方法相同）；
    2.将计算的到的输出和真实的数据进行比较，使用其中的差值来指导网络权重的更新
    """
    def training(self, input_list, target_list):
        # 得到输入的数组
        inputs = numpy.array(input_list, ndmin=2).T
        # 目标输出序列（真实的实际数据）
        targets = numpy.array(target_list, ndmin=2).T

        # 以下代码照抄函数query
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        # 输出的误差序列（用于优化隐藏层和输出层之间的权重矩阵）
        output_errors = targets - final_outputs
        # 隐藏层的误差序列（用于优化输入层和隐藏层之间的权重矩阵）
        hidden_errors = numpy.dot(self.who.T, output_errors)

        self.who += self.learning_rate * numpy.dot((output_errors* final_outputs*(1.0-final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.learning_rate * numpy.dot((hidden_errors* hidden_outputs*(1.0-hidden_outputs)), numpy.transpose(inputs))
        pass

    # 计算输出
    def query(self, inputs_list):
        # 数组的大小至少为2，并将数组进行转置
        inputs = numpy.array(inputs_list, ndmin=2).T

        # 将输入数组和输入的权重矩阵进行点积运算，得到隐藏层的输入数组
        hidden_inputs = numpy.dot(self.wih, inputs)

        # 将隐藏层的输入数组进行激活函数的运算，得到隐藏层的输出数组
        hidden_outputs = self.activation_function(hidden_inputs)

        # 隐藏层的输出数组和输出层的权重进行计算，得到输出层的输入数组
        final_inputs = numpy.dot(self.who, hidden_outputs)

        # 将输出层的输入数组进行激活函数的运算，得到输出层的输出数组
        final_outputs = self.activation_function(final_inputs)

        # 返回输出数组，即返回最后的结果
        return final_outputs
        pass


# 设置基础数据
test_input = 784
test_hidden = 100
test_out = 10
learning = 0.3
n = neuralNetwork(test_input, test_hidden, test_out, learning)
# 读取文件的数据
training_data_file = open("data\神经网络1.0\mnist_train_100.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()
for record in training_data_list:
    all_value = record.split(',')
    inputs = (numpy.asfarray(all_value[1:])/255.0*0.99)+0.01
    targets = numpy.zeros(test_out)+0.01
    targets[int(all_value[0])] = 0.99
    n.training(inputs, targets)
pass
"""训练完成（100个数据）"""
# 开始测试数据
test_data_file = open("data\神经网络1.0\mnist_test_10.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()
test_score = 0
for record in test_data_list:
    all_value = record.split(',')
    correct_answer = all_value[0]
    print("correct answer is :" + correct_answer)
    inputs = (numpy.asfarray(all_value[1:])/255.0*0.99)+0.01
    outputs = n.query(inputs)
    answer = numpy.argmax(outputs)
    print("our answer is :" + str(answer))
    if int(correct_answer) == int(answer):
        test_score += 1
    else:
        test_score += 0
        pass
    pass
print("last score is:"+str(test_score/10))
