# Name Netanel Bashan 323056077
# Name Tzur-Eitan Levy 205431935

import math

DEPTH = 4


def split(examples, used, trait):
    """
    examples is a list of lists. every list contains the attributes, the last item is the class. all items are 0/1.
    splits examples into two lists based on trait (attribute).
    updates used that trait was used.
    """
    newEx = [[], []]  # newEx is a list of two lists, list of Ex that Ex[trait]=0 and list of Ex that Ex[trait]=1
    if trait < 0 or trait > len(examples[0]) - 2 or used[trait] == 0:
        return newEx  # illegal trait
    for e in examples:
        newEx[e[trait]] += [e]
    used[trait] = 0  # used is a list that marks trait as used
    return newEx


def isSameClass(examples, num):
    """
    returns 0 if all the examples are classified as 0.
    returns 1 if all the examples are classified as 1.
    returns 7  if there are no examples.
    returns -2 if there are more zeros than ones.
    returns -1 if there are more or equal ones than zeros.
    """
    if examples == []:
        return 7
    zo = [0, 0]  # zo is a counter of notNums and nums in class
    for e in examples:
        index = 1 if e[-1] == num else 0  # adaptation for checking each given number
        zo[index] += 1
    if zo[0] == 0:
        return 1
    if zo[1] == 0:
        return 0
    if zo[0] > zo[1]:
        return -2
    else:
        return -1


def infoInTrait(examples, i, num):
    """
    calculates the information in trait i using Shannon's formula
    """
    count = [[0, 0], [0, 0]]  # [no. of ex. with attr.=0 and clas.=0,no. of ex. with attr.=0 and clas.=1],
    # [no. of ex. with attr.=1 and clas.=0,no. of ex. with attr.=1 and clas.=1]
    for e in examples:
        index = 1 if e[-1] == num else 0  # adaptation for checking each given number
        count[e[i]][index] += 1
    x = 0
    # Shannon's formula
    if count[0][0] != 0 and count[0][1] != 0:
        x = count[0][0] * math.log((count[0][0] + count[0][1]) / count[0][0]) + \
            count[0][1] * math.log((count[0][0] + count[0][1]) / count[0][1])
    if count[1][0] != 0 and count[1][1] != 0:
        x += count[1][0] * math.log((count[1][0] + count[1][1]) / count[1][0]) + \
             count[1][1] * math.log((count[1][0] + count[1][1]) / count[1][1])
    return x


def minInfoTrait(examples, used, num):
    """
    used[i]=0 if trait i was already used. 1 otherwise.

    Returns the number of the trait with max. info. gain.
    If all traits were used returns -1.
    """
    minTrait = m = -1
    for i in range(len(used)):
        if used[i] == 1:
            info = infoInTrait(examples, i, num)
            if info < m or m == -1:
                m = info
                minTrait = i
    return minTrait


def build(examples, num, depth=DEPTH):  # builds used
    """
    :param examples: matrix of list, in each list n-1 first element are the features and the n is the label
    :param num: the target label to classify
    :param depth: the tree depth
    :return: decision tree
    """
    used = [1] * (len(examples[0]) - 1)  # used[i]=1 means that attribute i hadn't been used
    return recBuild(examples, used, 0, depth, num)


def recBuild(examples, used, parentMaj, depth, num):
    """
    Builds the decision tree.
    parentMaj = majority class of the parent of this node. the heuristic is that if there is no decision returns parentMaj
    :param examples: matrix of list, in each list n-1 first element are the features and the n is the label
    :param used: list that represents the features by 1 if feture used or 0 if not
    :param parentMaj: the majority labels of the parent examples
    :param depth: tree depth
    :param num: the target label to classify
    :return: decision tree
    """
    cl = isSameClass(examples, num)
    if cl == 0 or cl == 1:  # all zeros or all ones
        return [[], cl, []]
    if cl == 7 or depth == 0:  # examples is empty
        return [[], parentMaj, []]
    trait = minInfoTrait(examples, used, num)
    if trait == -1:  # there are no more attr. for splitting
        return [[], cl + 2, []]  # cl+2 - makes cl 0/1 (-2+2 / -1+2)
    x = split(examples, used, trait)
    left = recBuild(x[0], used[:], cl + 2, depth - 1, num)
    right = recBuild(x[1], used[:], cl + 2, depth - 1, num)
    return [left, trait, right]


