#!/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    read.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ykuo <marvin@42.fr>                        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/05/13 21:33:15 by ykuo              #+#    #+#              #
#    Updated: 2022/05/13 23:13:03 by ykuo             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import random

# global variable

word_list     = []
output_buffer = []
nbr_line      = 0

if len(sys.argv) != 2:
	print(f'usage: {sys.argv[0]} <path_to_dictionary>')
	sys.exit(1)

try:
	f = open(sys.argv[1], "r")
except IOError as e:
	print("fatal: cannot open file: " + e.strerror)
	sys.exit(1)

for index, line in enumerate(f):
	line = line.strip()
	if line:
		if not line.isalpha() or len(line) != 5:
			print(f'error: line {index}: not a valid word.')
			sys.exit(1)
		else:
			if line not in word_list:
				word_list.append(line)
			else:
				print('error: dictionary contains duplicate.')
				sys.exit(1)
	nbr_line = index
f.close()

if not word_list:
	print("error: dictionary is empty.")
	sys.exit(1)

random_index = random.randint(0, nbr_line)
word_to_guess = word_list[random_index]
word_to_guess = "banjos"

# print(f'{random_index}: {word_list[random_index]}')


while 1:
	for i in output_buffer:
		print (f'{i}')
	output = ""
	user_input = input ("input:")
	if len(user_input) != 5:
		print('error: the word must contains 5 letters.')
		continue
	if user_input in word_list:
		for i,letter in enumerate(user_input):
			if word_to_guess[i] == user_input[i]:
				output = "".join([output, '\x1b[92m', user_input[i].upper(), '\x1b[0m', '  '])
			elif user_input[i] in word_to_guess:
				output = "".join([output, '\x1b[93m', user_input[i].upper(), '\x1b[0m', '  '])
			else:
				output = "".join([output, '\x1b[90m', user_input[i].upper(), '\x1b[0m', '  '])
		output_buffer.append(output)
	else:
		print(f'error: input \'{user_input}\' is not a valid word.')
		continue
