# Name Netanel Bashan 323056077
# Name Tzur-Eitan Levy 205431935

import random
import time

start_time = time.time()

N = 5  # no. of attributes
M = 100  # no. of rows in file
MINSUP = 0.2


# Creates a file named filename containing m sorted itemsets of items 0..N-1
def createfile(m, filename):
    f = open(filename, "w")
    for line in range(m):
        itemset = []
        for i in range(random.randrange(N) + 1):
            item = random.randrange(N)  # random integer 0..N-1
            if item not in itemset:
                itemset += [item]
        itemset.sort()
        for i in range(len(itemset)):
            f.write(str(itemset[i]) + " ")
        f.write("\n")
    f.close()


# Returns true iff all of smallitemset items are in bigitemset (the itemsets are sorted lists)
def is_in(smallitemset, bigitemset):
    s = b = 0  # s = index of smallitemset, b = index of bigitemset
    while s < len(smallitemset) and b < len(bigitemset):
        if smallitemset[s] > bigitemset[b]:
            b += 1
        elif smallitemset[s] < bigitemset[b]:
            return False
        else:
            s += 1
            b += 1
    return s == len(smallitemset)


# Returns a list of itemsets (from the list itemsets) that are frequent
# in the itemsets in filename
def frequent_itemsets(filename, itemsets):
    f = open(filename, "r")
    filelength = 0  # filelength is the no. of itemsets in the file. we
    # use it to calculate the support of an itemset
    count = [0] * len(itemsets)  # creates a list of counters
    count_absolute = [0] * len(itemsets)  # creates a list of counters
    line = f.readline()
    while line != "":
        filelength += 1
        line = line.split()  # splits line to separate strings
        for i in range(len(line)):
            line[i] = int(line[i])  # converts line to integers
        for i in range(len(itemsets)):
            if is_in(itemsets[i], line):
                count[i] += 1
        line = f.readline()
    f.close()
    freqitemsets = []
    for i in range(len(itemsets)):
        if count[i] >= MINSUP * filelength:
            freqitemsets += [itemsets[i]]
    return freqitemsets


def create_kplus1_itemsets(kitemsets, filename):
    """
    Create sets of all the combinations between the elements in 'kitemset'
    the length of each new sets will be grater in 1 from the length of the original sets.
    and remain only the sets that frequent in the file 'filename'
    :param kitemsets: list of list represents list of item sets
    :param filename: the file name
    :return: the sets that frequent in the file 'filename'
    """
    kplus1_itemsets = []
    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset

        while j < len(kitemsets) and kitemsets[i][:-1] == kitemsets[j][:-1]:
            sub_item_set = kitemsets[i] + [kitemsets[j][-1]]
            # Check that all the sub set are frequent,
            # if one of them not frequent - don't add the set to 'kplus1_itemsets'
            passed = True
            for k in range(len(sub_item_set)):
                temp = sub_item_set[0:k] + sub_item_set[k + 1:]
                if temp not in kitemsets:
                    passed = False
                    break
            if passed:
                kplus1_itemsets.append(sub_item_set)
            j += 1
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets)


def create_1itemsets(filename):
    """
    Create one initial item-set which every set contain one item from 0-N.
    :param filename: The file name
    :return: The sets that frequent in the file 'filename'
    """
    it = []
    for i in range(N):
        it += [[i]]
    return frequent_itemsets(filename, it)


def minsup_itemsets(filename):
    """
    Find all the item-set of all the sets that frequent in file 'filename' and its absolute support.
    :param filename: the file name
    :return: All the frequent set,
    The last element in each set representing the absolute support of the set in the file.
    """
    f = open(filename, "r")

    minsupsets = kitemsets = create_1itemsets(filename)  #
    while kitemsets != []:
        kitemsets = create_kplus1_itemsets(kitemsets, filename)
        minsupsets += kitemsets

    count_absolute = [0] * len(minsupsets)  # creates a list of counters

    filelength = 0
    line = f.readline()
    while line != "":
        filelength += 1
        for i in range(len(minsupsets)):
            if minsupsets[i] == [int(i) for i in line.split()]:
                count_absolute[i] += 1
        line = f.readline()
    f.close()
    for i in range(len(minsupsets)):
        minsupsets[i].append(count_absolute[i] / filelength)

    return minsupsets


# createfile(M, "itemsets.txt")
print(minsup_itemsets("itemsets.txt"))
print("--- %s seconds ---" % (time.time() - start_time))

