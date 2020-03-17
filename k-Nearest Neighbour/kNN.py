from numpy import *
import operator
from os import listdir


def classify0(in_x, data_set, labels, k_v):
    data_set_size = data_set.shape[0]
    diff_mat = tile(in_x, (data_set_size, 1)) - data_set  # 距离计算
    sq_diff_mat = diff_mat ** 2  # 距离计算
    sq_distances = sq_diff_mat.sum(axis=1)  # 距离计算
    distances = sq_distances ** 0.5  # 距离计算
    sorted_dist_indices = distances.argsort()
    class_count = {}
    for i in range(k_v):  # 选取距离最小的k个点
        vote_i_label = labels[sorted_dist_indices[i]]  # 选取距离最小的k个点
        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1  # 选取距离最小的k个点
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)  # 排序
    return sorted_class_count[0][0]


def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(input("percentage of time spent playing video games ?"))
    f_miles = float(input("frequent flier miles earned per year ?"))
    ice_cream = float(input("liters of ice cream consumed per year ?"))
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    nor_mat, ranges, min_val = auto_norm(dating_data_mat)
    in_arr = array([f_miles, percent_tats, ice_cream])
    classifier_result = classify0((in_arr - min_val) / ranges, nor_mat, dating_labels, 3)
    print("You will probably like this person : ", result_list[classifier_result - 1])


def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def file2matrix(filename):
    fr = open(filename)
    number_of_lines = len(fr.readlines())  # 得到文件的行数
    return_mat = zeros((number_of_lines, 3))  # 创建返回的 Numpy 矩阵
    class_label_vector = []  # 准备返回的标签
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split('\t')
        return_mat[index, :] = list_from_line[0:3]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return return_mat, class_label_vector


def auto_norm(data_set):
    min_val = data_set.min(0)
    max_val = data_set.max(0)
    ranges = max_val - min_val
    norm_data_set = zeros(shape(data_set))
    m = data_set.shape[0]
    norm_data_set = data_set - tile(min_val, (m, 1))
    norm_data_set = norm_data_set / tile(ranges, (m, 1))  # element wise divide
    return norm_data_set, ranges, min_val


def dating_class_test():
    ho_ratio = 0.50  # hold out 10%
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')  # load dataset from file
    norm_mat, ranges, min_val = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vec = int(m * ho_ratio)
    error_count = 0.0
    for i in range(num_test_vec):
        classifier_result = classify0(norm_mat[i, :], norm_mat[num_test_vec:m, :], dating_labels[num_test_vec:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifier_result, dating_labels[i]))
        if classifier_result != dating_labels[i]:
            error_count += 1.0
    print("the total error rate is: %f" % (error_count / float(num_test_vec)))
    print(error_count, num_test_vec)


def img2vector(filename):
    return_vec = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vec[0, 32 * i + j] = int(line_str[j])
    return return_vec


def handwriting_class_test():
    hw_labels = []
    training_file_list = listdir('trainingDigits')  # 获取目录的内容
    m = len(training_file_list)
    training_mat = zeros((m, 1024))
    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]  # 去除 .txt
        class_num_str = int(file_str.split('_')[0]) # 从文件名获取数字
        hw_labels.append(class_num_str)
        training_mat[i, :] = img2vector('trainingDigits/%s' % file_name_str)
    test_file_list = listdir('testDigits')  # iterate through the test set
    error_count = 0.0
    m_test = len(test_file_list)
    for i in range(m_test):
        file_name_str = test_file_list[i]
        file_str = file_name_str.split('.')[0]  # 去掉 .txt
        class_num_str = int(file_str.split('_')[0])
        vector_under_test = img2vector('testDigits/%s' % file_name_str)
        classifier_result = classify0(vector_under_test, training_mat, hw_labels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifier_result, class_num_str))
        if classifier_result != class_num_str:
            error_count += 1.0
    print("the total number of errors is: %d" % error_count)
    print("the total error rate is: %f" % (error_count / float(m_test)))
