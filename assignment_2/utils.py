from cmath import sqrt


def convert_2_arff_Not_Cleaned(num_of_files: int) -> None:
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


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert celsius to fahrenheit
    :param fahrenheit: degree
    :type fahrenheit: float
    :return: The same degree on the Celsius scale
    :rtype: float
    """
    return 5 / 9 * (fahrenheit - 32)


def is_celsius(celsius: float) -> float:
    """
    Check whether the degree scale is Celsius
    :param celsius: degree
    :type celsius: float
    :return: whether "celsius" is in reasonable range of Celsius
    :rtype: bool
    """
    return 36 <= celsius <= 43


def is_fahrenheit(fahrenheit: float) -> float:
    """
    Check whether the degree scale is Fahrenheit
    :param fahrenheit: degree
    :type fahrenheit: float
    :return: whether "fahrenheit" is in reasonable range of Fahrenheit
    :rtype: bool
    """
    return 96 <= fahrenheit <= 110


def high_or_low(degree: float) -> str:
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
                if is_celsius(degree):
                    degree = high_or_low(degree)
                elif is_fahrenheit(degree):
                    degree = high_or_low(fahrenheit_to_celsius(degree))
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
    my_sum = 0
    multi = 0
    num_of_patients = 0
    count = 0
    for time in range(60 * 24):
        s = fin.readline().split()
        for patient in range(len(s)):
            degree = float(s[patient])
            if is_fahrenheit(degree):
                degree = fahrenheit_to_celsius(degree)
                my_sum += degree
                multi += degree**2
                num_of_patients += 1
            elif is_celsius(degree):
                my_sum += degree
                multi += degree**2
                num_of_patients += 1
    fin.close()

    avg = my_sum / num_of_patients
    sqr_sum = multi / num_of_patients

    return sqrt(sqr_sum - avg**2)


# convert2arff(1)
# convert2arffNotCleaned(3)

print(stdv(1))
print(stdv(2))
print(stdv(3))
