import requests, json, sys, os.path, pickle
#from geopy.geocoders import Nominatim
import geopy

users_file_name = "users.pickle"


def startApp():
	while True:
		welcomeMessage = """
	Welcome to Weather Information
	Please select your option:

	1 -> Register New User
	2 -> Update User Information
	3 -> View Registered Users
	4 -> Get Weather Information
	6 -> Exit

	"""

		print(welcomeMessage)


		menuChoice = input()

		if menuChoice == '1':
			registerNewUser()

		elif menuChoice == '2':
			updateUserInfo()

		elif menuChoice == '3':
			viewRegisteredUsers()

		elif menuChoice == '4':
			getWeatherInfo()


		elif menuChoice == '6':
			sys.exit()


		else:
			print("Invalid Option Selected..\nPlease try again...")






def updateUserInfo():
	## Check if the storage file has been created already before commencing on update...
	if not os.path.exists(users_file_name):
		## The users.pickel file does not exist...
		print("No user to update")
	else:
		## The users.pickel file exists...
		with open(users_file_name, 'rb') as users:
			users = pickle.load(users)
		
		print("Enter email of the user or (X) to cancel:")
		email = input()
		
		for user in users:
			if email == user["email"]:
				## The user does exists...
				print('''
Enter the number of the data you want to update?
1 -> For title
2 -> For firstname
3 -> For lastname
4 -> To exit''')
				userInput = input()

				if userInput == "1":
					startUpdate("title", user, users)
					break
				elif userInput == "2":
					startUpdate("firstname", user, users)
					break
				elif userInput == "3":
					startUpdate("lastname", user, users)
					break
				elif userInput == "4":
					## The user wants to exit...
					sys.exit()
				else:
					print("Incorrect input!")
					updateUserInfo()
			elif email.upper() == "X":
				startApp()
		else:
			## The user does not exists...
			print("User does not exist!")
			updateUserInfo()



def startUpdate(choice, user, db):
	## The user wants to update the firstname...
	print("Are you sure? (Y/N):")
	sure = input().upper()
	if sure == "Y":
		if choice == "title":
			## User wants to update the title...
			print("""
Enter the number of your desired choice:
1 -> Mr
2 -> Mrs
3 -> Miss
4 -> Master
			""")
			userChoice = input()

			try:
				userChoiceInt = int(userChoice)
			except ValueError as err:
				print("Invalid input, the input must be an integer: ", err)
			else:
				if isinstance(int(userChoiceInt), int):
					if userChoice == "1":
						updateData("title", "Mr", user, db)
					elif userChoice == "2":
						updateData("title", "Mrs", user, db)
					elif userChoice == "3":
						updateData("title", "Miss", user, db)
					elif userChoice == "4":
						updateData("title", "Master", user, db)
					else:
						print("Incorrect Input!")
				else:
					print("Input must be an Integer!")

			
		else:
			## The user is sure, so get the new data from the User, verify the user input and update the data...
			print("Enter the new " + choice + ":")
			userInput = input()

			if verifyInputForString(userInput):
				updateData(choice, userInput, user, db)
			else:
				print("Inpiut must be a string!")
	elif sure == "N":
		updateUserInfo()
	else:
		print("Incorrect input! Try again.")
		updateUserInfo()





def verifyInputForString(userInput):
	if isinstance(userInput, str):
		## Variable is a string...
		return True
	else:
		## variable is not a string...
		return False


def updateData(data, userInput, user, db):
	## variable is a string...
	userInput = userInput.capitalize()

	user[data] = userInput

	print("Updating Users " + data + "...")

	pickle.dump((db), open(users_file_name, "wb"))
	print("User's " + data + " updated successfully!")












def viewRegisteredUsers():
	## check if the storage file has been created already..
	if not os.path.exists(users_file_name):
		print("No user has been registered")
	else:
		with open(users_file_name, 'rb') as stored_users:
			stored_users = pickle.load(stored_users)

			#print(stored_users)
			#print ("%-10s" % (stored_users))
			count = 1
			print(" --- Current Registered Users --- \n")
			for stored_user in stored_users:
				count = str(count)
				print("[" + count + "]" + " -> " + str(stored_user) + "\n")
				count = int(count)
				count =  count + 1



