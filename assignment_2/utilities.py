from cmath import sqrt


def convert2arffNotCleaned(num_of_files:int) ->None:
    fout=open("hospitalNotCleaned.arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute ward numeric\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time numeric\n")
    fout.write("@attribute temperature numeric\n\n")
    fout.write("@data\n")
    for ward in range(1, num_of_files+1):
        fin=open("department_" + str(ward)+".txt", "r")
        for time in range(60*24):
            s=fin.readline().split()
            for patient in range(len(s)):
                fout.write(str(ward)+","+str(patient+1)+"," + str(time)+","+s[patient]+"\n")
        fin.close()
    fout.close()


def fahrenheitToCelsius(F:float)->float:
    return 5/9*(F-32)

def isCelsius(C:float)->float:
    return 31 < C < 43

def isFahrenheit(F:float)->float:
    return 88 < F < 110

def highOrLow(degree:float)->str:
    if degree <= 37:
        return "Low"
    else:
        return "High"



def convert2arff(num_of_files:int) -> None:
    fout=open("hospital.arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time numeric\n")
    fout.write("@attribute temperature {Low, High}\n\n")
    fout.write("@data\n")
    for ward in range(1, num_of_files+1):
        fin=open("department_" + str(ward)+".txt", "r")
        for time in range(60*12):
            s=fin.readline().split()
            for patient in range(len(s)):
                degree = float(s[patient])
                if isCelsius(degree):
                    degree = highOrLow(degree)
                elif isFahrenheit(degree):
                    degree = highOrLow(fahrenheitToCelsius(degree))
                else:
                    degree = "?"
                fout.write(str(patient+1)+"," + str(time)+","+degree+"\n")
        fin.close()
    fout.close()


def stdv(num_file:int) -> float:
        fin=open("department_" + str(num_file)+".txt", "r")
        sum = 0
        num_of_patients = 0
        for time in range(60*24):
            s=fin.readline().split()
            for patient in range(len(s)):
                degree = float(s[patient])
                if isFahrenheit(degree):
                    degree = fahrenheitToCelsius(degree)
                if isCelsius(degree):
                    sum +=degree
                    num_of_patients += 1
        fin.close()

        fin=open("department_" + str(num_file)+".txt", "r")

        mean = sum / num_of_patients

        variance = 0

        for time in range(60*24):
            s=fin.readline().split()
            for patient in range(len(s)):
                degree = float(s[patient])
                variance += (degree - mean)**2

        variance = variance/num_of_patients

        dev = sqrt(variance)

        fin.close()

        return  dev

#convert2arff(3)
#convert2arffNotCleaned(3)

print(stdv(1))
print(stdv(2))
print(stdv(3))
