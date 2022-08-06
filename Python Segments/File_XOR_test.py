# This script performs an XOR of two files to find what is different
import os

def file_xor():
	with open('login_attempt.txt', 'r') as file1:
    	with open('webpage_status.txt', 'r') as file2:
        	new_activity = set(file1).difference(file2)
			# ex: 
			# x = {"apple", "banana", "cherry", "grapes", "canteloupes", "oranges"}
			# y = {"banana", "cherry", "grapes", "canteloupes", "oranges"}
			# z = x.difference(y) ---> {"apple"}
	with open('XOR_output.txt', 'w') as file_out:
		for line in new_activity:
			file_out.write(line)
