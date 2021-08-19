import requests
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

from fake_useragent import UserAgent
from random import choice, randint
from string import ascii_letters, punctuation, digits

from smsman import smsman
from smsman.errors import WrongTokenError



class CreateAccount:

	def __init__(self, AmazonID):

		self.useragent = UserAgent()

		self.myID = AmazonID



		with open("src/CONFIG", "r") as k:
			API = k.read().replace('\n', '').split("API=")[1].split("proxy")[0]
			self.api_key = API
			
		self.country_id_dict = {} # dict with phone id of sms man and amazon

		self.myphone_number = ""
		
		self.code = ""  # SMS code
		
		self.client = smsman.Smsman(self.api_key)

		self.name = '//*[@id="ap_customer_name"]'  # Login Customer Name

		self.mail = '//*[@id="ap_email"]'  # Login Customer Mail

		self.passwd = '//*[@id="ap_password"]'  # Login Customer Pass

		self.check_passwd = '//*[@id="ap_password_check"]'  # Login Customer Pass Check

		self._create_acc = '//*[@id="continue"]'  # (create account button) 

		#-----------------------------------   ( here captcha pop up, manual procedure )

		self.captcha = '//*[@id="cvf-input-code"]'


		self._nextbutton = '//*[@id="cvf-submit-otp-button"]/span/input' # ( click )

		#-----------------------------------

		self.phone = '/html/body/div[1]/div[2]/div/div/div/div/div/div/form/div[1]/div/div[2]/div/div[2]/input' # Phone Form

		self._phoneclick = '/html/body/div[1]/div[2]/div/div/div/div/div/div/form/span/span/input'  # Phone Form button


		#-----------------------------------


		self.mail_validation = "cvf-input-code"  # mail Form
		self.mail_validation_recovery = '//*[@id="cvf-input-code"]'  # If previus ID dont work use XPATH
		self._mail_validation = "/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[7]/span/span/input"  # mail button
		self._mail_validation_recovery = "a-button-input"

		# ---------------

		self.smscode = '/html/body/div[1]/div[2]/div/div/div/div/div/form/div[1]/div[5]/input'  # Mail code input form
		self.smscode_recovery = "code"
		self._smsbutton = '/html/body/div[1]/div[2]/div/div/div/div/div/form/div[1]/span/span/input' # Mail code input button
		self._smsbutton_recovery = 'cvf_action'


		# ----------------------------------- WEDDING FORM -----------------------------------


		self.FbuttonID = '/html/body/div[1]/div[2]/div/div/div/div[1]/div/a'  # Wedding Form Button

		self.Fname = '//*[@id="wr-create-registry"]/div/div[2]/div[1]/div[1]/div[2]/input'

		self.FSName = '//*[@id="wr-create-registry"]/div/div[2]/div[1]/div[2]/div[2]/input'

		self.ParthName = '//*[@id="wr-create-registry"]/div/div[2]/div[2]/div[1]/div[2]/input'

		self.PathFSName = '//*[@id="wr-create-registry"]/div/div[2]/div[2]/div[2]/div[2]/input'

		self.RButton1 = ['/html/body/div[1]/div[2]/div/div[2]/div[1]/div[3]/div[2]/span[1]/span/input', '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[3]/div[2]/span[2]/span/input', '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[3]/div[2]/span[3]/span/input']  #  3 button routes, choice random and click

		self.month = '//*[@id="wr-cm-event-date-month_RAND"]' # random month click
		self.day = '//*[@id="wr-cm-event-date-day_RAND"]' # random day click
		self.year = '//*[@id="wr-cm-event-date-year_RAND"]'  # random year click
		self.city = '//*[@id="wr-create-registry"]/div/div[2]/div[9]/div[2]/div[2]/div/div/input' #random spain city
		self.number = '//*[@id="wr-cm-event-guests-number"]'# -> random number
		self.cities = ["Malaga", "Madrid", "cadiz", "barcelona", "vigo", "bilbao"]  # Spain cities
		
		# -------- Location form ------

		self.addnew = "/html/body/div[1]/div[2]/div/div[2]/div[4]/div/div[2]/div/span/span/input"  # add new direction button

		self.location_myname = '//*[@id="address-ui-widgets-enterAddressFullName"]'
		self.cellphone = "address-ui-widgets-enterAddressPhoneNumber"
		self.address1 = '//*[@id="address-ui-widgets-enterAddressLine1"]'
		self.address2 = '//*[@id="address-ui-widgets-enterAddressLine2"]'
		self.postal = "address-ui-widgets-enterAddressPostalCode"
		self.poblation = "address-ui-widgets-enterAddressCity"
		self.province = "address-ui-widgets-enterAddressStateOrRegion"
		self.defaultt = "address-ui-widgets-use-as-my-default" #  check use as default button

		self.sendall = "/html/body/div[5]/div/div/div/form/span/div/span/span/span/input"  # send direction form


		# random UA

		profile = webdriver.FirefoxProfile()
		profile.set_preference("general.useragent.override", self.useragent.random)

		with open("src/CONFIG", "r") as f:
			proxy = f.read().replace('\n', '').split("proxy=")[1]  # get proxy=value from CONFIG
			if proxy.lower() == "true":
				hide = True
		hide = False
		if hide:  # if "proxy=True" in CONFIG
			myProxy = ""
			with open("deps/proxy.txt", "r") as m:
				myProxy = choice(m.readlines())

			proxy = Proxy({
	    		'proxyType': ProxyType.MANUAL,
	    		'httpProxy': myProxy,
	    		'ftpProxy': myProxy,
	   			'sslProxy': myProxy,
	   		 	'noProxy': ''
	  		  })



			self.browser = webdriver.Firefox(proxy=proxy, firefox_profile=profile)
		else:
			self.browser = webdriver.Firefox(firefox_profile=profile)

		# random screen size, get error
		
		"""
		#self.resolution_list = ["1920x1080", "1366x768", "1440x900", "1536x864","2560x1440","1680x1050","1280x720","1280x800","360x640","1600x900"]
		#resolution = choice(self.resolution_list)
		#width, height = resolution.split("x")
		#self.browser.set_window_size(width, height) 
		
		"""

		self.browser.get("https://www.amazon.es/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2F%3F_encoding%3DUTF8%26ref_%3Dnav_custrec_newcust&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")  # create account link
	
	def interact(self, type, locat, send, click, object_client):  # fill form and click [type of locator for html(xpath,ID), Button of form route, click or send text? (1/0), browser object created by Webdriver
	
		if click:
			object_client.find_element(type, locat).click()
		else:
			try:
				object_client.find_element(type, locat).clear()
			except:
				pass
			object_client.find_element(type, locat).send_keys(send)
		return 0

	def login(self, name, passwd, tempmail):  # Basic info
		self.interact(By.XPATH, self.name, name, 0, self.browser)
		self.interact(By.XPATH, self.mail, tempmail, 0, self.browser)
		self.interact(By.XPATH, self.passwd, passwd, 0, self.browser)
		self.interact(By.XPATH, self.check_passwd, passwd, 0, self.browser)

		self.interact(By.XPATH, self._create_acc, 1, 1, self.browser)
		return self.listener_mail(tempmail)

	def send_code(self, code):
		self.interact(By.XPATH, self.captcha, code, 0, self.browser)

		self.interact(By.XPATH, self._nextbutton, 1, 1, self.browser)

	def phone_verify(self, phone):
		self.interact(By.XPATH, self.phone, phone, 0, self.browser)

		self.interact(By.XPATH, self._phoneclick, 1, 1, self.browser)

	def sms_check(self, sms):
		try:
			self.interact(By.ID, self.mail_validation, sms, 0, self.browser)
		except:
			self.interact(By.XPATH, self.mail_validation_recovery, sms, 0, self.browser)
		try:
			self.interact(By.XPATH, self._mail_validation, 1, 1, self.browser)

		except:
			self.interact(By.CLASS_NAME, self._mail_validation_recovery, 1, 1, self.browser)

	def remove_line(self, lineToSkip):  # this func remove line of file by index, remove used names from names.txt
	    """ Removes a given line from a file """
	    with open("deps/names.txt",'r') as read_file:
	        lines = read_file.readlines()

	    currentLine = 1
	    with open("deps/names.txt",'w') as write_file:
	        for line in lines:
	            if currentLine == lineToSkip:
	                pass
	            else:
	                write_file.write(line)
		
	            currentLine += 1

	def generate_name(self):  # get random name
			
		with open("deps/names.txt", "r") as f:
			lists = f.readlines()
			name = choice(lists)
			self.remove_line(lists.index(name))
		return name

	def generate_pass(self, length):

		characters = ascii_letters + digits + punctuation

		result_str = ''.join(choice(characters) for i in range(length))

		return result_str

	def listener_mail(self, name):  # gets mail verification code, name= Customer Name
		name = name.replace("@byom.de", "").lower()
		
		options = webdriver.FirefoxOptions()

		options.add_argument('-headless')

		self.mailweb = webdriver.Firefox(options=options)

		self.mailweb.get("https://www.byom.de/")

		self.interact(By.XPATH, '//*[@id="main-search"]', name, 0, self.mailweb)

		self.interact(By.XPATH, '//*[@id="main-search-button"]', 1, 1, self.mailweb)

		while not "Amazon" in self.mailweb.page_source:
			try:
				self.interact(By.ID, 'refresh', 1, 1, self.mailweb)
			except:
				sleep(2)
				self.interact(By.ID, 'refresh', 1, 1, self.mailweb)


		self.interact(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]/td[2]', 1, 1, self.mailweb)

		self.mailweb.switch_to.frame(self.mailweb.find_element(By.ID, 'mail-html-iframe'));  # avoid iframe in mail web

		mail_code = self.mailweb.find_element(By.XPATH, '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/p[2]').text

		self.mailweb.close()

		return mail_code

	def receive_sms(self, request_id):  # used in generate_num, trying until success of fail
		try:
			self.code = self.client.get_sms(request_id)
			return True
		except Exception as e:
			print(e)
			return False

	def request(self,country_ids):  # return application ID and Phone number w/prefix, no "+"
		return self.client.request_phone_number(country_id=int(country_ids), application_id=176)

	def generate_num(self, country_name):
		with open("deps/phones.txt") as f:
			for i in f.readlines():
				csv = i.split(",")
				self.country_id_dict[csv[0]] = [csv[1], csv[2].replace("\n","")]
		
		countries = []
		with open("deps/phones.txt") as f:  # get countries, country ID and amazon phone list html id
			for i in f.readlines():
				countries.append(i.split(",")[0])

		while True:  # until no phone number try w/ different countries
			country_id, list_number  = self.country_id_dict[country_name]
			try:
				request_id, self.myphone_number = self.request(country_id)

				self.interact(By.ID, "cvf_phone_cc_aui", 1, 1, self.browser)
				self.interact(By.ID, "cvf_phone_cc_native_" + list_number, 1, 1, self.browser)
				break
				
			except WrongTokenError as e:
				print("\033[0;31;47mError in API!\033[0m-> " + str(e)) # mientras no haya numeros ejecuta
				
				if not "No numbers" in str(e):
					exit()


				countries.remove(country_name)
				
				if not len(countries):
					print("No more countries...")
					exit()

				country_name = choice(countries)
				print("\033[1;32;40m[*] Trying\033[0m " + country_name)

			except Exception as e:
				print("Error in SMS receive, but token related OK: " + str(e))
				exit()





		if country_name not in ["portugal", "irlanda"]:  # those countries have long prefix ( 3 ), cant send phone to amazon in wrong format
			self.interact(By.XPATH, self.phone, self.myphone_number[2:], 0, self.browser)
		else:
			self.interact(By.XPATH, self.phone, self.myphone_number[3:], 0, self.browser)

		self.interact(By.XPATH, self._phoneclick, 1, 1, self.browser)
		
		counter = 0
		while(True):
			if self.receive_sms(request_id):
				break
			else:
				if counter == 5:
					self.code = input("sms-man.com SMS code> ")
					break
				counter += 1
				sleep(2)
				continue

		try:
			self.interact(By.XPATH, self.smscode, self.code, 0, self.browser)
		except:
			self.interact(By.CLASS_NAME, self.smscode_recovery, self.code, 0, self.browser)

		try:
			self.interact(By.XPATH, self._smsbutton, 1, 1, self.browser)
		except:
			self.interact(By.CLASS_NAME, self._smsbutton_recovery, 1, 1, self.browser)


		try:
			self.interact(By.XPATH, self.sendall, 1, 1, self.browser)
			sleep(1)
			self.interact(By.XPATH, self.sendall, 1, 1, self.browser)
			sleep(1)
			self.interact(By.XPATH, self.sendall, 1, 1, self.browser)
		except:
			pass

	def BabyReg(self):  # fill baby form
		input("Send form and continue> ")
		self.browser.get("http://www.amazon.es/baby-reg/homepage?tag=" + self.myID)


		try:
			self.interact(By.ID, "a-autoid-2-announce", 1, 1, self.browser)
		except:
			sleep(1)
			self.interact(By.ID, "a-autoid-2-announce", 1, 1, self.browser)


		self.interact(By.ID, "arrivalDate-d", 1, 1, self.browser)
		self.interact(By.ID, "arrivalDate-d-native_" + str(randint(0,29)), 1, 1, self.browser)
		# arrivalDate-m random month

		self.interact(By.ID, "arrivalDate-m", 1, 1, self.browser)
		self.interact(By.ID, "arrivalDate-m-native_" + str(randint(8,11)), 1, 1, self.browser)

		#  ( year )
		self.interact(By.ID, "arrivalDate-y", 1, 1, self.browser)
		self.interact(By.ID, "arrivalDate-y-native_2", 1, 1, self.browser)

		try:
			self.interact(By.ID, "br-address-selection-dropdown", 1, 1, self.browser)
			self.interact(By.ID, "address-list_0", 1, 1, self.browser)
		except:
			sleep(1)
			self.interact(By.ID, "dps address-list_0", 1, 1, self.browser)


		input("Captcha> ")

		self.interact(By.ID, "a-autoid-0-announce", 1, 1, self.browser)

		sleep(3)

		self.browser.close()

	def FillWedding(self, name, Surname, ParnerName, ParnerSurName):

		try:
			self.browser.find_element(By.ID, "sp-cc-accept").click()
		except:
			pass
			
		self.browser.get("http://www.amazon.es/wedding?tag=" + self.myID)
		try:
			self.browser.find_element(By.ID, "sp-cc-accept").click()
		except:
			pass

		self.interact(By.XPATH, self.FbuttonID, 1, 1, self.browser)
		sleep(1)
		self.interact(By.XPATH, self.Fname, name, 0, self.browser)
		self.interact(By.XPATH, self.FSName, Surname, 0, self.browser)
		self.interact(By.XPATH, self.ParthName, ParnerName, 0, self.browser)
		self.interact(By.XPATH, self.PathFSName, ParnerSurName, 0, self.browser)
		self.interact(By.XPATH, choice(self.RButton1), 1, 1, self.browser)

		city = choice(self.cities)
		# ------ add direccion --------	
		try:
			self.browser.find_element(By.ID, "sp-cc-accept").click()
		except:
			pass

		self.interact(By.XPATH, self.addnew, 1, 1, self.browser)
		try:
			self.interact(By.XPATH, self.location_myname, name + " " + Surname, 0, self.browser)
		except:
			sleep(1)
			self.interact(By.XPATH, self.location_myname, name + " " + Surname, 0, self.browser)

		self.interact(By.ID, self.cellphone, self.myphone_number[-9:], 0, self.browser)

		with open("deps/names.txt", "r") as f:
			word = choice(f.readlines()).split(" ")[0]

		self.interact(By.XPATH, self.address1, "Calle " + word + " numero " + str(randint(1,15)), 0, self.browser)

		line2 = choice(["piso", "edificio", "apartamento"]) + " numero " + str(randint(1,10))

		self.interact(By.XPATH, self.address2, line2, 0, self.browser)
		self.interact(By.ID, self.postal, randint(11111,99999), 0, self.browser)
		self.interact(By.ID, self.poblation, city, 0, self.browser)
		self.interact(By.ID, self.province, city, 0, self.browser)
		try:
			self.interact(By.XPATH,  self.defaultt, 1, 1, self.browser)
		except:
			pass

		self.interact(By.XPATH, self.sendall, 1, 1, self.browser)

		try:
			self.interact(By.XPATH, self.sendall, 1, 1, self.browser)
			sleep(1)
			self.interact(By.XPATH, self.sendall, 1, 1, self.browser)
		except:
			pass

		# --------------
		
		self.interact(By.ID, 'a-autoid-7-announce', 1, 1, self.browser)

		self.interact(By.ID, "wr-cm-event-date-month_" + str(randint(0,11)), 1, 1, self.browser)


		self.interact(By.ID, "a-autoid-8-announce", 1, 1, self.browser)
		self.interact(By.ID, "wr-cm-event-date-day_" + str(randint(0,29)), 1, 1, self.browser)

		self.interact(By.ID, "a-autoid-9-announce", 1, 1, self.browser)
		self.interact(By.ID, "wr-cm-event-date-year_" + str(randint(0,19)), 1, 1, self.browser)

		self.interact(By.XPATH, self.city, city, 0, self.browser)
		self.interact(By.XPATH, self.number, randint(50,1000), 0, self.browser)

