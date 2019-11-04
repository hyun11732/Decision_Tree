import math

K = 3


# Binary tree node class with has left, right node connected with useful information building the decision tree
class Node:
    def __init__(self, value, axis):
        self.left = None
        self.right = None
        self.value = value
        self.axis = axis
        self.leaf = False
# BFS traverse for the result tree print
    def traverse(self, root):
        current_level = [root]
        level = 0
        while current_level:
            print(level, end=" ")
            for node in current_level:
                print(node.value, node.axis, end=" ")
            print("")
            next_level = list()
            for n in current_level:
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
                current_level = next_level
            level += 1


# Extract column from the 2-D list
def column(matrix, col):
    return [row[col] for row in matrix]


# Find split points from train_matrix
def find_split_points(train_matrix):
    num_col = len(train_matrix[0])
    split_points = []
    for i in range(num_col):
        temp = list(set(column(train_matrix, i)))
        temp = sorted(temp)
        splits = []
        for i in range(len(temp) - 1):
            splits.append((temp[i] + temp[i + 1]) / 2)
        split_points.append(splits)
    return split_points


# Calculate gini
def calculate_gini(D1, D2, label_vector):
    giniD1 = len(D1) / (len(D1) + len(D2))
    giniD2 = len(D2) / (len(D1) + len(D2))
    keys = list(set(label_vector))
    dic = dict()
    for key in keys:
        dic[key] = 0
    for elem in D1:
        dic[elem[1]] += 1
    D1_split_gini = 0
    for key in keys:
        D1_split_gini += (dic[key] / len(D1)) ** 2
    giniD1 = giniD1 * (1 - D1_split_gini)
    dic.clear()
    for key in keys:
        dic[key] = 0
    for elem in D2:
        dic[elem[1]] += 1
    D2_split_gini = 0
    for key in keys:
        D2_split_gini += (dic[key] / len(D2)) ** 2
    giniD2 = giniD2 * (1 - D2_split_gini)
    return giniD1 + giniD2


def train_DT(train_matrix, label_vector, depth):
    # Create a leaf node, base case
    if depth > 1 or len(set(label_vector)) == 1:
        # When there is only one label left
        if len(set(label_vector)) == 1:
            node = Node(label_vector[0], None)
            node.leaf = True
            return node
        # When there are multiple labels are left
        else:
            score = dict()
            # Count the number of labels and find the most label.
            for label in label_vector:
                if label not in score.keys():
                    score[label] = 1
                else:
                    score[label] += 1
            # When tie, find smaller label
            max_label = sorted(score, key=lambda l: (-score[l], l))[0]
            node = Node(max_label, None)
            node.leaf = True
            return node
    # Find the split points
    split_points = find_split_points(train_matrix)
    min_gini = 10000000000
    node_attri = 0
    node_value = 0
    count = 0
    for splits in split_points:
        for split in splits:
            attri = column(train_matrix, count)
            D1 = [(attri[i], label_vector[i]) for i in range(len(attri)) if attri[i] <= split]
            D2 = [(attri[i], label_vector[i]) for i in range(len(attri)) if attri[i] > split]
            # Calculate gini
            gini = calculate_gini(D1, D2, label_vector)
            # If gini is smaller than min_gini, update it
            if gini < min_gini:
                min_gini = gini
                node_attri = count
                node_value = split
            # When tie, compare split attribute and update with smaller split point
            elif gini == min_gini:
                if split < node_value:
                    min_gini = gini
                    node_attri = count
                    node_value = split
        count += 1
    root = Node(node_value, node_attri)
    splited_matrix1 = []
    splited_matrix2 = []
    splited_label1 = []
    splited_label2 = []
    index = 0
    # split matrix and vector of left and right child node for the next recursion
    for row in train_matrix:
        if row[node_attri] <= node_value:
            splited_matrix1.append(row)
            splited_label1.append(label_vector[index])
        else:
            splited_matrix2.append(row)
            splited_label2.append(label_vector[index])
        index += 1
    root.left = train_DT(splited_matrix1, splited_label1, depth + 1)
    root.right = train_DT(splited_matrix2, splited_label2, depth + 1)
    return root


# Help function of predictDT for the recursion
def helpPredict(value, node):
    if node.leaf:
        return node.value
    else:
        result = 0
        if value[node.axis] <= node.value:
            result = helpPredict(value, node.left)
        else:
            result = helpPredict(value, node.right)
        return result


# Predict test_matrix on DTmodel
def predictDT(test_matrix, model):
    result = []
    for row in test_matrix:
        result.append(helpPredict(row, model))
    return result

if __name__ == "__main__":
    attri_dict = dict()
    test_matrix = []
    train_matrix = []
    label_vector = []
    label_dic = dict()
    string = input()
    values = string.split()
    label = values[0]
    for i in range(1, len(values)):
        temp = values[i].split(":")
        attri_dict[temp[0]] = i - 1
    train_row = 0
    test_row = 0
    labels = []
    while string != "":
        values = string.split()
        label = values[0]
        if int(label) != 0:
            train_matrix.append([1] * len(attri_dict))
            label_vector.append(label)
            for i in range(1, len(values)):
                attr = values[i].split(":")
                train_matrix[train_row][attri_dict[attr[0]]] = float(attr[1])
            label_dic[tuple(train_matrix[train_row])] = label
            labels.append(label)
            train_row += 1
        else:
            test_matrix.append([1] * len(attri_dict))
            for i in range(1, len(values)):
                attr = values[i].split(":")
                test_matrix[test_row][attri_dict[attr[0]]] = float(attr[1])
            test_row += 1
        try:
            string = input()
        except:
            break
    labels = list(set(labels))
    DTmodel = train_DT(train_matrix, label_vector, 0)
    DT_values = predictDT(test_matrix, DTmodel)
    for value in DT_values:
        print(value)