def recClassifier(dtree, traits):  # dtree is the tree, traits is an example to be classified
    if dtree[0] == []:  # there is no left child, means arrive to a leaf
        return dtree[1]
    return recClassifier(dtree[traits[dtree[1]] * 2], traits)  # o points to the left child, 2 points to the right child


def classifier(dtree, traits):  # same as the former without recursion
    while dtree[0] != []:
        dtree = dtree[traits[dtree[1]] * 2]
    return dtree[1]


def convertArffToBinary(file_name, out_file, pixel=130):
    """
    Delete the arff attributes and for each line convert each feature to 1 if > pixel and 0 if <= pixel
    :param file_name: arrf file name
    :param out_file: target file to be the binary file
    :param pixel: the critical pixel
    :return: None
    """
    with open(file_name, "r") as a_file:
        lines = a_file.readlines()

    with open(out_file, "w") as new_file:
        lines = lines[lines.index("@data\n") + 1:]
        for j, line in enumerate(lines):
            line = line.split(',')
            for i, number in enumerate(line[:-1]):
                line[i] = '0' if int(number) < pixel else '1'
            line = ",".join(line)
            new_file.write(line)


def fileToMatrix(file_name):
    """
    Convert binary file to matrix
    :param file_name: binary file
    :return: matrix of all the line of the binary file
    """
    with open(file_name, 'r') as file:
        ret = [[int(num) for num in line.strip().split(',')] for line in file.readlines()]
    return ret


def buildClassifier(file_name, depth):
    """
    create decision trees to all numbers 0-9
    :param file_name: binary file of the traning data
    :param depth: trees depth
    :return: list of all the trees
    """
    mat = fileToMatrix(file_name)
    trees = []
    for i in range(10):
        trees.append(build(mat, i, depth))
    return trees


def classify(trees, image):
    """
    Classify the image in all the trees
    :param trees: list of decision trees
    :param image: list of n-1 features and label
    :return: all the image classify
    """
    ret = []
    for i, tree in enumerate(trees):
        if classifier(tree, image) == 1:
            ret.append(i)
    return ret


def tester(trees, tests):
    """
    Find the percent of the success classify to the all of the images in test
    :param trees: list of decision trees
    :param tests: list of images(list of n-1 features and 1 label)
    :return: the percent of success classify
    """
    correct = 0
    wrong = 0
    for test in tests:
        if classify(buildClassifier("binary_train.arff", 1), test) == [test[-1]]:
            correct += 1
        else:
            wrong += 1
    return correct / (correct + wrong)


def threshold():
    """
    Find the best critical pixel to get the best percent of success in classifing
    :return: the critical pixel
    """
    best = 0
    index = 0
    for i in range(256):
        convertArffToBinary("dig-test.arff", "binary_test.arff", i)
        tests = fileToMatrix("binary_test.arff")
        trees = buildClassifier("binary_train.arff", DEPTH)
        percentage = tester(trees, tests)
        if percentage > best:
            best = percentage
            index = i
    return index


e = [[1, 0, 0, 0, 0],
     [0, 1, 1, 0, 1],
     [1, 1, 1, 0, 0],
     [1, 1, 0, 1, 0],
     [0, 0, 1, 1, 1],
     [1, 0, 1, 1, 0],
     [1, 0, 0, 1, 1]]

# t = build(e)
# print(classifier(t, [0, 1, 1, 1]))


print(threshold())
