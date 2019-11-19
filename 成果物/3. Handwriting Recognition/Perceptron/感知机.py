import numpy
import scipy.special

class perceptron:
    # 初始化函数
    def __init__(self, inputnodes, outputnodes, learningrate):
        # 内容的初始化
        self.input_nodes = inputnodes
        self.output_nodes = outputnodes
        # 学习率
        self.learning_rate = learningrate
        # 权重,制作一个大小为输入结点*输出结点的权重大小矩阵
        self.wio = numpy.random.normal(0.0, pow(self.output_nodes, -0.5), (self.output_nodes, self.input_nodes))
        # 激活函数 y = 1/(1+exp(x))
        self.activation_function = lambda x: scipy.special.expit(x)
        pass

    # 训练函数
    def training(self, inputlist, outputlist):
        inputs = numpy.array(inputlist, ndmin=2).T
        outputs = numpy.array(outputlist, ndmin=2).T
        output_input = numpy.dot(self.wio, inputs)
        final_output = self.activation_function(output_input)
        error_list = outputs - final_output

        self.wio += self.learning_rate*numpy.dot((error_list*final_output*(1.0-final_output)), numpy.transpose(inputs))
        pass

    # 输出结果
    def query(self, inputlist):
        inputs = numpy.array(inputlist, ndmin=2).T
        output_input = numpy.dot(self.wio, inputs)
        final_output = self.activation_function(output_input)
        return final_output
        pass
    pass


test_input = 784
test_out = 10
learning = 0.1
n = perceptron(test_input, test_out, learning)
# 读取文件的数据
training_data_file = open("data\感知机\mnist_train_100.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()
for record in training_data_list:
    all_value = record.split(',')
    inputs = (numpy.asfarray(all_value[1:])/255.0*0.99)+0.01
    targets = numpy.zeros(test_out)+0.01
    targets[int(all_value[0])] = 0.99
    n.training(inputs, targets)
pass
"""训练完成"""
# 开始测试数据
test_data_file = open("data\感知机\mnist_test_10.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()
test_score = 0
for record in test_data_list:
    all_value = record.split(',')
    correct_answer = all_value[0]
    inputs = (numpy.asfarray(all_value[1:])/255.0*0.99)+0.01
    outputs = n.query(inputs)
    answer = numpy.argmax(outputs)
    # 计分器
    if int(correct_answer) == int(answer):
        test_score += 1
    else:
        test_score += 0
        pass
    pass
print(test_score)