def get_saved_users():

	if not os.path.exists(users_file_name):
		return None
	with open(users_file_name, 'rb') as users_file:
		users = pickle.load(users_file)
		return users


def checkUserExists(new_user, saved_users):
	##use the email for checking..
	email = new_user['email']

	for saved_user in saved_users:
		if email == saved_user['email']:
			# there is a match
			return True #the user exists..
	else:
		return False  #the user does not exist


def createUsersStorage(index_user = None):

	if index_user !=  None:
		pickle.dump( (index_user), open( users_file_name, "wb" ) )

	return True



def register_random_user(user_gender ='random'):
	if user_gender == 'random':
		api_request = "http://randomuser.me/api"
	elif user_gender == 'male':
		api_request = "http://randomuser.me/api/?gender=male"
	elif user_gender == 'female':
		api_request = "http://randomuser.me/api/?gender=female"
	else:
		api_request = "http://randomuser.me/api"

	#connect to the the randomUser API..
	#get a random user..
	result = requests.get(api_request)
	result = json.loads(result.text)
	result = result['results']
	#print(result)
	## Collects biodata information..
	#name, gender, title, location...
	title = result[0]['name']['title']
	firstname = result[0]['name']['first']
	lastname = result[0]['name']['last']

	location = result[0]['location'] 
	email = result[0]['email']	

	new_user = {
		'title': title, 
		'firstname': firstname,
		'lastname': lastname,
		'location': location,
		'email': email
		}

	## save this to the 
	## check if this user exists already...
	saved_users = get_saved_users()

	if saved_users == None:
		## theres no storage system at the moment .
		# create one ..
		# this is the first user..
		stored_users = []
		stored_users.append(new_user)
		if createUsersStorage(stored_users):
			print("New User Added")

	else:
		#check this file..
		#open the file for reading..
		#check if this user has been registered already..
		check_result = checkUserExists(new_user, saved_users)
		if check_result == True:
			#restart the process..
			register_random_user(user_gender)
		else:
			## register this user ..
			with open(users_file_name, "rb") as old_users:
				old_users_data = pickle.load(old_users)

				##push the new user ..
				old_users_data.append(new_user)

				#save back..
				pickle.dump( (old_users_data), open( users_file_name, "wb" ) )
				print("New User Added!")



def register_specific_user():
	firstname = input("Enter first name: ")
	lastname = input("Enter last name: ")
	title = input("Enter a title, e.g. Mr, Mrs, etc: ")
	email = input("Enter your email: ")
	##location is made up of ..
	"""
	{'street': {'number': 8713, 'name': 'George Street'}, 'city': 'Peterborough', 'state': 'Humberside', 'country': 'United Kingdom', 'postcode': 'L67 6BQ', 'coordinates': {'latitude': '6.0802', 'longitude': '25.5223'}, 'timezone': {'offset': '+3:30', 'description': 'Tehran'}}

	"""
	street_num = input("Enter your street number: ").strip()
	street_name = input("Enter your street name: ").strip()
	city = input("Enter your city: ").strip()
	state = input("Enter state: ").strip()
	postcode = input("Enter postcode: ").strip()
	country = input("Enter country: ").strip()

	#get the coordinates ..
	#geolocator = Nominatim(user_agent="APISTest1")

	default_address = "UPDC Estate, Lekki, Lagos state, Nigeria"

	g = geopy.geocoders.GoogleV3(api_key='Put Your Google API Key here')


	location = g.geocode(street_num + " "+ street_name + "street, " + city + ", " + state + ", " + country + ".")

	## We will be using the: 
	# - coordinates (longitude and latitude )
	# - 
	
	if location == None:
		#the information for the given location is not availabe..
		location = g.geocode(default_address)

	longitude = location.longitude
	latitude = location.latitude 

	complete_location = {'street': {'number': street_num, 'name': street_name}, 'city': city, 'state': state, 'country': country, 'postcode': postcode, 'coordinates': {'latitude': latitude, 'longitude': longitude}, 'timezone': {'offset': None, 'description': None}}


	## prepare the new user ..
	new_user = {
		'title': title, 
		'firstname': firstname,
		'lastname': lastname,
		'location': complete_location,
		'email': email
	}

	## save this to the 
	## check if this user exists already...
	saved_users = get_saved_users()
	if saved_users == None:
		## theres no storage system at the moment .
		# create one ..
		# this is the first user..
		stored_users = []
		stored_users.append(new_user)
		if createUsersStorage(stored_users):
			print("New User Added")
	else:
		#check this file..
		#open the file for reading..
		#check if this user has been registered already..
		check_result = checkUserExists(new_user, saved_users)
		if check_result == True:
			#restart the process..
			register_specific_user()
		else:
			## register this user ..
			with open(users_file_name, "rb") as old_users:
				old_users_data = pickle.load(old_users)

				##push the new user ..
				old_users_data.append(new_user)

				#save back..
				pickle.dump( (old_users_data), open( users_file_name, "wb" ) )
				print("New User Added!")




	
		


