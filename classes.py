class User(object):
	def __init__(self, userid, age = None, gender = None, occupation = None, zip_code = None):
		self.userid = int(userid)
		self.age = int(age)
		self.gender = gender
		self.occupation = occupation
		self.zip_code = zip_code
		self.ratings = {}

	def pearson_correlation(self, p2):
		p1, p2 = self.ratings, p2.ratings
		ratings_in_common = [item for item in p1 if item in p2]

		num_ratings_in_common = len(ratings_in_common)
		if num_ratings_in_common == 0:
			return 0

		sumx = sum(p1[x] for x in ratings_in_common)
		sumy = sum(p2[x] for x in ratings_in_common)
		
		sqx = sum([p1[x]**2 for x in ratings_in_common])
		sqy = sum([p2[x]**2 for x in ratings_in_common])

		#Other Example - Might be easier to understand:
		"""
		user1_avg = sumx/num_ratings_in_common
		user2_avg = sumy/num_ratings_in_common
		num = sum([(p1[x]-user1_avg) * (p2[x]-user2_avg) for x in ratings_in_common])
		"""

		tot = sum([p1[x]*p2[x] for x in ratings_in_common])
		num = tot - (sumx * sumy/num_ratings_in_common)
		den = pow((sqx - pow(sumx, 2)/num_ratings_in_common) * (sqy - pow(sumy, 2)/num_ratings_in_common), 0.5)

		if den == 0:
			return 0.0

		return num/den

	def manhattan_distance(self, p2):
		return sum([abs(self.ratings[x]-p2.ratings[x]) for x in self.ratings if x in p2.ratings])

	def __mean_vote(self):
		return sum(self.ratings.values())/len(self.ratings.values())

	def normalized_vote(self, item):
		try:
			return self.ratings[item.movieid] - self.__mean_vote()
		except KeyError:
			return False

	def __repr__(self):
		return "<User - ID: {}>".format(self.userid)

class Item(object):
	GENRES = ["unknown", "Action", "Adventure", "Animation", "Children's", 
	"Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film Noir", 
	"Horror", "Musical", "Mystery", "Romance", "Romance", "Sci-Fi", "Thriller",
	"War", "Western"]

	def __init__(self, movieid, title = None, release_date = None, video_release_date = None, imdb_url = None, genres = None):
		self.movieid = int(movieid)
		self.title = title
		self.release_date = release_date
		self.video_release_date = video_release_date
		self.imdb_url = imdb_url
		if genres != None:
			self.genres = dict(zip(self.GENRES, genres))

	def __repr__(self):
		return "<Movie - ID: {}>".format(self.movieid)

class Predictor(object):
	def __init__(self, users, items):
		self.users = users
		self.items = items

	def predict_rating(self, user, item):
		other_users = [us for us in self.users.values() if us.userid != user.userid and item.movieid in us.ratings]
		n, y = 0.0, 0.0

		for u in other_users:
			other_user_ratings_in_common = [v for k,v in u.ratings.iteritems() if k in user.ratings]
			
			if len(other_user_ratings_in_common) < 1:
				continue

			other_user_avg_rating = sum(other_user_ratings_in_common)/len(other_user_ratings_in_common)

			n += (u.ratings[item.movieid] - other_user_avg_rating) * user.pearson_correlation(u)
			y += abs(user.pearson_correlation(u))

		# Don't know what should be returned if n or y equals 0.
		if n == 0 or y == 0:
			predicted_rating = 3
		else:
			predicted_rating = sum(user.ratings.values())/len(user.ratings) + (n/y)

		return predicted_rating