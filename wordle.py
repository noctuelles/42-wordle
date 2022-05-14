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
import array

# global variable
word_list     = []
output_buffer = []
win           = 0

def read_dict(filename):
	try:
		f = open(filename, "r")
	except IOError as e:
		print("fatal: cannot open file: " + e.strerror)
		sys.exit(1)

	nbr_line      = 0
	for index, line in enumerate(f):
		line = line.strip()
		if line:
			if not line.isalpha(): #or len(line) != 5:
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
	return word_to_guess

def print_board(output_buffer):
	line_printed = 0

	for i in output_buffer:
		print (f'{i}')
		line_printed += 1
	
	i = line_printed
	while i < 6:
		print('_  _  _  _  _')
		i += 1
	print('\n')

def is_the_word_to_guess(input_idc):
	for i,value in enumerate(input_idc):
		if input_idc[i] != 2:
			return False
	return True

def convert_to_output_str(input_idc, user_input):
	output = ""

	for i,value in enumerate(input_idc):
		if value == 2:
			output = "".join([output, '\x1b[92m', user_input[i].upper(), '\x1b[0m', '  '])
		elif value == 1:
			output = "".join([output, '\x1b[93m', user_input[i].upper(), '\x1b[0m', '  '])
		elif value == 0:
			output = "".join([output, '\x1b[90m', user_input[i].upper(), '\x1b[0m', '  '])
	return output

def check_word(word_to_guess, user_input):
	global win
	output = ""
	input_idc = array.array('I', [0, 0, 0, 0, 0])

	for i,letter in enumerate(user_input):
		if user_input[i] == word_to_guess[i]:
			input_idc[i] = 2
		elif user_input[i] in word_to_guess:
			input_idc[i] = 1
	if is_the_word_to_guess(input_idc) == True:
		win = 1
		return convert_to_output_str(input_idc, user_input)
	for i,value in enumerate(input_idc):
			if value == 1:

				occurence_nbr = word_to_guess.count(user_input[i])
				for k,value in enumerate(word_to_guess):
					if value == user_input[i] and input_idc[k] == 2:
						occurence_nbr -= 1 
				if occurence_nbr <= 0:
					input_idc[i] = 0

				occurence_nbr = word_to_guess.count(user_input[i])
				k = 0
				while k != i:
					if user_input[i] == user_input[k] and input_idc[k] == 1:
						occurence_nbr -= 1
					k += 1
				if occurence_nbr <= 0:
					input_idc[i] = 0
	
	return convert_to_output_str(input_idc, user_input)

def game_loop(word_to_guess):
	game_turns = 0
	
	while 1:
		user_input = input ("input: ")
		print('\n')
		if len(user_input) != 5:
			print('error: the word must contains 5 letters.')
			continue
		if user_input in word_list:
			output_buffer.append(check_word(word_to_guess, user_input))
			print_board(output_buffer)
			game_turns += 1
			if win == 1:
				print('Congratulation, you won !')
				break
			elif game_turns == 6:
				print('You loose !')
				break
		else:
			print(f'error: input \'{user_input}\' is not a valid word.')
			continue

def main():
	if len(sys.argv) != 2:
		print(f'usage: {sys.argv[0]} <path_to_dictionary>')
		sys.exit(1)
	else:
		word_to_guess = read_dict(sys.argv[1])

	word_to_guess = 'maple'
	print(f'ans: {word_to_guess}')
	game_loop(word_to_guess)

if __name__ == "__main__":
    main()
