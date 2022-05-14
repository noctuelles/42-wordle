#!/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    read.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ykuo and plouvel                           +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/05/13 21:33:15 by ykuo              #+#    #+#              #
#    Updated: 2022/05/13 23:13:03 by ykuo             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import random
import signal
import array
import datetime
from display import *

# global variable
word_list     = []
output_buffer = []
win           = 0
keyboard      = std_keyboard

def read_dict(filename):
	try:
		f = open(filename, "r")
	except IOError as e:
		print("\x1b[31mfatal:\x1b[0m  cannot open file: " + e.strerror)
		sys.exit(1)

	nbr_line      = 0
	for index, line in enumerate(f):
		line = line.strip()
		if line:
			if not line.isalpha() or len(line) != 5:
				print(f'\x1b[31merror:\x1b[0m line {index}: not a valid word.')
				sys.exit(1)
			else:
				if line not in word_list:
					line = line.lower()
					word_list.append(line)
				else:
					print('\x1b[31merror:\x1b[0m dictionary contains duplicate.')
					sys.exit(1)
		nbr_line = index
	f.close()

	if not word_list:
		print("\x1b[31merror:\x1b[0m  dictionary is empty.")
		sys.exit(1)

def generate_new_word(word_list):
	os.system('clear')
	mode= True
	try:
		user_input = input('Do you want to play in ulmite mode? (y/n): ').strip().lower()
		if (user_input == 'y'):
			mode = False
	except KeyboardInterrupt:
		print('\nGoodbye !')
		sys.exit(1)
	except EOFError as err:
		print('\nGoodbye !')
		sys.exit(1)
	nbr_line = len(word_list)
	random_index = random.randint(0, nbr_line)
	if mode is True:
		random_index = datetime.date.today().year
		random_index += datetime.date.today().month
		random_index += datetime.date.today().day
		random_index %= nbr_line
	word_to_guess = word_list[random_index]
	return word_to_guess

def print_board(output_buffer):
	line_printed = 0

	print('\t\t\t\t' + '*' * 23)
	print('\t\t\t\t*' + ' ' * 21 + '*')
	for i in output_buffer:
		print (f'\t\t\t\t*  {i}  *')
		line_printed += 1
	
	i = line_printed
	while i < 6:
		print('\t\t\t\t*  _   _   _   _   _  *')
		i += 1
	print('\t\t\t\t*' + ' ' * 21 + '*')
	print('\t\t\t\t' + '*' * 23)
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
			output = "".join([output, '\x1b[92m', user_input[i].upper(), '\x1b[0m', '   '])
		elif value == 1:
			output = "".join([output, '\x1b[93m', user_input[i].upper(), '\x1b[0m', '   '])
		elif value == 0:
			output = "".join([output, '\x1b[90m', user_input[i].upper(), '\x1b[0m', '   '])
	return output.strip()

def color_keyboard(input_idc, user_input):
	global keyboard

	user_input = user_input.upper()
	for i,value in enumerate(input_idc):
		if value == 2:
			keyboard = keyboard.replace(f'|{user_input[i]} |', f'|\x1b[92m{user_input[i]}\x1b[0m |')
			keyboard = keyboard.replace(f'|\x1b[93m{user_input[i]}\x1b[0m |', f'|\x1b[92m{user_input[i]}\x1b[0m |')
			keyboard = keyboard.replace(f'|\x1b[90m{user_input[i]}\x1b[0m |', f'|\x1b[92m{user_input[i]}\x1b[0m |')
		elif value == 1:
			keyboard = keyboard.replace(f'|{user_input[i]} |', f'|\x1b[93m{user_input[i]}\x1b[0m |')
		elif value == 0:
			keyboard = keyboard.replace(f'|{user_input[i]} |', f'|\x1b[90m{user_input[i]}\x1b[0m |')
	
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
		color_keyboard (input_idc, user_input)
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
	color_keyboard (input_idc, user_input)
	return convert_to_output_str(input_idc, user_input)

def game_loop():
	game_turns = 0
	error_msg = ""
	word_to_guess = generate_new_word(word_list)

	while True:
		os.system('clear')
		print(title)
		print_board(output_buffer)
		if error_msg:
			print(error_msg)
			error_msg = ""
		print(keyboard)
		if win == 1:
			print('Congratulation, you won !')
			break
		elif game_turns == 6:
			print(f'You loose ! The word was : \'{word_to_guess}\'.')
			break
		try:
			user_input = input('Your word: ').strip().lower()
		except KeyboardInterrupt:
			print('\nGoodbye !')
			sys.exit(1)
		except EOFError as err:
			continue
		if len(user_input) != 5:
			error_msg = f'\x1b[31merror:\x1b[0m \'{user_input}\': must contains 5 letters.'
			continue
		if user_input in word_list:
			output_buffer.append(check_word(word_to_guess, user_input))
			game_turns += 1
		else:
			error_msg = f'\x1b[31merror:\x1b[0m  \'{user_input}\' is not a valid word.'
			continue
	retry()

def retry():
	global output_buffer
	global keyboard
	global win
	
	try:
		user_input = input('Do you want to retry (y/n): ').strip().lower()
		if (user_input == 'y'):
			output_buffer = []
			keyboard = std_keyboard
			win = 0
			game_loop()
		else:
			print('\nGoodbye !')
	except KeyboardInterrupt or EOFError as err:
		print('\nGoodbye !')
		sys.exit(1)

def main():
	global keyboard
	if len(sys.argv) != 2:
		print(f'\x1b[31musage:\x1b[0m: {sys.argv[0]} <path_to_dictionary>')
		sys.exit(1)
	else:
		print('Loading your dictionnary...')
		word_to_guess = read_dict(sys.argv[1])
	game_loop()

if __name__ == "__main__":
    main()