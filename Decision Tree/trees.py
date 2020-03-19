import operator
from math import log


def calc_shannon_ent(data_set):
    num_entries = len(data_set)
    label_counts = {}
    for featVec in data_set:  # 为所有可能分类创建字典
        current_label = featVec[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        shannon_ent -= prob * log(prob, 2)  # 以 2 为底求对数
    return shannon_ent


def create_data_set():
    data_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return data_set, labels


def split_data_set(data_set, axis, value):
    ret_data_set = []
    for featVec in data_set:
        if featVec[axis] == value:
            reduced_feat_vec = featVec[:axis]  # 抽取
            reduced_feat_vec.extend(featVec[axis + 1:])
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set


def choose_best_feature_to_split(data_set):
    num_features = len(data_set[0]) - 1  # 选最后一列为标签
    base_entropy = calc_shannon_ent(data_set)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_features):  # 遍历所有列
        feat_list = [example[i] for example in data_set]  # 创建唯一的分类标签列表
        unique_val = set(feat_list)  # 获取唯一的值
        new_entropy = 0.0
        for value in unique_val:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set) / float(len(data_set))
            new_entropy += prob * calc_shannon_ent(sub_data_set)
        info_gain = base_entropy - new_entropy  # 计算每种划分方式的信息熵
        if info_gain > best_info_gain:  # 比较信息熵
            best_info_gain = info_gain  # 如果比当前的优则设置
            best_feature = i
    return best_feature  # 返回最佳的信息熵


def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def create_tree(data_set, label):
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]  # 类别完全相同则停止划分
    if len(data_set[0]) == 1:  # 遍历完所有特征时返回出现次数最多的类别
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(data_set)
    best_feat_label = label[best_feat]
    my_tree = {best_feat_label: {}}
    del (label[best_feat])
    feat_values = [example[best_feat] for example in data_set]
    unique_val = set(feat_values)
    for value in unique_val:
        sub_labels = label[:]  # 复制所有标签，这样树就不会弄乱现有的标签
        my_tree[best_feat_label][value] = create_tree(split_data_set(data_set, best_feat, value), sub_labels)
    return my_tree


def classify(input_tree, feat_labels, test_vec):
    first_str = list(input_tree.keys())[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    key = test_vec[feat_index]
    value_of_feat = second_dict[key]
    if isinstance(value_of_feat, dict):
        class_label = classify(value_of_feat, feat_labels, test_vec)
    else:
        class_label = value_of_feat
    return class_label


def store_tree(input_tree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input_tree, fw)
    fw.close()


def grab_tree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)
