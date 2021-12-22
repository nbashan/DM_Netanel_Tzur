def idx2arff(images, labels, weka):
    fout = open(weka, "w")
    fout.write("@relation digits\n")
    for i in range(28):
        for j in range(28):
            fout.write("@attribute p_" + str(i) + "_" + str(j) + " numeric\n")
    fout.write("@attribute digit {0,1,2,3,4,5,6,7,8,9}\n")
    fout.write("@data\n")
    fimages = open(images, "rb")
    flabels = open(labels, "rb")
    flabels.seek(8)
    fimages.seek(16)
    x = fimages.read(1)
    while x != b"":
        fout.write(str(ord(x)) + ",")
        for i in range(783):
            fout.write(str(ord(fimages.read(1))) + ",")
        fout.write(str(ord(flabels.read(1))) + "\n")
        x = fimages.read(1)
    fout.close()
    fimages.close()
    flabels.close()


idx2arff("train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz", "digits-testing.arff")