def registerNewUser():
	print("Do you want to register a random user or enter a new one?")
	print("-> Yes Male(YM): Register Random male user")
	print("-> Yes Female (YF): Register Random female user")
	print("-> Yes(Y): Registers Random user")
	print("-> No(N): Enter user data")
	print("-> X: Go back to the main menu")

	register_method = input()

	if register_method.upper() == 'Y' or register_method.upper() == 'Yes':
		print("Generating a random user ...")
		register_random_user()

					

	elif register_method.upper() == 'YES MALE' or register_method.upper() == 'YM':
		print("Generating a random male user ...")
		register_random_user('male')


	elif register_method.upper() == 'YES FEMALE' or register_method.upper() == 'YF':
		print("Generating a random female user ...")
		register_random_user('female')

	elif register_method.upper() == 'NO' or register_method.upper() == 'N':
		print("Enter new user data: ")
		register_specific_user()


	elif register_method.upper() == 'X':
		print("go back to the main menu")



def getWeatherInfo():
	##get the registered users ..
	saved_users = get_saved_users()

	counter = 1
	virtual_mem = []
	index = 0
	print("Please select the User code number to get the weather information: ")
	for saved_user in saved_users:
		counter = str(counter)
		virtual_dict = {
			counter : saved_user
		}
		virtual_mem.append(virtual_dict)
		print( "[" +counter + "] -> " + virtual_mem[index][counter]['title'] + " " + virtual_mem[index][counter]['firstname'] + ", " +virtual_mem[index][counter]['lastname']  + " [ email: " + virtual_mem[index][counter]['email'] + "]" )
		counter = int(counter)
		counter = counter + 1
		index = index + 1

	print("\n")
	userCodeChoice = input("Enter code number: ")

	computeChoice = int(userCodeChoice) - 1

	try:
		selectedUser = virtual_mem[computeChoice]

		## get the weather info..
		weather_call = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API KEY HERE}")
		weather_call = json.loads(weather_call.text)
		#print(weather_call)
		# Get the min temperature::
		temp = weather_call['list'][0]['main']['temp']
		temp_min = weather_call['list'][0]['main']['temp_min']
		temp_max = weather_call['list'][0]['main']['temp_max']
		pressure = weather_call['list'][0]['main']['pressure']
		current_weather = weather_call['list'][0]['weather'][0]['main']
		current_weather_description = weather_call['list'][0]['weather'][0]['description']
		current_date_queried = weather_call['list'][0]['dt_txt'];
		feels_like = weather_call['list'][0]['main']['feels_like']

		weather_info = """ --- Weather Information Result --- \n"""

		weather_info += " -> Temperature: " + str(temp) + "\n"
		weather_info += " -> Maximum Temperature: " + str(temp_max) + "\n"
		weather_info += " -> Minimum Temperature: " + str(temp_min) + "\n"
		weather_info += " -> Pressure: " + str(pressure) + " Feels like: " + str(feels_like) + "\n"
		weather_info += " -> Current Weather: "+ str(current_weather) + "\n"
		weather_info += " -> Current Weather Description: "+ str(current_weather_description) + "\n"
		weather_info += " -> Date Queried: " + str(current_date_queried)


		print(weather_info)


	except :
		print("Invalid User code entered.\nTry again: ")
		getWeatherInfo()
	





	




	




#starts the application..
startApp()









