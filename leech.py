#!/usr/bin/python3
		
from sys import argv
from random import randint
from src.amz import *
from os import system, path
from selenium.common.exceptions import InvalidSelectorException

class GetRewards:
	
	@staticmethod  # using this func whitout an instance
	def main(argv1, argv2):
		acc = CreateAccount(argv1)  # create instance

		name = acc.generate_name()  # get name

		passw = acc.generate_pass(randint(8,12))  # generate random pass

		sms_code = acc.login(name, passw, name.replace(" ", "")	+"@byom.de")  # send name, passwd and name+mail ( to temp mailer )

		if not sms_code:
			return 0

		acc.sms_check(sms_code)  # send mail and get code

		acc.generate_num(argv2.lower())  # sms receive and send stuff

		save = "\033[1;32;40m[*] Created Account\033[0m " + name.replace(" ", "").replace("\n","") +"@byom.de" + ":" + passw + "\n"

		print(save)
		with open("accounts.txt", "a") as l:
			l.writelines(save)


		partner = acc.generate_name()  # wedding form partner name

		acc.FillWedding(name.split(" ")[0], name.split(" ")[1], partner.split(" ")[0], partner.split(" ")[1])  # Fill wedding form

		acc.BabyReg()  

if __name__ == "__main__":

	countries = []
	with open("deps/phones.txt") as f:  # get countries, country ID and amazon phone list html id
		for i in f.readlines():
			countries.append(i.split(",")[0])

	if len(argv) != 3:
		print("python3 leech.py REF COUNTRY")
		exit()

	if not argv[2] in countries:
		print("python3 leech.py REF COUNTRY")
		exit()

	while 1:
		try:

			GetRewards.main(argv[1], argv[2])
		except InvalidSelectorException as e:
			print("Error in selector!-> \033[0;31;47m" + str(e) + "\033[0m")
			exit()
		except Exception as e:
			print("Error! -> \033[0;31;47m" + str(e) + "\033[0m")
			exit()
