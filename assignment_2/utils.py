from cmath import sqrt


def convert2arffNotCleaned(num_of_files: int) -> None:
    """
    Convert cubeBase file to .arff
    without checking the reliability of the data
    :param num_of_files: num of files to convert
    :type num_of_files: int
    :return: None
    :rtype: None
    """
    fout = open("hospitalNotCleaned.arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute ward numeric\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time numeric\n")
    fout.write("@attribute temperature numeric\n\n")
    fout.write("@data\n")
    for ward in range(1, num_of_files + 1):
        fin = open("department_" + str(ward) + ".txt", "r")
        for time in range(60 * 24):
            s = fin.readline().split()
            for patient in range(len(s)):
                fout.write(str(ward) + "," + str(patient + 1) + "," + str(time) + "," + s[patient] + "\n")
        fin.close()
    fout.close()


def fahrenheitToCelsius(fahrenheit: float) -> float:
    """
    Convert celsius to fahrenheit
    :param fahrenheit: degree
    :type fahrenheit: float
    :return: The same degree on the Celsius scale
    :rtype: float
    """
    return 5 / 9 * (fahrenheit - 32)


def isCelsius(celsius: float) -> float:
    """
    Check whether the degree scale is Celsius
    :param celsius: degree
    :type celsius: float
    :return: whether "celsius" is in reasonable range of Celsius
    :rtype: bool
    """
    return 31 < celsius < 43


def isFahrenheit(fahrenheit: float) -> float:
    """
    Check whether the degree scale is Fahrenheit
    :param fahrenheit: degree
    :type fahrenheit: float
    :return: whether "fahrenheit" is in reasonable range of Fahrenheit
    :rtype: bool
    """
    return 88 < fahrenheit < 110


def highOrLow(degree: float) -> str:
    """
    Catalogs the degrees to "High" or "Low"
    :param degree:
    :type degree:
    :return: if degree <= 37 return "Low" otherwise return "High"
    :rtype: String
    """
    if degree <= 37:
        return "Low"
    else:
        return "High"


def convert2arff(num_of_files: int) -> None:
    """
    Convert cubeBase file to .arff
    Checking the reliability of the data
    :param num_of_files: num of files to convert
    :type num_of_files: int
    :return: None
    :rtype: None
    """
    fout = open("hospital.arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time numeric\n")
    fout.write("@attribute temperature {Low, High}\n\n")
    fout.write("@data\n")
    for ward in range(1, num_of_files + 1):
        fin = open("department_" + str(ward) + ".txt", "r")
        for time in range(60 * 12):
            s = fin.readline().split()
            for patient in range(len(s)):
                degree = float(s[patient])
                if isCelsius(degree):
                    degree = highOrLow(degree)
                elif isFahrenheit(degree):
                    degree = highOrLow(fahrenheitToCelsius(degree))
                else:
                    degree = "?"
                fout.write(str(patient + 1) + "," + str(time) + "," + degree + "\n")
        fin.close()
    fout.close()


def stdv(num_file: int) -> float:
    """
    Find the Standard deviation of the temperature of the inpatients of a certain ward
    :param num_file: the number of the ward
    :type num_file: int
    :return: Standard deviation of the patient
    :rtype: float
    """
    fin = open("department_" + str(num_file) + ".txt", "r")
    sum = 0
    num_of_patients = 0
    for time in range(60 * 24):
        s = fin.readline().split()
        for patient in range(len(s)):
            degree = float(s[patient])
            if isFahrenheit(degree):
                degree = fahrenheitToCelsius(degree)
            if isCelsius(degree):
                sum += degree
                num_of_patients += 1
    fin.close()

    fin = open("department_" + str(num_file) + ".txt", "r")

    mean = sum / num_of_patients

    variance = 0

    for time in range(60 * 24):
        s = fin.readline().split()
        for patient in range(len(s)):
            degree = float(s[patient])
            variance += (degree - mean) ** 2

    variance = variance / num_of_patients

    dev = sqrt(variance)

    fin.close()

    return dev


# convert2arff(3)
# convert2arffNotCleaned(3)

print(stdv(1))
print(stdv(2))
print(stdv(3))
