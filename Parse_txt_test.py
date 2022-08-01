# Get number of lines to determine which webpage program is on
def get_num_lines(fName):
    f = open(fName, 'r+')
    count = 0
    for line in f:
        count = count + 1
    f.close()
    print(count)
    return count

# File 1 overwrites File 2
def overwrite_file(file1, file2):
        fRead = open(file1, 'r')
        fWrite = open(file2, 'w+')
        while True:
                line = fRead.readline()
                if line == '':
                        break
                else:
                        fWrite.write(line)
        fRead.close()
        fWrite.close()

get_num_lines('11_13_2020_21_25.txt')
overwrite_file('11_13_2020_21_25.txt', '11_13_2020_20_27.txt')