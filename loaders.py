from classes import User, Item

class MovieLensLoader(object):
	"""
	Loads data from the MovieLens dataset into users and items directories.
	"""
	def __init__(self, path, dataset = "\u.data"):
		self.users = self.__load_users(path, dataset)
		self.items = self.__load_items(path)

	def __load_users(self, path, dataset):
		users = {}
		with open(path + "\u.user") as f:
			for line in f:
				userdata = line.rstrip().split("|")
				users[int(userdata[0])] = User(*userdata)

		with open(path + "\\" + dataset) as f:
			for line in f:
				userid, itemid, rating, timestamp = line.split("\t")
				users[int(userid)].ratings[int(itemid)] = float(rating)
		
		return users

	def __load_items(self, path):
		items = {}
		with open(path + "\u.item") as f:
			for line in f:
				values = line.rstrip().split("|")
				itemdata = values[:5]
				itemdata.append(values[-19:]) # Genres
				items[int(itemdata[0])] = Item(*itemdata)
		
		return items

class EachMovieLoader(object):
	"""
	Loads data from the EachMovie dataset into users and items directories.
	"""
	def __init__(self, path):
		self.users = self.__load_users(path)
		self.items = self.__load_items(path)

	def __load_users(self, path):
		users = {}
		with open(path + "\Person.txt") as f:
			for line in f:
				userdata = line.rstrip().split("\t")
				userid = int(userdata[0])
				try:
					age = userdata[1]
				except:
					age = 0

				try:
					gender = userdata[2]
				except:
					gender = "N/A"

				occupation = "N/A"

				try:
					zip_code = userdata[3]
				except:
					zip_code = "N/A"

				users[userid] = User(userid, age, gender, occupation, zip_code)

		with open(path + "\Vote.txt") as f:
			for line in f:
				data = line.split("\t")
				userid = int(data[0])
				itemid = int(data[1])
				rating = float(data[2])*5
				weight = float(data[3])

				if weight == 1.0:
					users[userid].ratings[itemid] = rating

		return users

	def __load_items(self, path):
		items = {}
		with open(path + "\Movie.txt") as f:
			for line in f:
				values = line.rstrip().split("\t")
				itemdata = values[:5]
				itemdata.append(values[-19:]) # Genres
				items[int(itemdata[0])] = Item(*itemdata)
		
		return items

class NetflixLoader(object):
	pass