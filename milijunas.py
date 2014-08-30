#-*- coding:utf-8 -*- 
import random

my_choice = None

counter =0

my_choice = raw_input("\nKoji je najveci kontinent?\n a) Europa \n b) Azija \n c) Sjeverna Amerika \n d) Antarktika \n\n Konacni odgovor:  ")

if my_choice != 'b':
	print " \n Netocan odgovor! \n"
	print ' Bodovi', counter, '\n'
else:
	print " Tocan odgovor! \n" 
	counter += 100
	print ' Bodovi', counter, '\n'
	
my_choice = raw_input("Koji je glavni grad Njemacke? \n a) Köln, \n b) Stuttgart \n c) Berlin \n d) München \n\n Konacni odgovor: ")
if my_choice != 'c':
	print " \n Netocan odgovor! \n"
else:
	print " Tocan odgovor! \n" 
	counter += 100
	print ' Bodovi', counter, '\n'
	

my_choice = raw_input("Koji je glavni grad Njemacke? \n a) Köln, \n b) Stuttgart \n c) Berlin \n d) München \n\n Konacni odgovor: ")
if my_choice != 'c':
	print " \n Netocan odgovor! \n"
else:
	print " Tocan odgovor! \n" 
	counter += 100
	print ' Bodovi', counter, '\n'
