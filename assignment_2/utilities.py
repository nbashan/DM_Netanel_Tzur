def convert2arff(num_of_files):
    fout=open("hospital.arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute ward numeric\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time numeric\n")
    fout.write("@attribute temperatue numeric\n\n")
    fout.write("@data\n")
    for ward in range(1, num_of_files+1):
        fin=open(str(ward)+".txt", "r")
        for time in range(60*24):
            s=fin.readline().split()
            for patient in range(len(s)):
                fout.write(str(ward)+","+str(patient+1)+",")
                fout.write(str(time)+","+s[patient]+"\n")
        fin.close()
    fout.close()

convert2arff(3)