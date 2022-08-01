# Function: delete_file(fName)
# Description: input file name with relative path to delete it
def delete_file(fName):
	toDelete = open(fName, 'w+') # deletes file by opening it as write
	toDelete.close()
#
#
# Function: display_file(fName)
# Description: Useful tool for displaying the contents of a text file.
def display_file(fName):
        disp = open(fName, 'r+')
        print("\n  FILE:",fName,":\n")
        count = 1
        for line in disp:
                print("  TAG", count, "--",line)
                count = count + 1
        print("  END OF FILE")
#
#
# Function: write_to_records()
# Description: appends the contents of a temp file into the records
def write_to_records():
	fRead = open('./temp.txt', 'r+')
	fWrite = open('./record.txt', 'a+')
	while True:
		line = fRead.readline()
		if line == '':
			break
		else:
			fWrite.write(line)
	fRead.close()
	fWrite.close()
#
#
# Function: overwrite_records()
# Description: erases the contents of record.txt upon opening and replaces it with contents of temp file
def overwrite_records():
        fRead = open('./temp.txt', 'r')
        fWrite = open('./record.txt', 'w+')
        while True:
                line = fRead.readline()
                if line == '':
                        break
                else:
                        fWrite.write(line)
        fRead.close()
        fWrite.close()
#
#
# Function: get_num_tags()
# Description: returns the number of tags registered in the record file. It does so by simply counting the lines
def get_num_tags():
	f = open('./record.txt', 'r+')
	count = 0
	for line in f:
		count = count + 1
	f.close()
	print("\nNUMBER OF TAGS REGISTERED: ", count)
	return count
