import math
DEPTH = 1


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


def isSameClass(examples):
    """
    returns 0 if all the examples are classified as 0.
    returns 1 if all the examples are classified as 1.
    returns 7  if there are no examples.
    returns -2 if there are more zeros than ones.
    returns -1 if there are more or equal ones than zeros.
    """
    if examples == []:
        return 7
    zo = [0, 0]  # zo is a counter of zeros and ones in class
    for e in examples:
        zo[e[-1]] += 1
    if zo[0] == 0:
        return 1
    if zo[1] == 0:
        return 0
    if zo[0] > zo[1]:
        return -2
    else:
        return -1


def infoInTrait(examples, i):
    """
    calculates the information in trait i using Shannon's formula
    """
    count = [[0, 0], [0, 0]]  # [no. of ex. with attr.=0 and clas.=0,no. of ex. with attr.=0 and clas.=1],
    # [no. of ex. with attr.=1 and clas.=0,no. of ex. with attr.=1 and clas.=1]
    for e in examples:
        count[e[i]][e[-1]] += 1
    x = 0
    # Shannon's formula
    if count[0][0] != 0 and count[0][1] != 0:
        x = count[0][0] * math.log((count[0][0] + count[0][1]) / count[0][0]) + \
            count[0][1] * math.log((count[0][0] + count[0][1]) / count[0][1])
    if count[1][0] != 0 and count[1][1] != 0:
        x += count[1][0] * math.log((count[1][0] + count[1][1]) / count[1][0]) + \
             count[1][1] * math.log((count[1][0] + count[1][1]) / count[1][1])
    return x


def minInfoTrait(examples, used):
    """
    used[i]=0 if trait i was already used. 1 otherwise.

    Returns the number of the trait with max. info. gain.
    If all traits were used returns -1.
    """
    minTrait = m = -1
    for i in range(len(used)):
        if used[i] == 1:
            info = infoInTrait(examples, i)
            if info < m or m == -1:
                m = info
                minTrait = i
    return minTrait


def build(examples, depth=DEPTH):  # builds used
    used = [1] * (len(examples[0]) - 1)  # used[i]=1 means that attribute i hadn't been used
    return recBuild(examples, used, 0, depth)


def recBuild(examples, used, parentMaj, depth):
    """
    Builds the decision tree.
    parentMaj = majority class of the parent of this node. the heuristic is that if there is no decision returns parentMaj
    """
    cl = isSameClass(examples)
    if cl == 0 or cl == 1:  # all zeros or all ones
        return [[], cl, []]
    if cl == 7 or depth == 0:  # examples is empty
        return [[], parentMaj, []]
    trait = minInfoTrait(examples, used)
    if trait == -1:  # there are no more attr. for splitting
        return [[], cl + 2, []]  # cl+2 - makes cl 0/1 (-2+2 / -1+2)
    x = split(examples, used, trait)
    left = recBuild(x[0], used[:], cl + 2, depth-1)
    right = recBuild(x[1], used[:], cl + 2, depth-1)
    return [left, trait, right]


def recClassifier(dtree, traits):  # dtree is the tree, traits is an example to be classified
    if dtree[0] == []:  # there is no left child, means arrive to a leaf
        return dtree[1]
    return recClassifier(dtree[traits[dtree[1]] * 2], traits)  # o points to the left child, 2 points to the right child


def classifier(dtree, traits):  # same as the former without recursion
    while dtree[0] != []:
        dtree = dtree[traits[dtree[1]] * 2]
    return dtree[1]


e = [[1, 0, 0, 0, 0],
     [0, 1, 1, 0, 1],
     [1, 1, 1, 0, 0],
     [1, 1, 0, 1, 0],
     [0, 0, 1, 1, 1],
     [1, 0, 1, 1, 0],
     [1, 0, 0, 1, 1]]


def convertArffToBinary(file_name,pixel = 130):
    with open(file_name, "r") as a_file:
        lines = a_file.readlines()

    with open("binary_train.arff", "w") as new_file:
        lines = lines[lines.index("@data\n") + 1:]
        for j,line in enumerate(lines):
            line = line.split(',')
            for i,number in enumerate(line[:-1]):
                line[i] = '0' if int(number) < pixel else '1'
            line = ",".join(line)
            new_file.write(line)


# t = build(e)
# print(classifier(t, [0, 1, 1, 1]))
convertArffToBinary("dig-train.arff")