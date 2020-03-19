import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")  # 定制文本框和箭头格式
leafNode = dict(boxstyle="round4", fc="0.8")  # 定制文本框和箭头格式
arrow_args = dict(arrowstyle="<-")  # 定制文本框和箭头格式


def plot_node(node_txt, center_pt, parent_pt, node_type):
    create_plot.ax1.annotate(node_txt, xy=parent_pt, xycoords='axes fraction',
                             xytext=center_pt, textcoords='axes fraction',
                             va="center", ha="center", bbox=node_type, arrowprops=arrow_args)  # 绘制带箭头的注解


# def create_plot():
#     fig = plt.figure(1, facecolor='white')
#     fig.clf()
#     create_plot.ax1 = plt.subplot(111, frameon=False)  # ticks for demo puropses
#     plot_node('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#     plot_node('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#     plt.show()

def plot_mid_text(ctr_pt, parent_pt, txt_string):
    x_mid = (parent_pt[0] - ctr_pt[0]) / 2.0 + ctr_pt[0]  # 在父子节点中填充文本信息
    y_mid = (parent_pt[1] - ctr_pt[1]) / 2.0 + ctr_pt[1]  # 在父子节点中填充文本信息
    create_plot.ax1.text(x_mid, y_mid, txt_string, va="center", ha="center", rotation=30)  # 在父子节点中填充文本信息


def plot_tree(my_tree, parent_pt, node_txt):
    num_leafs = get_num_leafs(my_tree)  # 计算树 x 轴的长度
    depth = get_tree_depth(my_tree)
    first_str = list(my_tree.keys())[0]  # 节点的标签
    ctr_pt = (plot_tree.xOff + (1.0 + float(num_leafs)) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(ctr_pt, parent_pt, node_txt)  # 标记子节点属性值
    plot_node(first_str, ctr_pt, parent_pt, decisionNode)
    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD  # 减少 y 的偏移
    for key in second_dict.keys():
        if type(second_dict[
                    key]).__name__ == 'dict':  # 测试节点的数据类型是否为字典，不是就是叶节点
            plot_tree(second_dict[key], ctr_pt, str(key))  # 递归
        else:  # 是叶节点则打印叶节点
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), ctr_pt, leafNode)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), ctr_pt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


def create_plot(in_tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    apropos = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **apropos)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plot_tree.totalW = float(get_num_leafs(in_tree))
    plot_tree.totalD = float(get_num_leafs(in_tree))
    plot_tree.xOff = -0.5 / plot_tree.totalW
    plot_tree.yOff = 1.0;
    plot_tree(in_tree, (0.5, 1.0), '')
    plt.show()


def get_num_leafs(my_tree):
    num_leafs = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[
                    key]).__name__ == 'dict':  # 测试节点的数据类型是否为字典，不是就是叶节点
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(my_tree):
    max_depth = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[
                    key]).__name__ == 'dict':  # 测试节点的数据类型是否为字典，不是就是叶节点
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def retrieve_tree(i):
    list_of_trees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                     {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                     ]
    return list_of_trees[i]